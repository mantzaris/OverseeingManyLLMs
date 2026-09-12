import tempfile,time,unittest,json
from pathlib import Path
from copy import deepcopy
from research.oversight_workflow.common import read,write,digest,ART
from research.oversight_workflow.protocol import replay
from research.oversight_workflow.pilot.server import Pilot,questionnaire
from research.oversight_workflow.pilot.analysis import load_runs,analyze,apply_adjudication
from research.oversight_workflow.pilot.materials import PILOT
from research.oversight_workflow.pilot.adapter import normalize

class PilotTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.app=Pilot(self.tmp.name,'software_fixture');self.addCleanup(self.app.stop);self.app.create(dict(code='fixture-test',assignment=0))
 def begin(self):
  self.app.begin(dict(seconds=5));time.sleep(.32);return self.app.desk
 def end(self):
  self.app.finish('early_finish');self.app.form({});path=Path(self.tmp.name)/'export.pilot.json';write(path,self.app.export());return path
 def test_assignment_balance_and_disjointness(self):
  m=read(PILOT/'manifest.json');from collections import Counter
  training=read(PILOT.parent/'study/training.json')['context']['id'];seen=[]
  from research.oversight_workflow.pilot.materials import shared_definition
  source_ids={i for p in m['packets'] for i in p['context_ids']};definitions=[shared_definition(q) for c in self.app.contexts if c['id'] in source_ids for q in c['questions'] if shared_definition(q)]
  self.assertEqual(len(definitions),len(set(definitions)))
  for a in m['assignments']:
   self.assertEqual({b['condition'] for b in a['blocks']},{'B','C','S'});self.assertEqual(len({b['packet'] for b in a['blocks']}),3)
   sources=[i for b in a['blocks'] for i in m['packets'][b['packet']]['context_ids']];self.assertEqual(len(set(sources)),6);self.assertNotIn(training,sources)
   seen.extend((b['condition'],pos,b['packet']) for pos,b in enumerate(a['blocks']))
  self.assertEqual(len(set(Counter(seen).values())),1)
  for rule in (lambda b,pos:(b['condition'],b['packet']),lambda b,pos:(pos,b['packet'])):
   counts=Counter(rule(b,pos) for i in m['example_six_run_assignment_ids'] for pos,b in enumerate(m['assignments'][i]['blocks']))
   self.assertEqual(set(counts.values()),{2});self.assertEqual(len(counts),9)
 def test_parser_projection_no_semantic_rescue(self):
  c=read(ART/'frozen/manifest.json')['contexts'][0]
  out,changes=normalize(dict(answer=[['a','b'],['c']],scale='',evidence='T0C1',derivation=''),c)
  self.assertEqual(out['answer'],['a','b','c']);self.assertTrue(changes)
  out,_=normalize(dict(answer=[],derivation='The answer might be 42'),c);self.assertEqual(out['answer'],[])
 def test_approval_release_and_replay(self):
  d=self.begin();rid=d.next_request();self.assertIsNotNone(rid)
  self.assertTrue(d.command('s','select',{'id':rid})['ok']);self.assertTrue(d.command('a','decide',dict(id=rid,version=1,decision='approve'))['ok']);self.assertEqual(d.counts()['released'],0)
  self.assertTrue(d.command('r','release',dict(id=rid,version=1))['ok']);self.assertEqual(d.counts()['released'],1)
  p=self.end();runs,n=load_runs([p],'software_fixture');self.assertEqual(n,0)
  s=runs[0]['sessions'][0];self.assertEqual(replay(s['events'],s['desk_condition']).logical(),s['state'])
 def test_kind_mixing_and_duplicate_exports(self):
  self.begin();p=self.end();self.assertRaises(ValueError,load_runs,[p],'participant')
  _,n=load_runs([p,p],'software_fixture');self.assertEqual(n,1)
  r=read(p);r['withdrawn']=True;p2=Path(self.tmp.name)/'different.json';write(p2,r);self.assertRaises(ValueError,load_runs,[p,p2],'software_fixture')
 def test_incorrect_packet_rejected(self):
  self.begin();p=self.end();r=read(p);r['sessions'][0]['packet']=1;write(p,r);self.assertRaises(ValueError,load_runs,[p],'software_fixture')
 def test_cutoff_and_late_action_retained(self):
  d=self.begin();rid=d.next_request();d.command('s','select',{'id':rid});self.app.current['duration_seconds']=.2;self.app.ensure_cutoff()
  self.assertFalse(d.command('late','decide',dict(id=rid,version=1,decision='approve'))['ok']);r=self.app.export()
  self.assertTrue(any(e['event_id']=='late' for e in r['sessions'][0]['events']));self.assertEqual(d.counts()['released'],0)
 def test_withdrawal_and_missing_sessions_not_discarded(self):
  self.begin();self.app.withdraw();p=Path(self.tmp.name)/'run.pilot.json';write(p,self.app.export());s=analyze([p],Path(self.tmp.name)/'analysis','software_fixture')
  self.assertTrue(s['missing'][0]['withdrawn']);self.assertEqual(s['missing'][0]['missing_completed_blocks'],[1,2,3]);self.assertEqual(s['paired_runs'],0)
 def test_active_export_preserved_as_incomplete(self):
  self.begin();p=Path(self.tmp.name)/'run.pilot.json';write(p,self.app.export());runs,_=load_runs([p],'software_fixture');self.assertIn('active_session',runs[0])
 def test_scored_outcomes_and_blinded_adjudication(self):
  self.app.run['next_block']=1;d=self.begin();rid=d.next_request();d.command('s','select',{'id':rid});d.command('a','decide',dict(id=rid,version=1,decision='correct',output={'answer':['0'],'scale':'','evidence':[]}));d.command('r','release',dict(id=rid,version=2));p=self.end()
  output=Path(self.tmp.name)/'analysis';summary=analyze([p],output,'software_fixture');self.assertFalse(summary['participant_results_populated'])
  import csv
  with (output/'sessions.csv').open() as f:row=next(csv.DictReader(f))
  self.assertEqual(row['offered'],'12');self.assertEqual(row['released'],'1');self.assertEqual(row['unfinished'],'11')
  blinded=read(output/'adjudication_blinded.json')['cases'][0];self.assertNotIn('condition',blinded);self.assertNotIn('participant_code',blinded);self.assertNotIn('official_em',blinded)
  before=(output/'answers_official.csv').read_bytes();f=Path(self.tmp.name)/'rating.csv';f.write_text('case_id,verdict,reason,rater_code\n'+blinded['case_id']+',uncertain,Software fixture only,test\n')
  apply_adjudication(output,f);self.assertEqual(before,(output/'answers_official.csv').read_bytes())
 def test_authorization_and_questionnaire_boundary(self):
  self.assertRaises(ValueError,Pilot,self.tmp.name,'participant')
  self.assertEqual(questionnaire({})['tlx'],[None]*6);self.assertFalse(questionnaire({})['complete']);self.assertRaises(ValueError,questionnaire,dict(tlx=[120]*6))
 def test_no_runtime_annotations(self):
  # The new runtime modules and public manifest never import offline scorers.
  for name in ('server.py','adapter.py','materials.py'):
   text=(PILOT/name).read_text();self.assertNotIn('from research.oversight_workflow.offline',text);self.assertNotIn('scoring import',text)
  for c in self.app.contexts:
   for q in c['questions']:self.assertNotIn('answer',q)
 def test_source_only_does_not_load_proposal(self):
  from unittest.mock import patch
  self.app.run['next_block']=3
  with patch('research.oversight_workflow.pilot.server.saved_output',side_effect=AssertionError('Proposal requested')):
   self.begin();r=self.app.export();self.assertTrue(all(x is None for x in r['active_session']['raw_proposals'].values()));self.assertTrue(all(not v['output']['answer'] for q in r['active_session']['state']['requests'].values() for v in q['versions'].values()))
 def test_no_duration_override_in_practice(self):
  p=Pilot(self.tmp.name,'investigator_practice');self.addCleanup(p.stop);p.create(dict(code='practice',assignment=0));self.assertRaises(ValueError,p.begin,dict(seconds=1))
if __name__=='__main__':unittest.main()
