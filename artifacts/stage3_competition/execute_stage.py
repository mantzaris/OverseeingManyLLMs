"""Actual one-shot Stage 3 launch with telemetry; run in the existing pod checkout."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

out = Path("artifacts/stage3_competition")
deadline = datetime.fromisoformat("2026-09-10T04:47:37+00:00")
remaining = (deadline - datetime.now(timezone.utc)).total_seconds()
assert remaining > 0
assert not (out / "run/execution.json").exists()
assert not (out / "launch.json").exists()
server_log = Path("artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/server.log")
command = [".venv/bin/python", "-m", "overseeing", "competition", "--out", str(out / "run"),
           "--server-pid", "7338", "--server-log", str(server_log),
           "--deadline-utc", deadline.isoformat()]
record = {"started_utc": datetime.now(timezone.utc).isoformat(), "command": command,
          "checkout": str(Path.cwd()), "server_log_start_bytes": server_log.stat().st_size}
with (out / "launch.json").open("x") as handle:
    json.dump(record, handle, indent=2)
with (out / "gpu_telemetry.csv").open("x") as telemetry:
    monitor = subprocess.Popen(["nvidia-smi", "--query-gpu=timestamp,uuid,name,memory.total,memory.used,utilization.gpu,power.draw",
                                "--format=csv", "--loop-ms=500"], stdout=telemetry, stderr=subprocess.STDOUT)
    try:
        with (out / "execution_stdout.txt").open("x") as stdout:
            completed = subprocess.run(command, stdout=stdout, stderr=subprocess.STDOUT, timeout=remaining)
        record["exit_code"] = completed.returncode
    finally:
        monitor.terminate()
        monitor.wait(timeout=10)
        record["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (out / "launch.json").write_text(json.dumps(record, indent=2) + "\n")
        with server_log.open("rb") as source:
            source.seek(record["server_log_start_bytes"])
            (out / "server_stage3.log").write_bytes(source.read())
print(json.dumps(record, indent=2))
print((out / "execution_stdout.txt").read_text())
raise SystemExit(record["exit_code"])
