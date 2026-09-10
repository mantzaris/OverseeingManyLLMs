#!/usr/bin/env python3
"""Reconcile every Stage 5 reservation, raw attempt, clock and historical byte hash."""
from collections import Counter,defaultdict
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.domain import digest
from overseeing.io import read_events,write_json,utc_now


def audit(root):
    root=Path(root);auth=json.loads((root/'authorization.json').read_text())
    ledger=read_events(root/'ledger.jsonl');calls={};attempts={}
    start=datetime.fromisoformat(auth['started_utc']);cutoff=datetime.fromisoformat(auth['inference_cutoff_utc'])
    for entry in ledger:
        assert start<=datetime.fromisoformat(entry['wall_utc'])<cutoff
        if entry['kind']=='call_reserved':
            assert entry['call_id'] not in calls;calls[entry['call_id']]=entry
        else:
            assert entry['kind']=='attempt_reserved' and entry['call_id'] in calls and entry['retry'] in (0,1)
            key=(entry['call_id'],entry['retry']);assert key not in attempts;attempts[key]=entry
    assert sorted(calls)==list(range(1,len(calls)+1));assert len(attempts)<=30000
    sent={};finished={};observed_calls=set();by_batch=defaultdict(Counter);request_groups=defaultdict(list)
    for path in sorted((root/'batches').glob('*/prepared/*/*_raw.jsonl.gz')):
        batch=path.parts[-4]
        for record in read_events(path):
            key=(record['session_call_id'],record['retry']);observed_calls.add(key[0])
            assert record['metadata']==calls[key[0]]['metadata']
            assert record['request_hash']==digest(record['request'])
            assert record['seed']==int(digest(dict(record['metadata'],retry=record['retry']))[:8],16)
            if 'serialized_request' in record:
                wire=json.loads(record['serialized_request']);assert wire==record['request']
                assert list(wire['guided_json']['anyOf'][0]['properties'])==['tool','arguments','confidence']
            if record['phase']=='inference_started':
                assert key in attempts and key not in sent;sent[key]=record
            if record['phase']=='attempt_finished':
                assert key not in finished;finished[key]=record
                by_batch[batch]['finished_attempt_records']+=1
                by_batch[batch]['generation_attempts']+=record['inference_request_attempted']
                by_batch[batch]['successful_generations']+='parsed_call' in record
                by_batch[batch]['failed_attempts']+='error' in record
                by_batch[batch]['retries']+=record['retry']>0
                for k in ('prompt_tokens','completion_tokens'):by_batch[batch][k]+=(record.get('usage') or {}).get(k,0)
                if 'parsed_call' in record:request_groups[record['request_hash']].append(record['parsed_call'])
    assert set(sent)<=set(attempts)
    hist=json.loads((root/'history_hashes.json').read_text())
    # Git normalizes historical CSV line endings. Capture an explicit LF-equivalent
    # hash at authorization; never normalize or accept other historical changes.
    lf_path=root/'history_csv_lf_hashes.json';lf=json.loads(lf_path.read_text()) if lf_path.exists() else {}
    changed=[];normalized=[]
    for name,expected in hist.items():
        raw=Path(name).read_bytes()
        if hashlib.sha256(raw).hexdigest()==expected:continue
        if name in lf and hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()==lf[name]:normalized.append(name)
        else:changed.append(name)
    assert not changed,changed
    cases=json.loads((root/'cases.json').read_text())['cases']
    assert len({c['source_case_group'] for c in cases})==len(cases)
    mixed=[h for h,rows in request_groups.items() if len({digest(r) for r in rows})>1]
    result=dict(status='verified',verified_utc=utc_now(),scheduled_calls=len(calls),generation_attempts=len(attempts),
        logged_generation_attempts=len(sent),successful_generations=sum('parsed_call' in r for r in finished.values()),
        failed_attempts=sum('error' in r for r in finished.values()),retries=sum(r['retry']>0 for r in finished.values()),
        failed_generation_attempts=sum('error' in r and r['inference_request_attempted'] for r in finished.values()),
        failed_preflight_attempts=sum('error' in r and not r['inference_request_attempted'] for r in finished.values()),
        prompt_tokens=sum((r.get('usage') or {}).get('prompt_tokens',0) for r in finished.values()),
        completion_tokens=sum((r.get('usage') or {}).get('completion_tokens',0) for r in finished.values()),
        unknown_token_attempts=sum(r['inference_request_attempted'] and r.get('usage') is None for r in finished.values())+len(set(sent)-set(finished)),
        unlogged_reserved_calls=sorted(set(calls)-observed_calls),unlogged_reserved_attempts=sorted(set(attempts)-set(sent)),
        unfinished_attempts=sorted(set(sent)-set(finished)),by_batch=dict(by_batch),
        historical_files_checked=len(hist),historical_changes=changed,historical_csv_line_endings=normalized,
        exact_request_groups=len(request_groups),repeated_exact_request_groups=sum(len(v)>1 for v in request_groups.values()),
        mixed_exact_request_groups=mixed,distinct_source_cases=len(cases),
        original_start_utc='2026-09-09T15:38:57+00:00',original_target_hours=36)
    def metrics(path,prefix):
        return sum(float(line.rsplit(' ',1)[1]) for line in path.read_text().splitlines() if line.startswith(prefix+'{'))
    if (root/'metrics_after.txt').exists():
        delta={key:metrics(root/'metrics_after.txt',metric)-metrics(root/'metrics_before.txt',metric)
            for key,metric in [('successful_generations','vllm:request_success_total'),('prompt_tokens','vllm:prompt_tokens_total'),('completion_tokens','vllm:generation_tokens_total')]}
        # Successful server generations also include truncated outputs rejected by parsing.
        completed_http=sum(r.get('http_status')==200 for r in finished.values())
        assert delta['successful_generations']==completed_http
        for key in ('prompt_tokens','completion_tokens'):assert delta[key]==result[key]
        result['server_metric_deltas']=delta;result['server_metrics_verified']=True
    write_json(root/'session_accounting.json',result)
    return result

if __name__=='__main__':print(json.dumps(audit(sys.argv[1] if len(sys.argv)>1 else 'artifacts/stage5_practical'),indent=2))
