"""Focused estimator, information-boundary, scheduling, and bounded-plan checks."""
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from overseeing.cli import load_config, validate_deadline
from overseeing.development import episode_plan, load_development_config, prepare_development, run_development
from overseeing.development_analysis import analyze_development
from overseeing.client import GPUClient
from overseeing.domain import POLICIES, STAGE1_POLICIES, ReviewRequest, generate_scenario
from overseeing.estimator import AgreementEstimator, calibration_examples, fit_estimator
from overseeing.fixtures import cases
from overseeing.io import read_events, write_json
from overseeing.policies import choose
from overseeing.simulator import StipulatedProposals, run_episode

ROOT = Path(__file__).resolve().parent.parent


class EstimatorChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)

    def test_labels_use_initial_proposal_and_include_unreviewed_jobs(self):
        examples = []
        for name in ("correctable", "expiry"):
            scenario, actions, probabilities, _ = cases()[name]
            path = self.path / (name + ".jsonl")
            result = run_episode(scenario, "fcfs", StipulatedProposals(actions), path)
            examples.extend(calibration_examples(path))
            if name == "correctable":
                self.assertEqual(result["correct_jobs"], 1)
                self.assertEqual(result["corrections"], 1)
        self.assertEqual([e["initial_error"] for e in examples], [1, 1])
        self.assertEqual([e["reviewed"] for e in examples], [True, False])
        # Collected pairs remain available if later work in an episode failed.
        path = self.path / "correctable.jsonl"
        events = read_events(path)
        events[-1]["status"] = "failed"
        path.write_text("\n".join(json.dumps(e) for e in events) + "\n")
        self.assertEqual(calibration_examples(path)[0]["initial_error"], 1)

    def test_sparse_bin_falls_back_to_smoothed_pool_and_threshold_is_ten(self):
        examples = ([{"agreement": True, "initial_error": 0}] * 9 +
                    [{"agreement": False, "initial_error": 1}] * 10)
        fitted = fit_estimator(examples, {})
        self.assertEqual(fitted["pooled"]["probability"], 11 / 21)
        self.assertTrue(fitted["bins"]["agree"]["pooled_fallback"])
        self.assertEqual(fitted["bins"]["agree"]["probability"], 11 / 21)
        self.assertFalse(fitted["bins"]["disagree"]["pooled_fallback"])
        self.assertEqual(fitted["bins"]["disagree"]["probability"], 11 / 12)
        empty_bin = fit_estimator(examples[:9], {})
        self.assertTrue(empty_bin["bins"]["disagree"]["pooled_fallback"])
        with self.assertRaises(ValueError):
            fit_estimator([], {})

    def test_estimator_is_frozen_hash_checked_and_accepts_actions_only(self):
        fitted = fit_estimator([{"agreement": True, "initial_error": 1}], {})
        estimator = AgreementEstimator.from_record(fitted)
        before = estimator.predict("reset_sensor", "reset_sensor")
        with self.assertRaises(FrozenInstanceError):
            estimator.agree_probability = 0
        with self.assertRaises(TypeError):
            estimator.predict(generate_scenario(200).jobs[0], "reset_sensor")
        fitted["bins"]["agree"]["probability"] = 0
        self.assertEqual(estimator.predict("reset_sensor", "reset_sensor"), before)
        with self.assertRaises(ValueError):
            AgreementEstimator.from_record(fitted)

    def test_hidden_truth_cannot_change_predictions_or_scheduler_input(self):
        original = generate_scenario(200)
        mutated = replace(original, jobs=tuple(replace(j, fault="filter" if j.fault == "sensor" else "sensor")
                                               for j in original.jobs))
        estimator = AgreementEstimator(0.2, 0.8, "synthetic-test")
        records = []
        for index, scenario in enumerate((original, mutated)):
            seen = []
            def inspect(policy, pending, tick):
                seen.append((tick, pending))
                self.assertTrue(all(type(r) is ReviewRequest and r.p_error == 0.2 for r in pending))
                return None  # Remove feedback differences to isolate hidden-state leakage.
            with patch("overseeing.simulator.choose", side_effect=inspect):
                result = run_episode(scenario, "fcfs", StipulatedProposals({j.public.job_id: "reset_sensor" for j in scenario.jobs}),
                                     self.path / (str(index) + ".jsonl"), estimator=estimator)
            self.assertEqual(result["status"], "completed")
            records.append(seen)
        self.assertEqual(records[0], records[1])


class DevelopmentPlanChecks(unittest.TestCase):
    def test_one_shot_pipeline_with_synthetic_transport_freezes_before_validation(self):
        # All network/GPU calls are replaced; temporary files never become live evidence.
        counter = [0]
        def transport(client, url, payload):
            if url.endswith("/tokenize"):
                return 200, '{"count":100}', None
            counter[0] += 1
            action = "reset_sensor" if payload["seed"] % 2 else "replace_filter"
            return 200, json.dumps({"id": "synthetic-{}".format(counter[0]), "choices": [
                {"finish_reason": "stop", "message": {"content": json.dumps({"action": action})}}],
                "usage": {"prompt_tokens": 100, "completion_tokens": 7}}), None
        def gpu(pid, log, path):
            write_json(path, {"status": "placement_verified", "model": "Qwen/Qwen2.5-7B-Instruct",
                "revision": "a09a35458c702b33eeacc393d103063234e8bc28",
                "cuda_runtime": {"bf16_matmul_verified": True, "device_name": "NVIDIA RTX 6000 Ada Generation"},
                "server_arguments": {"--dtype": "bfloat16", "--cpu-offload-gb": "0", "--swap-space": "0",
                                     "--tensor-parallel-size": "1", "--max-num-seqs": "1"},
                "serving_gpu_processes": [["synthetic", "0", "synthetic", "16000"]]})
        def metrics(out, suffix):
            (out / ("metrics_" + suffix + ".txt")).write_text("\n".join(
                '{}{{model="synthetic"}} {}'.format(name, counter[0] * multiplier) for name, multiplier in
                (("vllm:request_success_total", 1), ("vllm:prompt_tokens_total", 100), ("vllm:generation_tokens_total", 7))))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run"
            prepare_development(out)
            args = SimpleNamespace(out=str(out), deadline_utc=None, server_pid=0, server_log="synthetic")
            with patch("overseeing.development.collect_evidence", side_effect=gpu), \
                 patch("overseeing.development.server_snapshot", side_effect=metrics), \
                 patch("overseeing.development.validate_deadline", return_value=datetime.now(timezone.utc) + timedelta(minutes=2)), \
                 patch.object(GPUClient, "_http", transport), patch("builtins.print"):
                result = run_development(args)
                self.assertTrue(result["all_completed"])
                self.assertEqual(counter[0], 673)
                with self.assertRaises(FileExistsError):
                    run_development(args)
            verification = analyze_development(out)
            self.assertEqual(verification["completed_trace_replays"], 56)
            self.assertTrue(verification["frozen_estimator_verified"])

    def test_fixed_scope_rotation_and_historical_policy_set(self):
        config = load_development_config()
        plan = episode_plan(config)
        self.assertEqual(len(plan), 56)
        self.assertEqual(sum(p["planned_calls"] for p in plan), 672)
        self.assertEqual([p["seed"] for p in plan[:16]], list(range(200, 216)))
        for index, seed in enumerate(range(216, 224)):
            policies = [p["policy"] for p in plan if p["phase"] == "validation" and p["seed"] == seed]
            shift = index % 5
            self.assertEqual(policies, list(POLICIES[shift:] + POLICIES[:shift]))
        self.assertEqual(load_config(ROOT / "configs/stage1.json")["policies"], list(STAGE1_POLICIES))
        clock = json.loads((ROOT / "reports/implementation_clock.json").read_text())
        self.assertEqual(validate_deadline(None, clock, "stage2_development",
            datetime(2026, 9, 10, 1, 10, tzinfo=timezone.utc)).isoformat(), "2026-09-10T03:07:01+00:00")

    def test_greedy_earliest_completion_rule_ties_and_competition(self):
        a = ReviewRequest("A", 0, 0, 2, 0, 8, 2, 0.5, "reset_sensor")
        b = ReviewRequest("B", 1, 0, 5, 0, 12, 2, 0.5, "reset_sensor")
        self.assertEqual(choose("greedy", (a, b), 0), "B")
        self.assertEqual(choose("delay", (a, b), 0), "A")
        self.assertEqual(choose("greedy", (replace(a, job_id="late", deadline=1),), 0), None)
        self.assertEqual(choose("greedy", (replace(a, job_id="second", agent_id=1), a), 0), "A")
        with tempfile.TemporaryDirectory() as tmp:
            scenario, actions, _, expected = cases()["competition"]
            for policy in ("greedy", "delay"):
                path = Path(tmp) / (policy + ".jsonl")
                result = run_episode(scenario, policy, StipulatedProposals(actions), path)
                self.assertEqual(result["total_loss"], expected[policy])
                first = next(e for e in read_events(path) if e["event"] == "review_started")
                self.assertEqual(first["job_id"], "B" if policy == "greedy" else "A")


if __name__ == "__main__":
    unittest.main()
