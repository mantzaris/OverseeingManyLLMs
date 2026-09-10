# Stage 5: retail transactions under shared simulated review

Authorized start: 2026-09-10 14:15:20 UTC. Hard stop: 23:15:20 UTC.
Inference stops by 21:45:20 UTC, leaving 90 minutes for verification and writing.
The original clock and all Stage 1–4 results remain historical evidence.

## Question and contribution

Does planning a finite review queue prevent more consequential retail transaction
errors than immediate expected-benefit ranking or earliest-deadline-first?
This is an adapted τ-bench retail study with added simulated processing cutoffs,
not an official benchmark score or evidence of measured human performance.
We inherit benchmark tools, policy and source cases, and established scheduling
mechanisms. The contribution sought is an auditable application experiment on
stateful LLM workflows, including where simpler scheduling is sufficient.

## Bounded implementation and operational semantics

Inspect the pinned upstream cancellation, pending-order modification and
return/exchange cases before selecting the exact supported subset. Agents must
retrieve account/order/product information, interpret policy, obtain required
scripted-user confirmations and propose actual upstream state-changing calls.
Use isolated local copies of retail databases. Preserve upstream tool guards;
explicitly document any additional automatic checks and scripted-user changes.

Separate transaction proposal, review completion, transaction commitment and
processing cutoff. A finite-duration perfect simulated reviewer may correct a
pending proposal only when its review finishes in time. It cannot undo a posted
transaction or consequence. Scheduling receives only public request features,
costs, cutoffs and development-fitted risk. Evaluation targets and task solutions
remain private. Define the objective and expected avoidable loss from these
retail semantics before live development, not from maintenance downtime.

## Development, calibration and freeze

Partition by underlying upstream source case/template, before inference. Audit
selected cases for feasible tools and internally consistent target states.
Use development only for workflow viability, risk fitting and throughput.
Permit at most two documented revisions; narrow the workflow scope at most once
if the model cannot operate it. Preserve every failed attempt and revision.
Fit a small application-specific estimator with declared sparse-bin fallback.
Do not transfer maintenance calibration, inspect evaluation labels to tune it,
or choose cases based on a scheduling winner.

Before evaluation publish exact source IDs, bundle composition, generation
replicates, seeds, prompts, estimator hash, capacities, costs, policies, order,
maximum calls, analysis and stopping rules. Target 16–32 bundles with three
generation replicates, subject to distinct feasible cases and measured runtime.
Compare no review, FCFS, EDF, uncertainty-first, delay-aware greedy and exact
queue-order search under one primary constrained and one secondary capacity.
Only add idealized unlimited review if it fits the forecast inexpensively.

## Resource and decision rules

One session-wide reservation ledger; at most 30,000 generation attempts including
development, diagnostics and retries; at most one retry per ordinary call and
60 seconds per attempt. All inference uses the pinned BF16 GPU model without
offloading. Keep historical server settings; any larger-context serving
configuration is separate and recorded. Simulated time is independent of GPU
latency. Do not launch unrelated benchmarks or outcome-dependent replacement
seeds. Checkpoint complete bundles and retain incomplete planned rows.

Prefer a valid completed smaller fixed matrix over an unfinished target. Once
evaluation starts, no redesign or tuning on its outcomes. Search gains, EDF
ties, weak risk, insufficient competition and model/tool failures are all valid
outcomes. Any revised follow-up requires a separately declared fresh set.

## Analysis and deliverables

Primary: search minus greedy operational loss at constrained capacity. Average
replicates within bundle; use paired bundle-level intervals and account for
reused source cases. Report task completion separately from policy violations,
loss components, waiting/utilization/missed reviews, scheduling differences,
risk calibration/discrimination, variability, tokens and planning/inference
time. Include EDF prominently and documented benefit/tie/failure trace rules.

Deliver the adapter and semantic tests, source/adaptation table, verified
primary-source bibliography, frozen raw evidence and replay/accounting audits,
Stage 5 report, updated research draft and claim-evidence map. Commit milestones
directly to main without pushing. Stop only Stage 5 workers; retain the existing
server and pod files. Final report includes cumulative time and submission gaps.

## Frozen evaluation declaration

The complete matrix is now fixed in
`artifacts/stage5_practical/evaluation_freeze.json`: 32 source-disjoint bundles,
96 evaluation source cases, three fresh workflow replicates, six finite policies
and review durations 1/2. This means 288 live workflows and 1,152 paired policy
replays. An inexpensive parallel-perfect-review reference requires no further
inference. At most 4,032 evaluation calls and 8,064 attempts are allowed by the
per-workflow limits, within the tighter session-wide 30,000-attempt ceiling.

Development retained one interface revision, no scope narrowing, and all failed
pilots. The calibration collection has 64 staged proposals, 15 initial errors
and eight unstaged failures. Its two-tick search loss exceeds greedy's on saved
development trajectories. The fixed evaluation proceeds without changing the
cases, scheduler, objective or estimator in response to that result.
