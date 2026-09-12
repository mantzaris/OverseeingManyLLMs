# Adaptive correction transfer

Inspect one answer, obtain question-specific verified feedback, and selectively regenerate related answers. The controller models both repair and harm. A subsequent inspection can teach it whether a previous transfer helped that particular answer. It never receives unaudited sibling labels as an online reward.

This is a separately authorized exploration on TAT-QA, with a frozen comparison on 24 source contexts and two generation replicas. [REPORT.md](REPORT.md) contains the completed results and recommendation. [METHOD.md](METHOD.md) defines the protocol and comparators. The historical submission and earlier research packages remain intact.

## Reproduce saved-output evidence

From the repository root:

```bash
python3 -m pip install -r research/adaptive_correction_transfer/requirements.txt
bash research/adaptive_correction_transfer/reproduce.sh
```

The command needs no model, GPU, network, or private credentials. It verifies the declaration and recorded inspection boundary, reconstructs prompts and policy traces, computes official task metrics and paired intervals, runs the synthetic diagnostics and focused tests, and exports the figures. Selected source contexts and evaluator annotations are saved separately; the latter are used only for offline scoring. Full upstream data are not required for this path.

```bash
bash paper/adaptive_correction_transfer/build.sh
```

This optional command compiles the separate illustrated research note. It requires a local LaTeX installation. The final resource ledger is a historical record; reproduction does not reset its timestamp or claim new inference.

## Demonstrate an inspection

```bash
python3 -m research.adaptive_correction_transfer.prototype.server --port 9034
```

Open http://127.0.0.1:9034/. Select a context and policy. Inspect an answer to reveal only its benchmark feedback, then see the actual saved recipient continuations. A second inspection reveals additional information within the two-inspection limit. Source evidence, uncertain recipient relations, retained failures, and still-unverified answers remain visible. Closing or reopening a replay does not perform new generations.

The interface uses saved GPU trajectories and ideal annotation feedback. Clicking is a software demonstration, not participant evidence. It does not claim that arbitrary new user corrections have been evaluated. Logs record displayed-state hashes, UTC and monotonic times, and actions. `prototype/browser_smoke.mjs` tests the workflow and captures screenshots.

## Adapter boundary

`controller.run(context, initial_answers, parameters, inspector, generate_fn, seed, method, budget)` accepts two injected capabilities:

- `inspector.inspect(question)` returns only the selected answer, scale, derivation and provenance, and must enforce the response budget. A real user integration would replace this capability.
- `generate_fn(question, old_answer, acquired_corrections, step, reattempt)` returns a parsed proposal and usage record. `inference.request` implements the recorded GPU interface. `replay.RecordedInspector` and saved-request reconstruction implement deterministic replay without all-output annotations.

No controller API accepts the private evaluator map. Task grouping is restricted to a single context; it is not permission to copy an answer to another question. Syntactic acceptance preserves failed drafts but cannot establish semantic correctness.

## Original collection commands and provenance

```bash
python3 -m research.adaptive_correction_transfer.download
python3 -m research.adaptive_correction_transfer.pilot --revision v4 --limit 12
python3 -m research.adaptive_correction_transfer.fit
python3 -m research.adaptive_correction_transfer.collect --development
python3 -m research.adaptive_correction_transfer.freeze
# Commit the declaration before any evaluation generation.
python3 -m research.adaptive_correction_transfer.collect
```

These document the completed stage; the freeze refuses overwriting an existing declaration. Current inference authorization and immutable cutoffs are in `artifacts/adaptive_correction_transfer/authorization.json`. Reusing the old cache is replay, not a fresh replication. A future replication needs separate explicit authorization, new ledger and artifact namespace; historical authorization must not be edited.

The existing tunnel was `ssh -F /tmp/overseeing_stage2_ssh_config -N -L 8021:127.0.0.1:8000 overseeing-development`. It used the already authorized pod `root@38.80.152.248:33513`, pinned Qwen2.5-7B revision `a09a35458c702b33eeacc393d103063234e8bc28`, BF16 on RTX6000Ada, zero CPU model offload. Exact identity and serving evidence are in `gpu_initial.json`. Requests used temperature 0.3, top-p 1, 288 output tokens, a 2048-token model context, serial calls, and at most one retry. Tokenization preflight failures consume scheduled-call accounting but are not GPU generation attempts.

## Evidence map

All new artifacts are under `artifacts/adaptive_correction_transfer/`:

- `frozen/`: public selection, separately stored evaluator annotations, model/source hashes and synthetic declaration.
- `development*`, `raw/`, `attempts.jsonl`: all development versions, generated requests/responses and failures.
- `evaluation/`: common initial checkpoints and actual policy-specific continuations.
- `analysis/`: official metrics, paired context differences, transfer events, acquisition diagnostics and first-qualifying examples.
- `synthetic/`: explicitly authored mechanism boundaries, zero inference.
- `figures/`: vector PDF/SVG and PNG exports, with provenance captions.
- `interface/`: scripted screenshots and interaction records.
- `resource_ledger.json`: separate stage totals and cumulative historical accounting.

The frozen reporting code had a `scale_exact` versus `scale` field mismatch. `results.py` is the explicitly documented reporting-only repair; the frozen original, model, controller and experimental settings remain unchanged. No outcome-based redesign followed evaluation.
