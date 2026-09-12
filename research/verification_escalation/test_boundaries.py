"""Extra adversarial checks. These test limits, not stronger guarantees."""
import copy,unittest
from .synthetic import instance
from .controller import Controller
from .engine import execute,MachineBudget,verification_key

class BoundaryTests(unittest.TestCase):
 def test_aggregate_zero_is_not_an_empty_result_certificate(self):
  tasks,prep,targets,answers=instance('equal_snapshot',7200)
  qs=['SELECT count(*) FROM customers WHERE id<0','SELECT count(*) FROM customers WHERE id<0 AND 1=1']
  for obj in prep['export'].values():
   obj['candidates']=[dict(sql=q,meaning='Unverified restrictive interpretation') for q in qs]
  c=Controller(tasks,prep,0,24,'verification');c.inspect();r=c.result()['records']['export']
  self.assertEqual(r['reason'],'outcome_agreement')
  target=execute(tasks[0]['snapshot'],targets['export'],MachineBudget(1))
  self.assertNotEqual(r['result']['table_hash'],target['table_hash'])
  # COUNT returns one row. The nonempty heuristic cannot guarantee meaningfulness.
  self.assertEqual(r['result']['row_count'],1)
 def test_key_changes_for_each_registered_dependency(self):
  tasks,prep,_,_=instance('equal_snapshot',7200);t=tasks[0];key=verification_key(t,prep['export'])
  for field,value in [('request','new request'),('contract',{'kind':'sql_program','ordered':True}),('scope','Different project'),('version',2),('exceptions',['export']),('sources',[{'text':'new instruction'}]),('decision_id','different decision')]:
   changed=copy.deepcopy(t);changed[field]=value
   self.assertNotEqual(key,verification_key(changed,prep['export']),field)
 def test_execution_failure_charges_machine_budget(self):
  b=MachineBudget(1);r=execute('CREATE TABLE x(a);','SELECT missing FROM x',b)
  self.assertEqual(r['status'],'failed');self.assertEqual(b.used,1)
  self.assertIn('execution_budget',execute('CREATE TABLE x(a);','SELECT a FROM x',b)['error']);self.assertEqual(b.used,1)
 def test_agent_labels_do_not_create_goals_or_utility(self):
  tasks,prep,_,_=instance('shared_decision',7200)
  a=Controller(tasks,prep,0,24,'verification');a.inspect()
  labeled=copy.deepcopy(tasks)
  for t in labeled:t['agent_roles']=['agent_'+str(i) for i in range(8)]
  b=Controller(labeled,prep,0,24,'verification');b.inspect()
  self.assertEqual(set(a.result()['records']),set(b.result()['records']))
  for k in a.result()['records']:
   self.assertEqual(a.result()['records'][k]['status'],b.result()['records'][k]['status'])

if __name__=='__main__':unittest.main()
