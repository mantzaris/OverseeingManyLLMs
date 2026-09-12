import unittest
from .engine import MachineBudget
from .integrity import check_snapshot,ValidatedController
from .synthetic import instance
class IntegrityTests(unittest.TestCase):
 def test_foreign_key_violation_blocks_equality(self):
  t,p,_,_=instance('equal_snapshot',7200);t[0]['snapshot']+='CREATE TABLE orphan(p INTEGER REFERENCES customers(id));INSERT INTO orphan VALUES(99);'
  c=ValidatedController(t,p,1,24);self.assertIsNone(c.next_question());self.assertEqual(c.records['export']['reason'],'source_integrity_failed');self.assertEqual(c.spent,0)
 def test_broken_load_never_certifies(self):
  t,p,_,_=instance('equal_snapshot',7200);t[0]['snapshot']='not valid sqlite'
  c=ValidatedController(t,p,1,24);c.inspect();self.assertEqual(c.records['export']['status'],'unfinished')
 def test_integrity_checks_are_budgeted_and_cached(self):
  t,p,_,_=instance('equal_snapshot',7200);c=ValidatedController(t,p,0,24);c.inspect();used=c.machine.used;c.inspect();self.assertEqual(c.machine.used,used)
  r=check_snapshot(t[0]['snapshot'],MachineBudget(1));self.assertEqual(r['status'],'failed')
 def test_independent_valid_task_continues(self):
  t,p,_,_=instance('unaffected_work',7200);t[0]['snapshot']='invalid';c=ValidatedController(t,p,0,48);c.inspect();self.assertEqual(c.records['export']['status'],'unfinished');self.assertEqual(c.records['inventory']['status'],'released')
if __name__=='__main__':unittest.main()
