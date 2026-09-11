"""Event-driven state controller, shared by saved-output simulation and local UI."""
from dataclasses import asdict
from .method import Request, Settings, select, parts, certificate

LABELS=('normal','outdoor_damper','heating_valve','cooling_valve','abstain')

class Controller:
    def __init__(self, requests, settings=Settings(), policy='guarded'):
        self.requests={r.request_id:r for r in requests}
        if len(self.requests)!=len(requests): raise ValueError('Duplicate request')
        self.settings=settings;self.policy=policy;self.now=0.;self.used=0.;self.context=None
        self.status={r.request_id:'future' for r in requests};self.not_before={};self.final={r.request_id:r.proposal for r in requests}
        self.events=[];self.session=[];self.position=0;self.session_id=0;self.last_info={}
        self.reviewed=[];self.components={k:0. for k in ('setup','switch','decision','coordination')}
        self.visited=set();self.context_changes=0;self.repeated=0
        self.advance(0)

    def emit(self,event,**data):self.events.append(dict(event=event,tick=round(self.now,8),**data))

    def advance(self,to,completion_id=None):
        if to<self.now-1e-9:raise ValueError('Clock cannot go backwards')
        boundaries=sorted({x for r in self.requests.values() for x in (r.arrival,r.deadline) if self.now<=x<=to})
        for t in boundaries:
            self.now=t
            for key,r in self.requests.items():
                if self.status[key]=='future' and r.arrival<=t:
                    self.status[key]='pending';self.emit('arrival',request_id=key)
                if r.deadline<=t and self.status[key] in ('pending','active','deferred') and not (key==completion_id and abs(t-to)<1e-9):
                    self.status[key]='expired';self.emit('cutoff',request_id=key)
        self.now=to
        for key,t in list(self.not_before.items()):
            if t<=to and self.status[key]=='deferred':self.status[key]='pending';self.emit('deferral_due',request_id=key)

    def pending(self):return [r for key,r in self.requests.items() if self.status[key]=='pending' and self.not_before.get(key,0)<=self.now]

    def recommend(self):
        group,info=select(self.policy,self.pending(),self.now,self.context,self.settings,self.settings.budget-self.used)
        self.last_info=info
        return group,info

    def start(self,ids=None,override=False):
        if self.session:raise ValueError('Finish or end the active session first')
        group,info=self.recommend()
        if ids is not None:
            if not override and ids!=[r.request_id for r in group]:raise ValueError('Changed selection requires explicit override')
            if len(ids)!=len(set(ids)) or not 1<=len(ids)<=self.settings.max_group:raise ValueError('Invalid group size')
            if any(k not in {r.request_id for r in self.pending()} for k in ids):raise ValueError('Only pending requests can be selected')
            group=[self.requests[k] for k in ids]
            if len({r.context for r in group})!=1:raise ValueError('Separate record contexts need separate sessions')
            cert=certificate(group,self.pending(),self.now,self.context,self.settings,self.settings.budget-self.used)
            info=dict(info,certificate=cert,override=True)
            # Override can waive opportunity preservation, never time feasibility.
            from .method import schedule
            if not all(x['timely'] for x in schedule(group,self.now,self.context,self.settings,self.settings.budget-self.used,True)):
                raise ValueError('Session cannot finish within its deadlines and budget')
        if not group:return False
        self.session=[r.request_id for r in group];self.position=0;self.session_id+=1
        self.emit('session_started',session_id=self.session_id,request_ids=list(self.session),information=info,override=override)
        return True

    def end(self,reason='user ended session'):
        if self.session:self.emit('session_ended',session_id=self.session_id,remaining=list(self.session),reason=reason)
        self.session=[];self.position=0

    def complete(self,diagnosis):
        if not self.session:raise ValueError('No active session')
        key=self.session[0];r=self.requests[key]
        if self.status[key]!='pending':self.end('Request expired or deferred');return False
        p=parts(r,self.context,self.settings,self.position);duration=sum(p.values());finish=self.now+duration
        if finish>r.deadline+1e-9 or self.used+duration>self.settings.budget+1e-9:
            self.end('No longer feasible');return False
        previous=self.context
        if previous!=r.context:
            if previous is not None:self.context_changes+=1
            if r.context in self.visited:self.repeated+=1
            self.visited.add(r.context)
            self.emit('context_opened',context=r.context,previous=previous)
        elif not self.settings.reuse:self.repeated+=1
        self.emit('review_started',request_id=key,session_id=self.session_id,finish=finish,parts=p)
        self.status[key]='active';self.advance(finish,completion_id=key)
        # An invalid/failed reviewer response preserves the original proposal.
        valid=diagnosis in LABELS
        if valid:self.final[key]=diagnosis
        self.status[key]='reviewed';self.reviewed.append(key);self.used+=duration
        for k,v in p.items():self.components[k]+=v
        self.context=r.context;self.session.pop(0);self.position+=1
        self.emit('review_completed',request_id=key,diagnosis=self.final[key],response_failed=not valid)
        if not self.session:self.emit('session_ended',session_id=self.session_id,remaining=[],reason='Completed');self.position=0
        elif self.settings.reconsider and self.policy=='guarded':
            group=[self.requests[k] for k in self.session if self.status[k]=='pending']
            if not certificate(group,self.pending(),self.now,self.context,self.settings,self.settings.budget-self.used,position=self.position)['valid']:
                self.end('New state no longer preserves EDF opportunities')
        return True

    def defer(self,key,until):
        if key not in self.requests or self.status[key] not in ('pending','deferred'):raise ValueError('Cannot defer completed or unreleased request')
        if not self.now<until<self.requests[key].deadline:raise ValueError('Deferral must end before cutoff')
        if key in self.session:self.session.remove(key)
        self.status[key]='deferred';self.not_before[key]=until;self.emit('deferred',request_id=key,until=until)
        if not self.session:self.position=0

    def step(self,response):
        if not self.session and not self.start():
            upcoming=[r.arrival for r in self.requests.values() if r.arrival>self.now]
            upcoming += [r.deadline for k,r in self.requests.items() if self.status[k] in ('pending','deferred') and r.deadline>self.now]
            upcoming += [t for t in self.not_before.values() if t>self.now]
            if self.last_info.get('wake',0)>self.now:upcoming.append(self.last_info['wake'])
            if not upcoming:return False
            self.advance(min(upcoming));return True
        key=self.session[0]
        self.complete(response(key));return True

    def snapshot(self):
        group,info=self.recommend() if not self.session else ([self.requests[k] for k in self.session],self.last_info)
        return dict(tick=self.now,budget=self.settings.budget,used=self.used,context=self.context,policy=self.policy,
                    recommendation=[r.request_id for r in group],information=info,active=list(self.session),
                    requests=[dict(asdict(r),status=self.status[k],final_diagnosis=self.final[k],deferred_until=self.not_before.get(k))
                              for k,r in self.requests.items() if self.status[k]!='future'],
                    events=self.events[-30:],components=self.components)
