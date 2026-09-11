import copy
import json
import random
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from .planner import Factor,Task,Option,Planner,Protocol,OTHER,UNRESOLVED
from .synthetic import generate,decode
from .evaluate import run
from .exact import solve
from .common import ART,read,digest

class PlanningTests(unittest.TestCase):
    def test_complementary_questions(self):
        case,_=generate('complementary',2000);f,t=decode(case);p=Planner(f,t)
        self.assertEqual(p.factors[p.select(p.initial,2,1)].id,'q3')
        self.assertEqual(p.factors[p.select(p.initial,2,2)].id,'q1')
        c=Protocol(p,2);self.assertEqual(c.propose()['id'],'q1');c.answer('A')
        self.assertEqual(c.propose()['id'],'q2');c.answer('B')
        self.assertIsNone(c.propose());self.assertEqual(sum(x['status']=='release' for x in c.finish()),3)

    def test_unasked_hidden_state_isolation(self):
        case,gold=generate('scope_exception',2001);f,t=decode(case)
        a=Planner(f,t);b=Planner(f,t)
        altered=copy.deepcopy(gold)
        altered['truth']={k:'secret_canary' for k in gold['truth']}
        self.assertEqual(a.select(a.initial,2,2),b.select(b.initial,2,2))
        # Evaluator outputs can differ, but all events before any answer must match.
        _,ta,_=run(a,gold['targets'],gold['truth'],'depth2',0)
        _,tb,_=run(b,altered['targets'],altered['truth'],'depth2',0)
        self.assertEqual(ta['events'],tb['events'])

    def test_exact_agreement_small_instances(self):
        for family in ['independent','mixed','scope_exception','noisy_response','unresolved_response']:
            for seed in range(4):
                case,_=generate(family,seed);f,t=decode(case)
                for depth in [1,2,3]:
                    p=Planner(f,t,node_limit=1000000);a=p.select(p.initial,3,depth,'exact')
                    ref=solve(p,p.initial,3,depth)
                    self.assertEqual(a,ref['action'])
                    self.assertAlmostEqual(p.last_stats['expected_plan_loss'],ref['value'],10)

    def test_path_budget_all_response_branches(self):
        case,_=generate('noisy_response',7);f,t=decode(case);p=Planner(f,t,unresolved_probability=.2,response_error=.2)
        def walk(s,b,spent):
            a=p.select(s,b,2)
            self.assertLessEqual(spent,2)
            if a is None:return
            cost=p.factors[a].cost;self.assertLessEqual(cost,b)
            for _,_,n in p.response_branches(s,a):walk(n,b-cost,spent+cost)
        walk(p.initial,2,0)

    def test_unresolved_is_not_known_other(self):
        p=Planner([Factor('x',(OTHER,),(1.,))],[Task('a',(Option((('x','x'),)),))])
        c=Protocol(p,1);c.propose();c.answer(UNRESOLVED)
        self.assertEqual(c.finish()[0]['status'],'defer');self.assertEqual(c.spent,1)

    def test_out_of_support_paid_answer(self):
        p=Planner([Factor('x',('A',OTHER),(.2,.8))],[Task('a',(Option((('x','x'),)),))])
        c=Protocol(p,1);c.propose();c.answer('actual_new_value')
        self.assertEqual(c.finish()[0]['values']['x'],'actual_new_value')
        self.assertEqual(c.spent,1)

    def test_shared_factor_not_independent_copies(self):
        p=Planner([Factor('x',('A','B'),(.8,.2))],[Task('a',(Option((('first','x'),('second','x'))),))])
        self.assertAlmostEqual(p.terminal(p.initial)[1][0]['probability_correct'],.8)

    def test_exception_and_explicit_scope(self):
        f=Factor('x',('A','B'),(1.,0.),exceptions=('excepted',),allowed_tasks=('allowed','excepted'))
        p=Planner([f],[Task(k,(Option((('x','x'),)),)) for k in ['allowed','excepted','outside']])
        self.assertEqual([o['status'] for o in p.terminal(p.initial)[1]],['release','defer','defer'])

    def test_revision_and_revocation_invalidate_registered_releases(self):
        p=Planner([Factor('x',('A','B',OTHER),(1.,0.,0.)),Factor('z',('A','B'),(1.,0.))],
            [Task('a',(Option((('x','x'),)),)),Task('b',(Option((('z','z'),)),))])
        c=Protocol(p,2);c.finish();c.revise('x','B')
        self.assertFalse(c.release_current('a'));self.assertTrue(c.release_current('b'))
        self.assertEqual(c.finish()[0]['values']['x'],'B')
        c.revise('x',revoke=True);self.assertFalse(c.release_current('a'))
        self.assertEqual(c.finish()[0]['status'],'defer')

    def test_budget_and_scope_question_count_separate(self):
        case,gold=generate('scope_exception',4);f,t=decode(case);p=Planner(f,t)
        c=Protocol(p,0);self.assertIsNone(c.propose());self.assertEqual(c.spent,0)
        with self.assertRaises(ValueError):c.answer('yes')
        with self.assertRaises(ValueError):Protocol(p,-1)
        with self.assertRaises(ValueError):Factor('bad',('a',),(1.,),cost=0)

    def test_no_question_uses_evaluation_modules(self):
        import inspect
        from . import planner
        text=inspect.getsource(planner)
        for x in ['evaluation_only.json','gold[','truth[','from .evaluate','from .empirical']:self.assertNotIn(x,text)

    def test_estimator_hash_and_source_split(self):
        est=read(ART/'estimator.json');self.assertEqual(est['sha256'],digest({k:v for k,v in est.items() if k!='sha256'}))
        cases=read(ART/'data/public.json');audit=read(ART/'data/audit.json')
        self.assertEqual(len({c['id'] for c in cases}),60)
        self.assertTrue(all(len(c['tasks'])>=2 for c in cases))
        self.assertFalse({c['id'] for c in cases}&set(audit['previously_exposed_ids']))

    def test_expired_authorization_prevents_network(self):
        from . import client
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'authorization.json').write_text(json.dumps(dict(inference_cutoff_utc='2000-01-01T00:00:00+00:00')))
            with patch.object(client,'ART',root),patch.object(client,'http') as network:
                with self.assertRaisesRegex(RuntimeError,'cutoff'):client.generate('x',[],1,1)
                network.assert_not_called()

if __name__=='__main__':unittest.main()
