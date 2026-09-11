"""Constructed SQL workloads, distinct goals and explicit shared dependencies."""
import copy,random,csv
from pathlib import Path
from .common import ART,write_json,digest
from .engine import MachineBudget,execute
from .controller import Controller,METHODS
from .evaluate import strip_time
FAMILIES=['available_source','missing_preference','equal_snapshot','different_snapshot','shared_decision','scope_exception','unaffected_work','omitted_intent','correlated_omission','irrelevant_source','snapshot_change','coincidental_equality','failed_query','empty_trap','verification_waste','process_requirement','unresolved_answer']

def instance(family,seed):
    rng=random.Random(seed);base=rng.randint(10,30)
    equal=family in ['equal_snapshot','snapshot_change','coincidental_equality','verification_waste','process_requirement']
    records=[(1,base+100,4),(2,base+120,4 if equal else 1),(3,base,1),(4,base+10,1 if equal else 5)]
    snapshot='CREATE TABLE customers(id INTEGER PRIMARY KEY, spend INTEGER NOT NULL, orders INTEGER NOT NULL);'+''.join('INSERT INTO customers VALUES(%d,%d,%d);'%x for x in records)
    queries=['SELECT id FROM customers WHERE spend >= 100','SELECT id FROM customers WHERE orders >= 3']
    hidden=seed%2
    def task(tid,qs,decision='segment',scope='Atlas/segment'):
        return dict(id=tid,request='Prepare the eligible customer '+tid,schema='customers(id, spend, orders)',snapshot=snapshot,scope=scope,version=1,exceptions=[],decision_id=decision,sources=[],contract={'kind':'snapshot_table','ordered':False}),qs
    t,qs=task('export',queries);tasks=[t];qsets=[qs]
    if family in ['shared_decision','scope_exception','unaffected_work','correlated_omission']:
        t2,q2=task('count',[q.replace('SELECT id','SELECT count(*)') for q in queries]);tasks.append(t2);qsets.append(q2)
        if family=='scope_exception':t2.update(scope='Partner/count',decision_id='partner_segment')
    if family=='unaffected_work':
        t3,q3=task('inventory',['SELECT count(*) FROM customers']*2,decision='inventory',scope='Inventory');tasks.append(t3);qsets.append(q3)
    prep={};targets={};answers={}
    for i,(t,qs) in enumerate(zip(tasks,qsets)):
        intent=(1-hidden) if family=='scope_exception' and i==1 else hidden
        targets[t['id']]=qs[intent]
        candidate_qs=list(qs)
        if family in ['omitted_intent','correlated_omission']:
            candidate_qs=[qs[1-intent],qs[1-intent]+' AND 1=1']
        if family=='failed_query':candidate_qs[1]='SELECT missing FROM customers'
        if family=='empty_trap':candidate_qs=[q+' AND id<0' for q in candidate_qs]
        if family=='process_requirement':t['contract']['explicit_semantic_choice_required']=True
        obj={'candidates':[{'sql':q,'meaning':['spending threshold','order threshold'][j]} for j,q in enumerate(candidate_qs)],'unrepresented_possible':False}
        if family=='available_source' or (family=='unaffected_work' and i==2):
            text='Use the '+('spending' if intent==0 else 'order')+' rule for this scope.'
            t['sources']=[dict(id='S1',text=text,status='explicit_user_requirement',scope=t['scope'],version=1)]
            obj['source_quote_sha256']=digest(text);obj['candidates']=[dict(sql=qs[intent],meaning='Recovered source requirement')]
        if family=='irrelevant_source':
            t['sources']=[dict(id='S1',text='Use spending.',status='explicit_user_requirement',scope='Other project',version=1)];obj['source_quote_sha256']=digest('Use spending.')
        prep[t['id']]=dict(candidates=copy.deepcopy(obj),audit=copy.deepcopy(obj))
        answers[t['id']]=qs[intent]
    return tasks,prep,targets,answers

def run(output=None,seeds=range(7200,7216)):
    root=Path(output) if output else ART/'synthetic';root.mkdir(parents=True,exist_ok=True);rows=[];traces={}
    for family in FAMILIES:
        for seed in seeds:
            tasks,prep,targets,answers=instance(family,seed)
            for method in METHODS:
                for budget in [0,1,2]:
                    c=Controller(tasks,prep,budget,48,method)
                    if family=='snapshot_change':
                        c.inspect()
                        for t in tasks:c.revise(t['id'],snapshot=t['snapshot']+'UPDATE customers SET orders=0 WHERE id=1;')
                    while True:
                        q=c.next_question()
                        if q is None:break
                        response=None if family=='unresolved_answer' else {'sql_by_task':answers}
                        c.answer(q,response)
                    c.inspect();out=c.result();correct=wrong=unfinished=0
                    for t in c.tasks:
                        r=out['records'][t['id']];target=execute(t['snapshot'],targets[t['id']],MachineBudget(1))
                        if r['status']!='released':unfinished+=1
                        elif target['status']=='ok' and r['result']['table_hash']==target['table_hash']:correct+=1
                        else:wrong+=1
                    row=dict(family=family,seed=seed,method=method,budget=budget,goals=len(tasks),correct=correct,wrong=wrong,unfinished=unfinished,questions=out['questions'],project_correct=int(correct==len(tasks)),executions=out['executions'],loss=4*wrong+unfinished,suppressed=sum(r['reason']=='outcome_agreement' for r in out['records'].values()),recovered=sum(r['reason']=='source_recovery' for r in out['records'].values()),repeated_questions=max(0,out['questions']-len({e['decision'] for e in out['events'] if e['event']=='answer'})),trace_hash=digest(strip_time(out)))
                    rows.append(row)
                    if seed==7200:traces['|'.join(map(str,[family,method,budget]))]=strip_time(out)
    with (root/'episodes.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    write_json(root/'example_traces.json',traces);print('synthetic',len(rows));return rows
if __name__=='__main__':run()
