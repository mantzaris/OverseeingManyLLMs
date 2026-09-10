# Reproducing the robustness evidence and manuscript

The current submission draft is [main.pdf](main.pdf), built from [main.tex](main.tex). The verified main manuscript is nine pages; the supplement is ten. The [supplement](supplement.pdf) contains source cases, full outcome/resource tables, paired comparisons and audit details. The official unmodified ICAART 2027 template is in [template/](template/); [requirements](ICAART_REQUIREMENTS.md) distinguish review rules from accepted-paper page allowances. Neither PDF has been submitted or published.

## Saved-output path from a clean checkout

Run from the repository root with Python 3.8 or later. Simulation/replay uses the standard library; figure code uses the versions in `requirements-analysis.txt`. Install those dependencies in a local environment if needed. Building requires `latexmk`, `pdflatex`, BibTeX and the standard LaTeX font/science packages used by the official template. The verified local build uses TeX Live 2019/Debian. No model, GPU, token, paid service or SSH connection is required for saved-data reproduction.

```bash
python3 -m venv .analysis-env
. .analysis-env/bin/activate
pip install -r requirements-analysis.txt
bash scripts/replay_stage6.sh
```

If dependencies are already installed, only the final command is needed. It verifies the frozen declaration, source snapshots, account exclusions, attempt ledger, model placement records and server counters. It reconstructs every fresh and post hoc policy trace, checks historical reference equality, regenerates CSVs/figures/examples, and builds both PDFs. The final PDF audit runs after the build. Timing fields retain the original measurement and are excluded from deterministic trace equality. Bootstrap draws use the frozen seed 20260916 and 2,000 resamples. Generated tables and numerical figures come from saved outputs, not a new estimator fit.

The explicit commands are:

```bash
python3 -m unittest discover -s tests -p test_robustness.py -v
python3 scripts/verify_robustness.py
python3 scripts/analyze_robustness.py fresh
python3 scripts/analyze_robustness.py post_hoc_stage5
python3 scripts/robustness_diagnostics.py
python3 scripts/plot_robustness.py
python3 scripts/robustness_traces.py
python3 scripts/render_robustness_paper.py
bash paper/build.sh
python3 scripts/verify_manuscript.py
```

For a read-only recheck of earlier evidence, use `python3 scripts/verify_robustness_history.py`. It relocates audit reports into the Stage 6 directory. The earliest L40S run predates embedded source snapshots, so its exact executed source is recovered from historical commit `46e70003` into a temporary directory and checked against recorded hashes. This requires the repository's historical commits. Stage 2 contributes 56 live traces and five stipulated mechanics traces; Stage 3 contributes 192 live traces and Stage 4 contributes 3,056. Eight Stage 1 GPU traces and 288 Stage 5 preparation workflows are also checked. The 1,152 historical retail policy traces are matched in the Stage 6 post hoc analysis.

## Evidence layout

- `artifacts/stage6_robustness/batches/evaluation/declaration.json`: frozen cases, bundles, generation seeds, configuration, estimator, source hashes, variants and comparisons.
- `cases.json`: all-split source audit, Stage 5 account exclusions, deterministic selection and annotated transaction checks.
- `batches/evaluation/prepared/`: all 72 workflows and 675 raw generation attempts, including unsuccessful preparations.
- `analysis/fresh/`: 864 policy traces on eight fresh bundles, outcome/paired/risk/resource tables, figures and first-qualifying examples.
- `analysis/post_hoc_stage5/`: 3,456 traces on the earlier 32 bundles. This is **post hoc sensitivity**, not fresh held-out evaluation.
- `verification.json`, `original_preparation_audit.json`, `historical_audits/`: accounting, workflow replay and historical compatibility.
- `analysis_direction_repair.json`: secondary completion win/loss labels repaired after freeze; numeric effects and primary loss unchanged. `presentation_adjustments.json` records a readable failure-label clarification only.
- `gpu_before.json`, `gpu_after.json`, `metrics_*.txt`, `setup/`, `launches/`, `worker_absence.json`, `runtime_final_original_server.json`: execution evidence and final process state.
- `sources/`: official template provenance, checked conference pages and classical scheduling metadata.

Replaying may refresh Stage 6 audit timestamps and derived files. It does not alter historical evidence or regenerate model outputs. The session accounting checkpoint is an original-time record, separate from replay.

## Exact historical GPU commands

These commands document the completed run. They are **not** a request to regenerate it. The existing checkout/environment and cached weights were reused. Generation ran only between 21:37:01 and 21:57:01 UTC on 10 September 2026. Freeze commit `0fc51a9bbb5ca015650045c1c610cdc8fee27dc3` preceded the first call. The server-start script pins the full model and tokenizer revision `a09a35458c702b33eeacc393d103063234e8bc28`, BF16, one GPU, serial requests, zero CPU offload/swap, and the unchanged retail context/decoding configuration.

```bash
ssh -p 33513 root@38.80.152.248
cd /workspace/OverseeingManyLLMs-rtx6000-ada-20260910T002404Z
.venv/bin/python scripts/robustness_runtime.py start
.venv/bin/python scripts/robustness_runtime.py capture --label before
.venv/bin/python scripts/run_robustness_bounded.py
.venv/bin/python scripts/robustness_runtime.py capture --label after
.venv/bin/python scripts/robustness_runtime.py stop
```

The actual local connection reused the authenticated alias with `ssh -F /tmp/overseeing_stage2_ssh_config overseeing-development`. Its identity configuration is not committed. The preparation worker used the frozen source on the pod. Full server arguments are in `gpu_before.json` and `scripts/serve_retail_gpu.sh`. The worker is one-shot, its authorization expires, and the inference cutoff reserves 90 minutes. Later fresh regeneration requires a new explicit authorization, new evidence directory and declaration. A seed does not guarantee an identical model output.

All six policies and all operational variants use the same saved preparation in each replicate. Repeating policy comparisons therefore requires **zero** additional GPU calls. No Stage 6 placement generation, LLM user simulator, model search, retraining or new paid resource was used.

## Publication provenance

Stage 5 public evidence contains the previously disclosed redaction of unsolicited credential-like model text in auxiliary fields and subsequent prompts. Original file, request and response hashes remain; exact originals are retained on the authorized pod and in an ignored local evidence directory. Staged transactions, states, labels, token accounting and outcomes are unchanged. Public redacted requests are not claimed to be byte-identical regeneration inputs. Stage 6 required **no new redactions**, as recorded in its separate `publication_redactions.json`.
