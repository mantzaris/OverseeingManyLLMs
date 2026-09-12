import json
from copy import deepcopy
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from research.oversight_workflow.common import ART, read, write, digest
from research.oversight_workflow.pilot.materials import PILOT
from research.oversight_workflow.pilot.adapter import saved_output
from research.oversight_workflow.data import task
from research.oversight_workflow.offline import labels
from research.oversight_workflow.matched.materials import HERE, VERSION, build
from research.oversight_workflow.matched.server import MatchedPilot, setup_html, desk_js
from research.oversight_workflow.matched.protocol import MatchedDesk, replay
from research.oversight_workflow.matched.analysis import load_runs, analyze, apply_adjudication, behavior_counts


class MatchedTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.app=MatchedPilot(self.temp.name,'software_fixture');self.addCleanup(self.app.stop)
        self.app.create(dict(code='fixture-case',assignment=0))

    def begin(self,block=1):
        self.app.run['next_block']=block
        self.app.begin(dict(seconds=12));time.sleep(.3)
        return self.app.desk

    def finish(self):
        self.app.finish('early_finish');self.app.form({})
        p=Path(self.temp.name)/'fixture.pilot.json';write(p,self.app.export());return p

    def test_manifest_allocation_and_balanced_assignments(self):
        m=read(HERE/'manifest.json');self.assertEqual(m,build());self.assertEqual(m['review_seconds'],540)
        self.assertFalse(m['admission_controls']);self.assertEqual(len(m['outputs']),36)
        from collections import Counter
        positions=[]
        for assignment in m['assignments']:
            ids=[]
            for pos,b in enumerate(assignment['blocks']):
                p=m['packets'][b['packet']];self.assertEqual(len(p['question_ids']),12)
                ids+=p['context_ids'];positions.append((b['condition'],pos,b['packet']))
            self.assertEqual(len(set(ids)),6)
        self.assertEqual(set(Counter(positions).values()),{2})
        old=read(PILOT/'manifest.json')
        self.assertEqual([p['question_ids'] for p in m['packets']],[p['question_ids'] for p in old['packets']])

    def test_equal_real_configuration_all_three_conditions(self):
        settings=[]
        for block in (1,2,3):
            self.app.run['next_block']=block;self.app.begin({})
            s=self.app.current;settings.append((s['duration_seconds'],s['start_offsets'],len(s['question_ids']),len(self.app.desk.state['tasks'])))
            self.app.finish('early_finish');self.app.form({})
        self.assertEqual(len(set(str(s) for s in settings)),1);self.assertEqual(settings[0][0],540)
        self.assertEqual(settings[0][2:],(12,12))

    def test_manual_never_requests_model_output(self):
        with patch('research.oversight_workflow.matched.server.saved_output',side_effect=AssertionError('Draft loaded in M')):
            d=self.begin(3);s=self.app.export()['active_session']
        self.assertTrue(all(v is None for v in s['raw_proposals'].values()))
        self.assertTrue(all(r['versions']['1']['origin']=='source_only_placeholder' for r in d.state['requests'].values()))
        self.assertTrue(all(not r['versions']['1']['output']['answer'] for r in d.state['requests'].values()))

    def test_admission_disabled_and_q_grouping_refused_with_replay(self):
        d=self.begin(1)
        for action in ('pause','resume','session'):
            self.assertFalse(d.command(action,action,{'ids':[]})['ok'])
        self.assertFalse(d.state['paused'])
        self.assertEqual(replay(d.events,'queue').logical(),d.logical())
        g=MatchedDesk('sessions');self.assertFalse(g.command('p','pause')['ok'])
        self.assertEqual(replay(g.events,'sessions').logical(),g.logical())

    def test_stable_review_scope_and_versioned_release(self):
        d=self.begin(2);rid=d.next_request();d.command('select','select',{'id':rid});before=deepcopy(d.state['active'])
        time.sleep(.35);self.assertEqual(d.state['active'],before)
        self.assertTrue(d.command('note','note',{'text':'Check period'})['ok'])
        self.assertTrue(d.command('defer','decide',dict(id=rid,version=1,decision='defer',note='Unfinished check'))['ok'])
        self.assertTrue(d.command('back','select',{'id':rid})['ok'])
        self.assertEqual(d.state['active']['notes'],'Unfinished check')
        self.assertTrue(d.command('a','decide',dict(id=rid,version=1,decision='approve'))['ok']);self.assertEqual(d.counts()['released'],0)
        output=d.state['requests'][rid]['versions']['1']['output']
        d.command('rev','revise',dict(id=rid,output=output,origin='synthetic_version_fixture'))
        self.assertFalse(d.command('stale','release',dict(id=rid,version=1))['ok'])
        self.assertFalse(d.command('new','release',dict(id=rid,version=2))['ok'])
        self.assertEqual(replay(d.events,'sessions').logical(),d.logical())

    def test_source_group_requires_actual_source_and_separate_decisions(self):
        d=self.begin(2);time.sleep(.7)
        ids=list(d.state['requests']);rid=ids[0];d.command('s','select',{'id':rid})
        other=next(i for i in ids if d.state['tasks'][i]['source']['id']!=d.state['tasks'][rid]['source']['id'])
        self.assertFalse(d.command('badgroup','session',{'ids':[rid,other]})['ok'])
        same=[i for i in ids if d.state['tasks'][i]['source']['id']==d.state['tasks'][rid]['source']['id']]
        self.assertTrue(d.command('group','session',{'ids':same})['ok'])
        d.command('approve','decide',dict(id=rid,version=1,decision='approve'))
        self.assertEqual(len(d.state['decisions']),1);self.assertEqual(len(d.state['releases']),0)

    def test_no_annotations_in_online_context_and_no_inference_path(self):
        for c in self.app.contexts:
            self.assertTrue(all('answer' not in q and 'derivation' not in q for q in c['questions']))
        text=(HERE/'server.py').read_text()
        for forbidden in ('offline import','scoring import','LiveDriver','generate('):self.assertNotIn(forbidden,text)
        self.assertNotIn('pause new task starts',setup_html());self.assertIn('pause.hidden=true',desk_js())

    def test_kind_version_timing_and_assignment_isolation(self):
        self.begin();p=self.finish();runs,n=load_runs([p,p],'software_fixture');self.assertEqual(n,1)
        self.assertRaises(ValueError,load_runs,[p],'participant')
        for field,value in [('pilot_version','formative-v1'),('manifest_sha256','wrong')]:
            r=read(p);r[field]=value;bad=Path(self.temp.name)/field;write(bad,r)
            self.assertRaises(ValueError,load_runs,[bad],'software_fixture')
        for field,value in [('packet',2),('duration_seconds',11),('admission_controls',True)]:
            r=read(p);r['sessions'][0][field]=value;bad=Path(self.temp.name)/field;write(bad,r)
            self.assertRaises(ValueError,load_runs,[bad],'software_fixture')

    def test_authorization_version_and_practice_duration(self):
        self.assertRaises(ValueError,MatchedPilot,self.temp.name,'participant')
        old=dict(collection_authorized=True,institutional_determination='fixture',consent_version='fixture',investigator='fixture',record_reference='fixture')
        self.assertRaises(ValueError,MatchedPilot,self.temp.name,'participant',old)
        p=MatchedPilot(self.temp.name,'investigator_practice');self.addCleanup(p.stop);p.create(dict(code='practice-fixture',assignment=0))
        self.assertRaises(ValueError,p.begin,dict(seconds=2))

    def test_official_scoring_rejection_and_adjudication_separate(self):
        d=self.begin(1);rid=d.next_request();t=d.state['tasks'][rid];gold=labels()[t['source']['id']][t['question_id']]
        d.command('s','select',{'id':rid});d.command('a','decide',dict(id=rid,version=1,decision='correct',output=dict(answer=gold['answer'] if isinstance(gold['answer'],list) else [gold['answer']],scale=gold['scale'])))
        self.assertEqual(d.counts()['released'],0)
        d.command('r','release',dict(id=rid,version=2));time.sleep(.3)
        other=d.next_request();d.command('s2','select',{'id':other});d.command('reject','decide',dict(id=other,version=1,decision='reject'))
        p=self.finish();out=Path(self.temp.name)/'analysis';result=analyze([p],out,'software_fixture')
        import csv
        with (out/'sessions.csv').open() as f: row=next(csv.DictReader(f))
        self.assertEqual(int(row['offered']),12)
        self.assertEqual(int(row['joint_correct']),1);self.assertEqual(int(row['unfinished']),11);self.assertEqual(int(row['blocked']),1)
        self.assertEqual(float(row['correct_release_proportion']),1/12)
        self.assertFalse(list(out.glob('participant_*.png')));self.assertFalse(result['participant_results_populated'])
        before=(out/'answers_official.csv').read_bytes();blind=read(out/'adjudication_blinded.json')['cases'][0]
        f=Path(self.temp.name)/'judgment.csv';f.write_text('case_id,verdict,reason,rater_code\n'+blind['case_id']+',acceptable,unit fixture only,test-rater\n')
        apply_adjudication(out,f);self.assertEqual(before,(out/'answers_official.csv').read_bytes())

    def test_paired_outcome_denominators_missingness_and_withdrawal(self):
        import csv
        # Controlled software fixture: one reference-correct released answer in G;
        # zero releases in Q/M. This tests subtraction, not participant performance.
        for block in (1,2,3):
            d=self.begin(block)
            if block==2:
                rid=d.next_request();t=d.state['tasks'][rid]
                g=labels()[t['source']['id']][t['question_id']]
                d.command('select-G','select',{'id':rid})
                d.command('correct-G','decide',dict(id=rid,version=1,decision='correct',output=dict(answer=g['answer'] if isinstance(g['answer'],list) else [g['answer']],scale=g['scale'])))
                d.command('release-G','release',dict(id=rid,version=2))
            p=self.finish()
        out=Path(self.temp.name)/'paired';result=analyze([p],out,'software_fixture')
        self.assertEqual(result['contrasts']['G_minus_Q']['correct_release_proportion']['mean'],1/12)
        self.assertEqual(result['contrasts']['Q_minus_M']['correct_release_proportion']['mean'],0)
        self.assertEqual(result['contrasts']['G_minus_M']['correct_release_proportion']['n'],1)
        self.assertIsNone(result['contrasts']['G_minus_Q']['correct_release_proportion']['descriptive_bootstrap95'])
        record=read(p);record['withdrawn']=True;write(p,record)
        result=analyze([p],out,'software_fixture')
        self.assertEqual(result['contrasts']['G_minus_Q']['correct_release_proportion']['n'],0)
        self.assertTrue((out/'paired_descriptions.csv').exists())
        record['sessions']=[s for s in record['sessions'] if s['condition']!='G'];record['withdrawn']=False;write(p,record)
        result=analyze([p],out,'software_fixture')
        self.assertEqual(result['contrasts']['G_minus_Q']['correct_release_proportion']['n'],0)
        self.assertIn(2,result['missing'][0]['missing_completed_blocks'])

    def test_cutoff_unfinished_and_partial_exports_retained(self):
        d=self.begin();rid=d.next_request();d.command('s','select',{'id':rid})
        self.app.current['duration_seconds']=.2;self.app.ensure_cutoff()
        self.assertFalse(d.command('late','decide',dict(id=rid,version=1,decision='approve'))['ok'])
        self.assertEqual(d.counts()['offered'],12);self.assertEqual(d.counts()['released'],0)
        # Timing tampering is intentionally not a valid export; protocol still retains the late action.
        self.assertTrue(any(e['event_id']=='late' for e in self.app.export()['sessions'][0]['events']))

if __name__=='__main__':unittest.main()
