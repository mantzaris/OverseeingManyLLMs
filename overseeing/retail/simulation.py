"""Deterministic application of review policies to saved GPU-prepared transactions."""
import copy
from dataclasses import asdict

from .risk import RiskFeatures
from .scheduler import TransactionRequest, choose
from .upstream import invoke, state_hash


def simulate(bundle,prepared,cases,databases,estimator,policy,duration):
    pending={};states={k:copy.deepcopy(v) for k,v in databases.items()}
    events=[];active=None;committed=set();reviews=[];rows=[]
    plans={p['case_id']:p for p in prepared}
    for slot in bundle['slots']:
        case_id=slot['case_id'];p=plans[case_id]
        if p['proposal'] is not None:
            pending[case_id]=TransactionRequest(case_id,slot['agent_id'],slot['arrival'],slot['cutoff'],duration,
                estimator.predict(RiskFeatures(**p['features'])),slot['wrong_transaction_cost'],bundle['service_failure_cost'])
    def commit(case_id,tick,reviewed):
        proposal=cases[case_id]['target_action'] if reviewed else plans[case_id]['proposal']
        response=invoke(states[case_id],proposal)
        if response.startswith('Error:'):raise ValueError('Validated staged transaction failed at commit: '+response)
        after=state_hash(states[case_id]);correct=after==cases[case_id]['target_state_hash']
        events.append(dict(event='transaction_committed',tick=tick,case_id=case_id,reviewed=reviewed,
            action=proposal,response=response,state_hash=after,task_completed=correct,
            corrected=reviewed and plans[case_id]['initial_error']))
        committed.add(case_id);pending.pop(case_id,None)
    horizon=max(s['cutoff'] for s in bundle['slots'])
    for tick in range(horizon+1):
        # Completion at the cutoff is timely; it precedes irreversible processing.
        if active and active[1]==tick:
            case_id,_,started=active
            if case_id not in committed:
                commit(case_id,tick,True);reviews.append(dict(case_id=case_id,started=started,completed=tick,
                    waiting=started-next(s['arrival'] for s in bundle['slots'] if s['case_id']==case_id)))
                events.append(dict(event='review_completed',tick=tick,case_id=case_id,definitive_feedback=True))
            active=None
        for slot in bundle['slots']:
            case_id=slot['case_id']
            if slot['arrival']==tick and case_id in pending:
                events.append(dict(event='review_request_arrived',tick=tick,request=asdict(pending[case_id])))
            if slot['cutoff']==tick and case_id not in committed and plans[case_id]['proposal'] is not None:
                commit(case_id,tick,False)
                events.append(dict(event='processing_cutoff',tick=tick,case_id=case_id,
                    useful_opportunity_expired=plans[case_id]['initial_error']))
        if active is None:
            public=[r for r in pending.values() if r.arrived<=tick]
            selected,record=choose(policy,public,tick)
            # Same-state alternatives are diagnostics, never used to change the selected policy.
            greedy,_=choose('greedy',public,tick);search,_=choose('search',public,tick);edf,_=choose('edf',public,tick)
            record.update(event='dispatch',greedy_choice=greedy,search_choice=search,edf_choice=edf)
            events.append(record)
            if selected:
                active=(selected,tick+duration,tick)
                events.append(dict(event='review_started',tick=tick,case_id=selected,completion=tick+duration))
    for slot in bundle['slots']:
        case_id=slot['case_id'];p=plans[case_id]
        correct=case_id in committed and state_hash(states[case_id])==cases[case_id]['target_state_hash']
        wrong_commit=case_id in committed and not correct
        row=dict(case_id=case_id,agent_id=slot['agent_id'],family=cases[case_id]['family'],
            task_completed=correct,wrong_transaction_committed=wrong_commit,
            service_failure_loss=0 if correct else bundle['service_failure_cost'],
            wrong_transaction_loss=slot['wrong_transaction_cost'] if wrong_commit else 0,
            initial_error=p['initial_error'],staged=p['proposal'] is not None,
            reviewed=any(r['case_id']==case_id for r in reviews),
            automatic_rejections=p['automatic_rejections'])
        row['operational_loss']=row['service_failure_loss']+row['wrong_transaction_loss'];rows.append(row)
    result=dict(bundle_id=bundle['bundle_id'],replicate=bundle['replicate'],policy=policy,review_duration=duration,
        operational_loss=sum(r['operational_loss'] for r in rows),task_completed=sum(r['task_completed'] for r in rows),
        wrong_transactions=sum(r['wrong_transaction_committed'] for r in rows),
        service_failure_loss=sum(r['service_failure_loss'] for r in rows),
        wrong_transaction_loss=sum(r['wrong_transaction_loss'] for r in rows),
        completed_reviews=len(reviews),corrections=sum(plans[r['case_id']]['initial_error'] for r in reviews),
        expired_useful_opportunities=sum(r['wrong_transaction_committed'] for r in rows),
        review_busy_ticks=len(reviews)*duration,review_utilization=len(reviews)*duration/horizon,
        total_waiting_ticks=sum(r['waiting'] for r in reviews),
        multi_eligible_dispatches=sum(e.get('event')=='dispatch' and len(e['eligible'])>=2 for e in events),
        greedy_search_different_heads=sum(e.get('event')=='dispatch' and e['greedy_choice']!=e['search_choice'] for e in events),
        review_sequence=[r['case_id'] for r in reviews],jobs=rows,events=events,status='completed')
    return result
