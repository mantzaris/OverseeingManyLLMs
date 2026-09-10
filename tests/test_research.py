"""Concrete Stage 4 budget, public-posterior, nesting, and scheduling checks."""
from dataclasses import replace
from datetime import datetime,timedelta,timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from overseeing.domain import PublicJob,PrivateJob
from overseeing.research_budget import SessionLedger,ResearchBudgetExceeded,authorized_window
from overseeing.research_risk import analytical_error,load_risk
from overseeing.research_workload import generate_larger_scenario,job_rng

ROOT=Path(__file__).resolve().parent.parent

class ResearchFoundationChecks(unittest.TestCase):
    def test_analytical_complementary_actions_and_information_boundary(self):
        for clues,following in ((('filter','filter'),1/7),(('filter','sensor'),3/11)):
            public=PublicJob('x',0,0,4,1,8,clues)
            self.assertAlmostEqual(analytical_error(public,'replace_filter'),following)
            self.assertAlmostEqual(analytical_error(public,'reset_sensor'),1-following)
            self.assertAlmostEqual(analytical_error(replace(public,clues=tuple('sensor' if c=='filter' else 'filter' for c in clues)),'reset_sensor'),following)
            with self.assertRaises(TypeError):analytical_error(PrivateJob(public,'filter'),'replace_filter')
            # Costs and identity carry no information about the fault in this observation model.
            self.assertEqual(analytical_error(public,'replace_filter'),analytical_error(replace(public,terminal_cost=100,agent_id=5),'replace_filter'))
        frozen=load_risk('frozen',ROOT/'artifacts/stage2_development/run/estimator.json')
        self.assertEqual(frozen.predict(public,'reset_sensor','reset_sensor'),13/89)

    def test_larger_workload_nested_agents_closed_waves_and_independent_streams(self):
        for seed in range(400,464):
            small,large=generate_larger_scenario(seed,3),generate_larger_scenario(seed,6)
            self.assertEqual(small.jobs,large.jobs[:9])
            self.assertEqual((len(large.jobs),large.horizon),(18,24))
            for j in large.jobs:
                p=j.public;wave=int(p.job_id.split('j')[1]);self.assertIn(p.release-8*wave,(0,1))
                self.assertLess(p.deadline,8*(wave+1));self.assertIn(p.deadline-p.release,(2,4,6))
        original=generate_larger_scenario(400,6)
        def perturb(seed,agent,job,component):return job_rng(seed+(10000 if component=='hidden' else 0),agent,job,component)
        with patch('overseeing.research_workload.job_rng',side_effect=perturb):changed=generate_larger_scenario(400,6)
        self.assertEqual([replace(j.public,clues=('filter','filter')) for j in original.jobs],[replace(j.public,clues=('filter','filter')) for j in changed.jobs])

    def test_session_ledger_caps_single_writer_and_reporting_reserve(self):
        now=datetime.now(timezone.utc);start=now-timedelta(minutes=1)
        auth=dict(name='stage4_research',authorization='explicit_user_request',started_utc=start.isoformat(),deadline_utc=(start+timedelta(hours=9)).isoformat(),inference_cutoff_utc=(start+timedelta(hours=7.5)).isoformat(),limit_hours=9,scheduled_call_limit=50000,attempt_limit=60000)
        with self.assertRaises(ResearchBudgetExceeded):authorized_window(auth,start+timedelta(hours=8))
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'authorization.json').write_text(json.dumps(auth));ledger=SessionLedger(p,'fixture')
            with self.assertRaises(ResearchBudgetExceeded):SessionLedger(p,'second-worker')
            call=ledger.reserve_call({'scenario_seed':400},0);ledger.reserve_attempt(call,0);ledger.reserve_attempt(call,1)
            with self.assertRaises(ResearchBudgetExceeded):ledger.reserve_attempt(call,1)
            ledger.close();resumed=SessionLedger(p,'next-block');self.assertEqual((resumed.calls,resumed.attempts),(1,2))
            resumed.calls=50000
            with self.assertRaises(ResearchBudgetExceeded):resumed.reserve_call({},0)
            resumed.attempts=60000
            with self.assertRaises(ResearchBudgetExceeded):resumed.reserve_attempt(1,0)
            resumed.close()


    def test_exact_search_six_requests_and_stable_equal_value_ties(self):
        from overseeing.domain import ReviewRequest
        from overseeing.research_scheduler import ResearchScheduler
        from overseeing.research_workload import generate_competition_scenario
        from overseeing.policies import choose
        scenario=generate_competition_scenario(301)
        requests=tuple(ReviewRequest(j.public.job_id,j.public.agent_id,6,j.public.deadline,0,j.public.terminal_cost,1,13/89,'reset_sensor') for j in scenario.jobs if j.public.release==6)
        stable=ResearchScheduler('delay')
        self.assertEqual(stable(requests,6),'a0j1')
        self.assertEqual(stable(tuple(replace(r,p_error=18/98) for r in requests),6),'a0j1')
        six=tuple(ReviewRequest(str(i),i,0,6,0,4,1,.5,'reset_sensor') for i in range(6))
        self.assertEqual(stable(six,0),'0')
        self.assertEqual(stable.last_record['ordered_subsets_evaluated'],1957)
        with self.assertRaises(ValueError):stable(six+(replace(six[0],job_id='extra'),),0)

    def test_public_risk_simulation_future_boundary_and_compressed_replay(self):
        from overseeing.research_scheduler import ResearchScheduler
        from overseeing.simulator import run_episode,StipulatedProposals
        from overseeing.replay import replay_score
        from overseeing.io import read_events
        from overseeing.research_execution import compress_evidence
        scenario=generate_larger_scenario(410,6)
        risk=load_risk('analytical',ROOT/'artifacts/stage2_development/run/estimator.json')
        provider=StipulatedProposals({j.public.job_id:'replace_filter' for j in scenario.jobs})
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'events.jsonl'
            result=run_episode(scenario,'delay',provider,path,public_estimator=risk,scheduler=ResearchScheduler('delay'),max_pending=6,record_dispatch=True)
            self.assertEqual(result['status'],'completed')
            self.assertEqual(result['jobs_closed'],18)
            events=read_events(path)
            for e in events:
                if e['event']=='planning_decision':
                    self.assertLessEqual(e['pending_count'],6)
                    self.assertTrue(all(r['requested_at']<=e['tick'] for r in e['public_pending']))
            before=replay_score(path);compress_evidence(path)
            self.assertEqual(replay_score(path),before)
            observations=provider.observations
            self.assertEqual(len(observations),18)
            for obs in observations:
                self.assertNotIn('fault',obs['job'])
                self.assertTrue(all(h['job_id'].startswith('a'+str(obs['job']['agent_id'])+'j') for h in obs['history']))

    def test_objective_penalty_changes_public_benefit_and_eligibility_consistently(self):
        from overseeing.domain import ReviewRequest
        from overseeing.research_scheduler import ResearchScheduler
        a=ReviewRequest('a',0,0,2,0,4,2,.8,'replace_filter')
        b=ReviewRequest('b',1,0,2,0,12,2,.3,'replace_filter')
        self.assertEqual(ResearchScheduler('delay',0)((a,b),0),'b')
        self.assertEqual(ResearchScheduler('delay',4)((a,b),0),'a')
        free=replace(a,terminal_cost=0)
        self.assertIsNone(ResearchScheduler('delay',0)((free,),0))
        self.assertEqual(ResearchScheduler('delay',4)((free,),0),'a')
        self.assertIsNone(ResearchScheduler('delay',4)((free,),1))
        self.assertEqual(free.terminal_cost,0)  # Never mutate the original scoring objective.
        from overseeing.research_plan import objective_branch_plan,selected_evaluation_plan
        self.assertEqual(sum(r['planned_calls'] for r in objective_branch_plan()),1152)
        self.assertEqual(sum(r['planned_calls'] for r in objective_branch_plan(True)),4608)
        self.assertEqual(sum(r['planned_calls'] for r in selected_evaluation_plan()),43008)

    def test_historical_csv_portability_does_not_allow_changed_values(self):
        import hashlib
        from overseeing.research_analysis import historical_file_status
        raw=b'seed,loss\r\n100,3\r\n';lf=raw.replace(b'\r\n',b'\n')
        expected=hashlib.sha256(raw).hexdigest();normalized=hashlib.sha256(lf).hexdigest()
        self.assertEqual(historical_file_status(raw,expected,normalized),'unchanged')
        self.assertEqual(historical_file_status(lf,expected,normalized),'csv_line_endings')
        self.assertEqual(historical_file_status(lf.replace(b'100,3',b'100,4'),expected,normalized),'changed')
        self.assertEqual(historical_file_status(lf,expected),'changed')

    def test_gpu_startup_evidence_survives_long_cache_log(self):
        from overseeing.gpu import relevant_log_evidence
        log='Using CUDA device\nModel dtype bfloat16\nAPI_KEY=private cuda\n'+'GPU cache usage 0%\n'*200
        lines=relevant_log_evidence(log)
        self.assertIn('Using CUDA device',lines)
        self.assertIn('Model dtype bfloat16',lines)
        self.assertFalse(any('private' in line for line in lines))
        self.assertLessEqual(len(lines),100)

    def test_batch_saved_evidence_audit_and_paired_summary_with_stipulated_transport(self):
        from overseeing.client import GPUClient
        from overseeing.research_plan import run_entry,finish_plan
        from overseeing.research_execution import prepare_batch,run_batch
        from overseeing.research_analysis import audit_batch,summarize_batches,paired_interval
        from overseeing.io import write_json
        counter=[0]
        def transport(client,url,payload):
            if url.endswith('/tokenize'):return 200,'{"count":100}',None
            counter[0]+=1
            action='reset_sensor' if payload['seed']%2 else 'replace_filter'
            return 200,json.dumps({'id':'fixture-'+str(counter[0]),'choices':[{'finish_reason':'stop','message':{'content':json.dumps({'action':action})}}],'usage':{'prompt_tokens':100,'completion_tokens':7}}),None
        def gpu(pid,log,path):
            write_json(path,dict(status='placement_verified',model='Qwen/Qwen2.5-7B-Instruct',revision='a09a35458c702b33eeacc393d103063234e8bc28',
                cuda_runtime=dict(bf16_matmul_verified=True,device_name='NVIDIA RTX 6000 Ada Generation'),
                server_arguments={'--dtype':'bfloat16','--cpu-offload-gb':'0','--swap-space':'0','--tensor-parallel-size':'1','--max-num-seqs':'1'}))
        def metrics(out,suffix):
            (out/('metrics_'+suffix+'.txt')).write_text('\n'.join('{}{{model="fixture"}} {}'.format(name,counter[0]*multiplier) for name,multiplier in (('vllm:request_success_total',1),('vllm:prompt_tokens_total',100),('vllm:generation_tokens_total',7))))
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);start=datetime.now(timezone.utc)
            write_json(root/'authorization.json',dict(name='stage4_research',authorization='explicit_user_request',started_utc=start.isoformat(),deadline_utc=(start+timedelta(hours=9)).isoformat(),inference_cutoff_utc=(start+timedelta(hours=7.5)).isoformat(),limit_hours=9,scheduled_call_limit=50000,attempt_limit=60000))
            entries=finish_plan([run_entry('fixture','larger',seed,6,policy,2) for seed in (400,401) for policy in ('greedy','delay')]+[run_entry('objective_fixture','larger',402,6,'delay',2,penalty=k) for k in (0,4)])
            prepare_batch(root,'fixture',entries,'Stipulated transport test; not live evidence')
            with patch('overseeing.research_execution.collect_evidence',side_effect=gpu),patch('overseeing.research_execution.server_snapshot',side_effect=metrics),patch.object(GPUClient,'_http',transport),patch('builtins.print'):
                result=run_batch(root,'fixture',0,'fixture')
            self.assertEqual(result['status'],'completed')
            audit=audit_batch(root,'fixture');self.assertEqual(audit['completed_replays'],6)
            self.assertEqual(audit['counts']['scheduled_calls'],216)
            summary=summarize_batches(root,['fixture'],'fixture');self.assertEqual(summary['completed_episodes'],6)
            core=[r for r in summary['policy_outcomes'] if r['policy']=='delay' and r['study']=='core']
            objective=[r for r in summary['policy_outcomes'] if r['closure_penalty']==0 and r['study']=='objective']
            self.assertEqual(core[0]['completed_episodes'],2)
            self.assertEqual(objective[0]['completed_episodes'],1)
            with self.assertRaisesRegex(ValueError,'Duplicate scenario'):
                summarize_batches(root,['fixture','fixture'],'duplicate_fixture')
            self.assertEqual(paired_interval([1,1],[400,401]),(1.,1.))
            lo,hi=paired_interval([1,3],[400,401]);lo2,hi2=paired_interval([2,6],[400,401])
            self.assertEqual((lo2,hi2),(2*lo,2*hi))

    def test_declared_matrix_call_counts_and_no_evaluation_development_overlap(self):
        from overseeing.research_plan import development_plan,evaluation_plan
        development=development_plan();evaluation=evaluation_plan()
        self.assertEqual(sum(e['planned_calls'] for e in development),4032)
        self.assertEqual(sum(e['planned_calls'] for e in evaluation),38400)
        self.assertEqual(len(evaluation),2560)
        self.assertFalse({e['seed'] for e in development}&{e['seed'] for e in evaluation})
        self.assertEqual({e['seed'] for e in evaluation if e['workload']=='original'},set(range(10000,10064)))
        for e in evaluation:
            self.assertEqual(e['closure_penalty'],0)
            self.assertEqual(e['planned_calls'],2*e['jobs'])

if __name__=='__main__':unittest.main()
