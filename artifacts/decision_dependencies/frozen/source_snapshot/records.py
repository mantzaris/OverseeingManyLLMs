"""Source-backed preference records and explicit work dependencies.

This module never reads evaluator files. Values and inferred scopes can be wrong;
the release barrier guarantees version consistency, not semantic truth.
"""
import copy
import re
from .prompts import SLOTS

def normalize(value):
    text=' '.join(str(value).lower().strip().split())
    return {'city centre':'centre','center':'centre','guest house':'guesthouse',
            'price_range':'pricerange','cuisine':'food'}.get(text,text)

def rows(payload,field):
    if isinstance(payload,list) and len(payload)==1 and isinstance(payload[0],dict):payload=payload[0]
    result=payload.get(field,[]) if isinstance(payload,dict) else []
    return result if isinstance(result,list) else []

def extracted_records(payload,messages,source_guard=True):
    turns={t['turn']:t for t in messages};accepted={};rejected=[]
    for item in rows(payload,'records'):
        if not isinstance(item,dict):rejected.append(dict(reason='record_not_object'));continue
        domain=normalize(item.get('domain',''));slot=normalize(item.get('slot',''))
        value=normalize(item.get('value',''));quote=item.get('quote','');turn=item.get('turn')
        reason=None
        if domain not in SLOTS or slot not in SLOTS[domain] or not value or value in ('unknown','none','dontcare'):
            reason='unsupported_or_missing_field'
        elif source_guard:
            source=turns.get(turn)
            if not source or source['role']!='user':reason='not_a_user_source'
            elif not isinstance(quote,str) or not quote.strip() or ' '.join(quote.lower().split()) not in ' '.join(source['text'].lower().split()):
                reason='quote_not_in_cited_turn'
            elif re.search(r'\b(except|unless|only for|just for|for this|do not reuse|does not apply)\b',source['text'],re.I):
                reason='conditional_scope_requires_confirmation'
        if reason:rejected.append(dict(record=item,reason=reason));continue
        key=domain+'.'+slot
        clean=dict(key=key,domain=domain,slot=slot,value=value,turn=turn,quote=quote,
                   authority='inferred_user_preference',scope_status='inferred',kind='preference')
        if key in accepted and (accepted[key].get('conflict') or accepted[key]['value']!=value):
            clean.update(conflict=True,value=None)
        accepted[key]=clean
    return accepted,rejected

def parsed_queries(payload):
    output={}
    for row in rows(payload,'queries'):
        if not isinstance(row,dict) or not isinstance(row.get('id'),str):continue
        domain=normalize(row.get('domain',''));slot=normalize(row.get('slot',''))
        output[row['id']]=domain+'.'+slot if domain in SLOTS and slot in SLOTS[domain] else None
    return output

def model_answers(payload):
    result={}
    for row in rows(payload,'answers'):
        if not isinstance(row,dict) or not isinstance(row.get('id'),str):continue
        value=normalize(row.get('value',''))
        result[row['id']]=None if value in ('','unknown','none','dontcare') else value
    return result

class DecisionController:
    """One project, event-driven decision store and optimistic release barrier."""
    def __init__(self,project):
        self.project=project;self.epoch=0;self.records={};self.versions={}
        self.tasks={};self.requests={};self.events=[];self.sequence=0
        self.answer_cache={};self.confirmations=0

    def event(self,kind,**payload):
        self.sequence+=1
        self.events.append(dict(sequence=self.sequence,kind=kind,epoch=self.epoch,**copy.deepcopy(payload)))

    def publish(self,records,reason='New user conversation'):
        self.epoch+=1;changed=[]
        for key in sorted(set(self.records)|set(records)):
            previous=self.records.get(key);current=records.get(key)
            # Semantically equal values retain versions. A conflict or revocation
            # changes the version. Quote changes alone are retained as provenance.
            signature=lambda x: None if x is None else (x.get('value'),x.get('conflict',False),x.get('kind'),x.get('scope_status'),tuple(sorted(x.get('exceptions',[]))))
            if signature(previous)!=signature(current):
                self.versions[key]=self.versions.get(key,0)+1;changed.append(key)
        self.records=copy.deepcopy(records);self.answer_cache={}
        for task in self.tasks.values():
            affected=[key for key,basis in task['dependencies'].items() if not self.current(basis)]
            if affected:task['status']='needs_revalidation';task['affected']=affected
        self.event('source_update',reason=reason,changed_keys=changed,
                   affected_tasks=[k for k,t in self.tasks.items() if t['status']=='needs_revalidation'])
        return changed

    def submit(self,request):
        request=copy.deepcopy(request)
        if request.get('project')!=self.project:raise ValueError('Request belongs to a different project')
        if not isinstance(request.get('id'),str) or not request.get('text'):raise ValueError('Request ID and text required')
        if request['id'] in self.requests:raise ValueError('Duplicate request ID')
        self.requests[request['id']]=request;self.event('request_submitted',request=request)
        return self.lookup(request)

    def lookup(self,request,ignore_scope=False):
        if request.get('project')!=self.project:return dict(status='needs_user',reason='project_mismatch')
        key=request.get('key')
        if request.get('kind','preference')!='preference':
            cached=self.answer_cache.get(('request',request.get('id')))
            return copy.deepcopy(cached) if cached else dict(status='needs_user',reason='action_specific_approval')
        cached=self.answer_cache.get(('request',request.get('id')))
        if cached:return copy.deepcopy(cached)
        scoped=self.records.get(key,{})
        if request.get('entity') in scoped.get('exceptions',[]):return dict(status='needs_user',reason='explicit_exception')
        cached=self.answer_cache.get(('scope',key))
        if cached:return copy.deepcopy(cached)
        if ignore_scope and isinstance(key,str):
            options=[k for k in sorted(self.records) if k.split('.')[-1]==key.split('.')[-1]]
            key=options[0] if options else key
        record=self.records.get(key)
        if not record:return dict(status='needs_user',reason='no_supported_answer')
        if record.get('conflict') or record.get('value') is None:return dict(status='needs_user',reason='conflicting_answers')
        if record.get('kind')!='preference':return dict(status='needs_user',reason='not_preference_authority')
        if request.get('entity') in record.get('exceptions',[]):return dict(status='needs_user',reason='explicit_exception')
        return dict(status='available',value=record['value'],key=key,
                    basis=dict(key=key,version=self.versions.get(key,0),epoch=self.epoch,origin='record'),
                    source=copy.deepcopy(record),reason='Inferred applicable preference; source is inspectable')

    def answer(self,request,value,scope='request',key=None):
        if request.get('project')!=self.project:raise ValueError('Request belongs to a different project')
        if scope not in ('request','project'):raise ValueError('Choose request or project scope')
        if scope=='project' and request.get('kind','preference')!='preference':
            raise ValueError('An action-specific approval cannot become project authority')
        target=key if key is not None else request.get('key')
        if scope=='project' and not target:raise ValueError('A project answer requires an explicit domain and decision type')
        if scope=='project' and request.get('entity') in self.records.get(target,{}).get('exceptions',[]):
            raise ValueError('This request is an exception; answer it alone or explicitly revise the decision scope')
        result=dict(status='available',value=normalize(value),key=target,
                    basis=dict(key=target,version=self.versions.get(target,0),epoch=self.epoch,origin='user'),
                    source=dict(authority='explicit_user_answer',scope_status='confirmed',scope=scope),reason='User answered')
        cachekey=('scope',target) if scope=='project' else ('request',request.get('id'))
        self.answer_cache[cachekey]=copy.deepcopy(result);self.confirmations+=1
        self.event('user_answer',request_id=request.get('id'),value=result['value'],scope=scope,key=target)
        return result

    def current(self,basis):
        if basis.get('origin') in ('user','snapshot'):return basis.get('epoch')==self.epoch
        return basis.get('version')==self.versions.get(basis.get('key'),0) and basis.get('key') in self.records

    def prepare(self,task_id,answers):
        self.tasks[task_id]=dict(id=task_id,status='prepared',epoch=self.epoch,
                                dependencies={k:copy.deepcopy(a['basis']) for k,a in answers.items()},
                                answers=copy.deepcopy(answers),affected=[])
        self.event('work_prepared',task_id=task_id,dependencies=self.tasks[task_id]['dependencies'])

    def release(self,task_id,barrier=True):
        task=self.tasks[task_id]
        stale=[k for k,b in task['dependencies'].items() if not self.current(b)]
        if barrier and stale:
            task.update(status='needs_revalidation',affected=stale)
            self.event('release_blocked',task_id=task_id,stale=stale);return False
        task['status']='released';self.event('work_released',task_id=task_id,stale_dependencies=stale)
        return True

    def revise(self,key,value=None,exceptions=None,revoke=False):
        records=copy.deepcopy(self.records)
        if revoke:records.pop(key,None)
        else:
            if key not in records:raise ValueError('Unknown decision')
            records[key].update(value=records[key]['value'] if value is None else normalize(value),scope_status='confirmed',authority='explicit_user_answer')
            if exceptions is not None:records[key]['exceptions']=list(exceptions)
        self.publish(records,reason='User revoked a decision' if revoke else 'User revised a decision')

    def snapshot(self):
        return copy.deepcopy(dict(project=self.project,epoch=self.epoch,records=self.records,
                                  versions=self.versions,tasks=self.tasks,requests=self.requests,
                                  events=self.events,confirmations=self.confirmations))
