import unittest
from copy import deepcopy
from research.oversight_simulation.inputs import OUT,workload
from research.oversight_simulation.design import build_design
from research.oversight_simulation.run import environment
from research.oversight_simulation.simulation import simulate,replay_trace,SimulationDesk
from research.oversight_simulation.policies import choose
from research.oversight_simulation.reviewer import orientation_time
from research.oversight_workflow.common import read,digest


class SimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs=read(OUT/'inputs.json');cls.design=build_design();cls.env=environment(cls.inputs)
    def cfg(self,**changes):return {**self.design['configs'][3],**changes}
    def runone(self,policy='Q',**changes):
        c=self.cfg(**changes);items=workload(self.inputs,c,0)
        s,t=simulate(items,self.inputs['sources'],c,policy,17,self.env);return s,t,items
    def test_real_inputs_original_schedule_and_no_duplicate_goals(self):
        self.assertEqual(len(self.inputs['items']),36);self.assertEqual(sum(self.env.initial_correct.values()),7)
        x=workload(self.inputs,self.cfg(),0);self.assertEqual([i['start'] for i in x],[0.,4.,8.,12.,16.,20.,180.,184.,188.,192.,196.,200.])
        for n in (6,12,24,36):
            for r in (0,1,2):self.assertEqual(len({x['id'] for x in workload(self.inputs,self.cfg(offered=n),r)}),n)
    def test_equal_information_and_no_future_or_labels_in_selector(self):
        p=[dict(id='a',source_id='S',arrival=0),dict(id='b',source_id='T',arrival=1),dict(id='c',source_id='S',arrival=2)]
        for pol in ('Q','G','Q-source-aware','Q-sticky','M'):
            before=choose(deepcopy(p),pol,'S',[])
            hidden={'a':True,'b':False};hidden.update(a=False,b=True)
            self.assertEqual(before,choose(deepcopy(p),pol,'S',[]))
        self.assertEqual(choose(p,'Q-sticky','S',[])[0],'a')
        self.assertEqual(choose(p,'G',None,[])[1],['a','c'])
    def test_shared_familiarity_and_zero_cost_equivalence(self):
        for seed in (0,1,2):
            c=self.cfg(group_seconds=0,orientation=25);items=workload(self.inputs,c,0)
            a,ta=simulate(items,self.inputs['sources'],c,'G',seed,self.env)
            b,tb=simulate(items,self.inputs['sources'],c,'Q-source-aware',seed,self.env)
            for k in a:
                if k not in ('groups','events'):self.assertEqual(a[k],b[k],k)
            self.assertEqual([(r['id'],r['action'],r['end']) for r in ta['reviews']],[(r['id'],r['action'],r['end']) for r in tb['reviews']])
        item=items[0];self.assertGreater(orientation_time(item,0,{},0,c),orientation_time(item,10,{item['source_id']:(10,1)},1,c))
    def test_accounting_cutoff_and_partial_work(self):
        for policy in ('Q','G','Q-source-aware','Q-sticky','M'):
            s,t,_=self.runone(policy,horizon=15)
            self.assertEqual(s['correct']+s['incorrect']+s['unfinished'],12)
            self.assertLessEqual(sum(v for k,v in s.items() if k.startswith('time_')),15+1e-8)
            self.assertGreater(s['unstarted'],0);self.assertTrue(all(x[0]<=15 for x in t['commands']))
    def test_full_engine_replay_and_reproducibility(self):
        for pol in ('Q','G','M'):
            s,t,items=self.runone(pol)
            self.assertEqual(t['final_state_sha256'],replay_trace(t,items,self.inputs['sources'],pol,True))
            self.assertEqual((s,t),self.runone(pol)[:2])
    def test_failure_deferral_retains_original_and_does_not_release(self):
        s,t,items=self.runone('M',manual_accuracy=0.,recognized_failure=1.,manual_seconds=1.,orientation=0,question_seconds=1,interaction_seconds=1,horizon=540)
        self.assertEqual(s['released'],0);self.assertEqual(s['unfinished'],12)
        self.assertTrue(any(x[1]=='decide' and x[2]['decision']=='defer' for x in t['commands']))
        self.assertEqual(s['blocked'],12)
        self.assertEqual(replay_trace(t,items,self.inputs['sources'],'M',True),t['final_state_sha256'])
    def test_cutoff_equality_and_version_release(self):
        s,t,items=self.runone('M',orientation=0,manual_seconds=1,question_seconds=1,manual_accuracy=1,damage=0)
        end=t['reviews'][0]['end'];c=self.cfg(orientation=0,manual_seconds=1,question_seconds=1,manual_accuracy=1,damage=0,horizon=end)
        s2,t2=simulate(items,self.inputs['sources'],c,'M',17,self.env)
        self.assertEqual(s2['released'],1)
        self.assertTrue(all(p['version']==2 for _,a,p in t2['commands'] if a=='release'))
    def test_no_questionnaires_or_human_schema(self):
        _,t,_=self.runone();self.assertEqual(t['record_kind'],'computational_simulation')
        self.assertNotIn('participant_code',t);self.assertNotIn('questionnaire',t)

if __name__=='__main__':unittest.main()
