# Stage 6 bounded robustness and manuscript plan

Declared 2026-09-10 before new evaluation outcomes. Baseline is Stage 5 commit
`189cf517dc06f4bf3008281c0d2966dbceba928b`. Preserve every historical artifact and
all positive, null and unfavorable findings. Stage 6 starts 21:18:02 UTC, stops
inference by 2026-09-11 01:48:02 UTC, and ends by 03:18:02 UTC. Maximum 6,000 GPU
attempts, one retry per call, 60-second attempt timeout. A separate append-only
ledger enforces this window. No new paid resources or additional model search.

## Question and conditions

Does planning currently visible review order improve operational loss when the
reviewer can only approve or block? How sensitive is allocation to a simple
transaction-complexity review time? The source-based
[assumption review](../paper/RETAIL_ASSUMPTION_REVIEW.md) motivates these changes
and explicitly does not constitute independent human validation.

All conditions retain the frozen Stage 5 application estimator, automatic guards,
preparation interface and GPU decoding. Six policies are no review, FCFS, EDF,
uncertainty-first, delay-aware greedy and queue-order search. Both base review
capacities, one and two ticks, are retained. Three operational variants are:

1. **Reference:** unchanged Stage 5 correction authority and constant review time.
2. **Approve/block:** perfect detection only at completed review. Approve the
   unchanged correct proposal; block a wrong proposal without any replacement
   mutation. Blocking avoids processing cost but leaves service unresolved.
   Expected timely benefit is p times processing cost, rather than p times the
   sum of service and processing costs. Blocking is not task completion.
3. **Complexity time:** original correction authority, but add one review tick
   when the staged proposal's public item list contains at least two entries.
   All other settings match the reference. This is a constructed sensitivity,
   not a measured human time estimate. No combination with restricted authority.

Eligibility requires release and positive expected benefit from completion by
the cutoff, including equality. Only released public requests enter scheduling.
The oracle label or target can be used only in scoring or completed review.
After a cutoff posts a transaction, no subsequent review erases the consequence.
An unstaged workflow cannot be reviewed and retains four points service loss.

## Source pool and selection

Audit all 500 train, 20 dev and 115 test task records at the pinned upstream
revision. Exclude all 120 customer accounts appearing in Stage 5 declarations,
including development and pilot selection records, across every split. Keep the
historical supported explicit-instruction templates, single mutation, no
additional output requirement, and source-intent consistency checks. Inspect
annotations for tool validity and unique intent mapping, never model outcomes.

Use train then dev then test, ascending index within each family. Reserve the
scarce modification family first, cancellation next, returns/exchanges last,
with globally unique accounts. Choose 16 bundles if feasible, otherwise eight,
otherwise no fresh source-case evaluation. The completed pre-inference source
audit finds 10 unused eligible modification accounts, 26 cancellation and 69
return/exchange accounts. Sixteen bundles are infeasible. **Freeze eight bundles,
24 distinct train cases, three fresh replicates (0,1,2): 72 workflows.**
Duplicates across source splits are recorded. No customer account overlaps
Stage 5. Broad templates and public-benchmark contamination remain limitations.

## Frozen execution and limits

Use eight source bundles in ascending selected-family order. A Stage 6 scenario
seed prefix 62000 independently permutes arrivals 0/0/1, relative windows 2/4/5,
processing weights 4/8/12 and agent-family assignments, using the historical
bundle construction algorithm. Generation metadata uses partition
`stage6_evaluation`, bundle IDs `stage6_00` through `stage6_07`, replicate, source
case ID, tool step and retry. SHA256 gives the sampling seed, independent of
policy, capacity, operational variant and execution order. Rotate policy order
and balance which capacity runs first in local replays.

Every preparation uses fresh GPU calls and its own agent history. Reuse identical
saved preparations across six policies, two capacities and three variants:
**864 paired policy episodes**. At most 14 ordinary calls per workflow gives
**1,008 scheduled calls and 2,016 attempts**, within the session ceiling. No
placement generation is required if serving identity and BF16 CUDA evidence can
be checked without generation. No LLM customer simulator. There are no
performance-driven preparation revisions or additional live pilots. Mechanical
fixtures and offline source checks are allowed before the freeze.

Forecast from Stage 5's measured 4,016 seconds for 288 workflows is about 1,004
seconds for 72 workflows; a factor-two margin reserves 34 minutes. Declare and
commit all source IDs, exclusions, bundle assignments, generation metadata,
model/interface/estimator hashes, analysis code and source snapshots before the
first call. If the existing pod is unavailable, retain the declaration as not
executed and complete saved-data sensitivity and manuscript. If time or budget
interrupts execution, retain every planned row as incomplete, do not replace
seeds, and report any missing paired bundles without inventing uncertainty.

## Analysis fixed before outcomes

**Primary:** search minus greedy bundle-mean operational loss under approve/block
at base review duration two. Average the three replicates within each bundle
first. Use 2,000 paired bundle bootstrap draws, fixed seed 20260916, resampling
all matched conditions together. Report percentile 95% intervals, all eight
bundle differences and win/tie/loss counts. Wide intervals containing zero do
not establish equivalence. Other policy contrasts, capacity effects and variant
minus reference contrasts are secondary, without multiplicity correction.

Report operational loss and service/processing components, correct tasks, wrong
commits, blocked unresolved requests, unstaged failures, completed review counts,
review time, waiting time, missed useful opportunities, actual sequences,
same-public-state greedy/search head differences, public queue competition,
initial error/risk diagnostics, generation variation, inference and planning
costs. Check that no-review outcomes are invariant and approve/block cannot
increase task completion above initially correct preparations. Report algebraic
consequences separately from empirical findings.

Also apply these frozen operational variants to all 32 Stage 5 evaluation
bundles using their existing preparations. Label this **post hoc saved-data
sensitivity**, not fresh held-out evidence. It uses no additional GPU calls and
is never pooled with the eight fresh bundles. Original Stage 5 rows must match
exactly under the reference. Do not tune the estimator or select further
conditions using either result set.

Select traces by ascending bundle then replicate, using the primary restricted
condition: first search benefit, tie, unfavorable result and preparation failure,
if available. Do not select by effect magnitude. Explain actual actions and
blocked/posting consequences. Record absent example categories honestly.

## Manuscript and completion

Target current ICAART 2027 regular-paper instructions from official pages. Use
the official LaTeX template, anonymous author block, verified bibliography and
accurate AI-assistance disclosure. Put essential methods and unfavorable results
in the main paper. A separate supplement provides detailed matrices, source
provenance, individual differences and traces. Do not assume that regular-paper
supplement upload is permitted unless official policy establishes it.

Compile and inspect all PDF pages, fix layout and citation problems, and record
page/character counts. Provide saved-output reproduction commands. Verify new
semantics, complete replay and accounting, and historical compatibility without
overwriting history. Commit milestones directly to main, no push/submission.
Stop Stage 6 workers and its separate retail server, preserving the original
server and persistent files. Report Stage 6 time and cumulative original-clock
elapsed time, with any overrun explicit.
