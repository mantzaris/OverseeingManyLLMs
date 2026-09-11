#!/usr/bin/env python3
"""Retain the established official-template audit while writing Stage 7 evidence."""
from pathlib import Path
source=Path('scripts/verify_manuscript.py').read_text()
source=source.replace("root=Path('artifacts/stage6_robustness');provenance=json.loads((root/'sources/template_provenance.json').read_text())","root=Path('artifacts/stage7_empirical');provenance=json.loads(Path('artifacts/stage6_robustness/sources/template_provenance.json').read_text())")
exec(compile(source,'scripts/verify_manuscript.py','exec'))
