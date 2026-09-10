#!/usr/bin/env bash
# Read-only; no package installation, model loading, credentials, or full process arguments.
set -u
date -u '+%Y-%m-%dT%H:%M:%SZ'
nvidia-smi --query-gpu=uuid,name,memory.total,memory.used,driver_version --format=csv
nvidia-smi --query-compute-apps=pid,process_name,used_gpu_memory --format=csv
df -h . /tmp
free -h
getconf _NPROCESSORS_ONLN
ps -eo pid,comm
python3 - <<'PY'
import importlib.metadata
import json
import sys
versions = {}
for name in ('vllm', 'torch', 'transformers'):
    try:
        versions[name] = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        versions[name] = None
print(json.dumps({'python': sys.version, 'packages': versions}, sort_keys=True))
PY
