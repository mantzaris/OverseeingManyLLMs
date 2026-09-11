"""Interactive facade for the frozen planner. No labels or synthetic hidden state.

The demo's work is authored. User answers come from the browser/API, not the
experiment's evaluator. Narrow answers create request-specific record bindings.
"""
import copy
import json
import time
from dataclasses import asdict
from datetime import datetime,timezone
from pathlib import Path
from .common import canonical,digest
from .planner import Factor,Task,Option,Planner,State,OTHER,UNRESOLVED
from .safe_protocol import SafeProtocol as Protocol

NAMES={'format':'Release format','accessibility':'Accessibility requirement','meeting':'Meeting preference',
       'exception.format':'Partner export format','scope.exception':'Whether the shared format applies to the partner export'}


def demonstration():
    factors=[Factor('format',('web','pdf',OTHER),(.45,.45,.1),scope='Atlas project / publication format',
                    source='The project notes mention both web and PDF; no user choice is recorded.'),
             Factor('accessibility',('screen_reader','large_print',OTHER),(.45,.45,.1),scope='Atlas project / accessibility',
                    source='The project must be accessible, but the required support is not specified.'),
             Factor('meeting',('morning','afternoon',OTHER),(.45,.45,.1),scope='Atlas project / planning meeting',
                    source='The coordination agent can prepare one independent meeting proposal.'),
             Factor('exception.format',('spreadsheet','pdf',OTHER),(.45,.45,.1),scope='Partner export only',
                    source='The partner export may follow a separate handoff requirement.'),
             Factor('scope.exception',('yes','no'),(.5,.5),kind='scope',scope='Partner export',
                    source='No instruction yet authorizes reusing the Atlas format for the partner.')]
    shared=Option((('format','format'),('accessibility','accessibility')))
    tasks=[Task('Website implementation',(shared,)),Task('Accessibility test plan',(shared,)),Task('Publishing instructions',(shared,)),
           Task('Meeting proposal',(Option((('meeting','meeting'),)),)),
           Task('Partner export',(Option((('format','format'),),(('scope.exception','yes'),)),Option((('format','exception.format'),))))]
    return Planner(factors,tasks)

class Desk:
    def __init__(self,log_path=None):
        self.log_path=Path(log_path) if log_path else None
        self.events=[];self.shown_at=None;self.reset();self.log('started',{})

    def reset(self,method='depth2',budget=2):
        self.controller=Protocol(demonstration(),budget);self.method=method;self.question=None
        self.started=time.monotonic();self.shown_at=None;self.step=0;self.stop_reason=None

    def state(self):
        c=self.controller;p=c.planner
        outcomes=p.terminal(c.state)[1]
        records=[]
        for i,f in enumerate(p.factors):
            best=max(range(len(f.choices)),key=lambda k:c.state.beliefs[i][k]);value=f.choices[best]
            records.append(dict(id=f.id,label=NAMES.get(f.id,f.id),value=None if value==OTHER else value,
                scope=f.scope,exceptions=list(f.exceptions),version=f.version,
                status='received answer' if c.state.revealed&(1<<i) else f.status,
                source=f.source,allowed_tasks=list(f.allowed_tasks),
                affected=[t.id for t in p.tasks if any(i in p.deps(o) for o in t.options)]))
        q=copy.deepcopy(self.question)
        if q:
            q['label']=NAMES.get(q['id'],q['id']);q['text']=('May the Atlas format also be used for the partner export?' if q['kind']=='scope' else
                'Which '+q['label'].lower()+' should the agents use?')
            q['additional_needed']=[dict(task=t.id,decisions=[NAMES.get(p.factors[i].id,p.factors[i].id) for i in sorted(p.deps(o))
                if i!=p.index[q['id']] and not c.state.revealed&(1<<i) and max(c.state.beliefs[i])<1])
                for t in p.tasks for o in t.options[:1] if p.index[q['id']] in p.deps(o)]
        return dict(project='Atlas publishing project',method=self.method,remaining_budget=c.budget-c.spent,
            response_budget=c.budget,spent=c.spent,question=q,records=records,stop_reason=self.stop_reason,
            work=[dict(id=o['task'],status='Ready under current assumptions' if o['status']=='release' else 'Deferred',
                       preview=o['values'],registered_release=c.releases.get(o['task'],{}).get('status')) for o in outcomes],
            events=copy.deepcopy(c.events),demo=True,participant_data=False,
            note='Authored interactive demonstration. Budgets are response counts, not measured human effort.')

    def log(self,action,payload):
        now=time.monotonic()
        e=dict(record_type='scripted_or_development_interaction_not_participant_data',utc=datetime.now(timezone.utc).isoformat(),
            elapsed_seconds=now-self.started,action=action,payload=payload,
            response_seconds_since_shown=None if self.shown_at is None else now-self.shown_at,
            state_sha256=digest(self.state()),displayed_question=self.state()['question'])
        self.events.append(e)
        if self.log_path:
            self.log_path.parent.mkdir(parents=True,exist_ok=True)
            with self.log_path.open('a') as f:f.write(canonical(e)+'\n')

    def narrow(self,task_id):
        c=self.controller;p=c.planner;i=c.pending
        if i is None:raise ValueError('No displayed question')
        old=p.factors[i]
        if old.kind=='scope':raise ValueError('A scope answer already concerns the named exception; answer its explicit question')
        task=next((t for t in p.tasks if t.id==task_id),None)
        if task is None or not any(i in p.deps(o) for o in task.options):raise ValueError('This work does not depend on the displayed question')
        key=task_id+'::'+old.id;new=Factor(**dict(old.__dict__,id=key,scope='Only '+task_id,allowed_tasks=(task_id,)))
        factors=list(p.factors)+[new];tasks=[]
        for t in p.tasks:
            if t.id!=task_id:tasks.append(t);continue
            options=tuple(Option(tuple((field,key if f==old.id else f) for field,f in o.bindings),o.gates) for o in t.options)
            tasks.append(Task(t.id,options,t.error_weight,t.defer_weight))
        c.planner=Planner(factors,tasks,p.response_error,p.unresolved_probability,p.question_penalty,p.width,p.node_limit)
        c.state=State(c.state.beliefs+(c.state.beliefs[i],),c.state.asked,c.state.revealed)
        c.pending=len(factors)-1
        if task_id in c.releases:c.releases[task_id]['status']='needs_revalidation'
        c.events.append(dict(kind='answer_scope_narrowed',original=old.id,new=key,task=task_id))

    def act(self,args):
        before=copy.deepcopy(self.__dict__)
        try:
            action=args.get('action');c=self.controller
            if action=='reset':
                method=args.get('method','depth2');budget=args.get('budget',2)
                if method not in ['depth1','depth2','depth3','completion','memory','generic2','minimum_completion']:raise ValueError('Unknown planner')
                self.reset(method,int(budget))
            elif action=='next':
                self.question=c.propose(self.method);self.shown_at=time.monotonic() if self.question else None
                self.stop_reason=None if self.question else 'No available question plan is predicted to justify another answer under the current budget and assumptions.'
            elif action=='ask':
                if c.pending is not None:raise ValueError('Resolve the displayed question first')
                i=c.planner.index[args['id']]
                if i not in c.planner.available(c.state,c.budget-c.spent):raise ValueError('Question is already resolved, attempted or unaffordable')
                c.pending=i;self.question=c.planner.question(i);self.shown_at=time.monotonic();self.stop_reason=None
                c.events.append(dict(kind='user_selected_question',question=self.question))
            elif action=='answer':
                value=str(args.get('value','')).strip()
                if not value:raise ValueError('An answer is required')
                if args.get('only_task'):self.narrow(args['only_task'])
                self.controller.answer(value);self.question=None
            elif action=='defer':c.answer(UNRESOLVED);self.question=None
            elif action=='revise':
                c.revise(args['id'],value=args.get('value'),revoke=bool(args.get('revoke',False)),exceptions=args.get('exceptions'))
            elif action=='finish':c.finish()
            elif action=='inspect':pass
            else:raise ValueError('Unknown action')
            self.log(action,args);return self.state()
        except (KeyError,ValueError,TypeError):
            self.__dict__.clear();self.__dict__.update(before);raise
