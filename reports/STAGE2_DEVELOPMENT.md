# Stage 2: bounded calibration and development validation

**Completed: 16 calibration episodes and 40 validation episodes, with 672 experimental GPU generations plus one placement generation, zero retries, and zero failed attempts. All 56 completed traces independently replay.** The disagreement calibration bin was sparse and used the declared pooled fallback. Queue-order search tied delay-aware greedy in every validation scenario and lost two more total cost units than FCFS. These are retained development diagnostics, not a final effectiveness result.

## Authorization, declaration, and preservation

This stage continued `main` from **`77d0e16094b4529a23dfaf1907ba5ab87e25b660`**. Its separately recorded start was **2026-09-10 01:07:01 UTC**, with deadline **03:07:01 UTC**. The original overall start **2026-09-09 15:38:57 UTC** and overall deadline **2026-09-11 03:38:57 UTC** remain unchanged. All implementation, checks, inference, transfer, reporting, and commit time count toward the stage. [Clock record](../artifacts/stage2_development/continuation_clock.json), [complete historical clock](implementation_clock.json).

The [declaration](../artifacts/stage2_development/run/declaration.json) was saved at **01:18:35.229622 UTC**, before inference started at **01:19:34.940054 UTC**. It fixes seeds, policy execution order, review duration, runtime settings, source/configuration hashes, prompt hash, scenario hashes, failure handling, and call limits. Declaration hash: **`076a9e689465b54096a399a47346a70529aeb3abdee391f4d74e51f5564a5f65`**. The runner checks these hashes and refuses an existing execution marker; no episode was repeated.

The fixed plan was calibration seeds **200–215**, FCFS with provisional `p=0.5`, followed by validation seeds **216–223**, all five policies, review duration **two ticks**. All episodes retain three agents, two jobs each, twelve ticks, the original generator/costs/deadlines, prompts, and two fresh samples per job. Sampling seeds depend on scenario/agent/job/sample/retry identifiers, never policy or execution order. Policies use separate histories. The first sample executes; the second supplies agreement information only. Simulated time remains independent of inference latency.

Validation order rotates left through `[fcfs, uncertainty, myopic, greedy, delay]` by `(seed−216) mod 5`:

| Seed | Execution order |
| --- | --- |
| 216 | FCFS → uncertainty → myopic → greedy → search |
| 217 | uncertainty → myopic → greedy → search → FCFS |
| 218 | myopic → greedy → search → FCFS → uncertainty |
| 219 | greedy → search → FCFS → uncertainty → myopic |
| 220 | search → FCFS → uncertainty → myopic → greedy |
| 221 | FCFS → uncertainty → myopic → greedy → search |
| 222 | uncertainty → myopic → greedy → search → FCFS |
| 223 | myopic → greedy → search → FCFS → uncertainty |

The Stage 1 command keeps its explicit four-policy list and unchanged configuration. Its verifier now reads the policy list in the historical manifest, so adding the fifth global policy cannot expand an old run. Stage 1's saved live results still verify. All **296 historical artifact files**, prior reports, Stage 1 configuration, and prior clock entries are unchanged. [Stage 1 verification](../artifacts/stage2_development/stage1_verification.json), [preservation audit](../artifacts/stage2_development/history_preservation.json).

## Reused GPU runtime

The existing pod `efbc29db9f5f` at **38.80.152.248:33513** remained healthy. The existing checkout, environment, cached weights, API server PID **7338**, and engine PID **8449** were reused. No runtime installation or server restart was needed. Actual hardware is **NVIDIA RTX 6000 Ada Generation, 49,140 MiB**, driver **580.126.20**. Python **3.11.13**, vLLM **0.10.2**, PyTorch distribution **2.8.0** / runtime **2.8.0+cu128**, Transformers **4.55.2**, and actual PyTorch CUDA runtime **12.8** were retained. [Resolved versions](../artifacts/stage2_development/run/requirements.actual.txt).

Model and tokenizer remain **Qwen/Qwen2.5-7B-Instruct**, revision **`a09a35458c702b33eeacc393d103063234e8bc28`**. Serving remains BF16, one GPU, tensor parallelism 1, eager mode, one sequence, model length 2048, memory reservation 0.5, CPU offload **0**, swap **0**, and loopback port 8000. Decoding remains temperature 0.3, top-p 1, strict action JSON, input limit 1024, output limit 48, and the existing 60-second shared attempt timeout. Experimental calls permit at most one retry; the separate placement call was capped at **one attempt**.

The GPU gate checked the serving command/revisions, native BF16 CUDA execution, descendant GPU allocation, and CUDA/BF16 model logs [before](../artifacts/stage2_development/run/gpu_before.json), [after placement](../artifacts/stage2_development/run/gpu_after_placement.json), and [after validation](../artifacts/stage2_development/run/gpu_final.json). The [placement response](../artifacts/stage2_development/run/placement_raw_requests.jsonl) was `{"action":"replace_filter"}`. All model inference stayed on the GPU; orchestration, tokenization, fitting, simulation, scoring, and replay ran on the host.

At **01:24:34 UTC**, health remained HTTP 200, Jupyter responded HTTP 302, and the engine remained resident at **24,618 MiB**. The root/workspace filesystems had approximately **66/47 GB** free. Existing services and persistent files are preserved. The generation counter remained **722**, comprising the prior stage's 49 and this stage's 673. [Final status](../artifacts/stage2_development/final_status.json).

## Estimator fit and freeze

All **96 calibration pairs** received labels based on the **first proposal before correction**. This includes **42 reviewed jobs with 10 initial errors** and **54 unreviewed jobs with seven initial errors**. Reviewed status did not select training examples. All calibration episodes completed; there were no missing pairs. Calibration final correctness was 89/96 after ten corrections, which was **not** used as the training label. [Calibration examples](../artifacts/stage2_development/run/calibration_examples.csv).

Each bin's candidate estimate is `(errors+1)/(examples+2)`. Bins with fewer than ten examples use the pooled `(17+1)/(96+2)=0.1836734694` estimate instead.

| Calibration bin | Examples | Initial errors | Observed error rate | Bin-smoothed estimate | Frozen prediction | Pooled fallback |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Agree | 87 | 12 | 0.137931 | 0.146067 | **0.146067** | No |
| Disagree | 9 | 5 | 0.555556 | 0.545455 | **0.183673** | **Yes: fewer than 10** |
| Pooled | 96 | 17 | 0.177083 | 0.183673 | 0.183673 | Reference |

The [estimator record](../artifacts/stage2_development/run/estimator.json) includes bin counts/errors, both candidate and used probabilities, fallback decisions, calibration seeds, trace/request hashes, and provenance. It was frozen at **01:20:19.801377 UTC**, before validation. Estimator hash: **`54d9a97e25f5cb22cf0df216293303ea5c945713032c6bc1282c55fcf327e085`**. File SHA-256 is also recorded in the [execution manifest](../artifacts/stage2_development/run/manifest.json).

The runtime predictor is immutable and accepts only the two sampled action strings. It cannot access hidden labels, review status, or simulator objects. Validation checks the frozen estimator file hash before each episode. Offline verification independently reconstructs the calibration statistics and confirms that every validation prediction used this same estimator. Validation labels never updated it.

## Fifth policy and mechanics check

Delay-aware greedy selects the eligible request maximizing `p_i * G_i(t+s_i)`, where `G_i(T)=1[T≤d_i][c_i(d_i−T)+K_i]`. It shares eligibility and deterministic request-time/agent-ID ties with the original schedulers. The queue-order search algorithm is unchanged.

The existing competition fixture now includes greedy. Both proposals are **stipulated wrong actions**: A has terminal cost 8 and deadline 2; B has terminal cost 12 and deadline 5; both have zero downtime cost and `p=0.5`. Greedy chooses B first (estimated immediate benefit 6 versus 4), losing A's 8. Search chooses A then B and loses 0. FCFS/uncertainty also lose 0; myopic loses 8. All five fixture traces replay, with **zero model calls**. These engineered mechanics outcomes are not live effectiveness evidence. [Fixture CSV](../artifacts/stage2_development/mechanics/episodes.csv), [greedy trace](../artifacts/stage2_development/mechanics/greedy/trace.md), [search trace](../artifacts/stage2_development/mechanics/delay/trace.md).

## Validation prediction quality

Each policy has **48 collected job pairs across the same eight scenarios**. All five happened to produce the same bin/error counts and Brier scores; the diagnostics were calculated separately from each policy's actual saved trajectory.

| Policy | Agree: errors / examples | Disagree: errors / examples | Overall initial error rate | Frozen Brier | Constant 0.5 Brier | Pooled-calibration Brier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FCFS | 7/45 | 1/3 | 8/48 = 0.166667 | 0.138521 | 0.250000 | 0.139178 |
| Uncertainty-first | 7/45 | 1/3 | 0.166667 | 0.138521 | 0.250000 | 0.139178 |
| Myopic benefit | 7/45 | 1/3 | 0.166667 | 0.138521 | 0.250000 | 0.139178 |
| Delay-aware greedy | 7/45 | 1/3 | 0.166667 | 0.138521 | 0.250000 | 0.139178 |
| Queue-order search | 7/45 | 1/3 | 0.166667 | 0.138521 | 0.250000 | 0.139178 |

Within each policy, agreement-bin observed error is **0.155556** and disagreement-bin error is **0.333333**. Frozen/pooled Brier scores are **0.131448/0.132149** in the agreement bin and **0.244620/0.244620** in the disagreement bin. Constant 0.5 has Brier 0.25 in either bin. Complete per-policy/per-bin tables and individual labeled predictions are saved in [prediction diagnostics](../artifacts/stage2_development/run/prediction_diagnostics.csv) and [validation predictions](../artifacts/stage2_development/run/validation_predictions.csv).

Most improvement over constant 0.5 comes from estimating a lower base error rate. The frozen bin estimator improves Brier over the pooled estimate by only **0.000657** per policy. The disagreement bin had only nine calibration and three validation examples per policy, so these data do not establish reliable agreement-based uncertainty. Alternative Brier scores were computed from the same saved outputs, with **no additional generations**; they measure prediction on observed trajectories, not counterfactual scheduling performance.

## Validation task outcomes and paired differences

All policies completed **8/8 episodes**, with no missing outcomes or late review returns. The values below sum over their eight paired scenarios; correct-job denominator is 48 per policy.

| Policy | Total loss | Correct jobs | Completed reviews | Corrections | All expired requests | Expired useful opportunities | Wrong expired useful opportunities |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FCFS | **60** | 42/48 | 18 | 2 | 30 | 2 | 1 |
| Uncertainty-first | **60** | 42/48 | 18 | 2 | 30 | 2 | 1 |
| Myopic benefit | 62 | 42/48 | 18 | 2 | 30 | 2 | 1 |
| Delay-aware greedy | 62 | 42/48 | 18 | 2 | 30 | 2 | 1 |
| Queue-order search | 62 | 42/48 | 18 | 2 | 30 | 2 | 1 |

“Expired useful opportunities” is the existing `opportunity_lost_while_waiting` category: review had positive preventable consequence at arrival, but the request expired unserved. It is distinct from zero-value and infeasible-at-arrival requests. [All 56 episode rows](../artifacts/stage2_development/run/episodes.csv), [policy outcomes](../artifacts/stage2_development/run/policy_outcomes.csv), [queue timeline](../artifacts/stage2_development/run/queue_timeline.md).

| Validation seed | FCFS | Uncertainty | Myopic | Greedy | Search | Search − greedy | Search − FCFS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 216 | 19 | 19 | 19 | 19 | 19 | 0 | 0 |
| 217 | 14 | 14 | 14 | 14 | 14 | 0 | 0 |
| 218 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 219 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 220 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 221 | 6 | 6 | 6 | 6 | 6 | 0 | 0 |
| 222 | 11 | 11 | 11 | 11 | 11 | 0 | 0 |
| 223 | 10 | 10 | 12 | 12 | 12 | 0 | **2** |

Search versus greedy: **eight ties**, mean paired difference **0**. Search versus myopic: also eight loss ties. Search versus FCFS/uncertainty: **seven ties and one loss**, mean paired difference **+0.25**. All ten policy-pair comparisons, with scenario-level rows, are saved in [paired differences](../artifacts/stage2_development/run/paired_scenario_differences.csv) and [paired summaries](../artifacts/stage2_development/run/paired_comparisons.csv).

The negative example is seed 223. At tick 7, both `a1j1` and `a2j1` proposed `replace_filter` with agreeing samples. FCFS reviewed the actually wrong `a1j1` first and corrected it to `reset_sensor` at tick 9, leaving loss 2. Search/greedy/myopic first reviewed the already-correct `a2j1`, correcting `a1j1` at tick 11 and leaving loss 4. Both jobs eventually closed correctly. This extra downtime accounts for the entire two-unit aggregate difference. [FCFS trace](../artifacts/stage2_development/run/validation/223/fcfs/trace.md), [search trace](../artifacts/stage2_development/run/validation/223/delay/trace.md). No wrong valid output was retried, voted away, or repaired using scorer truth.

## Does the batch exercise scheduling?

A dispatch opportunity is a free-supervisor decision with at least one request passing the shared positive-benefit guard. Each policy observed **18 opportunities**, of which **four had at least two eligible requests**. These occur in **three of eight scenarios**: seed 219 at tick 1, seed 222 at tick 7, and seed 223 at ticks 1 and 7. All other scenarios had no competing eligible dispatch.

The policies' actual review sequences differed in **two scenarios**. In seed 219, myopic selected `a2j0` while the other policies selected `a0j0`; both choices yielded zero episode loss. In seed 223, FCFS/uncertainty reversed the order used by myopic/greedy/search for the two second-wave jobs, producing the loss difference above. Queue search and greedy had **identical actual review orders in all eight scenarios**.

The audit also applies all five deterministic selection rules offline to each saved public dispatch state. Search and greedy disagree on **zero** of the four competitive states along each policy's trajectory. Across five policies this is 20 logged competitive dispatches, but these repeated trajectories are **not 20 independent scenarios**. Offline alternative selections are diagnostic decisions only; no alternative rollout or generation occurred. [Dispatch records](../artifacts/stage2_development/run/dispatch_opportunities.csv), [observed orders](../artifacts/stage2_development/run/review_orders.csv), [scenario competition summary](../artifacts/stage2_development/run/competition_by_seed.csv).

Thus the tasks exercised correction and some review competition, while this batch supplied no live instance distinguishing greedy from queue search. The stipulated competition fixture proves that their implementations can differ; it does not fill that empirical gap.

## Calls, tokens, time, and limitations

| Work | Episodes | Scheduled / attempted generations | Retries / failed attempts | Prompt tokens | Output tokens | Request wall seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Calibration | 16 | 192 / 192 | 0 / 0 | 40,436 | 1,344 | 26.888199 |
| Validation | 40 | 480 / 480 | 0 / 0 | 100,420 | 3,360 | 66.917010 |
| Placement | — | 1 / 1 | 0 / 0 | 195 | 7 | 0.151009 |
| **Total** | **56** | **673 / 673** | **0 / 0** | **141,051** | **4,711** | **93.956218** |

Experimental usage stayed within **672 scheduled calls / at most 1,344 attempts**, and placement within one attempt. No token counts are unknown. Every declared episode row is retained; all are completed, so there are no missing-outcome bounds to interpret. The runner retains successfully collected partial calibration pairs and explicit incomplete episode rows if a future invocation fails; that failure path was not exercised by this live batch.

The runner recorded **135.541730 seconds** through episode completion; its final GPU/health checks follow that timestamp. The enclosing [launch record](../artifacts/stage2_development/launch.json) spans **01:19:34.675365–01:21:51.924506 UTC**, or **137.249141 seconds**, including final checks and telemetry. Experimental mean request latency was **0.139591 seconds**, nearest-rank p95 **0.144308 seconds**, and output throughput **50.15 tokens/second** of request wall time. [Accounting](../artifacts/stage2_development/accounting.json).

The [before](../artifacts/stage2_development/run/metrics_before.txt)/[after](../artifacts/stage2_development/run/metrics_after.txt) server counters increased from 49 to 722 successful requests and match every token total. GPU prefix caching remained enabled, with **132,784 additional prefix-cache hit tokens**. Prompt-token totals include cached prefixes; all generation responses were fresh. Native BF16 validation kernels are additional GPU work outside the generation counts. [273 GPU telemetry samples](../artifacts/stage2_development/gpu_telemetry.csv) observed maximum total memory **25,165 MiB** and utilization **94%**; sampled maxima are not exact kernel-time or peak-allocation measures.

Allocation start/end, billed intervals, hourly rate, and charges are unknown. The pod remains allocated, so request time is not allocation time. The environment, weights, server, and existing services are preserved.

There were **no deviations from the declared batch, no failed live attempts, and no corrective code changes after source freeze**. The calibration disagreement bin and validation disagreement bin are sparse; improvement over the pooled predictor is small; useful competition is limited; search does not beat its greedy comparator. We stop at the declared batch. The eight scenarios are development diagnostics, with no confidence interval, final effectiveness claim, or assumption that repeated policy episodes are independent scenarios. Perfect simulated supervision, mandatory compliance, deterministic review duration, synthetic faults, and fixed-model sampling remain strong idealizations.

## Verification and reproduction

**28 focused tests passed locally and on the pod**, including pre-correction labels, reviewed/unreviewed inclusion, partial-pair retention, sparse-bin fallback, estimator immutability/hash checks, information boundaries, greedy ties/eligibility, a complete synthetic execution/audit, and refusal to rerun. Synthetic test responses are temporary mechanics evidence and are excluded from live call counts. [Local checks](../artifacts/stage2_development/focused_checks.txt), [pod checks](../artifacts/stage2_development/pod_focused_checks.txt).

All **56 live traces** independently replayed on the pod and again after transfer. Verification also checked source/configuration hashes, unchanged prompts/settings, deterministic request seeds, primary-action execution, paired observations, serial request intervals, calibration-only fitting, frozen predictions, GPU evidence, and server-counter deltas. [Pod audit](../artifacts/stage2_development/pod_verification_stdout.json), [local audit](../artifacts/stage2_development/local_verification_stdout.json), [diagnostic summary](../artifacts/stage2_development/run/diagnostics.json). Every episode directory contains `raw_requests.jsonl`, `events.jsonl`, `trace.md`, and `replay.json`.

Verification and replay from the repository root, with no inference:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/verify_live_results.py artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run
python3 scripts/verify_development.py artifacts/stage2_development/run
for events in artifacts/stage2_development/run/calibration/*/*/events.jsonl \
              artifacts/stage2_development/run/validation/*/*/events.jsonl; do
  python3 -m overseeing replay "$events"
done
python3 -m overseeing development-mechanics --out artifacts/local-stage2-mechanics
```

Use a fresh output directory for repeated mechanics commands. The verifier regenerates diagnostic tables from saved evidence without making inference requests.

The actual preparation command was:

```bash
python3 -m overseeing prepare-development --out artifacts/stage2_development/run
```

Source and the prepared declaration/snapshot were transferred into the existing checkout, preserving Stage 1 outputs. The successful SSH configuration was:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=12 -o StrictHostKeyChecking=yes \
  -o UserKnownHostsFile=/tmp/runpod-nfx7q9p6vf4g8q-known_hosts \
  -p 33513 root@38.80.152.248
```

The [one-shot wrapper](../artifacts/stage2_development/execute_stage.py) reused the existing server and invoked:

```bash
cd /workspace/OverseeingManyLLMs-rtx6000-ada-20260910T002404Z
.venv/bin/python -m overseeing develop --out artifacts/stage2_development/run \
  --server-pid 7338 \
  --server-log artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/server.log \
  --deadline-utc 2026-09-10T03:07:01+00:00
```

These are historical execution commands; the saved output/one-shot marker prevents repetition and the recorded stage/overall caps remain enforced. Runtime setup and the unchanged server launch are documented in the [Stage 1 report](STAGE1_GPU_LIVE.md). No credentials, model weights, environment, or caches are committed. New evidence is confined to `artifacts/stage2_development/`; relevant code/docs/results are committed to `main`, with no push.

**Single recommended next step:** predeclare a small competition-focused development condition, with enough simultaneously eligible reviews to test the greedy-versus-search distinction. Fix its distribution and success criteria before new inference, and report it as a diagnostic rather than selecting favorable seeds. This batch's sparse disagreement data and identical greedy/search orders do not justify a larger effectiveness study yet. Review-duration controls, held-out evaluation, advanced tasks, and full manuscript drafting remain later work.

Report checkpoint: **2026-09-10T01:31:35.526400+00:00**, **1474.526 elapsed seconds** after stage start. Overall remaining time: **94041.474 seconds**. The task commit's committer timestamp records final Git completion.
