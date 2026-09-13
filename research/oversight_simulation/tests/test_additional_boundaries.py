"""Post-freeze read-only validation; no change to the declared model or matrix."""
import unittest
from copy import deepcopy
from research.oversight_workflow.common import read
from research.oversight_simulation.inputs import OUT,workload
from research.oversight_simulation.run import environment
from research.oversight_simulation.reviewer import ReviewerEnvironment,uniform
from research.oversight_simulation.simulation import simulate


class ExtraBoundaryTests(unittest.TestCase):
    def test_hidden_annotations_cannot_change_first_dispatch(self):
        inputs=read(OUT/'inputs.json');c=read(OUT/'design.json')['configs'][17]
        items=workload(inputs,c,0);env=environment(inputs)
        hidden=deepcopy(env.annotations)
        for q in hidden:hidden[q]['answer']='DIFFERENT_UNASKED_REFERENCE'
        other=ReviewerEnvironment(hidden,{q:not v for q,v in env.initial_correct.items()})
        for policy in ('Q','G','Q-source-aware','Q-sticky','M'):
            _,a=simulate(items,inputs['sources'],c,policy,5,env)
            _,b=simulate(items,inputs['sources'],c,policy,5,other)
            def prefix(trace):
                result=[]
                for event in trace['commands']:
                    result.append(event)
                    if event[1]=='select':break
                return result
            self.assertEqual(prefix(a),prefix(b))
    def test_manual_has_no_verification_or_initial_draft_approval(self):
        inputs=read(OUT/'inputs.json');c=read(OUT/'design.json')['configs'][17]
        s,t=simulate(workload(inputs,c,0),inputs['sources'],c,'M',5,environment(inputs))
        self.assertEqual(s['time_verification'],0)
        self.assertFalse(any(a=='decide' and p['decision']=='approve' for _,a,p in t['commands']))
    def test_pairing_does_not_depend_on_call_order(self):
        x=[uniform(7,q,1,'detection') for q in ('a','b','c')]
        y={q:uniform(7,q,1,'detection') for q in ('c','a','b')}
        self.assertEqual(x,[y[q] for q in ('a','b','c')])
    def test_approval_before_cutoff_is_not_a_release(self):
        inputs=read(OUT/'inputs.json');c=read(OUT/'design.json')['configs'][17];items=workload(inputs,c,0)
        _,t=simulate(items,inputs['sources'],c,'M',5,environment(inputs))
        first=t['reviews'][0];c={**c,'horizon':(first['decision_at']+first['end'])/2}
        s,t=simulate(items,inputs['sources'],c,'M',5,environment(inputs))
        if first['action']=='correct':
            self.assertEqual(s['released'],0);self.assertEqual(s['approved_unreleased'],1)
        self.assertEqual(s['correct']+s['incorrect']+s['unfinished'],12)

if __name__=='__main__':unittest.main()
