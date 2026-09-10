"""Offline verification and descriptive development diagnostics; never calls a model."""

from datetime import datetime, timedelta
import json
from pathlib import Path

from .client import ACTION_SCHEMA, MANUAL, parse_action
from .domain import POLICIES, ReviewRequest, digest
from .estimator import AgreementEstimator, calibration_examples, file_hash, fit_estimator
from .io import read_events, write_csv, write_json
from .policies import choose
from .replay import replay_score


def audit_requests(path, config, expected_seed):
    raw = read_events(path) if path.exists() else []
    finished = [r for r in raw if r["phase"] == "attempt_finished"]
    sent = [r for r in raw if r["phase"] == "inference_started"]
    started = [r for r in raw if r["phase"] == "attempt_started"]
    assert len(started) == len(finished), "Unfinished attempt retained: inspect raw log"
    calls, intervals = {}, []
    for r in finished:
        assert r["scenario_seed"] == expected_seed
        assert r["sample"] in (0, 1, "placement") and r["retry"] in (0, 1)
        metadata = {k: r[k] for k in ("scenario_seed", "agent_id", "job_id")}
        assert r["seed"] == int(digest(dict(metadata, sample=r["sample"], retry=r["retry"]))[:8], 16)
        assert r["request"]["seed"] == r["seed"]
        assert r["observation_hash"] == digest(json.loads(r["request"]["messages"][1]["content"]))
        for key, value in {"model": config["model"], "temperature": 0.3, "top_p": 1.0, "max_tokens": 48,
                           "guided_json": ACTION_SCHEMA, "n": 1, "stream": False}.items():
            assert r["request"][key] == value
        assert r["request"]["messages"][0]["content"] == MANUAL + (
            " Strictly follow the one-field JSON schema; include no prose." if r["retry"] else "")
        if "parsed_action" in r:
            assert parse_action(r["raw_response"]) == r["parsed_action"] and r["http_status"] == 200
        calls.setdefault((r["job_id"], r["sample"]), []).append(r)
        start = datetime.fromisoformat(r["wall_utc"])
        intervals.append((start, start + timedelta(seconds=r["attempt_wall_seconds"])))
    for attempts in calls.values():
        assert [r["retry"] for r in attempts] in ([0], [0, 1])
    counts = {"scheduled_calls": len(calls), "attempts": len(sent),
              "retries": sum(r["retry"] > 0 for r in finished),
              "failed_attempts": sum("error" in r for r in finished),
              "prompt_tokens": sum((r.get("usage") or {}).get("prompt_tokens", 0) for r in finished),
              "completion_tokens": sum((r.get("usage") or {}).get("completion_tokens", 0) for r in finished),
              "unknown_token_attempts": sum(r["inference_request_attempted"] and r.get("usage") is None for r in finished)}
    assert len(sent) == sum(r["inference_request_attempted"] for r in finished)
    return counts, calls, intervals


def analyze_development(path):
    out = Path(path)
    declaration = json.loads((out / "declaration.json").read_text())
    manifest = json.loads((out / "manifest.json").read_text())
    assert digest({k: v for k, v in declaration.items() if k != "declaration_hash"}) == declaration["declaration_hash"]
    assert manifest["declaration_hash"] == declaration["declaration_hash"]
    for name, expected in declaration["source_files_sha256"].items():
        assert file_hash(out / "source" / name) == expected, name
    assert declaration["config"]["calibration_seeds"] == list(range(200, 216))
    assert declaration["config"]["validation_seeds"] == list(range(216, 224))
    assert declaration["config"]["policies"] == list(POLICIES)
    for name in ("gpu_before.json", "gpu_after_placement.json", "gpu_final.json"):
        gpu_path = out / name
        if not gpu_path.exists():
            assert not manifest["all_completed"]
            continue
        gpu = json.loads(gpu_path.read_text())
        assert gpu["status"] == "placement_verified"
        assert gpu["model"] == declaration["runtime_config"]["model"]
        assert gpu["revision"] == declaration["runtime_config"]["revision"]
        assert gpu["cuda_runtime"]["bf16_matmul_verified"]
        assert gpu["cuda_runtime"]["device_name"] == "NVIDIA RTX 6000 Ada Generation"
        for flag, value in (("--dtype", "bfloat16"), ("--cpu-offload-gb", "0"), ("--swap-space", "0"),
                            ("--tensor-parallel-size", "1"), ("--max-num-seqs", "1")):
            assert gpu["server_arguments"][flag] == value
        assert sum(float(p[3]) for p in gpu["serving_gpu_processes"]) >= 14000
    fitted = json.loads((out / "estimator.json").read_text()) if (out / "estimator.json").exists() else None
    estimator = AgreementEstimator.from_record(fitted) if fitted else None
    if estimator:
        assert file_hash(out / "estimator.json") == manifest["estimator_file_sha256"]
        assert estimator.estimator_hash == manifest["estimator_hash"]
        assert fitted["provenance"]["seeds"] == list(range(200, 216))
        for provenance in fitted["provenance"]["episodes"]:
            events_path = out / provenance["events"]
            assert file_hash(events_path) == provenance["events_sha256"]
            assert file_hash(events_path.parent / "raw_requests.jsonl") == provenance["raw_requests_sha256"]
    placement, _, intervals = audit_requests(out / "placement_raw_requests.jsonl", declaration["runtime_config"], 200)
    assert placement["attempts"] <= 1 and placement["scheduled_calls"] <= 1
    episodes, calibration, predictions, dispatches, orders = [], [], [], [], []
    replay_count = 0
    for entry in declaration["episodes"]:
        folder = out / entry["folder"]
        events = read_events(folder / "events.jsonl")
        counts, calls, episode_intervals = audit_requests(folder / "raw_requests.jsonl", declaration["runtime_config"], entry["seed"])
        intervals.extend(episode_intervals)
        assert counts["scheduled_calls"] <= 12 and counts["attempts"] <= 24
        first, last = events[0], events[-1]
        completed = last.get("status") == "completed"
        if first["event"] == "episode_started":
            assert first["scenario_hash"] == entry["scenario_hash"] and first["review_ticks"] == 2
            assert first["scenario"]["seed"] == entry["seed"] and first["policy"] == entry["policy"]
            for field in ("scheduled_calls", "attempts", "prompt_tokens", "completion_tokens", "unknown_token_attempts"):
                assert counts[field] == last[field], (entry, field)
            if entry["phase"] == "validation":
                assert estimator is not None and first["estimator_hash"] == estimator.estimator_hash
                assert first["wall_utc"] >= fitted["fitted_utc"]
            else:
                assert first["p_error"] == 0.5 and first["estimator_hash"] is None
                if fitted:
                    assert last["wall_utc"] <= fitted["fitted_utc"]
            for e in events:
                if e["event"] != "proposal":
                    continue
                a, b = (calls[(e["job_id"], sample)][-1] for sample in (0, 1))
                assert a["observation_hash"] == b["observation_hash"]
                assert e["primary"] == a["parsed_action"] and e["secondary"] == b["parsed_action"]
                assert e["agreement"] == (e["primary"] == e["secondary"])
                expected_p = 0.5 if entry["phase"] == "calibration" else estimator.predict(e["primary"], e["secondary"])
                assert e["p_error"] == expected_p
            replay = replay_score(folder / "events.jsonl")
            if completed:
                assert replay["status"] == "verified" and counts["scheduled_calls"] == 12
                replay_count += 1
            else:
                assert replay["total_loss"] is None
        episode = dict(entry, **{k: last.get(k) for k in ("status", "total_loss", "accrued_loss", "loss_upper_bound",
                    "correct_jobs", "reviews_completed", "corrections", "expired_requests", "late_returns")})
        episode.update(counts)
        episodes.append(episode)
        examples = calibration_examples(folder / "events.jsonl")
        if entry["phase"] == "calibration":
            calibration.extend(examples)
            continue
        for example in examples:
            example["bin"] = "agree" if example["agreement"] else "disagree"
            error = example["initial_error"]
            example.update(brier_frozen=(example["p_error"] - error) ** 2, brier_constant=(0.5 - error) ** 2,
                           pooled_prediction=fitted["pooled"]["probability"],
                           brier_pooled=(fitted["pooled"]["probability"] - error) ** 2)
            predictions.append(example)
        review_order = [(e["tick"], e["job_id"]) for e in events if e["event"] == "review_started"]
        orders.append(dict(seed=entry["seed"], policy=entry["policy"], status=episode["status"],
                           review_order=[job for _, job in review_order], timed_order=review_order))
        for e in events:
            if e["event"] != "dispatch_considered":
                continue
            requests = tuple(ReviewRequest(**r) for r in e["eligible"])
            choices = {p: choose(p, requests, e["tick"]) for p in POLICIES}
            assert choices[entry["policy"]] == e["selected"]
            dispatches.append(dict(seed=entry["seed"], policy=entry["policy"], tick=e["tick"],
                eligible_count=len(requests), selected=e["selected"],
                any_policy_disagreement=len(set(choices.values())) > 1,
                search_greedy_disagreement=choices["delay"] != choices["greedy"], **{"choice_" + p: c for p, c in choices.items()}))
        episode["expired_opportunities"] = sum(e["event"] == "request_expired" and
            e.get("category") == "opportunity_lost_while_waiting" for e in events)
        episode["wrong_expired_opportunities"] = sum(e["event"] == "request_expired" and
            e.get("category") == "opportunity_lost_while_waiting" and e["initial_proposal_wrong"] for e in events)
    if fitted:
        refit = fit_estimator(calibration, {})
        assert refit["bins"] == fitted["bins"] and refit["pooled"] == fitted["pooled"]
    intervals.sort()
    assert all(a[1] <= b[0] + timedelta(milliseconds=1) for a, b in zip(intervals, intervals[1:])), "Overlapping requests"
    diagnostics, outcomes, paired, pair_summaries, competition = [], [], [], [], []
    for policy in POLICIES:
        for group in ("all", "agree", "disagree"):
            selected = [p for p in predictions if p["policy"] == policy and (group == "all" or p["bin"] == group)]
            n = len(selected)
            diagnostics.append(dict(policy=policy, bin=group, examples=n,
                initial_errors=sum(p["initial_error"] for p in selected),
                initial_error_rate=sum(p["initial_error"] for p in selected) / n if n else None,
                **{key: sum(p[key] for p in selected) / n if n else None for key in ("brier_frozen", "brier_constant", "brier_pooled")}))
        selected = [e for e in episodes if e["phase"] == "validation" and e["policy"] == policy]
        complete = [e for e in selected if e["status"] == "completed"]
        decisions = [d for d in dispatches if d["policy"] == policy and d["eligible_count"] > 0]
        outcomes.append(dict(policy=policy, planned_episodes=8, completed_episodes=len(complete),
            incomplete_episodes=8-len(complete), **{key: sum(e[key] for e in complete) for key in
            ("total_loss", "correct_jobs", "reviews_completed", "corrections", "expired_requests", "expired_opportunities", "wrong_expired_opportunities", "late_returns")},
            dispatch_opportunities=len(decisions), competing_dispatches=sum(d["eligible_count"] >= 2 for d in decisions),
            same_queue_search_greedy_disagreements=sum(d["search_greedy_disagreement"] for d in decisions)))
    by_run = {(e["seed"], e["policy"]): e for e in episodes if e["phase"] == "validation"}
    for seed in range(216, 224):
        selected = [o for o in orders if o["seed"] == seed and o["status"] == "completed"]
        competition.append(dict(seed=seed, completed_policies=len(selected),
            unique_observed_review_orders=len({tuple(o["review_order"]) for o in selected}),
            any_competing_dispatch=any(d["seed"] == seed and d["eligible_count"] >= 2 for d in dispatches)))
    for index, left in enumerate(POLICIES):
        for right in POLICIES[:index]:
            comparisons = []
            for seed in range(216, 224):
                a, b = by_run[(seed, left)], by_run[(seed, right)]
                difference = a["total_loss"] - b["total_loss"] if a["status"] == b["status"] == "completed" else None
                row = dict(seed=seed, left=left, right=right, loss_difference=difference,
                    lower_bound=(a["accrued_loss"] or 0) - b["loss_upper_bound"],
                    upper_bound=a["loss_upper_bound"] - (b["accrued_loss"] or 0))
                if difference is not None:
                    row.update(lower_bound=difference, upper_bound=difference)
                    comparisons.append(difference)
                paired.append(row)
            pair_summaries.append(dict(left=left, right=right, completed_scenario_pairs=len(comparisons),
                mean_loss_difference=sum(comparisons) / len(comparisons) if comparisons else None,
                left_lower_loss=sum(x < 0 for x in comparisons), ties=sum(x == 0 for x in comparisons),
                left_higher_loss=sum(x > 0 for x in comparisons)))
    totals = {key: sum(e[key] for e in episodes) for key in ("scheduled_calls", "attempts", "retries", "failed_attempts", "prompt_tokens", "completion_tokens", "unknown_token_attempts")}
    assert totals["scheduled_calls"] <= 672 and totals["attempts"] <= 1344
    for key in ("scheduled_calls", "attempts", "prompt_tokens", "completion_tokens", "unknown_token_attempts"):
        assert totals[key] == manifest["experimental_" + key]
    def metric(suffix, name):
        path = out / ("metrics_" + suffix + ".txt")
        return sum(float(line.rsplit(" ", 1)[1]) for line in path.read_text().splitlines() if line.startswith(name + "{"))
    metrics_verified = None
    if not totals["failed_attempts"] and not placement["failed_attempts"] and (out / "metrics_after.txt").exists():
        for name, key in (("vllm:request_success_total", "attempts"), ("vllm:prompt_tokens_total", "prompt_tokens"),
                          ("vllm:generation_tokens_total", "completion_tokens")):
            assert metric("after", name) - metric("before", name) == totals[key] + placement[key]
        metrics_verified = True
    summary = {"status": "verified", "completed_trace_replays": replay_count, "planned_episodes": 56,
               "independent_validation_scenarios": 8, "experimental": totals, "placement": placement,
               "calibration_bins": fitted["bins"] if fitted else None, "estimator_hash": manifest["estimator_hash"],
               "frozen_estimator_verified": estimator is not None, "serial_requests_verified": True,
               "server_metrics_verified": metrics_verified, "policy_outcomes": outcomes,
               "paired_comparisons": pair_summaries, "competition_by_seed": competition,
               "note": "Development diagnostics on observed trajectories; policy repetitions are not independent scenarios."}
    for name, records in (("prediction_diagnostics", diagnostics), ("validation_predictions", predictions),
                          ("policy_outcomes", outcomes), ("paired_scenario_differences", paired),
                          ("paired_comparisons", pair_summaries), ("dispatch_opportunities", dispatches),
                          ("review_orders", orders), ("competition_by_seed", competition)):
        write_csv(out / (name + ".csv"), records)
    write_json(out / "diagnostics.json", summary)
    return summary
