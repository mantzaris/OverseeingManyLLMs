"""Focused checks of constructed competition and its bounded execution path."""
from dataclasses import replace
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from overseeing.client import GPUClient
from overseeing.cli import validate_deadline
from overseeing.competition import (episode_plan, load_competition_config, prepare_competition,
                                    run_competition, load_frozen_estimator, FROZEN_ESTIMATOR)
from overseeing.competition_analysis import analyze_competition
from overseeing.competition_condition import generate_competition_scenario
from overseeing.domain import PrivateJob, PublicJob, ReviewRequest, Scenario, STAGE1_POLICIES, STAGE2_POLICIES
from overseeing.io import read_events, write_json
from overseeing.policies import choose
from overseeing.replay import replay_score
from overseeing.simulator import StipulatedProposals, run_episode

ROOT = Path(__file__).resolve().parent.parent


class CompetitionChecks(unittest.TestCase):
    def test_generator_separates_public_assignment_from_hidden_randomness(self):
        baseline = generate_competition_scenario(300)
        def changed_hidden(rng):
            for _ in range(100):
                rng.random()
            return 'sensor', ('filter', 'filter')
        with patch('overseeing.competition_condition.hidden_fault_and_clues', side_effect=changed_hidden):
            changed = generate_competition_scenario(300)
        assignments = lambda s: [(j.public.agent_id, j.public.release, j.public.deadline, j.public.terminal_cost) for j in s.jobs]
        self.assertEqual(assignments(baseline), assignments(changed))
        # Perturb each public stream; hidden faults/clues and the other assignment must stay fixed.
        from overseeing.competition_condition import component_rng
        for stream in ('deadlines', 'penalties'):
            def altered(seed, wave, component):
                return component_rng(seed + (1000 if component == stream else 0), wave, component)
            with patch('overseeing.competition_condition.component_rng', side_effect=altered):
                altered_scenario = generate_competition_scenario(300)
            self.assertEqual([(j.fault, j.public.clues) for j in baseline.jobs],
                             [(j.fault, j.public.clues) for j in altered_scenario.jobs])
            other = 'terminal_cost' if stream == 'deadlines' else 'deadline'
            self.assertEqual([getattr(j.public, other) for j in baseline.jobs],
                             [getattr(j.public, other) for j in altered_scenario.jobs])

    def test_matrix_has_identical_paired_scenarios_balanced_durations_and_all_assignments(self):
        config = load_competition_config()
        plan = episode_plan(config)
        self.assertEqual(len(plan), 192)
        self.assertEqual(sum(e['planned_calls'] for e in plan), 2304)
        first_durations = []
        per_agent = {a: set() for a in range(3)}
        for seed in range(300,316):
            runs = [e for e in plan if e['seed'] == seed]
            first_durations.append(runs[0]['review_ticks'])
            self.assertEqual(len({e['scenario_hash'] for e in runs}), 1)
            self.assertEqual(len({(e['policy'],e['review_ticks']) for e in runs}), 12)
            scenario = generate_competition_scenario(seed)
            for wave in (0,6):
                jobs = [j.public for j in scenario.jobs if j.public.release == wave]
                self.assertEqual(sorted(j.deadline-wave for j in jobs), [2,4,5])
                self.assertEqual(sorted(j.terminal_cost for j in jobs), [4,8,12])
                self.assertTrue(all(j.cost_per_tick == 0 for j in jobs))
                for j in jobs:
                    per_agent[j.agent_id].add(j.deadline-wave)
        self.assertEqual(first_durations.count(1), 8)
        self.assertEqual(first_durations.count(2), 8)
        self.assertTrue(all(windows == {2,4,5} for windows in per_agent.values()))
        self.assertEqual(len(STAGE1_POLICIES), 4)
        self.assertEqual(len(STAGE2_POLICIES), 5)

    def test_edf_guard_ties_equality_and_arithmetic_search_cases(self):
        a = ReviewRequest('A',0,0,2,0,4,2,.5,'reset_sensor')
        b = ReviewRequest('B',1,0,4,0,8,2,.5,'reset_sensor')
        c = ReviewRequest('C',2,0,5,0,12,2,.5,'reset_sensor')
        self.assertEqual(choose('edf',(c,b,a),0),'A')
        self.assertEqual(choose('edf',(replace(a,deadline=1),b),0),'B')
        self.assertEqual(choose('edf',(replace(a,job_id='Z',agent_id=1),a),0),'A')
        # At s=2 only two reviews fit. Search skips A to save B+C (20 > 16).
        self.assertEqual(choose('delay',(a,b,c),0),'B')
        self.assertEqual(choose('greedy',(a,b,c),0),'C')
        # At s=1 all three fit, with deterministic FCFS plan ties.
        self.assertEqual(choose('delay',tuple(replace(r,review_ticks=1) for r in (a,b,c)),0),'A')
        for tick in range(6):
            for duration in (1,2):
                requests = tuple(replace(r,review_ticks=duration) for r in (a,b,c))
                self.assertEqual(choose('myopic',requests,tick),choose('greedy',requests,tick))
        with tempfile.TemporaryDirectory() as tmp:
            scenario=Scenario(0,(PrivateJob(PublicJob('A',0,0,2,0,4,('filter','filter')),'filter'),))
            path=Path(tmp)/'events.jsonl'
            result=run_episode(scenario,'edf',StipulatedProposals({'A':'reset_sensor'}),path,review_ticks=2)
            self.assertEqual((result['total_loss'],result['corrections']),(0,1))
            self.assertEqual(replay_score(path)['status'],'verified')
            events=read_events(path)
            completion=next(i for i,e in enumerate(events) if e['event']=='review_completed')
            closure=next(i for i,e in enumerate(events) if e['event']=='job_closed')
            self.assertLess(completion,closure)

    def test_frozen_estimator_and_new_clock_do_not_extend_historical_commands(self):
        config=load_competition_config()
        estimator=load_frozen_estimator(FROZEN_ESTIMATOR,config)
        self.assertEqual(estimator.predict('replace_filter','replace_filter'),13/89)
        self.assertEqual(estimator.predict('replace_filter','reset_sensor'),18/98)
        with self.assertRaises(ValueError):
            load_frozen_estimator(FROZEN_ESTIMATOR,dict(config,estimator_file_sha256='wrong'))
        clock=json.loads((ROOT/'reports/implementation_clock.json').read_text())
        now=datetime(2026,9,10,3,30,tzinfo=timezone.utc)
        self.assertEqual(validate_deadline(None,clock,'stage3_competition',now).isoformat(),'2026-09-10T04:47:37+00:00')
        with self.assertRaises(ValueError):
            validate_deadline(None,clock,'stage2_development',now)
        with self.assertRaises(ValueError):
            validate_deadline('2026-09-10T04:47:38+00:00',clock,'stage3_competition',now)

    def test_full_synthetic_pipeline_and_audit_without_refitting_or_network(self):
        # Stipulated transport validates bookkeeping, not model quality; temporary evidence only.
        counter=[0]
        def transport(client,url,payload):
            if url.endswith('/tokenize'):
                return 200,'{"count":100}',None
            counter[0]+=1
            action='reset_sensor' if payload['seed']%2 else 'replace_filter'
            return 200,json.dumps({'id':'fixture-{}'.format(counter[0]),'choices':[{'finish_reason':'stop','message':{'content':json.dumps({'action':action})}}],
                                   'usage':{'prompt_tokens':100,'completion_tokens':7}}),None
        def gpu(pid,log,path):
            write_json(path,{'status':'placement_verified','model':'Qwen/Qwen2.5-7B-Instruct','revision':'a09a35458c702b33eeacc393d103063234e8bc28',
                'cuda_runtime':{'bf16_matmul_verified':True,'device_name':'NVIDIA RTX 6000 Ada Generation'},
                'server_arguments':{'--dtype':'bfloat16','--cpu-offload-gb':'0','--swap-space':'0','--tensor-parallel-size':'1','--max-num-seqs':'1'},
                'serving_gpu_processes':[['fixture','0','fixture','16000']]})
        def metrics(out,suffix):
            (out/('metrics_'+suffix+'.txt')).write_text('\n'.join('{}{{model="fixture"}} {}'.format(name,counter[0]*multiplier)
                for name,multiplier in (('vllm:request_success_total',1),('vllm:prompt_tokens_total',100),('vllm:generation_tokens_total',7))))
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'run'
            prepare_competition(out)
            args=SimpleNamespace(out=str(out),deadline_utc=None,server_pid=0,server_log='fixture')
            with patch('overseeing.competition.collect_evidence',side_effect=gpu), patch('overseeing.competition.server_snapshot',side_effect=metrics), \
                 patch('overseeing.competition.validate_deadline',return_value=datetime.now(timezone.utc)+timedelta(minutes=2)), \
                 patch.object(GPUClient,'_http',transport), patch('overseeing.estimator.fit_estimator',side_effect=AssertionError('Refitting forbidden')), patch('builtins.print'):
                result=run_competition(args)
                self.assertTrue(result['all_completed'])
                self.assertEqual(counter[0],2305)
                with self.assertRaises(FileExistsError):
                    run_competition(args)
                audit=analyze_competition(out)
                self.assertEqual(audit['completed_trace_replays'],192)
                self.assertTrue(audit['myopic_greedy_same_state_equivalence_verified'])


if __name__=='__main__':
    unittest.main()
