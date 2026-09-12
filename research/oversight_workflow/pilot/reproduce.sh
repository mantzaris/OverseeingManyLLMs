#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
python3 -m research.oversight_workflow.pilot.verify
python3 -m research.oversight_workflow.pilot.audit > /tmp/oversight-pilot-audit-reproduction.log
python3 -m unittest discover -s research/oversight_workflow/pilot/tests -v
python3 -m unittest discover -s research/oversight_workflow/tests -v
python3 -m research.oversight_workflow.pilot.analysis \
  artifacts/oversight_workflow/pilot_preparation/test_data/complete_fixture.pilot.json \
  --kind software_fixture --out /tmp/oversight-pilot-reproduced-analysis
