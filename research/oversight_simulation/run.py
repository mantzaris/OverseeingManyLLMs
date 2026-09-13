"""Frozen CPU batch; full compact command traces, no participant schema or IDs."""
import argparse,gzip,json,time,hashlib,subprocess
from datetime import datetime,timedelta
from pathlib import Path
from research.oversight_workflow.common import ROOT,read,write,digest
from research.oversight_workflow.offline import labels
from research.adaptive_correction_transfer.scoring import score
from .inputs import OUT,HERE,workload
from .reviewer import ReviewerEnvironment
from .simulation import simulate


def environment(inputs):
    private=labels();gold={qid:private[x['source_id']][qid] for qid,x in inputs['items'].items()}
    initial={qid:bool(score(x['output'],gold[qid])['joint']) for qid,x in inputs['items'].items()}
    return ReviewerEnvironment(gold,initial)


def frozen_files():
    ps=list(HERE.glob('*.py'))+list((HERE/'tests').glob('*.py'))+[HERE/'MODEL.md',OUT/'inputs.json',OUT/'design.json']
    ps += [ROOT/p for p in ['research/oversight_workflow/protocol.py','research/oversight_workflow/common.py','research/oversight_workflow/offline.py','research/adaptive_correction_transfer/scoring.py','artifacts/oversight_workflow/offline_annotations.json']]
    ps += list((ROOT/'research/adaptive_correction_transfer/vendor').glob('*.py'))
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ps}


def verify_freeze():
    f=read(OUT/'freeze.json')
    for name,sha in f['files'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('Frozen file changed: '+name)
    return f


def main():
    p=argparse.ArgumentParser();p.add_argument('--forecast',action='store_true');p.add_argument('--freeze',action='store_true');args=p.parse_args()
    inputs=read(OUT/'inputs.json');design=read(OUT/'design.json');env=environment(inputs)
    if args.freeze:
        if (OUT/'freeze.json').exists():raise ValueError('Refusing freeze overwrite')
        write(OUT/'freeze.json',dict(record_kind='computational_simulation',files=frozen_files(),baseline_commit=read(OUT/'ledger.json')['baseline_commit'],planned_simulations=len(design['configs'])*len(design['rotations'])*len(design['seeds'])*len(design['policies']),declaration='Frozen before comparative results. No human records and zero inference.'))
        print('Frozen');return
    if args.forecast:
        cfg=next(c for c in design['configs'] if c['offered']==36 and c['horizon']==900);items=workload(inputs,cfg,0);start=time.perf_counter()
        for seed in design['development_seeds']:simulate(items,inputs['sources'],cfg,'Q',seed,env)
        per=(time.perf_counter()-start)/len(design['development_seeds']);n=len(design['configs'])*len(design['rotations'])*len(design['seeds'])*len(design['policies'])
        record=dict(kind='Development throughput only; no comparative outcome inspected',seconds_per_36_task_run=per,planned_simulations=n,conservative_seconds_with_2x_margin=per*n*2)
        write(OUT/'forecast.json',record);print(json.dumps(record));return
    verify_freeze()
    if (OUT/'results.jsonl.gz').exists() or (OUT/'traces.jsonl.gz').exists():raise ValueError('Refusing to overwrite a completed or partial batch')
    start=time.perf_counter();count=0;stop_reason=None
    reserve=datetime.fromisoformat(read(OUT/'ledger.json')['deadline_utc'])-timedelta(minutes=20)
    with gzip.open(OUT/'results.jsonl.gz','wt',compresslevel=6) as results,gzip.open(OUT/'traces.jsonl.gz','wt',compresslevel=6) as traces:
        for cfg in design['configs']:
            if datetime.now(reserve.tzinfo)>=reserve:
                stop_reason='20-minute analysis reserve reached; remaining declarations retained';break
            for rotation in design['rotations']:
                items=workload(inputs,cfg,rotation)
                for seed in design['seeds']:
                    for policy in design['policies']:
                        ident=dict(record_kind='computational_simulation',scenario_id=cfg['id']+'/rotation'+str(rotation),simulation_run_id=cfg['id']+'/r'+str(rotation)+'/s'+str(seed)+'/'+policy,config=cfg['id'],family=cfg['family'],rotation=rotation,seed=seed,policy=policy)
                        summary,trace=simulate(items,inputs['sources'],cfg,policy,seed,env)
                        results.write(json.dumps({**ident,**summary},separators=(',',':'))+'\n')
                        traces.write(json.dumps({**ident,**trace},separators=(',',':'))+'\n');count+=1
            results.flush();traces.flush()
            print('Completed',cfg['id'],count,'simulations',round(time.perf_counter()-start,1),'CPU wall seconds',flush=True)
            write(OUT/'progress.json',dict(completed=count,last_complete_config=cfg['id'],elapsed_seconds=time.perf_counter()-start))
    write(OUT/'batch.json',dict(record_kind='computational_simulation',complete=count==len(design['configs'])*len(design['rotations'])*len(design['seeds'])*len(design['policies']),stop_reason=stop_reason,simulations=count,elapsed_seconds=time.perf_counter()-start,inference_calls=0,source_contexts=6,questions=36,independent_monte_carlo_seeds=len(design['seeds']),human_observations=0))


if __name__=='__main__':main()
