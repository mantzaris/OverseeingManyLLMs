"""Stronger secondary completion heuristic, preserving all frozen outcomes."""
import argparse
import itertools
from pathlib import Path
from .common import ART,read,write_json
from .planner import Planner
from .empirical import build
from .evaluate import run,finish,BUDGETS
from .synthetic import generate,decode

from .completion_rule import MinimumCompletion

def evaluate(out=None):
    out=Path(out or ART/'completion_audit');out.mkdir(parents=True,exist_ok=True)
    cases=[c for c in read(ART/'data/public.json') if c['split']=='evaluation'];truth={c['id']:c['target'] for c in read(ART/'data/evaluation_only.json')}
    est=read(ART/'estimator.json');db={d:read(ART/'data'/(d+'_db.json')) for d in ['hotel','restaurant','attraction']};rows=[];traces=[];costs=[]
    for case in cases:
        for rep in range(2):
            prep=read(ART/'prepared'/('evaluation_'+case['id'][:-5]+'_'+str(rep)+'.json'))
            targets={t['id']:{k:truth[case['id']][k] for k in t['required']} for t in case['tasks']}
            for weight in [2.,4.,8.]:
                for budget in BUDGETS:
                    p=build(case,prep,est,error_weight=weight);p=MinimumCompletion(p.factors,p.tasks)
                    row,trace,stats=run(p,targets,truth[case['id']],'minimum_completion',budget,databases=db)
                    meta=dict(id=case['id'],replicate=rep,method='minimum_completion',budget=budget,error_weight=weight)
                    row=dict(meta,failed_calls=sum(c['status']!='ok' or not c['parsed'] for c in prep['calls']),**row)
                    rows.append(row);traces.append(dict(meta,row=row,**trace));costs.append(dict(meta,**stats))
    finish(out,rows,traces,costs)
    case,gold=generate('complementary',2000);f,t=decode(case)
    row,trace,_=run(MinimumCompletion(f,t),gold['targets'],gold['truth'],'minimum_completion',2)
    write_json(out/'transparent_fixture.json',dict(row=row,trace=trace,label='Authored mechanism fixture'))
    print('Secondary baseline audit:',len(rows),'rows')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output');evaluate(p.parse_args().output)
