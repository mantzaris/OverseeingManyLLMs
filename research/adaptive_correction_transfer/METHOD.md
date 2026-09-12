# Adaptive acquisition and correction transfer

The intervention is an idealized, question-specific annotation disclosure followed by fallible model continuations. The algorithm selects which answer to inspect and whether to regenerate other answers. It does not certify that shared evidence implies a shared error.

## State and boundary

One episode contains the existing distinct questions in one TAT-QA context. Each question is assigned to an answer-producing agent role; these roles share a source but have separate prompts. This operationalizes oversight of multiple outputs and does not establish an architectural advantage over one orchestrator.

Public state contains the original question wording, rendered table and paragraphs, generated answer and scale, generated evidence references, operation, and acquired correction history. The private evaluator holds annotations. An inspection costs one response unit and discloses only the inspected question's answer, scale, derivation, and answer type. It replaces that answer directly. Annotation supervision is an ideal reference, not observed human or model review.

A correction is scoped to its source context and original question. Reuse is explicitly an inference. Each recipient is asked to independently solve its own question using the source and the acquired correction. A correct numerical answer need not establish a shared root cause. No sibling annotation or gold recipient list is disclosed. Already inspected answers are protected from subsequent transfer.

## Small transition model

Let e_j denote estimated initial answer error, f_r the probability that regeneration repairs an incorrect answer, and h_r the probability that regeneration damages a correct answer. Relation r is computed from generated evidence overlap, public question similarity, and generated operation. Exact evidence or table-row overlap takes precedence over lexical similarity >= 0.2, followed by same-context membership. These are noisy features, not applicability labels.

Development counts initialize Beta-smoothed error and transition estimates. Operation-specific risk and relation-specific fix/harm rates receive four virtual pooled observations. Conditional co-error rates use development question pairs. Related pairs are not independent empirical observations; the resulting probabilities are heuristic estimates rather than calibrated uncertainty bounds.

The predicted net transfer benefit is g(j,r) = e_j f_r - (1-e_j) h_r - 0.01. The last term is a declared dimensionless machine-cost preference, not money or measured mental effort. Applicability and conditional repair competence are not separately identifiable from these data. The protocol therefore estimates their observable combined effect and reports this limitation.

For each possible inspection i, its acquisition score is estimated current error plus the positive gains of at most three eligible uninspected recipients. This acquisition heuristic assumes that a disclosed example can aid a recipient even when the donor was already correct. It is not an exact value-of-information calculation. Recipient regeneration stops when no estimated positive gain remains. Inspection continues to the fixed budget, since direct verified correction has positive estimated benefit.

## Sequential protocol

1. Rank available inspections using the current model and public outputs.
2. With probability 0.05 choose uniformly among available questions, otherwise select the highest score. Log the realized selection probability. Deterministic ties use source question order and ID.
3. Purchase one disclosure and replace that question only with verified information.
4. Update error statistics using its original proposal. If this question was previously regenerated, compare its saved before/after states against this newly acquired annotation and update fix/harm counts. Labels of uninspected siblings never update the model.
5. Update paired-error counts only for pairs whose two questions have now been inspected. Recompute recipient gains, regenerate at most three positive-gain recipients, and retain their actual results.
6. Replan the next inspection. Stop at the declared budget.

A syntactically invalid regeneration retains the prior answer and records the failed proposal. A syntactically valid wrong regeneration is accepted and counted as harm. This guard establishes format compatibility only. It does not use an evaluator to rescue an incorrect answer.

Learning resets to the same development initialization in each episode. Evaluation labels never refit initialization. Randomized acquisition improves action support modestly but the study does not claim unbiased population transfer estimates from two selectively observed inspections. No regret or confidence-bound guarantee is claimed.

## Comparisons

- **Individual:** same fixed initial acquisition ranking, direct correction only.
- **Risk-only individual:** a strong simpler selector ranking development error risk without a hypothetical transfer bonus.
- **Context memory:** same fixed inspections; every uninspected sibling is regenerated with all acquired same-context corrections.
- **Source rule:** same fixed inspections; at most three recipients selected by initial evidence overlap, or lexical similarity with matching operation.
- **Reattempt:** same inspected questions and fixed recipient list as Source rule; regeneration receives no correction. It still receives the complete source.
- **Fixed acquisition:** same adaptive recipient model and purchased-feedback updates as the proposed method, but inspection order fixed from the initial state.
- **Adaptive:** recomputes inspection choices and updates its model from purchased feedback.
- **Frozen model diagnostic:** replans acquisition and conditions on acquired observations, but disables parameter updates.

All controlled methods have identical source access, parser, feedback, sampling settings, and release guards. Context memory has a larger recipient set; actual consumption and common ceilings are both reported. Budget-0/1 outcomes are prefixes of the budget-independent policy. Larger-budget prefixes reuse requests only when the full serialized request, seed, and call identity match.

## Properties and limits

Each inspection checks and increments a budget counter before revealing anything, giving pathwise adherence. No more than B(n-1) regeneration calls are allowed; the selective methods additionally cap each step at three. Ranking costs O(B n^2), with n <= 8; model generations dominate cost. Scope isolation is structural at context boundaries, while within-context applicability is uncertain. Changing an unasked hidden answer cannot change an online action when acquired disclosures are held fixed; a dedicated test checks this.

The protocol extends correlated audit allocation and feedback-memory systems by jointly tracking harmful and beneficial regeneration with labels restricted to purchased inspections. Bayesian acquisition, bandits, shared memory, and correction rules are established. The discriminating evidence must be improvement over fixed acquisition with the same transfer mechanism, not merely a gain from direct annotation replacement or an extra generation.

## Pseudocode and interpretation of learning

```
model <- development initialization
answers <- common generated checkpoint
for step in 1..inspection_budget:
    estimate current error and candidate transfer gains from public state
    choose an uninspected output with the declared epsilon mixture
    feedback <- purchase only that output's annotation
    if output was previously regenerated:
        score its saved transitions against this purchased feedback
        update the corresponding repair/harm counts
    update original-error and fully inspected pair counts
    replace this inspected answer with verified information
    select recipients under the current method's rule and remaining call cap
    for each recipient:
        generate a fresh answer from source + acquired scoped feedback
        accept only a structurally valid proposal; retain every attempt
```

At a two-inspection budget, the first disclosure can change the second acquisition through estimated error and co-error. A measured transfer transition is available only if the second inspection purchases a regenerated recipient's label. Such a transition can affect second-step transfer, but cannot retrospectively choose the second inspection. The three-inspection diagnostic permits that feedback to influence a later acquisition. This distinction limits what can be claimed about within-episode learning.

The donor and recipient share a context by construction, but their correctness events are not assumed independent. Conditional error features and transition histories represent some dependence. The additive acquisition score still approximates joint utility and can waste regeneration on a task later inspected directly. The study measures that cost rather than proving an optimal plan.

## Testable claim and falsification

The strongest protocol claim is observational: at the same paid-feedback boundary, adaptive acquisition should increase final correctness compared with fixed acquisition using the same recipient model. A second necessary practical check is whether it beats risk-ranked individual correction at reasonable additional computation. Lower recipient counts alone do not demonstrate greater correctness or reduced experienced workload. If the former comparison ties and the simpler individual method remains competitive, the current adaptive policy should remain a research baseline rather than the paper's central algorithmic contribution.

Output completeness is distinct from benchmark answer correctness. The guard validates answer shape, the scale vocabulary and any explicit arithmetic expression. Missing citations or derivations do not discard an otherwise parseable answer. Their absence is logged and reported as incomplete compliance with the requested output fields. Existing cell IDs are not proof of evidential support, and there is no private gold-evidence guard.

Adaptive and fixed acquisition have identical first-inspection choices and initial recipient rules. Their fresh identical requests can nevertheless produce different model answers. Budget-one differences between those two policies are therefore generation variation, not an acquisition advantage. The second step is the first opportunity for their acquisition rules to differ. Both raw answer/scale variation and changes in official correctness are measured for identical requests.

For matched feedback comparisons, the correction packet's `previous` field is the common initial checkpoint, not necessarily the most recent regenerated draft. The inspected annotation is the same under all fixed-inspection methods. The immediately preceding answer is separately retained as `current_before` and used for local-gain and purchased-transition scoring.
