# Figure definitions and captions

All principal plots live in `artifacts/verification_escalation/repair/figures/` with
PDF, SVG and 240-dpi PNG exports. Scripts read saved episode CSV/JSON and event
traces. The principal set has 24 source databases and two generation/intent replicas;
source availability is a paired subset of six databases. All sources are externally
authored benchmark tasks, not observed use of our system. No graphical encoding
represents human cognitive load.

| Figure | Caption and provenance |
|---|---|
| quality_vs_questions | Reference-table agreement versus simulated intent answers. Requests/annotations are human-authored; databases and SQL are generated. Intervals average replicas within source database before 2,000 fixed-seed resamples. Direct source reading is a secondary prompt-style diagnostic. Overlapping points are true ties, not omitted methods. |
| failures_and_budget | Mismatched releases and unfinished work across fixed answer budgets. Generated SQL and simulated policy replay. Budgets one and two tie because each source task offers one substantive intent question. |
| resolution_routes | Proportions recovered, conditionally equal, asked, or otherwise released/unfinished, at budget one. Generated preparations and simulated controller routes. A conditional equality route is not proof of correctness. |
| coverage_and_cost | Evaluator-only reference-output coverage versus release mismatch, plus charged SQL executions and simulated answers saved. Output coverage is weaker than semantic interpretation coverage. Same preparation calls across controlled methods; generation cost is separately logged. |
| paired_differences | Verification minus completion at budget one, with every source database in frozen ID order. Labels identify the four nonzero loss differences; the other 20 are ties. Negative loss would favor verification. Component intervals are paired source-level bootstrap intervals. |
| synthetic_ablations | Authored SQL workloads and stipulated interpretations, scopes and failures. Each cell is a mean difference from completion across nuisance seeds. These are mechanism tests, not empirical prevalence estimates. Displayed gains and harms use the same declared scoring. |
| synthetic_event_examples | Authored equal-count/blocked-export workflow and correlated-omission failure. Horizontal position is controller event order, not human time. Event colors distinguish release/update from question/answer, not correctness. A released export can be wrong. |
| matched_examples | Synthetic equal-snapshot success plus the frozen first tied and unfavorable source IDs, both replicas retained. No favorable empirical loss case exists. Source outputs are generated SQL scored against annotations, while the left panel is an authored control. |

Eight interface screenshots under `interface/final/` show source recovery, pending
consequences, scope exceptions, intent revisions, snapshot invalidation, narrow scope
mobile layout and a readable paper detail. They are scripted demonstrations. Their actual displayed records
replay separately from numerical policy experiments.
