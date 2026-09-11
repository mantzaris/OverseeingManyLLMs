import unittest,copy
from .engine import MachineBudget,execute,equivalent,verification_key
from .controller import Controller
from .synthetic import instance
from .common import digest
class Semantics(unittest.TestCase):
 def test_information_isolation(self):
  t,p,y,a=instance('missing_preference',7000);c=Controller(t,p,1);q=c.next_question();y[t[0]['id']]='SELECT 999';a.clear();from .evaluate import strip_time;self.assertEqual(strip_time(q),strip_time(Controller(t,p,1).next_question()))
 def test_budget(self):
  t,p,y,a=instance('missing_preference',7000);c=Controller(t,p,0);self.assertIsNone(c.next_question());self.assertLessEqual(c.machine.used,24)
  c=Controller(t,p,1);q=c.next_question();c.answer(q,None)
  with self.assertRaises(ValueError):c.answer(q,None)
  c=Controller(t,p,1,0);c.inspect();self.assertTrue(all(r['status']=='unfinished' for r in c.records.values()))
 def test_failure_not_equivalence(self):
  t,p,y,a=instance('failed_query',7000);c=Controller(t,p,0);c.inspect();self.assertEqual(c.records['export']['status'],'unfinished')
 def test_empty_trap(self):
  t,p,y,a=instance('empty_trap',7000);c=Controller(t,p,0);c.inspect();self.assertEqual(c.records['export']['status'],'unfinished')
 def test_conditional_omission(self):
  t,p,y,a=instance('omitted_intent',7000);c=Controller(t,p,0);c.inspect();self.assertEqual(c.records['export']['reason'],'outcome_agreement');target=execute(t[0]['snapshot'],y['export'],MachineBudget(1));self.assertNotEqual(target['table_hash'],c.records['export']['result']['table_hash'])
 def test_snapshot_invalidation(self):
  t,p,y,a=instance('snapshot_change',7000);c=Controller(t,p,0);c.inspect();self.assertEqual(c.records['export']['status'],'released');c.revise('export',snapshot=t[0]['snapshot']+'UPDATE customers SET orders=0 WHERE id=1;');c.inspect();self.assertEqual(c.records['export']['status'],'unfinished')
 def test_source_scope(self):
  t,p,y,a=instance('irrelevant_source',7000);c=Controller(t,p,0);self.assertFalse(c.recovery(t[0],p['export']))
 def test_scope_exception(self):
  t,p,y,a=instance('scope_exception',7000);c=Controller(t,p,1);q=c.next_question();c.answer(q,{'sql_by_task':a});self.assertEqual(sum(r['reason']=='user_answer' for r in c.records.values()),1)
 def test_process_constraint(self):
  t,p,y,a=instance('process_requirement',7000);c=Controller(t,p,0);c.inspect();self.assertEqual(c.records['export']['status'],'unfinished')
 def test_bag_null_shape(self):
  s='CREATE TABLE t(x);INSERT INTO t VALUES(NULL),(1),(1);'
  a=execute(s,'SELECT x FROM t',MachineBudget(1));b=execute(s,'SELECT DISTINCT x FROM t',MachineBudget(1));self.assertFalse(equivalent([a,b]));self.assertFalse(equivalent([a,execute(s,'SELECT x,x FROM t',MachineBudget(1))]))
 def test_write_guard(self):
  r=execute('CREATE TABLE t(x);','DELETE FROM t',MachineBudget(1));self.assertEqual(r['status'],'failed')
 def test_replay(self):
  from .evaluate import strip_time
  t,p,y,a=instance('equal_snapshot',7000);a=Controller(t,p,0);b=Controller(t,p,0);a.inspect();b.inspect();self.assertEqual(strip_time(a.result()),strip_time(b.result()))
 def test_baseline_agreement(self):
  t,p,y,a=instance('shared_decision',7000)
  qs=[Controller(t,p,1,method=m).next_question()['decision'] for m in ['recovery_completion','recovery_depth2']];self.assertEqual(qs[0],qs[1])
if __name__=='__main__':unittest.main()
