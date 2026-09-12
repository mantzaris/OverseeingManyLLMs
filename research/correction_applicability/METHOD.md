# Scoped computation patches under a fixed inspection budget

## Problem and information boundary

An episode contains the distinct original questions attached to one TAT-QA source context. Source data S are immutable. Agent output a_j contains an answer, scale and optional generated computation r_j. Private benchmark annotations are available only through an inspection capability. Exactly two question IDs are fixed from the historical development risk estimates and the common original outputs, with source-order ties. The controller does not adapt inspection selection.

One inspection reveals only that question's answer, scale and available derivation and directly replaces that answer. It does not certify a reusable root cause or expose sibling labels. User effort is represented by two unit-cost disclosures, not measured human time. Every comparison receives the same two disclosures. Agent roles are constructed assignments to separate questions, not independent empirical units.

## Representation and proposed patches

A supported record contains source identity/hash, generated entity and metric, operation, ordered source-cell references, period bindings, units/scale and a small arithmetic expression using x0, x1, etc. Operands are read from the recorded cells. Expression length is bounded by 160 characters, eight operands and 45 AST nodes. Arithmetic permits addition, subtraction, multiplication and division; calls, attributes, arbitrary code, excessive results and division by zero are rejected. Only a small declared constant set is allowed. Dash cells are unsupported rather than silently interpreted as zero. Textual or complex questions remain in outcome accounting with no supported expression.

A generated record is a hypothesis. Valid cell IDs prove only that the cells exist. Lexical row support and year checks are necessary checks, not complete natural-language understanding. Executing a program does not certify that it answers the question.

After inspection i, one bounded model continuation attempts a computation consistent with its annotation and source. Only if that computation explains the inspected answer and passes the donor contract does the controller infer a patch from its difference to the earlier computation:

- **Fact binding:** one source dependency changes. Only an output actually using the old element is a candidate. The recipient's own periods and metric must support the replacement. The source value itself is never edited.
- **Operation or operand order:** the source dependency set remains fixed but the expression template changes. The patch can generalize across periods for the same supported question operation and metric, while preserving each recipient's own operands, units and period bindings.
- **Scale:** the computation remains fixed but its output scale changes. A candidate must use the previous scale and compatible amount metric/unit; dimensionless ratios are excluded.

Multiple unsupported changes, missing representations and unexplained annotations remain local corrections. Annotation consistency validates the donor output only. The inferred reusable scope is not a benchmark annotation.

## Commit rule and rollback

For patch c and recipient j, define

C(c,j) = dependency_match(c,j) AND supported_preconditions(c,j)
         AND executable(candidate(c,j),S) AND preserved_bindings(c,j).

Then a'_j is the independently staged candidate if C(c,j), and otherwise a_j. Every event stores original, candidate, accepted output and rejection reasons. The checked candidate answer/scale are obtained from its executable representation. Already inspected outputs are protected. A no-change candidate is logged without claiming a repair.

The predicates establish only represented dependency membership, public source/hash consistency, selected period/operation/unit constraints, bounded arithmetic validity and unchanged protected fields. They do not prove arbitrary semantic applicability, financial meaning or global safety. A source, task-contract or interpretation change requires a fresh record; old source hashes cannot silently authorize a new snapshot.

## Protocol

```
initial outputs and public representations <- common checkpoint
inspections <- fixed risk ranking(initial outputs)[:2]
for selected question i:
    feedback <- purchase annotation of i
    replace i only with its verified information
    corrected_rep <- generated source-grounded explanation of feedback
    patch <- compare(original_rep[i], corrected_rep)
    for each still-uninspected question j:
        candidate <- bounded minimal patch to rep[j]
        if scope, source, task and execution checks pass:
            commit candidate to j
        else:
            retain j and record why
```

The current method does not learn acquisition scores. It avoids attributing changes in inspection selection or extra evidence access to correction applicability.

## Controls

**Individual** directly corrects inspected questions only. **Execution only** executes common extracted representations for the four eventual never-inspected questions when the common public contract passes. **Generic verification** gives those same independently selected questions a fresh source-reading pass and executes valid representations, without sibling disclosures. It is independently runnable without correction-derived recipient membership. **Ordinary reattempt** regenerates uninspected siblings at each step without corrective information. **Coarse transfer** uses the same broad recipient schedule, but includes acquired same-context annotations. It is the historical coarse-memory mechanism adapted to the common structured interface, not the previous adaptive acquisition policy. **Constrained patch** applies the new protocol. **No applicability** uses the exact same acquired donor reconstructions and candidate patch types but bypasses recipient-semantic checks; execution and source-version constraints remain.

All initial answers and the two inspection IDs are common. Initial representations are common and available to all methods. Methods may use fewer calls; none is forced to waste computation for equal totals. Reattempt and coarse transfer receive fresh continuations because their prompts differ. Only exactly identical serialized requests with matching seeds and settings may share cache entries. Donor reconstructions can be shared between patch and its ablation because their inputs are identical.

## Structural properties and complexity

For B inspections, n questions and expression bound K, no more than B donor reconstructions and O(B n K) bounded checks are needed for constrained patching. Immutable source hashes cost O(|S|) per explicit check in the simple implementation. Broad regeneration needs at most B(n-1) recipient calls. The transport separately enforces request/attempt ceilings, one retry and the stage cutoff.

**Preservation.** `apply_to_state` deep-copies the state and writes only recipients whose candidate has passed all checks. It skips inspected IDs. Therefore all rejected recipients and all protected inspected outputs are byte-equivalent in represented answer state, and S is unchanged. For an operation patch, its original recipient reference set is preserved by construction. For a fact-binding patch, only occurrences of the declared old reference are replaced. These follow directly from the permitted assignments, not from an assumption that the LLM follows instructions.

**Budget.** The inspection capability increments its counter before returning the selected disclosure and rejects a third call under budget two. No recipient evaluation label is requested outside this capability. Changing uninspected hidden annotations while retaining the purchased responses leaves online generation requests and state transitions unchanged; this is tested.

These properties establish a protocol boundary, not semantic correctness of the generated dependencies. They are established software principles used here to test a specific empirical correction-reuse claim.

## Outcomes and inference

Report official answer EM/F1, exact scale, joint correctness, whole-context success, unfinished outputs, expression/contract coverage, accepted/rejected revisions, final never-inspected repairs minus harms, and generation cost separately. A telescoping identity checks initial EM + direct inspection gains + helpful revision events - harmful revision events = final EM. Repeated events do not inflate final distinct-answer repair counts.

Development comparisons remain exploratory. If the gate supports held-out evaluation, the freeze uses context-paired differences with replicas averaged before 2000 bootstrap resamples, seed 92112. No equivalence or noninferiority claim follows from nonsignificance. Missing report identifiers limit independence even after exact evidence deduplication.
