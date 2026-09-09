#!/usr/bin/env bash
set -euo pipefail
# Run only on the allocated pod after preflight. Does not install packages or stop services.
# Use the same venv for the server and CLI. Redirect stdout/stderr to a retained log.
task_python="${OVERSIGHT_PYTHON:-.venv/bin/python}"
export CUDA_VISIBLE_DEVICES=0
"$task_python" -c 'import csv; from overseeing.gpu import output, validate_hardware, cuda_runtime_evidence; validate_hardware(list(csv.reader(output(["nvidia-smi", "--query-gpu=uuid,name,memory.total", "--format=csv,noheader,nounits"]).splitlines(), skipinitialspace=True))); print(cuda_runtime_evidence())'
exec "$(dirname "$task_python")/vllm" serve Qwen/Qwen2.5-7B-Instruct \
  --revision a09a35458c702b33eeacc393d103063234e8bc28 \
  --tokenizer-revision a09a35458c702b33eeacc393d103063234e8bc28 \
  --dtype bfloat16 --tensor-parallel-size 1 --max-model-len 2048 \
  --max-num-seqs 1 --gpu-memory-utilization 0.5 --enforce-eager \
  --cpu-offload-gb 0 --swap-space 0 --generation-config vllm \
  --seed 20260909 --host 127.0.0.1 --port 8000
