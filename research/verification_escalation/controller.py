"""Public-only escalation controller. The caller supplies answers only after ask()."""
import copy,time
from .common import digest
from .engine import MachineBudget,execute,equivalent,verification_key

METHODS=['recovery_completion','recovery_depth2','verification','full_context','matched_checking','no_recovery','no_verification','no_coverage_guard','no_sharing','all_wait']

def candidates(preparation):
    result=[];broken=False;unknown=False;origins=[]
    for name in ['candidates','audit']:
        obj=preparation.get(name)
        if not isinstance(obj,dict) or not isinstance(obj.get('candidates'),list) or not obj['candidates']:
            broken=True;continue
        unknown=unknown or obj.get('unrepresented_possible',True) is not False
        for x in obj['candidates'][:3]:
            if not isinstance(x,dict) or not isinstance(x.get('sql'),str):broken=True;result.append({'sql':None,'meaning':'Unsupported candidate','origin':name})
            else:result.append(dict(sql=x['sql'],meaning=str(x.get('meaning','')),origin=name))
        origins.append(name)
    return result,broken,unknown,origins

class Controller:
    def __init__(self,tasks,preparations,user_budget=1,machine_budget=24,method='verification'):
        if method not in METHODS:raise ValueError('unknown method')
        if user_budget<0 or machine_budget<0:raise ValueError('negative budget')
        self.tasks=copy.deepcopy(tasks);self.preparations=copy.deepcopy(preparations);self.method=method
        self.budget=user_budget;self.spent=0;self.machine=MachineBudget(machine_budget);self.events=[];self.records={};self.answers={};self.cache={};self.started=time.perf_counter()
    def log(self,event,**data):self.events.append(dict(event=event,**data))
    def recovery(self,t,p):
        if self.method=='no_recovery':return False
        for name in ['candidates','audit']:
            obj=p.get(name) or {};quoted=obj.get('source_quote_sha256') or digest(obj.get('source_quote',''))
            for s in t.get('sources',[]):
                if s.get('status')=='explicit_user_requirement' and s.get('scope')==t['scope'] and t['id'] not in s.get('exceptions',[]) and quoted==digest(s['text']) and s['text']:
                    return True
        return False
    def inspect(self):
        pending=[]
        for t in self.tasks:
            tid=t['id'];p=self.preparations[tid];cs,broken,unknown,origins=candidates(p);key=verification_key(t,cs)
            if tid in self.records and self.records[tid].get('key')==key and self.records[tid]['status']=='released':continue
            if key in self.cache:rs=self.cache[key]
            else:
                rs=[execute(t['snapshot'],x['sql'],self.machine,t['contract'].get('ordered',False)) for x in cs];self.cache[key]=rs
            recovered=self.recovery(t,p)
            valid=[i for i,r in enumerate(rs) if r['status']=='ok']
            issue=t.get('decision_id',tid);reuse=self.answers.get((issue,t['scope'])) if self.method!='no_sharing' else None
            # Reuse consumes only an explicitly registered shared decision and matching scope.
            if reuse and tid not in reuse.get('exceptions',[]) and reuse['version']==t['version']:
                sql=reuse.get('sql_by_task',{}).get(tid)
                if sql is not None:self.release_answer(t,sql,key,'shared_answer');continue
            reason='unresolved_interpretation';chosen=None
            if recovered and valid:chosen=valid[0];reason='source_recovery'
            elif self.method=='full_context' and valid:chosen=valid[0];reason='full_context_proposal'
            elif self.method=='matched_checking' and valid:
                # Comparable execution budget, agreement used as a vote rather than an escalation certificate.
                chosen=max(valid,key=lambda i:(sum(r.get('table_hash')==rs[i]['table_hash'] for r in rs),-i));reason='execution_vote'
            elif self.method not in ['recovery_completion','recovery_depth2','no_verification']:
                distinct=len(set(x['sql'] for x in cs))
                guard=(not broken and not unknown and len(origins)==2 and distinct>=2 and all(r.get('row_count',0)>0 for r in rs))
                if p.get('coverage')=='complete_enumeration':guard=not broken
                if self.method=='no_coverage_guard':guard=not broken
                if equivalent(rs) and guard and t['contract']['kind']=='snapshot_table' and not t['contract'].get('explicit_semantic_choice_required',False):
                    chosen=0;reason='outcome_agreement'
            if chosen is not None:
                self.records[tid]=dict(status='released',key=key,reason=reason,result=rs[chosen],sql=cs[chosen]['sql'],version=t['version'])
                self.log('release',task=tid,reason=reason,key=key);continue
            if not cs or not valid:reason='unsupported_preparation'
            if broken or any(r['status']!='ok' for r in rs):reason='verification_failed'
            pending.append(dict(task=tid,decision=issue,scope=t['scope'],issue='Which meaning should this result use?',evidence=t.get('sources',[]),candidates=[dict(meaning=c['meaning'],sql=c['sql'],outcome=r) for c,r in zip(cs,rs)],reason=reason,key=key))
            self.records[tid]=dict(status='unfinished',key=key,reason=reason,version=t['version'])
        if self.method=='all_wait' and pending:
            for t in self.tasks:
                if self.records[t['id']]['status']=='released':self.records[t['id']]['status']='unfinished';self.records[t['id']]['reason']='global_wait'
        self.pending=pending
        self.log('inspect',pending=[x['task'] for x in pending],remaining_answers=self.budget-self.spent,executions=self.machine.used)
        return pending
    def next_question(self):
        pending=self.inspect()
        answered={(x.get('task') if self.method=='no_sharing' else x.get('decision')) for x in self.events if x['event']=='answer'}
        pending=[q for q in pending if (q['task'] if self.method=='no_sharing' else q['decision']) not in answered]
        if not pending or self.spent>=self.budget:return None
        # One unresolved intent per empirical task: minimum completion and depth two agree.
        # Synthetic sharing is explicitly registered, not inferred from word similarity.
        counts={q['decision']:sum(x['decision']==q['decision'] and x['scope']==q['scope'] for x in pending) for q in pending}
        q=min(pending,key=lambda x:(-counts[x['decision']],x['task']))
        if self.method in ['recovery_completion','recovery_depth2']:
            from research.clarification_planning.completion_rule import MinimumCompletion
            from research.clarification_planning.planner import Factor,Task,Option
            ids=sorted({x['decision'] for x in pending})
            factors=[Factor(i,('a','b'),(.5,.5)) for i in ids]
            jobs=[Task(x['task'],(Option((('intent',x['decision']),)),)) for x in pending]
            planner=MinimumCompletion(factors,jobs);state=planner.initial
            if self.method=='recovery_completion':selected=planner.heuristic(state,self.budget-self.spent,'minimum_completion')
            else:selected=planner.select(state,self.budget-self.spent,2)
            if selected is None:return None
            chosen=planner.factors[selected].id;q=next(x for x in pending if x['decision']==chosen)
        if q['decision'] in [x.get('decision') for x in self.events if x['event']=='answer']:return None
        self.log('show_question',task=q['task'],decision=q['decision'],scope=q['scope'],text=q['issue'])
        return q
    def release_answer(self,t,sql,key,reason):
        r=execute(t['snapshot'],sql,self.machine,t['contract'].get('ordered',False))
        self.records[t['id']]=dict(status='released' if r['status']=='ok' else 'unfinished',reason=reason if r['status']=='ok' else 'answer_execution_failed',key=key,result=r,sql=sql,version=t['version'])
        self.log('answer_result',task=t['id'],status=self.records[t['id']]['status'],reason=reason)
    def answer(self,q,response):
        if self.spent>=self.budget:raise ValueError('answer_budget')
        if not any(x['task']==q['task'] and x['key']==q['key'] for x in getattr(self,'pending',[])):raise ValueError('stale_question')
        self.spent+=1;self.log('answer',decision=q['decision'],task=q['task'],unresolved=response is None)
        if response is None:return
        task=next(t for t in self.tasks if t['id']==q['task'])
        record=dict(scope=q['scope'],version=task['version'],exceptions=response.get('exceptions',[]),sql_by_task=response.get('sql_by_task',{}))
        self.answers[(q['decision'],q['scope'])]=record
        for t in self.tasks:
            if t['id'] in record['sql_by_task'] and t['scope']==q['scope'] and t.get('decision_id',t['id'])==q['decision'] and t['id'] not in record['exceptions'] and t['version']==task['version'] and (self.method!='no_sharing' or t['id']==q['task']):
                cs=candidates(self.preparations[t['id']])[0];self.release_answer(t,record['sql_by_task'][t['id']],verification_key(t,cs),'user_answer')
    def revise(self,task_id,**updates):
        t=next(t for t in self.tasks if t['id']==task_id);t.update(updates);t['version']+=1
        self.records.pop(task_id,None);self.log('revalidation_required',task=task_id,version=t['version'])
    def result(self):
        return dict(records=copy.deepcopy(self.records),events=copy.deepcopy(self.events),questions=self.spent,executions=self.machine.used,controller_seconds=time.perf_counter()-self.started)
