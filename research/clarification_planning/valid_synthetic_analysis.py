"""Valid source rows with the explicitly labeled scope repair; no replacement of originals."""
from collections import defaultdict
import numpy as np
from .common import ART,write_json
from .analyze import rows,METRICS
from .evaluate import csv_write
from .planner import Factor,Task,Option,Planner
from .synthetic import generate,decode
from .exact import solve

def run(root=None):
    global ART
    if root is not None:
        from pathlib import Path
        ART=Path(root)
    out=ART/'analysis';original=rows(ART/'synthetic/episodes.csv');repair=rows(ART/'scope_consistency_repair/episodes.csv')
    valid=[r for r in original if r['family'] not in ['scope_exception','wrong_sharing']]+repair
    grouped=defaultdict(list)
    for r in valid:grouped[(r['family'],r['method'],r['budget'])].append(r)
    summary=[];paired=[]
    for (family,method,budget),g in sorted(grouped.items(),key=lambda x:str(x[0])):
        summary.append(dict(family=family,method=method,budget=budget,instances=len(g),
            source='post_freeze_oracle_repair' if family in ['scope_exception','wrong_sharing'] else 'frozen_original',
            **{m:np.mean([r[m] for r in g]) for m in METRICS}))
    for family in sorted({r['family'] for r in valid}):
        for budget in [0.,1.,2.,4.,6.,'unlimited']:
            for baseline in ['depth1','completion','generic2','depth3','no_scope','request_specific','memory']:
                a={r['id']:r for r in grouped[(family,'depth2',budget)]};b={r['id']:r for r in grouped[(family,baseline,budget)]}
                d=[a[k]['loss']-b[k]['loss'] for k in a]
                paired.append(dict(family=family,budget=budget,baseline=baseline,loss_difference=np.mean(d),wins=sum(v<0 for v in d),ties=sum(v==0 for v in d),losses=sum(v>0 for v in d)))
    csv_write(out/'synthetic_valid_summary.csv',summary);csv_write(out/'synthetic_valid_paired.csv',paired)
    case,_=generate('complementary',4);f,t=decode(case)
    for i,weight in enumerate([.8,.7,.6]):
        key='a'+str(i);f.append(Factor(key,('A','B'),(.5,.5)));t.append(Task(key,(Option(((key,key),)),),4.,weight))
    p=Planner(f,t,width=2);chosen=p.select(p.initial,2,2);ref=solve(p,p.initial,2)
    write_json(out/'pruning_witness.json',dict(label='Authored post-freeze proof witness, not prevalence evidence',
        factors=6,budget=2,width=2,chosen=p.factors[chosen].id,exact_chosen=p.factors[ref['action']].id,
        approximate_expected_loss=p.last_stats['expected_plan_loss'],exact_expected_loss=ref['value'],gap=p.last_stats['expected_plan_loss']-ref['value']))
    print('Valid analysis view:',len(valid),'rows; 348 original instances + 40 corrected scope instances')
if __name__=='__main__':run()
