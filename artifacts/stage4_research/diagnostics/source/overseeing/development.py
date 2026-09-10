"""One predeclared calibration batch followed by frozen development validation."""

from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import shutil
import time
import urllib.request

from .cli import ROOT, load_config, new_output, source_manifest, timeline, validate_deadline
from .client import GPUClient, MANUAL
from .domain import STAGE2_POLICIES as POLICIES, digest, generate_scenario, observation
from .estimator import AgreementEstimator, calibration_examples, file_hash, fit_estimator
from .gpu import collect_evidence
from .io import append_jsonl, render_trace, utc_now, write_csv, write_json
from .replay import replay_score
from .simulator import StipulatedProposals, run_episode


def load_development_config():
    config = json.loads((ROOT / "configs/stage2.json").read_text())
    fixed = {"calibration_seeds": list(range(200, 216)), "validation_seeds": list(range(216, 224)),
             "calibration_policy": "fcfs", "policies": list(POLICIES), "review_ticks": 2,
             "agents": 3, "jobs_per_agent": 2, "horizon": 12, "calibration_p_error": 0.5,
             "minimum_bin_count": 10, "scheduled_calls_per_episode": 12,
             "scheduled_experimental_calls": 672, "maximum_experimental_attempts": 1344,
             "maximum_placement_attempts": 1, "policy_order": "left_rotate_by_seed_minus_216_mod_5",
             "continuation": "stage2_development",
             "baseline_commit": "77d0e16094b4529a23dfaf1907ba5ab87e25b660"}
    if config != fixed:
        raise ValueError("Stage 2 configuration differs from the explicitly authorized fixed batch")
    return config


def episode_plan(config):
    result = []
    for seed in config["calibration_seeds"]:
        result.append({"phase": "calibration", "seed": seed, "policy": "fcfs"})
    for index, seed in enumerate(config["validation_seeds"]):
        shift = index % len(POLICIES)
        for policy in POLICIES[shift:] + POLICIES[:shift]:
            result.append({"phase": "validation", "seed": seed, "policy": policy})
    for index, entry in enumerate(result):
        entry.update(execution_index=index, folder="{}/{}/{}".format(entry["phase"], entry["seed"], entry["policy"]),
                     scenario_hash=generate_scenario(entry["seed"]).hash, planned_calls=12)
    return result


def prepare_development(path):
    config = load_development_config()
    out = new_output(path)
    declaration = {"prepared_utc": utc_now(), "config": config,
                   "runtime_config": load_config(ROOT / "configs/stage1.json"),
                   "source_files_sha256": source_manifest(), "prompt_sha256": digest(MANUAL),
                   "episodes": episode_plan(config),
                   "authorization_clock": json.loads((ROOT / "reports/implementation_clock.json").read_text()),
                   "prediction_diagnostics": "Same saved validation trajectories; no counterfactual generations",
                   "failure_handling": "Retain partial pairs and every episode row; never replace seeds or rerun episodes"}
    declaration["declaration_hash"] = digest(declaration)
    write_json(out / "declaration.json", declaration)
    for name in declaration["source_files_sha256"]:
        target = out / "source" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    write_json(out / "scenarios.scorer-only.json", {str(seed): generate_scenario(seed).record() for seed in range(200, 224)})
    return {"status": "declared_without_inference", "episodes": 56, "scheduled_calls": 672,
            "declaration_hash": declaration["declaration_hash"], "out": str(out)}


def empty_episode(entry):
    scenario = generate_scenario(entry["seed"])
    return dict(entry, status="not_started", error=None, total_loss=None, accrued_loss=None,
                correct_jobs=None, loss_upper_bound=sum(j.public.cost_per_tick * (j.public.deadline - j.public.release)
                                                       + j.public.terminal_cost for j in scenario.jobs),
                scheduled_calls=0, attempts=0, prompt_tokens=0, completion_tokens=0,
                unknown_token_attempts=0, request_wall_seconds=0.0, episode_wall_seconds=0.0,
                reviews_completed=0, corrections=0, expired_requests=0, estimator_hash=None)


def development_mechanics(path):
    from .fixtures import cases
    out = new_output(path)
    scenario, actions, probabilities, expected = cases()["competition"]
    rows = []
    for policy in POLICIES:
        folder = out / policy
        folder.mkdir()
        result = run_episode(scenario, policy, StipulatedProposals(actions), folder / "events.jsonl",
                             fixture_probabilities=probabilities, record_dispatch=True)
        if result["status"] != "completed" or result["total_loss"] != expected[policy]:
            raise AssertionError("Competition mechanics failed: " + policy)
        rows.append(result)
        write_json(folder / "replay.json", replay_score(folder / "events.jsonl"))
        render_trace(folder / "events.jsonl", folder / "trace.md")
    write_csv(out / "episodes.csv", rows)
    timeline([(r["policy"], out / r["policy"] / "events.jsonl") for r in rows],
             out / "queue_timeline.md", "stipulated competition mechanics; zero model calls")
    return {"status": "passed", "fixture_policy_runs": 5, "llm_calls": 0}


def server_snapshot(out, suffix):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    for endpoint in ("health", "metrics"):
        with opener.open("http://127.0.0.1:8000/" + endpoint, timeout=5) as response:
            (out / (endpoint + "_" + suffix + ".txt")).write_bytes(response.read())


def run_development(args):
    out = Path(args.out)
    config = load_development_config()
    declaration = json.loads((out / "declaration.json").read_text())
    if digest({k: v for k, v in declaration.items() if k != "declaration_hash"}) != declaration["declaration_hash"]:
        raise ValueError("Declaration hash mismatch")
    if (declaration["config"] != config or declaration["episodes"] != episode_plan(config)
            or declaration["runtime_config"] != load_config(ROOT / "configs/stage1.json")
            or declaration["source_files_sha256"] != source_manifest()):
        raise ValueError("Source, runtime, or plan changed since predeclaration")
    clock = json.loads((ROOT / "reports/implementation_clock.json").read_text())
    deadline = validate_deadline(args.deadline_utc, clock, "stage2_development")
    started = time.monotonic()
    manifest = {"started_utc": utc_now(), "deadline_utc": deadline.isoformat(),
                "declaration_hash": declaration["declaration_hash"], "server_pid": args.server_pid,
                "server_log": args.server_log, "placement": {}, "status": "running",
                "planned_experimental_calls": 672, "maximum_experimental_attempts": 1344,
                "maximum_placement_attempts": 1, "estimator_hash": None}
    # This one-shot guard is written before any inference; interrupted work cannot silently rerun.
    with (out / "execution.json").open("x") as handle:
        json.dump(manifest, handle, indent=2)
    rows = [empty_episode(entry) for entry in declaration["episodes"]]
    write_csv(out / "episodes.csv", rows)
    placement, estimator = None, None
    try:
        collect_evidence(args.server_pid, args.server_log, out / "gpu_before.json")
        server_snapshot(out, "before")
        versions = sorted({"{}=={}".format(d.metadata["Name"], d.version)
                           for d in importlib.metadata.distributions() if d.metadata["Name"]})
        (out / "requirements.actual.txt").write_text("\n".join(versions) + "\n")
        placement_config = dict(declaration["runtime_config"], max_attempts_per_call=1)
        placement = GPUClient(placement_config, out / "placement_raw_requests.jsonl", deadline, max_calls=1)
        job = min(generate_scenario(200).jobs, key=lambda j: (j.public.release, j.public.agent_id)).public
        manifest["placement_action"] = placement.action(observation(job, job.release, []),
            {"scenario_seed": 200, "agent_id": job.agent_id, "job_id": "placement_check"}, "placement")
        collect_evidence(args.server_pid, args.server_log, out / "gpu_after_placement.json")
        for index, entry in enumerate(declaration["episodes"]):
            if datetime.now(timezone.utc) >= deadline:
                raise TimeoutError("Stage 2 deadline reached")
            if entry["phase"] == "validation" and estimator is None:
                examples, provenance = [], []
                for previous in rows[:16]:
                    path = out / previous["folder"] / "events.jsonl"
                    examples.extend(calibration_examples(path))
                    provenance.append({"seed": previous["seed"], "policy": "fcfs", "status": previous["status"],
                                       "events": str(path.relative_to(out)), "events_sha256": file_hash(path),
                                       "raw_requests_sha256": file_hash(path.parent / "raw_requests.jsonl")})
                write_csv(out / "calibration_examples.csv", examples)
                fitted = fit_estimator(examples, {"episodes": provenance, "seeds": list(range(200, 216)),
                    "planned_examples": 96, "collected_examples": len(examples),
                    "declaration_hash": declaration["declaration_hash"], "review_status_used_for_selection": False})
                write_json(out / "estimator.json", fitted)
                estimator = AgreementEstimator.from_record(fitted)
                manifest.update(estimator_hash=estimator.estimator_hash, estimator_frozen_utc=fitted["fitted_utc"],
                                estimator_file_sha256=file_hash(out / "estimator.json"))
                write_json(out / "manifest.json", manifest)
            if estimator is not None and file_hash(out / "estimator.json") != manifest["estimator_file_sha256"]:
                raise ValueError("Frozen estimator file changed")
            folder = out / entry["folder"]
            folder.mkdir(parents=True, exist_ok=False)
            provider = GPUClient(declaration["runtime_config"], folder / "raw_requests.jsonl", deadline, max_calls=12)
            result = run_episode(generate_scenario(entry["seed"]), entry["policy"], provider,
                                 folder / "events.jsonl", estimator=estimator, record_dispatch=True)
            rows[index] = dict(result, **entry, estimator_hash=estimator.estimator_hash if estimator else None)
            render_trace(folder / "events.jsonl", folder / "trace.md")
            try:
                write_json(folder / "replay.json", replay_score(folder / "events.jsonl"))
            except Exception as exc:
                rows[index].update(status="invalid_trace", total_loss=None, correct_jobs=None, error=str(exc))
                raise
            finally:
                write_csv(out / "episodes.csv", rows)
            print("{} {}/{} {} seed={} policy={} status={}".format(utc_now(), index + 1, 56,
                  entry["phase"], entry["seed"], entry["policy"], rows[index]["status"]), flush=True)
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
                 out / "queue_timeline.md", "live GPU development; see per-episode completion status")
    return {"all_completed": manifest["all_completed"], "status": manifest["status"],
            "scheduled_calls": manifest["experimental_scheduled_calls"], "out": str(out)}
