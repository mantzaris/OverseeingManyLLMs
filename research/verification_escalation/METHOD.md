# Verification-guided escalation

The unit of utility is a requested table artifact, not an agent instance. A project
has distinct deliverables T, registered decision dependencies, scoped source records,
a current SQLite snapshot and an output contract. User budget B counts substantive
intent answers, including unresolved replies. A machine budget M counts SQL
executions, including failures. Model calls are separately bounded and recorded.
No count here measures human mental workload or financial loss.

We use exact outcome agreement rather than minimax regret. For task j, execute
all represented candidate programs C_j on snapshot X. If every execution succeeds,
all normalized tables agree, the artifact contract permits snapshot output and
no explicit semantic choice is required, the common table is conditionally
invariant over C_j. Primary generated-candidate release additionally requires two
independent generation passes, at least two different SQL strings, no declared
unsupported alternative and nonempty results. These are conservative heuristics,
NOT calibrated coverage. An empty correct result can still be released after an
answer; two empty guesses are insufficient verification. Every failed candidate
blocks verification. No survivor-only comparison is used.

The certificate establishes only equality of the represented outputs under the
checked contract and snapshot. It does not establish intended-meaning coverage,
universal SQL equivalence, semantic/process compliance, or absolute quality.
We therefore score omitted reference outputs and incorrect suppression separately.
No probabilistic guarantee is claimed. Agreement from correlated errors is an
explicit failure condition, not independent evidence of correctness.

## Protocol

1. Read the entire compact database and all available instructions. The common
   model backend proposes up to three interpretations on each of two passes.
2. A recovered authoritative requirement must cite the entire existing instruction
   exactly and match its registered scope and exceptions. A copied quote validates
   provenance only. Its generated implementation may still be wrong.
3. Execute candidates with a read-only SQLite authorizer, 100,000 VM-instruction
   limit and 500-row cap. Record failures. Whole-database setup comes from trusted
   source artifacts, never generated SQL.
4. Release source-resolved or conditionally invariant tables. Keep other tasks
   independent. Explain differing results when asking which interpretation applies.
5. Ask at most one atomic intent question per registered decision, charge it before
   receiving a response, and execute the SQL generated from the actual clarified
   instruction. Unsupported answers remain unfinished. Shared answers apply only
   to registered dependencies with matching scope, version and exceptions.
6. Changes to source, scope, task contract, candidates or snapshot invalidate the
   certificate key. Registered revisions increment the version. Previous source
   records and interaction logs remain available.

A result is an unordered bag of rows with duplicate multiplicity, column order,
output width and NULL preserved. Strings compare exactly. Integer and floating
representations of the same exact decimal normalize together; there is no numeric
tolerance. Column aliases are ignored. Ordered contracts preserve row order.
The empirical contract requests snapshot tables and does not require ordering.
This is an explicitly adapted execution metric, not the official AMBROSIA score.

## Comparators and formal limits

Recovery plus minimum sufficient completion calls the historical public-only
MinimumCompletion policy. Recovery plus depth two calls its historical Bellman
planner. Each ambiguous source task has one unresolved intent, represented by
an assumed equiprobable binary factor, incorrect-release cost 4 and deferral cost
1. Asking perfectly reveals that abstract factor; actual generated answer errors
are retained by evaluation. With one question per task these two methods coincide.
They receive the same sources, candidates and execution budget as verification.
They do not receive annotated answers before asking. These are controlled
adaptations, not full reproductions of external systems.

Full context releases its first executable proposal, asking only when none works.
Matched checking executes the same candidates and selects the modal result, ties
by candidate order. This tests additional checking without the escalation rule.
Ablations remove recovery, verification, the generated coverage guard, registered
sharing, or selective continuation. The latter waits for all work. Reference
candidates intentionally receive privileged annotated SQL and exact returned
answers; their outcomes isolate mechanism feasibility, not deployable accuracy.

Budget adherence follows by induction: answer checks spent<B before increment;
execution checks used<M before increment, including failures. A revision never
resets either counter. Keys include all represented dependencies. These invariants
cannot discover missing dependencies or prove inferred scope is correct.
With n tasks and k<=6 candidates, one inspection costs at most nk bounded SQL
executions, memoized by dependency key. There is no optimizer or novelty claim
for enumeration. The proposed contribution is a testable conditional release and
escalation protocol that exposes the coverage boundary in multi-deliverable work.
The experiment may show that this protocol adds too little over source recovery.
