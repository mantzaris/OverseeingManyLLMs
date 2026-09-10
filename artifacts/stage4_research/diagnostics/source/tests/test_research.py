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

if __name__=='__main__':unittest.main()
