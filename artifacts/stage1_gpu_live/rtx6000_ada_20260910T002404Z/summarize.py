"""Recompute this continuation's compact accounting from retained evidence; no inference."""
import csv
from datetime import datetime
import json
import math
from pathlib import Path

out = Path(__file__).resolve().parent


def read(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


manifest = json.loads((out / "run/manifest.json").read_text())
accounting = {"policies": {}, "placement": manifest["placement"],
              "demo_command_wall_seconds": manifest["command_wall_seconds"],
              "started_utc": manifest["started_utc"], "finished_utc": manifest["finished_utc"],
              "allocation_started_utc": None, "allocation_ended_utc": None,
              "billing_intervals": "Unknown; provider timestamps and rate were not supplied.",
              "calibrated_probabilities": False, "inference_failures": []}
latencies = []
total_fields = ("scheduled_calls", "attempts", "prompt_tokens", "completion_tokens",
                "unknown_token_attempts", "request_wall_seconds")
totals = {name: 0 for name in total_fields}
for policy in ("placement", "fcfs", "uncertainty", "myopic", "delay"):
    path = out / "run/placement_raw_requests.jsonl" if policy == "placement" else out / "run" / policy / "raw_requests.jsonl"
    attempts = [r for r in read(path) if r["phase"] == "attempt_finished"]
    for r in attempts:
        if r.get("error"):
            accounting["inference_failures"].append({"policy": policy, "job_id": r["job_id"],
                "sample": r["sample"], "retry": r["retry"], "error": r["error"],
                "inference_request_attempted": r["inference_request_attempted"]})
    if policy == "placement":
        accounting["placement"]["retries"] = sum(r["retry"] > 0 for r in attempts)
        continue
    events = read(out / "run" / policy / "events.jsonl")
    result = dict(events[-1])
    result["retries"] = sum(r["retry"] > 0 for r in attempts)
    result["agreeing_pairs"] = sum(e["agreement"] for e in events if e["event"] == "proposal")
    result["expired_categories"] = {category: sum(e.get("category") == category for e in events
        if e["event"] == "request_expired") for category in
        ("zero_value", "infeasible_at_arrival", "opportunity_lost_while_waiting")}
    accounting["policies"][policy] = result
    for name in total_fields:
        totals[name] += result[name]
    latencies.extend(r["inference_wall_seconds"] for r in attempts if r["inference_request_attempted"])
totals["retries"] = sum(r["retries"] for r in accounting["policies"].values())
accounting["experimental_totals"] = totals
accounting["all_request_totals"] = {name: totals[name] + accounting["placement"][name] for name in total_fields}
accounting["all_request_totals"]["retries"] = totals["retries"] + accounting["placement"]["retries"]
accounting["experimental_mean_request_seconds"] = sum(latencies) / len(latencies) if latencies else None
accounting["experimental_p95_request_seconds_nearest_rank"] = sorted(latencies)[math.ceil(.95 * len(latencies)) - 1] if latencies else None
accounting["experimental_output_tokens_per_request_wall_second"] = totals["completion_tokens"] / totals["request_wall_seconds"] if totals["request_wall_seconds"] else None
execution = json.loads((out / "execution.json").read_text())
accounting["wrapper_wall_seconds"] = (datetime.fromisoformat(execution["finished_utc"]) - datetime.fromisoformat(execution["started_utc"])).total_seconds()
with (out / "gpu_telemetry.csv").open(newline="") as handle:
    rows = [{k.strip(): v.strip() for k, v in row.items()} for row in csv.DictReader(handle)]
accounting["telemetry"] = {"samples": len(rows), "interval_ms": 200,
    "maximum_observed_memory_mib": max(float(r["memory.used [MiB]"].split()[0]) for r in rows),
    "maximum_observed_utilization_percent": max(float(r["utilization.gpu [%]"].split()[0]) for r in rows),
    "note": "Sampled observations are not exact peak memory or kernel-time measurements."}
(out / "accounting.json").write_text(json.dumps(accounting, indent=2, sort_keys=True) + "\n")
print(json.dumps(accounting, indent=2, sort_keys=True))
