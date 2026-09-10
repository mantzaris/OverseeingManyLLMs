# OverseeingManyLLMs

A reproducible backbone for studying how one simulated human supervisor allocates review time across three LLM agents doing synthetic civilian maintenance tasks. It implements generation, public observations, GPU actions, a review queue, four schedulers, corrective interventions, loss scoring, and independent replay.

Start with the [current GPU report](reports/STAGE1_GPU_LIVE.md), [core method](paper/CORE_METHOD.md), and [proof-of-concept plan](plan/PROOF_OF_CONCEPT_PLAN.md). The current runtime uses an **RTX 6000 Ada**, the pinned **Qwen2.5-7B-Instruct** model, BF16, and zero CPU offloading. Supervision is simulated; error probability is the uncalibrated constant **p=0.5**. The Ada run completed all 49 requests without retries; all four policies tied at loss 0 with 5/6 correct jobs, one review, and no corrections. This stage demonstrates integration, not policy superiority.

## Inspect and verify

Host code requires Python 3.8+ and the standard library. These commands perform no model inference:

```bash
python3 -m unittest discover -s tests -v
python3 -m overseeing mechanics --out artifacts/local-mechanics
python3 -m overseeing replay artifacts/local-mechanics/competition/delay/events.jsonl

task_artifacts=artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z
python3 scripts/verify_live_results.py "$task_artifacts/run"
for policy in fcfs uncertainty myopic delay; do
  python3 -m overseeing replay "$task_artifacts/run/$policy/events.jsonl"
done
```

Use a fresh mechanics output directory on repeat runs. The five examples use **stipulated actions as mechanics fixtures**. Live raw requests/responses, episode CSV, event traces, queue timeline, GPU evidence, exact environment versions, and the executed source snapshot are saved together under [the Ada artifact directory](artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/). The verifier uses that snapshot so later source changes do not invalidate the historical audit.

## Verified GPU setup

In a dedicated pod checkout, the setup used the available Python 3.11.13 and these commands:

```bash
uv venv --python python3.11 .venv
timeout 5400 uv pip install --python .venv/bin/python -r requirements-gpu.txt
HF_HOME="$PWD/model-cache" bash scripts/serve_gpu.sh
```

The launcher serves the pinned model and tokenizer revision `a09a35458c702b33eeacc393d103063234e8bc28` on `127.0.0.1:8000`. It requires one verified L40S or RTX 6000 Ada with at least 45,000 MiB VRAM and native CUDA BF16. The 0.5 memory reservation, tensor parallelism 1, CPU offload 0, and swap 0 are fixed. Keep Jupyter and other existing services running.

The [report](reports/STAGE1_GPU_LIVE.md) records the exact SSH, isolated directory, detached server launch, and one-shot demonstration command, with server PID, logs, and full resolved dependency versions. The live CLI accepts `--continuation stage1_gpu_live_rtx6000_ada`, using its recorded deadline by default or an earlier explicit `--deadline-utc`. It retains the original overall deadline and rejects unknown, expired, or overlong continuation windows. Saved runs cannot be overwritten; the recorded demonstration wrapper also refuses a repeat execution.

## Preserved history and scope

The [original backbone report](reports/STAGE1_GPU_BACKBONE.md), [blocked recovery](reports/STAGE1_GPU_RECOVERY.md), and [first L40S live report](reports/STAGE1_GPU_L40S.md) remain available with their original artifacts. All clocks are retained in [implementation_clock.json](reports/implementation_clock.json).

Calibration, more seeds, additional baselines, larger experiments, and a full manuscript are later work. Weights, environments, and credentials are excluded from Git. Nothing is pushed automatically.
