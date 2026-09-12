# What this exploration supports

Paths below are relative to `artifacts/verification_escalation/` unless stated otherwise.
The empirical outcome is exact reference-table agreement on one snapshot, not
universal SQL equivalence or independently measured semantic correctness.

| Claim | Exact evidence | Interpretation limit |
|---|---|---|
| Generated agreement saves questions while degrading the declared outcome | `repair/analysis/summary.json`, `paired.json`: generated, budget 1, verification versus recovery_completion | 24 disjoint source databases, two generation/intent replicas; four databases have source-integrity violations |
| The adverse point estimate remains under uniform integrity quarantine | `integrity_sensitivity/analysis.json`: loss difference +0.25, interval [0, 0.50] | Post hoc derived sensitivity, not a fresh guarded experiment; all cases retained |
| Missing interpretations explain the observed suppression failures | `repair/analysis/coverage.json`, `secondary.json`, `matched_examples.json`, `repair/evaluation/traces.json` | Reference-output coverage is weaker than semantic coverage; manual failure diagnosis is developer inspection |
| Complete annotated alternatives do not support benign ambiguity in this sample | `repair/analysis/summary.json`: reference condition; `repair/analysis/secondary.json` | Privileged candidate and answer implementation; ambiguity-selected benchmark does not estimate practical prevalence |
| Direct source reading can remove redundant questions in the availability diagnostic | `repair/analysis/direct_source_reader.json`, source_recovery rows in `summary.json` | Six databases, 12 replicas; constructed availability manipulation and secondary prompt-style comparison |
| A stronger direct-reader prompt does not solve the ambiguous-input task | `direct_reader_audit/analysis.json`, `episodes.csv`, `frozen.json` | Separately declared post hoc audit on inspected cases; no new independent units |
| Conditional equality can safely save a question when its premises hold | `synthetic/example_traces.json`: equal_snapshot; `synthetic/episodes.csv` | Supplied interpretations and authored tables; mechanism example, not practical prevalence |
| Shared scope, exceptions and independent progress can be represented | `interface/final/interactions.jsonl`, `replay_verification.json`; synthetic unaffected_work and scope_exception | Scripted demonstration only; empirical tasks have no annotated cross-task decision |
| Registered changes invalidate artifacts, and invalid source snapshots block release | Focused tests in `research/verification_escalation/test_online.py`, `test_boundaries.py`, `test_integrity.py` | Registered dependencies and represented scope only; unknown semantic relations are not automatically detected |

No evidence here supports reduced human cognitive load, an empirical advantage
unique to several agents, quality-preserving automatic question suppression, or
superiority to the closest published systems. The most defensible deliverable is
the instrumented protocol and its reproducible negative boundary result.
