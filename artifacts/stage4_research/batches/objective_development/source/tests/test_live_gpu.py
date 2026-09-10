"""Focused continuation authorization and verified GPU placement gates; no inference."""

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from overseeing.cli import validate_deadline
from overseeing.client import MODEL
from overseeing.gpu import REQUIRED_FLAGS, collect_evidence, validate_hardware

ROOT = Path(__file__).resolve().parent.parent


class ContinuationChecks(unittest.TestCase):
    def setUp(self):
        self.clock = json.loads((ROOT / "reports/implementation_clock.json").read_text())
        self.now = datetime(2026, 9, 9, 23, 50, tzinfo=timezone.utc)
        self.deadline = "2026-09-10T01:42:54+00:00"

    def check(self, deadline=None, stage="stage1_gpu_live"):
        return validate_deadline(deadline or self.deadline, self.clock, stage, self.now)

    def test_explicit_continuation_accepts_new_deadline_preserving_historical_cap(self):
        self.assertEqual(self.check().isoformat(), self.deadline)
        self.assertEqual(self.clock["stage1_deadline_utc"], "2026-09-09T19:38:57+00:00")
        with self.assertRaises(ValueError):
            self.check(stage=None)

    def test_rejects_expired_unknown_unzoned_and_extended_deadlines(self):
        for deadline in ("2026-09-09T23:49:00+00:00", "2026-09-10T01:42:55+00:00",
                         "2026-09-10T01:00:00"):
            with self.subTest(deadline=deadline), self.assertRaises(ValueError):
                self.check(deadline)
        with self.assertRaises(ValueError):
            self.check(stage="unrecorded")

    def test_continuation_cannot_exceed_two_hours_or_overall_cap(self):
        original = deepcopy(self.clock)
        self.clock["continuation_stages"][0]["deadline_utc"] = "2026-09-10T02:00:00+00:00"
        with self.assertRaises(ValueError):
            self.check()

        self.clock = original
        self.clock["overall_deadline_utc"] = "2026-09-10T00:30:00+00:00"
        with self.assertRaises(ValueError):
            self.check()

    def test_ada_continuation_uses_its_own_record_without_resetting_prior_clocks(self):
        now = datetime(2026, 9, 10, 0, 40, tzinfo=timezone.utc)
        deadline = validate_deadline(None, self.clock, "stage1_gpu_live_rtx6000_ada", now)
        self.assertEqual(deadline.isoformat(), "2026-09-10T02:24:04+00:00")
        self.assertEqual(self.clock["overall_deadline_utc"], "2026-09-11T03:38:57+00:00")
        self.assertEqual(self.clock["continuation_stages"][0]["deadline_utc"], self.deadline)
        with self.assertRaises(ValueError):
            validate_deadline("2026-09-10T02:24:05+00:00", self.clock,
                              "stage1_gpu_live_rtx6000_ada", now)


class PlacementChecks(unittest.TestCase):
    def test_supported_gpu_memory_and_single_gpu_required(self):
        row = ["GPU-test", "NVIDIA L40S", "46068"]
        validate_hardware([row])
        validate_hardware([["GPU-test", "NVIDIA RTX 6000 Ada Generation", "49140"]])
        for rows in ([], [row, row], [["GPU-test", "NVIDIA A100", "80000"]],
                     [["GPU-test", "NVIDIA RTX 6000 Ada Generation", "16000"]],
                     [["GPU-test", "NVIDIA L40S", "16000"]]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                validate_hardware(rows)

    def test_placement_requires_cuda_bf16_resident_server_and_zero_offload(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "server.log"
            evidence = Path(tmp) / "evidence.json"
            args = ["vllm", "serve", MODEL, "--enforce-eager", "--port", "8000"]
            for flag, value in REQUIRED_FLAGS.items():
                args.extend([flag, value])
            gpu = "GPU-test, NVIDIA RTX 6000 Ada Generation, 49140, 24000, 580.126.20, 0"
            process = "GPU-test, 42, vllm, 22000"
            for case in ("valid", "cpu_offload", "swap", "revision", "no_bf16", "no_cuda_log", "unrelated_process", "small_allocation"):
                with self.subTest(case=case):
                    actual_args = list(args)
                    if case == "cpu_offload":
                        actual_args[actual_args.index("--cpu-offload-gb") + 1] = "1"
                    if case == "swap":
                        actual_args[actual_args.index("--swap-space") + 1] = "4"
                    if case == "revision":
                        actual_args[actual_args.index("--revision") + 1] = "main"
                    log.write_text({"no_bf16": "CUDA model loading", "no_cuda_log": "bfloat16 model loading"}
                                   .get(case, "CUDA model loading dtype=torch.bfloat16"))
                    proc = process if case != "small_allocation" else "GPU-test, 42, vllm, 1000"
                    with patch("overseeing.gpu.output", side_effect=[gpu, proc]), \
                         patch("overseeing.gpu.cuda_runtime_evidence", return_value={"bf16_matmul_verified": True}), \
                         patch("pathlib.Path.read_bytes", return_value="\0".join(actual_args).encode()), \
                         patch("overseeing.gpu.os.readlink", return_value="/test/python"), \
                         patch("overseeing.gpu.platform.platform", return_value="synthetic-test"), \
                         patch("overseeing.gpu.descendant", return_value=case != "unrelated_process"), \
                         patch("overseeing.gpu.importlib.metadata.version", return_value="synthetic-test"):
                        if case == "valid":
                            self.assertEqual(collect_evidence(42, log, evidence)["status"], "placement_verified")
                        else:
                            with self.assertRaises(RuntimeError):
                                collect_evidence(42, log, evidence)


if __name__ == "__main__":
    unittest.main()
