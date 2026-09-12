import unittest,copy
from .desk import Desk
from .online import OnlineController
from .synthetic import instance
class OnlineTests(unittest.TestCase):
 def test_reask_after_revision_preserves_budget_and_history(self):
  d=Desk();d.act({'action':'inspect'});d.act({'action':'answer','value':'spending'});spent=d.c.spent;old=list(d.c.events);d.act({'action':'snapshot'});d.act({'action':'inspect'});self.assertIsNotNone(d.question);self.assertEqual(d.c.spent,spent);self.assertTrue(all(e in d.c.events for e in old));self.assertEqual(d.question['task'],'count')
 def test_intent_revision_is_scoped_and_does_not_reset_budget(self):
  d=Desk();d.act({'action':'inspect'});d.act({'action':'answer','value':'spending'});before={t['id']:t['version'] for t in d.c.tasks}
  d.act({'action':'reconsider','task':'export'});after={t['id']:t['version'] for t in d.c.tasks}
  self.assertGreater(after['export'],before['export']);self.assertGreater(after['count'],before['count']);self.assertEqual(after['partner'],before['partner']);self.assertEqual(after['inventory'],before['inventory']);self.assertEqual(d.c.spent,1)
  d.act({'action':'inspect'});self.assertEqual(d.question['scope'],'Atlas/segment')
 def test_independent_answers_are_not_blocked_by_shared_identifier(self):
  tasks,prep,_,answers=instance('shared_decision',7200)
  tasks[1]['contract']['explicit_semantic_choice_required']=True
  c=OnlineController(tasks,prep,2,24,'no_sharing')
  first=c.next_question();c.answer(first,{'sql_by_task':answers})
  second=c.next_question();self.assertIsNotNone(second);self.assertNotEqual(first['task'],second['task'])
  c.answer(second,{'sql_by_task':answers});self.assertEqual(c.spent,2)
 def test_failed_answer_is_not_executed_again_without_change(self):
  tasks,prep,_,_=instance('missing_preference',7200);c=OnlineController(tasks,prep,1,24,'verification')
  q=c.next_question();c.answer(q,{'sql_by_task':{'export':'SELECT absent FROM customers'}});used=c.machine.used
  c.inspect();self.assertEqual(c.machine.used,used);self.assertEqual(c.records['export']['status'],'unfinished')
 def test_revoked_source_is_not_recovered(self):
  tasks,prep,_,_=instance('available_source',7200);tasks[0]['sources'][0]['status']='revoked'
  c=OnlineController(tasks,prep,0,24,'verification');c.inspect();self.assertNotEqual(c.records['export']['reason'],'source_recovery')
 def test_replaced_source_invalidates_quoted_provenance(self):
  tasks,prep,_,_=instance('available_source',7200);c=OnlineController(tasks,prep,0,24,'verification');c.inspect()
  sources=copy.deepcopy(tasks[0]['sources']);sources[0].update(text='Use orders, replacing the old instruction.',version=2)
  c.revise('export',sources=sources);c.inspect();self.assertNotEqual(c.records['export']['reason'],'source_recovery')
 def test_stale_answer_rejected(self):
  d=Desk();d.act({'action':'inspect'});d.c.revise('export',sources=[])
  with self.assertRaises(ValueError):d.act({'action':'answer','value':'spending'})
 def test_narrow_is_atomic(self):
  d=Desk();d.act({'action':'reset','budget':1});d.act({'action':'inspect'});state=copy.deepcopy(d.state())
  with self.assertRaises(ValueError):d.act({'action':'answer','value':'orders','only_this_request':True})
  self.assertEqual(d.state(),state)
 def test_scope_exception_and_source(self):
  d=Desk();d.act({'action':'inspect'});d.act({'action':'answer','value':'orders'});w={x['id']:x for x in d.state()['work']};self.assertEqual(w['partner']['status'],'unfinished');self.assertEqual(w['inventory']['reason'],'source_recovery')
 def test_two_decisions_for_narrow(self):
  d=Desk();d.act({'action':'inspect'});d.act({'action':'answer','value':'orders','only_this_request':True});self.assertEqual(d.c.spent,2)
  self.assertEqual(d.c.records['count']['reason'],'outcome_agreement')
  self.assertEqual(d.c.answers[('segment','Atlas/segment')]['exceptions'],['count'])
  self.assertNotIn('count',d.c.answers[('segment','Atlas/segment')]['sql_by_task'])
if __name__=='__main__':unittest.main()
