#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 -m unittest research.adaptive_correction_transfer.tests research.adaptive_correction_transfer.test_replay -q
python3 -m research.adaptive_correction_transfer.freeze --verify
python3 -m research.adaptive_correction_transfer.replay
python3 -m research.adaptive_correction_transfer.audit_integrity
python3 -m research.adaptive_correction_transfer.results
python3 -m research.adaptive_correction_transfer.mechanisms
python3 -m research.adaptive_correction_transfer.synthetic
PYTHONWARNINGS=ignore python3 -m research.adaptive_correction_transfer.plot
