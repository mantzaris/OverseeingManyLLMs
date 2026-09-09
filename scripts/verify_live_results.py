#!/usr/bin/env python3
"""Audit saved live requests and traces without issuing any inference requests."""

import argparse
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from overseeing.cli import load_config
from overseeing.client import ACTION_SCHEMA, parse_action
from overseeing.domain import POLICIES, digest
from overseeing.io import read_events, write_json
from overseeing.replay import replay_score


def verify(folder):
    folder = Path(folder)
    manifest = json.loads((folder / "manifest.json").read_text())
    assert manifest["gpu_inference_succeeded"] and manifest["all_four_completed"]
    assert manifest["config"] == load_config(Path(__file__).resolve().parent.parent / "configs/stage1.json")
    assert manifest["config"]["p_error"] == 0.5
    root = Path(__file__).resolve().parent.parent
    for name, expected_hash in manifest["source_files_sha256"].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected_hash, name
    result = {"status": "verified", "policies": {}, "experimental_attempts": 0,
              "experimental_prompt_tokens": 0, "experimental_completion_tokens": 0,
              "experimental_scheduled_calls": 0, "retries": 0, "replays_verified": 0}
    intervals = []
    for policy in ("placement",) + POLICIES:
        path = folder / "placement_raw_requests.jsonl" if policy == "placement" else folder / policy / "raw_requests.jsonl"
        raw = read_events(path)
        finished = [r for r in raw if r["phase"] == "attempt_finished"]
        sent = [r for r in raw if r["phase"] == "inference_started"]
        calls = {}
        for r in finished:
            key = (r["job_id"], r["sample"])
            calls.setdefault(key, []).append(r)
            assert r["retry"] in (0, 1)
            metadata = {k: r[k] for k in ("scenario_seed", "agent_id", "job_id")}
            assert r["seed"] == int(digest(dict(metadata, sample=r["sample"], retry=r["retry"]))[:8], 16)
            assert r["observation_hash"] == digest(json.loads(r["request"]["messages"][1]["content"]))
            assert r["evidence"] == "live_l40s"
            for field, value in {"model": manifest["config"]["model"], "temperature": 0.3,
                                 "top_p": 1.0, "max_tokens": 48, "n": 1,
                                 "guided_json": ACTION_SCHEMA, "stream": False}.items():
                assert r["request"][field] == value
            if "parsed_action" in r:
                assert r["http_status"] == 200 and parse_action(r["raw_response"]) == r["parsed_action"]
            start = datetime.fromisoformat(r["wall_utc"])
            intervals.append((start, start + timedelta(seconds=r["attempt_wall_seconds"])))
        for attempts in calls.values():
            assert [r["retry"] for r in attempts] in ([0], [0, 1])
            assert "parsed_action" in attempts[-1]
        assert len(calls) == (1 if policy == "placement" else 12)
        counts = {"scheduled_calls": len(calls), "attempts": len(sent),
                  "retries": sum(r["retry"] > 0 for r in finished),
                  "prompt_tokens": sum((r.get("usage") or {}).get("prompt_tokens", 0) for r in finished),
                  "completion_tokens": sum((r.get("usage") or {}).get("completion_tokens", 0) for r in finished),
                  "unknown_token_attempts": sum(r["inference_request_attempted"] and r.get("usage") is None for r in finished)}
        if policy == "placement":
            recorded = manifest["placement"]
            result["placement"] = counts
        else:
            events = read_events(folder / policy / "events.jsonl")
            recorded = events[-1]
            assert recorded["event"] == "episode_finished" and recorded["status"] == "completed"
            assert recorded["simulated_ticks_completed"] == 12 and recorded["planned_calls"] == 12
            assert events[0]["review_ticks"] == 2 and events[0]["p_error"] == 0.5
            assert events[0]["scenario_hash"] == manifest["scenario_hash"]
            proposals = [e for e in events if e["event"] == "proposal"]
            assert len(proposals) == 6
            for e in proposals:
                primary, secondary = (calls[(e["job_id"], sample)][-1] for sample in (0, 1))
                assert primary["observation_hash"] == secondary["observation_hash"]
                assert e["primary"] == primary["parsed_action"] and e["secondary"] == secondary["parsed_action"]
                assert e["agreement"] == (e["primary"] == e["secondary"]) and e["p_error"] == 0.5
            replay = replay_score(folder / policy / "events.jsonl")
            assert replay["status"] == "verified"
            result["replays_verified"] += 1
            result["policies"][policy] = dict(counts, total_loss=replay["total_loss"], correct_jobs=replay["correct_jobs"])
            for field in ("scheduled_calls", "attempts", "prompt_tokens", "completion_tokens"):
                result["experimental_" + field] += counts[field]
            result["retries"] += counts["retries"]
        for field in ("scheduled_calls", "attempts", "prompt_tokens", "completion_tokens", "unknown_token_attempts"):
            assert counts[field] == recorded[field], (policy, field)
    intervals.sort()
    # Logs combine wall timestamps with monotonic durations; tolerate sub-ms clock resolution.
    assert all(a[1] <= b[0] + timedelta(milliseconds=1) for a, b in zip(intervals, intervals[1:]))
    result["serial_requests_verified"] = True
    assert result["experimental_scheduled_calls"] == 48
    assert result["experimental_attempts"] <= 96
    def metric(path, name):
        return sum(float(line.rsplit(" ", 1)[1]) for line in path.read_text().splitlines()
                   if line.startswith(name + "{"))
    for name, expected in {"vllm:request_success_total": result["experimental_attempts"] + result["placement"]["attempts"],
                           "vllm:prompt_tokens_total": result["experimental_prompt_tokens"] + result["placement"]["prompt_tokens"],
                           "vllm:generation_tokens_total": result["experimental_completion_tokens"] + result["placement"]["completion_tokens"]}.items():
        delta = metric(folder.parent / "metrics_after.txt", name) - metric(folder.parent / "metrics_before.txt", name)
        assert delta == expected, (name, delta, expected)
    result["server_metrics_verified"] = True
    result["source_hashes_verified"] = True
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder")
    parser.add_argument("--out")
    args = parser.parse_args()
    result = verify(args.folder)
    if args.out:
        write_json(args.out, result)
    print(json.dumps(result, indent=2, sort_keys=True))
