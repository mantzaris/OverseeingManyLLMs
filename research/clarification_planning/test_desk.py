import copy
import json
import unittest
from .desk import Desk
from .planner import UNRESOLVED

class DeskTests(unittest.TestCase):
    def test_scope_can_be_narrowed_without_propagation(self):
        d=Desk();d.act({'action':'next'});q=d.state()['question'];original=q['id'];task=q['enables'][0]
        s=d.act({'action':'answer','value':'user_requirement','only_task':task})
        self.assertEqual(s['spent'],2)
        c=d.controller;p=c.planner
        self.assertFalse(c.state.revealed&(1<<p.index[original]))
        record=next(r for r in s['records'] if r['id']==task+'::'+original)
        self.assertEqual(record['allowed_tasks'],[task]);self.assertEqual(record['affected'],[task])

    def test_narrow_answer_needs_value_and_scope_budget(self):
        d=Desk();d.act({'action':'reset','budget':1})
        d.act({'action':'ask','id':'accessibility'});before=d.state()
        with self.assertRaises(ValueError):d.act({'action':'answer','value':'screen_reader','only_task':'Website implementation'})
        self.assertEqual(d.state(),before)

    def test_unresolved_visible_and_costed(self):
        d=Desk();d.act({'action':'next'});d.act({'action':'defer'})
        self.assertEqual(d.state()['spent'],1)
        self.assertTrue(any(w['status']=='Deferred' for w in d.state()['work']))

    def test_failure_is_transactional(self):
        d=Desk();d.act({'action':'next'});before=d.state()
        with self.assertRaises(ValueError):d.act({'action':'answer','value':'x','only_task':'not_a_task'})
        self.assertEqual(d.state(),before)

    def test_log_action_replay_and_actual_display(self):
        d=Desk();d.act({'action':'reset','budget':4,'method':'depth2'})
        d.act({'action':'next'});question=d.state()['question']
        self.assertEqual(d.events[-1]['displayed_question'],question)
        d.act({'action':'answer','value':'screen_reader'})
        d.act({'action':'next'});d.act({'action':'answer','value':'web'})
        d.act({'action':'finish'})
        e=Desk()
        for event in d.events:
            if event['action']!='started':e.act(event['payload'])
        self.assertEqual(e.state(),d.state())

    def test_revision_shows_affected_work_and_keeps_budget(self):
        d=Desk();d.act({'action':'next'});d.act({'action':'answer','value':'screen_reader'})
        d.act({'action':'next'});d.act({'action':'answer','value':'web'});d.act({'action':'finish'})
        self.assertEqual(d.state()['spent'],2)
        d.act({'action':'revise','id':'format','value':'pdf'})
        changed=[w for w in d.state()['work'] if w['registered_release']=='needs_revalidation']
        self.assertGreaterEqual(len(changed),3);self.assertEqual(d.state()['spent'],2)

if __name__=='__main__':unittest.main()
