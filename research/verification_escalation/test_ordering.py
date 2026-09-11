import unittest
from .repair_data import public_task
from .engine import execute,equivalent,MachineBudget
class OrderingTests(unittest.TestCase):
 def case(self,q):return dict(id='x',question=q,schema='[]',snapshot='CREATE TABLE t(x);',clarifications=[''],refs=[''])
 def test_public_detection(self):
  for q in ['List movies sorted by descending duration','Sort items by cost','Show highest costs first','Top 5 items']:
   self.assertTrue(public_task(self.case(q),0)['contract']['ordered'])
  self.assertFalse(public_task(self.case('Find order identifiers'),0)['contract']['ordered'])
 def test_different_order_is_consequential(self):
  s='CREATE TABLE t(x);INSERT INTO t VALUES(1),(2);'
  a=execute(s,'SELECT x FROM t ORDER BY x',MachineBudget(1),True);b=execute(s,'SELECT x FROM t ORDER BY x DESC',MachineBudget(1),True);self.assertFalse(equivalent([a,b]))
 def test_order_from_available_source(self):
  c=self.case('Show products');c['clarifications']=['List products in ascending cost order'];self.assertTrue(public_task(c,0,True)['contract']['ordered'])
if __name__=='__main__':unittest.main()
