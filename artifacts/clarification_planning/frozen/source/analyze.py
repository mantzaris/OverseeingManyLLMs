"""Frozen paired analyses; source dialogues, not roles or replay rows, are units."""
import argparse
import csv
import gzip
import json
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np
from .common import ART,read,write_json
from .evaluate import csv_write
from .empirical import predictions,build

SEED=82164
RESAMPLES=2000
METRICS=['loss','project_correct','correct','incorrect','unfinished','questions','repeated_questions','incorrect_scope_transfers','unresolved_responses','scope_questions','predicted_benefit','realized_benefit']

def rows(path):
    out=[]
    for r in csv.DictReader(Path(path).open()):
        for k,v in list(r.items()):
            try:r[k]=float(v)
            except (TypeError,ValueError):pass
        out.append(r)
    return out

def interval(v,indices):
    v=np.array(v,dtype=float);means=v[indices].mean(axis=1)
    return [float(v.mean()),float(np.quantile(means,.025)),float(np.quantile(means,.975))]

def paired_summary(data,output):
    ids=sorted({r['id'] for r in data});rng=np.random.default_rng(SEED)
    indices=rng.integers(0,len(ids),(RESAMPLES,len(ids)))
    grouped=defaultdict(list)
    for r in data:grouped[(r['id'],r['method'],r['budget'],r['error_weight'])].append(r)
    means={k:{m:np.mean([r[m] for r in rs]) for m in METRICS} for k,rs in grouped.items()}
    methods=sorted({r['method'] for r in data});summaries=[];contrasts=[];individual=[]
    for ew in [2.,4.,8.]:
        for b in [0.,1.,2.,4.,6.,'unlimited']:
            for method in methods:
                for metric in METRICS:
                    v=[means[(id,method,b,ew)][metric] for id in ids]
                    mean,lo,hi=interval(v,indices)
                    summaries.append(dict(method=method,budget=b,error_weight=ew,metric=metric,mean=mean,lo=lo,hi=hi,dialogues=len(ids)))
            for baseline in ['one_step','semantic_memory','completion','full_history','depth3','generic2','no_scope','request_specific','ideal_depth2']:
                for metric in ['loss','project_correct','correct','incorrect','unfinished','questions']:
                    v=[means[(id,'depth2',b,ew)][metric]-means[(id,baseline,b,ew)][metric] for id in ids]
                    mean,lo,hi=interval(v,indices)
                    contrasts.append(dict(baseline=baseline,budget=b,error_weight=ew,metric=metric,difference=mean,lo=lo,hi=hi,
                        negative=sum(x<-1e-10 for x in v),ties=sum(abs(x)<=1e-10 for x in v),positive=sum(x>1e-10 for x in v),dialogues=len(ids)))
                    if metric=='loss':
                        for id,x in zip(ids,v):individual.append(dict(id=id,baseline=baseline,budget=b,error_weight=ew,loss_difference=x))
    csv_write(output/'summary.csv',summaries);csv_write(output/'paired.csv',contrasts);csv_write(output/'individual.csv',individual)
    return summaries,contrasts

def empirical_diagnostics(out):
    cases=[c for c in read(ART/'data/public.json') if c['split']=='evaluation'];gold={c['id']:c['target'] for c in read(ART/'data/evaluation_only.json')}
    est=read(ART/'estimator.json');predrows=[];structure=[];fields=[]
    for case in cases:
        for rep in range(2):
            prep=read(ART/'prepared'/('evaluation_'+case['id'][:-5]+'_'+str(rep)+'.json'))
            for backend in ['extract','memory','history']:
                pred=predictions(case,prep,backend)
                for key in case['fields']:
                    probability=est['estimates'][backend]['domains'][key.split('.')[0]]['probability'] if key in pred else 0.
                    correct=int(pred.get(key)==gold[case['id']][key]);fields.append(dict(id=case['id'],replicate=rep,backend=backend,key=key,
                        supplied=int(key in pred),correct=correct,probability=probability,brier=(probability-correct)**2))
            p=build(case,prep,est);state=p.initial
            a=p.select(state,2,1);v1=p.last_stats['expected_plan_loss']
            b=p.select(state,2,2);v2=p.last_stats['expected_plan_loss']
            supplied=predictions(case,prep,'memory')
            structure.append(dict(id=case['id'],replicate=rep,tasks=len(case['tasks']),fields=len(case['fields']),
                multi_field_tasks=sum(len(t['required'])>=2 for t in case['tasks']),
                tasks_missing_two_values=sum(sum(k not in supplied for k in t['required'])>=2 for t in case['tasks']),
                shared_registered_decisions=0,depth1_question=None if a is None else p.factors[a].id,
                depth2_question=None if b is None else p.factors[b].id,first_question_differs=int(a!=b),
                predicted_two_step_advantage=v1-v2,
                zero_one_step_positive_two_step=int(p.terminal(state)[0]-v1<1e-10 and p.terminal(state)[0]-v2>1e-10)))
    csv_write(out/'prediction_fields.csv',fields);csv_write(out/'structure.csv',structure)
    for backend in ['extract','memory','history']:
        for domain in ['all','hotel','restaurant','attraction']:
            g=[r for r in fields if r['backend']==backend and (domain=='all' or r['key'].startswith(domain+'.'))]
            if not g:continue
            predrows.append(dict(backend=backend,domain=domain,fields=len(g),supplied=sum(r['supplied'] for r in g),correct=sum(r['correct'] for r in g),
                 brier=np.mean([r['brier'] for r in g]),mean_probability=np.mean([r['probability'] for r in g]),observed_accuracy=np.mean([r['correct'] for r in g])))
    csv_write(out/'prediction_summary.csv',predrows)


def analyze(root=None):
    root=Path(root or ART);out=root/'analysis';out.mkdir(parents=True,exist_ok=True)
    empirical=rows(root/'evaluation/episodes.csv');summaries,contrasts=paired_summary(empirical,out)
    syn=rows(root/'synthetic/episodes.csv');groups=defaultdict(list)
    for r in syn:groups[(r['family'],r['method'],r['budget'])].append(r)
    ss=[]
    for (family,method,b),g in sorted(groups.items(),key=lambda x:str(x[0])):
        ss.append(dict(family=family,method=method,budget=b,instances=len(g),**{m:np.mean([r[m] for r in g]) for m in METRICS}))
    csv_write(out/'synthetic_summary.csv',ss)
    sc=[]
    for family in sorted({r['family'] for r in syn}):
        for b in [0.,1.,2.,4.,6.,'unlimited']:
            for baseline in ['depth1','completion','generic2','depth3','no_scope','request_specific','memory']:
                a={r['id']:r for r in groups[(family,'depth2',b)]};z={r['id']:r for r in groups[(family,baseline,b)]}
                diffs=[a[k]['loss']-z[k]['loss'] for k in sorted(a)]
                sc.append(dict(family=family,budget=b,baseline=baseline,loss_difference=np.mean(diffs),wins=sum(v<0 for v in diffs),ties=sum(v==0 for v in diffs),losses=sum(v>0 for v in diffs),instances=len(diffs)))
    csv_write(out/'synthetic_paired.csv',sc)
    empirical_diagnostics(out)
    costs=[]
    for application in ['evaluation','synthetic']:
        cg=defaultdict(list)
        for r in rows(root/application/'costs.csv'):cg[r['method']].append(r)
        for method,g in cg.items():
            v=[r['episode_seconds'] for r in g]
            costs.append(dict(application=application,method=method,episodes=len(g),mean_episode_ms=1000*np.mean(v),p95_episode_ms=1000*np.quantile(v,.95),
                              summed_episode_seconds=sum(v),max_nodes=max(r['max_nodes'] for r in g)))
    csv_write(out/'computation.csv',costs)
    # First qualifying ID, not largest effect; generation replicate zero displayed.
    examples={}
    individual=rows(out/'individual.csv')
    for baseline in ['one_step','semantic_memory','completion']:
        g=[r for r in individual if r['baseline']==baseline and r['budget']==2 and r['error_weight']==4]
        for name,rule in [('benefit',lambda x:x<0),('tie',lambda x:x==0),('unfavorable',lambda x:x>0)]:
            ids=sorted(r['id'] for r in g if rule(r['loss_difference']))
            examples[baseline+'_'+name]=ids[0] if ids else None
    failures=sorted(r['id'] for r in empirical if r['failed_calls']>0)
    examples['preparation_failure']=failures[0] if failures else None
    write_json(out/'examples.json',dict(rule='First lexicographic dialogue whose replicate-mean primary loss difference qualifies; show replicate 0. Failure: first source ID with any retained failed call.',selection=examples))
    primary=[r for r in contrasts if r['budget']==2 and r['error_weight']==4 and r['metric']=='loss']
    write_json(out/'primary.json',dict(unit='source dialogue',replicates_averaged=2,resamples=RESAMPLES,analysis_seed=SEED,
                                     primary=[r for r in primary if r['baseline'] in ['one_step','semantic_memory']],secondary=primary))
    print(json.dumps(primary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root');analyze(p.parse_args().root)
