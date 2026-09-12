"""Interactive Decision desk mode using only authored public demonstration data."""
import copy,time,json
from datetime import datetime,timezone
from pathlib import Path
from .controller import candidates
from .online import OnlineController
from .integrity import ValidatedController
from .engine import verification_key
from .common import digest,canonical
def strip_time(value):
    if isinstance(value,dict):return {k:strip_time(v) for k,v in value.items() if k not in ['seconds','controller_seconds']}
    if isinstance(value,list):return [strip_time(v) for v in value]
    return value

def demonstration():
    snapshot='CREATE TABLE customers(id INTEGER PRIMARY KEY, spend INTEGER NOT NULL, orders INTEGER NOT NULL); INSERT INTO customers VALUES(1,120,4),(2,140,1),(3,20,1),(4,30,5);'
    tasks=[];prep={}
    for tid in ['export','count','inventory']:
        t=dict(id=tid,request='',snapshot=snapshot,schema='customers(id,spend,orders)',scope='Inventory' if tid=='inventory' else 'Atlas/segment',decision_id='inventory' if tid=='inventory' else 'segment',version=1,exceptions=[],sources=[],contract={'kind':'snapshot_table','ordered':False})
        field='id' if tid=='export' else 'count(*)'
        qs=['SELECT '+field+' FROM customers WHERE spend >= 100','SELECT '+field+' FROM customers WHERE orders >= 3']
        obj={'candidates':[dict(sql=q,meaning=['spending threshold','order threshold'][i]) for i,q in enumerate(qs)],'unrepresented_possible':False}
        if tid=='inventory':
            text='Count all current customer records.'
            t['sources']=[dict(id='S1',text=text,status='explicit_user_requirement',scope='Inventory',version=1)]
            obj={'candidates':[dict(sql='SELECT count(*) FROM customers',meaning='All current records')],'unrepresented_possible':False,'source_quote_sha256':digest(text)}
        tasks.append(t);prep[tid]=dict(candidates=copy.deepcopy(obj),audit=copy.deepcopy(obj))
    tasks[0]['request']='Export the IDs of eligible customers.'
    tasks[1]['request']='Count eligible customers for the capacity plan.'
    tasks[2]['request']='Count all current customer records for the audit inventory.'
    partner=copy.deepcopy(tasks[0]);partner.update(id='partner',scope='Partner/export',decision_id='partner_segment',request='Prepare the partner export under its separate eligibility requirement.')
    tasks.append(partner);prep['partner']=copy.deepcopy(prep['export'])
    names={'export':('Segmentation agent','Customer export'),'count':('Planning agent','Eligible-customer count'),'inventory':('Audit agent','Inventory total'),'partner':('Partner agent','Partner export')}
    for t in tasks:t['agent'],t['title']=names[t['id']]
    return tasks,prep

class Desk:
    def __init__(self,log_path=None,validate_sources=True):
        self.controller_class=ValidatedController if validate_sources else OnlineController
        self.path=Path(log_path) if log_path else None;self.events=[];self.started=time.monotonic();self.shown=None;self.reset();self.log('started',{})
    def reset(self,method='verification',budget=3):
        t,p=demonstration();self.c=self.controller_class(t,p,budget,64,method);self.question=None;self.c.inspect();self.changed=[];self.shown=None
    def state(self):
        c=self.c;work=[]
        for t in c.tasks:
            r=c.records.get(t['id'],{});work.append(dict(id=t['id'],title=t.get('title',t['id']),agent=t.get('agent','Agent'),request=t['request'],scope=t['scope'],status=r.get('status','needs_revalidation'),reason=r.get('reason','Input changed'),rows=r.get('result',{}).get('table',{}).get('rows'),source=t['sources'],version=t['version']))
        q=copy.deepcopy(self.question)
        if q:
            q['text']='Should eligibility mean spending at least 100, or at least 3 orders?'
            q['affected']=[t['title'] for t in c.tasks if t.get('decision_id',t['id'])==q['decision'] and t['scope']==q['scope']]
            q['remaining_work']=[w['title'] for w in work if w['status']=='released']
            for x in q['candidates']:x['preview']=x['outcome'].get('table',{}).get('rows',[])
        return dict(project='Atlas customer analytics',demo=True,participant_data=False,method=c.method,question=q,work=work,answers_remaining=c.budget-c.spent,answers_spent=c.spent,checks_remaining=c.machine.limit-c.machine.used,checks_used=c.machine.used,changes=self.changed,events=c.events[-12:])
    def log(self,action,payload):
        e=dict(utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-self.started,action=action,payload=payload,shown=strip_time(self.state()['question']),state_hash=digest(strip_time(self.state())),response_seconds=None if self.shown is None else time.monotonic()-self.shown,protocol='integrity_guard_v1' if self.controller_class==ValidatedController else 'legacy',record_type='Scripted/development interface observation, not participant data')
        self.events.append(e)
        if self.path:
            self.path.parent.mkdir(parents=True,exist_ok=True)
            with self.path.open('a') as f:f.write(canonical(e)+'\n')
    def act(self,a):
        op=a['action'];c=self.c
        if op=='reset':self.reset(a.get('method','verification'),int(a.get('budget',3)))
        elif op=='inspect':self.question=c.next_question();self.shown=time.monotonic()
        elif op=='answer':
            if self.question is None:raise ValueError('Inspect the current question first')
            value=a.get('value');narrow=a.get('only_this_request',False)
            if value not in ['spending','orders']:raise ValueError('Choose one stated definition')
            if c.spent+1+int(narrow)>c.budget:raise ValueError('A value plus a new narrow scope requires two answer units')
            q=self.question
            current=next(t for t in c.tasks if t['id']==q['task'])
            if verification_key(current,candidates(c.preparations[current['id']])[0])!=q['key']:raise ValueError('The displayed question is stale; inspect again')
            scope=q['scope'];affected=[t for t in c.tasks if t.get('decision_id',t['id'])==q['decision'] and t['scope']==scope]
            exceptions=[t['id'] for t in affected if narrow and t['id']!=q['task']]
            if narrow:c.spent+=1;c.log('scope_answer',task=q['task'],exceptions=exceptions)
            queries={}
            for t in affected:
                if t['id'] in exceptions:continue
                # A new instruction may lie outside previously represented candidates.
                # Invalidate all affected artifacts before accepting the new implementation.
                t['version']+=1;c.records.pop(t['id'],None)
                select='count(*)' if t['id']=='count' else 'id'
                queries[t['id']]='SELECT '+select+' FROM customers WHERE '+('spend >= 100' if value=='spending' else 'orders >= 3')
            c.answer(q,dict(sql_by_task=queries,exceptions=exceptions));self.question=None;self.changed=[]
        elif op=='defer':
            if self.question is None:raise ValueError('No active question')
            c.answer(self.question,None);self.question=None
        elif op=='snapshot':
            self.changed=[t['title'] for t in c.tasks]
            for t in list(c.tasks):c.revise(t['id'],snapshot=t['snapshot']+'UPDATE customers SET orders=0 WHERE id=1;')
            c.pending=[];self.question=None
        elif op=='reconsider':
            task=next((t for t in c.tasks if t['id']==a.get('task')),None)
            if task is None or task['id']=='inventory':raise ValueError('Choose a goal with an eligibility definition')
            affected=[t for t in c.tasks if t.get('decision_id',t['id'])==task.get('decision_id',task['id']) and t['scope']==task['scope']]
            self.changed=[t['title'] for t in affected]
            for t in affected:c.revise(t['id'],sources=[])
            self.question=None
        elif op=='inspect_details':pass
        else:raise ValueError('Unknown action')
        self.log(op,a);return self.state()
