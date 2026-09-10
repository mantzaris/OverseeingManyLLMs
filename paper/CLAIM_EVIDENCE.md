# Claim–evidence map

Working map prepared before evaluation analysis. Measured result claims will be filled only after complete saved-evidence audits. Paths are relative to repository root; CSV conditions below are explicit filters.

| Proposed claim | Exact supporting evidence | Scope / exclusions |
| --- | --- | --- |
| Actual model calls execute through the pinned BF16 GPU service, with zero configured offloading | `artifacts/stage4_research/batches/*/gpu_before.json`, `gpu_final.json`, raw requests, server metric deltas; initial pilot also preserves failed tail-log check and successful `gpu_final_recheck.json` | One RTX 6000 Ada and one model revision. CUDA kernel evidence alone is not model placement evidence; command flags, model loading logs, serving GPU process and successful generation counters are also retained. |
| The study separates public scheduling inputs from hidden labels and future jobs | Source snapshots; `tests/test_research.py`; completed trace audits; `planning_decision.public_pending` and raw model observations | Hidden truth in scorer-only saved artifacts is used for offline verification. It is not a scheduler feature. |
| Evaluation conditions and scenario prefixes were frozen after development | `artifacts/stage4_research/evaluation_freeze.json`; `batches/evaluation/declaration.json`; commit `3e1dc0039f0f08a38e44d3333d3fd0a59ad6713a`; first execution timestamp | Controlled developmental design choices are separate from fresh evaluation labels. Constructed workloads remain constructed distributions. |
| Stage 4 uses the original Stage 2 estimator without refitting | `artifacts/stage4_research/estimator.json`, canonical estimator hash and byte hash in declarations/audits | Historical calibration is small; frozen does not mean calibrated on new conditions. |
| Exact six-request enumeration is bounded and measured | Focused test checks 1,957 ordered subsets; live `planning_decision` effort/latency records | Exact only for the current-queue estimate; no future-arrival oracle and no large-queue scalability claim. |
| Numerical tie handling changed before Stage 4 evaluation | `artifacts/stage4_research/offline_risk/search_summation_choices.csv` and summary; historical source retained | 42/1,920 saved Stage 3 state choices change, all s=1. Same-state choice audit is not a historical trajectory rerun. |
| Same seeds do not guarantee the same model action | Historical Stage 3 variation; Stage 4 diagnostics and integrated request-hash groups | The 128 fixed diagnostic repetitions alone had no mixed group; later observed variation is retained. Saved-output replay is deterministic. |

## Evaluation claims awaiting measured results

Use `artifacts/stage4_research/summaries/evaluation/paired_comparisons.csv` for scenario-paired intervals and wins/ties/losses. Primary filters are `kind=policy`, `primary=True`: original and competition, frozen risk, two ticks, search minus greedy. EDF comparisons are secondary and explicit. `policy_outcomes.csv` contains losses, correct jobs, corrections, utilization and missed opportunities by full condition. `paired_scenarios.csv` identifies losses and actual action/prompt differences for each scenario pair.

Risk claims require both `prediction_quality.csv` / `reliability.csv` and actual rollout outcomes. The three-estimator figure/table uses the matching first 32 seeds, recorded in `risk_matched_outcomes.csv`; the complete 64-seed frozen replication mean is not substituted for that prefix. Brier scores on alternative probabilities over the same outputs are prediction diagnostics, not counterfactual policy performance.

Capacity claims use only the larger distribution and explicitly distinguish aggregate loss from loss per job. Per-agent distributions come from `per_agent_summary.csv` and per-episode agent rows in `batches/evaluation/analysis/per_agent.csv`. Objective claims compare the same original loss and incorrect-closure metrics for λ=0,4,8, with common-objective contrasts in `paired_comparisons.csv`.

The positive/negative examples are explanatory, not selected effect estimates. Their deterministic first-seed rule and any tie fallback are recorded in `summaries/evaluation/traces/selection.json`.

## Claims deliberately excluded

- Novelty of exhaustive scheduling, cost-sensitive deferral, or scalarizing multiple objectives.
- Measured human benefit, attention, trust, fatigue, diagnostic accuracy, or workload.
- General alignment, robustness across LLMs, or effectiveness on real maintenance incidents.
- Full-horizon optimality, optimality under unknown future arrivals, or an exact Pareto frontier.
- Treating repeated policy runs, individual jobs, or repeated prompts as independent scenario samples.
- Inferring counterfactual scheduling gains from Brier improvements alone.
- Promising identical regenerated GPU actions from equal seeds.

Primary related-work references and their verified scope are in [RELATED_WORK.md](RELATED_WORK.md).
