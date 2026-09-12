"""Post hoc uniform quarantine of source-integrity failures, no new inference."""
from pathlib import Path
import csv
import numpy as np
from .common import ART,read,write_json
from .analyze import load
from .engine import MachineBudget
from .integrity import check_snapshot
from .secondary_analysis import interval

def run(output=ART/'integrity_sensitivity'):
 root=Path(output);root.mkdir(parents=True,exist_ok=True);cases=read(ART/'repair/private/cases.json')['evaluation'];integrity={c['id']:check_snapshot(c['snapshot'],MachineBudget(2)) for c in cases};rows=load(ART/'repair/evaluation/episodes.csv');out=[]
 for r in rows:
  r=dict(r);r['source_trace_hash']=r.pop('trace_hash');r['controller_seconds']=None;r['execution_accounting']='Original charges plus two integrity checks; derived sensitivity, not newly measured latency';bad=integrity[r['id']]['status']!='ok';r['integrity_quarantined']=int(bad)
  if bad:
   for k in ['correct','wrong','questions','suppressed','incorrect_suppression','recovered','project_correct']:r[k]=0
   r.update(unfinished=1,loss=1,executions=2,reason='source_integrity_failed')
  else:r['executions']+=2
  assert r['correct']+r['wrong']+r['unfinished']==1 and r['executions']<=24
  out.append(r)
 with (root/'episodes.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
 summary=[];paired=[]
 for m in ['recovery_completion','verification']:
  z=[r for r in out if r['method']==m and r['condition']=='generated' and r['budget']==1]
  summary.append(dict(method=m,replicas=len(z),**{k:sum(r[k] for r in z) for k in ['questions','correct','wrong','unfinished','loss','executions']}))
 for metric in ['questions','correct','wrong','unfinished','loss']:
  vals=[]
  for c in cases:
   z=[r for r in out if r['id']==c['id'] and r['condition']=='generated' and r['budget']==1]
   vals.append(np.mean([r[metric] for r in z if r['method']=='verification'])-np.mean([r[metric] for r in z if r['method']=='recovery_completion']))
  paired.append(dict(metric=metric,**interval(vals)))
 record=dict(status='Post hoc source-integrity sensitivity using identical saved preparations. All 24 source units retained; failed snapshots become unfinished for every policy. Not a new held-out experiment.',source_integrity=integrity,summary=summary,paired=paired)
 write_json(root/'analysis.json',record);print(summary);print(paired);return record
if __name__=='__main__':run()
