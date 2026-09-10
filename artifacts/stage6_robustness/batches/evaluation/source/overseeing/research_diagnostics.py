"""One declared 128-call identical-request check and no stability-seeking reruns."""
from collections import defaultdict
import json
from pathlib import Path
import shutil
import time

from .cli import ROOT, load_config, source_manifest
from .client import GPUClient
from .development import server_snapshot
from .domain import digest
from .gpu import collect_evidence
from .io import read_events, utc_now, write_json
from .research_budget import SessionLedger


def prepare_diagnostics(root):
    root=Path(root);out=root/'diagnostics';out.mkdir(exist_ok=False)
    historical=ROOT/'artifacts/stage3_competition'
    variants=json.loads((historical/'identical_request_variation.json').read_text())
    mixed=sorted(group['request_hash'] for group in variants['groups'])
    records={}
    for path in sorted((historical/'run').glob('*/*/*/raw_requests.jsonl')):
        for record in read_events(path):
            if record['phase']=='attempt_finished' and 'parsed_action' in record and record['retry']==0:
                key=digest(record['request'])
                records.setdefault(key,dict(source_path=str(path.relative_to(ROOT)), request=record['request'],
                    metadata={k:record[k] for k in ('scenario_seed','agent_id','job_id')},sample=record['sample'],historical_action=record['parsed_action']))
    selected=mixed+[key for key in sorted(records) if key not in mixed][:32-len(mixed)]
    prompts=[dict(records[key],request_hash=key,prompt_index=index) for index,key in enumerate(selected)]
    calls=[]
    for repeat in range(4):
        shift=repeat*7
        for index in list(range(32))[shift:]+list(range(32))[:shift]:
            calls.append(dict(execution_index=len(calls),repeat=repeat,prompt_index=index))
    declaration=dict(prepared_utc=utc_now(),selection_rule='Two Stage 3 mixed-output request hashes sorted, then lexicographically first 30 other unique successful retry-0 request hashes; four repeats, order left-rotated by 7*repeat.',
        prompts=prompts,calls=calls,planned_calls=128,max_attempts=128,runtime_config=load_config(ROOT/'configs/stage1.json'),source_files_sha256=source_manifest())
    declaration['declaration_hash']=digest(declaration);write_json(out/'declaration.json',declaration)
    for name in declaration['source_files_sha256']:
        target=out/'source'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
    return dict(status='declared',planned_calls=128,declaration_hash=declaration['declaration_hash'])


def run_diagnostics(root,pid,log):
    root=Path(root);out=root/'diagnostics';d=json.loads((out/'declaration.json').read_text())
    assert digest({k:v for k,v in d.items() if k!='declaration_hash'})==d['declaration_hash']
    assert d['source_files_sha256']==source_manifest()
    with (out/'execution.json').open('x') as handle:json.dump(dict(started_utc=utc_now(),declaration_hash=d['declaration_hash']),handle)
    ledger=SessionLedger(root,'diagnostics');rows=[];start=time.monotonic()
    result=dict(status='incomplete',started_utc=utc_now(),planned_calls=128)
    try:
        collect_evidence(pid,log,out/'gpu_before.json');server_snapshot(out,'before')
        for entry in d['calls']:
            ledger.context='diagnostic/{}'.format(entry['execution_index'])
            prompt=d['prompts'][entry['prompt_index']]
            path=out/'raw'/('{:03d}.jsonl'.format(entry['execution_index']))
            client=GPUClient(dict(d['runtime_config'],max_attempts_per_call=1),path,ledger.deadline,max_calls=1,budget=ledger)
            row=dict(entry,request_hash=prompt['request_hash'],status='failed')
            try:
                row['action']=client.action(json.loads(prompt['request']['messages'][1]['content']),prompt['metadata'],prompt['sample'])
                row['status']='completed'
            except Exception as exc:row['error']=str(exc)
            row.update(client.stats());rows.append(row)
            raw=read_events(path)
            assert all(digest(r['request'])==prompt['request_hash'] for r in raw)
            if len(rows)%16==0:
                ledger.checkpoint();write_json(out/'responses.json',rows)
                print('{} diagnostic {}/128'.format(utc_now(),len(rows)),flush=True)
        result['status']='completed' if all(r['status']=='completed' for r in rows) else 'incomplete'
    except Exception as exc:result['error']=type(exc).__name__+': '+str(exc)
    finally:
        result.update(finished_utc=utc_now(),wall_seconds=time.monotonic()-start,completed_calls=sum(r['status']=='completed' for r in rows),
                      **{k:sum(r[k] for r in rows) for k in ('scheduled_calls','attempts','prompt_tokens','completion_tokens','unknown_token_attempts')})
        groups=defaultdict(list)
        for row in rows:
            if row['status']=='completed':groups[row['prompt_index']].append(row['action'])
        result['mixed_action_groups']=sum(len(set(values))>1 for values in groups.values())
        result['observed_groups']={str(k):v for k,v in groups.items()}
        try:
            collect_evidence(pid,log,out/'gpu_final.json');server_snapshot(out,'after')
        except Exception as exc:result['final_server_error']=str(exc)
        write_json(out/'responses.json',rows);write_json(out/'summary.json',result);ledger.close()
    return result
