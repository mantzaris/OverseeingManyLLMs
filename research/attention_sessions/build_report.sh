#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
pandoc research/attention_sessions/REPORT.md \
  --resource-path=research/attention_sessions \
  --pdf-engine=pdflatex -V geometry:margin=0.7in -V fontsize=10pt \
  -V colorlinks=true -V urlcolor=blue \
  -o research/attention_sessions/REPORT.pdf
