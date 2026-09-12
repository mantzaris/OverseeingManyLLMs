# What this implementation verifies

This note describes the current protocol. The frozen original METHOD.md remains
unchanged; REPAIR_PROTOCOL.md supersedes its blanket unordered empirical contract.

Let T be distinct requested table artifacts. Each task has a released request,
source records, registered scope, a version, a current database snapshot X, an
output contract K, and at most six generated SQL interpretations C. References and
the chosen simulated intent are evaluator-only. A candidate is a hypothesis, not
an independently validated reading of the request.

For each c in C, E(c,X,K) is a bounded read-only execution with a normalized result
or failure. Conditional agreement holds only if every E succeeds and every result
is identical. A release additionally requires the available structural constraints
and public process constraints to pass. Generated candidates require two sampling
passes, syntactic diversity, no declared unknown alternative, and a nonempty table.
These safeguards were fixed in development. They do not estimate set coverage.

The result is a finite-set certificate:

    for every represented c, E(c,X,K) = R.

It is not a statement that the actual intent belongs to C. It does not certify
semantic SQL equivalence, applicability to a later snapshot, energy or business
savings, authorization for a state change, or absolute output quality. Read-only
SQL cannot implement a consequential transaction in this prototype. Matching
outputs cannot override an explicit process/meaning requirement.

The controller operationalizes four states, with limited claims:

| State | Implemented evidence | Remaining uncertainty |
|---|---|---|
| Recovered | An available authoritative instruction is cited exactly, in the registered active scope and outside exceptions. | Its SQL implementation may be wrong. A correct quotation is not semantic validation. |
| Conditionally invariant | Every represented query executes to the same acceptable-format table. | Missing or misinterpreted alternatives can invalidate its relevance to the user. |
| Escalate | Results differ, a coverage safeguard fails, or an explicit meaning choice remains. | This supports asking; it is not proof that further machine work could never resolve the issue. |
| Unfinished | No affordable answer/check, failed execution, or unresolved response. | The goal remains counted; the system does not manufacture completion. |

The empirical output contract preserves duplicate row multiplicity, column order,
width, NULL and exact normalized values. Requested sorting is inferred from public
text before generation using the frozen repair regex. Ordered results preserve
row order. This detector is finite and could miss unfamiliar phrasing; it is not
an unrestricted semantic parser. Column aliases are ignored. No fuzzy numeric
comparison is used. A result table is the artifact; a reusable SQL program would
require a different validation contract.

Two zero-row guesses cannot justify generated-candidate release. However, COUNT
returns one row even when no record matches. The post-freeze adversarial test
`test_aggregate_zero_is_not_an_empty_result_certificate` preserves this failure:
two equally restrictive COUNT queries can produce a misleading certificate. No
policy was retuned after finding it.

A certificate cache key includes the request, schema, snapshot, source records,
scope, exceptions, version, decision dependency, output contract and candidates.
Any change to a registered field invalidates the key. An answer affects only
matching registered dependencies. The online desk rejects stale displayed
questions and permits a new question after a relevant revision without restoring
spent budget. These invariants cover represented dependencies, not unregistered
semantic relationships.

Question and execution counters enforce pathwise limits by charging before an
operation. Unresolved replies and failed queries consume their respective units.
The UI counts a scope restriction separately from its intent answer. Model calls
have a separate session ledger, one retry, context limit and inference cutoff.
The primary controlled comparison shares all model outputs across methods. The
extra candidate pass is real preparation cost, even when a replay never uses it.

One inspection uses at most six candidate executions per task. Answered SQL is
executed separately. In the frozen controller a failed answer can execute again
on later inspection; all such executions are charged and counted. The online
wrapper caches an unchanged failed answer to avoid that repeated work. The implementation caps each query at 100,000 VM
instructions and 500 rows. These limits bound demand but do not guarantee useful
completion. With M exhausted, tasks remain unfinished. A simpler deployment that
asks immediately could avoid some candidate-generation/checking work; our matched
backend deliberately holds that work constant for the mechanism comparison.

We report question demand, matching tables, mismatched releases, unfinished goals
and machine cost separately. The descriptive loss 4*mismatches + unfinished is a
constructed dimensionless score. Weight sensitivity rescoring uses 1, 2, 4 and 8;
it does not simulate a new utility-optimized policy. No noninferiority or mental
workload claim is inferred from a wide confidence interval.

Source-record versions are provenance, not automatically comparable to artifact
revision numbers. An instruction can remain active after a data snapshot changes.
The caller must explicitly replace or revoke a superseded source record; changed
text invalidates its earlier quotation hash. The controller does not infer that a
newer unrelated conversation turn revokes an otherwise applicable instruction.

## Current online source-integrity guard

The frozen terminal protocol checked query execution but did not gate on recorded
foreign-key violations. The online ValidatedController now checks quick_check and
foreign_key_check before candidate execution, charges the checks and caches their
snapshot dependency. A load or integrity failure leaves the affected goals
unfinished, never as an equality certificate. Uniform quarantine of four source
databases is reported as post hoc saved-output sensitivity. Frozen rows remain
unchanged; it is not presented as a fresh guarded evaluation.
