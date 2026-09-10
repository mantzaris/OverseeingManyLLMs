# Stage 5: adapted retail transaction review

This stage tests whether a shared finite-duration reviewer benefits from planning
the order of genuine retail transactions. It uses an adapted τ-bench subset,
actual GPU-generated tool workflows, and deterministic paired review replays.
It is not an official τ-bench score or a measurement of human supervision.

## Authorization and preserved evidence

Stage 5 began **2026-09-10 14:15:20 UTC**, with a hard deadline of
**23:15:20 UTC** and an inference cutoff of **21:45:20 UTC**. The last 90 minutes
were reserved for reporting. The hard generation-attempt ceiling is 30,000,
including development and retries; each ordinary call permits at most one retry
within its 60-second attempt timeout. The append-only reservation ledger covers
every Stage 5 generation. Historical clocks were not reset.

The original clock began 2026-09-09 15:38:57 UTC; its 36-hour target ends
2026-09-11 03:38:57 UTC. Final cumulative elapsed time is recorded below.
The baseline is `fef637276f7b7240b92900851cfffe9dc89cd32a`. All Stage 1–4 results,
including unfavorable and null findings, remain separate and preserved. An
authorization-time hash inventory covers 11,117 historical files.

## Source and practical semantics

The [adaptation table](../paper/RETAIL_ADAPTATION.md) specifies every inherited
component and modification. Upstream τ-bench is pinned at
`59a200c6d575d595120f1cb70fea53cef0632f6b`; its MIT license, tools, policy, source
records and validator implementation are retained under `third_party/tau_bench/`.
The repository warns that later benchmark releases fix tasks. This study audits
its chosen pinned cases and makes no claim to reproduce the latest leaderboard.

The three families are cancellation, pending-order item modification, and
delivered-order returns/exchanges. Agents authenticate, retrieve account/order
information, inspect product variants when needed, request explicit confirmation,
and invoke actual state-changing tool interfaces. Upstream status, inventory,
item compatibility, payment and balance checks stay active. Added deterministic
guards enforce account ownership, prior retrieval, nonempty transactions and
confirmation of exact proposed arguments. These guards never inspect the target.

The scripted customer repeats only its original operational instruction, with
personality directions removed, and confirms displayed proposals without
independently checking backend IDs. This simplifies the user interaction and
can leave semantic mistakes undetected. It is not a second perfect reviewer.
Unmentioned product options must retain their original values. Selected target
variants were checked for unique compatibility; all 17 selected multi-item
modification/exchange cases preserve their target hash under equivalent pair
permutations.

A validated mutation is **staged**, with no committed database change. Three
agent histories are interleaved during preparation using serial GPU requests.
After preparation, transactions enter a simulated processing batch at slots
0/0/1, independently permuted across agents. Relative cutoff windows 2/4/5 and
processing/rework weights 4/8/12 are separately permuted using declared seeds.
These slots represent order-processing, change-lock and reverse-logistics batch
cutoffs; they are our constructed operational extension, not measured retailer
deadlines. One tick is an abstract service-time unit, not an inference second.

One nonpreemptive **perfect simulated reviewer** takes two ticks in the primary
condition and one in the secondary condition. Only completion by the cutoff
permits correction to the private annotated transaction and immediate commitment.
Completion exactly at cutoff is timely. Otherwise the original proposal posts
at cutoff. A posted consequence cannot be erased. Preparation failures have no
valid staged transaction and cannot be rescued by this reviewer. Reviewer approval
is assumed sufficient to correct the staged transaction within the recorded
customer intent; a further customer conversation is not modeled. Upstream tool
checks run again at commitment, while the added exact-argument confirmation
guard applies during agent preparation. This corrective authority is an
explicit application assumption, not measured customer consent behavior.

Operational loss is four points per unresolved service request plus its public
4/8/12-point processing consequence if an incorrect transaction commits. These
are declared synthetic consequence points, not measured monetary losses.
Therefore expected review benefit at completion T is
`p(error) × (4 + processing_cost)` when `T ≤ cutoff`, and zero afterward. There
is no maintenance downtime term. Exact final-database equality uses upstream
validator semantics; correctness and policy-error classes are reported separately.
Thus an incorrect reason or refund destination can fail the annotated task even
when an order status changes as intended. The objective weights these declared
errors; it does not establish their real monetary severity.

## Development and frozen design

[The source declaration](../artifacts/stage5_practical/cases.json) selects 24
development and 96 evaluation cases from upstream retail training records.
Evaluation comprises 32 cancellation, 32 modification, 16 return and 16 exchange cases.
All 120 customer accounts are distinct, preventing repeated order/intent
variants from crossing cases or partitions. Selection uses ascending source
indices within supported families, not model errors or scheduler performance.
Workflow families and broad instruction templates are shared: this is held-out
source-case evaluation, not unseen-template generalization.

The first pilot made 168 successful GPU generations but staged **0/12** workflows.
An inherited serializer alphabetized guided-schema fields, placing arguments
before tool choice. The single live development revision preserves tool-first
wire order and adds public progress information. It retains the full policy,
guards, source cases, costs and model decoding parameters. The repeated pilot
made 90 generations, staged **12/12**, and completed **11/12** correctly. The
remaining valid error selected a plain skateboard design instead of the
requested custom design. Because serialization and prompt guidance changed
together, their separate causal effects are not identified.

No workflow narrowing or second live development revision was used. Earlier
pre-inference source-group selection and offline JSON-order replay defects were
repaired with failed declarations/audits preserved. Replay reconstructs assistant
history from the exact raw response text, including nested argument order.

Calibration used all 24 development cases with replicates 2/3/4: **72 workflows,
602 GPU generations, 64 staged proposals, 15 initial errors and eight unstaged
failures**. Every staged proposal receives its pre-review label, irrespective
of review selection. The error feature uses only public workflow family and an
uncertainty flag: non-high model confidence or any prior automatic rejection.
Laplace-smoothed bins with fewer than ten examples use the pooled estimate.
The final [estimator](../artifacts/stage5_practical/estimator.json) is frozen at
hash `5734f6babfbd33655a76595f001251bd5914d94dde0c0e3401af3fc4a762a581`.

| Family | Flag | Examples | Errors | Frozen probability | Fallback |
|---|---|---:|---:|---:|---|
| Cancellation | Present | 23 | 0 | 0.040000 | No |
| Modification | Present | 22 | 6 | 0.291667 | No |
| Return/exchange | Present | 19 | 9 | 0.476190 | No |
| Each family | Absent | 0 | 0 | 0.242424 | Pooled |

All staged calibration examples were flagged, so the feature does not establish
confidence discrimination; the fitted rule effectively separates families.
The maintenance estimator and analytical fault model were not transferred.

On development replays at two ticks, search loss was **72**, greedy **48**, and
EDF **80** points. At one tick, their losses were all **32**, entirely from
unstaged failures. This unfavorable development search result was retained;
it did not change the evaluation cases, methods or sample size.

The [evaluation freeze](../artifacts/stage5_practical/evaluation_freeze.json),
committed at `d0f47978` before evaluation generation, declares:

- 32 source-disjoint bundles, three source cases per bundle, three generation replicates.
- 288 fresh multistep GPU workflows, at most 14 calls each: 4,032 call and 8,064 attempt ceilings.
- FCFS, EDF, uncertainty-first, delay-aware greedy, queue-order search and no review.
- Review durations two (primary) and one (secondary), with balanced duration order and rotating policy order.
- 1,152 finite-policy replay episodes plus 96 inexpensive idealized parallel-perfect-review reference rows.
- Primary analysis: search minus greedy bundle-mean loss at two ticks, with 2,000 paired bootstrap resamples, seed 20260915.

Policies receive **the same saved prepared transactions**, not new generations
for each policy. No agent generation follows staging, so these paired replays
isolate allocation under the stated semantics. They do not test how retail
agents adapt later behavior to review feedback. Three fresh preparation
replicates measure generation variability and are averaged within each bundle
before paired inference. Policy runs and replicate rows are not independent
scenarios. Bootstrap intervals concern this selected source-case cohort, not a random sample of retailer traffic. The idealized reference gives every staged transaction its own
perfect reviewer; it still cannot fix unstaged preparation failures.

The measured calibration runtime was 926.89 seconds. The full evaluation
forecast was 3,707.54 seconds, or 6,488.20 seconds with a 1.75 margin, against
23,495.62 seconds remaining before the inference cutoff. The entire declared
matrix was selected before evaluation outcomes; no replacement cases or
effect-dependent stopping are permitted.

## Measured evaluation results

The complete fixed matrix produced **288 live workflow attempts, 233 staged
transactions, 182 initially correct transactions, 51 wrong valid transactions
and 55 unstaged failures**. All 1,152 paired policy episodes completed and
replayed; there are no missing or replaced bundle–replicate rows. The statistical
unit is the **32 source-disjoint bundles**, with three replicates averaged first.

The primary comparison does **not** establish a search advantage. At two ticks,
search minus greedy mean loss is **+0.2500 points**, 95% paired bootstrap interval
**[−0.3333, 1.0000]**, with **1 win, 29 ties and 2 losses** for search across bundles.
Search conducts 21 more reviews but corrects one fewer transaction than greedy.
This is an unfavorable point estimate with substantial uncertainty, not proof
of a population-level disadvantage.

| Duration | Policy | Total loss | Mean loss | Correct / 288 | Wrong commits | Reviews | Corrections | Missed useful |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | No review | 800 | 8.3333 | 182 | 51 | 0 | 0 | 51 |
| 1 | FCFS | 220 | 2.2917 | 233 | 0 | 233 | 51 | 0 |
| 1 | EDF | 220 | 2.2917 | 233 | 0 | 233 | 51 | 0 |
| 1 | Uncertainty-first | 220 | 2.2917 | 233 | 0 | 224 | 51 | 0 |
| 1 | Delay-aware greedy | 220 | 2.2917 | 233 | 0 | 224 | 51 | 0 |
| 1 | Queue-order search | 220 | 2.2917 | 233 | 0 | 233 | 51 | 0 |
| 2 | No review | 800 | 8.3333 | 182 | 51 | 0 | 0 | 51 |
| 2 | FCFS | 480 | 5.0000 | 210 | 23 | 182 | 28 | 23 |
| 2 | EDF | 440 | 4.5833 | 215 | 18 | 190 | 33 | 18 |
| 2 | Uncertainty-first | 332 | 3.4583 | 223 | 10 | 169 | 41 | 10 |
| 2 | Delay-aware greedy | 332 | 3.4583 | 223 | 10 | 169 | 41 | 10 |
| 2 | Queue-order search | 356 | 3.7083 | 222 | 11 | 190 | 40 | 11 |

Counts aggregate 96 bundle–replicate runs per policy/capacity, each with three
source cases. Means average the three replicates within each bundle and then
average bundles. A missed useful opportunity is an initially wrong staged
transaction that reaches its cutoff without successful review. It excludes
unstaged failures. Wrong commits are annotated-intent errors that passed active
automatic checks, not a complete natural-language policy-violation classifier.

At one tick, every review policy corrects all 51 queued errors and reaches the
idealized parallel-perfect-review floor: **220 loss points, mean 2.2917, 233/288
correct**. The floor is exactly 55 unstaged failures × four service-loss points.
Greedy and uncertainty-first leave nine initially correct transactions unreviewed;
EDF, FCFS and search review all 233. Their different orders yield no realized
loss difference. No review has loss 800 (mean 8.3333), comprising 424 service-loss
and 376 wrong-processing points.

At two ticks, search has 264 service-loss and 92 wrong-processing points; greedy
has 260 and 72; EDF has 292 and 148. Search minus EDF is **−0.8750 [−2.0000, 0]**,
with **3 wins, 29 ties, no losses**. Search minus FCFS is
−1.2917 [−2.5000, −0.2500]. These are secondary comparisons without a multiplicity
adjustment. The stronger primary comparator remains greedy; uncertainty-first
has the same aggregate outcomes as greedy.

### Competition, waiting and actual decisions

| Policy | Two-tick mean utilization | Mean waiting of completed reviews | Dispatches with ≥2 eligible requests |
|---|---:|---:|---:|
| FCFS | 71.18% | 0.835 ticks | 87 |
| EDF | 73.96% | 1.005 ticks | 103 |
| Uncertainty-first | 66.39% | 0.615 ticks | 83 |
| Greedy | 66.39% | 0.615 ticks | 83 |
| Search | 73.96% | 0.968 ticks | 103 |

Utilization is averaged over each run's declared processing horizon; no-review
utilization is zero. At one tick, mean utilization is 45.94% for FCFS/EDF/search
and 44.17% for uncertainty/greedy; corresponding served-request waiting means
are 0.494 and 0.433 ticks.

On search's own saved public states, greedy and search choose different heads
at **58/115** competitive dispatches at one tick and **47/103** at two ticks.
Their actual completed review sequences differ on **50/96** and **47/96** runs,
respectively. Search versus EDF sequences differ on **34/96** and **23/96**.
These are replicate-level descriptions, not independent scenario counts.

A separately labeled retrospective audit uses initial-error labels only offline.
Among search's competitive dispatches, only **7 at one tick and 4 at two ticks**
have at least two initially wrong eligible transactions. Most overlapping public
queues therefore contain at most one realized error. This limits what the batch
can establish about competition among several genuinely useful corrections.
The scheduler never receives these retrospective labels.

An exact-rational audit checks **6,372 dispatch records / 639 unique public
states**, including hypothetical alternatives on no-review states. It finds
**zero positive expected-value regret and zero canonical-tie discrepancies**.
The null/unfavorable primary finding is therefore not explained by a detected
arithmetic error in current-queue search. It remains a finite current-queue
objective without knowledge of future arrivals.

### Risk quality and workflow reliability

| Public family (all flagged) | Staged examples | Initial errors | Observed error rate | Frozen risk |
|---|---:|---:|---:|---:|
| Cancellation | 87 | 0 | 0.0000 | 0.0400 |
| Modification | 58 | 24 | 0.4138 | 0.2917 |
| Return/exchange | 88 | 27 | 0.3068 | 0.4762 |

All 233 staged evaluation proposals are flagged, so the uncertainty flag again
provides no within-family discrimination. The frozen estimator's **Brier score
is 0.15585**, versus **0.17153** for its pooled calibration probability and
0.25000 for constant 0.5; **AUROC is 0.7096**. Mean predicted error is 0.2674
versus observed 0.2189. Despite improving the aggregate Brier score, it ranks
return/exchange above modification while their observed error rates are reversed.
The combined return/exchange family also hides substantial heterogeneity:
returns have 6/48 staged errors; exchanges 21/40. These diagnostics do not refit
or alter the estimator. Since prepared outputs are identical across policies
and capacities, repeating the same Brier values per policy would duplicate data.

| Intended workflow | Attempts | Staged | Initially correct | Wrong valid | Unstaged |
|---|---:|---:|---:|---:|---:|
| Cancellation | 96 | 87 | 87 | 0 | 9 |
| Modification | 96 | 58 | 34 | 24 | 38 |
| Returns | 48 | 48 | 42 | 6 | 0 |
| Exchanges | 48 | 40 | 19 | 21 | 8 |

There are **778 blocked tool calls**: 719 adapter policy-guard rejections and
59 upstream backend errors; 338 are attempted mutations. The risk feature's
762 rejection count excludes 16 authentication/retrieval errors that do not
increment that feature. No automatically rejected mutation commits. Initial
wrong-valid argument differences include 45 variant-mapping differences and
eight wrong/incomplete item-list differences; categories can overlap and are
not a full policy-compliance taxonomy.

The 55 unstaged failures comprise **50 step-limit failures, four explicit
finish-without-staging outcomes and one exhausted generation retry**. Modification
is the largest reliability bottleneck: 38/96 attempts never stage. Even a perfect
transaction reviewer cannot rescue those workflows under the declared semantics.

Across three generation replicates, **25/96 source cases** have different
proposals or staging outcomes, and **12/96** vary in initial task success.
Thirty cases succeed in none of their three preparations, four in one, eight in
two and 54 in all three. These are generation-replicate differences, including
subsequent history changes; there are no repeated identical full requests in
this session from which to estimate same-request nondeterminism.

### Representative traces and figures

The [readable examples](../artifacts/stage5_practical/batches/evaluation/analysis/examples/REPRESENTATIVE_TRACES.md)
follow the frozen first-in-numerical-order selection rule:

- **Benefit — evaluation_28_r0:** search and EDF review an incorrect laptop modification by tick 2, then an incorrect puzzle exchange by tick 4. Greedy reviews the exchange first, allowing the laptop mistake to post at its tick-2 cutoff. Loss is 0 versus 8.
- **Tie — evaluation_00_r0:** search and greedy use different orders, but both miss a bookshelf exchange arriving at tick 1 with cutoff 3. Their reviewer is already occupied; completion from tick 2 would be too late. Both lose 16 points.
- **Unfavorable — evaluation_09_r0:** search protects an urgent but correct cancellation, then fixes an incomplete return. A later-released wrong wall-clock modification reaches cutoff uncorrected. Greedy fixes the return first and the modification next: loss 0 versus search's 12. Search cannot see the future modification at its initial decision.
- **Preparation failure — evaluation_00_r2 / train:062:** the agent retrieves account, order and product information but repeats rejected incomplete confirmations until the 14-call limit. No transaction enters review.

These examples show actual tool arguments and irreversible simulated posting,
not stipulated mechanics or selected favorable magnitudes. They distinguish a
different sequence from a realized benefit.

![Policy loss components](../artifacts/stage5_practical/batches/evaluation/analysis/figures/policy_loss_components.png)

*Mean loss components with 95% bundle-bootstrap intervals; the primary inference
uses paired differences, not overlap of these marginal intervals.*

![Paired losses](../artifacts/stage5_practical/batches/evaluation/analysis/figures/paired_loss.png)

*Two-tick search-minus-comparator differences, averaged across three replicates
within each of the 32 source-disjoint bundles.*

![Risk and generation variability](../artifacts/stage5_practical/batches/evaluation/analysis/figures/risk_and_generation_variability.png)

*Frozen risk versus observed staged-proposal errors, and initial task success
across the three generation replicates. Matching vector PDFs are saved beside
all figures.*


## Runtime, accounting and verification

The authenticated direct pod is `root@38.80.152.248`, port 33513, accessed with
the existing `/tmp/overseeing_stage2_ssh_config` alias `overseeing-development`.
The remote checkout is
`/workspace/OverseeingManyLLMs-rtx6000-ada-20260910T002404Z`.
No local SSH private key or configured service credential was copied into the transferred code or artifacts. Unsolicited credential-like model output is handled as described below.

Hardware is an RTX 6000 Ada, 49,140 MiB total VRAM, driver 580.126.20. The reused
environment is Python 3.11.13, PyTorch 2.8.0+cu128 (CUDA runtime 12.8), vLLM
0.10.2 and Transformers 4.55.2. Driver compatibility is not treated as toolkit
evidence; `nvcc` was not on PATH. Initial persistent storage had about 47 GiB free.

The original port-8000 server, PID 7338/engine 8449, is preserved. A separate
port-8015 server, PID 242538/engine 243285, serves the same pinned
Qwen/Qwen2.5-7B-Instruct revision
`a09a35458c702b33eeacc393d103063234e8bc28` in BF16, one GPU, one sequence,
eager execution, CPU offload zero and swap zero. Its context is 16,384 tokens,
GPU reservation 0.4 and observed allocation initially 19,708 MiB and 20,006 MiB before evaluation, alongside the
original server's 24,618 MiB. Temperature remains 0.3 and top-p 1.0. The separate
retail configuration allows 15,872 input and 512 output tokens, one structured
sample per tool turn. Native BF16 CUDA execution, serving ancestry/allocation,
model flags, logs, model endpoint and health were checked.

Port 8001 was occupied by the existing nginx service, so the first separate
server launch failed before generation or model allocation. Its log is retained.
Transfer initially encountered unsupported ownership changes on the persistent
volume; subsequent content transfers preserved pod ownership. Neither issue
changed existing authentication or services.

The [session audit](../artifacts/stage5_practical/session_accounting.json)
reconciles **3,311 scheduled calls, 3,313 GPU attempts, 3,310 parsed generations,
three failed generation attempts and two retries**. One ordinary call exhausts
both attempts. All three failed attempts are HTTP-200 outputs stopped at the
512-token limit; there are no failed preflights, unfinished attempts, unlogged
reservations or unknown token counts. There are no placement generations or
LLM user-simulator calls.

| Phase | Workflow attempts | Calls | GPU attempts | Failed generation attempts | Runtime |
|---|---:|---:|---:|---:|---:|
| Initial development pilot | 12 | 168 | 168 | 0 | 184.55 s |
| Revised pilot | 12 | 90 | 90 | 0 | 110.82 s |
| Calibration | 72 | 602 | 602 | 0 | 926.89 s |
| Frozen evaluation | 288 | 2,451 | 2,453 | 3 | 4,016.41 s |
| Total | 384 | 3,311 | 3,313 | 3 | Phase runtimes exclude intervening analysis/setup |

The stage consumes **15,777,578 prompt tokens and 257,047 completion tokens**;
evaluation contributes 11,837,012 and 197,346. Server counter deltas exactly
match all 3,313 completed HTTP generations, including truncated outputs, and
both token totals. Evaluation generation-request wall time is 3,845.65 seconds;
its 4,016.41-second end-to-end runtime is 1.083 times the 3,707.54-second forecast,
within the frozen 1.75 safety margin. The largest input is **11,883 tokens**;
all 3,313 tokenizer input counts match server usage. No overlapping attempt
intervals are detected. The output cap caused the three retained failures.

Actual search dispatches have at most two eligible requests: **five ordered
subsets**, mean **0.05135 ms**, p95 **0.07699 ms**, maximum **0.12670 ms** for the
218 two-request decisions across both capacities. Three-request no-review
states support hypothetical 16-subset audits; they are not actual three-request
search-dispatch timing measurements. Planning runs on the recorded local
Intel i5-10400 host (Python 3.8.10), not the GPU pod. The measured call includes
eligibility and public-record construction, excludes later alternative-policy
diagnostics, and is not a scalability or hard real-time guarantee.

Existing focused tests and the final nine application semantic checks pass.
Stage 1, 2, 3 and all Stage 4 historical audits pass without new inference;
11,117 historical files retain their original hashes. All 288 evaluation
preparations replay from both original and redacted public evidence, and all
1,152 policy traces replay. The integrity audit verifies 512 original evidence
file hashes, all 44 frozen source snapshots, unchanged execution/scoring methods
and estimator, and the pre-generation freeze commit. Two documented rendering
corrections move a legend and add a missing space; they change no analysis or
experiment semantics.

Evaluation workers finish at **2026-09-10 16:23:02 UTC**. Final GPU evidence is
captured at 16:23:59 UTC; the separate Stage 5 serving group is stopped and its
absence verified at **16:27:24 UTC**. Cleanup's status step initially lacked a
read-only helper and the locally captured baseline file; copying them completes
verification without restarting a server or generating another output. The
original PID 7338/engine 8449 remains healthy on port 8000 with its **51,347**
generation counter unchanged and 24,618 MiB GPU allocation. All persistent files
and cached weights remain. Billing information is unavailable, so no monetary
allocation estimate is inferred.

At the final reporting checkpoint **2026-09-10 17:03:04 UTC**, Stage 5 elapsed time is **2 h 47 min 44 s**, including setup, waits, development, evaluation, analysis and reporting. Cumulative wall time since the original start is **25 h 24 min 7 s** against the 36-hour target, leaving **10 h 35 min 52 s** and **zero overrun**. The final Git commit's committer timestamp marks completion of packaging and verification; clocks were not backdated. The adapter milestone is `0ac0cbfa2bb6ba8906a19e3a3ca2f08a8c7f424f`; the pre-generation evaluation freeze is `d0f47978e722988220240e74fb625cd8598293b1`. This completes the selected batch well within the nine-hour ceiling; unused time and call capacity do not authorize extending the frozen experiment.


Unsolicited credential-like text occurred in model-generated auxiliary
confirmation arguments, a truncated response, and subsequent prompt histories.
It was never used for authentication or sent to an external application tool.
The public package redacts these values in 16 model responses, 25 subsequent request attempts and auxiliary traces in four workflows (eight files), and preserves original live payload,
response and file hashes in the [publication manifest](../artifacts/stage5_practical/publication_redactions.json).
Public `request_hash` fields describe the redacted view; `original_request_hash`
retains the live payload hash when a prompt changed. The exact originals remain
on the pod and in a Git-ignored local evidence directory. Original and public
traces are each replayed. Staged transactions, backend states, labels,
attempts, token accounting and scheduling scores remain unchanged. Public
redacted prompts are not claimed to regenerate the original model responses.

## Reproduction

The source and batch declarations used the corresponding recorded source revision:

```bash
python3 scripts/prepare_retail_cases.py
python3 scripts/retail_experiment.py declare development_pilot --bundles 4 --replicates 0
python3 scripts/retail_experiment.py declare development_revision1 --bundles 4 --replicates 1
python3 scripts/retail_experiment.py declare development_calibration --bundles 8 --replicates 2 3 4
python3 scripts/analyze_retail.py fit development_calibration
python3 scripts/retail_experiment.py declare evaluation --partition evaluation --bundles 32 --replicates 0 1 2 --estimator artifacts/stage5_practical/estimator.json
```

These were interleaved with the corresponding development runs and the single
interface revision; they are not instructions to overwrite existing declarations
or to refit the frozen estimator. The original interface is in its source snapshot.
The prepared configuration, manifest and source hashes make those differences
explicit.

The exact bounded preparation commands used on the pod were:

```bash
.venv/bin/python scripts/run_retail_bounded.py development_pilot
.venv/bin/python scripts/run_retail_bounded.py development_revision1
.venv/bin/python scripts/run_retail_bounded.py development_calibration
.venv/bin/python scripts/run_retail_bounded.py evaluation
```

Each batch's declaration and source snapshot precede its first call. The failed
initial interface remains available in the pilot snapshot. Publication redactions
are applied by `python3 scripts/package_practical_evidence.py --complete`; their manifest
records the redacted prompt/auxiliary text and verifies unchanged staged transactions, states, labels and accounting. The separate serving
command is [scripts/serve_retail_gpu.sh](../scripts/serve_retail_gpu.sh), run in
the reused checkout with `HF_HOME` set to its `model-cache` directory; its full
arguments and PID are retained in `setup/launch.json` and GPU evidence.
The serving invocation was `HF_HOME="$PWD/model-cache" bash scripts/serve_retail_gpu.sh`, launched in its own process group with output redirected to `setup/server_port8015.log`. Final cleanup uses `.venv/bin/python scripts/finish_practical_runtime.py` after all preparation workers exit.
No model/environment installation was necessary. The existing server was never
reconfigured. These historical run directories are one-shot, and the original
authorization expires; repeating live inference requires a fresh explicitly
authorized output root and deadline, rather than overwriting these results.

Saved-data verification requires no GPU or new authorization:

```bash
python3 -m unittest discover -s tests -p test_retail.py
python3 scripts/analyze_retail.py audit development_pilot development_revision1 development_calibration evaluation
python3 scripts/analyze_retail.py score evaluation
python3 scripts/audit_retail_session.py
python3 scripts/verify_practical_package.py
python3 scripts/audit_practical_sources.py
python3 scripts/summarize_practical_errors.py
python3 scripts/audit_practical_scheduling.py
python3 scripts/plot_retail.py
python3 scripts/retail_traces.py
```

Plotting uses the existing `requirements-analysis.txt` environment. Replaying
saved traces preserves their original planning times and verifies all causal
events and losses; it does not promise bitwise regeneration of model outputs.

## Contribution and remaining limits

Primary-source/code verification and BibTeX are in
[RELATED_WORK.md](../paper/RELATED_WORK.md),
[references.bib](../paper/references.bib), and the
[source hashes](../artifacts/stage5_practical/sources/verified_sources.json).
τ-bench supplies the application substrate. KnowNo, Value of Information,
One Human N Agents and DeCCaF establish relevant help-seeking, communication,
shared auditing and cost/capacity allocation mechanisms. Four released
implementations linked by the respective authors/projects were inspected. No author-linked release for One Human N Agents
was located in its paper or focused searches; that availability limit is explicit.
Their full methods are conceptual comparisons, not reproduced baselines.

The contribution is the adapted transaction-review experiment and its measured
allocation evidence. Shared oversight, cost-aware deferral and exhaustive
scheduling are not new. Perfect review, scripted confirmation, constructed
cutoffs/weights, single-transaction cases, a single model and shared instruction
templates limit external validity. Public benchmark training cases may also
have been seen during model training. This experiment cannot establish actual
retailer savings, human workload, general LLM alignment, or full-horizon optimality.

This stage completes a genuine, bounded retail tool-workflow adapter and a
valid frozen comparison. It does **not** support a retail search-over-greedy
advantage: the point estimate is unfavorable, most scenario bundles tie, and
search spends more review time for slightly fewer correct tasks. Faster reviews
eliminate all queued semantic errors for every tested scheduler, while failures
before staging set a substantial ceiling. Better aggregate risk scoring does
not guarantee the relevant risk ranking or a planning benefit.

The strongest supported practical contribution is the explicit, auditable
transaction-review experiment and its boundary conditions, alongside preserved
maintenance evidence of conditional planning gains. Before submission, the
single most useful next step is **an independent domain review of the corrective
authority, processing cutoffs and consequence weights**. That would establish
which application assumptions deserve a separately preregistered robustness
study. No additional experiment, refit or scope revision was run after evaluation.
