"""Concrete risks found during audit, including online versus terminal-only use."""
import copy
import unittest
from unittest.mock import patch
from .planner import Factor,Task,Option,Planner,Protocol
from .safe_protocol import SafeProtocol
from .synthetic import generate,decode
from .repair_scope import repaired_case
from .evaluate import run
from .exact import solve
from .completion_audit import MinimumCompletion
from .common import ART,read
from .empirical import build

class AuditTests(unittest.TestCase):
    def test_confirmation_invalidates_previously_released_value(self):
        factors=[Factor('x',('A','B'),(.9,.1)),Factor('z',('A','B'),(1.,0.))]
        tasks=[Task('a',(Option((('x','x'),)),)),Task('b',(Option((('z','z'),)),))]
        c=SafeProtocol(Planner(factors,tasks),1);c.finish()
        self.assertTrue(c.release_current('a'));c.propose('depth2');c.answer('B')
        self.assertFalse(c.release_current('a'));self.assertTrue(c.release_current('b'))
        self.assertEqual(c.finish()[0]['values']['x'],'B')

    def test_scope_gate_cannot_bypass_explicit_exception(self):
        from .safe_protocol import SafePlanner
        f=[Factor('x',('A',),(1.,)),Factor('scope',('yes','no'),(1.,0.),kind='scope',exceptions=('b',))]
        t=[Task(id,(Option((('x','x'),),(('scope','yes'),)),)) for id in ['a','b']]
        c=SafeProtocol(Planner(f,t),0);out=c.finish()
        self.assertEqual([x['status'] for x in out],['release','defer'])
        c.revise('scope',value='yes',exceptions=())
        self.assertEqual([x['status'] for x in c.finish()],['release','release'])

    def test_confirmation_retains_received_answer_provenance(self):
        c=SafeProtocol(Planner([Factor('x',('A','B'),(.5,.5),source='ambiguous brief')],[Task('a',(Option((('x','x'),)),))]),1)
        c.propose();c.answer('B')
        self.assertIn('Received answer',c.planner.factors[0].source)
        self.assertIn('ambiguous brief',c.planner.factors[0].source)

    def test_corrected_local_answer_matches_effective_target(self):
        mismatches=0
        for family in ['scope_exception','wrong_sharing']:
            for seed in range(5000,5020):
                _,old=generate(family,seed);_,new=repaired_case(family,seed)
                mismatches+=old['truth']['exception.preference']!=old['targets']['exception_implementation']['value']
                self.assertEqual(new['truth']['exception.preference'],new['targets']['exception_implementation']['value'])
                self.assertEqual(new['targets'],old['targets'])
        self.assertEqual(mismatches,13)

    def test_minimum_sufficient_completion_counts_known_inputs(self):
        # Task a needs one answer despite having four uncertain/supplied factors.
        f=[Factor('a0',('A','B'),(.5,.5))]+[Factor('a'+str(i),('A','B'),(.99,.01)) for i in range(1,4)]
        f += [Factor('b'+str(i),('A','B'),(.5,.5)) for i in range(2)]
        tasks=[Task('a',(Option(tuple((x.id,x.id) for x in f[:4])),)),Task('b',(Option(tuple((x.id,x.id) for x in f[4:])),))]
        p=MinimumCompletion(f,tasks)
        self.assertEqual(p.factors[p.heuristic(p.initial,2,'minimum_completion')].id,'a0')

    def test_initial_question_is_independent_of_private_answers(self):
        from . import evaluate
        case,gold=generate('independent',33);f,t=decode(case);other=copy.deepcopy(gold)
        other['truth']={k:'B' if v=='A' else 'A' for k,v in gold['truth'].items()}
        for task in other['targets']:
            other['targets'][task]={k:other['truth'][k] for k in other['targets'][task]}
        a,ta,_=run(Planner(f,t),gold['targets'],gold['truth'],'depth2',2)
        b,tb,_=run(Planner(f,t),other['targets'],other['truth'],'depth2',2)
        self.assertEqual(ta['events'][0],tb['events'][0])

    def test_small_pruning_has_no_general_optimality_guarantee(self):
        case,gold=generate('complementary',4);f,t=decode(case)
        for i,weight in enumerate([.8,.7,.6]):
            key='a'+str(i);f.append(Factor(key,('A','B'),(.5,.5)));t.append(Task(key,(Option(((key,key),)),),4.,weight))
        p=Planner(f,t,width=2);p.select(p.initial,2,2)
        exact=solve(p,p.initial,2)
        self.assertAlmostEqual(p.last_stats['expected_plan_loss']-exact['value'],1.2)

    def test_online_fix_preserves_terminal_only_primary_decisions(self):
        from . import evaluate
        cases=[c for c in read(ART/'data/public.json') if c['split']=='evaluation']
        gold={c['id']:c['target'] for c in read(ART/'data/evaluation_only.json')};est=read(ART/'estimator.json')
        for case in cases:
            for rep in range(2):
                prep=read(ART/'prepared'/('evaluation_'+case['id'][:-5]+'_'+str(rep)+'.json'))
                targets={t['id']:{k:gold[case['id']][k] for k in t['required']} for t in case['tasks']}
                old,ot,_=run(build(case,prep,est),targets,gold[case['id']],'depth2',2)
                with patch.object(evaluate,'Protocol',SafeProtocol):new,nt,_=run(build(case,prep,est),targets,gold[case['id']],'depth2',2)
                self.assertEqual({k:v for k,v in old.items() if k not in ('planning_nodes','planning_caps')}, {k:v for k,v in new.items() if k not in ('planning_nodes','planning_caps')})
                self.assertEqual([e['question']['id'] for e in ot['events'] if e['kind']=='question_shown'],[e['question']['id'] for e in nt['events'] if e['kind']=='question_shown'])

if __name__=='__main__':unittest.main()
