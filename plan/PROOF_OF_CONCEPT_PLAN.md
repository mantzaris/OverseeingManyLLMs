# First GPU proof of concept

Proposed for external review, 2026-09-09. Planning only; implementation requires subsequent authorization. Its single 36-hour clock includes setup and failed attempts.

**Implementation note, 2026-09-10:** The user subsequently authorized bounded Stage 1 continuations. The original A100 allocation assumptions below are historical. The current pod has one verified **RTX 6000 Ada Generation (49,140 MiB, compute capability 8.9)**; the prior completed continuation used an L40S. The implementation supports these two verified 48 GB GPUs with native CUDA BF16 and the same pinned model, one-GPU serving, 0.5 memory reservation, and zero CPU offload/swap. See the [current report](../reports/STAGE1_GPU_LIVE.md), [preserved L40S report](../reports/STAGE1_GPU_L40S.md), and [unchanged overall clock plus separate continuation records](../reports/implementation_clock.json). The larger experiment matrix and later CLI contract below remain planned, not authorization for this stage.

## Objective and claim boundary

Demonstrate whether accounting for review duration and declining intervention value can improve allocation of one simulated supervisor across three LLM agents. Use synthetic campus ventilation maintenance, with no defense assumptions.

**Engineering evidence:** live A100 decisions drive a reproducible simulator, review queue, interventions, scoring, and report. **Preliminary policy evidence:** paired loss differences on a small frozen scenario distribution, including ties and losses. **Publication claims:** general superiority, novelty, realistic human behavior, or generalization require substantially broader studies. This is simulated supervision, not a human-subject study; workload, trust, and usability are not measured.

## Repository and environment findings

The inspected checkout was clean on `main`, at `23cc579`, with only `README.md` and `LICENSE`; no implementation, dependency lock, tests, or applicable `AGENTS.md` was present. Local Python is 3.8.10 and local free disk approximately 53 GB; neither establishes pod readiness.

The user reports one A100 SXM 80 GB, approximately 117 GB RAM, 16 vCPUs, and $1.59/hour. These remain unverified: `~/.ssh/id_ed25519` is absent, SSH-agent access was denied, and batch-mode direct SSH failed with `socket: Operation not permitted`. No remote checks executed. Pod disk, driver, inference software, cached weights, and processes are unknown.

At implementation start, use existing local credentials/configuration: `ssh root@154.54.102.29 -p 12448 -i ~/.ssh/id_ed25519`. The supplied gateway supports SSH without SCP/SFTP. Check `nvidia-smi`, GPU processes, `df -h`, RAM, Python/package versions, and services without disrupting them. Seek approximately 50 GB free disk and sufficient free VRAM for the reservation. Keep credentials and Codex authentication local; exclude keys, weights, environments, and bulk outputs from Git.

## Backbone and information boundaries

Implement one small Python package: simulator/scorer, observation serializer, GPU client, estimator, four schedulers, and JSONL logger/CLI. No agent framework or UI is needed.

| Component | Permitted information |
| --- | --- |
| Simulator/scorer | Full seeded faults, noisy observations, arrivals, actions, outcomes |
| Agent | Its current work order, public manual, two noisy clues, costs/deadline, and its own prior action/feedback history |
| Every scheduler | Current proposal, estimated error probability, public costs/deadline, request time, queue and service progress |
| Simulated supervisor | The reviewed job's definitive diagnostic and correct action, accessed only at completion |

Schedulers receive a separate immutable public record, never simulator objects, hidden labels, unreleased jobs, or another agent's privileged feedback. Calibration labels are available only offline on development data. During evaluation, labels reach the scorer and the supervisor at review completion; accrued loss is scorer-only during an episode. Agent histories persist within episodes and reset between episodes.

### Task and time semantics

Each agent receives two jobs, at `r = 0 + jitter` and `6 + jitter`, with independent jitter in `{0,1}`. Episodes cover intervals `[0,1)` through `[11,12)` and finalize at tick 12. Each job has a hidden fault, uniformly `filter` or `sensor`; the manual maps these to `replace_filter` or `reset_sensor`. Two independently noisy textual clues identify the fault with probabilities 0.8 and 0.6, disclosed in the manual. Correctness is deterministic given the seeded fault and action.

Public job parameters are independently uniform: window length `L ∈ {1,2,5}`, downtime cost `c ∈ {0,1,3}`, and terminal cost `K ∈ {0,8}`; deadline `d=r+L`. Generate these independently of fault and clue errors, including zero-cost and impossible-to-review jobs.

At arrival the GPU proposes an action. That action immediately controls the maintenance workflow, and a review request is automatically queued: this version studies allocation, holding admission constant. While waiting, the workflow continues unchanged; an incorrect action accrues `c` per tick. There are no repeated waiting-time model calls. At closure, an incorrect action additionally incurs `K`; the job cannot then be changed.

The supervisor handles one nonpreemptive review at a time, taking exactly `s=2` ticks in the main condition. At completion it checks the definitive diagnostic and issues the correct action. The agent controller obeys immediately, records the feedback, and uses that history for its next GPU decision. Review neither reverses accrued loss nor rescues closed jobs. Perfect diagnostic accuracy and mandatory compliance are explicit idealizations, not measured human abilities.

At each tick: apply completed reviews; close and score jobs due now; release jobs and collect proposals; dispatch an available review; accrue interval downtime. Thus completion exactly at `d` can avert `K`, but not earlier downtime. Pending closed jobs expire. Finalize residual service/queue statuses at tick 12 without extending task time.

For action trajectory `a_i(t)` and correct action `a_i*`:

`loss_i = c_i Σ[t=r_i..d_i-1] 1[a_i(t)≠a_i*] + K_i 1[a_i(d_i)≠a_i*]`.

### Five hand-inspectable cases

These arithmetic fixtures may override the generated parameter grid. Stipulated proposals test mechanics; live GPU demonstrations retain actual outputs even when the anticipated mistake does not occur.

| Case, all arriving at 0 unless stated | Expected mechanics with s=2 |
| --- | --- |
| Easy: agreeing clues, correct filter action, c=1, K=8, d=5 | Loss zero with or without review |
| Correctable: misleading clues, wrong reset, c=1, K=8, d=5 | Unreviewed loss 13; completion at 2 leaves loss 2 |
| Competition: both wrong; A has c=0, K=8, d=2; B has c=0, K=12, d=5; both estimated p=0.5 | Myopic B-first loses A's 8; A-first finishes at 2 and 4 and saves both |
| Expiry: wrong action, c=1, K=8, d=1 | Earliest completion 2 has no value; loss 9 remains. A forced late-return fixture must not change it |
| Baseline wins: B is agent 0, A agent 1; both d=2, c=0; A correct, p=0.5, K=8; B wrong, p=0.2, K=12 | Proposed reviews A (expected 4 versus 2.4); FCFS's ID tie-break selects B and avoids 12 more actual loss |

## GPU model and runtime

Choose [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct), revision [`a09a35458c702b33eeacc393d103063234e8bc28`](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct/tree/a09a35458c702b33eeacc393d103063234e8bc28), including tokenizer/chat template. It is an established Apache-2.0 instruction model with structured-output support; its approximately 7.6B BF16 parameters require about 15.2 GB for weights, leaving substantial A100 headroom.

Use **vLLM 0.10.2**, Python 3.11, PyTorch 2.8.0, Transformers 4.55.2. Official [GPU guidance](https://docs.vllm.ai/en/v0.10.2/getting_started/installation/gpu.html) supports A100; versioned [CUDA](https://github.com/vllm-project/vllm/blob/v0.10.2/requirements/cuda.txt) and [common requirements](https://github.com/vllm-project/vllm/blob/v0.10.2/requirements/common.txt) support these package selections. Pod compatibility is untested. Reuse a working compatible vLLM installation, recording replacement pins before the pilot; otherwise create an isolated environment with these defaults. Lock exact Python patch, resolved packages, CUDA/driver, server arguments, and model hashes. No floating revisions during evaluation.

All LLM forward passes run on the A100: BF16, tensor parallelism 1, CPU offload 0, swap 0; fail if CUDA is unavailable. Host simulation/tokenization/scoring are permitted. No CPU inference substitute, fine-tuning, or distributed execution.

Use schema-constrained JSON with one required `action` field, enum `replace_filter` or `reset_sensor`, and no extra fields/rationale; at most 1,024 input and 48 output tokens, temperature 0.3, top-p 1. Two independently seeded calls see the identical observation: execute the first; use the second only for uncertainty estimation, never majority-vote or correctness repair.

## Estimates and allocation policies

Bin proposals by whether the two sampled actions agree. On 16 calibration scenarios, estimate error probability `p̂_b=(errors_b+1)/(count_b+2)` for the first action. A bin with fewer than 10 examples uses the pooled rate. Test reliability/Brier score on eight separate development scenarios, including changed policy histories. Freeze afterward, without evaluation updates. This is a coarse empirical estimate, not calibrated self-reported confidence or a conformal guarantee; agreement can conceal shared mistakes. Extra samples count fully as GPU inference.

For completion time `T`, define remaining preventable consequence:

`G_i(T) = 1[T≤d_i] [c_i(d_i−T)+K_i]`.

Estimated review benefit is `p̂_i G_i(T)`, assuming the declared perfect supervisor. At each dispatch, every policy skips jobs whose earliest completion has zero benefit. Pending infeasible requests remain logged until expiry. Ties use request time then agent ID; tied queue plans first prefer fewer reviews, then lexicographic request/ID order.

* **FCFS:** earliest request.
* **Uncertainty-first:** largest `p̂`.
* **Myopic benefit:** largest `p̂_i[c_i(d_i−t)+K_i]`, ignoring service/waiting loss in its ranking.
* **Delay-aware:** enumerate ordered subsets of currently pending jobs, including empty. For order `π`, project `T_πk=t+Σ[j≤k]s_πj` and maximize `Σ_k p̂_πk G_πk(T_πk)`. Choose the first job of the best positive-valued order, otherwise idle. Recompute when service becomes free; do not anticipate future arrivals or interrupt service.

At most three pending jobs give 16 ordered subsets. This optimizes the estimated static queue, not the evolving episode. All policies share the feasibility guard. Known deadlines/durations make late completed reviews normally zero; report expired unserved requests separately to capture lost opportunities.

**Review note (2026-09-09):** The first bounded implementation stage is accepted. For later evaluation, add a delay-aware greedy baseline ranking each pending request by `p_i * G_i(t+s_i)`, its estimated benefit at earliest completion. Comparing this with queue-order search will separate delay awareness from lookahead. Adding that baseline requires updating the later experiment matrix and runtime forecast; this stage retains the four policies above.

## Experiment matrix and validity

| Stage | Independent scenarios and runs |
| --- | --- |
| Mechanics/demo | Five named fixtures, four policies, s=2: 20 runs |
| Timing pilot | Seeds 100–103, four policies, s in {1,2}: 32 runs; provisional p=0.5 |
| Development | Seeds 200–215: FCFS/s=2 calibration with provisional p=0.5 (16 runs); 216–223: four policies × two durations validation (64 runs) |
| Frozen evaluation | Default seeds 10000–10063: 64 scenarios × four policies × s in {1,2} = 512 runs |

The one-tick condition controls for review speed while retaining nonzero duration. Six jobs and two calls/job give **12 scheduled calls, at most 24 attempts per run**: 6,144 scheduled evaluation calls, at most 12,288 attempts.

Freeze generator, seed list, prompts, estimator, tie rules, model settings, and software/config hashes before examining evaluation outputs. Pair complete exogenous streams across policies and durations; derive sampling seeds from scenario/agent/job/sample/retry IDs, never policy or execution order. Rotate policy execution order by scenario. Calls are serial with fixed concurrency one, and simulated ticks pause at observation barriers until outputs resolve. Wall latency, batching, and host scheduling therefore cannot decide simulated queue order.

Use fresh GPU calls in every policy run. Replay verifies deterministic scoring. Any later caching requires identical serialized observation, feedback history, prompt, model revision, decoding settings, and random seed; count logical and physical calls separately. Never reuse across changed histories. Fixed seeds do not guarantee bitwise-identical GPU output; preserve raw responses.

One retry per malformed/truncated output or timeout (60 seconds per attempt); disable hidden client retries. Retry only the same observation with a fixed schema reminder, without truth. If either required sample remains invalid, flag an implementation-failed episode, retain partial trace/cost, and mark unfinished outcomes unknown. Show completed-pair comparisons alongside failure rates and conservative missing-outcome bounds `[accrued loss, Σ_i(c_i L_i+K_i)]`; never silently delete or replace failed seeds. Keep raw failures, request IDs, error category, token counts (unknown explicitly), and latency for every attempt. Separate wrong valid LLM decisions, scheduler choices that missed useful review, and infrastructure/serialization/scoring failures.

## Execution window, forecast, and fallback

| Elapsed hours after authorization | Deliverable |
| --- | --- |
| 0–4 | Preflight, pinned server, minimal three-agent loop, first complete live GPU trace |
| 4–6 | Five fixtures, timing pilot, focused validity checks |
| 6–12 | Development; at most two corrective iterations, each at most two hours and one 80-run development batch |
| 12–14 | Final estimator/config freeze and pilot-based size selection |
| 14–24 | Frozen evaluation, checkpointed after each paired scenario block |
| 24–30 | Tables, figures, trace, report, one live demonstration reproduction |
| 30–36 | Contingency and final artifact verification; stop by hour 36 |

Measure pilot p95 attempt latency `τ`, non-inference seconds/run `h`, load/warmup time, tokens/second, and peak VRAM. Forecast conservatively as `T_eval(N)=2×8N×(24τ+h)` seconds: full retry allowance and a further factor-two margin. Select the largest `N ∈ {64,32,16}` fitting the ten-hour evaluation slot and remaining wall-clock window; freeze that prefix before evaluation. Illustratively, τ=1 second and negligible h predicts 6.83 hours for 64; τ=2 seconds selects 32. These are examples, not measured throughput. Development and reproduction are budgeted separately in the schedule.

If nothing fits, retain all four policies and six jobs with live GPU inference for 16 scenarios at s=2 only (64 runs), and label the absent speed control. If that still cannot finish, report the live demo and available paired results as an incomplete evaluation. An interrupted final batch retains all scheduled rows/statuses; no favorable stopping rule. Reduce size, never model grounding or baseline quality.

No GPU trace by hour 4 permits one compatibility repair ending by hour 6; continued failure produces a blocked report. No CPU substitute, model search, or scenario tuning to produce a win. Post-freeze validity bugs invalidate affected results; retain logs and report incompleteness unless a full paired rerun fits existing limits.

Record allocation start/end (provider timestamps when available), idle/setup hours, sampled GPU utilization, server/request timings, and total experiment wall time separately from simulated ticks. Preserve `nvidia-smi` process/memory evidence and CUDA/BF16 server logs during actual requests; utilization sampling is not a precise kernel-time measurement. At the quoted rate, 36 allocated hours cost $57.24; report actual allocated hours and unknown billing intervals explicitly, including allocation outside the experiment clock.

## Outputs, verification, and reproduction

Produce `trace.md` plus raw `events.jsonl`; `episodes.csv` covering every planned run/status; `comparison.csv`; a paired loss-difference figure and a review-queue timeline; `report.md`; and versioned configs, seed manifest, dependency lock, hashes, and exact executed commands. Primary outputs: correct jobs at closure, total error cost (the defined loss), review starts/completions/busy ticks, corrections, late returns, and expired requests. Split expiry into zero-value, infeasible-at-arrival, and opportunity-lost-while-waiting categories; separately score which involved incorrect proposals. Also report calls, tokens, allocation hours, GPU evidence, and runtime.

Predeclare delay-aware minus myopic loss at s=2 as primary; other comparisons are descriptive. Report paired scenario-level means and 95% percentile bootstrap intervals (2,000 resamples, seed 20260909), resampling whole scenarios with all policy/duration outcomes together. Within-episode decisions are not independent samples. Small fallback samples yield tentative estimates, not significance claims.

Focused checks cover information-boundary mutation tests, queue event order/deadline equality and late-return behavior, hand-calculated scoring, deterministic replay hashes, and actual GPU placement. No broad CPU test campaign. Engineering success requires a complete GPU trace and auditable outcome package without unresolved validity defects; policy improvement is not a success gate. A null or negative result is retained and discussed.

Required CLI contract, **not commands available in this planning commit**: run on the pod from the eventual implementation checkout. The report must include actual working pins and configs, including any pre-pilot replacement:

```bash
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
CUDA_VISIBLE_DEVICES=0 .venv/bin/vllm serve Qwen/Qwen2.5-7B-Instruct \
  --revision a09a35458c702b33eeacc393d103063234e8bc28 \
  --tokenizer-revision a09a35458c702b33eeacc393d103063234e8bc28 \
  --dtype bfloat16 --tensor-parallel-size 1 --max-model-len 2048 \
  --max-num-seqs 1 --gpu-memory-utilization 0.5 --enforce-eager \
  --cpu-offload-gb 0 --swap-space 0 --generation-config vllm \
  --seed 20260909 --host 127.0.0.1 --port 8000
# In a second pod shell, with the server ready:
.venv/bin/python -m overseeing demo --config configs/demo.json
.venv/bin/python -m overseeing pilot --config configs/pilot.json
.venv/bin/python -m overseeing develop --config configs/development.json
.venv/bin/python -m overseeing freeze --config configs/evaluation.json
.venv/bin/python -m overseeing evaluate --manifest artifacts/frozen.json
.venv/bin/python -m overseeing report --manifest artifacts/frozen.json
```

## Focused overlap check and review questions

[KnowNo (Ren et al., 2023), §§2–3](https://arxiv.org/html/2307.01928v2), calibrates uncertainty to trigger help in LLM planning. [Dong et al. (2026), §§3–4](https://arxiv.org/html/2601.06407v1), weighs information value against communication cost. [Zavattari et al. (2026), §§3,6](https://arxiv.org/html/2607.28317v1), studies limited fleet audit allocation under miscalibrated, correlated confidence and replays recorded outputs. These directly overlap. Their inspected formulations emphasize help selection, communication cost, or per-round audit budgets; this demonstration exercises a nonpreemptive queue with expiring, corrective interventions. This focused contrast does not establish novelty for delay-aware oversight or scheduling.

External review should assess: is continued provisional work and perfect mandatory correction a meaningful first abstraction; is the shared feasibility guard and static-queue search a fair comparison; are two-sample error bins adequate to expose estimator failure; and can the implementation environment reach the pod with compatible software/disk? These assumptions remain unresolved. Acceptance concerns experimental clarity, not a promised win.

Later extensions only: voluntary help admission, uncertain review durations/deadlines, imperfect supervisors, stronger scheduling baselines, richer histories/tasks, multiple models/correlated errors, human studies, and subsequent civilian or defense logistics applications.
