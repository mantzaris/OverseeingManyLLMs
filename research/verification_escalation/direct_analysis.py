"""Paired post hoc comparator audit; no source sample is called fresh here."""
from pathlib import Path
from collections import Counter
import numpy as np
from .common import ART,read,write_json
from .analyze import load
from .secondary_analysis import interval

def run(root=ART/'direct_reader_audit',primary_root=ART/'repair'):
 root=Path(root);primary_root=Path(primary_root);rows=load(root/'episodes.csv');primary=load(primary_root/'evaluation/episodes.csv');summary=[];paired=[]
 for b in [0,1,2]:
  rr=[r for r in rows if r['budget']==b]
  summary.append(dict(budget=b,n_replicas=len(rr),n_sources=len({r['id'] for r in rr}),**{k:sum(r[k] for r in rr) for k in ['questions','correct','wrong','unfinished','loss','executions']}))
  assert len(rr)==48 and len({(r['id'],r['rep']) for r in rr})==48
  for m in ['verification','recovery_completion','full_context','matched_checking']:
   for metric in ['questions','correct','wrong','unfinished','loss','executions']:
    dif=[]
    for cid in sorted({r['id'] for r in rr}):
     a=[r[metric] for r in rr if r['id']==cid];z=[r[metric] for r in primary if r['id']==cid and r['budget']==b and r['condition']=='generated' and r['method']==m]
     assert len(a)==len(z)==2;dif.append(np.mean(a)-np.mean(z))
    paired.append(dict(budget=b,baseline=m,metric=metric,direction='Direct reader minus named baseline',**interval(dif)))
 for r in rows:
  assert r['correct']+r['wrong']+r['unfinished']==1 and r['questions']<=r['budget'] and r['executions']<=24
 obj=dict(classification='Post hoc audit on previously inspected source cases, not new held-out evidence',summary=summary,paired=paired,status_counts=dict(Counter(r['status'] for r in rows if r['budget']==1)))
 write_json(root/'analysis.json',obj);print(summary);print(obj['status_counts']);return obj
if __name__=='__main__':run()
