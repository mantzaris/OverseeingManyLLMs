"""Evaluator only: true targets and simulated responses never enter selection."""
import argparse
import copy
import csv
import gzip
import hashlib
import io
import json
import random
import time
from dataclasses import asdict
from pathlib import Path
from .common import ART,canonical,read,write_json,digest
from .planner import Protocol,Planner,Task,Option,Factor,OTHER,UNRESOLVED
from .synthetic import generate,decode,FAMILIES
from .empirical import build
from .data import norm

BUDGETS=[0,1,2,4,6,'unlimited']
EMPIRICAL_METHODS=['semantic_memory','full_history','one_step','completion','depth2','depth3','generic2','no_scope','request_specific','ideal_depth2']
SYNTHETIC_METHODS=['no_review','memory','uncertainty','depth1','completion','depth2','depth3','generic2','no_scope','request_specific']

def csv_write(path,rows):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def unshare(p):
    factors=[];tasks=[]
    for task in p.tasks:
        keys=sorted(set(k for o in task.options for _,k in o.bindings)|set(k for o in task.options for k,_ in o.gates))
        mapping={k:task.id+'::'+k for k in keys}
        for key in keys:
            old=p.factors[p.index[key]];factors.append(Factor(**dict(old.__dict__,id=mapping[key])))
        options=tuple(Option(tuple((k,mapping[v]) for k,v in o.bindings),tuple((mapping[k],v) for k,v in o.gates)) for o in task.options)
        tasks.append(Task(task.id,options,task.error_weight,task.defer_weight))
    return Planner(factors,tasks,p.response_error,p.unresolved_probability,p.question_penalty,p.width,p.node_limit)

def run(p,targets,truth,method,budget,seed=0,updates=(),databases=None):
    started=time.perf_counter();budget_value=sum(f.cost for f in p.factors)+len(updates) if budget=='unlimited' else budget
    c=Protocol(p,budget_value);plans=[];updates=list(updates);initial=p.terminal(c.state)[0]
    while True:
        q=c.propose(method)
        if p.last_stats:
            plans.append(dict(p.last_stats,question=None if q is None else q['id']))
        if q is None:
            if updates:
                for u in updates:c.revise(**u)
                updates=[];p=c.planner;continue
            break
        key=q['id'].split('::')[-1]
        # Shared exogenous outcomes keyed by source/question, not method/order.
        r=random.Random(int(hashlib.sha256((str(seed)+'/'+key).encode()).hexdigest()[:12],16))
        answer=truth[key]
        if r.random()<p.unresolved_probability:answer=UNRESOLVED
        elif r.random()<p.response_error:
            choices=[v for v in c.planner.factors[c.planner.index[q['id']]].choices if v!=answer and v!=OTHER]
            answer=choices[0] if choices else 'incorrect_response'
        c.answer(answer)
        if updates:
            for u in updates:c.revise(**u)
            updates=[]
        p=c.planner
    outcomes=c.finish();correct=wrong=unfinished=scope_errors=0;details=[]
    for out in outcomes:
        expected=targets[out['task']];values=out['values']
        iscorrect=out['status']=='release' and {k:norm(v) for k,v in values.items()}=={k:norm(v) for k,v in expected.items()}
        output=None
        if databases is not None and out['status']=='release':
            domain=out['task'].replace('_shortlist','');constraints={k.split('.')[1]:norm(v) for k,v in values.items()}
            def query(vals):return sorted(str(r.get('name','unnamed')) for r in databases[domain] if all(norm(r.get(k,''))==v for k,v in vals.items()))
            output=dict(constraints=constraints,matches=query(constraints))
            expected_output=query({k.split('.')[1]:norm(v) for k,v in expected.items()})
            iscorrect=iscorrect and output['matches']==expected_output
        status='unfinished' if out['status']=='defer' else 'correct' if iscorrect else 'incorrect'
        correct+=int(status=='correct');wrong+=int(status=='incorrect');unfinished+=int(status=='unfinished')
        if out['status']=='release':
            task=next(t for t in p.tasks if t.id==out['task']);opt=task.options[out['option']]
            wrong_scope=sum(truth[k.split('::')[-1]]!=v for k,v in opt.gates)
            scope_errors+=wrong_scope
            if wrong_scope and status=='correct':
                status='incorrect';correct-=1;wrong+=1
        details.append(dict(out,status=status,expected=expected,output=output))
    weights={t.id:t for t in p.tasks}
    loss=sum(weights[d['task']].error_weight if d['status']=='incorrect' else weights[d['task']].defer_weight if d['status']=='unfinished' else 0 for d in details)
    asked=[e['id'].split('::')[-1] for e in c.events if e['kind']=='answer_received']
    row=dict(tasks=len(p.tasks),project_correct=int(correct==len(p.tasks)),correct=correct,incorrect=wrong,unfinished=unfinished,
        loss=loss,questions=c.spent,distinct_questions=len(set(asked)),repeated_questions=len(asked)-len(set(asked)),
        incorrect_scope_transfers=scope_errors,unresolved_responses=sum(e['kind']=='answer_received' and e['value']==UNRESOLVED for e in c.events),scope_questions=sum(e['kind']=='question_shown' and e['question']['kind']=='scope' for e in c.events),initial_predicted_loss=initial,final_predicted_loss=p.terminal(c.state)[0],
        predicted_benefit=initial-p.terminal(c.state)[0],realized_benefit=None,
        planning_nodes=sum(s['nodes'] for s in plans),planning_caps=sum(s['capped'] for s in plans))
    # No-question realized counterfactual uses the same input beliefs and targets,
    # rather than an evaluator-guided action. Set outside for paired rows.
    stats=dict(episode_seconds=time.perf_counter()-started,planning_seconds=sum(s['seconds'] for s in plans),
               planning_calls=len(plans),max_nodes=max([s['nodes'] for s in plans] or [0]))
    cleanplans=[{k:v for k,v in s.items() if k!='seconds'} for s in plans]
    return row,dict(events=c.events,outcomes=details,plans=cleanplans),stats

def evaluate_empirical(split='evaluation',out=None):
    out=Path(out or ART/split);out.mkdir(parents=True,exist_ok=True)
    cases=[c for c in read(ART/'data/public.json') if c['split']==split]
    gold={x['id']:x['target'] for x in read(ART/'data/evaluation_only.json')};est=read(ART/'estimator.json')
    assert est['sha256']==digest({k:v for k,v in est.items() if k!='sha256'})
    db={d:read(ART/'data'/(d+'_db.json')) for d in ['hotel','restaurant','attraction']}
    rows=[];traces=[];costs=[]
    for case in cases:
        for rep in range(2):
            prep=read(ART/'prepared'/('%s_%s_%d.json'%(split,case['id'][:-5],rep)))
            targets={t['id']:{k:gold[case['id']][k] for k in t['required']} for t in case['tasks']}
            for ew in [2.,4.,8.]:
                for method in EMPIRICAL_METHODS:
                    backend='history' if method=='full_history' else 'memory'
                    for budget in BUDGETS:
                        p=build(case,prep,est,backend,ideal=gold[case['id']] if method=='ideal_depth2' else None,error_weight=ew)
                        if method=='request_specific':p=unshare(p)
                        policy={'semantic_memory':'memory','full_history':'memory','one_step':'depth1','ideal_depth2':'depth2','request_specific':'depth2'}.get(method,method)
                        row,trace,stats=run(p,targets,gold[case['id']],policy,budget,databases=db)
                        meta=dict(id=case['id'],replicate=rep,method=method,budget=budget,error_weight=ew)
                        row=dict(meta,failed_calls=sum(c['status']!='ok' or not c['parsed'] for c in prep['calls']),**row)
                        rows.append(row);traces.append(dict(meta,row=row,**trace));costs.append(dict(meta,**stats))
        print('Replayed',case['id'],flush=True)
    finish(out,rows,traces,costs)

def evaluate_synthetic(out=None,development=False):
    out=Path(out or ART/'synthetic');out.mkdir(parents=True,exist_ok=True)
    seeds=range(2000,2004) if development else range(5000,5020)
    rows=[];traces=[];costs=[];references=[]
    families=FAMILIES+['grid_%s_arity_%d'%(o,a) for o in ['none','one','full'] for a in [1,2,3]]
    for family in families:
        current_seeds=(range(2100,2102) if development else range(6000,6012)) if family.startswith('grid_') else seeds
        for seed in current_seeds:
            case,gold=generate(family,seed);factors,tasks=decode(case)
            for method in SYNTHETIC_METHODS:
                for budget in BUDGETS:
                    p=Planner(factors,tasks,case['response_error'],case['unresolved_probability'])
                    if method=='request_specific':p=unshare(p)
                    updates=case['updates']
                    if method=='request_specific':
                        updates=[dict(u,key=f.id) for u in updates for f in p.factors if f.id.split('::')[-1]==u['key']]
                    row,trace,stats=run(p,gold['targets'],gold['truth'],'depth2' if method=='request_specific' else method,budget,seed,updates)
                    meta=dict(id=case['id'],family=family,seed=seed,method=method,budget=budget)
                    rows.append(dict(meta,**row));traces.append(dict(meta,row=rows[-1],**trace));costs.append(dict(meta,**stats))
            if len(factors)<=6 and seed<5005 and not updates and family not in ['revision','revocation']:
                for budget in [1,2,3,4]:
                    for depth,construction,width in [(1,'dependency',8),(2,'dependency',8),(2,'dependency',2),(3,'dependency',8),(budget,'exact',8)]:
                        p=Planner(factors,tasks,case['response_error'],case['unresolved_probability'],width=width,node_limit=1000000)
                        a=p.select(p.initial,budget,depth,construction)
                        if construction=='exact':
                            from .exact import solve
                            ref=solve(p,p.initial,budget)
                            assert abs(ref['value']-p.last_stats['expected_plan_loss'])<1e-8
                            assert ref['action']==a
                        from .exact import solve
                        same_depth=solve(p,p.initial,budget,depth)
                        references.append(dict(id=case['id'],budget=budget,construction=construction,reference_same_depth=same_depth['value'],pruning_gap=p.last_stats['expected_plan_loss']-same_depth['value'],
                                               action=None if a is None else p.factors[a].id,**p.last_stats))
        print('Synthetic',family,flush=True)
    finish(out,rows,traces,costs);csv_write(out/'exact_reference.csv',references)

def finish(out,rows,traces,costs):
    # Matched zero-budget outcomes define realized loss prevented. Whole task sets
    # and all failures are retained; not a conditional-only success score.
    base={(r['id'],r.get('replicate',0),r['method'],r.get('error_weight',4)):r['loss'] for r in rows if r['budget']==0}
    for r,t in zip(rows,traces):
        r['realized_benefit']=base[(r['id'],r.get('replicate',0),r['method'],r.get('error_weight',4))]-r['loss'];t['row']=r
    csv_write(out/'episodes.csv',rows);csv_write(out/'costs.csv',costs)
    with (out/'traces.jsonl.gz').open('wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',mtime=0,filename='') as z:
            for t in traces:z.write((canonical(t)+'\n').encode())
    write_json(out/'replay_digest.json',dict(rows=len(rows),sha256=digest(traces),new_generations=0))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--kind',choices=['development','evaluation','synthetic','synthetic_development'],required=True);p.add_argument('--output');a=p.parse_args()
    if a.kind.startswith('synthetic'):evaluate_synthetic(a.output,development=a.kind.endswith('development'))
    else:evaluate_empirical(a.kind,a.output)
