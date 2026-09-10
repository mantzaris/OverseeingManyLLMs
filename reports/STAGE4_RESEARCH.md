# Stage 4 research session — development in progress

The nine-hour stage started **2026-09-10 03:48:53 UTC**, with a hard finish at **12:48:53 UTC** and inference cutoff **11:18:53 UTC**, reserving 90 minutes for reporting. Historical clocks and command limits remain unchanged. A single append-only ledger enforces 50,000 scheduled calls and 60,000 generation attempts. Every ordinary call permits at most one retry. [Authorization](../artifacts/stage4_research/authorization.json), [initial register](../artifacts/stage4_research/RESEARCH_PLAN.md), [decision log](../artifacts/stage4_research/decisions.jsonl).

This milestone contains the verified foundation and declarations; it is not the completed research report. No evaluation has begun and no optional branch has been selected.

## Foundation findings

All 33 existing focused checks and the Stage 1, 2, and 3 historical audits passed; all 1,460 historical evidence/configuration files checked by byte hash remain unchanged. The existing RTX 6000 Ada server is healthy and retained, with the pinned model, BF16, one GPU, and zero CPU offloading. Its initial counter was 3,027 generations.

The deterministic request-variation diagnostic selected the two historical mixed-output request groups followed by 30 other unique request hashes in lexical order, with four repetitions each. All **128/128** requests completed with one attempt each, no retries or failures, and no mixed-action group within these new four-repeat sets. This finite check does not establish deterministic GPU outputs or erase historical variation. [Declaration](../artifacts/stage4_research/diagnostics/declaration.json), [summary](../artifacts/stage4_research/diagnostics/summary.json).

Offline prediction rescoring on 232 saved development episodes (1,392 job pairs) gives:

| Workload | Frozen agreement Brier | Frozen pooled Brier | Analytical reference Brier |
| --- | ---: | ---: | ---: |
| Original Stage 2 validation | 0.138521 | 0.139178 | 0.146396 |
| Stage 3 competition | 0.212629 | 0.206178 | 0.159686 |

These repeated policy trajectories are not independent scenarios. The reference knows the synthetic prior and clue likelihoods, uses only public clues and the proposed action, and is never fitted to labels. Prediction rescoring is not counterfactual rollout evidence. [Per-trajectory summaries](../artifacts/stage4_research/offline_risk/prediction_summary.csv).

A numerical tie defect was identified before expansion: sequential floating-point addition sometimes gave mathematically equal review orders different values. Stage 4 exact search uses `math.fsum`; historical search code and results are preserved. The objective, eligibility, exhaustive enumeration, and deterministic tie rule remain the same. A six-request queue examines all **1,957 ordered subsets** including empty. The new workload has stable per-agent/job streams, three waves in 24 ticks, matching first-three-agent exogenous jobs in three/six-agent conditions, and a checked six-request outstanding bound.

All **39 focused checks** pass after the extensions, including analytical complementary-action cases, public/private independence, nested agent conditions, reporting reserve/ledger caps, stable search ties, full enumeration, history boundaries, and compressed evidence replay. [Checks](../artifacts/stage4_research/core_checks.txt).

The declared initial rollout pilot uses seeds 400–407 for risk comparisons and 408–411 for the larger workload: **256 episodes / 4,032 scheduled calls**. It will precede branch selection and evaluation freeze. [Pilot declaration](../artifacts/stage4_research/batches/development_pilot/declaration.json).
