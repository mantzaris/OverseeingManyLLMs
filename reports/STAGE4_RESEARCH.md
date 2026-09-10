# Stage 4 research: planning, prediction, capacity, and objective choice

The complete frozen evaluation finished: **2,752/2,752 episodes**, plus **304/304 development episodes**, all replayed. The session used **48,320 GPU generations / 48,320 attempts**, with **zero retries, failed attempts, incomplete episodes, or unknown token counts**. No further inference was launched. The original Stage 1–3 findings and 1,460 checked historical files remain preserved.

Planning helped under some conditions, not uniformly. At two-tick reviews, search reduced mean competition-workload loss from greedy's 3.000 to 1.688 (paired difference −1.3125, 95% interval [−2.2500, −0.4375]), while the original-workload difference was −0.09375 [−0.5625, 0.34375]. Search and EDF both achieved zero loss in the one-tick competition condition. In the larger six-agent workload, search beat greedy strongly at one tick but nearly tied it at two. Better risk prediction did not consistently improve allocation. The selected count-penalty extension reduced incorrect closures at one tick while increasing original weighted cost.

This is evidence about one LLM in controlled civilian synthetic maintenance with simulated supervision. It does not measure human performance, establish general alignment, or introduce exhaustive scheduling as a new algorithm. The [research draft](../paper/RESEARCH_DRAFT.md), [claim–evidence map](../paper/CLAIM_EVIDENCE.md), and [verified related-work note](../paper/RELATED_WORK.md) state the bounded contribution.

## Frozen evaluation results

Each replication condition has 64 paired scenarios and 384 jobs. `delay` is queue-order search; `greedy` is delay-aware greedy. Loss includes continuing downtime and terminal incorrect-closure penalties. A missed opportunity means an initially useful request expired while waiting; it does not necessarily mean its action was wrong. Initial infeasibility and zero-value requests are counted separately in the saved tables.

| Workload | Review ticks | Policy | Mean loss | Correct / jobs | Corrections | Utilization | Missed opportunities |
| --- | --- | --- | --- | --- | --- | --- | --- |
| competition | 1 | delay | 0.000 | 384 / 384 | 96 | 0.500 | 0 |
| competition | 1 | edf | 0.000 | 384 / 384 | 97 | 0.500 | 0 |
| competition | 1 | fcfs | 1.250 | 375 / 384 | 84 | 0.445 | 42 |
| competition | 1 | greedy | 0.375 | 378 / 384 | 90 | 0.458 | 32 |
| competition | 1 | myopic | 0.375 | 378 / 384 | 92 | 0.458 | 32 |
| competition | 1 | uncertainty | 1.688 | 372 / 384 | 81 | 0.440 | 46 |
| competition | 2 | delay | 1.688 | 357 / 384 | 71 | 0.667 | 128 |
| competition | 2 | edf | 4.250 | 351 / 384 | 62 | 0.667 | 128 |
| competition | 2 | fcfs | 4.438 | 350 / 384 | 61 | 0.667 | 128 |
| competition | 2 | greedy | 3.000 | 352 / 384 | 64 | 0.667 | 128 |
| competition | 2 | myopic | 3.000 | 352 / 384 | 63 | 0.667 | 128 |
| competition | 2 | uncertainty | 4.125 | 352 / 384 | 61 | 0.667 | 128 |
| original | 1 | delay | 2.906 | 351 / 384 | 74 | 0.352 | 21 |
| original | 1 | edf | 2.969 | 353 / 384 | 76 | 0.359 | 15 |
| original | 1 | fcfs | 3.312 | 349 / 384 | 70 | 0.327 | 40 |
| original | 1 | greedy | 3.672 | 343 / 384 | 64 | 0.305 | 57 |
| original | 1 | myopic | 3.375 | 345 / 384 | 64 | 0.312 | 51 |
| original | 1 | uncertainty | 3.281 | 351 / 384 | 71 | 0.329 | 38 |
| original | 2 | delay | 7.328 | 322 / 384 | 43 | 0.406 | 27 |
| original | 2 | edf | 7.656 | 320 / 384 | 41 | 0.406 | 27 |
| original | 2 | fcfs | 7.875 | 319 / 384 | 40 | 0.396 | 31 |
| original | 2 | greedy | 7.422 | 320 / 384 | 39 | 0.391 | 33 |
| original | 2 | myopic | 7.406 | 320 / 384 | 40 | 0.393 | 32 |
| original | 2 | uncertainty | 7.531 | 321 / 384 | 42 | 0.401 | 29 |

The primary comparison is search minus greedy at two ticks, separately by workload. Intervals are 95% scenario-paired percentile bootstrap intervals (2,000 resamples, seed 20260910); additional comparisons are secondary and are not adjusted for multiplicity.

| Workload | Ticks | Comparator | Search − comparator | 95% paired interval | Search W/T/L | Different review orders |
| --- | --- | --- | --- | --- | --- | --- |
| competition | 1 | edf | 0.000 | [0.000, 0.000] | 0/64/0 | 62 / 64 |
| competition | 1 | greedy | -0.375 | [-0.688, -0.125] | 6/58/0 | 62 / 64 |
| competition | 2 | edf | -2.562 | [-4.000, -1.312] | 19/37/8 | 57 / 64 |
| competition | 2 | greedy | -1.312 | [-2.250, -0.438] | 15/42/7 | 53 / 64 |
| original | 1 | edf | -0.062 | [-0.203, 0.047] | 3/59/2 | 17 / 64 |
| original | 1 | greedy | -0.766 | [-1.516, -0.125] | 10/46/8 | 37 / 64 |
| original | 2 | edf | -0.328 | [-0.797, 0.000] | 3/61/0 | 5 / 64 |
| original | 2 | greedy | -0.094 | [-0.562, 0.344] | 3/59/2 | 9 / 64 |

Search's competition advantage at two ticks totals **84 loss units** versus greedy and **164** versus EDF. It wins/ties/loses against greedy in 15/42/7 scenarios, so the aggregate improvement is not universal. Unlike Stage 3's smaller development sample, it also closes five more jobs correctly than greedy here; Stage 3's opposite count result is retained and not rewritten. Myopic and delay-aware greedy have identical same-state rankings in the terminal-only workload; differences in their initial-error and correction counts reflect fresh trajectories.

The original two-tick workload supplies little useful competition: on search trajectories, only **32/156** dispatch opportunities have at least two eligible requests. Of 384 requests, 144 are already infeasible under the positive-benefit completion guard, 57 have zero original value, and 27 lose an initially useful opportunity while waiting (nine initially wrong). Low overall utilization does not imply those deadline-bound requests could have been rescued. Search/greedy orders differ in only 9/64 scenarios. In competition at two ticks, **224/256** search dispatches are competitive, search and greedy disagree on 72 of those same saved public states, and their actual sequences differ in 53/64 scenarios. All policies complete 256 reviews and miss 128 initially useful requests; search changes which costs are left exposed. Search leaves 27 wrong closures, each at penalty four, totaling 108.

At one tick, search and EDF can serve every competition request by its deadline. Their actual sequences differ in 62/64 scenarios despite identical zero loss. This distinguishes different scheduling decisions from a demonstrated reduction in realized loss.

![Policy losses](../artifacts/stage4_research/summaries/evaluation/figures/policy_losses.png)

[Full condition outcomes](../artifacts/stage4_research/summaries/evaluation/policy_outcomes.csv), [paired comparisons](../artifacts/stage4_research/summaries/evaluation/paired_comparisons.csv), [scenario differences and action/prompt diagnostics](../artifacts/stage4_research/summaries/evaluation/paired_scenarios.csv).

## Capacity and the larger workload

There are 32 nested scenarios per condition: 288 jobs for three agents and 576 for six. Loss per job separates added task volume from increased contention.

| Agents | Ticks | Policy | Mean loss | Loss / job | Incorrect / jobs | Corrections | Utilization |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 1 | delay | 5.656 | 0.628 | 11 / 288 | 81 | 0.345 |
| 3 | 1 | edf | 6.562 | 0.729 | 7 / 288 | 83 | 0.352 |
| 3 | 1 | fcfs | 6.812 | 0.757 | 12 / 288 | 80 | 0.337 |
| 3 | 1 | greedy | 6.219 | 0.691 | 15 / 288 | 75 | 0.323 |
| 3 | 2 | delay | 14.906 | 1.656 | 32 / 288 | 59 | 0.510 |
| 3 | 2 | edf | 15.469 | 1.719 | 27 / 288 | 61 | 0.542 |
| 3 | 2 | fcfs | 16.188 | 1.799 | 36 / 288 | 56 | 0.484 |
| 3 | 2 | greedy | 14.625 | 1.625 | 37 / 288 | 56 | 0.451 |
| 6 | 1 | delay | 16.188 | 0.899 | 34 / 576 | 139 | 0.594 |
| 6 | 1 | edf | 23.688 | 1.316 | 22 / 576 | 150 | 0.652 |
| 6 | 1 | fcfs | 24.000 | 1.333 | 52 / 576 | 120 | 0.534 |
| 6 | 1 | greedy | 22.375 | 1.243 | 67 / 576 | 108 | 0.487 |
| 6 | 2 | delay | 36.562 | 2.031 | 92 / 576 | 78 | 0.680 |
| 6 | 2 | edf | 46.000 | 2.556 | 92 / 576 | 83 | 0.706 |
| 6 | 2 | fcfs | 41.406 | 2.300 | 95 / 576 | 74 | 0.654 |
| 6 | 2 | greedy | 36.781 | 2.043 | 100 / 576 | 73 | 0.625 |

With six agents and one-tick reviews, search minus greedy mean loss is **−6.1875 [−9.3758, −3.2813]**, with 23/5/4 scenario wins/ties/losses. At two ticks it is **−0.21875 [−2.3133, 1.9695]**, with 11/12/9. The three-agent, two-tick comparison is slightly unfavorable to search: **+0.28125 [−1.4375, 1.8750]**. More demanding supervision therefore does not monotonically increase search's advantage over greedy.

On six-agent search trajectories, competitive dispatches rise to 353/456 at one tick and remain 185/261 at two. Two ticks produce 241 missed originally useful opportunities, 72 of them initially wrong, plus 35 initial infeasibilities and 39 zero-value requests. Search and greedy differ on 173/456 same public states at one tick and 56/261 at two; actual review sequences differ in 32/32 and 29/32 scenarios. More sequence differences alone do not imply a larger loss benefit.

EDF highlights the objective tradeoff. At one tick, six-agent search has mean loss 16.1875 versus EDF 23.6875, but **34 versus 22 incorrect closures**. Six of 32 scenarios show lower search cost with more incorrect closures. At two ticks their incorrect counts tie at 92, while search's mean loss is 9.4375 lower [−14.7516, −5.0625].

Per-agent outcomes are retained, not averaged away. In six-agent, one-tick search, incorrect closures for agent IDs 0–5 total **[1, 6, 11, 4, 4, 8]**, versus EDF **[0, 3, 4, 3, 6, 6]**. Search's mean per-agent losses range from 2.0313 to 3.4063; its largest single agent/scenario loss is 15, versus EDF's 28. At two ticks, search's per-agent incorrect counts are [9, 15, 23, 15, 14, 16], and its largest single agent/scenario loss is 42. These finite-sample distributions and deterministic ID tie rules provide no fairness guarantee. [All per-agent means, 90th percentiles and maxima](../artifacts/stage4_research/summaries/evaluation/per_agent_summary.csv), [individual agent/scenario rows](../artifacts/stage4_research/batches/evaluation/analysis/per_agent.csv).

![Capacity effects](../artifacts/stage4_research/summaries/evaluation/figures/capacity.png)

## Prediction quality versus actual allocation

The frozen estimator underpredicts errors across the new distributions. The following rows describe search's **full core, two-tick trajectories**. Each alternative Brier score is computed on those same saved labels; these rows are not risk-specific rollout comparisons.

| Workload | Agents | Agree errors / examples | Disagree errors / examples | Overall initial error | Mean frozen risk | Brier frozen / pooled / analytical |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Original | 3 | 90 / 350 | 15 / 34 | 0.2734 | 0.1494 | 0.21305 / 0.20673 / 0.15707 |
| Competition | 3 | 84 / 353 | 14 / 31 | 0.2552 | 0.1491 | 0.20025 / 0.19519 / 0.16352 |
| Larger | 3 | 80 / 271 | 11 / 17 | 0.3160 | 0.1483 | 0.24286 / 0.23364 / 0.19640 |
| Larger | 6 | 152 / 543 | 18 / 33 | 0.2951 | 0.1482 | 0.22861 / 0.22046 / 0.17500 |

[Every policy/duration/risk condition's bin counts and Brier scores](../artifacts/stage4_research/summaries/evaluation/tables/prediction_diagnostics.md), [pointwise reliability summaries](../artifacts/stage4_research/summaries/evaluation/reliability.csv), and [prediction records](../artifacts/stage4_research/batches/evaluation/analysis/predictions.csv) retain sparse bins and initial labels. No evaluation label updates the estimator.

The fresh ablation uses the matching first 32 replication seeds. At two ticks, original search mean loss is **7.625 frozen, 7.875 pooled, 7.500 analytical**; competition search is **1.625, 1.625, 1.500**. Analytical-minus-frozen search differences are −0.125 [−0.5625, 0.1250] in original and −0.125 [−0.7500, 0.6250] in competition. Original greedy instead changes from 7.5625 to 7.8125 under analytical risk; competition greedy changes from 3.250 to 2.875. All three estimates tie at zero for competition search at one tick. A small secondary original one-tick search improvement is −0.250 [−0.5320, −0.0313]. Thus improved prediction scores do not establish a consistent allocation improvement.

The analytical reference changes the hypothetical search head on only 4/156 original and 8/256 competition full-core two-tick search states. Eligibility and cost/deadline structure limit where different risk rankings can matter. Pooled risk carries no within-queue ranking information when frozen risks already coincide. In the complete exact-rational numerical audit, uniform scaling changes 111 hypothetical search heads among 15,727 uniform-risk states, but every changed head is exactly co-optimal. These numerical tie changes must not be interpreted as better uncertainty discrimination.

![Risk estimates](../artifacts/stage4_research/summaries/evaluation/figures/risk_estimates.png)

[Matched rollout table](../artifacts/stage4_research/summaries/evaluation/tables/risk_rollouts.md) includes both durations and policies. No analytical-risk rollout was added to the larger workload; its alternative prediction scores above are offline diagnostics only.

## Selected extension: cost versus incorrect closures

The extension uses 16 new scenarios per distribution, separate from core evaluation, and one fixed λ grid. All rows retain original maintenance loss and incorrect-job count; columns L+4U and L+8U evaluate the same objective across all settings.

| Workload | Ticks | λ | Mean original loss | Mean incorrect | Mean L+4U | Mean L+8U |
| --- | --- | --- | --- | --- | --- | --- |
| competition | 1 | 0 | 0.000 | 0.000 | 0.000 | 0.000 |
| competition | 1 | 4 | 0.000 | 0.000 | 0.000 | 0.000 |
| competition | 1 | 8 | 0.000 | 0.000 | 0.000 | 0.000 |
| competition | 2 | 0 | 1.750 | 0.438 | 3.500 | 5.250 |
| competition | 2 | 4 | 1.750 | 0.438 | 3.500 | 5.250 |
| competition | 2 | 8 | 1.750 | 0.438 | 3.500 | 5.250 |
| larger | 1 | 0 | 13.312 | 1.062 | 17.562 | 21.812 |
| larger | 1 | 4 | 14.500 | 0.438 | 16.250 | 18.000 |
| larger | 1 | 8 | 15.062 | 0.312 | 16.312 | 17.562 |
| larger | 2 | 0 | 31.375 | 3.062 | 43.625 | 55.875 |
| larger | 2 | 4 | 32.062 | 2.938 | 43.812 | 55.562 |
| larger | 2 | 8 | 32.938 | 2.938 | 44.688 | 56.438 |

In the larger one-tick condition, λ=8 versus λ=0 raises mean original loss by **1.750 [0.1875, 3.4375]** and reduces incorrect closures by **0.750 [0.375, 1.125]** per scenario. Total wrong closures fall from 17 to five while cost rises from 213 to 241. The common L+8U objective improves by −4.250 [−7.625, −1.000], whereas the L+4U difference is −1.250 [−3.4375, 0.8766]. This supports an objective-dependent tradeoff, not universal improvement. Per-agent wrong closures change from [5, 3, 2, 1, 4, 2] to [3, 1, 1, 0, 0, 0]; several agents incur more original loss despite fewer wrong closures.

At two ticks, λ=8 reduces only two wrong closures across all 16 scenarios and increases original cost by 25. The paired incorrect-count interval includes zero, and even common L+8U is slightly worse (+0.5625). The extension is therefore not uniformly helpful as review capacity falls.

Competition is a structural null control: all λ settings have identical actual review orders and losses at both durations. An exact public-arithmetic audit checks 288 possible wave configurations × two durations × three λ values. With one-tick reviews, all three jobs can be served; with two ticks, every exact-optimal plan serves the cost-eight and cost-twelve jobs throughout the frozen-risk/λ grid. The count penalty cannot change that useful served set. This explains a null result without modifying the declared batch. [Arithmetic audit](../artifacts/stage4_research/numerical_audits/objective_structural_null.json).

![Objective tradeoff](../artifacts/stage4_research/summaries/evaluation/figures/objective_tradeoff.png)

## Planning cost, variation, and readable examples

The live workload reached six outstanding and six eligible requests. The planner examined all 1,957 ordered subsets on each six-eligible decision. It never truncated a queue or substituted a heuristic.

| Eligible requests | Decisions | Mean ms | 95th percentile ms | Max ms | Ordered subsets |
| --- | --- | --- | --- | --- | --- |
| 0 | 5848 | 0.006 | 0.010 | 0.060 | 1 |
| 1 | 1707 | 0.020 | 0.028 | 0.920 | 2 |
| 2 | 1465 | 0.028 | 0.039 | 0.165 | 5 |
| 3 | 1180 | 0.054 | 0.077 | 0.229 | 16 |
| 4 | 325 | 0.156 | 0.217 | 0.518 | 65 |
| 5 | 246 | 0.756 | 1.064 | 1.221 | 326 |
| 6 | 22 | 4.531 | 6.861 | 6.881 | 1957 |

These timings measure the actual scheduler call on the pod, separate from inference and simulated time. Six-request search averaged 4.531 ms over 22 decisions, with a 6.881 ms maximum. This supports the declared small-queue implementation, not large-queue scalability. [Detailed effort table](../artifacts/stage4_research/summaries/evaluation/planning_effort.csv).

Across the full session, **38 of 7,276 repeated full-request hash groups** contain differing actions, with 38 minority-action occurrences. Evaluation accounts for 33 mixed groups among 6,308 repeated groups, touching 172 episodes. All mixed groups concern first samples. No requests were repeated to obtain a preferred action. Equal request seeds are therefore not a bitwise reproducibility guarantee.

The primary original and competition search/greedy comparisons have no differing first actions under identical full requests. They do have respectively two and six scenario pairs with differing first actions under changed histories. In competition, the 58 pairs whose first actions match contribute −76 of the aggregate −84 loss difference; this descriptive decomposition is not a new causal estimate or a reason to discard the other six pairs. In the larger two-tick search/greedy comparison, five first-action differences occur despite identical full requests, alongside a small total loss difference of −7. Generation sensitivity matters especially for interpreting such small effects. Saved-output replay remains deterministic in every case.

The declared first-seed selection rule yields both positive and negative examples without filtering by matching model actions:

| Workload, two ticks | First search win | First search loss |
| --- | --- | --- |
| Original | [10022: ΔL=−2](../artifacts/stage4_research/summaries/evaluation/traces/original_positive.md) | [10000: ΔL=+6](../artifacts/stage4_research/summaries/evaluation/traces/original_negative.md) |
| Competition | [11000: ΔL=−4](../artifacts/stage4_research/summaries/evaluation/traces/competition_positive.md) | [11021: ΔL=+4](../artifacts/stage4_research/summaries/evaluation/traces/competition_negative.md) |
| Larger, six agents | [12001: ΔL=−2](../artifacts/stage4_research/summaries/evaluation/traces/larger_positive.md) | [12006: ΔL=+4](../artifacts/stage4_research/summaries/evaluation/traces/larger_negative.md) |

All six selected core pairs happen to have identical first actions; observations can still differ. In competition seed 11000, search reviews the cost-eight request before its tick-two deadline, then the cost-twelve request; greedy reviews cost twelve first and misses cost eight. The missed wrong job costs four under search and eight under greedy. In original seed 10000, search protects an urgent but already correct request before a costly wrong job, delaying the latter's correction by two ticks and adding six downtime units. The frozen risks do not identify that realized mistake. These traces distinguish useful planning from realized over-allocation to a correct job.

The first objective tradeoff example is [larger seed 13011, one tick](../artifacts/stage4_research/summaries/evaluation/traces/larger_s1_objective.md): λ=8 has zero incorrect closures and loss 16, versus one and loss nine at λ=0. It additionally reviews a zero-original-cost wrong job, but also changes later histories: six observations and one first action differ. Its cost change is an integrated trajectory effect, not an isolated fixed-action scheduling effect. No qualifying λ=8 lower-count/higher-cost example exists for competition or larger two-tick reviews. [Selection record](../artifacts/stage4_research/summaries/evaluation/traces/selection.json).

The exact-rational audit of all **34,660 saved evaluation public states** finds **zero positive expected-value regret** for the selected floating search heads, with 58 differences from canonical exact tie preference. This checks each chosen head against the best plan beginning with it; it does not prove full-horizon optimality or deterministic floating tie behavior. [Numerical audit](../artifacts/stage4_research/numerical_audits/evaluation_summary.json).

## Declaration, budget, and development decisions

The stage started at 2026-09-10 03:48:53 UTC. Its separately authorized nine-hour deadline is 12:48:53 UTC; inference stops at 11:18:53 UTC to reserve the final 90 minutes for reporting. Historical clocks and historical command limits remain unchanged. A single append-only ledger enforces 50,000 scheduled calls and 60,000 actual generation attempts, with at most one retry per ordinary call. The original 36-hour target begins at 2026-09-09 15:38:57 UTC. Final elapsed and cumulative accounting are recorded below and in `reports/implementation_clock.json`.

The fixed diagnostic used 32 deterministically selected historical request hashes (the two previously mixed groups, then 30 unique hashes in lexical order), repeated four times each. All 128 calls succeeded without retries; none of these four-repeat sets mixed actions. This finite result does not establish deterministic regeneration. Integrated rollouts again showed variation, retained and quantified below.

Offline rescoring reused 232 historical development episodes / 1,392 jobs without new inference. Original Stage 2 validation Brier scores were 0.138521 frozen, 0.139178 pooled, and 0.146396 analytical. Stage 3 competition scores were 0.212629, 0.206178, and 0.159686. These are prediction diagnostics on saved trajectories; they did not substitute for fresh estimator-specific rollouts.

The core pilot used seeds 400–407 for original/competition risk comparisons and 408–411 for the larger workload: 256 episodes / 4,032 calls, approximately the authorized 4,000-call development allowance. The fixed objective pilot used seeds 412–415: 48 episodes / 1,152 calls. All 304 episodes completed and replayed without failed generation attempts. No additional calibration, placement generation, seed replacement, or stabilization rerun was made.

Branch A was selected because the larger six-agent, one-tick pilot repeatedly exposed the cost/count tradeoff: search totaled loss 63 with 67 correct jobs, versus EDF loss 95 with 69; two of four scenarios had lower cost but more incorrect closures. Stage 3 had already shown this concern at two ticks. One fixed λ=0/4/8 pilot iteration then produced mostly ties or slight cost increases; the grid was retained, without a second iteration. No imperfect-supervision or sampling-replicate branch was added.

The evaluation freeze at 04:29:16.884231 UTC selected every full user-target core prefix, plus 16 objective-extension seeds per distribution. Its declaration hash is `3f6c6d664639ca25a6c2c4085bae734fe8b56a64c3a020b92c98c5ca79ecea0d`. The forecast used 1.5 times measured p95 end-to-end episode seconds/call, plus 30 minutes contingency, predicting completion at 09:20 UTC before the inference cutoff. No evaluation outcomes were inspected to choose methods or sample sizes. Policy order rotates, duration order is balanced, and model sampling seeds exclude policy, estimator, duration, objective and execution order. Every condition uses fresh calls and its own histories.

| Study | Seeds and conditions | Episodes | Scheduled calls |
| --- | --- | ---: | ---: |
| Core development | 400–411; risk and capacity pilots | 256 | 4,032 |
| Objective development | 412–415; competition a3/larger a6, search, λ=0/4/8, s=1/2 | 48 | 1,152 |
| Replication | Original 10000–10063, competition 11000–11063; six policies, s=1/2 | 1,536 | 18,432 |
| Risk ablation | First 32 replication seeds; greedy/search, pooled/analytical, s=1/2 | 512 | 6,144 |
| Capacity | 12000–12031; three/six agents, four policies, s=1/2 | 512 | 13,824 |
| Objective evaluation | 13000–13015; competition a3/larger a6, search, λ=0/4/8, s=1/2 | 192 | 4,608 |
| Separate repeated-request diagnostic | 32 hashes × four repetitions | — | 128 |
| Total | Development and evaluation remain separate | 3,056 | 48,320 |

The 2,752 evaluation episodes represent paired scenario sets, not 2,752 independent scenarios. The objective extension uses a distinct seed cohort and is not pooled with the core λ=0 rows. The risk ablation reuses only the matching first 32 frozen-estimator rows, not the full 64-scenario replication mean. Primary contrasts are search minus greedy loss at two ticks, separately original and competition; EDF is prominent. Bootstrap intervals use 2,000 scenario-paired resamples and seed 20260910, without multiplicity adjustment.

## Implementation and concrete validity repairs

The original and competition generators remain unchanged. The new larger workload uses three or six agents, three jobs each, 24 ticks, releases at 0/8/16 plus independent jitter 0/1, deadline windows 2/4/6, downtime rates 0/1/3, and terminal penalties 0/4/8/12. Independent component streams separate public costs and arrivals from hidden faults. Stable per-agent/job streams nest the first three agents across team sizes. Every wave closes before the next release. Schedulers receive only released public requests; no future-arrival lookahead is used.

The exact Stage 2 estimator is preserved: agreement 13/89, disagreement pooled fallback 18/98, canonical hash `54d9a97e25f5cb22cf0df216293303ea5c945713032c6bc1282c55fcf327e085`. The pooled alternative uses 18/98 everywhere. The analytical reference knows the uniform fault prior and independent clue accuracies 0.8/0.6, but never reads the realized fault: following agreeing clues gives error probability 1/7, following the stronger conflicting clue 3/11, and complementary actions 6/7 or 8/11. Both samples remain in all conditions. Labels concern the first action before correction; no estimator is refitted.

The λ extension adds an incorrect-closure penalty consistently to eligibility and expected intervention benefit. Original maintenance loss L and incorrect closures U remain separate outcomes. Common objectives L, L+4U and L+8U are compared across every λ setting; unlike own-objective scores are not used to claim superiority.

A concrete numerical defect was repaired before expanded inference: sequential floating addition could give mathematically equal review orders different values. Stage 4 search uses `math.fsum` while preserving historical code and source snapshots. A same-state audit of 1,920 historical Stage 3 dispatches changes 42 hypothetical search heads, all at one tick, none at two. This is not a historical trajectory rerun. Floating products still allow alternative resolutions of exact rational ties, so a separate exact-rational head-value audit accompanies the results. Queues are checked at six and never truncated; six eligible requests require all 1,957 ordered subsets including empty.

One non-generation GPU evidence check failed after the initial pilot: a tail-only server-log selection dropped the original CUDA/BF16 startup anchors. Its failed record is preserved. A separately timestamped check verified the same server and serving GPU process, and the validator now retains startup anchors. This was not a failed inference call. All subsequent placement checks passed.

Reporting checks prevent accidental pooling of core and extension cohorts and reject duplicate scenario rows. A narrowly scoped historical CSV audit permits Git's configured CRLF-to-LF normalization while still rejecting changed values; raw evidence, estimator and source hashes remain strict. The 1,460 historical files retain their original contents.

The initial 33 focused checks and Stage 1–3 audits passed once at foundation. The full pre-freeze suite passed 42 checks; the later focused reporting and portability suite passed ten checks. New checks cover public/private boundaries, analytical complementary-action cases, stable nested workload streams, queue bounds, complete enumeration, λ eligibility, compressed replay, deadline/ledger limits and cohort separation. No broad framework rewrite was made.

## Runtime, accounting, and final status

Stage 4 reused the authenticated `root@38.80.152.248:33513` connection, the existing `/workspace/OverseeingManyLLMs-rtx6000-ada-20260910T002404Z` checkout, its isolated environment and cached weights. No private key was displayed or transferred, no environment reinstallation was needed, and no serving process was restarted.

| Runtime item | Verified value |
| --- | --- |
| Model / revision | Qwen/Qwen2.5-7B-Instruct / `a09a35458c702b33eeacc393d103063234e8bc28` |
| GPU | NVIDIA RTX 6000 Ada Generation; 49,140 MiB; compute capability 8.9 |
| Python / serving | Python 3.11.13; vLLM 0.10.2; Transformers 4.55.2 |
| Torch / installed CUDA runtime | Torch 2.8.0+cu128; CUDA runtime 12.8; native BF16 verified |
| Driver | 580.126.20; `nvcc` was not on PATH, so no installed-toolkit version is inferred |
| Placement | BF16, tensor parallelism one, GPU memory reservation 0.5, CPU offload zero, swap zero |
| Serving limits | One concurrent sequence; context limit 2,048; eager mode; serial requests |
| Decoding | Temperature 0.3, top-p 1.0, max output 48 tokens, two-action guided JSON, n=1 |
| Attempts | Existing 60-second attempt timeout; at most one retry; zero actual retries |
| Observed input length | Maximum 292 tokens in evaluation; no truncation needed |
| Host analysis | Python 3.8.10; NumPy 1.22.1; Matplotlib 3.1.2 |

The placement evidence combines actual CUDA BF16 matrix execution, server model/revision and dtype flags, zero-offload/swap settings, startup loading logs, the serving GPU process and allocation, successful raw generations, and server counter/token deltas. A small CUDA probe alone would not prove model placement; the combined serving evidence is retained in each batch. All LLM inference ran through this GPU service. Host tokenization, orchestration, scheduling, scoring and analysis were ordinary CPU work.

| Accounting item | Actual |
| --- | ---: |
| Development episodes completed / replayed | 304 / 304 |
| Evaluation episodes completed / replayed | 2,752 / 2,752 |
| Scheduled experimental generations | 48,192 |
| Separate diagnostic generations | 128 |
| Separate placement generations | 0 |
| Total scheduled / attempted / successful generations | 48,320 / 48,320 / 48,320 |
| Retries / failed attempts / incomplete episodes | 0 / 0 / 0 |
| Prompt / completion tokens | 10,738,298 / 338,408 |
| Total tokens | 11,076,706 |
| Unknown-token or unfinished attempts | 0 |
| Remaining scheduled-call allowance | 1,680 (unused) |
| Sum of bounded worker wall times | 10,101.935 seconds (2 h 48 m 21.9 s) |
| Evaluation worker wall time | 8,969.695 seconds (2 h 29 m 29.7 s) |
| First / final server generation counter | 3,027 / 51,347 |

The evaluation worker finished at **2026-09-10 07:00:35.506830 UTC**, over four hours before the inference cutoff. The sum of worker times includes diagnostics, pilots, evaluation, their runtime evidence checks and worker overhead; it is not the full session clock. Setup, waits, analysis, reporting and commits are included in the separately recorded session elapsed clock. Detailed durations are in `launches/*/launch.json`; the append-only [ledger](../artifacts/stage4_research/ledger.jsonl) and [reconciled accounting](../artifacts/stage4_research/session_accounting.json) preserve every call and attempt.

At final runtime inspection (07:00:47.880102 UTC), **no experimental workers remained**, no server requests were running or waiting, `/health` returned 200, and the same server PID 7338 / engine PID 8449 remained alive. The engine held 24,618 MiB, total GPU use was 24,628 MiB, utilization was zero, and `/workspace` had approximately 47 GiB free. Pod, cached model, persistent files, Jupyter and existing services were preserved. [Final status](../artifacts/stage4_research/runtime_final.json), [final GPU evidence](../artifacts/stage4_research/batches/evaluation/gpu_final.json), [environment packages](../artifacts/stage4_research/batches/evaluation/requirements.actual.txt), [telemetry](../artifacts/stage4_research/launches/evaluation/gpu_telemetry.csv). Provider billing/allocation balances were not exposed by this runtime inspection, so no dollar cost is invented.

All 3,056 completed traces replay, all planned rows are retained, and session reservations match raw attempt records with no gaps. The final audit also verifies the estimator, source snapshots, request seeds/settings, observation boundary, serial execution, GPU metrics and all 1,460 historical file hashes. The transferred archive's SHA256 and preservation of the earlier ledger prefix are recorded separately. [Evaluation audit](../artifacts/stage4_research/batches/evaluation/analysis/audit.json), [session audit](../artifacts/stage4_research/session_accounting.json), [transfer verification](../artifacts/stage4_research/transfer_verification.json).

## Reproduction and research package

The [verified reproduction guide](../artifacts/stage4_research/REPRODUCE.md) records exact setup references, declarations, bounded server-side execution commands, and offline reproduction. Source snapshots remain under each batch's `source/`; final analysis includes explicitly documented reporting fixes without altering the frozen inference implementation. Raw request/response and event files are losslessly compressed; compression was checked before plain copies were removed. No raw experimental evidence was discarded.

From the repository root, reproduce saved evaluation results without inference:

```bash
python3 scripts/analyze_research.py --batches evaluation --label evaluation
python3 scripts/audit_numerical_ties.py --batches evaluation --label evaluation
python3 scripts/audit_objective_null.py
python3 scripts/plot_research.py
python3 scripts/research_traces.py
python3 scripts/research_tables.py
python3 scripts/audit_research_session.py
python3 -m overseeing replay artifacts/stage4_research/batches/evaluation/episodes/replication/original/10000/a3/s2/frozen/delay/lambda0/events.jsonl.gz
```

The four figures are also saved as PDF and SVG for publication. Every table links back to per-episode data and raw traces. The [experiment register](../artifacts/stage4_research/EXPERIMENT_REGISTER.md), [initial plan](../artifacts/stage4_research/RESEARCH_PLAN.md), [evaluation freeze](../artifacts/stage4_research/evaluation_freeze.json), and [append-only decisions](../artifacts/stage4_research/decisions.jsonl) preserve adaptation provenance. Historical Stage 2 and Stage 3 negative findings are separate from these new distributions and seeds.

The strongest supported contribution is an auditable LLM supervision experiment showing that **the value of review-order planning depends on deadline structure and capacity, while prediction quality and correct-job count do not reduce to weighted-loss performance**. The framework makes the public/private boundary, feedback histories, simulated clock, uncertainty assumptions and objective tradeoffs inspectable. The related-work note compares this scope with KnowNo, constrained cost-sensitive deferral, and established scheduling literature; it makes no novelty claim for enumeration or scalar penalties.

Limitations remain substantial: one model and revision; binary synthetic faults; deliberately constructed workloads; perfect completed reviews; immediate compliance; automatic request admission; a small historical calibration sample; only six-request exact search; no future-arrival planning; and no real humans or equipment. Bootstrap intervals use scenarios as the unit but do not separate generation variance from scenario variance. Analytical risk knows the generating likelihoods. Secondary comparisons are exploratory and not multiplicity-adjusted. No method was redesigned using evaluation outcomes.

The single next useful step is a **predeclared generation-replicate study on fresh scenario seeds**, pairing greedy, EDF and search within each replicate, to quantify whether the small original/two-tick-larger differences and objective tradeoffs persist across generation variation. Keep the present methods frozen for that study. No such follow-up was launched in this session.

## Session clock and commits

At the final report checkpoint **2026-09-10T07:18:52.046563+00:00**, Stage 4 elapsed time is **12599.047 seconds (3.500 hours)**, including setup, waits, inference, repairs, analysis and documentation. Cumulative calendar elapsed time since the original start is **15.665 hours of the 36-hour target**, with **zero overrun** and **20.335 hours remaining**. Historical timestamps remain unchanged. The final commit’s actual committer timestamp is the finish marker for the immediately following Git verification and commit; no record is backdated.

Milestones on `main`: `e2b7cb9069d1d5f5f475f2b2672cf2e71ceebdca` (foundation and pilot declaration), `3e1dc0039f0f08a38e44d3333d3fd0a59ad6713a` (full evaluation freeze), and `c8f9983fdb162a94087f17236fc6f6b78afddadd` (cohort-safe analysis and methods draft), followed by the final research-package commit. No push is performed. Keys, credentials, weights, environments and caches are excluded.
