#!/usr/bin/env python3
"""Rescore three frozen risks on existing development trajectories; no new rollouts."""
from collections import defaultdict
from dataclasses import replace
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from overseeing.domain import Scenario,ReviewRequest
from overseeing.io import read_events,write_csv,write_json
from overseeing.policies import choose
from overseeing.research_risk import load_risk
root=Path(__file__).resolve().parent.parent;out=root/'artifacts/stage4_research/offline_risk';out.mkdir(exist_ok=True)
estimators={name:load_risk(name,root/'artifacts/stage2_development/run/estimator.json') for name in ('frozen','pooled','analytical')}
paths=[('original',p) for p in sorted((root/'artifacts/stage2_development/run/validation').glob('*/*/events.jsonl'))]
paths += [('competition',p) for p in sorted((root/'artifacts/stage3_competition/run').glob('*/*/*/events.jsonl'))]
rows,choices=[],[]
for workload,path in paths:
    events=read_events(path);header=events[0];scenario=Scenario.from_record(header['scenario']);jobs={j.public.job_id:j for j in scenario.jobs}
    proposals={e['job_id']:e for e in events if e['event']=='proposal'}
    for job_id,event in proposals.items():
        job=jobs[job_id];label=int(event['primary']!=job.correct_action)
        for name,estimator in estimators.items():
            p=estimator.predict(job.public,event['primary'],event['secondary'])
            rows.append(dict(workload=workload,seed=scenario.seed,policy=header['policy'],review_ticks=header['review_ticks'],job_id=job_id,estimator=name,prediction=p,initial_error=label,brier=(p-label)**2))
    for event in events:
        if event['event']!='dispatch_considered':continue
        requests=[ReviewRequest(**r) for r in event['eligible']]
        if len(requests)<2:continue
        selected={}
        for name,estimator in estimators.items():
            queue=tuple(replace(r,p_error=estimator.predict(jobs[r.job_id].public,proposals[r.job_id]['primary'],proposals[r.job_id]['secondary'])) for r in requests)
            for policy in ('greedy','delay'):selected[name+'_'+policy]=choose(policy,queue,event['tick'])
        choices.append(dict(workload=workload,seed=scenario.seed,observed_policy=header['policy'],review_ticks=header['review_ticks'],tick=event['tick'],eligible_count=len(requests),**selected))
summaries=[]
groups=defaultdict(list)
for r in rows:groups[(r['workload'],r['policy'],r['review_ticks'],r['estimator'])].append(r)
for key,group in groups.items():
    n=len(group);summaries.append(dict(zip(('workload','policy','review_ticks','estimator'),key),examples=n,initial_error_rate=sum(r['initial_error'] for r in group)/n,mean_prediction=sum(r['prediction'] for r in group)/n,brier=sum(r['brier'] for r in group)/n))
reliability=[];groups=defaultdict(list)
for r in rows:groups[(r['workload'],r['estimator'],round(r['prediction'],12))].append(r)
for key,group in groups.items():reliability.append(dict(workload=key[0],estimator=key[1],prediction=key[2],examples=len(group),observed_error_rate=sum(r['initial_error'] for r in group)/len(group),note='Repeated policy trajectories, not independent observations'))
choice_summaries=[]
for workload in ('original','competition'):
    for duration in (1,2):
        selected=[r for r in choices if r['workload']==workload and r['review_ticks']==duration]
        for policy in ('greedy','delay'):
            for estimate in ('pooled','analytical'):
                choice_summaries.append(dict(workload=workload,review_ticks=duration,policy=policy,alternative=estimate,competitive_states=len(selected),changed_first_choices=sum(r['frozen_'+policy]!=r[estimate+'_'+policy] for r in selected)))
for name,data in (('predictions',rows),('prediction_summary',summaries),('reliability',reliability),('dispatch_choices',choices),('choice_summary',choice_summaries)):write_csv(out/(name+'.csv'),data)
write_json(out/'summary.json',dict(episodes=len(paths),job_pairs=len(rows)//3,fit_performed=False,choice_summary=choice_summaries,note='Offline rescoring on saved development trajectories cannot establish counterfactual allocation performance.'))
print(json.dumps(dict(episodes=len(paths),job_pairs=len(rows)//3,choices=choice_summaries),indent=2))
