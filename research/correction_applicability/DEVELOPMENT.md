# Development record

All observations in this file use previously inspected material or the twelve predeclared training contexts. They cannot establish fresh evaluation performance.

## Historical audit

`historical_audit.json` retains the first three helpful, harmful and score-tied adaptive transfers in the preceding frozen source order, then replica, inspection and recipient order. These nine traces come from six source contexts, with several related events; they are not nine independent error studies. Source and full before/after derivations are preserved.

- Helpful changes include reversed operands, removal of extraneous operands from an answer list, and correcting Level 2 to Level 1 column selection. None alone proves that acquired feedback was necessary.
- Harm includes copying the wrong-period variance (245 rather than the requested 273), changing percentage change into a ratio, and an unexplained 0.9-to-1.0 change. The last case is retained as unresolved rounding/extraction/generation failure.
- Score ties include unchanged wrong aggregation, changed but still wrong aggregation/column selection, and formatting-only regeneration of an already correct unrelated answer. A score tie is not necessarily identical output.

These observations motivate separate execution, independent verification and ordinary reattempt controls. Coarse row overlap cannot certify period or operation applicability.

## First working version

v1 uses existing v4 initial answers from all twelve predeclared training contexts. Fresh Qwen calls extract a bounded representation while preserving the old answer. Two fixed risk-ranked questions are inspected in every method. Their acquired annotations may prompt source-supported donor reconstructions. Differences between old and reconstructed computations produce local fact-binding, operation or scale patches. No gold sibling information enters patch selection or acceptance.

Operation patches may generalize across periods while preserving the recipient's own source cells and supported question operation. Fact-binding patches require an actual dependency on the changed element and must pass recipient-period checks. Failed or ambiguous candidates roll back. Exact entity matching and weak lexical metric support are conservative hypotheses, not annotated applicability.

The common execution-only baseline executes extracted expressions. Generic verification independently rereads the source for each question not scheduled for inspection. Coarse correction and ordinary reattempt perform comparable serial recipient generations, retaining valid wrong responses. No-applicability uses the same generated donor reconstruction but bypasses semantic recipient eligibility, retaining the source-version/execution boundary. All generation and parse failures are retained.

The first source snapshot is `development_v1_source.json`. There may be at most two diagnosed refinements. The gate is assessed only after all twelve contexts complete; interim throughput checks do not change selection.
