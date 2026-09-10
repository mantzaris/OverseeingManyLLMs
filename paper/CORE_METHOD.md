# Core method: allocating simulated supervision

## Research question

How should one simulated human supervisor allocate a limited amount of review time across three LLM agents when incorrect actions incur continuing cost and the opportunity to correct them expires? The implemented comparison asks whether planning review order using completion times changes loss relative to FCFS, uncertainty-first, myopic benefit, and delay-aware greedy. The backbone and small development batches establish integration and diagnostics; they do not establish policy superiority or novelty.

## Implemented mechanism

Each agent receives two independent synthetic campus ventilation maintenance jobs during a 12-tick episode. A hidden `filter` or `sensor` fault determines the correct repair. Agents see their current public job, a shared manual, two noisy clues with declared accuracies 0.8 and 0.6, costs, deadline, and their own action/review history. Hidden faults and unreleased jobs are excluded from these observations.

The pinned Qwen2.5-7B-Instruct model makes two independently seeded GPU generation requests for the same observation. The first action executes immediately; the second is retained only to measure agreement. Every proposal joins the review queue. Valid wrong actions remain valid model outputs. Stage 1 and development calibration collection use the **provisional, uncalibrated constant `p=0.5`**. Development validation uses a frozen empirical agreement-based estimate; no online updating occurs.

## Frozen agreement estimator

Calibration collects 16 FCFS episodes, seeds 200–215, at review duration two. Every successfully collected action pair receives an offline label: whether the **first initial proposal** was wrong, before any supervisor correction. Reviewed status does not select examples. A partial episode contributes its successfully collected pairs; missing pairs remain missing and are counted. Truth is accessed only by this offline extraction, scoring, and completed supervision.

For agreement bin `b`, estimate `p_b=(errors_b+1)/(count_b+2)`. A bin with fewer than ten examples uses the pooled calibration estimate `(total_errors+1)/(total_examples+2)`. Counts, errors, fallback decisions, source-trace hashes, and the fitted estimator hash are saved. A frozen immutable predictor accepts only the two sampled action strings, with no access to hidden state or review status.

The estimator is frozen before the first validation episode. Validation uses seeds 216–223, five policies, and review duration two: 40 episodes. Policy order rotates by scenario; sampling seeds exclude policy and execution order. Each policy uses fresh generation calls and separate histories. The full development stage has 56 episodes and 672 scheduled experimental calls, plus at most one placement generation.

In the completed batch, agreeing calibration pairs had 12 initial errors among 87 examples; disagreeing pairs had 5 among 9 and therefore triggered pooled fallback. Frozen probabilities were 13/89 for agreement and 18/98 for disagreement. The [fitted estimator](../artifacts/stage2_development/run/estimator.json) preserves these counts, provenance, and hash.

Prediction diagnostics compare the frozen estimator, constant 0.5, and the pooled calibration estimate using Brier scores on the **same saved validation trajectories**, separately by policy and agreement bin. Alternative prediction scores do not estimate counterfactual scheduling performance. Validation labels never update the estimator.

Schedulers receive only immutable public review records for released, pending jobs: proposal, estimated error probability, request time, costs, deadline, and review duration. They cannot inspect hidden faults, future jobs, scorer loss, or another agent's feedback. The supervisor performs one nonpreemptive review at a time. Reviews take two ticks in Stages 1–2; Stage 3 compares one and two ticks. Only when the review completes does it obtain definitive diagnostic information and command the correct action. The controller obeys immediately for an open job. Review cannot erase accumulated loss or reopen a closed job.

At each tick the simulator applies completed reviews, closes due jobs, releases new jobs and resolves their model calls, dispatches a review, then charges interval costs. Completion exactly at the deadline can prevent terminal loss. Inference wall time pauses the simulated clock, so hardware latency does not determine queue order. Full truth in saved scorer traces is offline diagnostic data, never a scheduler input.

## Loss and scheduling

For job `i`, release `r_i`, deadline `d_i`, downtime rate `c_i`, terminal cost `K_i`, action `a_i(t)`, and correct action `a_i*`, the episode loss sums

`loss_i = c_i Σ[t=r_i,...,d_i−1] 1[a_i(t) ≠ a_i*] + K_i 1[a_i(d_i) ≠ a_i*]`.

The preventable consequence of completing a review at `T` is

`G_i(T) = 1[T ≤ d_i] [c_i(d_i−T) + K_i]`.

All policies skip requests with no positive estimated benefit at earliest completion `t+s_i`.

| Policy | Dispatch rule for feasible requests |
| --- | --- |
| FCFS | Earliest request, with agent ID as tie-break. |
| Uncertainty-first | Highest `p_i`; shared FCFS tie-break. Constant probabilities can make it identical to FCFS. |
| Myopic benefit | Highest `p_i G_i(t)`, ignoring service time in the ranking. |
| Delay-aware greedy (`greedy`) | Highest `p_i G_i(t+s_i)`, with the shared request-time/agent-ID tie-break. |
| Earliest-deadline-first (`edf`, Stage 3) | Earliest absolute deadline, followed by the shared request-time/agent-ID/job-ID tie-break. |
| Queue-order search (`delay`) | Enumerate ordered subsets of the current queue and maximize `Σ_k p_i G_i(t+Σ_{j≤k}s_j)`; dispatch the first review and recompute when free. |

Queue-order search optimizes the current queue estimate, without anticipating arrivals. Tied plans prefer fewer reviews, then lexicographic request/agent order. Correct jobs at closure are reported alongside loss: a wrong job with both costs zero contributes zero loss.

## Assumptions and evidence

Supervision is **simulated**, with perfect diagnosis, fixed duration, and mandatory compliance. There are no human participants or measurements of workload, trust, or usability. Automatic review admission, two repair actions, independent synthetic jobs, and public deterministic deadlines/costs are simplifying assumptions. Stage 1 probabilities are uncalibrated; the development estimator is a small empirical fit with no reliability guarantee. Two samples can agree on an incorrect action.

The five [Stage 1 mechanics fixtures](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/mechanics/episodes.csv) stipulate actions to demonstrate arithmetic, correction, competition, expiry, and a baseline win. They are not model-quality observations. The [extended competition fixture](../artifacts/stage2_development/mechanics/episodes.csv) shows greedy choosing B first (loss 8) while queue search chooses A first (loss 0); these remain stipulated actions.

Stage 1's [Ada report](../reports/STAGE1_GPU_LIVE.md) and [episode CSV](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/episodes.csv) preserve its zero-loss tie with no corrections. The [development report](../reports/STAGE2_DEVELOPMENT.md) links the frozen estimator, live outcomes, raw requests, replay, Brier diagnostics, and dispatch competition. The eight validation scenarios are development diagnostics. Their five policy repetitions are not 40 independent scenarios and are not a final effectiveness study. The controlled Stage 3 duration comparison is described below. Held-out evaluation, larger experiments, and a full manuscript remain later work.

Observed Stage 2 validation loss was 60 for FCFS/uncertainty-first and 62 for myopic/greedy/queue search, with 42/48 jobs correct and two corrections per policy. Queue search and greedy had identical review orders on all eight scenarios. Only three scenarios contained competing eligible requests. Frozen-estimator Brier score was 0.138521 versus 0.139178 for the pooled estimate and 0.25 for constant 0.5 on each policy's observed trajectory. These [diagnostics](../artifacts/stage2_development/run/prediction_diagnostics.csv) show little incremental predictive improvement over the pooled base rate; they do not establish agreement-based calibration or a scheduling advantage.

## Constructed competition condition (Stage 3)

Stage 2 had identical greedy/search orders, limited simultaneous eligible reviews, and slightly higher loss for search than FCFS. Stage 3 therefore deliberately changes the workload to investigate competition. This is a development diagnostic motivated by observed Stage 2 limitations, not an independent confirmation on the original distribution. The original generator, configurations, results, and estimator remain preserved.

For each of seeds 300–315, three first jobs arrive together at tick 0 and three second jobs at tick 6. Each wave independently permutes relative deadline windows `{2,4,5}` and terminal penalties `{4,8,12}` across the three agents. Separate seeded random streams generate deadline assignments, penalty assignments, and hidden faults/clues. Faults retain the equal binary prior and clues retain independent accuracies 0.8 and 0.6. Public urgency and penalty do not depend on hidden faults or clue correctness. Every declared scenario is included. Random permutation provides exchangeability across agent IDs; finite samples need not have exactly equal counts.

Downtime cost is zero, isolating terminal missed-deadline loss. Within the common positive-benefit eligibility guard, myopic and delay-aware greedy both rank `p_i K_i`; they are mathematically equivalent on a shared public state. Queue search may select a smaller immediate benefit to preserve multiple future completions. Earliest-deadline-first instead prioritizes urgency without weighting terminal penalties. Exhaustive scheduling itself is not claimed as novel. The experiment examines these rules inside an LLM action/feedback loop with imperfect error estimates and simulated supervision.

The Stage 2 estimator is loaded byte-for-byte and hash-verified: agreement probability `13/89`, disagreement probability `18/98` via the original sparse-bin fallback. No Stage 3 label is used to fit or update it. All six policies run on each scenario at review durations one and two: 192 episodes but only **16 paired scenario units**. Each episode receives fresh GPU calls and isolated agent histories. Scenario identity and per-sample seeds are independent of policy and duration; actual prompts can differ after different reviews. Policy order rotates and each duration runs first for eight scenarios.

The [Stage 3 declaration](../artifacts/stage3_competition/run/declaration.json) fixes source/configuration/scenario/estimator hashes, execution order, 2,304 experimental calls plus at most one placement generation, retries/timeouts, and analysis definitions before inference. Analyses separate durations and report paired scenario losses, review sequences, choices on identical saved public states, initial-action errors, and frozen-estimator Brier scores. Comparing choices on a saved state is not a counterfactual rollout. A changed review order is distinct from a reduction in realized loss. The queue illustration uses the first numerical seed with different greedy/search sequences, irrespective of the winner.

Measured results and limitations are in the [Stage 3 report](../reports/STAGE3_COMPETITION.md), [policy outcomes](../artifacts/stage3_competition/run/policy_outcomes.csv), [paired comparisons](../artifacts/stage3_competition/run/paired_comparisons.csv), and [prediction diagnostics](../artifacts/stage3_competition/run/prediction_diagnostics.csv). This narrow synthetic condition, small frozen calibration sample, binary actions, perfect simulated diagnosis, mandatory compliance, and selected review durations do not establish general effectiveness or human benefit.

All 192 Stage 3 episodes completed and replayed, with 2,304 experimental GPU generations plus one placement and no retries/failures. At review duration one, total losses were FCFS 28, uncertainty-first 28, myopic/greedy 12, and EDF/search 0. At duration two, losses were 52, 56, 52, 52, 84, and 44 respectively. Search versus greedy had scenario win/tie/loss counts 3/13/0 at one tick and 3/12/1 at two; search versus EDF had 0/16/0 and 5/9/2. Different greedy/search sequences occurred in 15/16 and 14/16 scenarios, much more often than loss differences. At two ticks every policy missed 32 review opportunities; search reduced weighted loss while leaving more jobs incorrect than greedy (11 versus 8). These are observed results of the constructed condition, not a general superiority claim.

The frozen estimator underpredicted observed initial errors (about 27–28% overall), with Brier scores around 0.211–0.219 and only 3–6 disagreement examples per policy/duration. Two groups of repeated identical requests, including sampling seeds, returned different valid actions; the cause is not established and no calls were rerun. Same-state myopic/greedy decisions and their actual review orders still matched throughout. Saved traces replay exactly, but exact regenerated GPU actions are not guaranteed by the evidence. See the [reproducibility record](../artifacts/stage3_competition/identical_request_variation.json). A held-out replication of the unchanged condition is the next useful step; these diagnostic outputs should not be used to choose favorable scenarios.
