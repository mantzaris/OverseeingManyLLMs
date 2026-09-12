# Scoped coordination with verified uptake

## Question and contribution boundary

Can selective delivery of an authorized requirement change reduce communication or improve correct adaptation compared with a global shared-state check and direct broadcast? The unit of useful work is the complete four-artifact project, not the number of agents agreeing. This is a protocol and controlled application study. Dependency invalidation, message routing, versioning and feedback repair are established mechanisms. The testable addition is their explicit integration with scoped user changes, executable artifact checks, bounded propagation and an unaffected-work invariant. An empirical advance requires beating competent simpler implementations on the correctness-cost tradeoff. A deterministic parameterized pipeline is a particularly strong competing explanation.

## State and authority

Let the registered acyclic graph G=(A,E) contain the analysis, chart, report and appendix responsibilities. Edges are analysis -> chart -> report. The appendix has its own scope and no incoming edges. A user instruction is U=(source,version,scope,exceptions,fields). Only the authorized application boundary can install U. A peer may forward that immutable instruction along a registered edge, but cannot alter its scope, exceptions, source or version.

For agent i, state X_i contains the resolved applicable contract C_i, a proposed tool plan, consumed-contract hash, artifact revision, hashes of consumed dependencies, executable evidence, acceptance and unresolved issues. Scope resolution is explicit and authored here. It is not inferred reliably from arbitrary language. For a main-report change, the appendix keeps its original contract and version. An analysis-only formatting field is excluded from contracts that do not consume it. The controller handles one change at a time and rejects unsupported graphs and cycles.

A packet P_i contains the authorized source and change, current resolved requirements, recipient responsibility, observable issues, permitted forward recipients and delivery provenance. Inputs from data files and peer artifacts remain evidence. The same packet constructor is used by broadcast, targeted and sparse routing. A shared-state baseline receives the same resolved requirements and checks, plus the full current project state. No method is denied the update.

## Observable verification and private evaluation

The public guard checks selected query parameters against the applicable contract, runs the generated query on the read-only transaction snapshot and authored public sentinel rows, checks chart selection and units against the actual accepted table, and computes report claims from the actual accepted chart. It also checks dependency hashes and rejects results derived from unaccepted parents. An acknowledgment or `keep` cannot update a stale dependency or instruction hash. Incorrect proposals remain in the trace even if the guard blocks their release.

The final constrained interface is a legitimate application tool, not unrestricted SQL generation. An LLM selects every query field. A deterministic compiler produces SQL from those fields. The chart agent selects a source, prefix size and unit. The reporting agent selects a source and unit and supplies explanatory text. Tools copy plotted values and perform arithmetic. The agent is still responsible for selecting current, applicable parameters and using the right parent. We separately compare a pipeline that selects all these parameters deterministically from the same public contract. This comparator needs no LLM.

The evaluator independently aggregates the real rows in Python and compares exact stock-code/value tables, chart points and structured report claims. The online controller never imports this evaluator or sees its answers. Public sentinel expectations are constructed tool tests, not withheld transaction aggregates. Finite probes alone do not prove universal query equivalence. Current snapshot equality alone does not excuse a wrong required filter. Structured numerical claims, units and source selection are evaluated; unrestricted prose and the semantics of chart titles are retained but not exhaustively graded. Accepted views use explicit contract labels to prevent free text from replacing them.

## Routing and bounded feedback loop

All methods have two reconciliation rounds and at most two calls per role, eight logical generation calls per continuation. Each ordinary generation allows at most one transport retry. A role can run only when its registered parents are accepted. Each call executes the returned tool plan and rechecks the graph. Nothing silently disappears on failure.

1. Install the single authorized change and resolve each role's contract.
2. Inspect all current artifacts. Retain the invalid artifacts as unfinished work.
3. Choose recipients using one of the rules below.
4. In topological order, send the role-specific packet to an eligible recipient, generate its actual continuation, execute its tool plan and check uptake.
5. In the second round, inspect all roles and expand to every remaining invalid role, subject to the common per-role cap.
6. Stop when all artifacts pass or the cap is reached. Report unresolved work. No extra user question is simulated in these fully specified briefs.

| Rule | First-round delivery | Later reconciliation |
|---|---|---|
| Shared state/global check | Inspect every role, call only invalid roles; expose current shared state | Call remaining invalid roles |
| Direct broadcast | Deliver the same scoped packet to every role, including the protected appendix; allow valid `keep` | Same global check |
| Targeted injections | Deliver to roles whose resolved contract changed | Expand to remaining invalid roles |
| Sparse propagation | Deliver to roots of the affected subgraph; model can notify immediate registered dependents | Global fallback for missing or failed propagation |
| Targeted without feedback | Same routing and checks as targeted; omit the observable-issue list from the prompt | Same caps and acceptance guard |
| Parameterized pipeline | Select the correct tool parameters directly from the public contract | Topological invalidation, no model calls |

The no-feedback condition retains the allowed-action guard and current instructions. It removes detailed repair explanations, not all information about failure. Broadcast versus targeted isolates routing with an identical packet constructor. The global baseline differs in presentation as well as routing, so its comparison cannot isolate packet wording. Sparse propagation is model-selected notification inside a deterministic trust boundary, not decentralized consensus.

## Costs and error

For the four required artifacts, R is the number whose proposed result violates the applicable executable contract or differs from the private numerical reference. D counts invalid or stale dependency checks, at most four checks for the two edges. F is the number of required artifacts not accepted. Define V=R/4 + min(D,4)/4 + F/4, in [0,3]. Each component is reported separately. A missing artifact contributes to R and F. All-abstention cannot win. An online analogue uses public contract checks without the private numerical comparison. V is an authored diagnostic score, not financial loss or human workload. Full project correctness requires all four required artifacts accepted and numerically correct.

Report accepted wrong artifacts, raw snapshot matches, correct accepted artifacts, unfinished work, preservation of the appendix, modifications to any unaffected artifact, repair rounds, direct and forwarded messages, logical calls, attempts, input/output tokens, public probes, database executions and elapsed time. A tool or guard improvement is attributed to that component. The primary evidence is correctness and resource consumption, not a weighted score alone.

## Narrow properties and limits

**Bounded propagation.** A run visits four registered roles at most once in each of two rounds. Forwarding only adds an immediate dependent that has not yet been called in that round. Therefore there are at most eight calls, including unsuccessful calls. With one retry, at most sixteen generation attempts occur per continuation. The separate session ledger can impose a stricter cutoff. Cyclic graphs are rejected rather than assumed to converge.

**Scope confinement.** The controller resolves and sends C_i from authorized state; peer `notify` can only name a registered child. The appendix's contract is invariant under the supported project constructor and validated main-scope API; arbitrary dictionaries passed directly to the internal experiment runner are outside that guarantee. This establishes message authority and represented-scope preservation, not that an LLM complies. Actual outputs must still pass the guard.

**Dependency freshness.** Acceptance requires current parent hashes and accepted parents. If the parent artifact changes, an unchanged child is invalidated. A `keep` returns the old artifact with its old hashes, so it cannot falsely certify uptake. Timing metadata is excluded from identity. Content, query parameters and dependency hashes are not.

No contraction guarantee is claimed for LLM repairs. V can increase after a bad continuation; unchanged requirements and natural completion can also reduce V. Matched policy-specific continuations and the deterministic comparator test whether injections add value. The four roles share one pinned model, not independent expertise. No inference about human attention, experienced workload or organizational deployment follows from message counts.

### Interpretation of the stress rewrite count

The frozen score field named `unnecessary_modifications` counts identity changes to contract-unaffected artifacts. In the ordinary condition all original artifacts were valid, so this measures avoidable rewriting. In the exception-corruption stress condition, restoring the appendix is necessary even though its contract did not change. Stress analyses therefore call the same count **unaffected-artifact rewrites**, not unnecessary repairs. The raw score is preserved; the interpretation is narrowed rather than assigning success to leaving corruption untouched.

## Post-study routing-equivalence audit

For the ordinary declared inputs, targeted routing and the matched packet-format global check are the same decision rule up to an extra repeated inspection call. Initially every artifact passes. A main contract change affects exactly the main dependency closure because each child contract contains all its parent's reporting fields. A display-prefix change affects exactly chart and report. Therefore the roles with changed contracts are exactly those that the global check invalidates. Both methods then visit those roles in the same order, send the same packet, and use the same global fallback. With equal observed histories their next request is identical. Fresh generation can still vary, so unequal sampled outcomes would not establish distinct policy value.

The compatible-parser follow-up verifies identical request sequences for all sixteen targeted/global-packet project pairs. The original global-state baseline differs in presentation, and active broadcast differs in whether already valid recipients must process a notification. Thus the study supports a software protocol and diagnoses information-delivery/interface costs, but cannot establish a new recipient-selection algorithm on this workload. The few extra public checks in the global implementation are redundant inspections, not a fundamental complexity advantage for targeted routing.
