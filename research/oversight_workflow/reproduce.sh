#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 -m unittest discover -s research/oversight_workflow/tests -q
python3 -m research.oversight_workflow.analyze > /tmp/oversight-saved-analysis.log
python3 -m research.oversight_workflow.figures
python3 -m research.oversight_workflow.report
printf '%s\n' 'Saved-output tables, figures, 144 scenario traces and browser/live journals verified. No inference performed.'
