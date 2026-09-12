#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/adaptive-correction-latex.log
bibtex main > /tmp/adaptive-correction-bibtex.log
pdflatex -interaction=nonstopmode -halt-on-error main.tex >> /tmp/adaptive-correction-latex.log
pdflatex -interaction=nonstopmode -halt-on-error main.tex >> /tmp/adaptive-correction-latex.log
