"""Exact bounded live invocation. Run from the isolated pod checkout only."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import urllib.request

out = Path("artifacts/stage1_gpu_live")
deadline = datetime.fromisoformat("2026-09-10T01:42:54+00:00")
remaining = (deadline - datetime.now(timezone.utc)).total_seconds()
assert remaining > 0, "Authorized continuation has expired"
assert not (out / "run").exists(), "Never overwrite or repeat this demonstration"
assert not (out / "execution.json").exists()
server_pid = int((out / "setup/server.pid").read_text())
command = [".venv/bin/python", "-m", "overseeing", "demo", "--config", "configs/stage1.json",
           "--out", str(out / "run"), "--server-pid", str(server_pid),
           "--server-log", str(out / "setup/server.log"), "--continuation", "stage1_gpu_live",
           "--deadline-utc", deadline.isoformat()]
record = {"started_utc": datetime.now(timezone.utc).isoformat(), "command": command,
          "server_pid": server_pid, "checkout": str(Path.cwd())}
for endpoint in ("health", "metrics"):
    with urllib.request.urlopen("http://127.0.0.1:8000/" + endpoint, timeout=5) as response:
        (out / (endpoint + "_before.txt")).write_bytes(response.read())
with (out / "gpu_telemetry.csv").open("x") as telemetry:
    monitor = subprocess.Popen(["nvidia-smi", "--query-gpu=timestamp,uuid,name,memory.total,memory.used,utilization.gpu,power.draw",
                                "--format=csv", "--loop-ms=200"], stdout=telemetry, stderr=subprocess.STDOUT)
    try:
        with (out / "demo_stdout.txt").open("x") as stdout:
            completed = subprocess.run(command, stdout=stdout, stderr=subprocess.STDOUT, timeout=remaining)
        record["exit_code"] = completed.returncode
    finally:
        monitor.terminate()
        monitor.wait(timeout=10)
        record["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (out / "execution.json").write_text(json.dumps(record, indent=2) + "\n")
for endpoint in ("health", "metrics"):
    with urllib.request.urlopen("http://127.0.0.1:8000/" + endpoint, timeout=5) as response:
        (out / (endpoint + "_after.txt")).write_bytes(response.read())
print(json.dumps(record, indent=2))
print((out / "demo_stdout.txt").read_text())
raise SystemExit(record["exit_code"])
