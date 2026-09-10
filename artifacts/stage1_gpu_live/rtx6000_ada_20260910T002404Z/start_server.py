"""Exact isolated server launch used for this continuation; no inference requests."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import socket
import subprocess

out = Path("artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup")
deadline = datetime.fromisoformat("2026-09-10T02:24:04+00:00")
assert datetime.now(timezone.utc) < deadline, "Continuation expired"
assert not (out / "server.pid").exists(), "Do not launch a second server"
with socket.socket() as probe:
    probe.bind(("127.0.0.1", 8000))
environment = dict(os.environ, HF_HOME=str(Path.cwd() / "model-cache"))
with (out / "server.log").open("x") as log:
    process = subprocess.Popen(["bash", "scripts/serve_gpu.sh"], env=environment,
                               stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
(out / "server.pid").write_text(str(process.pid) + "\n")
record = {"started_utc": datetime.now(timezone.utc).isoformat(), "pid": process.pid,
          "command": ["bash", "scripts/serve_gpu.sh"], "cwd": str(Path.cwd()),
          "environment_overrides": {"HF_HOME": environment["HF_HOME"], "CUDA_VISIBLE_DEVICES": "0"},
          "launch_script": "scripts/serve_gpu.sh", "gpu_memory_utilization": 0.5,
          "cpu_offload_gb": 0, "swap_space_gb": 0}
(out / "server_launch.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
