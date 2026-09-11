#!/usr/bin/env python3
"""Verify source isolation, frozen hashes, every attempt and accounting."""
import json,hashlib,subprocess,sys,math
from datetime import datetime,timedelta,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.hvac import digest,save,parse,FIELDS
root=Path('artifacts/stage7_empirical');declaration=json.loads((root/'declaration.json').read_text());auth=json.loads((root/'authorization.json').read_text())
assert declaration['sha256']==digest({k:v for k,v in declaration.items() if k!='sha256'})
for name,h in declaration['source_hashes'].items():
    assert hashlib.sha256((root/'frozen_source'/name).read_bytes()).hexdigest()==h,name
    assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==h,name
commit=(root/'freeze_commit.txt').read_text().strip();commit_utc=datetime.fromisoformat(subprocess.check_output(['git','show','-s','--format=%cI',commit],text=True).strip())
assert subprocess.check_output(['git','show',commit+':'+str(root/'declaration.json')])==(root/'declaration.json').read_bytes()
cases=json.loads((root/'cases.json').read_text());attempts=[];by_split={}
for split in ('development','development_revision1','evaluation'):
    paths=sorted((root/split).glob('*_attempts.json'));items=[]
    expected=[c for c in cases if c['split']==('evaluation' if split=='evaluation' else 'development')]
    for c in expected:
        saved=json.loads((root/split/(c['case_id']+'.json')).read_text())
        for role in ('proposal','review'):
            records=json.loads((root/split/(c['case_id']+'_'+role+'_attempts.json')).read_text());assert 1<=len(records)<=2
            assert [r['retry'] for r in records]==list(range(len(records)))
            valid=[r for r in records if r['success']]
            assert saved[role]==(json.loads(valid[-1]['response'])['choices'][0]['message']['content'] if valid else '')
            for r in records:
                now=datetime.fromisoformat(r['started_utc']);assert datetime.fromisoformat(auth['started_utc'])<=now<datetime.fromisoformat(auth['inference_cutoff_utc'])
                assert now+timedelta(seconds=r['elapsed_seconds'])<=datetime.fromisoformat(auth['inference_cutoff_utc'])
                if split=='evaluation':assert commit_utc<now
                req=r['request'];assert req['model']=='Qwen/Qwen2.5-7B-Instruct' and req['temperature']==.3 and req['max_tokens']==128 and req['top_p']==1
                contents=' '.join(x['content'] for x in req['messages']);assert c['source_date'] not in contents and 'Ground Truth' not in contents
                if r['success']:assert parse(json.loads(r['response'])['choices'][0]['message']['content'])!='invalid'
                items.append(r)
    by_split[split]=dict(workflows=len(expected),scheduled_calls=len(expected)*2,attempts=len(items),failed_attempts=sum(not x['success'] for x in items));attempts.extend(items)
ledger=[json.loads(s) for s in (root/'ledger.jsonl').read_text().splitlines()];assert len(ledger)==len(attempts)<=auth['attempt_limit']
assert sorted((x['case_id'],x['role'],x['retry'],x['utc']) for x in ledger)==sorted((x['case_id'],x['role'],x['retry'],x['started_utc']) for x in attempts)
for c in cases:
    assert len(c['signals']['sat'])==60
    for k in FIELDS:
        v=c['signals'][k];expected=[round(sum(v)/60,3),min(v),max(v),round(v[-1]-v[0],3)];assert expected==c['public']['readings'][k]
usage=[json.loads(x['response'])['usage'] for x in attempts if 'response' in x]
prompt=sum(x['prompt_tokens'] for x in usage);completion=sum(x['completion_tokens'] for x in usage)
def metrics(label):
    lines=(root/('metrics_'+label+'.txt')).read_text().splitlines()
    return {key:sum(float(s.rsplit(' ',1)[1]) for s in lines if s.startswith('vllm:'+key+'{')) for key in ('prompt_tokens_total','generation_tokens_total','request_success_total')}
before=metrics('before');after=metrics('after');delta={k:after[k]-before[k] for k in before}
assert delta['request_success_total']==len(usage) and delta['prompt_tokens_total']==prompt and delta['generation_tokens_total']==completion,delta
for label in ('before','after'):assert json.loads((root/('gpu_'+label+'.json')).read_text())['status']=='placement_verified'
result=dict(status='verified',verified_utc=datetime.now(timezone.utc).isoformat(),freeze_commit=commit,by_split=by_split,scheduled_calls=sum(x['scheduled_calls'] for x in by_split.values()),generation_attempts=len(attempts),failed_attempts=sum(not x['success'] for x in attempts),retries=sum(x['retry'] for x in attempts),prompt_tokens=prompt,completion_tokens=completion,inference_seconds=sum(x['elapsed_seconds'] for x in attempts),max_attempt_seconds=max(x['elapsed_seconds'] for x in attempts),max_prompt_tokens=max(x['prompt_tokens'] for x in usage),max_completion_tokens=max(x['completion_tokens'] for x in usage),first_generation_utc=min(x['started_utc'] for x in attempts),last_generation_finished_utc=max(datetime.fromisoformat(x['started_utc'])+timedelta(seconds=x['elapsed_seconds']) for x in attempts).isoformat(),server_metric_deltas=delta,source_days=26,development_days=8,evaluation_days=18,equipment_count=1)
save(root/'verification.json',result);print(json.dumps(result,indent=2))
