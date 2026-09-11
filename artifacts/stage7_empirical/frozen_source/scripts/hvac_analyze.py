#!/usr/bin/env python3
"""Offline fitting, frozen paired simulation and deterministic replay."""
import argparse,csv,gzip,hashlib,json,sys,itertools
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.hvac import *
ROOT=Path('artifacts/stage7_empirical')
def records(split):
    result={}
    for c in json.loads((ROOT/'cases.json').read_text()):
        if c['split']!=split:continue
        folder='development_revision1' if split=='development' else split
        p=ROOT/folder/(c['case_id']+'.json');result[c['case_id']]=json.loads(p.read_text()) if p.exists() else dict(case_id=c['case_id'],proposal='',review='',missing=True)
    return result
def vector(c):return [float(c['public']['equipment_mode']=='SZVAV'),float(c['public']['window_start'].split(':')[0])]+[v for k in sorted(FIELDS) for v in c['public']['readings'][k]]
def write_csv(path,rows):
    if not rows:return
    with Path(path).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def fitted():
    cases=[c for c in json.loads((ROOT/'cases.json').read_text()) if c['split']=='development'];rec=records('development');e=fit(cases,rec);save(ROOT/'estimator.json',e)
    x=np.array([vector(c) for c in cases]);mean=x.mean(0);std=x.std(0);std[std<1e-9]=1
    centers={label:((x[[c['source_label']==label for c in cases]]-mean)/std).mean(0).tolist() for label in LABELS}
    save(ROOT/'baseline.json',dict(mean=mean.tolist(),std=std.tolist(),centers=centers,training_cases=[c['case_id'] for c in cases]))
    print(json.dumps(e,indent=2))
def baseline(c,b):
    x=(np.array(vector(c))-b['mean'])/b['std'];return min(LABELS,key=lambda l:float(np.sum((x-b['centers'][l])**2)))
def analyze(verify=False):
    e=json.loads((ROOT/'estimator.json').read_text());assert e['sha256']==digest({k:v for k,v in e.items() if k!='sha256'})
    cases=[c for c in json.loads((ROOT/'cases.json').read_text()) if c['split']=='evaluation'];rec=records('evaluation');b=json.loads((ROOT/'baseline.json').read_text())
    results=[];out=ROOT/'analysis';out.mkdir(exist_ok=True);tracepath=ROOT/'policy_traces.jsonl.gz'
    for run in sorted({c['run_id'] for c in cases}):
        group=[c for c in cases if c['run_id']==run]
        for reviewer,weights,capacity,duration,policy in itertools.product(('model','model_risk','ideal'),('heterogeneous','uniform'),(1,2),(1,2,3),POLICIES):
            results.append(simulate(group,rec,e,policy,duration,capacity,reviewer,weights))
    if verify:
        with gzip.open(tracepath,'rt') as f:old=[json.loads(s) for s in f]
        assert [without_timing(x) for x in results]==[without_timing(x) for x in old]
        print('Verified',len(results),'policy traces');return
    with gzip.open(tracepath,'wt') as f:
        for r in results:f.write(json.dumps(r)+'\n')
    episodes=[{k:v for k,v in r.items() if k not in ('events','jobs','sequence')} for r in results];write_csv(out/'episodes.csv',episodes)
    jobs=[]
    for c in cases:
        p=parse(rec[c['case_id']]['proposal']);r=parse(rec[c['case_id']]['review']);truth=c['source_label'];pred=e['bins'][p]['prediction'];base=baseline(c,b)
        jobs.append(dict(case_id=c['case_id'],run_id=c['run_id'],mode=c['source_mode'],truth=truth,proposal=p,review=r,initial_correct=int(p==truth),review_correct=int(r==truth),correction=int(p!=truth and r==truth),harm=int(p==truth and r!=truth and r!='invalid'),preserved_correct=int(p==truth and (r==truth or r=='invalid')),unresolved_wrong=int(p!=truth and r!=truth),proposal_failure=int(p=='invalid'),review_failure=int(r=='invalid'),abstention=int(r=='abstain'),risk=pred['risk'],predicted_gain=pred['gain'],brier=(pred['risk']-int(p!=truth))**2,baseline=base,baseline_correct=int(base==truth)))
    write_csv(out/'diagnoses.csv',jobs)
    runs=sorted({c['run_id'] for c in cases});rng=np.random.default_rng(20260917)
    # Stratify by mode; one resampling matrix shared by every matched condition.
    groups=[[i for i,run in enumerate(runs) if next(c['source_mode'] for c in cases if c['run_id']==run)==mode] for mode in ('SZCAV','SZVAV')]
    indices=np.concatenate([rng.choice(g,(2000,len(g)),replace=True) for g in groups],axis=1)
    summaries=[];paired=[];diffs=[]
    for reviewer,weights,capacity,duration in itertools.product(('model','model_risk','ideal'),('heterogeneous','uniform'),(1,2),(1,2,3)):
        condition=dict(reviewer=reviewer,weights=weights,capacity=capacity,duration=duration)
        subset=[r for r in results if all(r[k]==v for k,v in condition.items())]
        for policy in POLICIES:
            rows=sorted([r for r in subset if r['policy']==policy],key=lambda r:r['run_id']);loss=np.array([r['loss'] for r in rows]);correct=np.array([r['correct']/3 for r in rows]);ci=np.quantile(loss[indices].mean(1),[.025,.975]);cci=np.quantile(correct[indices].mean(1),[.025,.975])
            summaries.append(dict(**condition,policy=policy,n_runs=len(runs),mean_loss=float(loss.mean()),ci_low=ci[0],ci_high=ci[1],correct_rate=float(correct.mean()),correct_low=cci[0],correct_high=cci[1],**{k:sum(r[k] for r in rows) for k in ('correct','corrections','harmful_reviews','unresolved','completed_reviews','review_time','waiting_time','missed_useful')}))
        search={r['run_id']:r for r in subset if r['policy']=='search'}
        for comparator in ('greedy','edf','no_review'):
            comp={r['run_id']:r for r in subset if r['policy']==comparator};delta=np.array([search[run]['loss']-comp[run]['loss'] for run in runs]);ci=np.quantile(delta[indices].mean(1),[.025,.975])
            paired.append(dict(**condition,comparison='search-'+comparator,mean_difference=float(delta.mean()),ci_low=ci[0],ci_high=ci[1],wins=int(sum(delta<0)),ties=int(sum(delta==0)),losses=int(sum(delta>0)),different_sequences=sum(search[run]['sequence']!=comp[run]['sequence'] for run in runs)))
            for run,d in zip(runs,delta):diffs.append(dict(**condition,comparison='search-'+comparator,run_id=run,difference=float(d)))
    write_csv(out/'policy_summary.csv',summaries);write_csv(out/'paired.csv',paired);write_csv(out/'bundle_differences.csv',diffs)
    transitions={k:sum(j[k] for j in jobs) for k in ('initial_correct','review_correct','correction','harm','preserved_correct','unresolved_wrong','proposal_failure','review_failure','abstention','baseline_correct')}
    effort=[ev for r in results if r['policy']=='search' for ev in r['events'] if ev['event']=='dispatch' and ev['eligible']]
    save(out/'diagnostics.json',dict(n_runs=len(runs),n_tasks=len(jobs),transitions=transitions,brier=float(np.mean([j['brier'] for j in jobs])),mean_risk=float(np.mean([j['risk'] for j in jobs])),mean_predicted_gain=float(np.mean([j['predicted_gain'] for j in jobs])),planning_mean_ms=float(np.mean([x['planning_seconds']*1000 for x in effort])) if effort else 0,planning_max_ms=max([x['planning_seconds']*1000 for x in effort] or [0]),max_subsets=max([x['subsets'] for x in effort] or [0]),traces=len(results),independent_equipment=1))
    print(json.dumps(transitions));print([x for x in paired if x['reviewer']=='model' and x['weights']=='heterogeneous' and x['capacity']==1 and x['duration']==2])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['fit','analyze','verify']);a=p.parse_args();fitted() if a.command=='fit' else analyze(a.command=='verify')
