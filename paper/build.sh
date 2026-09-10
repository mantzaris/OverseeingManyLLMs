#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export TEXINPUTS=".:./template:${TEXINPUTS:-}"
export BSTINPUTS=".:./template:${BSTINPUTS:-}"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
if [[ -f supplement.tex ]]; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex
fi
