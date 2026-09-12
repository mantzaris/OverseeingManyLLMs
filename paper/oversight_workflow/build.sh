#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/oversight-latex-pass1.log
bibtex main > /tmp/oversight-bibtex.log
pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/oversight-latex-pass2.log
pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/oversight-latex-pass3.log
pdfinfo main.pdf | head -18
