"""Focused risks for the refined public interface and recorded desk."""
import copy,tempfile,unittest
from pathlib import Path
from .common import ART,read,digest,stable
from .tests import C,Q1,Q2,q
from .backend import load
from .representation_v2 import parse,contract,messages
from .prototype.server import Desk
from .replay import RecordedInspector

class RefinedBoundaries(unittest.TestCase):
 def test_binding_read_from_source_and_period_not_self_report(self):
  a=parse({'answer':['245'],'rep':{'op':'difference','refs':['T1C1','T1C2'],'expression':'x0-x1','scale':'million','periods':['2017','2018'],'metric':'invented'}},C)
  self.assertEqual(a['rep']['periods'],['2018','2019']);self.assertNotEqual(a['rep']['metric'],'invented');self.assertIn('period_binding',contract(C,Q2,a['rep']))
 def test_execution_and_scale_not_semantic_certificate(self):
  a=parse({'rep':{'op':'lookup','refs':['T1C1'],'expression':'x0','scale':'percent'}},C)
  self.assertTrue(a['representation_valid']);self.assertIn('unsupported_percent_scale',contract(C,q('q1','What are research expenses in 2019?'),a['rep']))
 def test_non_numeric_failure_cannot_pass(self):
  a=parse({'rep':{'op':'lookup','refs':['T1C0'],'expression':'x0','scale':''}},C)
  self.assertFalse(a['representation_valid']);self.assertTrue(contract(C,Q1,a['rep']))
 def test_no_reuse_prompts_cannot_receive_feedback(self):
  sentinel={'answer':'HIDDEN_SIBLING_88771','scale':'million','derivation':'PRIVATE_SENTINEL'}
  for mode in ['extract','verify','reattempt']:
   self.assertEqual(messages(C,Q1,mode=mode),messages(C,Q1,mode=mode,feedback=sentinel))
 def test_guarded_parser_and_infer_reject_partial_donor(self):
  engine=load('v2_guarded');a={'rep':{'refs':['T1C1'],'expression':'x0','op':'lookup','scale':'million'}}
  p=engine.infer(C,Q1,a,a,{'answer':'6577','scale':'million'});self.assertFalse(p['supported'])
 def test_desk_discloses_only_completed_inspections(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=Desk('v2',Path(tmp)/'log.jsonl');s=d.open(5,'patch');self.assertIsNone(s['last']);self.assertEqual(s['remaining'],2);self.assertNotIn('annotations',s)
   s=d.inspect(s['session']);self.assertEqual(s['remaining'],1);self.assertEqual(s['last']['disclosure']['id'],s['last']['inspected']);s=d.inspect(s['session'])
   with self.assertRaises(ValueError):d.inspect(s['session'])
   import json
   rows=[json.loads(x) for x in (Path(tmp)/'log.jsonl').read_text().splitlines()];self.assertEqual(len(rows),3)
   for row in rows:self.assertEqual(digest(row['displayed_state']),row['state_sha256']);self.assertFalse(row['participant'])
 def test_wrong_inspection_cannot_read_another_record(self):
  r=read(ART/'development_v2/c05_patch.json');i=RecordedInspector(r['events'])
  with self.assertRaises(AssertionError):i.inspect({'id':'not-selected'})
 def test_synthetic_semantic_harm_retained(self):
  e=read(ART/'synthetic/coincidental_formula_harm/patch.json');self.assertTrue(e['event']['accepted']);self.assertEqual(float(e['event']['after']['answer'][0]),300);self.assertEqual(e['target'],100)
if __name__=='__main__':unittest.main()
