# Verification-guided escalation: completed exploration

**Recommendation:** retain source recovery, explicit scope and targeted clarification.
Do not make automatic release from generated-query agreement the paper's central
method. The prototype is useful for showing consequences and letting unaffected
work proceed, but the operational experiment saved questions by missing relevant
interpretations. It did not preserve the stronger completion baseline's outcomes.

The current implementation and evidence are separate from all completed maintenance,
retail, attention-session, decision-dependency and clarification-planning studies.
The submission manuscript is unchanged. Work began on clean `main` at `9cea20b9`.
Protocol freezes are `ab3c62df` and `58c366d7`; the evaluated implementation and
results milestone is `683e4840`. Nothing was pushed.

## Research question and implemented method

Can executable checks of competing interpretations reduce substantive user decisions
beyond source recovery plus minimum sufficient completion, while preserving useful
completion and correctness? We study requested **snapshot tables**, not universal
SQL programs or database changes.

The controller reads public evidence, attempts exact provenance-checked source
recovery, generates candidate interpretations, runs bounded read-only SQL, and
compares complete table outputs. A task can proceed when its represented outcomes
agree and its public output contract permits that release. Other tasks remain
separate. A question includes the unresolved issue, source evidence, proposed
interpretations and their consequences, affected scope, and work already able to
continue. A charged unresolved reply leaves the task unfinished.

The protocol does not certify that the correct interpretation was generated. Its
certificate states equality over a finite candidate set on a named snapshot under
a specified output contract. Every candidate must execute; failing queries are not
dropped to create agreement. Primary generated release also requires two generation
passes, distinct SQL strings, no declared unknown alternative and nonempty results.
These are uncalibrated safeguards. Aliasing differences can satisfy syntactic
diversity without adding a meaning. Two mistaken COUNT queries can agree on zero
while still returning one row. That counterexample is an executable test.

The controller uses registered decision dependencies, scope, exceptions and versions.
Semantic similarity alone never authorizes answer transfer. Cache keys include all
represented source, snapshot, task, scope and candidate dependencies. The online
wrapper handles renewed questions after revisions, rejects stale displayed questions,
and avoids rerunning an unchanged failed answer. See [the method](METHOD.md),
[the corrected contract](REPAIR_PROTOCOL.md), and [the exact verification boundary](VERIFICATION_BOUNDARY.md).

## Source audit and development boundary

We inspected full methods and evaluations for AmbiQT, AmbiSQL, PRACTIQ,
BIRD-Interact, KnowNo, Value of Information, AMBROSIA, Disambiguate First Parse Later,
Sphinteract and SOMA-SQL. [LITERATURE.md](LITERATURE.md) gives sections, publication
status, assets and precise distinctions. BIRD-Interact still requires requesting
reference SQL/tests. No request or external contact was made. AmbiSQL's inspected
code contains five interface examples, and PRACTIQ supplies a generation pipeline.
AmbiQT's mapping of constructed alternatives back to original SQL could produce
mechanical equality, so it was not used to claim practical verification benefits.

The accessible fallback is [AMBROSIA](https://ambrosia-benchmark.github.io/), a
NeurIPS 2024 benchmark. Its questions and disambiguated interpretations are
human-authored. Its 846 databases are generated and filtered benchmark records.
Scope/attachment SQL is template-generated and vague SQL human-authored. These are
not observed operational databases or observations of humans using our system.

Nine distinct databases supported two development passes, 72 scheduled calls.
Development found context failures and no verification-specific question savings.
We compacted the public database serialization and clarified the unsupported-option
flag, retaining both passes. A first frozen evaluation then used 48 fresh databases
and two replicas, with 312 further calls. Inspection found an ordering defect: its
blanket unordered contract and prompt contradicted ranking requests 2842 and 2863.
All those rows remain under the original `evaluation/` namespace as a **flawed-adapter
diagnostic**. They are not pooled with the principal follow-up.

Before generating the follow-up, commit `58c366d7` froze an ordering-aware public
contract and **24 new databases**, eight per ambiguity type. It excluded all 57
previous databases. Selection used source order and the original semantic eligibility
rules, never model outcomes. The controller, comparison methods, scoring and analysis
remained fixed. The selected fresh requests contain no explicit ordering detected by
the frozen regex, so ordered semantics are exercised by focused tests, not estimated
as a separate fresh empirical effect. The changed prompt nevertheless removes the
incorrect blanket instruction from every case.

The 24 databases span four domains and reused source construction conventions.
They are the paired analysis units, not 48 independent observations. Source-order
selection and shared domain/templates limit population inference. Two replicas vary
model seeds and rotate the simulated intended annotation. They therefore cover both
generation and intent variation, rather than pure repeated sampling of one intent.
No source annotations establish a shared decision across separate tasks. All shared
agent dependencies below are authored extensions.

## Frozen principal comparison

Each replica uses two public candidate-generation calls and one separately cached
SQL generation after the simulated clarification. The latter remains inaccessible
until a policy spends an answer. Six databases also receive a source-availability
condition that places the actual annotation in a prior scoped instruction. It needs
12 additional calls. The corrected batch therefore uses **156 GPU calls**, 48 task
replicas, and **3,240 policy/condition rows**. All planned rows were retained.

Policies share the same preparations, available evidence, candidate checks, answer
cache and budgets. Core methods are recovery plus minimum completion, recovery plus
the historical depth-two planner, verification, a first-executable full-context
proposal, and execution-result voting with matched candidates. The last two are
explicit adaptations, not reproductions of SOMA-SQL or other published systems.
Ablations remove recovery, verification, coverage guards, sharing or independent
continuation. One intent question resolves each empirical task, so minimum completion
and depth two mechanically coincide. Budget two also cannot improve on budget one
through an additional interaction in this adapter.

The primary budget is one intent answer per task. Budgets zero and two are also
reported. Machine budget is 24 SQL executions per task; query limits are 100,000 VM
instructions and 500 rows. Repeated-question and cross-scope-transfer counts are zero by construction in these single-task source cases; they are not empirical evidence of semantic scope recognition. Model context is 2,048 tokens, output limits 512 for
candidates and 256 for answered SQL. The existing Qwen2.5-7B-Instruct revision
`a09a35458c702b33eeacc393d103063234e8bc28` ran in BF16 on one RTX 6000 Ada with zero
CPU offloading, temperature 0.3 and top-p 1. GPU placement, process identity and
server status are saved. Host SQL execution and analysis are ordinary orchestration.

We preserve duplicate rows, column positions, NULL, exact normalized values and
requested ordering. Aliases do not affect comparison. This stricter adapted metric
is **reference-table agreement**, not the official AMBROSIA metric. The source's
unordered comparator flattens row cells; we do not use it. An extra output column
can cause a mismatch without proving a wrong semantic interpretation. Public
execution checks establish executable shape and bounds, not semantic correctness.

## Principal results

Totals below are over 48 replicas from 24 source databases at budget one. A mismatch
is a released table differing from the selected reference under the frozen contract.
Each row accounts for all 48 deliverables. Whole-project agreement is the same as
task agreement here because each empirical project contains one requested artifact.

| Method | Intent answers | Matching tables | Mismatched releases | Unfinished | Loss | SQL executions |
|---|---:|---:|---:|---:|---:|---:|
| Recovery + minimum completion | 48 | 19 | 22 | 7 | 95 | 240 |
| Recovery + depth two | 48 | 19 | 22 | 7 | 95 | 240 |
| Verification | 40 | 16 | 26 | 6 | 110 | 231 |
| Full-context first executable proposal | 3 | 14 | 34 | 0 | 136 | 190 |
| Matched execution voting | 3 | 14 | 34 | 0 | 136 | 190 |
| No coverage guard | 40 | 16 | 26 | 6 | 110 | 231 |

Verification saves eight answers but loses three matching results and adds four
mismatched releases. It does not meet the desired quality-preserving interpretation
of reduced demand. There is no declared noninferiority margin and no claim of
preserved quality from overlapping uncertainty intervals.

Replicas were averaged within database before 2,000 paired bootstrap resamples,
seed 86421. Intervals describe this small, deliberately ambiguous sample.

| Verification minus completion, per task | Mean | Paired 95% interval |
|---|---:|---:|
| Intent answers | -0.1667 | [-0.2708, -0.0625] |
| Matching tables | -0.0625 | [-0.1458, 0.0000] |
| Mismatched releases | +0.0833 | [+0.0208, +0.1667] |
| Unfinished work | -0.0208 | [-0.0625, 0.0000] |
| Loss, 4*mismatch + unfinished | +0.3125 | [+0.0625, +0.6250] |

At the source level, loss yields **0 wins, 20 ties and 4 losses** for verification.
Seven databases save answers and 17 tie. The declared loss-weight sensitivity gives
mean differences +0.0625, +0.1458, +0.3125 and +0.6458 for mismatch weights 1, 2, 4
and 8. These rescore unchanged trajectories; they are not new optimized policies.
A post hoc aggregation across only four domains remains unfavorable, but four
clusters cannot provide a stable broad-population uncertainty estimate.

At budget zero, completion leaves all 48 tasks unfinished. Verification releases
two matching and six mismatched tables and leaves 40 unfinished. Budget two repeats
the budget-one outcomes. Full-context answering and voting suppress more demand,
but their 34 mismatched releases make clear why question reduction alone is not
success. Full declared tables and per-source paired differences remain saved.

## What caused the difference

**Candidate coverage is the bottleneck.** The generated candidate sets contain the
intended reference output in 15/48 replicas and every annotated output in 0/48.
Eight verification releases suppress a question. Six mismatch the target, and all
six lack its output in the candidate set. There are 28 failed executions among
187 public candidate programs. One of the 96 corrected public generation calls
produces unparseable JSON. Failed candidates block equality rather than disappearing.
Seven baseline clarified implementations remain unfinished; none was replaced.

The privileged-reference diagnostic supplies all annotated SQL interpretations and
an exact returned implementation. Every one of the 24 source databases has differing
reference outcomes. Completion and verification both ask 48 questions and return
48 matching tables. Thus the operational savings do not reveal a source-supported
region of harmless ambiguity. Two generated suppressions happened to match the
selected intent while still omitting other supported outputs.

Developer inspection of the six suppressed mismatches found five with a missing
semantic requirement and one attributable solely to extra projected columns. This
is post hoc code inspection, not independent human expert validation or rescoring.
The four incremental mismatches relative to completion involve missing attachment,
collective or inclusive interpretations. The finding therefore cannot be explained
only by the strict projection metric. The complete review is saved in
`repair/analysis/failure_review.json`.

**Source recovery explains the safer opportunity.** In the six-database availability
subset, seven of 12 preparations satisfy the exact source-citation check. Completion
uses five answers, with five matching, six mismatched and one unfinished result.
Verification uses four answers, with four matching, seven mismatched and one
unfinished result. Its one extra suppression loses a matching table.

A secondary source-reading audit uses the cached SQL response to the exact same
available instruction, rather than requiring a candidate-enumeration prompt to
quote it. It uses **zero questions with the same 5/6/1 outcome counts as completion**.
This prompt-style diagnostic is not the frozen common-backend comparison, but it is
a stronger practical source-reading alternative. It shows that some repeated
questions compensate for a narrow recovery interface. It does not eliminate the
model's remaining SQL interpretation failures.

## Source-integrity limitation and guarded sensitivity

The source audit recorded foreign-key violations in four of the 24 generated
databases (IDs 467, 2900, 2896 and 2981). All 56 reference queries execute, but that
alone is not sufficient source-integrity validation. The frozen controller did not
gate releases on these recorded violations. One of its eight agreement releases
(ID 2896 replica 1) occurs on such a database. This limits the frozen protocol as
a practical release rule and is preserved explicitly rather than erased.

The current online prototype checks SQLite integrity and foreign keys before
candidate execution, charges those checks, and leaves affected goals unfinished.
Other valid sources can proceed. A separately labeled **post hoc uniform-quarantine
sensitivity** uses the same saved preparations, retaining all 24 units and placing
both replicas of the four inconsistent databases in unfinished status for every
method. It is not a new held-out study or measured new controller latency.

Under this rule, completion asks 40 questions and yields 17 matching, 18 mismatched
and 13 unfinished results. Verification asks 33 and yields 14 matching, 21 mismatched
and 13 unfinished results. Loss is 85 versus 97. The paired mean loss difference is
+0.25 with interval [0.00, 0.50], and 0 wins, 21 ties, 3 losses. The adverse point
estimate persists, but the interval now includes zero. It does not demonstrate
equivalence or preserved quality. This sensitivity isolates source quarantine;
it does not reinterpret the original trace as a newly executed guarded run.

## Additional direct-reading audit, declared after the principal result

The frozen full-context baseline selected its first executable candidate from an
interpretation-enumeration prompt. To check that limitation, commit `80f5722a`
declared a separate direct-reading, answer-or-ask prompt, four fixed development
cases and both replicas of the same 24 already inspected source cases. The 52 new
calls bring the session total to 592, within the original 600 ceiling. This is a
**post hoc comparator audit**, not another fresh held-out evaluation. No primary
method, source selection or frozen result changed.

The direct reader requests clarification in six replicas and declares 42 ready.
At budget one it yields 12 matching, 30 mismatched and six unfinished results, with
six answers, 48 SQL executions and loss 126. At budget zero it has 12 matching,
25 mismatched and 11 unfinished results. None of its six clarification branches
produces a matching table; five produce mismatched tables and one remains unfinished.
Thus a simpler direct-reading prompt does not establish a superior automatic
alternative on these ambiguous tasks. The existing source-availability direct-reader
diagnostic remains distinct: it has an explicit prior instruction and matches
completion with zero extra answers. Both findings favor distinguishing available
knowledge from unresolved intent rather than treating fewer questions as success.

The new prompt uses only the public request and database. It may independently
choose ready, clarify or unsupported. A malformed/unsupported result or failed SQL
remains unfinished; a syntax failure alone does not trigger a user question. This
is another controlled practical adaptation, not a reproduction of a published
full-context system. Its model-call budget is smaller, while its maximum execution
budget matches the other methods. Complete paired summaries and raw traces are in
`direct_reader_audit/`. Its observed cases are not counted as additional independent
source units.

## Synthetic mechanisms and their limits

The frozen synthetic set has 17 authored family labels, 16 nuisance seeds per family,
three answer budgets and ten methods, producing 8,160 rows. These are controlled
arithmetic cases, not 272 independent real-world projects. Several labels reuse the
same structure. They cannot estimate the prevalence of harmless uncertainty.

| Controlled case, budget one | Completion | Verification | Interpretation |
|---|---|---|---|
| Available authoritative source | 1 correct, 0 answers | 1 correct, 0 answers | Source recovery already suffices. |
| Equal snapshot outputs | 1 correct, 1 answer | 1 correct, 0 answers | Conditional output release can save a decision when coverage is stipulated. |
| Different outputs | 1 correct, 1 answer | 1 correct, 1 answer | No benefit when the distinction matters. |
| Scoped exception with invariant count | 1 correct, 1 unfinished | 2 correct, 0 unfinished | The count can proceed independently; this is not answer transfer across the exception. |
| Missing intended interpretation | 1 correct, 1 answer | 1 wrong, 0 answers | Consensus conceals a consequential omission. |
| Correlated omission across export/count | 2 correct, 1 answer | 1 correct, 1 wrong, 0 answers | Shared model mistakes do not become independent evidence. |
| Failed query or direct empty-result trap | 1 correct, 1 answer | 1 correct, 1 answer | Conservative checks prevent survivor-only agreement. |
| Explicit semantic-choice requirement | 1 correct, 1 answer | 1 correct, 1 answer | Equal tables do not override the requested decision. |
| Unresolved reply | 1 unfinished, 1 answer | 1 unfinished, 1 answer | No artificial completion after deferral. |

A changed snapshot invalidates an earlier equality result. An unchanged snapshot
never proves equivalence on a future database. At budget zero, selective continuation
returns two unaffected results in the authored three-goal workload; global waiting
returns none. At budget one, both finish all three goals with one answer. This is a
modeled progress distinction, not a measured response-time or cognitive-load effect.

The export and count have registered sharing, but the count often happens to be
invariant. Consequently, the frozen no-sharing ablation has no quality effect in
these cases. A duplicate-question guard would also limit its generality for two
consequential tasks; the online wrapper repairs that case and tests it separately.
Neither repair nor authored sharing establishes an empirical multi-agent advantage.
Agent labels can be multiplied without changing utility, goals or outcomes.

## Examples, figures and working system

The frozen rule selects the first lexicographic source ID with a favorable, tied or
unfavorable mean loss difference, showing both replicas. There is **no favorable
empirical loss example**. The tie is ID 1475: both policies ask, one clarified query
misses the common-to-all requirement, and the other replica matches. The unfavorable
example is ID 1484: one replica needs the program common to all authorities.
Verification releases a six-row authority/program join without asking. Completion
asks and returns the one-row common-program result. The other replica matches under
both methods. The synthetic equal-snapshot case supplies a visibly labeled success.

Eight numerical figures have PDF, SVG and PNG exports under `repair/figures/`:
quality versus questions with source-level intervals, budget failures, resolution
routes, coverage/cost, paired differences, synthetic ablations, event timelines and
matched examples. Plots are generated from saved rows and traces. Captions distinguish
human-authored annotations, model-generated databases/proposals and simulated policy
or workload mechanisms. No figure labels GPU latency as human inspection time.

The localhost Decision desk displays available source resolutions, ready and
unfinished goals, differing query outputs, answer scope, affected work, and separate
question/check budgets. A user can answer broadly or only this request, leave a
question unresolved, revisit an instruction, or simulate changed data. Partner
scope remains separate. Eight browser screenshots and the actual displayed-interaction
log are saved under `interface/final/`. They are scripted software observations,
not participant data. See [API.md](API.md) and [README.md](README.md).

## Novelty and paper recommendation

Avoiding clarification, considering alternative interpretations, retrieval, SQL
execution probes and expected-value communication are established. PRACTIQ already
returns useful outputs covering some ambiguity. Disambiguate First Parse Later
uses execution to diagnose missing interpretations. SOMA-SQL closely overlaps the
general combination of retrieval, alternative candidates and execution probes.
Our possible distinction is a conditional artifact-release protocol that exposes
unresolved meaning, scope and dependencies rather than claiming to infer intent
from a database pattern. This is useful system design, but not yet a demonstrated
new algorithm or sufficient central paper contribution.

The evidence supports a concrete warning about generated-candidate agreement and
a reusable instrumented desk. It does **not** establish quality-preserving decision
savings, reduced human mental workload, or an empirical benefit unique to several
agents. Keep this as a separate negative-results research note. The strongest next
step is a source-reading and targeted-clarification system with explicit task
contracts; evaluate interpretation coverage on genuinely shared user work before
allowing automatic suppression to become a central method. More timing replays or
larger samples of this same omission-prone protocol would not resolve that issue.

## Verification, preservation and accounting

Thirty-four focused tests passed, including hidden-answer isolation, budget limits,
source revocation, scope exceptions, candidate omission, ordered/bag comparison,
failed-query accounting and cache invalidation. The 27 relevant historical
clarification tests passed once. All 3,240 corrected rows, 6,480 initial diagnostic
rows and 8,160 synthetic rows replay exactly in outcomes and events; eight primary
analysis tables reproduce. The 18 final displayed interactions also replay. The
browser ran 14 checks. Earlier failed tests and browser attempts remain preserved.

The final one-command reproduction also verifies 144 post hoc direct-reader rows
and all 3,240 derived integrity-sensitivity rows. The separate 14-page research note
compiled with no final-pass LaTeX warnings or unresolved citations. All pages, eight
numerical figures and eight interface captures were visually inspected. Source
disjointness is within this project; public-benchmark training contamination is
unknown. The release rule assumes that registered source authority is accurate.

The first run's ordering defect is separately recorded, not silently fixed by
rescoring its generations. The initial 48-database diagnostic found 87 versus 96
answers and loss 176 versus 169 for verification versus completion. Those numbers
are retained only with the defective-adapter qualification. Prior stages, frozen
estimators and manuscript sources were not changed.

Full source records and raw prompt envelopes remain local and excluded from Git,
following the source authors' request against uploading their dataset. The release
contains source IDs/hashes, generated SQL, compact outcomes, attempt accounting,
figures and source-reconstruction code. This publication-redaction choice is explicit
and does not rewrite historical redaction provenance. A clean checkout can reproduce
tables and figures without new inference after downloading the original source.

<!-- ACCOUNTING_START -->
The separately authorized session began **2026-09-11 23:08:26 UTC**, with deadline
**2026-09-12 02:08:26 UTC** and inference cutoff **01:23:26 UTC**. At the final
accounting checkpoint `2026-09-12T00:53:48.700237+00:00`, elapsed time was
**1h 45m 23s**. The final repository commit follows this
checkpoint. The selected experiment and reporting finished before the three-hour
limit; unused time and call allowance were not filled with additional experiments.

| Batch | Scheduled calls | GPU attempts |
|---|---:|---:|
| Two development passes | 72 | 66 |
| Initial flawed-adapter diagnostic | 312 | 312 |
| Disjoint ordering-correct follow-up | 156 | 156 |
| Post hoc direct-reader audit | 52 | 52 |
| **Session total** | **592 / 600 ceiling** | **586 / 1,200 ceiling** |

Six development requests failed the context-length check before generation. There
were zero transport failures or retries and two unparseable successful responses;
all remain recorded. Usage was **461,283 prompt tokens + 79,978 completion tokens
= 541,261 tokens**. Summed generation latency was **1,673.44 seconds**, which is not
provider allocation or billing time. The last generation began at
**2026-09-12 00:25:31 UTC**, before the reporting reserve. No paid resources were
provisioned. Price and provider billing/allocation totals were unavailable.

Cumulative wall time from the preserved original start is
**57h 14m 52s**, or **21h 14m 52s**
beyond the original 36-hour target. This includes inter-session gaps and is not a
sum of active research hours. The original deadline was already past when this
new session was authorized. Cumulative recorded inference is **57,358 scheduled
calls**, **57,354 attempts**, two retries, three failed attempts, **31,795,238 prompt
tokens** and **867,356 completion tokens**. Historical ledgers were not reset.

Per-policy SQL executions, including failures, are in the episode tables. Auxiliary
source-audit, evaluator and replay CPU queries are not exhaustively counted in a
session-wide tool ledger. The integrity sensitivity's execution charges are derived;
its latency field is intentionally absent. Model inference ran on the existing
RTX 6000 Ada in BF16 with zero CPU offloading. A final read-only check returned HTTP
200 with the pinned model and unchanged server process. The temporary local UI,
headless browser, inference tunnels and experiment workers have stopped. The
existing GPU server remains running. See `resource_ledger.json`,
`final_service_status.json` and `temporary_service_cleanup.json`.
<!-- ACCOUNTING_END -->
