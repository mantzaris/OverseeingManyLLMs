"""Paired source-database analysis; replicates averaged within each source case."""
import csv,json
from pathlib import Path
import numpy as np
from .common import ART,write_json
METRICS=['questions','correct','wrong','unfinished','loss','executions','suppressed','incorrect_suppression','recovered']

def load(path):
    rows=list(csv.DictReader(Path(path).open()))
    for r in rows:
        for k in list(r):
            if k not in ['id','db','domain','kind','condition','method','reason','trace_hash','family']:
                try:r[k]=float(r[k])
                except ValueError:pass
    return rows

def run(root=ART):
    root=Path(root);rows=load(root/'evaluation/episodes.csv');summaries=[];paired=[]
    for condition in sorted({r['condition'] for r in rows}):
        for b in [0,1,2]:
            rr=[r for r in rows if r['condition']==condition and r['budget']==b]
            methods=sorted({r['method'] for r in rr})
            for m in methods:
                z=[r for r in rr if r['method']==m]
                summaries.append(dict(condition=condition,budget=b,method=m,n_replicates=len(z),n_sources=len({r['id'] for r in z}),**{k:sum(r[k] for r in z) for k in METRICS}))
            for baseline in ['recovery_completion','recovery_depth2','full_context','matched_checking']:
                for metric in ['questions','correct','wrong','unfinished','loss','executions']:
                    ids=sorted({r['id'] for r in rr});diff=[]
                    for i in ids:
                        a=[r[metric] for r in rr if r['id']==i and r['method']=='verification'];v=[r[metric] for r in rr if r['id']==i and r['method']==baseline]
                        diff.append(float(np.mean(a)-np.mean(v)))
                    x=np.array(diff);rng=np.random.RandomState(86421);boot=x[rng.randint(0,len(x),(2000,len(x)))].mean(axis=1)
                    paired.append(dict(condition=condition,budget=b,baseline=baseline,metric=metric,mean=float(x.mean()),low=float(np.percentile(boot,2.5)),high=float(np.percentile(boot,97.5)),negative=int((x<0).sum()),ties=int((x==0).sum()),positive=int((x>0).sum()),n=len(x),source_ids=ids,differences=diff))
    write_json(root/'analysis/summary.json',summaries);write_json(root/'analysis/paired.json',paired)
    diag=[]
    for r in rows:
        if r['method']=='verification' and r['budget']==1:
            diag.append({k:r[k] for k in ['id','db','kind','rep','condition','covered_references','references','intended_covered','reference_equal','reference_failure','verification_failures','suppressed','incorrect_suppression']})
    write_json(root/'analysis/coverage.json',diag)
    examples={}
    for label,sign in [('favorable',-1),('tie',0),('unfavorable',1)]:
        for p in paired:
            if p['condition']=='generated' and p['budget']==1 and p['baseline']=='recovery_completion' and p['metric']=='loss':
                eligible=[i for i,v in zip(p['source_ids'],p['differences']) if np.sign(v)==sign];examples[label]=eligible[0] if eligible else None
    write_json(root/'analysis/examples.json',dict(rule='First lexicographic source ID with negative/zero/positive mean loss difference, then both replicas. Missing categories remain absent.',selected=examples))
    print('analysis',len(summaries),len(paired));return summaries,paired
if __name__=='__main__':run()
