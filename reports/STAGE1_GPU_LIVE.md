# Stage 1 live GPU demonstration: RTX 6000 Ada

**Real GPU inference succeeded: one placement request and all 48 scheduled experimental calls completed, with 49 attempts, zero retries, and zero failed model requests. All four episodes completed and their scores independently replayed.** Every policy scored loss 0, five of six correct jobs, one completed review, and no corrections. This establishes the working integration, without evidence of policy superiority or a beneficial live correction.

## Runtime and GPU evidence

Direct SSH reused the available identity and authenticated as root to `38.80.152.248:33513`, container `efbc29db9f5f`. No keys or credentials were copied. The dedicated project is `/workspace/OverseeingManyLLMs-rtx6000-ada-20260910T002404Z`, with its own `.venv` and `model-cache`. [Connection record](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/connection.json).

The actual GPU is **NVIDIA RTX 6000 Ada Generation, 49,140 MiB**, initially idle with 1 MiB used. Driver **580.126.20** reports CUDA compatibility 13.0; the actual PyTorch runtime is **CUDA 12.8**. Compute capability **8.9** and native BF16 were verified by executing a BF16 matrix multiplication on `cuda:0`. `nvcc` was absent from PATH, so no toolkit version is inferred from the driver. [Preflight](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/preflight.txt), [runtime verification](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/runtime.json).

The base environment had Python 3.12.3 and torch 2.8.0+cu128, but lacked vLLM and Transformers. The isolated environment used available **Python 3.11.13**, **vLLM 0.10.2**, **torch distribution 2.8.0 / runtime 2.8.0+cu128**, and **Transformers 4.55.2**, installed with uv 0.9.0. All planned dependency pins were retained. [Resolved versions](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/requirements.actual.txt), [installation log](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/install.log).

Model and tokenizer are **Qwen/Qwen2.5-7B-Instruct**, revision **`a09a35458c702b33eeacc393d103063234e8bc28`**. All 11 downloaded files, including four BF16 weight shards, were SHA-256 hashed: **15,242,788,168 bytes** total; only the [hash manifest](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/model_files.json) is committed. Hashing took 15.746 seconds and performs no model inference.

Serving retained BF16, tensor parallelism 1, eager mode, 2048-token model length, one sequence, loopback port 8000, GPU memory utilization **0.5**, CPU offload **0**, and swap **0**. The reservation did not need adjustment. The validator extends the earlier L40S gate to the verified Ada name and still requires one supported GPU with at least 45,000 MiB, native CUDA BF16, the exact pinned serving arguments, and a descendant GPU process with at least 14,000 MiB allocated. Generic `live_gpu` labels now defer actual hardware identity to the placement records.

API server PID **7338** owns GPU engine PID **8449**. The server logs show `device_config=cuda`, `dtype=torch.bfloat16`, `quantization=None`, Flash Attention, and **14.2488 GiB** of loaded weights. Model loading including download took **546.299054 seconds**; shard loading itself took **29.73 seconds**. All model forward passes executed on the GPU, with no CPU inference or offloading. Tokenization, simulation, scoring, logging, and file hashing ran on the host.

Placement was checked [before the request](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/gpu_before.json), [after the request](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/gpu_after_placement.json), and [after the episodes](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/gpu_final.json). The [raw placement response](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/placement_raw_requests.jsonl) was `{"action":"reset_sensor"}`. [Server log](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/server.log), [110 telemetry samples](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/gpu_telemetry.csv). Maximum observed total memory was **25,165 MiB** and utilization **94%** at approximately 200 ms sampling intervals. These are sampled observations, not exact peak memory or kernel-time measurements.

The initial workspace had approximately 70 GB free and the root filesystem 75 GB free; afterward they had approximately 47 GB and 66 GB free. The cgroup reports a 187,999,997,952-byte memory limit and a CPU quota equivalent to 20.4 cores; `free`/processor counts in preflight describe the shared host. Existing nginx, SSH, Jupyter, and their observed service PIDs remain present. At **00:49:30 UTC**, vLLM health was HTTP 200, Jupyter responded HTTP 302, engine memory was **24,618 MiB**, and server counters still totaled **49 generations**. The server is retained, with no further model requests launched. [Final status](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/final_status.json).

## Live configuration and outcomes

The unchanged [Stage 1 configuration](../configs/stage1.json) uses seed **100**, three agents, two jobs each, **12 ticks**, review duration **2**, and the four original policies. Each job receives two fresh independently seeded requests with identical observations: execute the first action and retain the second only for agreement. The estimator stays **provisional and uncalibrated at p=0.5**. Calls are serial and wall latency does not advance simulated time. Scenario hash is `46a0826cab9be11d19cdac899a1febe746c52296070d8ab010bea452c3545e55`.

| Policy | Status | Loss | Correct jobs | Reviews started/completed | Corrections | Expired requests | Replay |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| FCFS | Completed | 0 | 5/6 | 1/1 | 0 | 5 | Verified |
| Uncertainty-first | Completed | 0 | 5/6 | 1/1 | 0 | 5 | Verified |
| Myopic benefit | Completed | 0 | 5/6 | 1/1 | 0 | 5 | Verified |
| Queue-order search | Completed | 0 | 5/6 | 1/1 | 0 | 5 | Verified |

[Episode CSV](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/episodes.csv), [queue timeline](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/queue_timeline.md), and readable traces for [FCFS](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/fcfs/trace.md), [uncertainty-first](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/uncertainty/trace.md), [myopic benefit](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/myopic/trace.md), and [queue-order search](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/delay/trace.md). Each policy directory also retains `raw_requests.jsonl`, `events.jsonl`, and `replay.json`.

All four actual proposal, review, and closure trajectories matched. At tick 0, `a0j0` proposed the correct `reset_sensor` action and began review. Completion at tick 2 confirmed it; there was no correction. `a1j0` proposed `replace_filter` in both samples despite its sensor fault and closed wrong at tick 1. Both of that job's costs were zero, explaining zero loss despite imperfect accuracy. The other five jobs closed correctly. Wrong valid actions were preserved without retry, vote, or truth-based repair.

Each policy had four agreeing sample pairs, two supervisor-busy ticks, zero late returns, three zero-value expiries, two infeasible-at-arrival expiries, and no expiry classified as opportunity lost while waiting. Only one request offered positive review benefit at dispatch. Constant probabilities make uncertainty-first rank like FCFS for matching queues. Delay-aware minus myopic loss is **0**; one seed provides no general policy-effect estimate or meaningful scenario-level confidence interval.

## Mechanics and information boundaries

**21 focused tests passed on the pod**, covering generator/observation boundaries, future-job exclusion, feedback timing and isolation, review ordering and deadline equality, late returns, independent score replay, unknown failed outcomes, two-sample behavior, retry/token accounting, fixed scope, continuation bounds, and CUDA/BF16/model/offload gates. [Captured test output](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/focused_checks.txt).

All **20 fixture-policy runs** also passed and independently replayed. Their actions are explicitly **stipulated mechanics fixtures**, with zero model calls; their engineered outcomes are not empirical policy evidence.

| Mechanics fixture | FCFS loss | Uncertainty loss | Myopic loss | Queue-search loss |
| --- | ---: | ---: | ---: | ---: |
| Correct action (`easy`) | 0 | 0 | 0 | 0 |
| Correctable mistake | 2 | 2 | 2 | 2 |
| Competing reviews | 0 | 0 | 8 | 0 |
| Expired opportunity | 9 | 9 | 9 | 9 |
| Baseline wins | 0 | 12 | 12 | 12 |

[Mechanics CSV](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/mechanics/episodes.csv), [summary](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/mechanics/summary.json), [competition timeline](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/mechanics/queue_timeline.md). Further arithmetic checks retain unreviewed loss 13, deadline-equality loss 6 with prior downtime preserved, and forced-late loss 9 with no reopening.

Schedulers still receive only immutable public records for currently released requests. They never receive hidden faults, future jobs, or accrued scorer loss. Definitive diagnostic feedback enters only when a review completes, and only that agent's history receives it. Full truth in saved scorer traces remains offline diagnostic data. The [core-method note](../paper/CORE_METHOD.md) describes the implemented mechanism, loss, and idealizations: simulated perfect supervision, fixed review duration, automatic admission, and mandatory compliance.

## Calls, timing, and failures

| Work | Scheduled / attempts | Retries | Prompt tokens | Output tokens | Request wall seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Placement | 1 / 1 | 0 | 195 | 7 | 3.373192 |
| FCFS | 12 / 12 | 0 | 2,508 | 84 | 1.689429 |
| Uncertainty-first | 12 / 12 | 0 | 2,508 | 84 | 1.682490 |
| Myopic benefit | 12 / 12 | 0 | 2,508 | 84 | 1.673245 |
| Queue-order search | 12 / 12 | 0 | 2,508 | 84 | 1.675321 |
| Total | 49 / 49 | 0 | 10,227 | 343 | 10.093677 |

No token counts are unknown. Experimental request wall time was **6.720485 seconds**, mean **0.140010 seconds**, nearest-rank p95 **0.142555 seconds**, and approximately **50.00 output tokens/second** of experimental request wall time. These measurements describe this tiny warmed run, not a larger-study forecast. The live CLI ran **00:47:35.588437–00:47:56.907411 UTC** in **21.319011 seconds**; the telemetry wrapper took **22.373845 seconds**. [Accounting](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/accounting.json), [exact invocation and exit code](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/execution.json).

Every generation attempt retained its request, seed, response, usage, phase, and latency. The existing 60-second shared tokenization/generation attempt deadline and maximum of one retry remained unchanged. The limits were 48 scheduled experimental calls / at most 96 attempts, plus one placement call / at most two attempts. Actual usage was 48/48 plus 1/1. There were no malformed, truncated, timed-out, or failed model responses.

[Before](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/metrics_before.txt), [after](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/metrics_after.txt), and [final](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/metrics_final.txt) server metrics independently confirm 49 successful generations, zero length/abort completions, and the token totals. vLLM's default GPU prefix cache recorded 9,520 hit tokens; prompt accounting includes cached prefixes. All 49 generations were fresh requests, with no saved-response substitution. Internal GPU profiling/warmup and small BF16 verification kernels are additional GPU work, separate from user generation-call counts.

Setup prepared 147 packages in 91 seconds and installed them in 362 seconds. Persistent-volume copies and model downloads were slow but completed on the first installation and server launch. Nonfatal messages reported cross-filesystem hardlink fallback and use of PyTorch-native sampling because optional FlashInfer was absent; CUDA model execution and Flash Attention remained active. A local test-edit `NameError` was corrected before source freeze; all final focused checks passed. [Setup notes](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup_notes.json).

## Clocks and preservation

This separately authorized continuation, **`stage1_gpu_live_rtx6000_ada`**, started **2026-09-10 00:24:04 UTC**, with hard deadline **02:24:04 UTC**. Setup to observed server readiness took **1,411.100462 seconds**. All setup, waiting, checks, inference, and reporting count toward this stage. The original implementation start **2026-09-09 15:38:57 UTC**, original four-hour Stage 1 deadline **19:38:57 UTC**, overall **36-hour** budget, and overall deadline **2026-09-11 03:38:57 UTC** remain unchanged. At this continuation's start, overall elapsed time was **31,507 seconds**, with **98,093 seconds** remaining. [Implementation clock](implementation_clock.json), [separate continuation clock](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/continuation_clock.json).

The CLI selects an explicitly recorded continuation and can derive its deadline when `--deadline-utc` is omitted. An explicit deadline may only shorten that window; two-hour and original overall caps still apply. It rejects unknown, unzoned, expired, or extended windows and preserves existing outputs.

All **154 historical artifact files** and previous clock records are preserved. The earlier live report is copied byte-for-byte to [STAGE1_GPU_L40S.md](STAGE1_GPU_L40S.md); the [original backbone](STAGE1_GPU_BACKBONE.md) and [blocked recovery](STAGE1_GPU_RECOVERY.md) reports remain unchanged. The updated verifier also passed on the old L40S artifacts against their original source. [Preservation audit](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/history_preservation.json), [historical-result audit](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/historical_result_verification.json).

Provider allocation start/end, billed intervals, hourly rate, and charges are **unknown**. The observed container-process start, **00:13:33 UTC**, is not a billing timestamp. The previous A100 rate is not applied to the Ada. Allocation remains open beyond the generation interval.

## Reproduction commands

The exact successful SSH options were:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=12 -o StrictHostKeyChecking=yes \
  -o UserKnownHostsFile=/tmp/runpod-nfx7q9p6vf4g8q-known_hosts \
  -p 33513 root@38.80.152.248
```

Source was copied into a new dedicated pod directory using SSH/tar with `--no-same-owner`; no private keys, model weights, environments, or unrelated project files were transferred as source. From that pod checkout, setup and detached startup used:

```bash
cd /workspace/OverseeingManyLLMs-rtx6000-ada-20260910T002404Z
task_artifacts=artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z
bash scripts/pod_preflight.sh > "$task_artifacts/setup/preflight.txt"
uv venv --python python3.11 .venv
timeout 5400 uv pip install --python .venv/bin/python -r requirements-gpu.txt \
  > "$task_artifacts/setup/install.log" 2>&1
.venv/bin/python "$task_artifacts/start_server.py"
```

For exact dependency reconstruction, use `uv pip install --python .venv/bin/python -r "$task_artifacts/run/requirements.actual.txt"` in a fresh Python 3.11.13 environment. The [startup wrapper](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/start_server.py) checks that port 8000 is available, sets project-local `HF_HOME`, invokes [serve_gpu.sh](../scripts/serve_gpu.sh) in its own process session, and saves its PID and log. The expanded model launch is:

```bash
CUDA_VISIBLE_DEVICES=0 HF_HOME="$PWD/model-cache" .venv/bin/vllm serve Qwen/Qwen2.5-7B-Instruct \
  --revision a09a35458c702b33eeacc393d103063234e8bc28 \
  --tokenizer-revision a09a35458c702b33eeacc393d103063234e8bc28 \
  --dtype bfloat16 --tensor-parallel-size 1 --max-model-len 2048 \
  --max-num-seqs 1 --gpu-memory-utilization 0.5 --enforce-eager \
  --cpu-offload-gb 0 --swap-space 0 --generation-config vllm \
  --seed 20260909 --host 127.0.0.1 --port 8000
```

After health returned HTTP 200, the actual demonstration wrapper was `.venv/bin/python "$task_artifacts/execute_demo.py"`. It executed:

```bash
.venv/bin/python -m overseeing demo --config configs/stage1.json \
  --out "$task_artifacts/run" --server-pid 7338 \
  --server-log "$task_artifacts/setup/server.log" \
  --continuation stage1_gpu_live_rtx6000_ada \
  --deadline-utc 2026-09-10T02:24:04+00:00
```

These are the historical one-shot execution commands. The saved wrappers refuse existing PID/log/execution files, output directories cannot be overwritten, and the recorded deadline is enforced. This stage's single live demonstration is complete. The following checks and replay are repeatable from the repository root with **no inference**:

```bash
python3 -m unittest discover -s tests -v
python3 -m overseeing mechanics --out artifacts/local-mechanics
python3 -m overseeing replay artifacts/local-mechanics/competition/delay/events.jsonl

task_artifacts=artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z
python3 scripts/verify_live_results.py "$task_artifacts/run"
for policy in fcfs uncertainty myopic delay; do
  python3 -m overseeing replay "$task_artifacts/run/$policy/events.jsonl"
done
python3 "$task_artifacts/summarize.py"
```

The verifier passed both on the pod and after transfer, checking source/configuration hashes, GPU evidence, paired samples, primary action execution, request seeds, serial calls, attempt/token totals, server metrics, and all four replayed scores. [Pod verification](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/result_verification.json), [local verification](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/local_result_verification.json), [executed source snapshot](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/source/), [source/configuration hashes](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/source_files_sha256.json). Captured logs and raw model responses are retained verbatim; no weights or environments are committed.

The next useful step is a separately predeclared development calibration batch estimating first-sample error by whether the two actions agree. No calibration, additional seeds, baselines, larger evaluation, advanced tasks, or full manuscript drafting ran in this continuation. Relevant code, documentation, and compact results are committed directly on `main`; nothing is pushed.

Report checkpoint: **2026-09-10T00:56:55.849320+00:00**, **1971.849 seconds** (32.86 minutes) after continuation start. Overall elapsed time was **33478.849 seconds**, with **96121.151 seconds** remaining. The task commit's committer timestamp marks final Git completion.
