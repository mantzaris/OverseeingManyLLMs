# Correction applicability and constrained repair

This package tests whether one purchased correction can justify changes to other answers. **The development gate failed.** Neither live version generated a supported reusable patch. Risk-ranked individual correction is the supported simpler default; this package does not establish an independently evaluated improvement.

Read [REPORT.md](REPORT.md) for results, [METHOD.md](METHOD.md) for the protocol, [DEVELOPMENT.md](DEVELOPMENT.md) for the complete failed-development record, [DATA.md](DATA.md) for provenance and [LITERATURE.md](LITERATURE.md) for the SERAC/PAL/Binder/ExpeL comparisons. The separate illustrated note is [main.pdf](../../paper/correction_applicability/main.pdf). The existing submission manuscript is unchanged.

## Reproduce without inference

From the repository root, with Python 3.8+, NumPy, SciPy and Matplotlib installed:

```bash
bash research/correction_applicability/reproduce.sh
```

This verifies all 168 completed traces against 720 exact saved requests, checks feedback/budget/scope boundaries, reruns the official scorer on selected saved annotations, reproduces descriptive paired tables and all six PDF/SVG/PNG figures, and reruns the 11 constructed mechanism cases. It does not need SSH, raw TAT-QA downloads, the model or new credentials. It does not update the historical runtime ledger. Raw model outputs and acquired disclosures live under `artifacts/correction_applicability/`; offline full annotations are stored separately and are never passed to the controller.

Figure captions and source counts are in `artifacts/correction_applicability/figures/captions.json`. `analysis_v1` and `analysis_v2` must be interpreted as two development versions on the same 12 source contexts, not independent replicas. `development_gate.json` explains why no held-out evaluation was launched.

## Run the inspection desk

```bash
python3 -m research.correction_applicability.prototype.server --port 9035
```

Open http://127.0.0.1:9035. Select **Group 6** and **Constrained correction**. This is the first source in fixed order with an executable donor explanation rejected by the percentage-formula check.

1. Inspect the percentage change in inventories. The recorded annotation is disclosed for that question only.
2. Expand the inferred patch and source evidence. The explanation does not support a reusable correction, so unrelated answers remain intact.
3. Inspect the remaining selected question. The interface refuses a third inspection and retains unresolved sibling answers.
4. Compare **Coarse transfer** or **Ordinary reattempt** on the identical starting answers and inspected questions. Group 1 shows percentage-scale changes; these are improvements of a simpler control, not successful constrained patches.

This is a saved-output replay with simulated annotation feedback, not a live human study. To record demonstration interactions, add `--log /tmp/correction-desk-demo.jsonl`. Source details, candidate computations and exact rejection reasons remain inspectable. Scripted browser checks and desktop/mobile screenshots are saved under `artifacts/correction_applicability/interface/`.

## Small adapter

The online core takes public source/question data, generated output records and the purchased donor disclosure. It has no all-answer scoring argument:

```python
from research.correction_applicability.backend import load
engine = load('v2_guarded')
patch = engine.infer(context, inspected_question, old_output,
                     corrected_output, purchased_disclosure)
next_outputs, events = engine.apply_to_state(
    context, context['questions'], current_outputs, patch, inspected_ids)
```

`corrected_output` is generated from the inspected question's annotation, not its siblings' answers. `events` retains before, candidate, accepted output and rejection reasons. Source mutation, failed execution and missing bindings reject a candidate without replacing the old answer. `representation_v2.parse` accepts the small model schema documented in its system prompt. This is a bounded implementation, with the semantic limitations stated in METHOD.md.

HTTP adapter: `GET /api/catalog`, `POST /api/open` with `{"index":5,"method":"patch"}`, then `POST /api/inspect` with the returned session ID. The replay endpoint discloses only completed recorded inspections. There is no evaluator or arbitrary sibling-label API.

## Model collection and accounting

The exact executed commands were:

```bash
python3 -m research.correction_applicability.experiment --revision v1
python3 -m research.correction_applicability.experiment --revision v2
```

They used the already running pinned Qwen2.5-7B BF16 server on the RTX 6000 Ada. The separately recorded authorization and cutoff are in `authorization.json`; they must not be reset to repeat inference. The source manifest and original initial outputs, versioned prompts, seeds, requests, responses and preflight rejections are retained. Regeneration is stochastic even with matching seeds; saved-output replay is deterministic. New collection after the cutoff requires a separately authorized stage, not an edit to historical clocks.

The optional raw source audit uses the official pinned release described in DATA.md and `provenance.json`; it is not needed for saved-output reproduction. No fresh source labels were used for tuning or evaluation in this stage.

## Build the illustrated note

With `pdflatex`, `bibtex` and `pdfinfo` installed:

```bash
bash paper/correction_applicability/build.sh
```

The six scientific figures are programmatically generated. The positive patch and rejected wrong-period examples are explicitly constructed diagnostics. There was no naturally committed patch to illustrate as empirical success.
