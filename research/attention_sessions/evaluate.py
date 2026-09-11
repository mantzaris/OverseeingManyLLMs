"""Declared CPU replay. Never writes to historical artifact directories."""
import argparse,csv,gzip,json,time,hashlib
from pathlib import Path
from dataclasses import asdict
from datetime import datetime,timezone
from .data import *
from .method import POLICIES
from .controller import Controller

METRICS=('loss','correct','unresolved','reviews','corrections','harms','abstentions','proposal_failures','review_failures',
         'missed_useful','active_time','setup_time','switch_time','decision_time','coordination_time','session_offers',
         'context_changes','repeated_context_inspections','expired_unreviewed','waiting_time')

def simulate(public,private,config,policy):
    start=time.perf_counter();c=Controller(public,settings(config),policy);iterations=0
    while c.step(lambda key:response(private,config['reviewer'],key)):
        iterations+=1
        if iterations>1000:raise RuntimeError('Controller failed to progress')
    if any(s in ('future','pending','active','deferred') for s in c.status.values()):raise AssertionError('Unfinished accounting')
    jobs=[]
    for r in public:
        key=r.request_id;truth=private[key]['truth'];initial=r.proposal==truth;final=c.final[key]==truth
        raw_response=response(private,config['reviewer'],key);potential=r.proposal if raw_response=='invalid' else raw_response
        jobs.append(dict(request_id=key,initial_correct=initial,correct=final,unresolved=not final,
            reviewed=key in c.reviewed,correction=not initial and final,harm=initial and not final,
            proposal_failure=r.proposal=='invalid',review_failure=key in c.reviewed and raw_response=='invalid',
            useful_missed=not initial and potential==truth and key not in c.reviewed,final=c.final[key],weight=r.weight))
    fail=sum(e.get('response_failed',False) for e in c.events if e['event']=='review_completed')
    starts={e['request_id']:e['tick'] for e in c.events if e['event']=='review_started'}
    row=dict(loss=sum(x['weight'] for x in jobs if x['unresolved']),correct=sum(x['correct'] for x in jobs),unresolved=sum(x['unresolved'] for x in jobs),
        reviews=len(c.reviewed),corrections=sum(x['correction'] for x in jobs),harms=sum(x['harm'] for x in jobs),abstentions=sum(x['final']=='abstain' for x in jobs),
        proposal_failures=sum(x['proposal_failure'] for x in jobs),review_failures=fail,missed_useful=sum(x['useful_missed'] for x in jobs),
        active_time=c.used,setup_time=c.components['setup'],switch_time=c.components['switch'],decision_time=c.components['decision'],coordination_time=c.components['coordination'],
        session_offers=c.session_id,context_changes=c.context_changes,repeated_context_inspections=c.repeated,
        expired_unreviewed=sum(s=='expired' for s in c.status.values()),waiting_time=sum(starts[r.request_id]-r.arrival for r in public if r.request_id in starts),
        planning_and_controller_seconds=time.perf_counter()-start)
    return dict(metrics=row,events=c.events,jobs=jobs,sequence=c.reviewed)

def csv_write(path,rows):
    with Path(path).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def freeze():
    ROOT.mkdir(exist_ok=True,parents=True)
    if (ROOT/'declaration.json').exists():raise RuntimeError('Declaration already exists')
    cases,records,e=load();source={str(p):sha(p) for p in sorted(Path('research/attention_sessions').rglob('*.py'))}
    source['research/attention_sessions/PLAN.md']=sha('research/attention_sessions/PLAN.md')
    data={str(HIST/'cases.json'):sha(HIST/'cases.json'),str(HIST/'estimator.json'):sha(HIST/'estimator.json')}
    for c in cases:data[str(HIST/'evaluation'/(c['case_id']+'.json'))]=sha(HIST/'evaluation'/(c['case_id']+'.json'))
    d=dict(frozen_utc=datetime.now(timezone.utc).isoformat(),status='exploratory saved-output comparison; all source evaluation outcomes previously inspected',
           cases=[c['case_id'] for c in cases],bundles=bundles(cases),policies=POLICIES,conditions=conditions(),source_hashes=source,data_hashes=data,
           expected_rows=len(bundles(cases))*len(POLICIES)*len(conditions()),new_inference=0,primary='guarded minus sticky_edf; core_high_1_12_ideal',
           bootstrap_seed=20260911,bootstrap_resamples=2000,response_invariance='Individual evidence and stored response fixed; joint human presentation effects not identified')
    save_json(ROOT/'declaration.json',d);print('Frozen',d['expected_rows'],'policy replays; commit before run.')

def run(split,verify=False):
    cases,records,e=load(split);groups=bundles(cases);out=ROOT/split
    configs=conditions() if split=='evaluation' else [dict(condition_id='development',study='development',load='high',setup=1,budget=12,reviewer='ideal',contexts='related')]
    if split=='evaluation':
        dec=json.loads((ROOT/'declaration.json').read_text())
        for p,h in dict(dec['source_hashes'],**dec['data_hashes']).items():
            if sha(p)!=h:raise ValueError('Frozen source mismatch: '+p)
        assert groups==dec['bundles'] and configs==dec['conditions']
    rows=[];traces=[]
    for bi,days in enumerate(groups):
        for config in configs:
            public,private=workload(days,cases,records,e,config)
            input_hash=hashlib.sha256(json.dumps([asdict(r) for r in public],sort_keys=True).encode()).hexdigest()
            for policy in POLICIES:
                result=simulate(public,private,config,policy)
                meta=dict(bundle=bi,condition_id=config['condition_id'],policy=policy,input_hash=input_hash)
                rows.append(dict(meta,**{k:config[k] for k in ('study','load','setup','budget','reviewer','contexts')},**result['metrics']))
                traces.append(dict(meta,**result))
        print('Completed bundle',bi,days,flush=True)
    if verify:
        with gzip.open(out/'traces.jsonl.gz','rt') as f:old=[json.loads(x) for x in f]
        for r in old:r['metrics'].pop('planning_and_controller_seconds',None)
        for r in traces:r['metrics'].pop('planning_and_controller_seconds',None)
        assert old==traces;print('Replay verified:',len(traces));return
    if out.exists():raise RuntimeError('Preserve previous run; output directory already exists')
    out.mkdir(parents=True)
    csv_write(out/'episodes.csv',rows)
    with gzip.open(out/'traces.jsonl.gz','wt') as f:
        for r in traces:f.write(json.dumps(r,sort_keys=True)+'\n')
    save_json(out/'accounting.json',dict(rows=len(rows),cases=len(cases),days=len({c['run_id'] for c in cases}),bundles=len(groups),equipment=1,new_inference=0,
        completed_utc=datetime.now(timezone.utc).isoformat(),total_controller_seconds=sum(r['planning_and_controller_seconds'] for r in rows)))
    print('Saved',len(rows),'rows')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['development','freeze','run','verify']);a=p.parse_args()
    if a.command=='freeze':freeze()
    else:run('development' if a.command=='development' else 'evaluation',a.command=='verify')
