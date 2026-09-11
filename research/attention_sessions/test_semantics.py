import unittest,json
from dataclasses import replace
from .method import *
from .controller import Controller
from .evaluate import simulate
from .data import load,workload,bundles,conditions

def req(key,context='A',arrival=0,deadline=10,gain=.5,scope=''):
    return Request(key,context,context,arrival,deadline,4,.5,gain,'normal',{},scope)

class Semantics(unittest.TestCase):
    def test_exact_deadline_and_late_override(self):
        r=req('a',deadline=2);c=Controller([r],Settings(setup=1,decision=1),'edf')
        self.assertTrue(c.start());self.assertTrue(c.complete('heating_valve'))
        self.assertEqual(c.status['a'],'reviewed');self.assertEqual(c.now,2)
        c=Controller([r],Settings(setup=1,decision=1),'edf');c.advance(.01)
        with self.assertRaises(ValueError):c.start(['a'],override=True)

    def test_guard_rejects_context_batch_that_loses_outside_deadline(self):
        a=req('a',deadline=10);b=req('b',deadline=10);urgent=req('c','B',deadline=2)
        s=Settings(setup=0,switch=0,coordination=0)
        cert=certificate([a,b],[a,b,urgent],0,None,s,12)
        self.assertFalse(cert['valid']);self.assertIn('c',cert['lost'])
        group,_=select('guarded',[a,b,urgent],0,None,s,12)
        self.assertTrue(certificate(group,[a,b,urgent],0,None,s,12)['valid'])

    def test_singletons_share_context_with_all_policies(self):
        c=Controller([req('a'),req('b')],Settings(setup=1,switch=.5,coordination=0),'fifo')
        while c.step(lambda k:'normal'):pass
        self.assertEqual(c.components['setup'],1);self.assertEqual(c.used,3)
        self.assertEqual(c.session_id,2)

    def test_setup_switch_coordination_are_distinct(self):
        s=Settings(setup=1,switch=.5,coordination=.25)
        self.assertEqual(parts(req('x','B'),'A',s,1),dict(setup=1,switch=.5,decision=1,coordination=.25))
        self.assertEqual(parts(req('y','B'),'B',s,1)['setup'],0)

    def test_active_coordination_is_in_certificate(self):
        s=Settings(setup=0,switch=0,decision=1,coordination=.25)
        r=req('a',deadline=1)
        self.assertTrue(certificate([r],[r],0,'A',s,10)['valid'])
        self.assertFalse(certificate([r],[r],0,'A',s,10,position=1)['valid'])

    def test_negative_gain_and_budget_do_not_force_review(self):
        for policy in POLICIES:
            group,_=select(policy,[req('a',gain=-.2)],0,None,Settings(),12)
            self.assertEqual(group,[])
            group,_=select(policy,[req('a')],0,None,Settings(),0)
            self.assertEqual(group,[])

    def test_no_future_or_private_input(self):
        with self.assertRaises(ValueError):select('edf',[req('future',arrival=2)],0,None,Settings(),12)
        with self.assertRaises(ValueError):select('edf',[{'truth':'normal'}],0,None,Settings(),12)
        with self.assertRaises(ValueError):replace(req('a'),evidence={'source_label':'normal'})
        c=Controller([req('future',arrival=2)])
        self.assertEqual(c.snapshot()['requests'],[])

    def test_deferral_keeps_item_visible_and_resumes(self):
        c=Controller([req('a')]);c.defer('a',3)
        self.assertEqual(c.snapshot()['requests'][0]['status'],'deferred')
        self.assertEqual(c.pending(),[]);c.advance(3);self.assertEqual(len(c.pending()),1)
        with self.assertRaises(ValueError):c.defer('a',10)

    def test_no_answer_propagation_by_similarity(self):
        with self.assertRaises(ValueError):validate_shared_answer([req('a'),req('b')],'same-equipment',['a','b'])
        a=req('a',scope='decision:ventilation-mode:v1');b=req('b',scope=a.scope)
        self.assertEqual(validate_shared_answer([a,b],a.scope,['a','b']),('a','b'))
        with self.assertRaises(ValueError):validate_shared_answer([a,b],a.scope,['a'])
        with self.assertRaises(ValueError):validate_shared_answer([a,replace(b,scope='v2')],a.scope,['a','b'])

    def test_imperfect_groups_do_not_cross_verified_contexts(self):
        a=req('a','A');b=replace(req('b','B'),suggested_context='A')
        self.assertTrue(all(len({r.context for r in g})==1 for g in candidates([a,b],3)))
        c=Controller([a,b])
        with self.assertRaises(ValueError):c.start(['a','b'],override=True)

    def test_failures_and_harm_are_retained(self):
        config=dict(setup=0,budget=12,reviewer='model_risk')
        p=[req('bad'),req('harm'),req('review_failed')]
        p[0]=replace(p[0],proposal='invalid')
        private={'bad':dict(truth='heating_valve',review='invalid'),'harm':dict(truth='normal',review='cooling_valve'),
                 'review_failed':dict(truth='normal',review='invalid')}
        r=simulate(p,private,config,'fifo')
        self.assertEqual(r['metrics']['proposal_failures'],1);self.assertEqual(r['metrics']['review_failures'],2)
        self.assertEqual(r['metrics']['harms'],1);self.assertEqual(r['metrics']['unresolved'],2)
        self.assertEqual(len(r['jobs']),3)

    def test_label_permutation_does_not_change_dispatch(self):
        cases,records,e=load('development');cfg=dict(load='high',reviewer='ideal')
        pub,priv=workload(bundles(cases)[0],cases,records,e,cfg)
        config=dict(cfg,setup=1,budget=12)
        r=simulate(pub,priv,config,'guarded')
        changed={k:dict(v,truth='normal') for k,v in priv.items()}
        other=simulate(pub,changed,config,'guarded')
        self.assertEqual(r['sequence'],other['sequence'])
        self.assertNotIn('source_label',json.dumps([asdict(r) for r in pub]))

    def test_exact_replay(self):
        c=Controller([req('a'),req('b','B',arrival=1)]);d=Controller([req('a'),req('b','B',arrival=1)])
        while c.step(lambda k:'normal'):pass
        while d.step(lambda k:'normal'):pass
        self.assertEqual(c.events,d.events)

    def test_source_bundles_are_disjoint_whole_days(self):
        cases,records,e=load();groups=bundles(cases)
        self.assertEqual(len(groups),6);self.assertEqual(len(set(sum(groups,[]))),18)
        self.assertEqual(len(cases),54)
        for day in sum(groups,[]):self.assertEqual(sum(c['run_id']==day for c in cases),3)

if __name__=='__main__':unittest.main()
