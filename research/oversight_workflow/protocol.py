"""Atomic event protocol. No scorer, annotations, model, or scheduler beliefs here."""
from copy import deepcopy
import threading
import time
from datetime import datetime, timezone
from .common import digest, canonical

CONDITIONS = ('threads', 'queue', 'sessions')
DECISIONS = ('approve', 'correct', 'reject', 'defer')

class ProtocolError(ValueError):
    pass

class Desk:
    def __init__(self, condition='sessions'):
        if condition not in CONDITIONS:
            raise ProtocolError('Unknown interface condition')
        self.lock = threading.RLock()
        self.changed = threading.Condition(self.lock)
        self.state = dict(condition=condition, paused=False, tasks={}, requests={},
                          active=None, session=[], decisions=[], releases=[], displays=[])
        self.events = []
        self.receipts = {}
        self.started = time.monotonic()

    def logical(self):
        with self.lock:
            return deepcopy(self.state)

    def view(self):
        with self.lock:
            s = self.logical()
            s.update(sequence=len(self.events), elapsed=time.monotonic()-self.started,
                     counts=self.counts(), state_sha256=digest(self.state))
            return s

    def counts(self):
        ts = list(self.state['tasks'].values())
        rs = list(self.state['requests'].values())
        return dict(offered=len(ts), admitted=sum(t['admitted_at'] is not None for t in ts),
                    started=sum(t['started_at'] is not None for t in ts), received=len(rs),
                    unstarted=sum(t['started_at'] is None for t in ts),
                    in_flight=sum(t['started_at'] is not None and t['id'] not in self.state['requests'] for t in ts),
                    queued=sum(r['status']=='queued' for r in rs),
                    active=int(self.state['active'] is not None),
                    deferred=sum(r['status']=='deferred' for r in rs),
                    unresolved=sum(r['status'] in ('queued','active','deferred') for r in rs),
                    resolved=sum(r['status']=='resolved' for r in rs),
                    withdrawn=sum(r['status']=='withdrawn' for r in rs),
                    released=sum(self.current_released(r['id']) for r in rs),
                    remaining=len(ts)-sum(r['status'] in ('resolved','withdrawn') for r in rs))

    def current_released(self, rid):
        r = self.state['requests'][rid]
        return r['status'] != 'withdrawn' and any(x['request_id']==rid and x['version']==r['current_version'] for x in self.state['releases'])

    def next_request(self, now=None):
        with self.lock:
            now = time.monotonic()-self.started if now is None else now
            pending=[r for r in self.state['requests'].values() if r['status']=='queued' or
                     (r['status']=='deferred' and r['defer_until'] is not None and r['defer_until']<=now)]
            session=[r for r in pending if r['id'] in self.state['session']]
            if self.state['condition']=='sessions' and session:
                pending=session
            def order(r):
                t=self.state['tasks'][r['id']]
                return (-t['priority'], t['deadline'] if t['deadline'] is not None else float('inf'), r['received_at'], r['id'])
            return min(pending,key=order)['id'] if pending else None

    def command(self, event_id, action, payload=None, *, at=None):
        payload=deepcopy(payload or {})
        with self.lock:
            fingerprint=digest([action,payload])
            if event_id in self.receipts:
                old=self.receipts[event_id]
                if old['fingerprint']!=fingerprint:
                    raise ProtocolError('Event ID reused for different content')
                return deepcopy(old['result'])
            stamp=time.monotonic()-self.started if at is None else float(at)
            before=deepcopy(self.state)
            begin=time.perf_counter()
            try:
                result=self._apply(action,payload,stamp)
                self._invariants()
                response=dict(ok=True,result=result)
            except (ProtocolError,KeyError,TypeError,ValueError) as e:
                self.state=before
                response=dict(ok=False,error=str(e))
            event=dict(sequence=len(self.events)+1,event_id=event_id,action=action,payload=payload,
                       at=stamp,utc=datetime.now(timezone.utc).isoformat(),response=response,
                       state_sha256=digest(self.state),handler_ms=(time.perf_counter()-begin)*1000)
            self.events.append(event)
            self.receipts[event_id]=dict(fingerprint=fingerprint,result=response)
            self.changed.notify_all()
            return deepcopy(response)

    def _task(self, rid):
        if rid not in self.state['tasks']: raise ProtocolError('Unknown task')
        return self.state['tasks'][rid]

    def _request(self, rid):
        if rid not in self.state['requests']: raise ProtocolError('Request not received')
        return self.state['requests'][rid]

    def _apply(self, action, p, t):
        s=self.state
        if action=='offer':
            required={'id','agent','question_id','question','source'}
            if not required<=set(p):raise ProtocolError('Incomplete task metadata')
            if set(p)-required-{'priority','deadline','priority_origin','dependencies'}:raise ProtocolError('Unsupported task fields')
            if p['id'] in s['tasks']:raise ProtocolError('Task already offered')
            source=p['source']
            if set(source)-{'id','table','paragraphs','provenance','sha256'}:raise ProtocolError('Unsupported source fields')
            if digest({k:source[k] for k in ('id','table','paragraphs')})!=source['sha256']:raise ProtocolError('Source hash mismatch')
            if any(set(x)-{'order','text'} for x in source['paragraphs']):raise ProtocolError('Unsupported paragraph fields')
            deadline=p.get('deadline');priority=p.get('priority',0)
            if (deadline is not None or priority) and not p.get('priority_origin'):raise ProtocolError('Priority origin required')
            if any(x not in s['tasks'] for x in p.get('dependencies',[])):raise ProtocolError('Unknown explicit dependency')
            s['tasks'][p['id']]={**p,'priority':priority,'deadline':deadline,'priority_origin':p.get('priority_origin','none'),
                'dependencies':p.get('dependencies',[]),'offered_at':t,'admitted_at':None,'started_at':None}
        elif action in ('admit','start'):
            task=self._task(p['id'])
            if s['paused']:raise ProtocolError('New task starts are paused; in-flight work continues')
            if action=='admit':
                if task['admitted_at'] is not None:raise ProtocolError('Already admitted')
                task['admitted_at']=t
            else:
                if task['admitted_at'] is None or task['started_at'] is not None:raise ProtocolError('Task cannot start')
                task['started_at']=t
        elif action=='receive':
            task=self._task(p['id'])
            if task['started_at'] is None:raise ProtocolError('Task has not started')
            if p['id'] in s['requests']:raise ProtocolError('Request already received')
            output=self._output(p['output'])
            s['requests'][p['id']]=dict(id=p['id'],status='queued',received_at=t,current_version=1,
                versions={'1':dict(output=output,origin=p.get('origin','model'),created_at=t)},
                defer_until=None,notes='',history=[],requested_decision='Review this answer before release')
        elif action=='pause': s['paused']=True
        elif action=='resume': s['paused']=False
        elif action=='select':
            r=self._request(p['id'])
            if s['active']:raise ProtocolError('Finish or defer the active review first')
            if r['status'] not in ('queued','deferred'):raise ProtocolError('Request is not pending')
            r['status']='active';r['defer_until']=None
            v=r['current_version']
            s['active']=dict(request_id=r['id'],version=v,output=deepcopy(r['versions'][str(v)]['output']),
                source=deepcopy(self._task(r['id'])['source']),opened_at=t,notes=r['notes'])
            r['history'].append(dict(action='select',at=t,version=v))
        elif action=='session':
            if s['condition']!='sessions':raise ProtocolError('Source sessions are disabled')
            ids=p['ids']
            if not 1<=len(ids)<=3 or len(set(ids))!=len(ids):raise ProtocolError('Select one to three distinct requests')
            rs=[self._request(i) for i in ids]
            if any(r['status'] not in ('queued','deferred','active') for r in rs):raise ProtocolError('Only pending requests can join')
            if len({self._task(i)['source']['id'] for i in ids})!=1:raise ProtocolError('A source session requires the same source ID')
            s['session']=ids
        elif action=='note':
            a=s['active']
            if not a:raise ProtocolError('No active review')
            self._request(a['request_id'])['notes']=str(p['text'])[:5000]
            a['notes']=str(p['text'])[:5000]
        elif action=='refresh':
            a=s['active']
            if not a:raise ProtocolError('No active review')
            r=self._request(a['request_id']);v=r['current_version']
            a.update(version=v,output=deepcopy(r['versions'][str(v)]['output']),opened_at=t)
            r['history'].append(dict(action='refresh',at=t,version=v))
        elif action=='revise':
            r=self._request(p['id'])
            if r['status']=='withdrawn':raise ProtocolError('Withdrawn request cannot be revised')
            v=r['current_version']+1
            r['versions'][str(v)]=dict(output=self._output(p['output']),origin=p.get('origin','model_revision'),created_at=t)
            r['current_version']=v
            # Preserve the pinned old view. Its eventual stale approval is refused.
            if not s['active'] or s['active']['request_id']!=r['id']:r['status']='queued'
            r['history'].append(dict(action='revise',at=t,version=v,previous_superseded=v-1))
        elif action=='decide':
            a=s['active'];rid=p['id'];v=p['version'];choice=p['decision']
            if not a or a['request_id']!=rid or a['version']!=v:raise ProtocolError('Decision does not match the active reviewed version')
            r=self._request(rid)
            if choice not in DECISIONS:raise ProtocolError('Unknown decision')
            # Deferral remains possible while a newer draft is waiting.
            if choice!='defer' and v!=r['current_version']:raise ProtocolError('A newer version requires review before approval, correction or rejection')
            decision=dict(request_id=rid,version=v,decision=choice,at=t,by=p.get('by','local_user'))
            if choice=='correct':
                v+=1;r['current_version']=v
                r['versions'][str(v)]=dict(output=self._output(p['output']),origin='user_correction',created_at=t)
                decision.update(version=v,reviewed_version=a['version'],authorizes='approval_of_this_user_correction')
            if choice=='defer':
                r['status']='deferred';r['defer_until']=p.get('until');r['notes']=str(p.get('note',r['notes']))[:5000]
                decision.update(until=r['defer_until'],note=r['notes'])
            else:r['status']='resolved'
            s['decisions'].append(decision);r['history'].append(deepcopy(decision));s['active']=None
            return dict(version=v,decision=choice)
        elif action=='release':
            r=self._request(p['id']);v=p['version']
            if v!=r['current_version'] or r['status']!='resolved':raise ProtocolError('Only the current resolved version can be released')
            decisions=[d for d in s['decisions'] if d['request_id']==r['id'] and d['version']==v]
            if not decisions or decisions[-1]['decision'] not in ('approve','correct'):raise ProtocolError('No approval for this version')
            if self.current_released(r['id']):raise ProtocolError('Version already released')
            s['releases'].append(dict(request_id=r['id'],version=v,at=t,output_sha256=digest(r['versions'][str(v)]['output'])))
        elif action=='withdraw':
            r=self._request(p['id']);r['status']='withdrawn';r['history'].append(dict(action='withdraw',at=t,reason=p.get('reason','')))
            if s['active'] and s['active']['request_id']==r['id']:s['active']=None
        elif action=='display':
            # This is a browser observation, not evidence that a person read it.
            allowed={'view','request_id','version','visible_ids','client_elapsed_ms','received_to_render_ms','http_roundtrip_ms','focus','action'}
            if set(p)-allowed:raise ProtocolError('Unsupported display fields')
            s['displays'].append(dict(at=t,**p))
        else:raise ProtocolError('Unknown action')
        return None

    @staticmethod
    def _output(output):
        if not isinstance(output,dict):raise ProtocolError('Output must be an object')
        allowed={'answer','scale','evidence','operation','derivation','valid','issues','invalid_evidence','calculation','status'}
        if set(output)-allowed:raise ProtocolError('Unsupported output fields')
        if not isinstance(output.get('answer'),list):raise ProtocolError('Answer must be a list, including [] for failed work')
        return deepcopy(output)

    def _invariants(self):
        s=self.state
        active=[r['id'] for r in s['requests'].values() if r['status']=='active']
        assert active==([] if s['active'] is None else [s['active']['request_id']])
        for rid,r in s['requests'].items():
            assert rid in s['tasks'] and s['tasks'][rid]['started_at'] is not None
            assert str(r['current_version']) in r['versions']
        if s['active']:
            a=s['active'];r=s['requests'][a['request_id']]
            assert a['output']==r['versions'][str(a['version'])]['output']
        for release in s['releases']:
            r=s['requests'][release['request_id']]
            assert release['output_sha256']==digest(r['versions'][str(release['version'])]['output'])
        c=self.counts()
        assert c['offered']==c['unstarted']+c['in_flight']+c['received']
        assert c['received']==c['queued']+c['active']+c['deferred']+c['resolved']+c['withdrawn']


def replay(events,condition='sessions'):
    desk=Desk(condition)
    for e in events:
        response=desk.command(e['event_id'],e['action'],e['payload'],at=e['at'])
        if response!=e['response'] or digest(desk.state)!=e['state_sha256']:
            raise AssertionError('Replay mismatch at event '+str(e['sequence']))
    return desk
