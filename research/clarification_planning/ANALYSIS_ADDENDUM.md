# Post-freeze analysis and comparator audit

This addendum does not replace the frozen protocol or its outcomes. It is recorded
before inspecting the completed held-out summary tables. The source cases and
GPU outputs are already generated, so any added comparison is secondary and uses
previously collected preparations, not a new confirmatory sample.

1. The frozen analysis completed its CSV computations but failed when serializing
   NumPy integer win/tie/loss counters to the final JSON. `analysis_runner.py`
   converts scalar types only at serialization. Frozen analysis.py, statistical
   definitions and policy traces stay unchanged. The original failure log is saved.
2. This host's Matplotlib predates TwoSlopeNorm and the combined tick/label API.
   Plotting uses symmetric Normalize limits around zero and separate tick labels.
   No numerical data are changed.
3. The declared completion heuristic counts every still-queryable factor in a
   task, including uncertain supplied values. That can overcount how many answers
   are actually sufficient to cross the common release threshold. It is a clear
   baseline limitation. Add a **minimum sufficient completion** audit, using the
   same public beliefs, question channel and release rule. Enumerate small blocks
   of unasked dependencies in increasing total cost. Keep a block only when every
   supported response path permits the selected task to be released. Among the
   smallest blocks for currently deferred tasks, break ties by expected task-loss
   reduction per question cost, then task ID and factor ID. Execute the first
   question and re-evaluate. Ignore already releasable tasks, as a completion-first
   heuristic normally would. Questions resolving several tasks are still charged
   once. Limit block size to six and the remaining budget. With no sufficient
   affordable block, stop and defer. This comparator is deterministic, uses no
   true targets, and receives no additional generation budget.

Run the audit at every declared empirical response budget and all three loss
weights. Also run it on the small transparent complementary fixture. Keep its
paired results explicitly secondary. If it matches or beats the planner, that
limits a practical algorithmic advantage even if the two frozen primary contrasts
are favorable. It must not be omitted because it weakens the claim.

4. The frozen example rule selects the first qualifying dialogue and initially
   displays replicate zero. Replicate zero sometimes ties even when the dialogue
   average qualifies through replicate one. Keep every selected ID unchanged and
   preserve the original replicate-zero trace file, but expand the final figure
   to show both replicates. This presentation change is explicit and does not
   select another outcome or alter statistical comparisons.
5. The online protocol repair is isolated from frozen experiments. It also checks
   explicit exceptions on applicability-gate records and exposes the stronger
   completion audit in the same interface. No evaluation outcomes are regenerated
   under a silently changed protocol. The original inference and timing records
   remain authoritative for the experimental accounting.
