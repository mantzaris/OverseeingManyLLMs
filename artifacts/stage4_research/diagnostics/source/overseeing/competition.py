"""One frozen-estimator, predeclared Stage 3 competition matrix; no calibration."""

from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import shutil
import time

from .cli import ROOT, load_config, new_output, source_manifest, timeline, validate_deadline
from .client import GPUClient, MANUAL
from .competition_condition import GENERATOR_SPEC, generate_competition_scenario
from .development import server_snapshot
from .domain import STAGE3_POLICIES, digest, observation
from .estimator import AgreementEstimator, file_hash
from .gpu import collect_evidence
from .io import append_jsonl, render_trace, utc_now, write_csv, write_json
from .replay import replay_score
from .simulator import run_episode

FROZEN_ESTIMATOR = ROOT / "artifacts/stage2_development/run/estimator.json"
FIXED_CONFIG = {'seeds': [300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315],
 'policies': ['fcfs', 'uncertainty', 'myopic', 'greedy', 'edf', 'delay'],
 'review_ticks': [1, 2],
 'agents': 3,
 'jobs_per_agent': 2,
 'horizon': 12,
 'scheduled_calls_per_episode': 12,
 'scheduled_experimental_calls': 2304,
 'maximum_experimental_attempts': 4608,
 'maximum_placement_attempts': 1,
 'policy_order': 'left_rotate_by_(2*seed_index+duration_position)_mod_6',
 'duration_order': '[1,2] for even seed index; [2,1] for odd',
 'continuation': 'stage3_competition',
 'baseline_commit': 'c6871facdae9d0ebff0aa74dbe9a443ba6ff00c1',
 'estimator_hash': '54d9a97e25f5cb22cf0df216293303ea5c945713032c6bc1282c55fcf327e085',
 'estimator_file_sha256': '4ce8309bce27b70cdab1bd707bc3468f1039e88d4c30632541231efd6dde0d9d'}

ANALYSIS_DEFINITIONS = {
    "provenance": "Constructed diagnostic motivated by Stage 2 limited competition, identical greedy/search orders and slightly lower FCFS loss; separate from original distribution.",
    "unit": "16 paired scenarios; policies and durations are repeated conditions, not independent scenarios",
    "outcomes": "Per duration/policy: total and mean completed-episode loss, correctness, reviews, corrections, opportunity_lost_while_waiting; incomplete rows and bounds retained",
    "paired_differences": "All policy pairs within scenario/duration; left minus right, negative favors left; wins/ties/losses on completed pairs",
    "dispatch": "Free-supervisor saved public states; opportunity has >=1 eligible request, competition >=2; offline greedy/search and search/EDF choices on identical states",
    "orders": "Compare actual ordered review job IDs per scenario and duration; different order alone is not a realized loss advantage",
    "predictions": "Initial FIRST-action labels from every collected pair, before correction; bin counts/errors and frozen-estimator Brier separately by policy/duration; no refit",
    "equivalence": "With zero downtime and common eligibility, myopic and greedy both rank p*K; check equal choices on every saved public state",
    "figure": "Two duration panels, per-scenario search-minus-greedy and search-minus-EDF loss differences; no independent-episode uncertainty claims",
    "queue_example": "First numerical seed with completed differing greedy/search review sequences; if both durations qualify choose duration 1 before 2, regardless of winner",
    "failure_handling": "Never replace or rerun episodes; partial labels retained, paired loss missing with conservative bounds for incomplete runs",
}


def load_competition_config():
    config = json.loads((ROOT / "configs/stage3.json").read_text())
    if config != FIXED_CONFIG or config["policies"] != list(STAGE3_POLICIES):
        raise ValueError("Stage 3 configuration differs from the authorized fixed matrix")
    return config


def load_frozen_estimator(path, config):
    if file_hash(path) != config["estimator_file_sha256"]:
        raise ValueError("Stage 2 estimator file hash mismatch")
    estimator = AgreementEstimator.from_record(json.loads(Path(path).read_text()))
    if estimator.estimator_hash != config["estimator_hash"]:
        raise ValueError("Stage 2 estimator identity mismatch")
    return estimator


def episode_plan(config):
    result = []
    for index, seed in enumerate(config["seeds"]):
        durations = [1, 2] if index % 2 == 0 else [2, 1]
        for position, duration in enumerate(durations):
            shift = (2 * index + position) % 6
            policies = STAGE3_POLICIES[shift:] + STAGE3_POLICIES[:shift]
            for policy in policies:
                result.append(dict(seed=seed, policy=policy, review_ticks=duration,
                    folder="{}/s{}/{}".format(seed, duration, policy),
                    execution_index=len(result), scenario_hash=generate_competition_scenario(seed).hash,
                    planned_calls=12))
    return result


def prepare_competition(path):
    config = load_competition_config()
    load_frozen_estimator(FROZEN_ESTIMATOR, config)
    out = new_output(path)
    declaration = dict(prepared_utc=utc_now(), config=config, generator_spec=GENERATOR_SPEC,
        runtime_config=load_config(ROOT / "configs/stage1.json"), source_files_sha256=source_manifest(),
        prompt_sha256=digest(MANUAL), estimator_source=str(FROZEN_ESTIMATOR.relative_to(ROOT)),
        estimator_hash=config["estimator_hash"], estimator_file_sha256=config["estimator_file_sha256"],
        episodes=episode_plan(config), analysis_definitions=ANALYSIS_DEFINITIONS,
        sampling_seeds="Existing SHA256(scenario_seed,agent_id,job_id,sample,retry); excludes policy, duration and execution order",
        authorization_clock=json.loads((ROOT / "reports/implementation_clock.json").read_text()))
    declaration["config_hash"] = digest(config)
    declaration["runtime_config_hash"] = digest(declaration["runtime_config"])
    declaration["declaration_hash"] = digest(declaration)
    write_json(out / "declaration.json", declaration)
    shutil.copyfile(FROZEN_ESTIMATOR, out / "estimator.json")
    for name in declaration["source_files_sha256"]:
        target = out / "source" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    write_json(out / "scenarios.scorer-only.json", {str(seed): generate_competition_scenario(seed).record() for seed in config["seeds"]})
    return dict(status="declared_without_inference", episodes=192, scheduled_calls=2304,
                declaration_hash=declaration["declaration_hash"], out=str(out))


def empty_episode(entry):
    return dict(entry, status="not_started", error=None, total_loss=None, accrued_loss=None,
                correct_jobs=None, loss_upper_bound=48, scheduled_calls=0, attempts=0,
                prompt_tokens=0, completion_tokens=0, unknown_token_attempts=0,
                request_wall_seconds=0.0, episode_wall_seconds=0.0, reviews_completed=0,
                corrections=0, expired_requests=0, estimator_hash=None)


def run_competition(args):
    out = Path(args.out)
    config = load_competition_config()
    declaration = json.loads((out / "declaration.json").read_text())
    if digest({k: v for k, v in declaration.items() if k != "declaration_hash"}) != declaration["declaration_hash"]:
        raise ValueError("Declaration hash mismatch")
    if (declaration["config"] != config or declaration["episodes"] != episode_plan(config)
            or declaration["generator_spec"] != GENERATOR_SPEC
            or declaration["analysis_definitions"] != ANALYSIS_DEFINITIONS
            or declaration["runtime_config"] != load_config(ROOT / "configs/stage1.json")
            or declaration["source_files_sha256"] != source_manifest()):
        raise ValueError("Source, runtime, or plan changed since predeclaration")
    clock = json.loads((ROOT / "reports/implementation_clock.json").read_text())
    deadline = validate_deadline(args.deadline_utc, clock, "stage3_competition")
    started = time.monotonic()
    manifest = {"started_utc": utc_now(), "deadline_utc": deadline.isoformat(),
                "declaration_hash": declaration["declaration_hash"], "server_pid": args.server_pid,
                "server_log": args.server_log, "placement": {}, "status": "running",
                "planned_experimental_calls": 2304, "maximum_experimental_attempts": 4608,
                "maximum_placement_attempts": 1, "estimator_hash": config["estimator_hash"],
                "estimator_file_sha256": config["estimator_file_sha256"]}
    # This one-shot guard is written before any inference; interrupted work cannot silently rerun.
    with (out / "execution.json").open("x") as handle:
        json.dump(manifest, handle, indent=2)
    rows = [empty_episode(entry) for entry in declaration["episodes"]]
    write_csv(out / "episodes.csv", rows)
    placement = None
    estimator = load_frozen_estimator(out / "estimator.json", config)
    try:
        collect_evidence(args.server_pid, args.server_log, out / "gpu_before.json")
        server_snapshot(out, "before")
        versions = sorted({"{}=={}".format(d.metadata["Name"], d.version)
                           for d in importlib.metadata.distributions() if d.metadata["Name"]})
        (out / "requirements.actual.txt").write_text("\n".join(versions) + "\n")
        placement_config = dict(declaration["runtime_config"], max_attempts_per_call=1)
        placement = GPUClient(placement_config, out / "placement_raw_requests.jsonl", deadline, max_calls=1)
        job = min(generate_competition_scenario(300).jobs, key=lambda j: (j.public.release, j.public.agent_id)).public
        manifest["placement_action"] = placement.action(observation(job, job.release, []),
            {"scenario_seed": 300, "agent_id": job.agent_id, "job_id": "placement_check"}, "placement")
        collect_evidence(args.server_pid, args.server_log, out / "gpu_after_placement.json")
        for index, entry in enumerate(declaration["episodes"]):
            if datetime.now(timezone.utc) >= deadline:
                raise TimeoutError("Stage 3 deadline reached")
            if estimator is not None and file_hash(out / "estimator.json") != manifest["estimator_file_sha256"]:
                raise ValueError("Frozen estimator file changed")
            folder = out / entry["folder"]
            folder.mkdir(parents=True, exist_ok=False)
            provider = GPUClient(declaration["runtime_config"], folder / "raw_requests.jsonl", deadline, max_calls=12)
            result = run_episode(generate_competition_scenario(entry["seed"]), entry["policy"], provider,
                                 folder / "events.jsonl", review_ticks=entry["review_ticks"], estimator=estimator, record_dispatch=True)
            rows[index] = dict(result, **entry, estimator_hash=estimator.estimator_hash if estimator else None)
            render_trace(folder / "events.jsonl", folder / "trace.md")
            try:
                write_json(folder / "replay.json", replay_score(folder / "events.jsonl"))
            except Exception as exc:
                rows[index].update(status="invalid_trace", total_loss=None, correct_jobs=None, error=str(exc))
                raise
            finally:
                write_csv(out / "episodes.csv", rows)
            print("{} {}/{} {} seed={} policy={} status={}".format(utc_now(), index + 1, 192,
                  "review_ticks=" + str(entry["review_ticks"]), entry["seed"], entry["policy"], rows[index]["status"]), flush=True)
        manifest["status"] = "completed" if all(r["status"] == "completed" for r in rows) else "incomplete"
    except Exception as exc:
        manifest.update(status="incomplete", error="{}: {}".format(type(exc).__name__, exc))
    finally:
        for row in rows:
            if row["status"] == "not_started":
                row["error"] = manifest.get("error", "Not reached")
                folder = out / row["folder"]
                folder.mkdir(parents=True, exist_ok=True)
                events = folder / "events.jsonl"
                if not events.exists():
                    append_jsonl(events, dict(row, event="run_blocked", tick=None, wall_utc=utc_now(), seq=0))
                (folder / "raw_requests.jsonl").touch(exist_ok=True)
                render_trace(events, folder / "trace.md")
        if placement is not None:
            manifest["placement"] = placement.stats()
        for field in ("scheduled_calls", "attempts", "prompt_tokens", "completion_tokens", "unknown_token_attempts", "request_wall_seconds"):
            manifest["experimental_" + field] = sum(r[field] for r in rows)
        manifest.update(finished_utc=utc_now(), command_wall_seconds=round(time.monotonic() - started, 6),
                        all_completed=all(r["status"] == "completed" for r in rows))
        try:
            collect_evidence(args.server_pid, args.server_log, out / "gpu_final.json")
            server_snapshot(out, "after")
            manifest["final_server_status"] = "healthy and GPU-resident; retained"
        except Exception as exc:
            manifest["final_server_status"] = "Final check failed: " + str(exc)
        write_csv(out / "episodes.csv", rows)
        write_json(out / "manifest.json", manifest)
        timeline([(r["folder"], out / r["folder"] / "events.jsonl") for r in rows],
                 out / "queue_timeline.md", "live GPU constructed competition; see per-episode completion status")
    return {"all_completed": manifest["all_completed"], "status": manifest["status"],
            "scheduled_calls": manifest["experimental_scheduled_calls"], "out": str(out)}
