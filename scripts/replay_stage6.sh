#!/usr/bin/env bash
# Deterministic saved-output reconstruction. Never starts a model server.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/verify_robustness.py
python3 scripts/analyze_robustness.py fresh
python3 scripts/analyze_robustness.py post_hoc_stage5
python3 scripts/robustness_diagnostics.py
python3 scripts/plot_robustness.py
python3 scripts/robustness_traces.py
python3 scripts/render_robustness_paper.py
bash paper/build.sh
python3 scripts/verify_manuscript.py
