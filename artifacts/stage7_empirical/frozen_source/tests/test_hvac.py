import copy,json,unittest
from pathlib import Path
from overseeing.hvac import *

class HVACSemantics(unittest.TestCase):
    def test_public_boundary_and_split(self):
        cases=json.loads(Path('artifacts/stage7_empirical/cases.json').read_text());dev={c['run_id'] for c in cases if c['split']=='development'};ev={c['run_id'] for c in cases if c['split']=='evaluation'}
        self.assertFalse(dev&ev);self.assertEqual(len(dev),8);self.assertEqual(len(ev),18)
        for c in cases:
            self.assertEqual(set(c['public']),{'equipment_mode','window_start','window_end','sample_interval_minutes','n_samples','units','statistic_order','readings'})
            self.assertNotIn(c['source_date'],json.dumps(c['public']));self.assertEqual(set(c['public']['readings']),set(FIELDS))
    def test_equality_and_expiry(self):
        r=PublicRequest('a',0,0,2,2,8,.5,.4)
        self.assertEqual(choose('greedy',[r],0)[0],'a');self.assertIsNone(choose('greedy',[r],1)[0])
    def test_signed_gain(self):
        r=PublicRequest('a',0,0,4,2,8,.9,-.1)
        for p in POLICIES:self.assertIsNone(choose(p,[r],0)[0])
    def test_planning_arithmetic(self):
        a=PublicRequest('a',0,0,2,2,4,.5,.5);b=PublicRequest('b',1,0,4,2,8,.5,.5)
        self.assertEqual(choose('greedy',[a,b],0)[0],'b');self.assertEqual(choose('search',[a,b],0)[0],'a')
        self.assertEqual(choose('edf',[a,b],0)[0],'a')
    def test_no_hidden_scheduler_fields(self):
        self.assertRaises(AssertionError,choose,'search',[{'truth':'normal'}],0)
        self.assertRaises(AssertionError,choose,'search',[PublicRequest('a',0,2,4,1,8,.5,.5)],0)
    def test_development_only_and_signed_fit(self):
        cs=[dict(case_id=str(i),split='development',source_label='normal') for i in range(6)]
        rs={str(i):dict(proposal='{"diagnosis":"normal"}',review='{"diagnosis":"heating_valve"}') for i in range(6)}
        e=fit(cs,rs);self.assertLess(e['bins']['normal']['prediction']['gain'],0)
        self.assertTrue(e['bins']['heating_valve']['fallback']);cs[0]['split']='evaluation';self.assertRaises(AssertionError,fit,cs,rs)
    def test_harm_and_pairing(self):
        cs=[dict(case_id='run00_w'+str(i),run_id='run00',source_label='normal') for i in range(3)]
        rs={c['case_id']:dict(proposal='{"diagnosis":"normal"}',review='{"diagnosis":"heating_valve"}') for c in cs}
        e=dict(bins={'normal':dict(prediction=dict(risk=.5,gain=.5))});original=copy.deepcopy(rs)
        r=simulate(cs,rs,e,'search',1,2,'model');self.assertEqual(r['harmful_reviews'],3);self.assertEqual(r['correct'],0);self.assertEqual(rs,original)
        ideal=simulate(cs,rs,e,'search',1,2,'ideal');self.assertEqual(ideal['correct'],3)
        no=simulate(cs,rs,e,'no_review',1,2,'model');self.assertEqual(no['correct'],3)
    def test_failed_review_preserves(self):
        cs=[dict(case_id='run00_w'+str(i),run_id='run00',source_label='normal') for i in range(3)]
        rs={c['case_id']:dict(proposal='{"diagnosis":"normal"}',review='') for c in cs};e=dict(bins={'normal':dict(prediction=dict(risk=.5,gain=.5))})
        r=simulate(cs,rs,e,'search',1,2,'model');self.assertEqual(r['correct'],3)
