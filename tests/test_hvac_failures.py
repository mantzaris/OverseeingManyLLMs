import unittest
from overseeing.hvac import simulate,without_timing

class RetainedFailureAccounting(unittest.TestCase):
    def setUp(self):
        self.cases=[dict(case_id='run00_w'+str(i),run_id='run00',source_label='normal') for i in range(3)]
        self.records={c['case_id']:dict(proposal='',review='{"diagnosis":"normal"}') for c in self.cases}
        self.estimator=dict(bins={'invalid':dict(prediction=dict(risk=.8,gain=.5))})
    def test_preparation_failure_is_in_denominator(self):
        r=simulate(self.cases,self.records,self.estimator,'no_review',2,1,'model')
        self.assertEqual(r['unresolved'],3);self.assertEqual(sum(x['preparation_failure'] for x in r['jobs']),3)
        self.assertEqual(r['loss'],24)
    def test_review_cannot_apply_after_cutoff(self):
        r=simulate(self.cases,self.records,self.estimator,'search',7,2,'ideal')
        self.assertEqual(r['completed_reviews'],0);self.assertEqual(r['correct'],0)
        self.assertTrue(all(e['tick'] in (2,4,6) for e in r['events'] if e['event']=='cutoff'))
    def test_multiple_reviewers_and_replay(self):
        r=simulate(self.cases,self.records,self.estimator,'search',1,2,'model')
        self.assertEqual(r['correct'],3);self.assertEqual(r['corrections'],3)
        events=r['events']
        for tick in range(7):
            active=sum(e['tick']<=tick<e['finish'] for e in events if e['event']=='review_started')
            self.assertLessEqual(active,2)
        self.assertEqual(without_timing(r),without_timing(simulate(self.cases,self.records,self.estimator,'search',1,2,'model')))
