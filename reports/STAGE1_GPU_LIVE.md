# First live GPU demonstration

**Completed on the L40S: 49 successful model-generation requests, comprising one placement request and 48 experimental requests. No retries or failed inference attempts occurred. All four policies completed and independently replayed.** Each scored loss 0 and 5/6 correct jobs. This establishes live integration, with no evidence of policy superiority or a beneficial live correction.

## Authorization and connection

The continuation began **2026-09-09 23:42:54 UTC**, with a two-hour deadline of **2026-09-10 01:42:54 UTC**. The original Stage 1 deadline, **2026-09-09 19:38:57 UTC**, and overall deadline, **2026-09-11 03:38:57 UTC**, remain intact. The CLI now requires `--continuation stage1_gpu_live` to select this explicitly recorded authorization. It rejects an unknown continuation, an expired deadline, a continuation exceeding two hours, or a deadline beyond the overall cap. See [implementation clock](implementation_clock.json) and [continuation record](../artifacts/stage1_gpu_live/continuation_clock.json).

An interactive SSH gateway session authenticated from this execution environment to `077o8p8te96mml-644115d4@ssh.runpod.io`, reaching `root@8fa682f09541`. Socket creation was permitted. The pod's effective SSH configuration enabled public-key authentication and used `/root/.ssh/authorized_keys`. The authorized local RSA public key was missing; it was appended, preserving the original five bytes. Ownership is root:root; directory/file modes are 0700/0600. SSH configuration and existing authentication methods were preserved.

The gateway-observed ED25519 host fingerprint and independently scanned direct endpoint fingerprint both were **`SHA256:BuwepStKo/u/bR7fuRmbGdMlPeeSEMoPzkTgGd6E+Gc`**. Only after comparison, direct SSH to `root@209.170.80.132:19211` used strict host checking and public-key-only authentication. SCP then transferred source and small evidence files. No private-key contents were displayed or transferred as data; no keys or credentials are included in this commit. [Connection record](../artifacts/stage1_gpu_live/connection.json).

## Actual hardware and runtime

The pod confirmed one **NVIDIA L40S, 46,068 MiB**, initially with 0 MiB allocated and no GPU processes. Driver **580.159.04** reports CUDA compatibility 13.0. Actual inference uses **PyTorch CUDA runtime 12.8**, independently verified by executing a BF16 matrix operation on `cuda:0`. Compute capability is **8.9**. `nvcc` was absent from PATH; no installed CUDA toolkit version is claimed.

The base environment had Python 3.12.3 and PyTorch 2.8.0+cu128, with no vLLM or Transformers. An isolated environment was installed under `/workspace/OverseeingManyLLMs-stage1-live-20260909T234254Z/.venv` using available Python **3.11.13**. Actual pins are **vLLM 0.10.2, torch distribution 2.8.0 / runtime 2.8.0+cu128, Transformers 4.55.2**. [Resolved package versions](../artifacts/stage1_gpu_live/run/requirements.actual.txt), [installation log](../artifacts/stage1_gpu_live/setup/install.log), and [preflight](../artifacts/stage1_gpu_live/setup/preflight.txt) are retained.

The root filesystem had approximately 75 GiB free initially and 66 GiB after installation. `/workspace` reported 383 TiB free on its shared filesystem; this is filesystem capacity, not a verified account quota. Existing nginx, SSH, Jupyter, and terminal services were preserved. Port 8000 was available.

Model and tokenizer: **`Qwen/Qwen2.5-7B-Instruct`**, revision **`a09a35458c702b33eeacc393d103063234e8bc28`**. SHA-256 hashes were computed from every downloaded model/tokenizer file, including all four weight shards; only the [hash manifest](../artifacts/stage1_gpu_live/model_files.json) is committed. Weights, environment, and caches remain on the pod.

Serving uses BF16, one GPU, tensor parallelism 1, eager mode, model length 2048, one sequence, GPU memory utilization 0.5, CPU offload **0**, swap **0**, and loopback port 8000. Requests retain temperature 0.3, top-p 1, schema-constrained JSON, 1024 input/48 output token limits, and a shared 60-second attempt budget. No inference configuration was changed after seeing results.

## Placement and execution evidence

The validator now requires one L40S with at least 45,000 MiB total memory. It still verifies the exact server arguments, a descendant serving process with at least 14,000 MiB GPU allocation, CUDA/BF16 logs, and successful native BF16 execution. Evidence was collected [before inference](../artifacts/stage1_gpu_live/run/gpu_before.json), [after placement](../artifacts/stage1_gpu_live/run/gpu_after_placement.json), and [after the demonstration](../artifacts/stage1_gpu_live/run/gpu_final.json).

API server PID **97762** owns engine PID **98651**, observed with **23,050 MiB** GPU allocation. The server reports **14.2488 GiB** of model weights loaded in **25.624858 seconds**, `dtype=torch.bfloat16`, `device_config=cuda`, and no quantization. The successful placement response was `{"action":"reset_sensor"}`. [Raw placement request/response](../artifacts/stage1_gpu_live/run/placement_raw_requests.jsonl) and [server log](../artifacts/stage1_gpu_live/setup/server.log) preserve this evidence.

The live CLI ran **23:51:28.703447–23:51:47.237581 UTC**, completing in **18.534152 seconds**, including placement and GPU checks. The wrapper took **19.393477 seconds**. [Exact invocation and exit code 0](../artifacts/stage1_gpu_live/execution.json).

## Four policy outcomes

Exactly seed **100**, three agents with two jobs each, **12 simulated ticks**, review duration **2**, and each original policy once. Each job received two fresh independently seeded generation requests: the first action executed; the second measured agreement only. Provisional error probability stayed **0.5**. Inference latency never advanced simulated time. Scenario hash: `46a0826cab9be11d19cdac899a1febe746c52296070d8ab010bea452c3545e55`.

| Policy | Status | Loss | Correct jobs | Reviews completed | Corrections | Expired requests | Calls / retries | Replay |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| FCFS | Completed | 0 | 5/6 | 1 | 0 | 5 | 12 / 0 | Verified |
| Uncertainty-first | Completed | 0 | 5/6 | 1 | 0 | 5 | 12 / 0 | Verified |
| Myopic benefit | Completed | 0 | 5/6 | 1 | 0 | 5 | 12 / 0 | Verified |
| Delay-aware queue search | Completed | 0 | 5/6 | 1 | 0 | 5 | 12 / 0 | Verified |

All four used two supervisor-busy ticks and had zero late returns. Their action and queue trajectories matched. Delay-aware minus myopic loss is **0**. There is one scenario, so no confidence interval or generalization claim is warranted. Constant p=0.5 also makes uncertainty-first rank the same as FCFS when queues match. [Outcome CSV](../artifacts/stage1_gpu_live/run/episodes.csv).

Readable complete traces: [FCFS](../artifacts/stage1_gpu_live/run/fcfs/trace.md), [uncertainty-first](../artifacts/stage1_gpu_live/run/uncertainty/trace.md), [myopic](../artifacts/stage1_gpu_live/run/myopic/trace.md), [delay-aware](../artifacts/stage1_gpu_live/run/delay/trace.md), and [queue timeline](../artifacts/stage1_gpu_live/run/queue_timeline.md). Each directory retains `events.jsonl`, `raw_requests.jsonl`, and `replay.json`.

The common trace is easy to inspect:

| Tick | Event and implication |
| --- | --- |
| 0 | `a0j0` proposes reset_sensor; its second sample disagrees. Review starts and is due at 2. `a1j0` proposes replace_filter in both samples. |
| 1 | `a1j0` closes **wrong**: its true fault is sensor. Both costs are zero, so measured loss is zero. Its request expires. `a2j0` arrives with a correct first sample and a disagreeing second sample. |
| 2 | Review confirms `a0j0` was already correct; no action changes. `a2j0` closes correctly and its zero-value request expires. |
| 5 | `a0j0` closes correctly. |
| 6–7 | `a1j1` arrives and closes correctly; its one-tick window prevents a useful two-tick review. |
| 7–9 | `a0j1` and `a2j1` arrive and close correctly. Their earliest review completions prevent no cost, so both requests expire unserved. |
| 12 | Finalization; six jobs closed, one review completed, no residual service. |

Per policy, expiries comprise **three zero-value** and **two infeasible-at-arrival** requests; none is classified as an opportunity lost while waiting. All policies faced only one job with positive review value at dispatch. The wrong, agreeing `a1j0` response is retained in every run. No valid wrong action was retried, voted away, repaired using truth, or replaced. Four of six sample pairs agreed per policy; this is descriptive agreement, not a calibrated reliability estimate.

## Calls, tokens, and allocation accounting

| Work | Scheduled / attempted | Retries | Prompt tokens | Output tokens | Request wall seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Placement | 1 / 1 | 0 | 195 | 7 | 3.281524 |
| FCFS | 12 / 12 | 0 | 2,508 | 84 | 1.926142 |
| Uncertainty-first | 12 / 12 | 0 | 2,508 | 84 | 1.894538 |
| Myopic | 12 / 12 | 0 | 2,508 | 84 | 1.904642 |
| Delay-aware | 12 / 12 | 0 | 2,508 | 84 | 1.900884 |
| **Total** | **49 / 49** | **0** | **10,227** | **343** | **10.907731** |

No token counts are unknown. Experimental requests alone took **7.626206 seconds**; the four simulator runs took **8.926765 seconds**. Mean experimental request latency was **0.158879 seconds**, nearest-rank p95 **0.163364 seconds**, and aggregate experimental output throughput **44.06 tokens/second** of request wall time. These describe this warmed, tiny run, not a larger-study forecast.

The server's [before](../artifacts/stage1_gpu_live/metrics_before.txt)/[after](../artifacts/stage1_gpu_live/metrics_after.txt) counters independently confirm **49 successful generations**, zero aborts/truncations, and the token totals. vLLM's default prefix caching was enabled and recorded **9,520 prefix-cache hit tokens**. Prompt totals therefore count API-accounted input, including cached prefixes. Every generation was a fresh request with a fresh response; no completed-response cache substituted policy calls. Internal model profiling/warmup and small BF16 validation kernels are additional GPU work, not user generation requests or metered output tokens.

[GPU telemetry](../artifacts/stage1_gpu_live/gpu_telemetry.csv) contains **95 samples** at approximately 200 ms intervals covering the run. Maximum observed total memory was **23,596 MiB**, including the CLI's CUDA validation context; maximum observed utilization was **97%**. These samples are not exact peak memory or kernel-time measurements. [Accounting summary](../artifacts/stage1_gpu_live/accounting.json).

The container's observed process start was **2026-09-09 17:53:28 UTC**; that is not a provider billing timestamp. Provider allocation start/end, hourly rate, billable intervals, and charges are unknown. The former A100 rate is not applied to this L40S. Allocation remains open and includes setup, idle time, and time outside this demonstration.

## Verification, setup repairs, and reproduction

**11 focused tests passed**, covering L40S memory/placement/offload rejection, continuation bounds, fixed demonstration scope, first/second sample behavior, and retry/timeout accounting. Shell syntax and source whitespace checks passed; captured metrics and server logs preserve upstream trailing whitespace. [Test output](../artifacts/stage1_gpu_live/focused_checks.txt). The [saved-results audit](../scripts/verify_live_results.py) confirms all four independent replays, 48 scheduled experimental calls, valid request settings and seeds, primary-action execution, serial requests, token totals, server counters, and executed source hashes. [Verification result](../artifacts/stage1_gpu_live/result_verification.json).

Setup-only errors were repaired before or after inference without repeating the live demonstration: unavailable local encoding helper, tar ownership preservation unsupported on the persistent filesystem, a synthetic-test mock interaction, and an SCP `/.` source rejection. Details are retained in [setup notes](../artifacts/stage1_gpu_live/setup_notes.json). Installation and the first model-server launch succeeded; no runtime compatibility replacement or failed model request occurred. All prior Stage 1 and recovery artifacts/reports remain unchanged.

Reproduce verification locally, with **no inference**:

```bash
PYTHONPATH=tests python3 -m unittest -v test_live_gpu test_backbone.ResponseChecks \
  test_backbone.BackboneChecks.test_gpu_gate_rejects_non_l40s_before_any_request \
  test_backbone.BackboneChecks.test_cli_rejects_expanded_scenario_or_calibration
python3 scripts/verify_live_results.py artifacts/stage1_gpu_live/run
for policy in fcfs uncertainty myopic delay; do
  python3 -m overseeing replay "artifacts/stage1_gpu_live/run/$policy/events.jsonl"
done
```

The actual isolated installation commands, from the pod checkout, were:

```bash
cd /workspace/OverseeingManyLLMs-stage1-live-20260909T234254Z
uv venv --python python3.11 .venv
timeout 5400 uv pip install --python .venv/bin/python -r requirements-gpu.txt
```

The full resolved package list is saved for environment reconstruction. The server was started with `bash scripts/serve_gpu.sh` in a detached process session, with `HF_HOME=/workspace/OverseeingManyLLMs-stage1-live-20260909T234254Z/model-cache`; the launcher contains every vLLM argument. The exact executed demonstration command was:

```bash
.venv/bin/python -m overseeing demo --config configs/stage1.json \
  --out artifacts/stage1_gpu_live/run --server-pid 97762 \
  --server-log artifacts/stage1_gpu_live/setup/server.log \
  --continuation stage1_gpu_live --deadline-utc 2026-09-10T01:42:54+00:00
```

[execute_demo.py](../artifacts/stage1_gpu_live/execute_demo.py) is the exact executed wrapper, including telemetry, metrics snapshots, deadline timeout, and refusal to overwrite this run. These are historical reproduction commands, not authorization to run another demonstration: the existing output is protected, and the deadline remains enforced. Future inference requires its own authorization and a fresh output directory.

## Final status and limits

At **2026-09-09 23:54:04 UTC**, the server remained healthy (HTTP 200), PID 97762 with GPU engine 98651 resident at 23,050 MiB; generation counters still totaled 49. [Final status](../artifacts/stage1_gpu_live/final_status.json). The pod, isolated environment, model cache, and persistent source/evidence files are preserved. No existing services were stopped. Only the temporary telemetry process was stopped.

This demonstrates real BF16 GPU proposals driving the simulator, queue, review confirmation, scoring, logging, and replay. It does **not** demonstrate a live beneficial correction, distinguish queue policies, calibrate uncertainty, or establish realistic human supervision. Review is perfect and mandatory by construction. Fixed seeds do not promise identical future GPU outputs. No calibration, extra seeds, larger evaluation, or new policy development ran.

The smallest next research step is a separately authorized, predeclared calibration batch on development scenarios to estimate first-sample error separately for agreeing and disagreeing pairs. The retained wrong-but-agreeing action motivates that check. No further GPU work was launched. Task changes and small artifacts are committed on `main`; nothing is pushed.

Report checkpoint: **2026-09-09T23:57:40.560414+00:00**, **886.56 seconds** after continuation start. The task commit timestamp marks final Git completion.
