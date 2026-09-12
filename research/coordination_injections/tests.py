"""Focused semantics, using authored transactions and controlled responses, no GPU."""
import copy,tempfile,sqlite3,unittest
from pathlib import Path
from unittest.mock import patch
from .contracts import project,contract,ROLES,compile_sql
from .controller import run,artifact_hash,validate_graph,inspect,build_artifact
from .pipeline import deterministic_call,exact_tool_call
from .execution import CREATE,probe_rows,execute,probe
from .common import stable,digest

class ProtocolTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.db=Path(self.tmp.name)/'test.sqlite';self.p=project('test','2011-02','country','France')
  c=sqlite3.connect(str(self.db));c.execute(CREATE);c.executemany('INSERT INTO transactions VALUES(?,?,?,?,?,?,?,?,?,?,?)',probe_rows(contract(self.p,'analysis',0)));c.commit();c.close()
  self.patcher=patch('research.coordination_injections.execution.DB',self.db);self.patcher.start()
 def tearDown(self):self.patcher.stop();self.tmp.cleanup()
 def before(self):return run(self.p,0,generate_fn=deterministic_call)
 def test_actual_repair_and_scope(self):
  initial=self.before();out=run(self.p,0,'targeted',initial['artifacts'],deterministic_call)
  self.assertTrue(all(a['accepted'] for a in out['artifacts'].values()))
  self.assertEqual(artifact_hash(initial['artifacts']['appendix']),artifact_hash(out['artifacts']['appendix']))
  self.assertNotEqual(initial['artifacts']['analysis']['sql'],out['artifacts']['analysis']['sql'])
  self.assertNotEqual(initial['artifacts']['analysis']['execution']['rows'],out['artifacts']['analysis']['execution']['rows'])
 def test_keep_is_not_repair(self):
  def keep(*args):return dict(status='keep',notify=[]),dict(call_id=args[0],attempts=0,tokens=0,seconds=0,status='controlled')
  out=run(self.p,0,'targeted',self.before()['artifacts'],keep)
  self.assertFalse(out['artifacts']['analysis']['accepted']);self.assertLessEqual(len(out['calls']),8)
  self.assertIn('stale_instruction',out['artifacts']['analysis']['online_issues'])
 def test_peer_cannot_extend_authority(self):
  def rogue(*a):
   p,u=deterministic_call(*a);p['notify']=['appendix','external','analysis'];return p,u
  out=run(self.p,0,'sparse',self.before()['artifacts'],rogue)
  self.assertNotIn('appendix',[r['role'] for r in out['routes']])
  self.assertTrue(all(a['accepted'] for a in out['artifacts'].values()))
 def test_adaptive_expansion_repairs_exception_stress(self):
  out=run(self.p,0,'targeted',self.before()['artifacts'],deterministic_call,stress='exception_generalization')
  self.assertTrue(out['artifacts']['appendix']['accepted'])
  self.assertEqual([r['round'] for r in out['routes'] if r['role']=='appendix'],[1])
 def test_malformed_kept_as_unfinished(self):
  def bad(*a):return None,dict(call_id=a[0],attempts=0,tokens=0,seconds=0,status='failed')
  out=run(self.p,0,generate_fn=bad)
  self.assertFalse(any(a['accepted'] for a in out['artifacts'].values()))
  self.assertEqual(len(out['calls']),4)
 def test_external_scope_exception_validation(self):
  from .api import validate_project
  self.assertIs(validate_project(self.p),self.p)
  wrong=copy.deepcopy(self.p);wrong['after']['appendix']['country']='France'
  with self.assertRaises(ValueError):validate_project(wrong)
  peer=copy.deepcopy(self.p);peer['user_change']['source']='peer_agent'
  with self.assertRaises(PermissionError):validate_project(peer)
 def test_cycle_rejected(self):
  with self.assertRaises(ValueError):validate_graph(dict(analysis=['report'],chart=['analysis'],report=['chart'],appendix=[]))
 def test_information_isolation(self):
  # No evaluator state is passed to run; extra hidden labels cannot affect routing or prompts.
  other=copy.deepcopy(self.p);other['evaluator_only']={'answer':'different'}
  a=run(self.p,0,generate_fn=deterministic_call);b=run(other,0,generate_fn=deterministic_call)
  self.assertEqual(stable(a),stable(b))
 def test_hash_ignores_runtime_only(self):
  a=self.before()['artifacts']['analysis'];b=copy.deepcopy(a);b['execution']['seconds']+=99
  self.assertEqual(artifact_hash(a),artifact_hash(b));b['execution']['rows'][0][1]+=1;self.assertNotEqual(artifact_hash(a),artifact_hash(b))
 def test_probe_and_read_only_failure(self):
  c=contract(self.p,'analysis',0);self.assertEqual(probe(compile_sql(c),c)['status'],'passed')
  wrong=compile_sql(c).replace('quantity > 0 AND ','');self.assertEqual(probe(wrong,c)['status'],'failed')
  self.assertEqual(execute('DELETE FROM transactions')['status'],'failed')
 def test_hand_calculated_transaction_contract(self):
  from .execution import python_aggregate
  c=contract(self.p,'analysis',0);rows=probe_rows(c)
  self.assertEqual(python_aggregate(rows,c),[['C',20],['F',11],['B',7],['A',2]])
  self.assertEqual(python_aggregate(rows,dict(c,country='France',customer='known')),[['B',7],['A',2]])
  self.assertEqual(python_aggregate(rows,dict(c,inclusion='signed',metric='value_micro')),[['C',40000000],['F',22000000],['I',18000000],['B',7000000],['A',4000000]])
 def test_budget_cutoff_before_network(self):
  from . import client
  auth=dict(inference_cutoff_utc='2000-01-01T00:00:00+00:00',scheduled_call_ceiling=2,attempt_ceiling=2)
  with patch.object(client,'ART',Path(self.tmp.name)),patch.object(client,'read',return_value=auth),patch.object(client,'http') as network:
   with self.assertRaises(RuntimeError):client.generate('new',[],1,20)
   network.assert_not_called()
 def test_failed_attempts_retained_and_cached(self):
  from . import client
  from .common import write,read
  root=Path(self.tmp.name);auth=dict(inference_cutoff_utc='2099-01-01T00:00:00+00:00',scheduled_call_ceiling=2,attempt_ceiling=2)
  write(root/'authorization.json',auth)
  def network(path,payload):
   if path=='/tokenize':return {'count':10}
   raise TimeoutError('Controlled failure')
  with patch.object(client,'ART',root),patch.object(client,'http',side_effect=network):
   r=client.generate('failure',[],1,20);self.assertEqual(r['status'],'failed');self.assertEqual(len(r['attempts']),2)
   again=client.generate('failure',[],1,20);self.assertEqual(r,again)
   with self.assertRaises(ValueError):client.generate('failure',[],2,20)
  self.assertEqual(len((root/'attempts.jsonl').read_text().splitlines()),2)
 def test_identical_replay(self):
  a=run(self.p,0,generate_fn=deterministic_call);b=run(self.p,0,generate_fn=deterministic_call);self.assertEqual(stable(a),stable(b))
if __name__=='__main__':unittest.main()
