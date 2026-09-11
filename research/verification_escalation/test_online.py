import unittest,copy
from .desk import Desk
from .online import OnlineController
from .synthetic import instance
class OnlineTests(unittest.TestCase):
 def test_reask_after_revision_preserves_budget_and_history(self):
  d=Desk();d.act({'action':'inspect'});d.act({'action':'answer','value':'spending'});spent=d.c.spent;old=list(d.c.events);d.act({'action':'snapshot'});d.act({'action':'inspect'});self.assertIsNotNone(d.question);self.assertEqual(d.c.spent,spent);self.assertTrue(all(e in d.c.events for e in old));self.assertEqual(d.question['task'],'count')
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
if __name__=='__main__':unittest.main()
