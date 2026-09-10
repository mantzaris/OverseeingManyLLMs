"""Offline audit and paired diagnostics of the constructed condition; zero inference."""

from datetime import datetime, timedelta
from itertools import combinations
import json
from pathlib import Path

from .competition import ANALYSIS_DEFINITIONS, FIXED_CONFIG, episode_plan, load_frozen_estimator
from .competition_condition import GENERATOR_SPEC, generate_competition_scenario
from .development_analysis import audit_requests
from .domain import ReviewRequest, STAGE3_POLICIES, digest
from .estimator import calibration_examples, file_hash
from .io import read_events, write_csv, write_json
from .policies import choose
from .replay import replay_score


COUNT_FIELDS = ("scheduled_calls", "attempts", "retries", "failed_attempts", "prompt_tokens",
                "completion_tokens", "unknown_token_attempts")
OUTCOME_FIELDS = ("total_loss", "correct_jobs", "reviews_completed", "corrections", "expired_requests",
                  "expired_opportunities", "wrong_expired_opportunities", "late_returns")


def analyze_competition(path):
    out = Path(path)
    declaration = json.loads((out / "declaration.json").read_text())
    manifest = json.loads((out / "manifest.json").read_text())
    config = declaration["config"]
    assert config == FIXED_CONFIG and declaration["generator_spec"] == GENERATOR_SPEC
    assert declaration["episodes"] == episode_plan(config)
    assert declaration["config_hash"] == digest(config)
    assert declaration["runtime_config_hash"] == digest(declaration["runtime_config"])
    assert declaration["analysis_definitions"] == ANALYSIS_DEFINITIONS
    assert digest({k: v for k, v in declaration.items() if k != "declaration_hash"}) == declaration["declaration_hash"]
    assert manifest["declaration_hash"] == declaration["declaration_hash"]
    assert declaration["prepared_utc"] <= manifest["started_utc"]
    for name, expected in declaration["source_files_sha256"].items():
        assert file_hash(out / "source" / name) == expected, name
    scenarios = json.loads((out / "scenarios.scorer-only.json").read_text())
    assert scenarios == {str(seed): json.loads(json.dumps(generate_competition_scenario(seed).record())) for seed in config["seeds"]}
    estimator = load_frozen_estimator(out / "estimator.json", config)
    assert manifest["estimator_hash"] == declaration["estimator_hash"] == estimator.estimator_hash
    assert manifest["estimator_file_sha256"] == declaration["estimator_file_sha256"] == file_hash(out / "estimator.json")
    for name in ("gpu_before.json", "gpu_after_placement.json", "gpu_final.json"):
        if not (out / name).exists():
            assert not manifest["all_completed"]
            continue
        gpu = json.loads((out / name).read_text())
        assert gpu["status"] == "placement_verified"
        assert gpu["model"] == declaration["runtime_config"]["model"]
        assert gpu["revision"] == declaration["runtime_config"]["revision"]
        assert gpu["cuda_runtime"]["bf16_matmul_verified"]
        assert gpu["cuda_runtime"]["device_name"] == "NVIDIA RTX 6000 Ada Generation"
        for flag, value in (("--dtype", "bfloat16"), ("--cpu-offload-gb", "0"), ("--swap-space", "0"),
                            ("--tensor-parallel-size", "1"), ("--max-num-seqs", "1")):
            assert gpu["server_arguments"][flag] == value
        assert sum(float(p[3]) for p in gpu["serving_gpu_processes"]) >= 14000
    placement, _, intervals = audit_requests(out / "placement_raw_requests.jsonl", declaration["runtime_config"], 300)
    assert placement["scheduled_calls"] <= 1 and placement["attempts"] <= 1 and placement["retries"] == 0
    episodes, predictions, dispatches, orders, replays = [], [], [], [], 0
    for entry in declaration["episodes"]:
        folder = out / entry["folder"]
        events = read_events(folder / "events.jsonl")
        counts, calls, times = audit_requests(folder / "raw_requests.jsonl", declaration["runtime_config"], entry["seed"])
        intervals.extend(times)
        first, last = events[0], events[-1]
        complete = last.get("status") == "completed"
        assert counts["scheduled_calls"] <= 12 and counts["attempts"] <= 24
        if first["event"] != "run_blocked":
            assert first["scenario_hash"] == entry["scenario_hash"] == digest(first["scenario"])
            assert first["scenario"] == scenarios[str(entry["seed"])]
            assert first["review_ticks"] == entry["review_ticks"] and first["policy"] == entry["policy"]
            assert first["estimator_hash"] == estimator.estimator_hash
            assert declaration["prepared_utc"] <= first["wall_utc"] <= manifest["deadline_utc"]
            for key in ("scheduled_calls", "attempts", "prompt_tokens", "completion_tokens", "unknown_token_attempts"):
                assert counts[key] == last[key], (entry, key)
            for event in events:
                if event["event"] != "proposal":
                    continue
                a, b = (calls[(event["job_id"], sample)][-1] for sample in (0, 1))
                assert a["observation_hash"] == b["observation_hash"]
                assert event["primary"] == a["parsed_action"] and event["secondary"] == b["parsed_action"]
                assert event["agreement"] == (event["primary"] == event["secondary"])
                assert event["p_error"] == estimator.predict(event["primary"], event["secondary"])
            replay = replay_score(folder / "events.jsonl")
            if complete:
                assert replay["status"] == "verified" and counts["scheduled_calls"] == 12
                replays += 1
            else:
                assert replay["total_loss"] is None
        episode = dict(entry, **{k: last.get(k) for k in ("status", "total_loss", "accrued_loss", "loss_upper_bound",
            "correct_jobs", "reviews_completed", "corrections", "expired_requests", "late_returns")}, **counts)
        episode["expired_opportunities"] = sum(e["event"] == "request_expired" and e.get("category") == "opportunity_lost_while_waiting" for e in events)
        episode["wrong_expired_opportunities"] = sum(e["event"] == "request_expired" and e.get("category") == "opportunity_lost_while_waiting" and e["initial_proposal_wrong"] for e in events)
        episodes.append(episode)
        for example in calibration_examples(folder / "events.jsonl"):
            # This helper extracts pre-correction truth offline; no estimator fitting occurs.
            example.update(review_ticks=entry["review_ticks"], bin="agree" if example["agreement"] else "disagree",
                           brier_frozen=(example["p_error"] - example["initial_error"]) ** 2)
            predictions.append(example)
        review_order = [(e["tick"], e["job_id"]) for e in events if e["event"] == "review_started"]
        orders.append(dict(seed=entry["seed"], review_ticks=entry["review_ticks"], policy=entry["policy"],
                           status=episode["status"], review_order=[job for _, job in review_order], timed_order=review_order))
        for event in events:
            if event["event"] != "dispatch_considered":
                continue
            requests = tuple(ReviewRequest(**r) for r in event["eligible"])
            choices = {p: choose(p, requests, event["tick"]) for p in STAGE3_POLICIES}
            assert choices[entry["policy"]] == event["selected"]
            assert all(r.cost_per_tick == 0 for r in requests)
            assert choices["myopic"] == choices["greedy"], "Terminal-only equivalence failed"
            dispatches.append(dict(seed=entry["seed"], review_ticks=entry["review_ticks"], policy=entry["policy"],
                tick=event["tick"], eligible_count=len(requests), selected=event["selected"],
                search_greedy_disagreement=choices["delay"] != choices["greedy"],
                search_edf_disagreement=choices["delay"] != choices["edf"],
                **{"choice_" + p: value for p, value in choices.items()}))
    intervals.sort()
    assert all(a[1] <= b[0] + timedelta(milliseconds=1) for a, b in zip(intervals, intervals[1:])), "Overlapping generations"
    outcomes, diagnostics, paired, comparisons, sequence_comparisons = [], [], [], [], []
    by_run = {(e["seed"], e["review_ticks"], e["policy"]): e for e in episodes}
    by_order = {(o["seed"], o["review_ticks"], o["policy"]): o for o in orders}
    for duration in (1, 2):
        for policy in STAGE3_POLICIES:
            selected = [e for e in episodes if e["review_ticks"] == duration and e["policy"] == policy]
            completed = [e for e in selected if e["status"] == "completed"]
            decisions = [d for d in dispatches if d["review_ticks"] == duration and d["policy"] == policy and d["eligible_count"] > 0]
            outcomes.append(dict(review_ticks=duration, policy=policy, planned_episodes=16, completed_episodes=len(completed),
                incomplete_episodes=16-len(completed), **{key: sum(e[key] for e in completed) for key in OUTCOME_FIELDS},
                mean_loss=sum(e["total_loss"] for e in completed)/len(completed) if completed else None,
                dispatch_opportunities=len(decisions), competing_dispatches=sum(d["eligible_count"] >= 2 for d in decisions),
                same_state_search_greedy_differences=sum(d["search_greedy_disagreement"] for d in decisions),
                same_state_search_edf_differences=sum(d["search_edf_disagreement"] for d in decisions)))
            for group in ("all", "agree", "disagree"):
                examples = [e for e in predictions if e["review_ticks"] == duration and e["policy"] == policy and (group == "all" or e["bin"] == group)]
                n = len(examples)
                errors = sum(e["initial_error"] for e in examples)
                diagnostics.append(dict(review_ticks=duration, policy=policy, bin=group, examples=n, initial_errors=errors,
                    initial_error_rate=errors/n if n else None, brier_frozen=sum(e["brier_frozen"] for e in examples)/n if n else None))
        for right, left in combinations(STAGE3_POLICIES, 2):
            differences, order_differences = [], []
            for seed in config["seeds"]:
                a, b = by_run[(seed, duration, left)], by_run[(seed, duration, right)]
                complete = a["status"] == b["status"] == "completed"
                difference = a["total_loss"] - b["total_loss"] if complete else None
                row = dict(seed=seed, review_ticks=duration, left=left, right=right, loss_difference=difference,
                    lower_bound=(a["accrued_loss"] or 0)-b["loss_upper_bound"],
                    upper_bound=a["loss_upper_bound"]-(b["accrued_loss"] or 0))
                if complete:
                    row.update(lower_bound=difference, upper_bound=difference)
                    differences.append(difference)
                paired.append(row)
                different_order = (by_order[(seed, duration, left)]["review_order"] != by_order[(seed, duration, right)]["review_order"]) if complete else None
                sequence_comparisons.append(dict(seed=seed, review_ticks=duration, left=left, right=right, different_order=different_order))
                if complete:
                    order_differences.append(different_order)
            comparisons.append(dict(review_ticks=duration, left=left, right=right, completed_pairs=len(differences),
                total_loss_difference=sum(differences), mean_loss_difference=sum(differences)/len(differences) if differences else None,
                left_wins=sum(d < 0 for d in differences), ties=sum(d == 0 for d in differences), left_losses=sum(d > 0 for d in differences),
                actual_order_differences=sum(order_differences)))
    totals = {key: sum(e[key] for e in episodes) for key in COUNT_FIELDS}
    assert totals["scheduled_calls"] <= 2304 and totals["attempts"] <= 4608
    for key in ("scheduled_calls", "attempts", "prompt_tokens", "completion_tokens", "unknown_token_attempts"):
        assert totals[key] == manifest["experimental_" + key]
    assert manifest["all_completed"] == (replays == 192)
    metrics_verified = None
    if not totals["failed_attempts"] and not placement["failed_attempts"] and (out / "metrics_after.txt").exists():
        def metric(suffix, name):
            return sum(float(line.rsplit(" ", 1)[1]) for line in (out / ("metrics_" + suffix + ".txt")).read_text().splitlines() if line.startswith(name + "{"))
        for name, key in (("vllm:request_success_total", "attempts"), ("vllm:prompt_tokens_total", "prompt_tokens"), ("vllm:generation_tokens_total", "completion_tokens")):
            assert metric("after", name)-metric("before", name) == totals[key]+placement[key]
        metrics_verified = True
    examples = [s for s in sequence_comparisons if s["left"] == "delay" and s["right"] == "greedy" and s["different_order"]]
    example = min(examples, key=lambda s: (s["seed"], s["review_ticks"])) if examples else None
    summary = dict(status="verified", planned_episodes=192, completed_trace_replays=replays, independent_scenarios=16,
        experimental=totals, placement=placement, estimator_hash=estimator.estimator_hash, frozen_estimator_verified=True,
        serial_requests_verified=True, server_metrics_verified=metrics_verified, myopic_greedy_same_state_equivalence_verified=True,
        policy_outcomes=outcomes, paired_comparisons=comparisons, queue_example=example,
        note="Constructed development diagnostic; repeated policies/durations are not independent scenarios. No estimator refit.")
    for name, rows in (("policy_outcomes", outcomes), ("prediction_diagnostics", diagnostics), ("initial_predictions", predictions),
        ("paired_scenario_differences", paired), ("paired_comparisons", comparisons), ("review_orders", orders),
        ("sequence_comparisons", sequence_comparisons), ("dispatch_opportunities", dispatches)):
        write_csv(out / (name + ".csv"), rows)
    write_json(out / "diagnostics.json", summary)
    write_queue_example(out, example, by_run, by_order)
    return summary


def write_queue_example(out, example, by_run, by_order):
    if example is None:
        (out / "queue_example.md").write_text("# Queue example\n\nNo completed scenario had differing greedy/search review sequences.\n")
        return
    seed, duration = example["seed"], example["review_ticks"]
    scenario = generate_competition_scenario(seed)
    text = ["# Queue example: seed {}, review duration {}\n".format(seed, duration),
        "Selected by the predeclared first-seed rule, irrespective of winner. Faults and correctness below are offline scoring annotations; schedulers never receive them.\n",
        "| Job | Release | Deadline | Penalty | Correct action (offline) |", "| --- | ---: | ---: | ---: | --- |"]
    for job in scenario.jobs:
        p = job.public
        text.append("| {} | {} | {} | {} | {} |".format(p.job_id, p.release, p.deadline, p.terminal_cost, job.correct_action))
    for policy in ("greedy", "delay"):
        row = by_run[(seed, duration, policy)]
        events = read_events(out / row["folder"] / "events.jsonl")
        text.extend(["", "## {}: loss {}\n".format(policy, row["total_loss"]),
                     "| Tick | Event | Job | Details |", "| ---: | --- | --- | --- |"])
        for e in events:
            if e["event"] in ("proposal", "review_started", "review_completed", "request_expired", "job_closed"):
                details = {k:v for k,v in e.items() if k not in ("seq", "wall_utc", "tick", "event", "job_id", "observation")}
                text.append("| {} | {} | {} | {} |".format(e["tick"], e["event"], e.get("job_id", ""), json.dumps(details, sort_keys=True)))
    text.append("\nA changed review sequence alone does not imply lower realized loss; compare the two observed loss totals.\n")
    (out / "queue_example.md").write_text("\n".join(text))
