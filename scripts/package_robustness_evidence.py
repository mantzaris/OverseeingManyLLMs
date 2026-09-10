#!/usr/bin/env python3
"""Apply the unchanged Stage 5 publication-redaction procedure to Stage 6 only."""
from pathlib import Path
# Historical entry point is immutable; parameterize only its two output roots.
source=Path(__file__).with_name('package_practical_evidence.py')
code=source.read_text().replace('stage5_practical_private','stage6_robustness_private').replace('stage5_practical','stage6_robustness')
exec(compile(code,str(source),'exec'),{'__name__':'__main__','__file__':str(source.resolve())})
