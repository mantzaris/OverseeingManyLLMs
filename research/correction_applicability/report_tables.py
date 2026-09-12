"""Numerical tables for the report and illustrated note from saved results."""
import csv
from pathlib import Path
from .common import ART,ROOT,read,write

def build():
 tables={}
 for v in ['v1','v2']:
  with (ART/f'analysis_{v}/summary.csv').open() as f:tables[v]={r['method']:r for r in csv.DictReader(f)}
 names={'individual':'Individual correction','execute':'Execution only','reattempt':'Ordinary reattempt','verify':'Source verification','coarse':'Coarse transfer','patch':'Constrained patch','no_applicability':'No applicability'}
 md=['| Method | v1 EM / 72 | v2 EM / 72 | v2 mean F1 | v2 joint / 72 | v2 sibling repairs / harms | v2 extra calls |','|---|---:|---:|---:|---:|---:|---:|'];tex=[]
 for m,name in names.items():
  a=tables['v1'][m];r=tables['v2'][m]
  md.append(f"| {name} | {float(a['em']):.0f} | {float(r['em']):.0f} | {float(r['f1'])/72:.3f} | {float(r['joint']):.0f} | {r['sibling_fixed']} / {r['sibling_harmed']} | {r['calls']} |")
  tex.append(f"{name} & {float(a['em']):.0f} & {float(r['em']):.0f} & {float(r['f1'])/72:.3f} & {r['sibling_fixed']}/{r['sibling_harmed']} & {r['calls']} \\\\")
 (ART/'result_table.md').write_text('\n'.join(md)+'\n');paper=ROOT/'paper/correction_applicability';paper.mkdir(parents=True,exist_ok=True);(paper/'result_rows.tex').write_text('\n'.join(tex)+'\n')
if __name__=='__main__':build()
