"""Discrete-event CPU simulation, with the existing atomic transition semantics.

FastDesk omits per-command wall-clock profiling/deep-copy hashing for bulk runs.
It calls the existing _apply and invariants. Saved command streams can also be
replayed through ordinary Desk.command, independently checking identical state.
"""
from copy import deepcopy
from collections import defaultdict
import heapq,math,time
from research.oversight_workflow.protocol import Desk
from research.oversight_workflow.common import digest
from .policies import choose


class SimulationDesk(Desk):
    def _apply(self,action,p,stamp):
        result=super()._apply(action,p,stamp)
        if action=='decide' and p['decision']=='correct':
            self.state['requests'][p['id']]['versions'][str(result['version'])]['origin']='simulated_reviewer_correction'
        return result


class FastDesk(SimulationDesk):
    def apply(self,action,payload,at):
        result=self._apply(action,payload,float(at))
        self._invariants()
        return result


def simulate(items,sources,cfg,policy,seed,env,keep_trace=True):
    desk=FastDesk('sessions' if policy=='G' else 'queue');cmds=[];heap=[];sequence=0
    itemmap={x['id']:x for x in items};horizon=cfg['horizon'];attempts=defaultdict(int)
    memory={};completed=0;previous_source=None;group=[];busy=None;held_release=False;now=0.
    observed=[];reviews=[];time_spent=defaultdict(float);switches=returns=0;seen=set();waits={};attempted=set();events=0
    def cmd(action,p,at):
        nonlocal events
        result=desk.apply(action,p,at);events+=1
        # Initial sources/drafts are referenced from inputs, not copied per run.
        if keep_trace:cmds.append([at,action,deepcopy(p) if action not in ('offer','receive') else {'id':p['id']}])
        return result
    def push(at,kind,data):
        nonlocal sequence
        sequence+=1;heapq.heappush(heap,(at,sequence,kind,data))
    for item in items:
        public=dict(id=item['id'],agent=item['agent'],question_id=item['id'],question=item['question'],source=sources[item['source_id']],dependencies=[])
        cmd('offer',public,0.)
        push(item['start'],'start',item['id']);push(item['arrival'],'arrival',item['id'])
    def pending(at):
        return [dict(id=rid,source_id=itemmap[rid]['source_id'],arrival=r['received_at']) for rid,r in desk.state['requests'].items()
                if r['status']=='queued' or (r['status']=='deferred' and r['defer_until'] is not None and r['defer_until']<=at)]
    def start_review(at):
        nonlocal busy,group,switches,returns
        if busy is not None or held_release or at>=horizon:return
        rid,group,opened=choose(pending(at),policy,previous_source,group)
        if rid is None:return
        item=itemmap[rid];attempts[rid]+=1;attempted.add(rid);waits.setdefault(rid,at-item['arrival'])
        if previous_source is not None and previous_source!=item['source_id']:switches+=1
        if item['source_id'] in seen and item['source_id']!=previous_source:returns+=1
        seen.add(item['source_id'])
        if opened and policy=='G':cmd('session',dict(ids=group),at)
        cmd('select',dict(id=rid),at)
        plan=env.plan(item,policy,seed,attempts[rid],at,memory,completed,previous_source,cfg,opened)
        cursor=at;segments=[]
        for name,duration in plan['phases']:
            segments.append([name,cursor,cursor+duration]);cursor+=duration
            time_spent[name]+=max(0,min(horizon,cursor)-min(horizon,cursor-duration))
        decision_at=cursor-(cfg['interaction_seconds']/2 if plan['releases'] else 0)
        record=dict(id=rid,source_id=item['source_id'],attempt=attempts[rid],start=at,decision_at=decision_at,end=cursor,segments=segments,
                    action=plan['action'],potential_correct=plan['correct'],origin=plan['origin'],group_opened=opened and policy=='G',carryover_harm=plan['carryover_harm'])
        reviews.append(record);busy=dict(id=rid,plan=plan,record=record)
        if decision_at<=horizon:push(decision_at,'decision',busy)
        # A cutoff leaves the active request/unfinished computation intact.
    while heap:
        at,seq,kind,data=heapq.heappop(heap)
        if at>horizon:break
        now=at
        if kind=='start':cmd('admit',dict(id=data),at);cmd('start',dict(id=data),at)
        elif kind=='arrival':
            output=itemmap[data]['output'] if policy!='M' else dict(answer=[],scale='',evidence=[],derivation='Manual source-only simulation; no model draft',issues=[])
            cmd('receive',dict(id=data,output=deepcopy(output),origin='actual_saved_model_output' if policy!='M' else 'simulation_manual_placeholder'),at)
        elif kind=='decision':
            rid=data['id'];plan=data['plan'];item=itemmap[rid]
            payload=dict(id=rid,version=desk.state['active']['version'],decision=plan['action'],by='simulated_reviewer')
            if plan['action']=='correct':payload['output']=plan['output']
            if plan['action']=='defer':payload.update(until=at+cfg['defer_seconds'],note='SIMULATION: unresolved construction; retained for one further attempt')
            result=cmd('decide',payload,at)
            completed+=1;memory[item['source_id']]=(at,completed);previous_source=item['source_id'];busy=None
            if plan['releases']:
                held_release=True
                push(data['record']['end'],'release',dict(id=rid,version=result['version'],correct=plan['correct'],origin=plan['origin'],carryover_harm=plan['carryover_harm']))
            elif plan['action']=='defer':push(at+cfg['defer_seconds'],'wake',rid)
        elif kind=='release':
            cmd('release',dict(id=data['id'],version=data['version']),at);held_release=False
            observed.append(dict(id=data['id'],correct=data['correct'],origin=data['origin'],carryover_harm=data['carryover_harm']))
        elif kind!='wake':raise ValueError(kind)
        # Process every exogenous event at this timestamp before the next choice.
        if not heap or heap[0][0]>at:start_review(at)
    cmd('close_session',{},horizon)
    counts=desk.counts();correct=sum(x['correct'] for x in observed);wrong=len(observed)-correct
    assert counts['offered']==len(items) and counts['released']==len(observed)
    assert correct+wrong+(len(items)-len(observed))==len(items)
    assert sum(time_spent.values())<=horizon+1e-7
    # Queue-wait estimate includes never-selected received requests through cutoff.
    allwait=[waits.get(x['id'],max(0,horizon-x['arrival'])) for x in items if x['arrival']<=horizon]
    unrelated_wait=0.
    for item in items:
        first=next((r['start'] for r in reviews if r['id']==item['id']),horizon)
        for r in reviews:
            if r['source_id']!=item['source_id']:
                unrelated_wait+=max(0,min(horizon,first,r['end'])-max(item['arrival'],r['start']))
    summary=dict(correct=correct,incorrect=wrong,released=len(observed),unfinished=len(items)-len(observed),offered=len(items),admitted=counts['admitted'],started=counts['started'],received=counts['received'],
                 never_selected=len(items)-len(attempted),unstarted=counts['unstarted'],deferred=counts['deferred'],active=counts['active'],approved_unreleased=counts['resolved']-counts['released'],
                 blocked=sum(r['status']=='resolved' and not desk.current_released(rid) and any(d['request_id']==rid and d['decision']=='reject' for d in desk.state['decisions']) for rid,r in desk.state['requests'].items()),
                 review_attempts=sum(attempts.values()),revisits=sum(max(0,v-1) for v in attempts.values()),source_switches=switches,source_returns=returns,
                 mean_wait=sum(allwait)/len(allwait) if allwait else 0.,unrelated_wait_sum=unrelated_wait,carryover_harms=sum(x['carryover_harm'] for x in observed),
                 initial_correct=sum(env.initial_correct[x['id']] for x in items),released_initial_correct=sum(env.initial_correct[x['id']] for x in observed),
                 repairs=sum(x['correct'] and not env.initial_correct[x['id']] for x in observed) if policy!='M' else 0,
                 damage=sum(not x['correct'] and env.initial_correct[x['id']] for x in observed) if policy!='M' else 0,
                 groups=sum(r['group_opened'] for r in reviews),events=events)
    # Rejections are not approvals waiting for release.
    summary['approved_unreleased']-=summary['blocked']
    for name in ('orientation','question','verification','construction','interaction','release','grouping'):summary['time_'+name]=time_spent[name]
    summary['time_idle']=horizon-sum(time_spent.values())
    trace=dict(schema='oversight-simulation-trace-v1',record_kind='computational_simulation',commands=cmds,reviews=reviews,observed_outcomes=observed,final_state_sha256=digest(desk.logical())) if keep_trace else None
    return summary,trace


def replay_trace(trace,items,sources,policy,full_engine=False):
    desk=SimulationDesk('sessions' if policy=='G' else 'queue') if full_engine else FastDesk('sessions' if policy=='G' else 'queue')
    itemmap={i['id']:i for i in items}
    for n,(at,action,payload) in enumerate(trace['commands']):
        p=deepcopy(payload)
        if action=='offer':
            i=itemmap[p['id']];p=dict(id=i['id'],agent=i['agent'],question_id=i['id'],question=i['question'],source=sources[i['source_id']],dependencies=[])
        if action=='receive':
            p.update(output=deepcopy(itemmap[p['id']]['output']) if policy!='M' else dict(answer=[],scale='',evidence=[],derivation='Manual source-only simulation; no model draft',issues=[]),origin='actual_saved_model_output' if policy!='M' else 'simulation_manual_placeholder')
        if full_engine:
            result=desk.command('sim:'+str(n),action,p,at=at)
            assert result['ok'],result
        else:desk.apply(action,p,at)
    return digest(desk.logical())
