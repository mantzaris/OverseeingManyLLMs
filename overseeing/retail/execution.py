"""One-shot GPU preparation batches and explicit frozen evaluation declarations."""
import gzip
import hashlib
import json
from pathlib import Path
import random
import shutil
import time

from overseeing.domain import digest
from overseeing.io import write_json, utc_now
from .client import RetailClient, RetailLedger
from .upstream import ROOT, account_database, load_database
from .workflow import RetailWorkflow, INSTRUCTIONS, ACTION_SCHEMA


def source_hashes():
    paths=list((ROOT/'overseeing').rglob('*.py'))+list((ROOT/'scripts').glob('*retail*.py'))+[
        ROOT/'configs/stage5_retail.json',ROOT/'scripts/serve_retail_gpu.sh']
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def make_bundles(cases,partition,replicates,bundle_count):
    families=('cancel','modify','return_exchange')
    groups={f:sorted([c for c in cases if c['partition']==partition and c['family']==f],key=lambda c:c['source_index']) for f in families}
    bundles=[]
    for index in range(bundle_count):
        seed=(51000 if partition=='development' else 52000)+index
        rng=random.Random(seed);windows=[2,4,5];costs=[4,8,12];arrivals=[0,0,1]
        rng.shuffle(windows);rng.shuffle(costs);rng.shuffle(arrivals)
        order=list(families);rng.shuffle(order)
        slots=[dict(agent_id=i,case_id=groups[f][index]['case_id'],arrival=arrivals[i],
            cutoff=arrivals[i]+windows[i],wrong_transaction_cost=costs[i]) for i,f in enumerate(order)]
        for replicate in replicates:
            bundles.append(dict(bundle_id=partition+'_{:02d}'.format(index),scenario_seed=seed,
                replicate=replicate,slots=slots,service_failure_cost=4))
    return bundles


def declare(root,name,partition,bundle_count,replicates,estimator_path=None):
    root=Path(root);folder=root/'batches'/name;folder.mkdir(parents=True,exist_ok=False)
    case_record=json.loads((root/'cases.json').read_text());config=json.loads((ROOT/'configs/stage5_retail.json').read_text())
    bundles=make_bundles(case_record['cases'],partition,replicates,bundle_count)
    record=dict(name=name,partition=partition,created_utc=utc_now(),bundles=bundles,
        workflow_count=len(bundles)*3,max_scheduled_calls=len(bundles)*3*config['max_agent_calls'],
        max_attempts=min(30000,len(bundles)*3*config['max_agent_calls']*2),
        case_manifest_hash=case_record['case_manifest_hash'],config=config,
        prompt_hash=digest(INSTRUCTIONS),schema_hash=digest(ACTION_SCHEMA),source_hashes=source_hashes(),
        inference_protocol='Fresh multistep GPU workflow per case and generation replicate; paired deterministic scheduling of the SAME staged proposals across policies and capacities. No downstream agent generation after staging.',
        sampling_seed='SHA256 of partition,bundle_id,case_id,replicate,tool_step,retry; independent of policy, capacity and execution order',
        time_semantics='Concurrent preparation rounds precede a review batch. Arrival 0/0/1 and cutoff windows 2/4/5 are declared processing-service slots, independent of GPU latency and proposal errors.',
        objective='4 points for unresolved service request plus public 4/8/12-point rework/processing consequence for a committed wrong transaction. Synthetic consequence points, not measured dollars.',
        primary_comparison='search minus greedy bundle-mean operational loss at review duration 2',
        secondary_comparison='EDF and other policies; review duration 1',
        analysis=dict(unit='source-disjoint scenario bundle; average generation replicates before paired analysis',
            bootstrap_resamples=2000,bootstrap_seed=20260915,interval='percentile 95%',
            trace_selection='Ascending bundle then replicate: first search<greedy, first tie, first search>greedy; separately first failed workflow. Never select by magnitude.',
            failures='Retain every planned row. Failed preparation has service loss 4, cannot be repaired by transaction review; no replacement cases.'),
        policy_order=[config['policies'][i%6:]+config['policies'][:i%6] for i in range(bundle_count)],
        duration_order=[[2,1] if i%2==0 else [1,2] for i in range(bundle_count)])
    if partition=='evaluation':
        if estimator_path is None:raise ValueError('Evaluation requires a frozen estimator')
        from .risk import RetailRisk
        estimator=json.loads(Path(estimator_path).read_text());RetailRisk.load(estimator)
        record['estimator']=estimator;record['estimator_hash']=estimator['estimator_hash']
        record['planned_policy_episodes']=len(bundles)*12
        if any((root/'batches'/n/'run_started.json').exists() for n in ['evaluation']):
            raise RuntimeError('Evaluation has already begun')
    record['declaration_hash']=digest(record);write_json(folder/'declaration.json',record)
    for relative in record['source_hashes']:
        target=folder/'source'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/relative,target)
    return record


def run(root,name):
    root=Path(root);folder=root/'batches'/name;record=json.loads((folder/'declaration.json').read_text())
    if digest({k:v for k,v in record.items() if k!='declaration_hash'})!=record['declaration_hash']:raise ValueError('Declaration changed')
    if record['source_hashes']!=source_hashes():raise ValueError('Implementation changed since declaration')
    case_record=json.loads((root/'cases.json').read_text())
    if case_record['case_manifest_hash']!=record['case_manifest_hash']:raise ValueError('Case selection changed')
    cases={c['case_id']:c for c in case_record['cases']};data=load_database()
    marker=folder/'run_started.json'
    with marker.open('x') as stream:json.dump(dict(started_utc=utc_now()),stream)
    ledger=RetailLedger(root,name);completed=[];started=time.monotonic()
    try:
        for bundle in record['bundles']:
            ledger.check();key=bundle['bundle_id']+'_r'+str(bundle['replicate']);dest=folder/'prepared'/key;dest.mkdir(parents=True,exist_ok=False)
            workflows={};clients={};initials={};failures={}
            for slot in bundle['slots']:
                case=cases[slot['case_id']];initial=account_database(data,case['user_id']);initials[case['case_id']]=initial
                workflows[case['case_id']]=RetailWorkflow(case['customer_message'],initial,record['config'].get('interface_revision',0))
                clients[case['case_id']]=RetailClient(record['config'],dest/(case['case_id'].replace(':','_')+'_raw.jsonl'),
                    ledger.deadline,max_calls=record['config']['max_agent_calls'],budget=ledger)
            # Independent agent histories; serial GPU dispatch interleaves preparation steps.
            for step in range(record['config']['max_agent_calls']):
                for slot in bundle['slots']:
                    case_id=slot['case_id'];workflow=workflows[case_id]
                    if workflow.finished:continue
                    metadata=dict(partition=record['partition'],bundle_id=bundle['bundle_id'],case_id=case_id,
                        replicate=bundle['replicate'],tool_step=step)
                    try:
                        call=clients[case_id].generate(workflow.messages,metadata);workflow.step(call)
                    except Exception as exc:
                        workflow.finished=True;failures[case_id]=type(exc).__name__+': '+str(exc)
            rows=[]
            for slot in bundle['slots']:
                case_id=slot['case_id'];workflow=workflows[case_id]
                failure=failures.get(case_id)
                if not workflow.finished:failure='Maximum agent tool-call steps reached'
                result=workflow.result(cases[case_id],initials[case_id],failure)
                result.update(bundle_id=bundle['bundle_id'],replicate=bundle['replicate'],counts=clients[case_id].stats())
                rows.append(result)
            write_json(dest/'workflows.json',rows)
            for path in dest.glob('*_raw.jsonl'):
                raw=path.read_bytes();compressed=gzip.compress(raw,mtime=0)
                if gzip.decompress(compressed)!=raw:raise RuntimeError('Raw compression verification failed')
                path.with_suffix('.jsonl.gz').write_bytes(compressed);path.unlink()
            completed.append(key)
            checkpoint=dict(completed_bundles=completed,planned_bundles=len(record['bundles']),
                completed_workflows=len(completed)*3,elapsed_seconds=time.monotonic()-started,captured_utc=utc_now())
            write_json(folder/'checkpoint.json',checkpoint)
            print(json.dumps(dict(bundle=key,staged=sum(r['proposal'] is not None for r in rows),
                errors=sum(r['initial_error'] for r in rows),calls=sum(r['counts']['scheduled_calls'] for r in rows),
                elapsed_seconds=round(time.monotonic()-started,2))),flush=True)
        write_json(folder/'run_finished.json',dict(status='completed',finished_utc=utc_now(),
            elapsed_seconds=time.monotonic()-started,completed_bundles=completed))
    finally:ledger.close()
