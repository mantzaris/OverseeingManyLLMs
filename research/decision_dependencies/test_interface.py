"""Online override semantics, separate from the frozen source-output evaluation."""
import json
import tempfile
import unittest
from pathlib import Path
from .prototype.server import Desk

class InterfaceChecks(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.desk=Desk(Path(self.temp.name)/'demo.jsonl')
    def tearDown(self):self.temp.cleanup()
    def answer(self,id='dining_shortlist',value='christmas',scope='project'):
        return self.desk.act(dict(action='answer',id=id,value=value,scope=scope,key='restaurant.food'))
    def test_one_answer_unblocks_two_roles_without_answer_labels(self):
        state=self.answer();responses={r['id']:r['answer'] for r in state['requests']}
        self.assertEqual(responses['dining_shortlist']['value'],'christmas')
        self.assertEqual(responses['itinerary_brief']['value'],'christmas')
        self.assertEqual(state['confirmations'],1)
        serialized=json.dumps(state)
        for field in ('annotation_states','evaluation_only','expected_output','changed_fields'):self.assertNotIn(field,serialized)
    def test_request_only_answer_does_not_propagate(self):
        state=self.answer(scope='request');responses={r['id']:r['answer'] for r in state['requests']}
        self.assertEqual(responses['dining_shortlist']['value'],'christmas')
        self.assertEqual(responses['itinerary_brief']['status'],'needs_user')
    def test_rejected_action_is_atomic(self):
        before=self.desk.state()
        with self.assertRaises(ValueError):
            self.desk.act(dict(action='answer',id='accommodation_brief',value='expensive',key='hotel.pricerange',scope='unsupported'))
        self.assertEqual(self.desk.state(),before)
    def test_human_can_correct_unknown_request_scope(self):
        state=self.desk.act(dict(action='answer',id='accommodation_brief',value='hotel',key='hotel.type',scope='project'))
        request=next(r for r in state['requests'] if r['id']=='accommodation_brief')
        self.assertEqual(request['key'],'hotel.type');self.assertEqual(request['answer']['value'],'hotel')
    def test_changed_source_blocks_old_work(self):
        self.answer();self.desk.act(dict(action='prepare'))
        self.desk.act(dict(action='source_update'))
        state=self.desk.act(dict(action='release',id='dining_shortlist'))
        self.assertEqual(state['tasks']['dining_shortlist']['status'],'needs_revalidation')
        self.desk.act(dict(action='prepare'));state=self.desk.act(dict(action='release',id='dining_shortlist'))
        self.assertEqual(state['tasks']['dining_shortlist']['status'],'released')
        self.assertEqual(state['tasks']['dining_shortlist']['answers']['restaurant.food']['value'],'indian')
    def test_live_project_override_invalidates_prepared_work(self):
        self.answer();self.desk.act(dict(action='prepare'));self.answer(value='italian')
        state=self.desk.act(dict(action='release',id='dining_shortlist'))
        self.assertEqual(state['tasks']['dining_shortlist']['status'],'needs_revalidation')
    def test_live_request_override_requires_repreparation(self):
        self.answer();self.desk.act(dict(action='prepare'));self.answer(value='italian',scope='request')
        with self.assertRaises(ValueError):self.desk.act(dict(action='release',id='dining_shortlist'))
        self.desk.act(dict(action='prepare'));state=self.desk.act(dict(action='release',id='dining_shortlist'))
        self.assertEqual(state['tasks']['dining_shortlist']['answers']['restaurant.food']['value'],'italian')
    def test_deferral_and_interaction_provenance(self):
        self.desk.act(dict(action='shown',ids=['dining_shortlist']))
        self.desk.act(dict(action='defer',id='dining_shortlist'))
        self.assertTrue(next(r for r in self.desk.state()['requests'] if r['id']=='dining_shortlist')['deferred'])
        self.desk.act(dict(action='resume',id='dining_shortlist'));self.answer()
        rows=[json.loads(x) for x in self.desk.log.read_text().splitlines()]
        self.assertTrue(all(x['record_type']=='development_demonstration_not_participant_data' for x in rows))
        self.assertGreaterEqual(rows[-1]['response_seconds_since_shown'],0)

if __name__=='__main__':unittest.main()
