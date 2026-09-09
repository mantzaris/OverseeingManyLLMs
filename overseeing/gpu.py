"""Read-only same-pod placement evidence. No package install or service management."""

import csv
import importlib.metadata
import os
from pathlib import Path
import platform
import subprocess
import sys

from .client import MODEL, REVISION
from .io import utc_now, write_json

EXPECTED_GPU_NAME = "NVIDIA L40S"
MINIMUM_GPU_MEMORY_MIB = 45000

REQUIRED_FLAGS = {
    "--revision": REVISION, "--tokenizer-revision": REVISION,
    "--dtype": "bfloat16", "--tensor-parallel-size": "1", "--max-model-len": "2048",
    "--max-num-seqs": "1", "--gpu-memory-utilization": "0.5",
    "--cpu-offload-gb": "0", "--swap-space": "0", "--generation-config": "vllm",
    "--host": "127.0.0.1", "--seed": "20260909",
}


def output(command):
    return subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, timeout=10).stdout.strip()


def validate_hardware(gpus):
    if (len(gpus) != 1 or gpus[0][1] != EXPECTED_GPU_NAME
            or float(gpus[0][2]) < MINIMUM_GPU_MEMORY_MIB):
        raise ValueError("Expected one NVIDIA L40S with at least 45000 MiB total memory")


def cuda_runtime_evidence():
    import torch
    if (not torch.cuda.is_available() or torch.cuda.device_count() != 1
            or torch.cuda.get_device_name(0) != EXPECTED_GPU_NAME
            or not torch.cuda.is_bf16_supported()):
        raise ValueError("Expected one CUDA L40S with native BF16 support")
    # A tiny CUDA BF16 kernel verifies the runtime, independently of driver compatibility.
    with torch.inference_mode():
        x = torch.ones((32, 32), device="cuda:0", dtype=torch.bfloat16)
        y = x @ x
        torch.cuda.synchronize()
        if y.dtype != torch.bfloat16 or y.device.type != "cuda" or y[0, 0].item() != 32:
            raise ValueError("CUDA BF16 kernel verification failed")
    return {"torch": torch.__version__, "torch_cuda_runtime": torch.version.cuda,
            "device_name": torch.cuda.get_device_name(0),
            "compute_capability": list(torch.cuda.get_device_capability(0)),
            "native_bf16_supported": True, "bf16_matmul_device": str(y.device),
            "bf16_matmul_dtype": str(y.dtype), "bf16_matmul_verified": True}


def descendant(pid, ancestor):
    for _ in range(32):
        if pid == ancestor:
            return True
        if pid <= 1:
            break
        try:
            status = Path("/proc/{}/status".format(pid)).read_text()
            pid = int(next(line.split()[1] for line in status.splitlines() if line.startswith("PPid:")))
        except (OSError, StopIteration, ValueError):
            break
    return False


def collect_evidence(server_pid, server_log, path, expected_port=8000):
    record = {"captured_utc": utc_now(), "status": "unverified", "server_pid": server_pid,
              "python": sys.version, "platform": platform.platform(),
              "model": MODEL, "revision": REVISION}
    try:
        gpu_text = output(["nvidia-smi", "--query-gpu=uuid,name,memory.total,memory.used,driver_version,utilization.gpu",
                           "--format=csv,noheader,nounits"])
        record["gpu_query"] = gpu_text
        gpus = list(csv.reader(gpu_text.splitlines(), skipinitialspace=True))
        validate_hardware(gpus)
        record["expected_gpu_name"] = EXPECTED_GPU_NAME
        record["minimum_gpu_memory_mib"] = MINIMUM_GPU_MEMORY_MIB
        record["cuda_runtime"] = cuda_runtime_evidence()
        args = Path("/proc/{}/cmdline".format(server_pid)).read_bytes().decode().strip("\0").split("\0")
        if "serve" not in args or MODEL not in args or "--enforce-eager" not in args:
            raise ValueError("PID is not the planned vLLM serve command")
        flags = dict(REQUIRED_FLAGS, **{"--port": str(expected_port)})
        for flag, expected in flags.items():
            if args.count(flag) != 1 or args[args.index(flag) + 1] != expected:
                raise ValueError("Missing/different required server flag " + flag)
        if any(flag in args for flag in ("--quantization", "--lora-modules", "--speculative-config")):
            raise ValueError("Unplanned model/decoding modification")
        record["server_arguments"] = dict(flags, enforce_eager=True, model=MODEL)
        record["server_executable"] = os.readlink("/proc/{}/exe".format(server_pid))
        process_text = output(["nvidia-smi", "--query-compute-apps=gpu_uuid,pid,process_name,used_gpu_memory",
                               "--format=csv,noheader,nounits"])
        processes = list(csv.reader(process_text.splitlines(), skipinitialspace=True))
        own = [row for row in processes if len(row) == 4 and row[0] == gpus[0][0]
               and descendant(int(row[1]), server_pid) and float(row[3]) > 0]
        record["serving_gpu_processes"] = own
        if not own:
            raise ValueError("No GPU-resident process belongs to the serving PID")
        if sum(float(row[3]) for row in own) < 14000:
            raise ValueError("Serving GPU allocation is too small for the pinned BF16 model")
        record["package_versions"] = {name: importlib.metadata.version(name)
                                      for name in ("vllm", "torch", "transformers")}
        record["cuda_toolkit_query"] = "Driver and runtime details are also retained in server logs/pip freeze."
        log = Path(server_log).read_text(errors="replace")
        keywords = ("cuda", "gpu", "bfloat16", "loading model", "model loading", "api server version")
        record["relevant_server_log"] = [line[:2000] for line in log.splitlines()
            if any(k in line.lower() for k in keywords)
            and not any(k in line.lower() for k in ("api_key", "authorization", "password", "secret"))][-100:]
        if not any("cuda" in line.lower() for line in record["relevant_server_log"]):
            raise ValueError("Server logs do not establish CUDA execution")
        if not any("bfloat16" in line.lower() for line in record["relevant_server_log"]):
            raise ValueError("Server logs do not establish BF16 model placement")
        record["status"] = "placement_verified"
    except Exception as exc:
        record["error"] = "{}: {}".format(type(exc).__name__, exc)
    write_json(path, record)
    if record["status"] != "placement_verified":
        raise RuntimeError(record["error"])
    return record
