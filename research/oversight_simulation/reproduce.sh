#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 -c 'from research.oversight_simulation.run import verify_freeze; verify_freeze()'
python3 -m research.oversight_simulation.analyze
python3 -m research.oversight_simulation.plot
python3 -m research.oversight_simulation.report
if [[ "${1:-}" == "--verify-all" ]]; then
  python3 -m research.oversight_simulation.verify
fi
bash paper/oversight_simulation/build.sh
