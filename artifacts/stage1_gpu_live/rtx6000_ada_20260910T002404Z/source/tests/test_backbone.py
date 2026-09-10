"""Focused mechanics/validity checks. No model, network, or GPU inference."""

from dataclasses import asdict, replace
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from overseeing.cli import load_config
from overseeing.client import GPUClient, parse_action
from overseeing.domain import POLICIES, PrivateJob, ReviewRequest, Scenario, generate_scenario, observation
from overseeing.fixtures import cases, job
from overseeing.gpu import collect_evidence
from overseeing.io import read_events
from overseeing.policies import choose
from overseeing.replay import replay_score
from overseeing.simulator import ProposalFailure, StipulatedProposals, run_episode

ROOT = Path(__file__).resolve().parent.parent


class BackboneChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)

    def fixture(self, name, policy="delay", filename="events.jsonl", **kwargs):
        scenario, actions, probabilities, _ = cases()[name]
        return run_episode(scenario, policy, StipulatedProposals(actions), self.path / filename,
                           fixture_probabilities=probabilities, **kwargs)

    def test_five_fixtures_all_four_policies_and_replay(self):
        for name, (_, _, _, expected) in cases().items():
            for policy in POLICIES:
                with self.subTest(fixture=name, policy=policy):
                    filename = name + "_" + policy + ".jsonl"
                    result = self.fixture(name, policy, filename)
                    self.assertEqual(result["status"], "completed", result["error"])
                    self.assertEqual(result["total_loss"], expected[policy])
                    self.assertEqual(result["attempts"], 0)
                    self.assertEqual(replay_score(self.path / filename)["total_loss"], expected[policy])

    def test_deadline_equality_saves_terminal_not_accrued_downtime(self):
        scenario = Scenario(-6, (job("boundary", 0, 2, 3, 8),))
        result = run_episode(scenario, "delay", StipulatedProposals({"boundary": "reset_sensor"}), self.path / "e.jsonl")
        self.assertEqual(result["total_loss"], 6)
        events = read_events(self.path / "e.jsonl")
        kinds = [e["event"] for e in events if e["tick"] == 2]
        self.assertLess(kinds.index("review_completed"), kinds.index("job_closed"))
        self.assertEqual(replay_score(self.path / "e.jsonl")["total_loss"], 6)

    def test_forced_late_review_does_not_reopen_or_erase_loss(self):
        result = self.fixture("expiry", fixture_dispatch=lambda requests, tick: requests[0].job_id if requests else None)
        self.assertEqual((result["total_loss"], result["late_returns"], result["corrections"]), (9, 1, 0))
        response = next(e for e in read_events(self.path / "events.jsonl") if e["event"] == "review_completed")
        self.assertEqual(response["tick"], 2)
        self.assertFalse(response["applied"])
        self.assertEqual(replay_score(self.path / "events.jsonl")["total_loss"], 9)

    def test_unreviewed_counterfactual_arithmetic(self):
        result = self.fixture("correctable", fixture_dispatch=lambda requests, tick: None)
        self.assertEqual(result["total_loss"], 13)

    def test_hidden_state_mutation_cannot_change_observations_or_scheduler_records(self):
        first = generate_scenario(100)
        second = replace(first, jobs=tuple(replace(j, fault="sensor" if j.fault == "filter" else "filter") for j in first.jobs))
        observed, scheduled = [], []
        for index, scenario in enumerate((first, second)):
            provider = StipulatedProposals({j.public.job_id: "replace_filter" for j in scenario.jobs})
            records = []
            def public_only(policy, pending, tick):
                for r in pending:
                    self.assertIs(type(r), ReviewRequest)
                    self.assertNotIn("fault", asdict(r))
                    self.assertNotIn("correct_action", asdict(r))
                records.append((tick, pending))
                return None  # No feedback, so changing truth must not alter later public histories.
            with patch("overseeing.simulator.choose", side_effect=public_only):
                run_episode(scenario, "fcfs", provider, self.path / (str(index) + ".jsonl"))
            observed.append(provider.observations)
            scheduled.append(records)
        self.assertEqual(observed[0], observed[1])
        self.assertEqual(scheduled[0], scheduled[1])
        with self.assertRaises(TypeError):
            observation(first.jobs[0], 0, [])
        with self.assertRaises(TypeError):
            choose("delay", (first.jobs[0],), 0)

    def test_agent_histories_are_isolated_and_reset_between_episodes(self):
        jobs = []
        for agent in (0, 1):
            for wave in (0, 1):
                initial = job("a{}j{}".format(agent, wave), agent, 2, 0, 8)
                jobs.append(replace(initial, public=replace(initial.public, release=6 * wave, deadline=6 * wave + 2)))
        scenario = Scenario(-7, tuple(jobs))
        provider = StipulatedProposals({j.public.job_id: "reset_sensor" for j in jobs})
        for run in range(2):
            run_episode(scenario, "fcfs", provider, self.path / (str(run) + ".jsonl"))
        for obs in provider.observations:
            if obs["tick"] == 0:
                self.assertEqual(obs["history"], [])
            for entry in obs["history"]:
                self.assertTrue(entry["job_id"].startswith("a{}j".format(obs["job"]["agent_id"])))
        first_agent_second_job = [o for o in provider.observations if o["job"]["job_id"] == "a0j1"]
        self.assertTrue(any("instructed_action" in e for e in first_agent_second_job[0]["history"]))
        self.assertEqual(provider.observations[:4], provider.observations[4:])

    def test_replay_detects_corrupt_score(self):
        self.fixture("correctable")
        path = self.path / "events.jsonl"
        events = read_events(path)
        events[-1]["total_loss"] = 999
        path.write_text("\n".join(json.dumps(e) for e in events) + "\n")
        with self.assertRaises(ValueError):
            replay_score(path)

    def test_future_jobs_are_absent_and_feedback_appears_only_at_completion(self):
        # Stipulated boundary probe: same agent observes just before and at completion.
        jobs = tuple(replace(job("probe{}".format(t), 0, 5 + t, 1, 8),
                             public=replace(job("probe{}".format(t), 0, 5 + t, 1, 8).public,
                                            release=t)) for t in range(3))
        scenario = Scenario(-8, jobs)
        provider = StipulatedProposals({j.public.job_id: "reset_sensor" for j in jobs})
        def inspect(policy, pending, tick):
            released = {j.public.job_id for j in jobs if j.public.release <= tick}
            self.assertTrue(all(r.job_id in released and r.requested_at <= tick for r in pending))
            return choose(policy, pending, tick)
        with patch("overseeing.simulator.choose", side_effect=inspect):
            result = run_episode(scenario, "fcfs", provider, self.path / "boundary.jsonl")
        self.assertEqual(result["status"], "completed")
        before, at_completion = provider.observations[1:]
        self.assertFalse(any("instructed_action" in e for e in before["history"]))
        feedback = [e for e in at_completion["history"] if "instructed_action" in e]
        self.assertEqual(len(feedback), 1)
        self.assertEqual(feedback[0]["review_completed_at"], 2)
        self.assertEqual(feedback[0]["instructed_action"], "replace_filter")

    def test_incomplete_episode_has_unknown_outcome(self):
        class FailingProvider(StipulatedProposals):
            def pair(self, obs, metadata):
                raise ProposalFailure("Stipulated transport failure; no inference")
        scenario = generate_scenario(100)
        result = run_episode(scenario, "fcfs", FailingProvider({}), self.path / "e.jsonl")
        self.assertEqual(result["status"], "failed")
        self.assertIsNone(result["total_loss"])
        self.assertIsNone(replay_score(self.path / "e.jsonl")["total_loss"])

    def test_gpu_gate_rejects_unsupported_hardware_before_any_request(self):
        with patch("overseeing.gpu.output", return_value="GPU-test, CPU substitute, 80000, 15000, 1, 0"):
            with self.assertRaises(RuntimeError):
                collect_evidence(1, self.path / "none.log", self.path / "gpu.json")
        self.assertEqual(json.loads((self.path / "gpu.json").read_text())["status"], "unverified")

    def test_cli_rejects_expanded_scenario_or_calibration(self):
        config = load_config(ROOT / "configs/stage1.json")
        for change in ({"seed": 101}, {"p_error": 0.2}, {"max_attempts_per_call": 3}):
            path = self.path / "config.json"
            path.write_text(json.dumps(dict(config, **change)))
            with self.assertRaises(ValueError):
                load_config(path)


class ResponseChecks(unittest.TestCase):
    """Synthetic HTTP responses in temporary files, never reported as GPU evidence."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "requests.jsonl"
        self.client = GPUClient(load_config(ROOT / "configs/stage1.json"), self.path,
                                datetime.now(timezone.utc) + timedelta(minutes=2))

    @staticmethod
    def response(content, finish="stop"):
        return json.dumps({"id": "synthetic-test-response", "choices": [{"finish_reason": finish,
            "message": {"content": content}}], "usage": {"prompt_tokens": 100, "completion_tokens": 10}})

    def test_retry_retains_malformed_output_and_accepts_valid_wrong_action(self):
        malformed = self.response('{"action":"replace_filter","action":"reset_sensor"}')
        valid_wrong = self.response('{"action":"reset_sensor"}')
        requests = []
        def transport(url, payload):
            requests.append(payload)
            if url.endswith("/tokenize"):
                return 200, '{"count":100}', None
            return 200, malformed if len(requests) == 2 else valid_wrong, None
        obs = {"job": {"clues": ["filter", "filter"]}, "history": []}
        with patch.object(self.client, "_http", side_effect=transport):
            action = self.client.action(obs, {"scenario_seed": 100, "agent_id": 0, "job_id": "test"}, 0)
        self.assertEqual(action, "reset_sensor")  # No correctness repair.
        self.assertEqual(self.client.stats()["attempts"], 2)
        self.assertEqual(self.client.stats()["prompt_tokens"], 200)
        finished = [r for r in read_events(self.path) if r["phase"] == "attempt_finished"]
        self.assertEqual(finished[0]["raw_response"], malformed)
        self.assertIn("error", finished[0])
        self.assertEqual(requests[1]["messages"][-1], requests[3]["messages"][-1])

    def test_two_calls_identical_observations_distinct_seeds_and_no_vote(self):
        payloads = []
        def transport(url, payload):
            if url.endswith("/tokenize"):
                return 200, '{"count":100}', None
            payloads.append(payload)
            action = "reset_sensor" if len(payloads) == 1 else "replace_filter"
            return 200, self.response(json.dumps({"action": action})), None
        with patch.object(self.client, "_http", side_effect=transport):
            pair = self.client.pair({"history": []}, {"scenario_seed": 100, "agent_id": 0, "job_id": "test"})
        self.assertEqual(pair, ("reset_sensor", "replace_filter"))
        self.assertEqual(payloads[0]["messages"], payloads[1]["messages"])
        self.assertNotEqual(payloads[0]["seed"], payloads[1]["seed"])
        self.assertEqual(self.client.stats()["scheduled_calls"], 2)

    def test_timeouts_stop_after_two_attempts_and_tokens_remain_unknown(self):
        def transport(url, payload):
            if url.endswith("/tokenize"):
                return 200, '{"count":100}', None
            raise TimeoutError("Synthetic test timeout")
        with patch.object(self.client, "_http", side_effect=transport):
            with self.assertRaises(ProposalFailure):
                self.client.action({}, {"scenario_seed": 100, "agent_id": 0, "job_id": "test"}, 0)
        self.assertEqual(self.client.stats()["attempts"], 2)
        self.assertEqual(self.client.stats()["unknown_token_attempts"], 2)
        finished = [r for r in read_events(self.path) if r["phase"] == "attempt_finished"]
        self.assertEqual(len(finished), 2)
        self.assertTrue(all(r["usage"] is None for r in finished))

    def test_tokenization_consumes_the_same_sixty_second_attempt_budget(self):
        current = [datetime.now(timezone.utc)]
        timeouts = []
        class Clock:
            @classmethod
            def now(cls, tz):
                return current[0]
        class Response:
            status, headers = 200, {}
            def __init__(self, body):
                self.body = body
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def read(self):
                return self.body.encode()
        def open_request(request, timeout):
            timeouts.append(timeout)
            if request.full_url.endswith("/tokenize"):
                current[0] += timedelta(seconds=40)  # Synthetic clock advance; no sleep/inference.
                return Response('{"count":100}')
            return Response(self.response('{"action":"reset_sensor"}'))
        with patch("overseeing.client.datetime", Clock), patch.object(self.client.opener, "open", side_effect=open_request):
            self.client.action({}, {"scenario_seed": 100, "agent_id": 0, "job_id": "test"}, 0)
        self.assertEqual(timeouts, [60.0, 20.0])


if __name__ == "__main__":
    unittest.main()
