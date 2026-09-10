#!/usr/bin/env python3
"""Reconcile the append-only session ledger with all saved raw evidence; no inference."""
import argparse,csv,hashlib,json
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from overseeing.domain import digest
from overseeing.io import read_events,write_json
from overseeing.research_analysis import historical_file_status


def audit(root):
    root=Path(root);auth=json.loads((root/'authorization.json').read_text());freeze=json.loads((root/'evaluation_freeze.json').read_text())
    events=read_events(root/'ledger.jsonl');calls={};attempts={}
    start=datetime.fromisoformat(auth['started_utc']);cutoff=datetime.fromisoformat(auth['inference_cutoff_utc'])
    for e in events:
        assert start<=datetime.fromisoformat(e['wall_utc'])<cutoff
        if e['kind']=='call_reserved':
            assert e['call_id'] not in calls;calls[e['call_id']]=e
        else:
            assert e['kind']=='attempt_reserved' and e['call_id'] in calls and e['retry'] in (0,1)
            key=(e['call_id'],e['retry']);assert key not in attempts;attempts[key]=e
    assert sorted(calls)==list(range(1,len(calls)+1))
    assert len(calls)<=auth['scheduled_call_limit'] and len(attempts)<=auth['attempt_limit']
    assert len({r['attempt_id'] for r in attempts.values()})==len(attempts)
    raw_paths=list((root/'diagnostics/raw').glob('*.jsonl'))
    for batch in (root/'batches').iterdir():raw_paths+=list((batch/'episodes').rglob('raw_requests.jsonl.gz'))+list((batch/'episodes').rglob('raw_requests.jsonl'))
    seen_calls=set();sent=set();finished={};groups=defaultdict(list)
    for path in sorted(raw_paths):
        for r in read_events(path):
            key=(r['session_call_id'],r['retry']);seen_calls.add(key[0]);reservation=calls[key[0]]
            assert reservation['metadata']=={k:r[k] for k in ('agent_id','job_id','scenario_seed')} and reservation['sample']==r['sample']
            if r['phase']=='inference_started':assert key in attempts and key not in sent;sent.add(key)
            if r['phase']=='attempt_finished':
                assert key not in finished;finished[key]=r
                if 'parsed_action' in r:groups[digest(r['request'])].append(dict(call_id=key[0],sample=r['sample'],action=r['parsed_action'],context=reservation['context']))
    summary=dict(verified_utc=datetime.now(timezone.utc).isoformat(),reserved_scheduled_calls=len(calls),reserved_attempts=len(attempts),logged_scheduled_calls=len(seen_calls),logged_generation_attempts=len(sent),
        finished_attempt_records=len(finished),successful_generations=sum('parsed_action' in r for r in finished.values()),failed_attempts=sum('error' in r for r in finished.values()),retries=sum(r['retry']>0 for r in finished.values()),
        prompt_tokens=sum((r.get('usage') or {}).get('prompt_tokens',0) for r in finished.values()),completion_tokens=sum((r.get('usage') or {}).get('completion_tokens',0) for r in finished.values()),
        unknown_token_attempts=sum(r['inference_request_attempted'] and r.get('usage') is None for r in finished.values())+len(sent-set(finished)),
        unlogged_reserved_calls=sorted(set(calls)-seen_calls),unlogged_reserved_attempts=sorted(set(attempts)-sent),unfinished_attempts=sorted(sent-set(finished)),
        total_declared_scheduled_calls=freeze['total_session_planned_calls'],all_within_authorized_inference_window=True,
        exact_request_groups=len(groups),repeated_request_groups=sum(len(v)>1 for v in groups.values()))
    mixed=[dict(request_hash=h,occurrences=v) for h,v in groups.items() if len({r['action'] for r in v})>1]
    summary.update(mixed_action_groups=len(mixed),mixed_primary_groups=sum(g['occurrences'][0]['sample']==0 for g in mixed),minority_action_occurrences=sum(len(g['occurrences'])-max(sum(v['action']==a for v in g['occurrences']) for a in ('replace_filter','reset_sensor')) for g in mixed))
    d=json.loads((root/'diagnostics/declaration.json').read_text())
    assert len(list((root/'diagnostics/raw').glob('*.jsonl')))==128
    assert digest({k:v for k,v in d.items() if k!='declaration_hash'})==d['declaration_hash']
    for record in d['calls']:
        raw=read_events(root/'diagnostics/raw'/('{:03d}.jsonl'.format(record['execution_index'])))
        assert all(digest(r['request'])==d['prompts'][record['prompt_index']]['request_hash'] for r in raw)
    historical=json.loads((root/'history_hashes.json').read_text())
    lf_path=root/'history_csv_lf_hashes.json';lf=json.loads(lf_path.read_text()) if lf_path.exists() else {}
    states={p:historical_file_status(Path(p).read_bytes(),h,lf.get(p) if p.endswith('.csv') else None) for p,h in historical.items()}
    changed=[p for p,status in states.items() if status=='changed']
    summary.update(historical_files_checked=len(historical),historical_files_changed=changed,historical_csv_line_ending_variations=[p for p,status in states.items() if status=='csv_line_endings'])
    assert not changed
    completed=0;planned=sum(json.loads(p.read_text())['planned_episodes'] for p in (root/'batches').glob('*/declaration.json'))
    for p in (root/'batches').glob('*/analysis/audit.json'):
        a=json.loads(p.read_text());completed+=a['completed_replays']
    summary.update(completed_replayed_episodes=completed,planned_episodes=planned)
    launches=[]
    for p in sorted((root/'launches').glob('*/launch.json')):
        r=json.loads(p.read_text());assert r.get('finished_utc') and datetime.fromisoformat(r['finished_utc'])<=datetime.fromisoformat(auth['deadline_utc']);launches.append(r)
    summary['launches']=launches
    summary['inference_worker_wall_seconds']=sum((datetime.fromisoformat(r['finished_utc'])-datetime.fromisoformat(r['started_utc'])).total_seconds() for r in launches)
    if completed==planned:
        assert len(calls)==freeze['total_session_planned_calls']
        assert not summary['unlogged_reserved_calls'] and not summary['unlogged_reserved_attempts'] and not summary['unfinished_attempts']
    summary['status']='verified'
    write_json(root/'session_request_variation.json',mixed);write_json(root/'session_accounting.json',summary)
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',default='artifacts/stage4_research');args=parser.parse_args();print(json.dumps(audit(args.root),indent=2))
