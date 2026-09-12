#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/correction-paper-pass1.log
bibtex main > /tmp/correction-paper-bibtex.log
pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/correction-paper-pass2.log
pdflatex -interaction=nonstopmode -halt-on-error main.tex > /tmp/correction-paper-pass3.log
pdfinfo main.pdf > pdfinfo.txt
python3 - <<'PY'
from pathlib import Path
p=Path('pdfinfo.txt');p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
s=Path('main.log').read_text()
issues=[x for x in s.splitlines() if 'Overfull' in x or 'undefined' in x or 'LaTeX Warning' in x]
Path('build_audit.txt').write_text('\n'.join(issues) if issues else 'No overfull boxes, undefined references or LaTeX warnings.\n')
print(Path('pdfinfo.txt').read_text().split('Pages:')[1].splitlines()[0].strip()+' pages')
print(Path('build_audit.txt').read_text())
PY
