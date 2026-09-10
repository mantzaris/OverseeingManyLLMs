"""Checkpointed, one-shot declared research batches using the shared call ledger."""
from datetime import datetime,timezone
import gzip
import importlib.metadata
import json
from pathlib import Path
import shutil
import time

from .cli import ROOT,load_config,source_manifest
from .client import GPUClient
from .development import server_snapshot
from .domain import digest
from .gpu import collect_evidence
from .io import append_jsonl,read_events,utc_now,write_csv,write_json
from .replay import replay_score
from .research_budget import SessionLedger,ResearchBudgetExceeded
from .research_plan import development_plan
from .research_risk import ESTIMATOR_FILE_HASH,ESTIMATOR_HASH,load_risk
from .research_scheduler import ResearchScheduler
from .research_workload import SPEC,scenario_for
from .simulator import run_episode
from .estimator import file_hash

ANALYSIS = dict(primary='Search minus greedy loss at review duration 2, separately original and competition; frozen estimator.',
    bootstrap='2000 paired scenario resamples, fixed analysis seed 20260910; every condition for a scenario resampled together.',
    comparators='EDF prominently; other policies, durations, estimators, capacity and any extension are secondary.',
    failures='All planned rows retained; no failed seed replacement; completed pairs with conservative incomplete bounds.',
    trace_selection='Per workload: numerically first evaluation seed with search lower loss and first with search higher loss than greedy at s=2; if absent use first tie and say so.',
    risk='Initial first-action labels; Brier, pointwise reliability and decisions on same public states. No refitting.',
    outcomes='Original weighted loss, incorrect closures, corrections, review utilization, missed opportunities, per-agent outcomes.',
    search='Exact all ordered subsets of at most six released pending requests; math.fsum fixes order-dependent floating-point ties; measured planning wall time and examined candidates.',
    inference='Two fresh independent samples per job; execute first. Seeds exclude policy, risk, duration, objective, execution order. No promise of exact regenerated GPU actions.')


def prepare_batch(root,name,entries,decision):
    root=Path(root);out=root/'batches'/name;out.mkdir(parents=True,exist_ok=False)
    estimator_source=ROOT/'artifacts/stage2_development/run/estimator.json'
    if file_hash(estimator_source)!=ESTIMATOR_FILE_HASH:raise ValueError('Historical estimator changed')
    frozen=root/'estimator.json'
    if not frozen.exists():shutil.copyfile(estimator_source,frozen)
    if file_hash(frozen)!=ESTIMATOR_FILE_HASH:raise ValueError('Session estimator changed')
    declaration=dict(prepared_utc=utc_now(),name=name,decision=decision,episodes=entries,
        planned_episodes=len(entries),planned_calls=sum(e['planned_calls'] for e in entries),
        runtime_config=load_config(ROOT/'configs/stage1.json'),source_files_sha256=source_manifest(),
        estimator_hash=ESTIMATOR_HASH,estimator_file_sha256=ESTIMATOR_FILE_HASH,larger_workload_spec=SPEC,
        analysis_definitions=ANALYSIS,authorization=json.loads((root/'authorization.json').read_text()))
    declaration['declaration_hash']=digest(declaration);write_json(out/'declaration.json',declaration)
    for file in declaration['source_files_sha256']:
        target=out/'source'/file;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/file,target)
    scenarios={}
    for entry in entries:scenarios.setdefault(entry['scenario_hash'],scenario_for(entry).record())
    write_json(out/'scenarios.scorer-only.json',scenarios)
    return dict(status='declared',name=name,episodes=len(entries),calls=declaration['planned_calls'],declaration_hash=declaration['declaration_hash'])


def compress_evidence(path):
    # Keep every raw byte while avoiding hundreds of MB of repeated prompt strings.
    path=Path(path)
    target=Path(str(path)+'.gz')
    with path.open('rb') as source,target.open('xb') as destination:
        with gzip.GzipFile(filename='',mode='wb',fileobj=destination,mtime=0) as zipped:
            shutil.copyfileobj(source,zipped)
    if gzip.decompress(target.read_bytes())!=path.read_bytes():raise ValueError('Compression round-trip failed')
    path.unlink()


def empty_row(entry):
    return dict(entry,status='not_started',error=None,total_loss=None,accrued_loss=None,correct_jobs=None,
                scheduled_calls=0,attempts=0,prompt_tokens=0,completion_tokens=0,unknown_token_attempts=0,
                request_wall_seconds=0,episode_wall_seconds=0,reviews_completed=0,corrections=0,expired_requests=0)


def run_batch(root,name,pid,log):
    root=Path(root);out=root/'batches'/name;d=json.loads((out/'declaration.json').read_text())
    if digest({k:v for k,v in d.items() if k!='declaration_hash'})!=d['declaration_hash']:raise ValueError('Declaration altered')
    if d['source_files_sha256']!=source_manifest():raise ValueError('Source changed after this batch was declared')
    if file_hash(root/'estimator.json')!=ESTIMATOR_FILE_HASH:raise ValueError('Frozen estimator changed')
    ledger=SessionLedger(root,name)
    if ledger.calls+d['planned_calls']>50000:
        ledger.close();raise ResearchBudgetExceeded('Declared batch exceeds remaining scheduled-call budget')
    with (out/'execution.json').open('x') as handle:json.dump(dict(started_utc=utc_now(),declaration_hash=d['declaration_hash']),handle)
    start=time.monotonic();rows=[empty_row(e) for e in d['episodes']]
    manifest=dict(name=name,status='running',started_utc=utc_now(),declaration_hash=d['declaration_hash'],
        planned_calls=d['planned_calls'],planned_episodes=len(rows),ledger_calls_before=ledger.calls,ledger_attempts_before=ledger.attempts)
    write_csv(out/'episodes.csv',rows)
    try:
        collect_evidence(pid,log,out/'gpu_before.json');server_snapshot(out,'before')
        (out/'requirements.actual.txt').write_text('\n'.join(sorted('{}=={}'.format(p.metadata['Name'],p.version) for p in importlib.metadata.distributions() if p.metadata['Name']))+'\n')
        for index,entry in enumerate(d['episodes']):
            ledger.check_time()
            if ledger.calls>=50000 or ledger.attempts>=60000:raise ResearchBudgetExceeded('Session ceiling reached')
            if file_hash(root/'estimator.json')!=ESTIMATOR_FILE_HASH:raise ValueError('Estimator changed mid-batch')
            folder=out/'episodes'/entry['run_id'];folder.mkdir(parents=True,exist_ok=False)
            ledger.context=name+'/'+entry['run_id']
            client=GPUClient(d['runtime_config'],folder/'raw_requests.jsonl',ledger.deadline,max_calls=entry['planned_calls'],budget=ledger)
            scheduler=ResearchScheduler(entry['policy'],entry['closure_penalty'])
            estimator=load_risk(entry['risk'],root/'estimator.json')
            result=run_episode(scenario_for(entry),entry['policy'],client,folder/'events.jsonl',review_ticks=entry['review_ticks'],public_estimator=estimator,scheduler=scheduler,record_dispatch=True,max_pending=6)
            rows[index]=dict(result,**entry)
            replay=replay_score(folder/'events.jsonl')
            if result['status']=='completed' and replay['status']!='verified':raise ValueError('Replay failed')
            write_json(folder/'result.json',dict(rows[index],replay=replay))
            append_jsonl(out/'completed_rows.jsonl',rows[index])
            compress_evidence(folder/'raw_requests.jsonl');compress_evidence(folder/'events.jsonl')
            ledger.checkpoint()
            # Checkpoint after a complete scenario block, never based on its scores.
            next_entry=d['episodes'][index+1] if index+1<len(rows) else None
            if next_entry is None or (next_entry['workload'],next_entry['seed'])!=(entry['workload'],entry['seed']):
                write_csv(out/'episodes.csv',rows)
                manifest.update(last_completed_index=index,completed_episodes=sum(r['status']=='completed' for r in rows),checkpoint_utc=utc_now())
                write_json(out/'manifest.json',manifest)
                print('{} {}/{} calls={} completed block {} seed={}'.format(utc_now(),index+1,len(rows),ledger.calls,entry['workload'],entry['seed']),flush=True)
        manifest['status']='completed' if all(r['status']=='completed' for r in rows) else 'incomplete'
    except Exception as exc:manifest.update(status='incomplete',error=type(exc).__name__+': '+str(exc))
    finally:
        for row in rows:
            if row['status']=='not_started':row['error']=manifest.get('error','Not reached')
        try:collect_evidence(pid,log,out/'gpu_final.json');server_snapshot(out,'after');manifest['server_status']='healthy GPU server retained'
        except Exception as exc:manifest['server_status']='Final check failed: '+str(exc)
        manifest.update(finished_utc=utc_now(),wall_seconds=time.monotonic()-start,completed_episodes=sum(r['status']=='completed' for r in rows),
            ledger_calls_after=ledger.calls,ledger_attempts_after=ledger.attempts,
            **{key:sum(r[key] for r in rows) for key in ('scheduled_calls','attempts','prompt_tokens','completion_tokens','unknown_token_attempts','request_wall_seconds')})
        write_csv(out/'episodes.csv',rows);write_json(out/'manifest.json',manifest);ledger.close()
    return manifest
