# OverseeingManyLLMs

A reproducible research framework for allocating one simulated reviewer across LLM agents. It includes measured laboratory HVAC diagnosis, synthetic civilian maintenance, and adapted tau-bench retail workflows on simulated customer records. Review duration, expiring intervention opportunities, risk estimates and operational loss are explicit; supervision is simulated throughout.

Start with the [practical application report](reports/STAGE5_PRACTICAL.md), [source/adaptation table](paper/RETAIL_ADAPTATION.md), and completed [Stage 4 research report](reports/STAGE4_RESEARCH.md), [research draft](paper/RESEARCH_DRAFT.md), [competition report](reports/STAGE3_COMPETITION.md), [Stage 2 report](reports/STAGE2_DEVELOPMENT.md), [core method](paper/CORE_METHOD.md), and [proof-of-concept plan](plan/PROOF_OF_CONCEPT_PLAN.md). The runtime uses an **RTX 6000 Ada**, the pinned **Qwen2.5-7B-Instruct** model, BF16, and zero CPU offloading. Supervision is simulated. Stage 1's [preserved GPU report](reports/STAGE1_GPU_LIVE.md) records its four-policy zero-loss tie with no corrections.

Stage 2 adds an offline agreement-based error estimator and a delay-aware greedy baseline. Calibration uses 16 FCFS episodes with provisional **p=0.5**; the frozen estimator then drives five policies on eight development scenarios. The declared scope is 56 episodes, 672 experimental calls, and at most one placement generation. A bin with fewer than ten calibration examples uses the smoothed pooled estimate. This development batch is not a held-out effectiveness study.

All 56 episodes completed and replayed: **672 experimental generations plus one placement**, with no retries or failures. Calibration had 87 agreeing pairs (12 errors) and nine disagreeing pairs (five errors), so disagreement used pooled fallback. Validation loss totaled 60 for FCFS/uncertainty-first and 62 for myopic/greedy/queue search; each policy corrected two jobs. Queue search and greedy chose identical review orders on all eight scenarios. These ties and negative results are retained.

## Measured HVAC study and current manuscript

The principal externally grounded application uses **measured FLEXLAB sensor data** with experimentally imposed fault labels. Eight whole days are development and **18 held-out day blocks on one air handler** supply 54 proposal/review pairs. Windows and policy replays are not independent buildings or source cases.

The proposer gets **19/54** diagnoses correct, versus **27/54** for a development-trained conventional baseline. Model review corrects one error but makes six correct proposals unresolved. The frozen signed-benefit rule declines review, so the primary search-minus-greedy difference is mechanically **0 [0, 0]**, with 18 day ties. This is not proof of scheduling-policy equivalence. Risk-only scheduling applies harmful reviews and raises search loss relative to no review by **2.667 [0.217, 5.778]**. Under ideal review, search improves on greedy by **3.333 [1.778, 4.889]** loss points, while **EDF matches search**.

All **204 GPU attempts** succeed, with no retries. The **3,888 paired scheduling traces** and result tables replay without inference. Arrivals, cutoffs, review duration and loss weights remain constructed assumptions; no repair outcomes, energy savings or human performance are measured. SQL was not evaluated because Critic reference assets require contact and a valid BIRD-SQL fallback did not fit the remaining original deadline.

Read the [Stage 7 report](reports/STAGE7_EMPIRICAL.md), [provenance](artifacts/stage7_empirical/provenance.json), [assumption assessment](paper/HVAC_ASSUMPTIONS.md), [eight-page manuscript](paper/main.pdf), [17-page supplement](paper/supplement.pdf), and [reproduction guide](paper/STAGE7_REPRODUCTION.md). The main paper retains both unfavorable retail comparisons and condenses synthetic maintenance into a mechanism study.

```bash
bash scripts/replay_stage7.sh
```

This reconstructs saved-output tables, figures and PDFs without new inference. Historical artifacts, clocks and redaction provenance are preserved. The original server remains healthy. No new server or paid resource was provisioned.

## Robustness study and ICAART manuscript

Stage 6 is complete on **24 fresh source cases in eight disjoint bundles**, each with three GPU preparation replicates. It preserves the Stage 5 risk estimator and preparation interface while separately testing approve-or-block authority and one extra review tick for multi-item proposals. All 120 prior accounts are excluded across the pinned train/dev/test splits. Only ten eligible modification accounts remain, so the declared eight-bundle fallback is used.

The restricted-authority primary result is unfavorable to search: **+1.6667 loss points versus greedy, 95% paired interval [0.0000, 4.6667], W/T/L 0/6/2**. Blocking prevents posting consequences but does not complete the request. All policies complete the same 39 initially correct tasks under this authority. The 72 fresh workflows include 51 staged proposals, 12 initial errors and 21 unstaged failures. All 675 GPU calls succeed with no retries. The 864 fresh policy traces and 3,456 separate post hoc traces replay, including 1,152 exact historical reference matches.

| Fresh two-tick policy | Correction mean loss | Approve/block mean loss | Complexity-time mean loss |
|---|---:|---:|---:|
| No review | 9.8333 | 9.8333 | 9.8333 |
| FCFS | 5.5000 | 7.0000 | 5.8333 |
| EDF | 5.5000 | 7.0000 | 5.8333 |
| Uncertainty-first | 3.5000 | 5.5000 | 3.8333 |
| Delay-aware greedy | 3.5000 | 5.5000 | 3.8333 |
| Queue-order search | 5.8333 | 7.1667 | 6.1667 |

At one tick, every review policy prevents all staged errors in each fresh condition. The restricted-authority completion floor and no-review invariance follow from the semantics. They are not new empirical discoveries. The fresh eight bundles and the post hoc 32-bundle sensitivity remain separate; broad source templates are shared and public-data contamination is not ruled out.

Read the [Stage 6 report](reports/STAGE6_ROBUSTNESS.md), [source-based assumption review](paper/RETAIL_ASSUMPTION_REVIEW.md), [manuscript](paper/main.pdf), [supplement](paper/supplement.pdf), and [reproduction guide](paper/STAGE6_REPRODUCTION.md). The Stage 6 manuscript originally had nine pages and its supplement ten, preserved at commit d9b39589. The current PDFs linked above incorporate Stage 7 using the same official ICAART 2027 template. Human authors must finalize submission declarations and confirm AI-disclosure/supplement handling; nothing is pushed or submitted.

At the preserved Stage 6 commit `d9b39589`, reproduce its saved tables, figures and original PDFs without inference using the command below. On current main, use the Stage 7 command above for the updated manuscript and audits that write only to the new artifact directory.

```bash
bash scripts/replay_stage6.sh
```

The [plan](plan/STAGE6_ROBUSTNESS_PLAN.md) and [frozen declaration](artifacts/stage6_robustness/batches/evaluation/declaration.json) predate fresh inference. The original GPU server remains healthy and the separate Stage 6 server/workers are stopped. Stage 6 has its own six-hour clock; all earlier clocks and evidence remain intact.

## Practical retail application

The Stage 5 study uses 96 evaluation source cases in 32 bundles, three fresh GPU preparation replicates and two review capacities. FCFS, EDF, uncertainty-first, greedy, search and no review receive identical saved transactions; policy replay isolates scheduling without claiming subsequent agent feedback adaptation. A development-only application estimator replaces the maintenance risk model. Upstream tool guards remain active, while only a completed perfect simulated review can correct a staged semantic mistake before its processing cutoff.

All 288 workflow attempts and 1,152 paired policy traces complete and replay. There are 233 staged proposals, 51 initial errors and 55 unstaged failures. **The primary result does not show a search advantage:** two-tick search minus greedy mean loss is +0.2500, 95% paired interval [−0.3333, 1.0000], over 32 bundle means. One-tick review policies all reach the preparation-failure floor.

| Policy | Mean loss, 1 tick | Mean loss, 2 ticks | Correct tasks, 2 ticks / 288 | Wrong commits, 2 ticks |
|---|---:|---:|---:|---:|
| No review | 8.3333 | 8.3333 | 182 | 51 |
| FCFS | 2.2917 | 5.0000 | 210 | 23 |
| EDF | 2.2917 | 4.5833 | 215 | 18 |
| Uncertainty-first | 2.2917 | 3.4583 | 223 | 10 |
| Delay-aware greedy | 2.2917 | 3.4583 | 223 | 10 |
| Queue-order search | 2.2917 | 3.7083 | 222 | 11 |

The session uses 3,313 GPU attempts across 3,311 calls, with three truncated attempts and two retries. The original inference server remains healthy; the separate retail server is stopped. These are adapted transaction-boundary comparisons with perfect simulated review, not measured human or retailer performance.

Verify saved evidence without inference:

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

Figures use Matplotlib. The [frozen declaration](artifacts/stage5_practical/batches/evaluation/declaration.json), raw traces, source snapshots, estimator, ledger and analysis CSVs are under `artifacts/stage5_practical/`. The [report](reports/STAGE5_PRACTICAL.md) records exact historical server/preparation commands and clock limits. Live runs are one-shot and require an unexpired explicit authorization; saved-data verification does not. A disclosed publication redaction removes unsolicited credential-like text from auxiliary tool arguments, responses and later prompts. Exact originals remain on the pod; staged transactions, backend states, labels and scores are unchanged. This is an adapted benchmark study, not an official τ-bench score or a human study.

## Inspect and verify

Core host simulation and replay require Python 3.8+ and the standard library. Stage 4 summaries and its integration checks also use NumPy; figure rendering uses Matplotlib (`requirements-analysis.txt`). Exact analysis versions are saved with the research artifacts. These commands perform no model inference:

```bash
python3 -m unittest discover -s tests -v
python3 -m overseeing mechanics --out artifacts/local-mechanics
python3 -m overseeing replay artifacts/local-mechanics/competition/delay/events.jsonl
python3 -m overseeing development-mechanics --out artifacts/local-development-mechanics
python3 scripts/verify_development.py artifacts/stage2_development/run
python3 scripts/verify_competition.py artifacts/stage3_competition/run

task_artifacts=artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z
python3 scripts/verify_live_results.py "$task_artifacts/run"
for policy in fcfs uncertainty myopic delay; do
  python3 -m overseeing replay "$task_artifacts/run/$policy/events.jsonl"
done
```

Use a fresh mechanics output directory on repeat runs. The five examples use **stipulated actions as mechanics fixtures**. Live raw requests/responses, episode CSV, event traces, queue timeline, GPU evidence, exact environment versions, and the executed source snapshot are saved together under [the Ada artifact directory](artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/). The verifier uses that snapshot so later source changes do not invalidate the historical audit.

The [development artifacts](artifacts/stage2_development/run/) contain the pre-inference declaration, frozen estimator, raw attempts, all 56 episode rows, replayable traces, per-policy Brier scores, paired scenario differences, and dispatch-competition diagnostics. The development verifier recomputes diagnostics from saved outputs without generation requests.

## Verified GPU setup

In a dedicated pod checkout, the setup used the available Python 3.11.13 and these commands:

```bash
uv venv --python python3.11 .venv
timeout 5400 uv pip install --python .venv/bin/python -r requirements-gpu.txt
HF_HOME="$PWD/model-cache" bash scripts/serve_gpu.sh
```

The launcher serves the pinned model and tokenizer revision `a09a35458c702b33eeacc393d103063234e8bc28` on `127.0.0.1:8000`. It requires one verified L40S or RTX 6000 Ada with at least 45,000 MiB VRAM and native CUDA BF16. The 0.5 memory reservation, tensor parallelism 1, CPU offload 0, and swap 0 are fixed. Keep Jupyter and other existing services running.

The [report](reports/STAGE1_GPU_LIVE.md) records the exact SSH, isolated directory, detached server launch, and one-shot demonstration command, with server PID, logs, and full resolved dependency versions. The live CLI accepts `--continuation stage1_gpu_live_rtx6000_ada`, using its recorded deadline by default or an earlier explicit `--deadline-utc`. It retains the original overall deadline and rejects unknown, expired, or overlong continuation windows. Saved runs cannot be overwritten; the recorded demonstration wrapper also refuses a repeat execution.

The separate development path predeclares source/configuration hashes and ordered episodes before inference:

```bash
python3 -m overseeing prepare-development --out artifacts/stage2_development/run
.venv/bin/python -m overseeing develop --out artifacts/stage2_development/run \
  --server-pid 7338 \
  --server-log artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/server.log \
  --deadline-utc 2026-09-10T03:07:01+00:00
```

These are historical execution commands. Existing outputs and the one-shot execution marker prevent repetition. The named Stage 2 authorization and original overall deadline remain enforced; subsequent inference requires its own authorization.

## Preserved history and scope

The [original backbone report](reports/STAGE1_GPU_BACKBONE.md), [blocked recovery](reports/STAGE1_GPU_RECOVERY.md), and [first L40S live report](reports/STAGE1_GPU_L40S.md) remain available with their original artifacts. All clocks are retained in [implementation_clock.json](reports/implementation_clock.json).

The declared development calibration and fifth baseline are implemented. The separate Stage 3 condition adds deadline-first scheduling and a one-versus-two-tick review comparison. Stage 4 extends this history with frozen evaluation seeds, a larger workload, public risk references, and a research draft. The separate Stage 5 application adds bounded retail transaction workflows; richer interactive application evaluation and real-human validation remain outside the implemented scope. Weights, environments, and credentials are excluded from Git. Nothing is pushed automatically.

## Stage 3 competition diagnostic

Motivated by Stage 2's limited competition, a separate generator releases three jobs together at ticks 0 and 6, independently permutes deadline windows 2/4/5 and penalties 4/8/12, and sets downtime costs to zero. The frozen Stage 2 estimator is reused without fitting. Six policies, two review durations, and seeds 300–315 give **192 episodes / 2,304 experimental calls**, with one separate placement request. The 192 repeated conditions represent 16 paired scenarios, not 192 independent observations. Historical policy lists and commands retain their original scope.

All 192 episodes completed and replayed with **2,305 total GPU generations, zero retries/failures**. At one tick, search and EDF tied at loss 0 versus greedy's 12. At two ticks, search totaled 44 versus greedy's 52 and EDF's 84, while losing on individual scenarios. Search/greedy orders differed in 15/16 and 14/16 scenarios. These deliberately constructed development results are separate from Stage 2; exact regenerated actions are not assured, and every saved result remains replayable.

[Declaration and raw evidence](artifacts/stage3_competition/run/), [paired-loss figure](artifacts/stage3_competition/run/paired_loss.png), and [first differing queue example](artifacts/stage3_competition/run/queue_example.md) accompany the [report](reports/STAGE3_COMPETITION.md). Verify saved results with the command above. Recreate the figure with `python3 scripts/plot_competition.py artifacts/stage3_competition/run` (requires Matplotlib; the audit itself uses only the standard library).

Historical execution commands, guarded against overwriting or rerunning the saved batch:

```bash
python3 -m overseeing prepare-competition --out artifacts/stage3_competition/run
.venv/bin/python -m overseeing competition --out artifacts/stage3_competition/run \
  --server-pid 7338 \
  --server-log artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/server.log \
  --deadline-utc 2026-09-10T04:47:37+00:00
```

The separately recorded Stage 3 authorization lasts at most two hours and remains within the original overall deadline. Earlier command deadlines are unchanged. That historical authorization ends with its batch; Stage 4 uses its own separately recorded scope.

## Stage 4 research session

The bounded research session completed **2,752 frozen evaluation episodes plus 304 development episodes**, all replayed, with **48,320 successful GPU generations, zero retries and zero failures**. The [completed report](reports/STAGE4_RESEARCH.md), [register](artifacts/stage4_research/RESEARCH_PLAN.md), and [decisions](artifacts/stage4_research/decisions.jsonl) distinguish development from frozen evaluation. The execution used a shared 50,000-call / 60,000-attempt ledger and reserved the final 90 minutes before the stage deadline for reporting. All experimental workers have stopped; the existing GPU server and pod files remain intact. Historical commands retain their previous limits. No claim is made that equal sampling seeds reproduce identical GPU actions.


The main findings are conditional. Search minus greedy mean loss at two ticks is **−0.094** on the original workload (95% paired interval includes zero), and **−1.313** on the constructed competition workload ([−2.250, −0.438]). EDF matches search's zero loss at one-tick competition. Larger-workload planning gains are strong at one tick but small at two. Analytical public risk improves prediction scores without consistently improving allocation. Adding an incorrect-closure penalty reduces wrong closures at one tick while increasing original cost; null and negative results are retained. See the report for all policies, per-agent outcomes and scenario-paired comparisons.

The [saved-output reproduction guide](artifacts/stage4_research/REPRODUCE.md) gives exact audit and rendering commands. The new larger workload supports three or six agents, three jobs per agent, a 24-tick horizon, and at most six outstanding requests. Search enumerates every ordered subset of the eligible public queue; no queue truncation or future-arrival access is used. Frozen agreement, pooled calibration, and analytical public-clue risk rules are compared without refitting. The selected extension adds a declared incorrect-closure penalty while retaining original maintenance loss as a separate metric.

```bash
python3 scripts/analyze_research.py --batches evaluation --label evaluation
python3 scripts/audit_numerical_ties.py --batches evaluation --label evaluation
python3 scripts/audit_objective_null.py
python3 scripts/plot_research.py
python3 scripts/research_traces.py
python3 scripts/research_tables.py
python3 scripts/audit_research_session.py
```

The [research draft](paper/RESEARCH_DRAFT.md), [claim–evidence map](paper/CLAIM_EVIDENCE.md), and [verified related-work note](paper/RELATED_WORK.md) distinguish the framework and measured analysis from established scheduling and uncertainty-guided help-seeking methods. Supervision remains simulated; exhaustive scheduling itself is not claimed as novel.


## Verification-guided escalation exploration

The separate [research package](research/verification_escalation/README.md) includes
a local Decision desk, a frozen SQL comparison on 24 new AMBROSIA databases,
controlled counterexamples, and [a completed report](research/verification_escalation/REPORT.md).
Generated-query agreement reduced questions but increased mismatched releases.
Source recovery and targeted clarification remain the supported default; source
integrity and candidate coverage limitations are explicit. The existing submission
and all earlier experiments remain unchanged.
