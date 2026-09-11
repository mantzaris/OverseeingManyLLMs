#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/verify_hvac.py
python3 scripts/reproduce_hvac_analysis.py
python3 scripts/plot_hvac_compat.py
python3 scripts/hvac_diagnostics.py
bash paper/build.sh
python3 scripts/verify_stage7_manuscript.py
