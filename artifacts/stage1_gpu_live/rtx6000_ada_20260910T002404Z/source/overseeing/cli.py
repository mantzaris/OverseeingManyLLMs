"""Only mechanics, the authorized four-run demo, blocked records, and replay."""

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import time
import urllib.parse

from .client import GPUClient, MODEL, REVISION
from .domain import POLICIES, generate_scenario, observation
from .fixtures import cases
from .gpu import collect_evidence
from .io import append_jsonl, read_events, render_trace, utc_now, write_csv, write_json
from .replay import replay_score
from .simulator import StipulatedProposals, run_episode

ROOT = Path(__file__).resolve().parent.parent


def validate_deadline(deadline_utc, clock, continuation=None, now=None):
    """Select an explicitly recorded authorization; never extend the overall cap."""
    now = now or datetime.now(timezone.utc)
    maximum = datetime.fromisoformat(clock["stage1_deadline_utc"])
    if continuation:
        stages = [s for s in clock.get("continuation_stages", []) if s["name"] == continuation]
        if len(stages) != 1:
            raise ValueError("Continuation must name one recorded user authorization")
        stage = stages[0]
        start = datetime.fromisoformat(stage["started_utc"])
        maximum = datetime.fromisoformat(stage["deadline_utc"])
        if (start.tzinfo is None or maximum.tzinfo is None or start > now
                or not start < maximum <= start + timedelta(hours=2)
                or stage.get("authorization") != "explicit_user_request"):
            raise ValueError("Invalid authorized continuation window")
    overall = datetime.fromisoformat(clock["overall_deadline_utc"])
    if maximum.tzinfo is None or overall.tzinfo is None:
        raise ValueError("Deadlines require a UTC offset")
    if deadline_utc is None and not continuation:
        raise ValueError("Provide a deadline or select an explicitly recorded continuation")
    # A named authorization supplies its own cap; never invent or reset a clock.
    deadline = datetime.fromisoformat(deadline_utc) if deadline_utc else min(maximum, overall)
    if deadline.tzinfo is None:
        raise ValueError("Deadlines require a UTC offset")
    if deadline > min(maximum, overall) or deadline <= now:
        raise ValueError("Deadline exceeds the recorded stage/overall window or has expired")
    return deadline


def load_config(path):
    config = json.loads(Path(path).read_text())
    fixed = {"seed": 100, "agents": 3, "jobs_per_agent": 2, "horizon": 12,
             "review_ticks": 2, "policies": list(POLICIES), "p_error": 0.5,
             "model": MODEL, "revision": REVISION, "temperature": 0.3, "top_p": 1.0,
             "max_input_tokens": 1024, "max_output_tokens": 48, "timeout_seconds": 60,
             "max_attempts_per_call": 2, "scheduled_calls_per_policy": 12, "placement_calls": 1}
    for key, value in fixed.items():
        if config.get(key) != value:
            raise ValueError("Stage 1 fixes {}={!r}; this CLI cannot launch other studies".format(key, value))
    return config


def source_manifest():
    files = sorted((ROOT / "overseeing").glob("*.py")) + sorted((ROOT / "scripts").glob("*.sh"))
    files += sorted((ROOT / "scripts").glob("*.py")) + sorted((ROOT / "tests").glob("*.py"))
    files += [ROOT / "configs/stage1.json", ROOT / "requirements-gpu.txt"]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def new_output(path):
    out = Path(path)
    out.mkdir(parents=True, exist_ok=False)
    return out


def timeline(entries, path, evidence):
    lines = ["# Review-queue timeline", "", "Evidence: **{}**.".format(evidence), "",
             "Snapshots are after completion, closure, arrivals and dispatch; before interval loss.", "",
             "| Run | Tick | In service (completion tick) | Pending |", "| --- | --- | --- | --- |"]
    for label, event_path in entries:
        for event in read_events(event_path):
            if event["event"] == "queue_snapshot":
                busy = event["busy"]
                lines.append("| {} | {} | {} | {} |".format(label, event["tick"],
                    "{} ({})".format(busy["job_id"], busy["finish"]) if busy else "—",
                    ", ".join(event["pending"]) or "—"))
    if len(lines) == 8:
        lines.append("\nNo simulated intervals ran; no GPU timeline exists.")
    path.write_text("\n".join(lines) + "\n")


def mechanics(out):
    out = new_output(out)
    rows, timelines = [], []
    for name, (scenario, actions, probabilities, expected) in cases().items():
        for policy in POLICIES:
            folder = out / name / policy
            folder.mkdir(parents=True)
            result = run_episode(scenario, policy, StipulatedProposals(actions), folder / "events.jsonl",
                                 fixture_probabilities=probabilities)
            result.update(fixture=name, expected_loss=expected[policy])
            rows.append(result)
            write_csv(out / "episodes.csv", rows)
            if result["status"] != "completed" or result["total_loss"] != expected[policy]:
                raise AssertionError("Fixture failed: {}/{}: {}".format(name, policy, result))
            write_json(folder / "replay.json", replay_score(folder / "events.jsonl"))
            render_trace(folder / "events.jsonl", folder / "trace.md")
            if name == "competition" and policy in ("myopic", "delay"):
                timelines.append((name + "/" + policy, folder / "events.jsonl"))
    timeline(timelines, out / "queue_timeline.md", "stipulated mechanics; NOT GPU inference")
    write_json(out / "summary.json", {"status": "passed", "fixture_policy_runs": len(rows),
               "independent_replays_verified": len(rows), "llm_calls": 0,
               "evidence": "stipulated_mechanics_only", "source_files_sha256": source_manifest()})
    return {"status": "passed", "fixture_policy_runs": len(rows), "llm_calls": 0}


def empty_row(policy, scenario, status, reason):
    return {"policy": policy, "seed": 100, "scenario_hash": scenario.hash,
            "evidence": "no_gpu_inference", "status": status, "error": reason,
            "planned_calls": 12, "scheduled_calls": 0, "attempts": 0,
            "prompt_tokens": 0, "completion_tokens": 0, "unknown_token_attempts": 0,
            "request_wall_seconds": 0.0, "total_loss": None, "accrued_loss": None,
            "correct_jobs": None, "jobs_closed": 0, "reviews_started": 0,
            "reviews_completed": 0, "corrections": 0, "late_returns": 0,
            "expired_requests": 0, "review_busy_ticks": 0, "simulated_ticks_completed": 0,
            "episode_wall_seconds": 0.0}


def blocked_trace(out, row):
    folder = out / row["policy"]
    folder.mkdir(exist_ok=True)
    (folder / "raw_requests.jsonl").touch(exist_ok=True)
    events = folder / "events.jsonl"
    if not events.exists():
        append_jsonl(events, dict(row, event="run_blocked", wall_utc=utc_now(), seq=0, tick=None))
    render_trace(events, folder / "trace.md")


def summary(out, manifest, rows):
    write_csv(out / "episodes.csv", rows)
    write_json(out / "manifest.json", manifest)
    lines = ["# Stage 1 live demonstration", "", "GPU inference succeeded: **{}**.".format(
             manifest["gpu_inference_succeeded"]), "", "p(error)=0.5 is provisional and uncalibrated.", "",
             "| Policy | Status | Loss | Correct jobs | Calls scheduled / attempted |",
             "| --- | --- | --- | --- | --- |"]
    for row in rows:
        lines.append("| {} | {} | {} | {} | {} / {} |".format(row["policy"], row["status"],
                     row["total_loss"] if row["total_loss"] is not None else "unknown",
                     row["correct_jobs"] if row["correct_jobs"] is not None else "unknown",
                     row["scheduled_calls"], row["attempts"]))
    lines += ["", "Planned experimental calls: 48. Placement check is separate; see manifest.json.",
              "Unstarted/incomplete outcomes are unknown, not zero loss.",
              "Final server status: " + manifest["final_server_status"] + "."]
    (out / "trace.md").write_text("\n".join(lines) + "\n")
    timeline([(r["policy"], out / r["policy"] / "events.jsonl") for r in rows],
             out / "queue_timeline.md", "live GPU only if verified in manifest")


def run_demo(args, blocked=False):
    config = load_config(args.config)
    out, scenario = new_output(args.out), generate_scenario(100)
    started = time.monotonic()
    manifest = {"started_utc": utc_now(), "config": config, "scenario_hash": scenario.hash,
                "source_files_sha256": source_manifest(), "gpu_inference_succeeded": False,
                "calibrated_estimator": False, "planned_experimental_calls": 48,
                "planned_placement_calls": 1, "placement": {"scheduled_calls": 0, "attempts": 0,
                "prompt_tokens": 0, "completion_tokens": 0, "unknown_token_attempts": 0,
                "request_wall_seconds": 0.0}, "final_server_status": "unknown; not inspected",
                "allocation_started_utc": None, "allocation_ended_utc": None,
                "allocation_hours": None, "billing_intervals": "unknown; includes time outside this stage"}
    write_json(out / "scenario.scorer-only.json", scenario.record())
    rows = [empty_row(p, scenario, "not_started", None) for p in POLICIES]
    write_csv(out / "episodes.csv", rows)
    placement = None
    try:
        if blocked:
            connection = json.loads(Path(args.connection).read_text())
            manifest["connection"] = connection
            raise RuntimeError(connection["blocker"])
        clock = json.loads((ROOT / "reports/implementation_clock.json").read_text())
        continuation = getattr(args, "continuation", None)
        deadline = validate_deadline(args.deadline_utc, clock, continuation)
        manifest["continuation"] = continuation
        manifest["authorization_clock"] = clock
        manifest["deadline_utc"] = deadline.isoformat()
        port = urllib.parse.urlparse(config["base_url"]).port or 8000
        collect_evidence(args.server_pid, args.server_log, out / "gpu_before.json", port)
        manifest["preflight_verified"] = True
        manifest["final_server_status"] = "running; retained"
        # Version pins only: pip freeze can expose credentials in direct dependency URLs.
        versions = sorted({"{}=={}".format(d.metadata["Name"], d.version)
                           for d in importlib.metadata.distributions() if d.metadata["Name"]})
        (out / "requirements.actual.txt").write_text("\n".join(versions) + "\n")
        placement = GPUClient(config, out / "placement_raw_requests.jsonl", deadline, max_calls=1)
        first_job = min(scenario.jobs, key=lambda j: (j.public.release, j.public.agent_id)).public
        action = placement.action(observation(first_job, first_job.release, []),
                                  {"scenario_seed": 100, "agent_id": first_job.agent_id,
                                   "job_id": "placement_check"}, sample="placement")
        manifest["placement_action"] = action
        collect_evidence(args.server_pid, args.server_log, out / "gpu_after_placement.json", port)
        manifest["gpu_inference_succeeded"] = True
        for index, policy in enumerate(POLICIES):
            folder = out / policy
            folder.mkdir()
            provider = GPUClient(config, folder / "raw_requests.jsonl", deadline)
            rows[index] = run_episode(scenario, policy, provider, folder / "events.jsonl")
            render_trace(folder / "events.jsonl", folder / "trace.md")
            try:
                write_json(folder / "replay.json", replay_score(folder / "events.jsonl"))
            except Exception as exc:
                rows[index].update(status="invalid_trace", total_loss=None, correct_jobs=None,
                                   error="Replay validation failed: " + str(exc))
                raise
            write_csv(out / "episodes.csv", rows)
    except Exception as exc:
        reason = "{}: {}".format(type(exc).__name__, exc)
        manifest["blocker"] = reason
        for index, row in enumerate(rows):
            if row["status"] == "not_started":
                rows[index] = empty_row(row["policy"], scenario, "blocked", reason)
    finally:
        if manifest.get("preflight_verified"):
            try:
                collect_evidence(args.server_pid, args.server_log, out / "gpu_final.json", port)
                manifest["final_server_status"] = "running and GPU-resident; retained; health see request logs"
            except Exception as exc:
                present = Path("/proc/{}".format(args.server_pid)).exists()
                manifest["final_server_status"] = ("process present" if present else "process absent") + "; final GPU verification failed: " + str(exc)
        if placement:
            manifest["placement"] = placement.stats()
        (out / "placement_raw_requests.jsonl").touch(exist_ok=True)
        for row in rows:
            if row["status"] == "blocked":
                blocked_trace(out, row)
        manifest["finished_utc"] = utc_now()
        manifest["command_wall_seconds"] = round(time.monotonic() - started, 6)
        manifest["all_four_completed"] = all(r["status"] == "completed" for r in rows)
        summary(out, manifest, rows)
    return {"gpu_inference_succeeded": manifest["gpu_inference_succeeded"],
            "all_four_completed": manifest["all_four_completed"], "output": str(out)}


def main():
    parser = argparse.ArgumentParser(description="Bounded Stage 1 backbone; no calibration/evaluation entry point")
    commands = parser.add_subparsers(dest="command", required=True)
    mechanics_parser = commands.add_parser("mechanics", help="Stipulated arithmetic checks; no inference")
    mechanics_parser.add_argument("--out", required=True)
    replay_parser = commands.add_parser("replay", help="Independently score saved events; no inference")
    replay_parser.add_argument("events")
    for name in ("demo", "record-blocked"):
        sub = commands.add_parser(name)
        sub.add_argument("--config", default=str(ROOT / "configs/stage1.json"))
        sub.add_argument("--out", required=True)
        if name == "demo":
            sub.add_argument("--server-pid", required=True, type=int)
            sub.add_argument("--server-log", required=True)
            sub.add_argument("--deadline-utc", help="Optional earlier cap; defaults to the named continuation's recorded deadline")
            sub.add_argument("--continuation", help="Name of an explicitly authorized recorded continuation")
        else:
            sub.add_argument("--connection", required=True)
    args = parser.parse_args()
    if args.command == "mechanics":
        result = mechanics(args.out)
    elif args.command == "replay":
        result = replay_score(args.events)
    else:
        result = run_demo(args, blocked=args.command == "record-blocked")
    print(json.dumps(result, sort_keys=True))
    return 0 if result.get("all_four_completed", True) else 2
