#!/usr/bin/env bash
set -euo pipefail
# Separate Stage 5 service; preserve the historical port-8000 server.
export CUDA_VISIBLE_DEVICES=0
exec .venv/bin/vllm serve Qwen/Qwen2.5-7B-Instruct \
  --revision a09a35458c702b33eeacc393d103063234e8bc28 \
  --tokenizer-revision a09a35458c702b33eeacc393d103063234e8bc28 \
  --dtype bfloat16 --tensor-parallel-size 1 --max-model-len 16384 \
  --max-num-seqs 1 --gpu-memory-utilization 0.4 --enforce-eager \
  --cpu-offload-gb 0 --swap-space 0 --generation-config vllm \
  --seed 20260909 --host 127.0.0.1 --port 8015
