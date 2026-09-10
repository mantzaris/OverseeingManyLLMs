#!/usr/bin/env python3
"""Read-only input verification and accounting; write audits under Stage 6 only."""
from collections import Counter
from datetime import datetime,timedelta
import csv,hashlib,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.domain import digest
from overseeing.io import read_events,write_json,utc_now
from overseeing.retail.analysis import audit_preparation
from overseeing.retail.risk import RetailRisk

root=Path('artifacts/stage6_robustness');batch=root/'batches/evaluation'
d=json.loads((batch/'declaration.json').read_text());auth=json.loads((root/'authorization.json').read_text())
commit=(root/'freeze_commit.txt').read_text().strip()
assert subprocess.check_output(['git','show',commit+':'+str(batch/'declaration.json')])==(batch/'declaration.json').read_bytes()
commit_time=subprocess.check_output(['git','show','-s','--format=%cI',commit],text=True).strip()
assert digest({k:v for k,v in d.items() if k!='declaration_hash'})==d['declaration_hash']
assert hashlib.sha256((root/'authorization.json').read_bytes()).hexdigest()==d['authorization_sha256']
repairs={r['path']:r for r in json.loads((root/'analysis_direction_repair.json').read_text())['changes']}
presentation={r['path']:r for r in json.loads((root/'presentation_adjustments.json').read_text())['changes']}
allowed=dict(repairs,**presentation)
for name,h in d['source_hashes'].items():
    assert hashlib.sha256((batch/'source'/name).read_bytes()).hexdigest()==h,name
    expected=h
    if name in allowed:
        assert allowed[name]['before_sha256']==h;expected=allowed[name]['after_sha256']
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==expected,name
risk=json.loads((root/'estimator.json').read_text())
assert risk==d['estimator']==json.loads(Path('artifacts/stage5_practical/estimator.json').read_text())
assert RetailRisk.load(risk).estimator_hash==d['estimator_hash']
history=json.loads((root/'historical_hashes.json').read_text())
for name,h in history.items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==h,name
cases=json.loads((root/'cases.json').read_text())['cases']
old_accounts={c['user_id'] for p in Path('artifacts/stage5_practical').glob('cases*.json') for c in json.loads(p.read_text())['cases']}
assert len(cases)==len({c['user_id'] for c in cases})==24
assert not {c['user_id'] for c in cases}&old_accounts
planned={(b['bundle_id'],b['replicate'],s['case_id']) for b in d['bundles'] for s in b['slots']}
prepared=[r for p in sorted((batch/'prepared').glob('*/workflows.json')) for r in json.loads(p.read_text())]
actual=[(r['bundle_id'],r['replicate'],r['case_id']) for r in prepared]
assert len(actual)==len(set(actual)) and set(actual)==planned
prep_audit=audit_preparation(root,'evaluation')
ledger=read_events(root/'ledger.jsonl');calls={};attempts={}
for r in ledger:
    assert datetime.fromisoformat(auth['started_utc'])<=datetime.fromisoformat(r['wall_utc'])<datetime.fromisoformat(auth['inference_cutoff_utc'])
    if r['kind']=='call_reserved':
        assert r['call_id'] not in calls;calls[r['call_id']]=r
    else:
        assert r['kind']=='attempt_reserved' and r['retry'] in (0,1) and r['call_id'] in calls
        key=(r['call_id'],r['retry']);assert key not in attempts;attempts[key]=r
assert sorted(calls)==list(range(1,len(calls)+1))
assert len(calls)<=d['max_scheduled_calls'] and len(attempts)<=d['max_attempts']<=auth['attempt_limit']
assert datetime.fromisoformat(d['created_utc'])<=datetime.fromisoformat(commit_time)<datetime.fromisoformat(calls[1]['wall_utc'])
sent={};finished={};groups={}
for path in sorted((batch/'prepared').glob('*/*_raw.jsonl.gz')):
    for r in read_events(path):
        key=(r['session_call_id'],r['retry'])
        assert r['metadata']==calls[key[0]]['metadata'] and r['metadata']['partition']=='stage6_evaluation'
        assert r['request_hash']==digest(r['request'])
        assert r['seed']==int(digest(dict(r['metadata'],retry=r['retry']))[:8],16)
        if 'serialized_request' in r:assert json.loads(r['serialized_request'])==r['request']
        if r['phase']=='inference_started':assert key in attempts and key not in sent;sent[key]=r
        if r['phase']=='attempt_finished':
            assert key not in finished;finished[key]=r
            if 'parsed_call' in r:groups.setdefault(r['request_hash'],[]).append(digest(r['parsed_call']))
assert set(attempts)==set(sent)=={k for k,r in finished.items() if r['inference_request_attempted']}
assert set(calls)=={k[0] for k in finished}
previous_end=None
for key,r in sorted(finished.items()):
    if r.get('usage'):assert r['input_tokens']==r['usage']['prompt_tokens']
    began=datetime.fromisoformat(r['wall_utc'])
    assert previous_end is None or began+timedelta(milliseconds=1)>=previous_end
    previous_end=began+timedelta(seconds=r['attempt_wall_seconds'])
    assert previous_end<=datetime.fromisoformat(auth['inference_cutoff_utc'])
result=dict(status='verified',verified_utc=utc_now(),freeze_commit=commit,freeze_commit_utc=commit_time,
    first_call_utc=calls[1]['wall_utc'],last_attempt_finished_utc=previous_end.isoformat(),
    frozen_source_snapshots=len(d['source_hashes']),documented_reporting_repairs=sorted(repairs),documented_presentation_changes=sorted(presentation),historical_files_unchanged=len(history),
    source_cases=24,excluded_stage5_accounts=len(old_accounts),source_bundles=8,replicates=3,workflows=len(prepared),
    scheduled_calls=len(calls),generation_attempts=len(attempts),successful_generations=sum('parsed_call' in r for r in finished.values()),
    failed_attempts=sum('error' in r for r in finished.values()),failed_generation_attempts=sum('error' in r and r['inference_request_attempted'] for r in finished.values()),
    retries=sum(r['retry']>0 for r in finished.values()),unknown_token_attempts=sum(r['inference_request_attempted'] and not r.get('usage') for r in finished.values()),
    prompt_tokens=sum((r.get('usage') or {}).get('prompt_tokens',0) for r in finished.values()),
    completion_tokens=sum((r.get('usage') or {}).get('completion_tokens',0) for r in finished.values()),
    inference_request_wall_seconds=sum(r.get('inference_wall_seconds',0) for r in finished.values()),
    max_attempt_wall_seconds=max(r['attempt_wall_seconds'] for r in finished.values()),max_input_tokens=prep_audit['max_input_tokens'],max_output_tokens=prep_audit['max_output_tokens'],
    repeated_identical_request_groups=sum(len(v)>1 for v in groups.values()),mixed_identical_request_groups=sum(len(set(v))>1 for v in groups.values()),serial_attempts_verified=True)
for label in ('before','after'):
    gpu=json.loads((root/('gpu_'+label+'.json')).read_text())
    assert gpu['status']=='placement_verified' and gpu['cuda_runtime']['bf16_matmul_verified'] and gpu['cuda_runtime']['native_bf16_supported']
    assert gpu['server_arguments']['--dtype']=='bfloat16'
    assert gpu['server_arguments']['--cpu-offload-gb']==gpu['server_arguments']['--swap-space']=='0'
def metric(label,name):
    return sum(float(line.rsplit(' ',1)[1]) for line in (root/('metrics_'+label+'.txt')).read_text().splitlines() if line.startswith(name+'{'))
deltas={k:metric('after',m)-metric('before',m) for k,m in [('completed_http_generations','vllm:request_success_total'),('prompt_tokens','vllm:prompt_tokens_total'),('completion_tokens','vllm:generation_tokens_total')]}
assert deltas['completed_http_generations']==sum(r.get('http_status')==200 for r in finished.values())
for k in ('prompt_tokens','completion_tokens'):assert deltas[k]==result[k]
result['server_metric_deltas']=deltas
inventory=json.loads((root/'evidence_original_hashes.json').read_text())['files'];redactions=json.loads((root/'publication_redactions.json').read_text())
public={r['path']:r for r in redactions['files']}
for name,h in inventory.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==public.get(name,{}).get('public_sha256',h),name
for name,r in public.items():assert inventory[name]==r['original_sha256']
result['original_evidence_files']=len(inventory);result['publication_redacted_files']=len(public)
for cohort,episodes in [('fresh',864),('post_hoc_stage5',3456)]:
    folder=root/'analysis'/cohort
    if not (folder/'summary.json').exists():continue
    summary=json.loads((folder/'summary.json').read_text())
    rows=list(csv.DictReader((folder/'episodes.csv').open()))
    keys=[tuple(r[k] for k in ('bundle_id','replicate','variant','review_duration','policy')) for r in rows]
    assert len(keys)==len(set(keys))==episodes
    assert all(r['status']=='completed' for r in rows)
    assert len(list((folder/'traces').glob('*/*.json.gz')))==episodes
    assert summary['all_policy_traces_replayed'] and not summary['missing_bundle_replicates']
    if cohort=='post_hoc_stage5':assert summary['historical_reference_traces_matched']==1152
    result[cohort+'_policy_replays']=episodes
write_json(root/'verification.json',result);print(json.dumps(result,indent=2))
