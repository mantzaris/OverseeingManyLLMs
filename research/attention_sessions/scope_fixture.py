"""Stipulated authority mechanics. These are not observations or pilot cases."""
from dataclasses import replace
from .method import Request,Settings,validate_shared_answer
from .controller import Controller
from .data import ROOT,save_json

def examples():
    a=Request('decision-a','record-a','record-a',0,10,4,.5,.5,'normal',{})
    b=replace(a,request_id='decision-b',proposal='heating_valve')
    c=Controller([a,b],Settings(setup=0,switch=0,coordination=0),'guarded')
    c.start(['decision-a','decision-b'],override=True)
    c.complete('normal');c.complete('heating_valve')
    assert c.final=={'decision-a':'normal','decision-b':'heating_valve'}
    rejected=False
    try:validate_shared_answer([a,b],'equipment-similarity',[a.request_id,b.request_id])
    except ValueError:rejected=True
    # A separate fictional common decision has an explicit versioned scope.
    # The labels are evaluator-only. A valid scope authorizes recipients but
    # does not make the answer correct, nor guarantee intervention benefit.
    scope='configuration:record-a:approval-v1'
    shared=[replace(a,scope=scope),replace(b,scope=scope,proposal='normal')]
    ids=validate_shared_answer(shared,scope,[r.request_id for r in shared])
    truth={key:'normal' for key in ids};wrong='heating_valve'
    return dict(evidence_type='stipulated mechanics, not source cases or participant data',
                separate_decisions=dict(final=c.final,events=c.events,similarity_propagation_rejected=rejected),
                explicit_dependency=dict(scope=scope,recipients=list(ids),correct_answer='normal',wrong_answer=wrong,
                                         harmed_recipients=sum(wrong!=truth[key] for key in ids)),
                interpretation='Exact scope prevents unintended recipients; it does not prevent correlated harm from a mistaken shared answer. Shared-answer execution is deliberately absent from the HVAC interface.')

if __name__=='__main__':save_json(ROOT/'scope_mechanics.json',examples())
