import copy,tempfile,unittest
from pathlib import Path
from .tests import C,G,P,initial,responder
from .answers import prepare
from .controller import run
from .feedback import Inspector
from .replay import RecordedInspector
from .common import stable
from .scoring import score
from .prototype.server import Desk
class AdditionalBoundaries(unittest.TestCase):
 def test_recorded_feedback_replay_needs_no_sibling_gold(self):
  a=run(C,initial(),P,Inspector(G,2),responder,50,'adaptive',2)
  b=run(C,initial(),P,RecordedInspector(a['events'],2),responder,50,'adaptive',2)
  self.assertEqual(stable(a),stable(b))
 def test_scale_sensitive_amount_and_ratio(self):
  g=dict(answer=10,scale='million',answer_type='arithmetic',derivation='')
  self.assertEqual(score(prepare(dict(answer=['10'],scale='million'),C),g)['em'],1)
  self.assertEqual(score(prepare(dict(answer=['10'],scale='percent'),C),g)['em'],0)
  g.update(answer=100,scale='percent')
  self.assertEqual(score(prepare(dict(answer=['=(20-10)/10*100'],scale='percent'),C),g)['em'],1)
 def test_frozen_initialization_unchanged(self):
  p=copy.deepcopy(P);run(C,initial(),p,Inspector(G,2),responder,50,'adaptive',2);self.assertEqual(p,P)
 def test_zero_budget_no_feedback(self):
  def forbidden(q):raise AssertionError('Unexpected feedback')
  ins=Inspector(G,0);ins.inspect=forbidden
  r=run(C,initial(),P,ins,responder,50,budget=0);self.assertEqual(r['answers'],initial());self.assertEqual(r['calls'],[])
 def test_ui_hides_future_disclosures(self):
  r=run(C,initial(),P,Inspector(G,2),responder,50,'adaptive',2)
  with tempfile.TemporaryDirectory() as p:
   d=Desk(Path(p)/'log');d.sessions['x']=dict(context=C,run=r,step=0);s=d.state('x')
   self.assertIsNone(s['last']);self.assertNotIn('disclosure',str(s['next']));s=d.inspect('x');self.assertEqual(s['remaining'],1);self.assertEqual(s['last']['inspected'],r['events'][0]['inspected'])
if __name__=='__main__':unittest.main()
