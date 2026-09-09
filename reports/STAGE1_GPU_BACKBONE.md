# Stage 1: local backbone verified; GPU demonstration blocked

The minimal backbone is implemented and its focused mechanics checks pass. **Real GPU inference did not run, and end-to-end GPU integration has not been demonstrated.** The authorized fallback was used: complete useful local scaffolding, retain honest blocked outcomes, and stop after committing this stage.

## Clock and connection

Stage 1 and the overall implementation clock started **2026-09-09 15:38:57 UTC**. At the report checkpoint, **16:09:59 UTC**, elapsed time was **1,862 seconds (31 minutes 2 seconds)**, including connection checks, implementation, verification, and artifact preparation. The Stage 1 commit's committer timestamp records the final Git step. The hard stage deadline remains **2026-09-09 19:38:57 UTC**; the overall 36-hour deadline remains **2026-09-11 03:38:57 UTC**. These clocks do not reset after retries or between stages; see [implementation_clock.json](implementation_clock.json).

One direct SSH attempt used batch mode, strict host-key checking, no host-key updates, and an eight-second connection timeout. It returned exit code 255:

```text
Warning: Identity file /home/resort/.ssh/id_ed25519 not accessible: No such file or directory.
socket: Operation not permitted
ssh: connect to host 154.54.102.29 port 12448: failure
```

The existing SSH agent also returned `Operation not permitted`. The required key is absent, and permitted connectivity was not established. No gateway retry, access bypass, package installation, model download, or compatibility repair was attempted. No credentials or authentication files were copied. Exact observations are in [connection.json](../artifacts/stage1/connection.json).

Pod GPU/driver, free memory/disk, installed packages, and existing processes remain unverified. **Final inference-server status: unknown because the pod is unreachable.** No service was started, stopped, or modified, and the pod and its persistent files were untouched.

Allocation start/end, billed hours, and charge are **unknown**. Zero request time does not imply zero allocation time. The user quoted $1.59/hour; no actual charge is inferred from local work duration. Allocation may include time before and after this stage.

## Implementation and verification

[overseeing/](../overseeing/) provides deterministic synthetic jobs, separate public observation/request records, independent agent histories, the four schedulers, a serial vLLM client, simulated supervision, scoring, JSONL logs, independent score replay, and a small CLI. There is no calibration/evaluation entry point, agent framework, dashboard, training, or CPU inference implementation.

The event order is completion → closure → arrival/proposals → dispatch → interval scoring. Timely simulated supervision commands the correct action; the controller obeys and records feedback only in that agent's history. Existing downtime remains charged. Schedulers receive immutable public records, and accrued loss stays out of observations. The live path fixes `p(error)=0.5`: it is **not calibrated**, and uncertainty-first has the same ranking as FCFS when their queues match.

The client makes two independently seeded calls with identical observations, executes the first action, and records agreement with the second. It uses the pinned model, strict one-field JSON, 1,024 input/48 output token limits, serial calls, a shared 60-second tokenization/generation attempt budget, and at most one retry. Wrong valid actions are accepted. Invalid responses, request payloads, tokenization metadata, attempt phases, response IDs, usage, and latency are retained; missing token usage remains explicitly unknown. Model-call caps and the recorded wall deadline are enforced. Host tokenization calls are not LLM forward passes.

The pod-only live command requires evidence of the A100, the exact serving arguments, descendant serving processes with at least 14,000 MiB allocated on that GPU, and CUDA server logs. It saves placement evidence before/after the separate real request, actual installed version pins, and final server evidence. This path is implemented but **untested against the pod**. The client follows the [versioned vLLM protocol](https://github.com/vllm-project/vllm/blob/v0.10.2/vllm/entrypoints/openai/protocol.py).

**14 focused tests passed** in the last recorded test run (0.122 seconds), covering all five fixtures, deadline equality, forced late return, unreviewed arithmetic, hidden-state mutation, history isolation/resets, score-corruption detection, incomplete outcomes, GPU rejection, fixed stage scope, structured-response retry behavior, and a shared attempt deadline. HTTP tests use synthetic responses in temporary files; they are not GPU evidence. Shell syntax checks passed. See [checks.json](../artifacts/stage1/checks.json) and [tests](../tests/test_backbone.py).

The saved mechanics package contains 20 fixture/policy runs and 20 successful independent replays. Expected losses are:

| Stipulated fixture only | FCFS | Uncertainty | Myopic | Queue-order search |
| --- | ---: | ---: | ---: | ---: |
| Easy | 0 | 0 | 0 | 0 |
| Correctable | 2 | 2 | 2 | 2 |
| Competition | 0 | 0 | 8 | 0 |
| Expiry | 9 | 9 | 9 | 9 |
| Baseline wins | 0 | 12 | 12 | 12 |

Additional checks verify unreviewed loss 13, deadline-equality loss 6 with earlier downtime preserved, and forced-late loss 9 with no reopening. These are arithmetic checks, not empirical LLM-policy comparisons.

## Authorized live scenario and accounting

The seed-100 exogenous scenario was generated locally and saved identically for all four planned runs: three agents, two jobs each, 12 ticks, and review duration two. No policy episode with live proposals started.

| Policy | Status | Task loss / correct jobs | Planned calls | Scheduled calls | Attempts | Prompt / output tokens |
| --- | --- | --- | ---: | ---: | ---: | --- |
| FCFS | Blocked | Unknown / unknown | 12 | 0 | 0 | 0 / 0 |
| Uncertainty-first | Blocked | Unknown / unknown | 12 | 0 | 0 | 0 / 0 |
| Myopic benefit | Blocked | Unknown / unknown | 12 | 0 | 0 | 0 / 0 |
| Queue-order search | Blocked | Unknown / unknown | 12 | 0 | 0 | 0 / 0 |

**Experimental total:** 48 planned, **0 scheduled, 0 attempts, 0 tokens, 0 seconds inference-request time**. **Separate placement check:** one planned, **0 scheduled, 0 attempts, 0 tokens**. No inference failures or raw GPU responses exist because no inference was attempted. The empty raw-response files intentionally reflect this. All live task outcomes are blank/null, never zero-loss successes. The 0.005287-second blocked-record command duration in its manifest is artifact-writing time, not experiment or allocation runtime. There is no measured GPU throughput or timing pilot.

## Reviewable artifacts

* [Live CSV](../artifacts/stage1/live/episodes.csv), [manifest](../artifacts/stage1/live/manifest.json), and [readable status trace](../artifacts/stage1/live/trace.md). Each policy subdirectory contains a blocked JSONL trace and empty `raw_requests.jsonl`; the placement log is also empty.
* [Mechanics CSV](../artifacts/stage1/mechanics/episodes.csv), [summary](../artifacts/stage1/mechanics/summary.json), and [compact queue timeline](../artifacts/stage1/mechanics/queue_timeline.md). Each fixture/policy directory contains `events.jsonl`, `trace.md`, and `replay.json`; for example, [competition/search](../artifacts/stage1/mechanics/competition/delay/trace.md).
* [Fixed configuration](../configs/stage1.json), [runtime pins](../requirements-gpu.txt), source-file hashes in both manifests, and the clock/connection/check records above. Full scenario truth in `scenario.scorer-only.json` and event headers is diagnostic data; it is not serialized into model or scheduler inputs.

The artifacts are approximately 200 KB of file contents. No weights, environments, caches, or credentials are included.

## Reproduction and next stage

Actual host runtime was **Python 3.8.10**, using only the standard library. Reproduce local checks and saved scoring from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 -m overseeing mechanics --out artifacts/local-mechanics
python3 -m overseeing replay artifacts/local-mechanics/competition/delay/events.jsonl
python3 -m overseeing record-blocked --config configs/stage1.json \
  --connection artifacts/stage1/connection.json --out artifacts/local-blocked
```

The blocked command exits 2 intentionally. Output directories must be new; earlier traces are preserved.

The unexecuted GPU target remains **Qwen/Qwen2.5-7B-Instruct**, revision **`a09a35458c702b33eeacc393d103063234e8bc28`**, **BF16**, with **vLLM 0.10.2 / PyTorch 2.8.0 / Transformers 4.55.2 / Python 3.11**. Actual pod runtime/driver versions are unknown. Reuse a compatible installation after preflight; otherwise the isolated setup and bounded reproduction command, to run on the pod once access is available, are:

```bash
mkdir -p artifacts/gpu-stage1
bash scripts/pod_preflight.sh > artifacts/gpu-stage1/preflight.txt
# If a compatible environment is not already present:
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements-gpu.txt
# After checking that port 8000 is available and preserving unrelated services:
bash scripts/serve_gpu.sh > artifacts/gpu-stage1/server.log 2>&1 &
task_server_pid=$!
# Once this server's log confirms readiness:
.venv/bin/python -m overseeing demo --config configs/stage1.json \
  --out artifacts/gpu-stage1/run --server-pid "$task_server_pid" \
  --server-log artifacts/gpu-stage1/server.log \
  --deadline-utc 2026-09-09T19:38:57+00:00
```

This command performs only one placement request and the four seed-100 runs, with at most 96 experimental attempts plus two placement attempts. It leaves the server running and preserves files. The committed deadline is enforced and cannot be extended past the original stage/overall limits by a CLI flag. No GPU command above was executed in this operation.

No unresolved mechanics defect was observed. GPU runtime compatibility, real response behavior, token counts/latency, and model decision quality remain unverified; fixed seeds also do not guarantee bitwise-identical live generations. Perfect mandatory simulated correction and provisional error estimates limit later scientific claims. No policy superiority is established.

The smallest next step is the **same placement check and 48-call seed-100 demonstration from an environment with existing credentials and permitted SSH connectivity**, within the remaining authorized clock. Review its real traces and replay before considering calibration. The plan now notes the future greedy `p_i G_i(t+s_i)` baseline and required matrix/forecast update; it is not added to this stage. No development matrix, calibration, frozen evaluation, or broader workflow was launched. Nothing was pushed.
