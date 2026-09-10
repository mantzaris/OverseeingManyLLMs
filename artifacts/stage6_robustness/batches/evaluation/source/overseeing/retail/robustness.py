"""Stage 6 intervention variants, isolated from historical retail semantics."""
import copy
from dataclasses import asdict, dataclass
from itertools import permutations
import math
import time

from .risk import RiskFeatures
from .scheduler import POLICIES
from .simulation import simulate as historical_simulate
from .upstream import invoke,state_hash

VARIANTS=('reference','approve_block','complexity_time')


@dataclass(frozen=True)
class ReviewRequest:
    request_id: str
    agent_id: int
    arrived: int
    cutoff: int
    review_ticks: int
    p_error: float
    processing_cost: int
    recoverable_service_cost: int

    @property
    def tie_key(self):return (self.arrived,self.agent_id,self.request_id)

    def benefit(self,completion):
        return self.p_error*(self.processing_cost+self.recoverable_service_cost) if completion<=self.cutoff else 0.0


def choose(policy,pending,tick):
    """Enumerate only typed, released public requests, with historical tie rules."""
    if policy not in POLICIES:raise ValueError('Unknown policy')
    if len(pending)>3 or any(type(r) is not ReviewRequest for r in pending):raise ValueError('Expected up to three public requests')
    start=time.perf_counter()
    eligible=sorted((r for r in pending if r.arrived<=tick and r.benefit(tick+r.review_ticks)>0),key=lambda r:r.tie_key)
    selected=None;examined=0
    if eligible and policy!='no_review':
        if policy=='fcfs':selected=eligible[0]
        elif policy=='edf':selected=min(eligible,key=lambda r:(r.cutoff,r.tie_key))
        elif policy=='uncertainty':selected=min(eligible,key=lambda r:(-r.p_error,r.tie_key))
        elif policy=='greedy':selected=min(eligible,key=lambda r:(-r.benefit(tick+r.review_ticks),r.tie_key))
        else:
            best=(0,0,());examined=1
            for length in range(1,len(eligible)+1):
                for order in permutations(eligible,length):
                    finish=tick;values=[]
                    for request in order:
                        finish+=request.review_ticks;values.append(request.benefit(finish))
                    key=(-math.fsum(values),length,tuple(r.tie_key for r in order));examined+=1
                    if key<best:best,selected=key,order[0]
    record=dict(policy=policy,tick=tick,public_pending=[asdict(r) for r in pending],eligible=[r.request_id for r in eligible],
        selected=selected.request_id if selected else None,planning_seconds=time.perf_counter()-start,ordered_subsets_evaluated=examined)
    return record['selected'],record


def review_ticks(proposal,base_duration,variant):
    if variant not in VARIANTS:raise ValueError('Unknown operational variant')
    count=len(proposal['arguments'].get('item_ids',[]))
    return base_duration+int(variant=='complexity_time' and count>=2)


def simulate(bundle,prepared,cases,databases,estimator,policy,duration,variant):
    if variant not in VARIANTS:raise ValueError('Unknown operational variant')
    if variant=='reference':
        result=historical_simulate(bundle,prepared,cases,databases,estimator,policy,duration)
        result.update(variant=variant,blocked_unresolved=0,unstaged_failures=sum(p['proposal'] is None for p in prepared))
        for row in result['jobs']:row['blocked_unresolved']=False
        return result
    pending={};states={k:copy.deepcopy(v) for k,v in databases.items()}
    events=[];active=None;committed=set();blocked=set();reviews=[];rows=[]
    plans={p['case_id']:p for p in prepared};slots={s['case_id']:s for s in bundle['slots']}
    for slot in bundle['slots']:
        case_id=slot['case_id'];p=plans[case_id]
        if p['proposal'] is not None:
            pending[case_id]=ReviewRequest(case_id,slot['agent_id'],slot['arrival'],slot['cutoff'],
                review_ticks(p['proposal'],duration,variant),estimator.predict(RiskFeatures(**p['features'])),
                slot['wrong_transaction_cost'],0 if variant=='approve_block' else bundle['service_failure_cost'])
    def commit(case_id,tick,reviewed):
        proposal=cases[case_id]['target_action'] if reviewed and variant!='approve_block' else plans[case_id]['proposal']
        response=invoke(states[case_id],proposal)
        if response.startswith('Error:'):raise ValueError('Validated mutation failed at commitment: '+response)
        after=state_hash(states[case_id]);correct=after==cases[case_id]['target_state_hash']
        events.append(dict(event='transaction_committed',tick=tick,case_id=case_id,reviewed=reviewed,action=proposal,
            response=response,state_hash=after,task_completed=correct,corrected=reviewed and plans[case_id]['initial_error']))
        committed.add(case_id);pending.pop(case_id,None)
    horizon=max(s['cutoff'] for s in bundle['slots'])
    for tick in range(horizon+1):
        if active and active[1]==tick:
            case_id,_,started=active
            assert case_id not in committed and case_id not in blocked
            # Truth is consulted only now, at completed perfect diagnosis.
            if variant=='approve_block' and plans[case_id]['initial_error']:
                blocked.add(case_id);pending.pop(case_id,None)
                events.append(dict(event='transaction_blocked',tick=tick,case_id=case_id,state_hash=state_hash(states[case_id]),
                    task_completed=False,service_unresolved=True,definitive_feedback=True))
            else:commit(case_id,tick,True)
            reviews.append(dict(case_id=case_id,started=started,completed=tick,waiting=started-slots[case_id]['arrival']))
            events.append(dict(event='review_completed',tick=tick,case_id=case_id,definitive_feedback=True))
            active=None
        for slot in bundle['slots']:
            case_id=slot['case_id']
            if slot['arrival']==tick and case_id in pending:
                events.append(dict(event='review_request_arrived',tick=tick,request=asdict(pending[case_id])))
            if slot['cutoff']==tick and case_id not in committed and case_id not in blocked and plans[case_id]['proposal'] is not None:
                commit(case_id,tick,False)
                events.append(dict(event='processing_cutoff',tick=tick,case_id=case_id,useful_opportunity_expired=plans[case_id]['initial_error']))
        if active is None:
            public=[r for r in pending.values() if r.arrived<=tick]
            selected,record=choose(policy,public,tick)
            greedy,_=choose('greedy',public,tick);search,_=choose('search',public,tick);edf,_=choose('edf',public,tick)
            record.update(event='dispatch',greedy_choice=greedy,search_choice=search,edf_choice=edf);events.append(record)
            if selected:
                finish=tick+pending[selected].review_ticks;active=(selected,finish,tick)
                events.append(dict(event='review_started',tick=tick,case_id=selected,completion=finish))
    assert active is None
    for slot in bundle['slots']:
        case_id=slot['case_id'];p=plans[case_id]
        correct=case_id in committed and state_hash(states[case_id])==cases[case_id]['target_state_hash']
        wrong_commit=case_id in committed and not correct
        row=dict(case_id=case_id,agent_id=slot['agent_id'],family=cases[case_id]['family'],task_completed=correct,
            wrong_transaction_committed=wrong_commit,blocked_unresolved=case_id in blocked,
            service_failure_loss=0 if correct else bundle['service_failure_cost'],
            wrong_transaction_loss=slot['wrong_transaction_cost'] if wrong_commit else 0,
            initial_error=p['initial_error'],staged=p['proposal'] is not None,
            reviewed=any(r['case_id']==case_id for r in reviews),automatic_rejections=p['automatic_rejections'])
        row['operational_loss']=row['service_failure_loss']+row['wrong_transaction_loss'];rows.append(row)
    return dict(bundle_id=bundle['bundle_id'],replicate=bundle['replicate'],policy=policy,review_duration=duration,variant=variant,
        **{name:sum(r[key] for r in rows) for name,key in [('operational_loss','operational_loss'),('task_completed','task_completed'),
            ('wrong_transactions','wrong_transaction_committed'),('service_failure_loss','service_failure_loss'),('wrong_transaction_loss','wrong_transaction_loss'),
            ('blocked_unresolved','blocked_unresolved')]},unstaged_failures=sum(p['proposal'] is None for p in prepared),
        completed_reviews=len(reviews),corrections=0 if variant=='approve_block' else sum(plans[r['case_id']]['initial_error'] for r in reviews),
        expired_useful_opportunities=sum(r['wrong_transaction_committed'] for r in rows),
        review_busy_ticks=sum(r['completed']-r['started'] for r in reviews),
        review_utilization=sum(r['completed']-r['started'] for r in reviews)/horizon,
        total_waiting_ticks=sum(r['waiting'] for r in reviews),
        multi_eligible_dispatches=sum(e.get('event')=='dispatch' and len(e['eligible'])>=2 for e in events),
        greedy_search_different_heads=sum(e.get('event')=='dispatch' and e['greedy_choice']!=e['search_choice'] for e in events),
        review_sequence=[r['case_id'] for r in reviews],jobs=rows,events=events,status='completed')


def without_timing(result):
    result=copy.deepcopy(result)
    for event in result['events']:event.pop('planning_seconds',None)
    return result
