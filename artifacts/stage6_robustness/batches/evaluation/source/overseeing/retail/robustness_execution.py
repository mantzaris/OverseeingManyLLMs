"""Separate Stage 6 authorization and frozen retail preparation path."""
from datetime import datetime,timedelta,timezone
import fcntl
import gzip
import hashlib
import json
from pathlib import Path
import random
import shutil
import time

from overseeing.domain import digest
from overseeing.io import append_jsonl,utc_now,write_json
from .client import RetailClient,RetailLedger
from .upstream import ROOT,account_database,load_database
from .workflow import RetailWorkflow,INSTRUCTIONS,ACTION_SCHEMA
from .risk import RetailRisk

ARTIFACTS=Path('artifacts/stage6_robustness')


class RobustnessLedger(RetailLedger):
    def __init__(self,root,context):
        self.root=Path(root);self.context=context
        self.auth=json.loads((self.root/'authorization.json').read_text())
        start=datetime.fromisoformat(self.auth['started_utc']);end=datetime.fromisoformat(self.auth['deadline_utc'])
        self.deadline=datetime.fromisoformat(self.auth['inference_cutoff_utc'])
        if (self.auth['name']!='stage6_robustness' or self.auth['authorization']!='explicit_user_request'
            or self.auth['attempt_limit']!=6000 or self.auth['maximum_retries_per_call']!=1
            or end!=start+timedelta(hours=6) or self.deadline!=end-timedelta(minutes=90)
            or not start<=datetime.now(timezone.utc)<self.deadline):raise RuntimeError('Invalid or expired Stage 6 authorization')
        self.lock=(self.root/'worker.lock').open('a');fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        self.path=self.root/'ledger.jsonl'
        records=[json.loads(s) for s in self.path.read_text().splitlines()] if self.path.exists() else []
        self.calls=sum(r['kind']=='call_reserved' for r in records);self.attempts=sum(r['kind']=='attempt_reserved' for r in records)
        self.seen={(r['call_id'],r['retry']) for r in records if r['kind']=='attempt_reserved'}

    def check(self):
        if datetime.now(timezone.utc)>=self.deadline:raise RuntimeError('Stage 6 inference cutoff reached')
        if self.attempts>=6000:raise RuntimeError('Stage 6 attempt ceiling reached')

    def close(self):
        write_json(self.root/'ledger_state.json',dict(captured_utc=utc_now(),scheduled_calls=self.calls,attempts=self.attempts,
            attempt_limit=6000,inference_cutoff_utc=self.deadline.isoformat()))
        fcntl.flock(self.lock,fcntl.LOCK_UN);self.lock.close()


def source_hashes():
    paths=list((ROOT/'overseeing').rglob('*.py'))+list((ROOT/'scripts').glob('*robustness*.py'))+[
        ROOT/'configs/stage5_retail.json',ROOT/'scripts/serve_retail_gpu.sh',ROOT/'tests/test_robustness.py',
        ROOT/'plan/STAGE6_ROBUSTNESS_PLAN.md',ROOT/'paper/RETAIL_ASSUMPTION_REVIEW.md']
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def declare():
    root=ARTIFACTS;folder=root/'batches/evaluation';folder.mkdir(parents=True,exist_ok=False)
    cases=json.loads((root/'cases.json').read_text());n=cases['bundle_count']
    config=json.loads((ROOT/'configs/stage5_retail.json').read_text())
    estimator=json.loads((ROOT/'artifacts/stage5_practical/estimator.json').read_text());RetailRisk.load(estimator)
    groups={f:[c for c in cases['cases'] if c['family']==f] for f in ('cancel','modify','return_exchange')}
    bundles=[]
    for index in range(n):
        seed=62000+index;rng=random.Random(seed);windows=[2,4,5];costs=[4,8,12];arrivals=[0,0,1]
        rng.shuffle(windows);rng.shuffle(costs);rng.shuffle(arrivals);families=list(groups);rng.shuffle(families)
        slots=[dict(agent_id=i,case_id=groups[f][index]['case_id'],arrival=arrivals[i],cutoff=arrivals[i]+windows[i],
            wrong_transaction_cost=costs[i]) for i,f in enumerate(families)]
        for rep in (0,1,2):bundles.append(dict(bundle_id='stage6_{:02d}'.format(index),replicate=rep,scenario_seed=seed,slots=slots,service_failure_cost=4))
    record=dict(name='evaluation',partition='evaluation',generation_partition='stage6_evaluation',created_utc=utc_now(),
        bundles=bundles,workflow_count=n*9,max_scheduled_calls=n*9*14,max_attempts=n*9*28,
        case_manifest_hash=cases['case_manifest_hash'],config=config,estimator=estimator,estimator_hash=estimator['estimator_hash'],
        prompt_hash=digest(INSTRUCTIONS),schema_hash=digest(ACTION_SCHEMA),source_hashes=source_hashes(),
        authorization_sha256=hashlib.sha256((root/'authorization.json').read_bytes()).hexdigest(),
        variants={'reference':dict(authority='perfect_correction',extra_multi_item_ticks=0),
            'approve_block':dict(authority='perfect_detection_approve_or_block',extra_multi_item_ticks=0),
            'complexity_time':dict(authority='perfect_correction',extra_multi_item_ticks=1)},
        planned_policy_episodes=n*3*6*2*3,policy_order=[config['policies'][i%6:]+config['policies'][:i%6] for i in range(n)],
        duration_order=[[2,1] if i%2==0 else [1,2] for i in range(n)],
        generation_seed='SHA256 of partition=stage6_evaluation,bundle_id,case_id,replicate,tool_step,retry; independent of operational variants and policies',
        primary='search minus greedy mean operational loss under approve_block at base duration 2',
        analysis=dict(bootstrap_resamples=2000,bootstrap_seed=20260916,unit='average three generation replicates within source-disjoint bundle; resample all conditions together',
            interval='percentile 95%',secondary='other policy contrasts, reference and complexity_time, duration 1, variant minus reference',
            examples='ascending bundle then replicate: first primary benefit, tie, unfavorable, and first unstaged failure',
            missing='retain all planned rows, no replacement; paired intervals only on complete matched bundles, report any missing bundles explicitly'),
        historical_sensitivity=dict(root='artifacts/stage5_practical',batch='evaluation',label='post_hoc_stage5',fresh=False,
            note='All 32 existing bundles, three saved replicates; do not pool with fresh eight-bundle follow-up'))
    record['declaration_hash']=digest(record);write_json(folder/'declaration.json',record)
    for name in record['source_hashes']:
        target=folder/'source'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
    shutil.copyfile(ROOT/'artifacts/stage5_practical/estimator.json',root/'estimator.json')
    return record


def run():
    root=ARTIFACTS;folder=root/'batches/evaluation';record=json.loads((folder/'declaration.json').read_text())
    assert digest({k:v for k,v in record.items() if k!='declaration_hash'})==record['declaration_hash']
    for name,expected in record['source_hashes'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
    assert hashlib.sha256((root/'authorization.json').read_bytes()).hexdigest()==record['authorization_sha256']
    case_record=json.loads((root/'cases.json').read_text())
    assert digest({k:v for k,v in case_record.items() if k!='case_manifest_hash'})==record['case_manifest_hash']
    cases={c['case_id']:c for c in case_record['cases']};data=load_database()
    # No model generation before an independently checked serving identity record.
    gpu=json.loads((root/'gpu_before.json').read_text());assert gpu['status']=='placement_verified'
    ledger=RobustnessLedger(root,'evaluation');completed=[];started=time.monotonic()
    try:
        with (folder/'run_started.json').open('x') as stream:json.dump(dict(started_utc=utc_now()),stream)
        for bundle in record['bundles']:
            ledger.check();key=bundle['bundle_id']+'_r'+str(bundle['replicate']);dest=folder/'prepared'/key;dest.mkdir(parents=True,exist_ok=False)
            workflows={};clients={};initials={};failures={}
            for slot in bundle['slots']:
                case=cases[slot['case_id']];initial=account_database(data,case['user_id']);initials[case['case_id']]=initial
                workflows[case['case_id']]=RetailWorkflow(case['customer_message'],initial,record['config']['interface_revision'])
                clients[case['case_id']]=RetailClient(record['config'],dest/(case['case_id'].replace(':','_')+'_raw.jsonl'),
                    ledger.deadline,max_calls=record['config']['max_agent_calls'],budget=ledger)
            for step in range(record['config']['max_agent_calls']):
                for slot in bundle['slots']:
                    case_id=slot['case_id'];workflow=workflows[case_id]
                    if workflow.finished:continue
                    metadata=dict(partition=record['generation_partition'],bundle_id=bundle['bundle_id'],case_id=case_id,
                        replicate=bundle['replicate'],tool_step=step)
                    try:workflow.step(clients[case_id].generate(workflow.messages,metadata))
                    except Exception as exc:workflow.finished=True;failures[case_id]=type(exc).__name__+': '+str(exc)
            rows=[]
            for slot in bundle['slots']:
                case_id=slot['case_id'];workflow=workflows[case_id];failure=failures.get(case_id)
                if not workflow.finished:failure='Maximum agent tool-call steps reached'
                result=workflow.result(cases[case_id],initials[case_id],failure)
                result.update(bundle_id=bundle['bundle_id'],replicate=bundle['replicate'],counts=clients[case_id].stats());rows.append(result)
            write_json(dest/'workflows.json',rows)
            for path in dest.glob('*_raw.jsonl'):
                raw=path.read_bytes();compressed=gzip.compress(raw,mtime=0);assert gzip.decompress(compressed)==raw
                path.with_suffix('.jsonl.gz').write_bytes(compressed);path.unlink()
            completed.append(key)
            write_json(folder/'checkpoint.json',dict(completed_bundles=completed,planned_bundles=len(record['bundles']),
                completed_workflows=len(completed)*3,elapsed_seconds=time.monotonic()-started,captured_utc=utc_now()))
            print(json.dumps(dict(bundle=key,staged=sum(r['proposal'] is not None for r in rows),errors=sum(r['initial_error'] for r in rows),
                calls=sum(r['counts']['scheduled_calls'] for r in rows),elapsed_seconds=round(time.monotonic()-started,2))),flush=True)
        write_json(folder/'run_finished.json',dict(status='completed',finished_utc=utc_now(),elapsed_seconds=time.monotonic()-started,completed_bundles=completed))
    finally:ledger.close()
