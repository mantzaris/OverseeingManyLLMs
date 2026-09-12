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

## Refinement 1 prepared from diagnosed interface failures

During the complete v1 pilot, valid-looking records repeatedly used cell IDs as metric names, units as scales, and full dates where the contract expected years. A metadata-only diagnostic on the first 60 available v1 extractions recovered 11 passing public contracts, versus none under v1, without using answer labels. The full twelve-context gate assessment is still required before the next generation batch.

The v2 refinement shortens the shared model output to operation, references, expression and scale. Entity is explicitly a source-context anchor, not a recovered company identity. Row/section labels and explicit year bindings are read from the selected cells' public table metadata, and remain fallible evidence of semantic applicability. This removes unnecessary generated field-name failures equally for every method. Public percentage/unit and question-period checks remain active. Model calls use smaller draft payloads to reduce context failures.

The same refinement checks relative operand-year roles before transporting an operation template, refreshes derived metadata after a fact-binding change while keeping the recipient question fixed, and keeps a correction local when the prior computation already explains the acquired annotation. It does not introduce gold applicability labels or change acquisition. v1 code and results remain replayable through their saved source snapshot. No new task selection is used.


### Completed v1 decision

All 84 policy traces completed on all twelve contexts and 72 questions. Individual correction: 41/72 EM, ordinary reattempt: 42/72, coarse transfer: 44/72. Execution, generic verification and constrained patch each scored 41/72. Thirty initial representations executed, but zero passed the full contract; no patch committed. This fails the evaluation gate. It is a representation/contract failure, not evidence that a zero-revision policy solved correction transfer.

Proceed only to the uniform v2 development refinement described above. The generic source-verification control also permits exact nonnumeric spans within its generated cited evidence; mere source support is not certified question relevance. It receives no sibling feedback. The v2 donor test keeps already explained computations local rather than calling a generic arithmetic repair correction-dependent. All methods retain the same original answers, fixed inspection choices and source cases.


### Structural repair during v2 collection

A controlled malformed-record test exposed `KeyError('metric')` when a partial computation happened to execute but lacked required binding fields. The guard now rejects incomplete donor/recipient schemas before inspecting those fields. The first ten completed v2 traces replayed identically after the repair; no existing outcome was altered and no new model prompt was introduced. The original v2 snapshot and this repair snapshot are both retained. This is the second and final bounded implementation refinement; no further semantic tuning is planned.

### Final gate and retained versions

All 84 v2 traces completed. Individual, execution, source verification, patch and no-applicability each scored 41/72 EM. Ordinary reattempt scored 37/72; coarse transfer scored 43/72. Only 8/72 initial representations executed and 1/72 passed the public contract, compared with 30 and 0 in v1. Of 24 acquired donor reconstructions, 19 lacked a complete earlier or revised record; the other five failed period, percentage-formula or numeric-cell checks. There were zero supported patches and zero commits.

**The gate failed. No fresh evaluation was frozen or generated.** The source audit found 223 unused technically eligible test contexts, but source availability is not evidence that the mechanism works. We did not expand, narrow to favorable cases, or begin another acquisition policy. The completed result is a development diagnostic, not the intended independently evaluated improvement.

The original v2 worker retained its loaded code throughout collection. Full replay subsequently found two patch/ablation records in context 9 whose rejection reasons differ under the later schema guard, although every final answer, snapshot and generation request is identical. `backend.py` now replays v1 and v2 using their original patch source snapshots. `v2_guarded` is the repaired API, audited separately in `verification.json`; it is not silently substituted for historical event records.

The full metadata-only reanalysis of v1 finds 12/72 passing public contracts if the same generated cells are given source-derived metadata. This post hoc diagnostic is not a third live implementation trial. It shows that contract formatting contributed to rejection, while the shortened v2 model interface generated fewer usable hypotheses. All raw requests remain available to investigate that failure.

### Score-change diagnosis and limits

Every final never-inspected gain from coarse transfer was a scale-only change in development context 0: four answers in v1 and two in v2. The table already labels all three year columns with `%`. Thus a more competent source-unit reader is the nearest explanation; these are not evidence for a reusable latent arithmetic rule. All gains were concentrated in one source context. v1 reattempt also fixed one of these scale errors without the annotation. The remaining v1 reattempt gain corrected a numeric lookup in context 9, while another numeric answer there became wrong.

The v1 coarse-transfer EM loss was an explanatory span extended with “from 2018 to 2019.” That is retained as official metric harm, but no new financial contradiction is established by the extra phrase. v2 reattempt repeated that span change, changed one correct numeric answer, and changed two correct thousand-scale answers to million. `diagnostics/final_score_changes.json` contains every changed final never-inspected score, including the unchanged numbers and changed scales.

### Constructed semantic counterexample

After the empirical gate, a boundary diagnostic tests a percentage-change template with a missing denominator. It matches a donor whose earlier value is one, passes structural checks, and damages a recipient with an earlier value of three. This was added to expose the conditional nature of the protocol, not to tune it again. Synthetic fixtures establish rollback and declared dependency properties, not natural transfer prevalence or semantic safety.
