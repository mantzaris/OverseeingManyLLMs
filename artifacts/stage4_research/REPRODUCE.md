# Reproducing saved Stage 4 results

Run these commands from the repository root. They read saved outputs and perform no model inference. Host analysis used Python 3.8, NumPy 1.22.1, and Matplotlib 3.1.2; see this directory’s `analysis_environment.json` and the repository-root `requirements-analysis.txt`.

```bash
python3 scripts/analyze_research.py --batches development_pilot objective_development --label development
python3 scripts/analyze_research.py --batches evaluation --label evaluation
python3 scripts/audit_numerical_ties.py --batches development_pilot objective_development --label development
python3 scripts/audit_numerical_ties.py --batches evaluation --label evaluation
python3 scripts/audit_objective_null.py
python3 scripts/plot_research.py
python3 scripts/research_traces.py
python3 scripts/research_tables.py
python3 scripts/audit_research_session.py
```

The analysis command audits raw requests and replays every completed trace before producing scenario-paired summaries. It uses 2,000 bootstrap resamples with fixed analysis seed 20260910. Tables use complete condition keys, including separate core and objective-extension cohorts. Matching frozen-estimator rows for the risk comparison come from the first 32 replication seeds. The final analysis contains reporting fixes made after the execution snapshot was frozen; these do not modify any saved trajectory.

An individual compressed trace can also be replayed:

```bash
python3 -m overseeing replay artifacts/stage4_research/batches/evaluation/episodes/replication/original/10000/a3/s2/frozen/delay/lambda0/events.jsonl.gz
```

## Recorded inference procedure

These commands document the procedure actually used, not permission to repeat the experiment. Existing outputs, one-shot markers, the shared ledger, and authorization deadlines prevent silently overwriting or extending this session. New inference needs a new authorization and fresh output directory. Do not delete historical markers or reset the ledger.

The existing pod connection was `ssh -p 33513 root@38.80.152.248`, using the already authenticated identity and verified host. The execution environment used its preserved SSH configuration alias `overseeing-development`. The checkout was `/workspace/OverseeingManyLLMs-rtx6000-ada-20260910T002404Z`. Its existing `.venv`, cached model and healthy server were reused. Stage 4 did not reinstall the runtime or restart the server. The original isolated setup and server launch are recorded in `reports/STAGE1_GPU_LIVE.md`; the launch uses `HF_HOME="$PWD/model-cache" bash scripts/serve_gpu.sh` with the pinned revision, BF16, one GPU, and zero CPU offloading.

Declarations were created locally, inspected, and transferred with the frozen source and authorization before their corresponding GPU calls:

```bash
python3 scripts/research_session.py prepare-diagnostics
python3 scripts/research_session.py prepare-pilot --batch development_pilot
python3 scripts/research_session.py prepare-branch --batch objective_development
python3 scripts/research_session.py prepare-evaluation --batch evaluation
```

The objective branch and evaluation were declared only after the preceding development evidence and the evaluation forecast were recorded. On the pod, the actual execution commands were:

```bash
cd /workspace/OverseeingManyLLMs-rtx6000-ada-20260910T002404Z
.venv/bin/python artifacts/stage4_research/run_bounded.py diagnostics \
  .venv/bin/python scripts/research_session.py diagnostics
.venv/bin/python artifacts/stage4_research/run_bounded.py development_pilot \
  .venv/bin/python scripts/research_session.py run-batch --batch development_pilot
.venv/bin/python artifacts/stage4_research/run_bounded.py objective_development \
  .venv/bin/python scripts/research_session.py run-batch --batch objective_development
.venv/bin/python artifacts/stage4_research/run_bounded.py evaluation \
  .venv/bin/python scripts/research_session.py run-batch --batch evaluation
```

The default validated server PID was 7338, with log `artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/server.log`. `launches/*/launch.json` records exact commands and wall clocks. The wrapper terminates experimental process groups at the inference cutoff and leaves the serving process intact. `batches/*/declaration.json` records ordered runs, scenario/source/configuration hashes, call limits and estimator hash. `source/` inside each batch preserves its executed project source.

Fresh generation uses the declared seeds and decoding settings but is not guaranteed to return identical actions. Deterministic replay of saved outputs is the reproducibility guarantee verified here. No command above pushes to a remote Git repository.
