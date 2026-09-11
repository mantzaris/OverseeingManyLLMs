#!/usr/bin/env python3
"""Recompute tables in a temporary directory without replacing measured timings."""
import contextlib,importlib.util,io,json,tempfile
from pathlib import Path
root=Path('artifacts/stage7_empirical').resolve()
spec=importlib.util.spec_from_file_location('hvac_analysis','scripts/hvac_analyze.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.analyze(True)
with tempfile.TemporaryDirectory(prefix='hvac_replay_') as folder:
    temp=Path(folder)
    for name in ('cases.json','estimator.json','baseline.json','evaluation'):(temp/name).symlink_to(root/name)
    m.ROOT=temp
    with contextlib.redirect_stdout(io.StringIO()):m.analyze()
    tables=['episodes.csv','diagnoses.csv','policy_summary.csv','paired.csv','bundle_differences.csv']
    # Git normalizes CSV CRLF to LF in a clean checkout. Universal-newline text
    # comparison retains every value and column while allowing that transport detail.
    for name in tables:assert (temp/'analysis'/name).read_text()==(root/'analysis'/name).read_text(),name
    current=json.loads((temp/'analysis/diagnostics.json').read_text());saved=json.loads((root/'analysis/diagnostics.json').read_text())
    for k in current:
        if k not in ('planning_mean_ms','planning_max_ms'):assert current[k]==saved[k],k
print('Recomputed five result tables and prediction diagnostics exactly; original planning timings preserved.')
