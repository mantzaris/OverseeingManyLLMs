# Clarification planning

This completed experiment adds a budgeted clarification planner and a local Decision desk. Two-step planning improves on one-step selection in the frozen source-grounded comparison. A stronger completion heuristic matches its quality with fewer questions. See [REPORT.md](REPORT.md) for the result and its limits, and [the separate manuscript](../../paper/clarification_planning/main.pdf). Historical submission files and experiments are unchanged.

## Reproduce without inference

From the repository root, using Python 3.8 or newer with NumPy and Matplotlib:

```bash
python3 -m research.clarification_planning.reproduce \
  --figures --output /tmp/clarification-reproduction
```

This checks the committed freeze, reconstructs 396 exact requests and 132 preparations, replays all 44,688 policy/audit rows, compares their digests, reproduces paired statistics and diagnostic tables, and regenerates ten sets of PDF/SVG/PNG figures. It reads the saved source subset and model responses. It makes **zero GPU/API calls** and writes its output to the separate requested directory. Original timing measurements remain attached to the original run; replay timings are not substituted into published cost tables. The final verification file lists the checked row and interaction counts.

Verified environment: Python 3.8.10, NumPy 1.22.1 and Matplotlib 3.1.2. Only the analysis/plotting stack requires these packages; the controller and local server use the standard library. Exact compatible versions are recorded in `artifacts/clarification_planning/software_versions.json`. A local environment can be prepared with:

```bash
python3 -m venv /tmp/clarification-env
/tmp/clarification-env/bin/pip install numpy matplotlib
/tmp/clarification-env/bin/python -m research.clarification_planning.reproduce \
  --figures --output /tmp/clarification-reproduction
```

Byte-level numerical CSV checks are verified on the recorded environment. Different NumPy versions may change final floating-point formatting or bootstrap implementation; inspect a reported discrepancy rather than silently replacing historical tables.

## Open the working interface

```bash
python3 research/clarification_planning/prototype/server.py
```

Open `http://127.0.0.1:9031/`. The localhost server has no external services or model dependency. Stop it with Ctrl-C. It logs development interactions in `/tmp/clarification-desk-interactions.jsonl`. The interface contains an authored publishing project, not evaluator answers.

A short walkthrough:

1. Keep the two-question planner and budget two. Ask for its next question.
2. Answer the accessibility requirement with `screen_reader` for the stated project scope.
3. Ask again and choose `web` as the release format. Finish. Three distinct publishing deliverables are ready; the independent meeting and exceptional partner export remain visible and deferred.
4. Inspect the release-format record and revise it to `pdf`. The three registered releases require revalidation.
5. Start a comparison with one-step VoI and budget two. It first asks the independent partner export format, then the meeting preference. It completes two independent tasks in this authored example.
6. Start another run and answer accessibility only for `Website implementation`. The test plan and publishing guide do not silently receive that narrow answer. An unresolved response consumes an answer unit and leaves affected work deferred.

These examples establish interface and protocol behavior, not participant benefits. [API.md](API.md) includes a Python adapter, direct public task registration and the HTTP actions. Screenshots and a real scripted browser log are under `artifacts/clarification_planning/interface/`.

## Focused checks and independent source verification

```bash
python3 -m unittest \
  research.clarification_planning.test_planner \
  research.clarification_planning.test_desk \
  research.clarification_planning.test_audits -v
python3 -m research.clarification_planning.verify_source --download
bash paper/clarification_planning/build.sh
```

The source check downloads the pinned approximately 14 MB MultiWOZ archive into `/tmp/clarification-source/`, verifies its SHA-256, and compares selected dialogues, label derivation, split membership and database files. It does not overwrite source artifacts or perform inference. To use an existing archive, supply `--archive /path/to/MULTIWOZ2.4.zip` without `--download`. The MIT license and exact URLs are in the data provenance manifest. The manuscript build requires a standard TeX Live installation with `pdflatex` and `bibtex`; it changes only `paper/clarification_planning/`.

Historical regression checks were run once and saved in `historical_regression.log`: decision-dependency semantics/interface/package plus attention-session semantics/package, 41 checks. No expensive unrelated GPU audits were repeated.

## Fresh generation is a different operation

Saved replay is deterministic; GPU regeneration is not promised to be bitwise reproducible. The original collection command was:

```bash
python3 -m research.clarification_planning.collect --split evaluation
```

It used an existing authenticated tunnel at `http://127.0.0.1:8018/v1/chat/completions`, the pinned Qwen model, and this experiment's separately scoped authorization. Calls already saved are cached and are not repeated. The client enforces its recorded deadline, inference cutoff, serial request limits and at most one retry. **Do not edit this historical authorization to regenerate.** A future fresh study requires a separately authorized namespace and ledger. No key, credential, model weight or environment is stored in this package. Existing GPU server arguments and evidence are in `gpu_initial.json` and `gpu_after_generation.json`.

## Package map

| Location | Contents |
|---|---|
| `METHOD.md`, `PLAN.md`, `frozen/` artifacts | Original committed method and experiment declaration |
| `LITERATURE.md`, `NOVELTY.md` | Verified closest methods, competing explanations and final novelty limit |
| `DATA.md`, `data/` artifacts | Provenance, exposure audit, public inputs and evaluator-only targets |
| `planner.py`, `exact.py`, `safe_protocol.py` | Frozen algorithm/reference and isolated online release repair |
| `empirical.py`, `synthetic.py`, `evaluate.py` | Model-to-belief adapter, authored conditions and privileged evaluator |
| `completion_audit.py`, `repair_scope.py` | Explicitly secondary stronger comparator and isolated synthetic answer repair |
| `reproduce.py`, `plot.py`, `effort_plot.py` | Saved-output verification and numerical figures |
| `prototype/`, `adapter.py` | Local interface and integration API |
| `REPORT.md`, `CLAIM_EVIDENCE.md` | Results, limitations and claim-level artifact links |
| `paper/clarification_planning/` | Standalone draft, bibliography, build command and inspected PDF |

All new data are under `artifacts/clarification_planning/`. The interface also exposes the stronger minimum-sufficient-completion audit; it is not a newly frozen evaluation condition. Original synthetic scope rows remain preserved but are excluded from valid outcome summaries as documented in `SEMANTIC_AUDIT.md`. The stronger completion audit is not part of the preregistered primary comparisons. Its unfavorable finding is included in the report and main draft table.
