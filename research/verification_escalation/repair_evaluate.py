"""Evaluator-only targets, simulated answers and grouped outcome accounting."""
import argparse,csv,json,time
from pathlib import Path
from .common import ART,read,write_json,digest
from .repair_data import public_task,intent_index
ART=ART/'repair'
from .engine import MachineBudget,execute,equivalent
from .controller import Controller,METHODS,candidates
BUDGETS=[0,1,2]

def strip_time(value):
    if isinstance(value,dict):return {k:strip_time(v) for k,v in value.items() if k not in ['seconds','controller_seconds']}
    if isinstance(value,list):return [strip_time(v) for v in value]
    return value

def score(case,rep,prepared,condition,method,budget):
    recovery=condition=='source_recovery';task=public_task(case,rep,recovery)
    p=prepared['calls']
    if recovery:p={k:prepared.get('recovery') for k in ['candidates','audit']}
    if condition=='reference_candidates':
        obj={'candidates':[dict(meaning='Privileged reference interpretation '+str(i+1),sql=q) for i,q in enumerate(case['refs'])],'unrepresented_possible':False}
        p=dict(candidates=obj,audit=obj,coverage='complete_enumeration')
    c=Controller([task],{task['id']:p},budget,24,method)
    q=c.next_question()
    if q:
        answer=prepared.get('answered') or {};sql=answer.get('sql')
        if condition=='reference_candidates':sql=case['refs'][intent_index(case,rep)]
        c.answer(q,dict(sql_by_task={task['id']:sql}) if isinstance(sql,str) else None)
    c.inspect();out=c.result();r=out['records'][task['id']]
    refs=[execute(case['snapshot'],sql,MachineBudget(1),task['contract']['ordered']) for sql in case['refs']]
    target=refs[intent_index(case,rep)];released=r['status']=='released';correct=released and target['status']=='ok' and r['result']['table_hash']==target['table_hash']
    generated=[execute(case['snapshot'],x['sql'],MachineBudget(1),task['contract']['ordered']) for x in candidates(p)[0]]
    hashes={x.get('table_hash') for x in generated if x['status']=='ok'}
    covered=sum(x['status']=='ok' and x['table_hash'] in hashes for x in refs)
    row=dict(id=case['id'],db=case['db'],domain=case['domain'],kind=case['kind'],rep=rep,condition=condition,method=method,budget=budget,questions=out['questions'],correct=int(correct),wrong=int(released and not correct),unfinished=int(not released),project_correct=int(correct),loss=4*int(released and not correct)+int(not released),recovered=int(r['reason']=='source_recovery'),suppressed=int(r['reason']=='outcome_agreement'),incorrect_suppression=int(r['reason']=='outcome_agreement' and not correct),covered_references=covered,references=len(refs),intended_covered=int(target['status']=='ok' and target['table_hash'] in hashes),reference_equal=int(equivalent(refs)),reference_failure=int(target['status']!='ok'),verification_failures=sum(x['status']!='ok' for x in generated),executions=out['executions'],controller_seconds=out['controller_seconds'],reason=r['reason'],trace_hash=digest(strip_time(out)),repeated_questions=0,incorrect_scope_transfers=0)
    # Compact public evidence has hashes, generated SQL and outcomes, no source rows.
    trace=strip_time(out)
    for record in trace['records'].values():
        if 'result' in record:record['result'].pop('table',None)
    return row,trace

def run(split='evaluation',output=None,revision='v2'):
    root=Path(output) if output else ART/split;root.mkdir(parents=True,exist_ok=True);rows=[];traces={}
    cases=read(ART/'private'/'cases.json')[split]
    for n,case in enumerate(cases):
        reps=range(1 if split=='development' else 2)
        for rep in reps:
            key='repair_'+split+('_'+revision if revision else '')+'_'+case['id']+'_r'+str(rep)
            path=ART/'prepared'/(key+'.json')
            if not path.exists():continue
            prep=read(path)
            conditions=['generated','reference_candidates']
            if 'recovery' in prep:conditions.append('source_recovery')
            for condition in conditions:
                for method in METHODS:
                    for b in BUDGETS:
                        row,trace=score(case,rep,prep,condition,method,b);rows.append(row)
                        traces['|'.join(map(str,[case['id'],rep,condition,method,b]))]=trace
    if rows:
        with (root/'episodes.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    write_json(root/'traces.json',traces)
    summary=[]
    for condition in sorted({r['condition'] for r in rows}):
        for method in METHODS:
            for budget in BUDGETS:
                rr=[r for r in rows if (r['condition'],r['method'],r['budget'])==(condition,method,budget)]
                if rr:summary.append(dict(condition=condition,method=method,budget=budget,n=len(rr),**{k:sum(r[k] for r in rr) for k in ['questions','correct','wrong','unfinished','loss','recovered','suppressed','incorrect_suppression','executions']}))
    write_json(root/'summary.json',summary);print('rows',len(rows));return rows
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('split',choices=['development','evaluation']);p.add_argument('--revision',default='v2');p.add_argument('--output');a=p.parse_args();run(a.split,a.output,a.revision)
