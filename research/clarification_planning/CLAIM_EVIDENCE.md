# Claim and evidence map

Paths below are relative to `artifacts/clarification_planning/` unless noted. Paired differences are always planner minus comparator; negative loss favors the planner.

| Proposed claim | Exact evidence | Qualification |
|---|---|---|
| Complementary clarification need not have diminishing returns | `development_synthetic_corrected/`, `synthetic/` family `complementary`, B=2; `test_planner.py`; METHOD proof | Authored mechanism, not measured prevalence; Bellman/nonmyopic elicitation already established |
| Two-step selection improves loss over one-step at budget two on this adapter | `analysis/primary.json`: −0.239583, CI [−0.364583,−0.114583], 17/29/2 | 48 dialogues, two replicates averaged, simulated accurate answers and e=4,d=1; marginal interval |
| A practical advantage over semantic memory remains uncertain | Same file: −0.09375 [−0.21875,+0.010417], 6/40/2 | Planner asks 17 more answers and completes two fewer whole projects across preparations |
| A stronger completion rule undermines the broad planning claim | `completion_audit/episodes.csv`; `analysis/minimum_completion_paired.csv`; `analysis/primary_totals.csv` | Secondary audit after freeze, same saved preparations, not a new confirmatory sample |
| Minimum sufficient completion uses fewer answers with near-equal loss | Primary totals: 62 loss/135 answers vs 63/177; paired loss +0.010417 [−0.114583,+0.104167] | Wide interval is not proof of equivalence; extra wrong release for simple rule |
| Better interpretation is a strong competing explanation | `analysis/conditional_prediction_quality.csv`, `prediction_fields.csv`, `source_guard_counts.csv`; full-history rows | Memory covers 160/382 fields, history 379/382. All required values were already stated. Backend comparison differs from mechanism comparison |
| Objective weight changes the preferred strategy | `analysis/paired.csv`, B=2, full_history, e=2 and e=8 | Weight-specific secondary contrasts, dimensionless costs rather than financial or human utility measurements |
| Complementary requirements occur, but shared authority is unestablished | `analysis/structure_summary.json`, `source_task_structure.csv`, `data/audit.json` | 73/96 tasks multi-field; 70/192 generated tasks missing two values; zero annotated cross-task shared factors |
| Dependency ranking lacks empirical advantage over generic search here | `analysis/paired.csv`, generic2 at B=2 | Every empirical candidate set fits width8. The synthetic distractor gain is authored |
| Approximation has explicit limits | `synthetic/exact_reference.csv`, `analysis/pruning_summary.csv`, `analysis/pruning_witness.json` | Finite small checks match; separate width2 witness gap1.2. No optimality or submodular guarantee |
| Scope and version protocol properties are limited | `test_planner.py`, `test_desk.py`, `test_audits.py`, `safe_protocol.py`, SEMANTIC_AUDIT.md | Complete registered dependencies and represented scope only; no semantic-correctness guarantee |
| Actual inference and all preparation failures were accounted | `raw/`, `attempts.jsonl`, `prepared/`, `gpu_initial.json`, `gpu_after_generation.json`, `resource_ledger.json` | 396 GPU calls/attempts, zero retries/transport failures. Interpretation errors and guard rejections are distinct |
| Replay is deterministic on saved outputs | `full_replay.log`, `complete_reproduction.log`, frozen hashes | Fresh GPU outputs and latency are not promised deterministic |
| A local prototype works end to end | `interface/verification.json`, `interactions.jsonl`, six screenshots, `browser_final.log` | Scripted demonstration, no human participants or workload measurements |
| Historical evidence is preserved | `historical_regression.log`, repository diff restricted to three new namespaces | Retail, HVAC, attention-session and earlier decision-reuse results retain their original interpretation |

Unsupported claims include a novel Bellman recursion, generally superior search, reduced cognitive load, transfer of a preference into consequential authorization, natural prevalence of cross-agent scoped decisions in these dialogues, absence of pretraining contamination, or an official MultiWOZ score.
