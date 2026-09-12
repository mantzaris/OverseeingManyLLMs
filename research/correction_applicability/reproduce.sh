#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 -m research.correction_applicability.replay --revision v1
python3 -m research.correction_applicability.replay --revision v2
python3 -m research.correction_applicability.analyze --revision v1
python3 -m research.correction_applicability.analyze --revision v2
python3 -m research.correction_applicability.diagnostics > /tmp/correction-applicability-diagnostics.log
python3 -m research.correction_applicability.examples
python3 -m research.correction_applicability.synthetic
python3 -m unittest research.correction_applicability.tests research.correction_applicability.test_protocol -q
python3 -m research.correction_applicability.verification
python3 -m research.correction_applicability.figures
python3 -m research.correction_applicability.report_tables
