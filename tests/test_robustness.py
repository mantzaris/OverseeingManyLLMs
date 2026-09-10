"""Stipulated mechanics fixtures for Stage 6, with no inference."""
import copy
from datetime import datetime,timedelta,timezone
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from overseeing.retail.robustness import ReviewRequest,choose,review_ticks,simulate,without_timing
from overseeing.retail.robustness_analysis import bundle_means,paired_summary
from overseeing.retail.robustness_execution import RobustnessLedger
from overseeing.retail.risk import RetailRisk
from overseeing.retail.upstream import account_database,load_database,state_hash


class RobustnessSemantics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=load_database()
        cls.case=next(c for c in json.loads(Path('artifacts/stage5_practical/cases.json').read_text())['cases'] if c['family']=='cancel')

    def fixture(self,wrong=True,staged=True):
        c=self.case;db=account_database(self.data,c['user_id']);proposal=copy.deepcopy(c['target_action'])
        if wrong:proposal['arguments']['reason']='ordered by mistake' if proposal['arguments']['reason']=='no longer needed' else 'no longer needed'
        p=dict(case_id=c['case_id'],proposal=proposal if staged else None,initial_error=wrong if staged else False,
            initial_task_success=staged and not wrong,features=dict(family='cancel',uncertain=False),automatic_rejections=0)
        b=dict(bundle_id='fixture',replicate=0,service_failure_cost=4,slots=[dict(case_id=c['case_id'],agent_id=0,arrival=0,cutoff=2,wrong_transaction_cost=8)])
        return b,[p],{c['case_id']:c},{c['case_id']:db},RetailRisk((('cancel:0',.5),),.5,'fixture')

    def test_block_prevents_processing_without_completing_or_mutating(self):
        args=self.fixture();r=simulate(*args,'fcfs',2,'approve_block')
        self.assertEqual((r['operational_loss'],r['blocked_unresolved'],r['task_completed'],r['corrections'],r['wrong_transactions']),(4,1,0,0,0))
        block=next(e for e in r['events'] if e['event']=='transaction_blocked')
        self.assertEqual(block['tick'],2);self.assertEqual(block['state_hash'],state_hash(args[3][self.case['case_id']]))
        self.assertFalse(any(e['event']=='transaction_committed' for e in r['events']))

    def test_approve_preserves_original_arguments_and_late_cannot_block(self):
        args=self.fixture(wrong=False);r=simulate(*args,'fcfs',2,'approve_block')
        e=next(e for e in r['events'] if e['event']=='transaction_committed')
        self.assertEqual(e['action'],args[1][0]['proposal']);self.assertEqual(r['task_completed'],1)
        late=simulate(*self.fixture(),'fcfs',3,'approve_block')
        self.assertEqual((late['operational_loss'],late['blocked_unresolved'],late['completed_reviews']),(12,0,0))

    def test_preparation_failure_outside_scope_and_no_review_invariant(self):
        args=self.fixture(staged=False)
        for variant in ('reference','approve_block','complexity_time'):
            result=simulate(*args,'search',1,variant)
            self.assertEqual((result['operational_loss'],result['completed_reviews'],result['unstaged_failures']),(4,0,1))
        args=self.fixture()
        for variant in ('reference','approve_block','complexity_time'):
            self.assertEqual(simulate(*args,'no_review',1,variant)['operational_loss'],12)

    def test_restricted_benefit_can_change_ranking_not_uniform_rescaling(self):
        reference=[ReviewRequest('a',0,0,4,2,.5,4,4),ReviewRequest('b',1,0,4,2,.3,8,4)]
        restricted=[ReviewRequest('a',0,0,4,2,.5,4,0),ReviewRequest('b',1,0,4,2,.3,8,0)]
        self.assertEqual(choose('greedy',reference,0)[0],'a');self.assertEqual(choose('greedy',restricted,0)[0],'b')
        self.assertEqual(restricted[0].benefit(4),2);self.assertEqual(restricted[0].benefit(5),0)

    def test_variable_duration_and_visible_queue_only(self):
        p={'tool':'return_delivered_order_items','arguments':{'item_ids':['one','two']}}
        self.assertEqual(review_ticks(p,2,'complexity_time'),3);self.assertEqual(review_ticks(p,2,'approve_block'),2)
        q=[ReviewRequest('long',0,0,2,3,.8,12,4),ReviewRequest('short',1,0,4,2,.5,4,4),ReviewRequest('future',2,1,4,1,1,12,4)]
        choice,record=choose('search',q,0)
        self.assertEqual(choice,'short');self.assertEqual(record['eligible'],['short'])
        with self.assertRaises(ValueError):choose('search',[{'hidden_target':'x'}],0)

    def test_planning_arithmetic_and_search_effort(self):
        q=[ReviewRequest('urgent',0,0,2,2,.5,8,0),ReviewRequest('large',1,0,5,2,.5,12,0),ReviewRequest('medium',2,0,4,2,.5,4,0)]
        self.assertEqual(choose('greedy',q,0)[0],'large');self.assertEqual(choose('search',q,0)[0],'urgent')
        self.assertEqual(choose('edf',q,0)[0],'urgent');self.assertEqual(choose('search',q,0)[1]['ordered_subsets_evaluated'],16)

    def test_bundle_aggregation_prevents_replication_pseudoreplication(self):
        rows=[dict(bundle_id=b,variant='approve_block',review_duration=2,policy='search',replicate=i,operational_loss=v)
              for b,values in [('a',[0,30,0]),('b',[3,3,3])] for i,v in enumerate(values)]
        means=bundle_means(rows,'operational_loss');self.assertEqual(len(means),2)
        self.assertEqual(sorted(means.values()),[3,10])
        with self.assertRaises(ValueError):bundle_means(rows[:-1],'operational_loss')
        r=paired_summary([10,3],[[0,0],[1,1],[0,1]])
        self.assertEqual(r['mean_difference'],6.5);self.assertEqual(r['losses'],2)
        completion=paired_summary([10,3],[[0,0],[1,1],[0,1]],lower_is_better=False)
        self.assertEqual(completion['wins'],2);self.assertEqual(completion['losses'],0)
        self.assertEqual(completion['mean_difference'],r['mean_difference'])

    def test_source_exclusion_and_frozen_estimator(self):
        record=json.loads(Path('artifacts/stage6_robustness/cases.json').read_text());cases=record['cases']
        self.assertEqual(len(cases),24);self.assertEqual(len({c['user_id'] for c in cases}),24)
        self.assertFalse({c['user_id'] for c in cases}&set(record['excluded_stage5_accounts']))
        import importlib.util
        spec=importlib.util.spec_from_file_location('stage6_sources','scripts/prepare_robustness_cases.py')
        source_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(source_module)
        candidate=source_module.candidate
        import ast
        from overseeing.retail.upstream import RETAIL
        for split in ('train','dev','test'):
            tree=ast.parse((RETAIL/('tasks_'+split+'.py')).read_text());nodes=next(n.value.elts for n in tree.body if isinstance(n,ast.Assign))
            for c in cases:
                if c['source_split']==split:self.assertEqual(candidate(split,c['source_index'],nodes[c['source_index']],self.data),c)
        estimator=json.loads(Path('artifacts/stage5_practical/estimator.json').read_text())
        self.assertEqual(RetailRisk.load(estimator).estimator_hash,'5734f6babfbd33655a76595f001251bd5914d94dde0c0e3401af3fc4a762a581')

    def test_stage6_authorization_and_retry_limit_preserve_stage5(self):
        now=datetime.now(timezone.utc);start=now-timedelta(minutes=1)
        auth=dict(name='stage6_robustness',authorization='explicit_user_request',attempt_limit=6000,maximum_retries_per_call=1,
            started_utc=start.isoformat(),deadline_utc=(start+timedelta(hours=6)).isoformat(),inference_cutoff_utc=(start+timedelta(hours=4,minutes=30)).isoformat())
        with TemporaryDirectory() as folder:
            path=Path(folder)/'authorization.json';path.write_text(json.dumps(auth));ledger=RobustnessLedger(folder,'fixture')
            try:
                call=ledger.reserve_call({'fixture':True});ledger.reserve_attempt(call,0);ledger.reserve_attempt(call,1)
                with self.assertRaises(RuntimeError):ledger.reserve_attempt(call,1)
                ledger.attempts=6000
                with self.assertRaises(RuntimeError):ledger.reserve_call({'fixture':True})
            finally:ledger.close()
            auth['name']='stage5_practical';path.write_text(json.dumps(auth))
            with self.assertRaises(RuntimeError):RobustnessLedger(folder,'fixture')

if __name__=='__main__':unittest.main()
