"""Focused application semantics; stipulated calls are mechanics fixtures, not inference."""
import copy
from dataclasses import FrozenInstanceError,asdict
import json
from pathlib import Path
import unittest

from overseeing.domain import digest
from overseeing.retail.execution import make_bundles
from overseeing.retail.risk import RetailRisk,RiskFeatures,fit_development
from overseeing.retail.scheduler import TransactionRequest,choose
from overseeing.retail.simulation import simulate
from overseeing.retail.upstream import account_database,invoke,load_database,state_hash
from overseeing.retail.workflow import RetailWorkflow


class RetailSemantics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=json.loads(Path('artifacts/stage5_practical/cases.json').read_text())['cases']
        cls.data=load_database()

    def case(self,family):return next(c for c in self.cases if c['partition']=='development' and c['family']==family)

    def prepared_workflow(self,case):
        initial=account_database(self.data,case['user_id']);workflow=RetailWorkflow(case['customer_message'],initial)
        user=initial['users'][case['user_id']]
        for action in [dict(tool='find_user_id_by_email',arguments={'email':user['email']}),
            dict(tool='get_user_details',arguments={'user_id':case['user_id']}),
            dict(tool='get_order_details',arguments={'order_id':case['order_id']})]:
            workflow.step(dict(action,confidence='high'))
        return initial,workflow

    def test_authentication_and_confirmation_guard(self):
        case=self.case('cancel');initial=account_database(self.data,case['user_id']);w=RetailWorkflow(case['customer_message'],initial)
        self.assertIn('authenticate',w.step(dict(case['target_action'],confidence='high')))
        self.assertIsNone(w.proposal)
        initial,w=self.prepared_workflow(case)
        self.assertIn('confirmation',w.step(dict(case['target_action'],confidence='high')))
        w.step(dict(tool='request_confirmation',arguments=dict(action=case['target_action'],summary='Cancel requested order',all_items_confirmed=True),confidence='high'))
        altered=copy.deepcopy(case['target_action']);altered['arguments']['reason']='ordered by mistake'
        if altered!=case['target_action']:self.assertIn('confirmation',w.step(dict(altered,confidence='high')))
        w.step(dict(case['target_action'],confidence='high'))
        self.assertEqual(state_hash(w.data),state_hash(initial));self.assertIsNotNone(w.proposal)

    def test_upstream_guards_and_target_state_reuse(self):
        import ast,__future__,hashlib
        from overseeing.retail.upstream import PACKAGE
        tree=ast.parse((PACKAGE/'envs/base.py').read_text())
        selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('to_hashable','consistent_hash')]
        code=ast.Module(body=selected,type_ignores=[]);namespace={'sha256':hashlib.sha256}
        exec(compile(code,'upstream-validator','exec',flags=__future__.annotations.compiler_flag),namespace)
        fixture={'a':[1,2.0,{'b':'value'}],'c':{'x':False}}
        self.assertEqual(state_hash(fixture),namespace['consistent_hash'](namespace['to_hashable'](fixture)))
        for case in self.cases:
            initial=account_database(self.data,case['user_id']);target=copy.deepcopy(initial)
            self.assertFalse(invoke(target,case['target_action']).startswith('Error:'))
            self.assertEqual(state_hash(target),case['target_state_hash'])
        case=self.case('cancel');db=account_database(self.data,case['user_id']);db['orders'][case['order_id']]['status']='processed'
        before=state_hash(db);self.assertTrue(invoke(db,case['target_action']).startswith('Error:'));self.assertEqual(before,state_hash(db))

    def test_split_and_public_assignment_pairing(self):
        self.assertEqual(len({c['source_case_group'] for c in self.cases}),120)
        bundles=make_bundles(self.cases,'evaluation',[0,1,2],32)
        for index in range(32):
            self.assertEqual(bundles[index*3]['slots'],bundles[index*3+1]['slots'])
        self.assertEqual(len({s['case_id'] for b in bundles for s in b['slots']}),96)
        for case in self.cases:
            workflow=RetailWorkflow(case['customer_message'],{})
            self.assertEqual(workflow.public_family,case['family'])

    def test_valid_wrong_transaction_is_not_filtered_by_hidden_target(self):
        case=self.case('cancel');initial,w=self.prepared_workflow(case)
        wrong=copy.deepcopy(case['target_action'])
        wrong['arguments']['reason']='ordered by mistake' if wrong['arguments']['reason']=='no longer needed' else 'no longer needed'
        w.step(dict(tool='request_confirmation',arguments=dict(action=wrong,summary='Cancel the requested order',all_items_confirmed=True),confidence='high'))
        w.step(dict(wrong,confidence='high'))
        result=w.result(case,initial)
        self.assertTrue(result['initial_error']);self.assertIsNotNone(w.proposal)
        alternative=copy.deepcopy(case);alternative['target_state_hash']=result['proposed_state_hash']
        rescored=w.result(alternative,initial)
        self.assertFalse(rescored['initial_error']);self.assertEqual(rescored['features'],result['features'])

    def test_wire_schema_selects_tool_before_arguments(self):
        from datetime import datetime,timedelta,timezone
        from unittest.mock import patch
        from overseeing.retail.client import RetailClient
        from overseeing.retail.workflow import ACTION_SCHEMA
        from tempfile import TemporaryDirectory
        class Response:
            status=200;headers={}
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self):return b'{}'
        with TemporaryDirectory() as temp:
            config=json.loads(Path('configs/stage5_retail.json').read_text())
            client=RetailClient(config,Path(temp)/'raw.jsonl',datetime.now(timezone.utc)+timedelta(minutes=1))
            with patch.object(client.opener,'open',return_value=Response()) as request:
                client._http(config['base_url']+'/chat/completions',dict(guided_json=ACTION_SCHEMA))
                payload=json.loads(request.call_args[0][0].data)
                self.assertEqual(list(payload['guided_json']['anyOf'][0]['properties']),['tool','arguments','confidence'])

    def test_session_reserve_and_retry_limits(self):
        from datetime import datetime,timedelta,timezone
        from tempfile import TemporaryDirectory
        from overseeing.retail.client import RetailLedger
        now=datetime.now(timezone.utc)
        auth=dict(name='stage5_practical',authorization='explicit_user_request',attempt_limit=30000,
            started_utc=(now-timedelta(minutes=1)).isoformat(),deadline_utc=(now+timedelta(hours=9,minutes=-1)).isoformat(),
            inference_cutoff_utc=(now+timedelta(hours=7,minutes=29)).isoformat())
        with TemporaryDirectory() as temp:
            path=Path(temp)/'authorization.json';path.write_text(json.dumps(auth))
            ledger=RetailLedger(temp,'mechanics_fixture')
            try:
                call=ledger.reserve_call({'fixture':True});ledger.reserve_attempt(call,0);ledger.reserve_attempt(call,1)
                with self.assertRaises(RuntimeError):ledger.reserve_attempt(call,1)
                ledger.attempts=30000
                with self.assertRaises(RuntimeError):ledger.reserve_call({'fixture':True})
            finally:ledger.close()
            start=now-timedelta(hours=8)
            auth.update(started_utc=start.isoformat(),deadline_utc=(start+timedelta(hours=9)).isoformat(),
                inference_cutoff_utc=(start+timedelta(hours=7,minutes=30)).isoformat())
            path.write_text(json.dumps(auth))
            with self.assertRaises(RuntimeError):RetailLedger(temp,'expired_fixture')

    def test_search_preserves_expiring_opportunity_and_deadline_equality(self):
        requests=[TransactionRequest('urgent',0,0,2,2,.5,8),TransactionRequest('large',1,0,5,2,.5,12),TransactionRequest('medium',2,0,4,2,.5,4)]
        self.assertEqual(choose('greedy',requests,0)[0],'large')
        self.assertEqual(choose('search',requests,0)[0],'urgent')
        self.assertEqual(choose('edf',requests,0)[0],'urgent')
        self.assertEqual(requests[0].benefit(2),6);self.assertEqual(requests[0].benefit(3),0)
        self.assertEqual(choose('search',requests,0)[1]['ordered_subsets_evaluated'],16)

    def test_sparse_calibration_is_pre_review_and_frozen(self):
        rows=[dict(proposal={'tool':'fixture'},initial_error=True,features=dict(family='modify',uncertain=True),reviewed=False),
              dict(proposal={'tool':'fixture'},initial_error=False,features=dict(family='cancel',uncertain=False),reviewed=True)]
        fitted=fit_development(rows,{'partition':'development'})
        estimator=RetailRisk.load(fitted);self.assertEqual(estimator.predict(RiskFeatures('modify',True)),.5)
        self.assertTrue(all(b['fallback'] for b in fitted['bins'].values()))
        with self.assertRaises(FrozenInstanceError):estimator.pooled=.9
        with self.assertRaises(TypeError):estimator.predict(dict(hidden_target='x'))
        changed=copy.deepcopy(fitted);changed['pooled_probability']=.9
        with self.assertRaises(ValueError):RetailRisk.load(changed)

    def test_completed_review_can_correct_but_late_review_cannot_erase(self):
        case=self.case('cancel');initial=account_database(self.data,case['user_id'])
        wrong=copy.deepcopy(case['target_action']);wrong['arguments']['reason']='ordered by mistake' if wrong['arguments']['reason']=='no longer needed' else 'no longer needed'
        p=dict(case_id=case['case_id'],proposal=wrong,initial_error=True,features=dict(family='cancel',uncertain=False),automatic_rejections=0)
        estimator=RetailRisk((('cancel:0',.5),),.5,'fixture')
        bundle=dict(bundle_id='fixture',replicate=0,service_failure_cost=4,slots=[dict(case_id=case['case_id'],agent_id=0,arrival=0,cutoff=2,wrong_transaction_cost=8)])
        args=(bundle,[p],{case['case_id']:case},{case['case_id']:initial},estimator)
        timely=simulate(*args,policy='fcfs',duration=2);late=simulate(*args,policy='fcfs',duration=3)
        self.assertEqual(timely['operational_loss'],0);self.assertEqual(timely['corrections'],1)
        self.assertEqual(late['operational_loss'],12);self.assertEqual(late['completed_reviews'],0)
        self.assertEqual(late['wrong_transactions'],1)
        requests=[e['request'] for e in late['events'] if e['event']=='review_request_arrived']
        self.assertNotIn('initial_error',requests[0]);self.assertNotIn('target_action',requests[0])

if __name__=='__main__':unittest.main()
