"""Declared loss sensitivity and explicitly post hoc diagnostic summaries.

All inputs are frozen saved outputs. No policy is rerun under new utility weights.
"""
from pathlib import Path
from collections import defaultdict
import numpy as np
from .common import ART,read,write_json,digest
from .analyze import load
from .engine import execute,MachineBudget,equivalent

def interval(values):
 x=np.asarray(values,dtype=float);rng=np.random.RandomState(86421)
 b=x[rng.randint(0,len(x),(2000,len(x)))].mean(axis=1)
 return dict(mean=float(x.mean()),low=float(np.percentile(b,2.5)),high=float(np.percentile(b,97.5)),negative=int((x<0).sum()),ties=int((x==0).sum()),positive=int((x>0).sum()),n=len(x))

def run(root=ART/'repair',source_root=None):
 root=Path(root);source_root=Path(source_root or root)
 rows=load(root/'evaluation/episodes.csv');base=[r for r in rows if r['condition']=='generated' and r['budget']==1]
 weights=[]
 for w in [1,2,4,8]:
  dif=[]
  for i in sorted({r['id'] for r in base}):
   a=[w*r['wrong']+r['unfinished'] for r in base if r['id']==i and r['method']=='verification']
   b=[w*r['wrong']+r['unfinished'] for r in base if r['id']==i and r['method']=='recovery_completion']
   dif.append(np.mean(a)-np.mean(b))
  weights.append(dict(incorrect_release_weight=w,unfinished_weight=1,analysis='Declared rescoring sensitivity; unchanged trajectories',**interval(dif)))
 grouped=[]
 for attr in ['kind','domain']:
  for group in sorted({r[attr] for r in base}):
   rr=[r for r in base if r[attr]==group]
   for method in ['recovery_completion','verification','full_context','matched_checking','no_coverage_guard']:
    z=[r for r in rr if r['method']==method]
    grouped.append(dict(grouping=attr,group=group,method=method,n_sources=len({r['id'] for r in z}),n_replicates=len(z),**{k:sum(r[k] for r in z) for k in ['questions','correct','wrong','unfinished','suppressed','incorrect_suppression','intended_covered','covered_references','references','verification_failures']}))
 # Domains are not sampling units, but inspect this stronger aggregation too.
 domain_diff=[]
 for domain in sorted({r['domain'] for r in base}):
  a=[r['loss'] for r in base if r['domain']==domain and r['method']=='verification'];b=[r['loss'] for r in base if r['domain']==domain and r['method']=='recovery_completion']
  domain_diff.append(np.mean(a)-np.mean(b))
 lat={}
 for method in sorted({r['method'] for r in base}):
  z=[r for r in base if r['method']==method];t=[r['controller_seconds'] for r in z]
  lat[method]=dict(median_ms=float(np.median(t)*1000),p95_ms=float(np.percentile(t,95)*1000),sum_executions=sum(r['executions'] for r in z),note='Measured CPU controller time; generation separately accounted')
 coverage=[r for r in base if r['method']=='verification'];prep=[];audits=[]
 from .repair_data import public_task
 from .controller import candidates
 cases=read(source_root/'private/cases.json')['evaluation']
 for c in cases:
  task=public_task(c,0);refs=[execute(c['snapshot'],q,MachineBudget(1),task['contract']['ordered']) for q in c['refs']]
  audits.append(dict(id=c['id'],db=c['db'],kind=c['kind'],ordered=task['contract']['ordered'],references=len(refs),status=[r['status'] for r in refs],all_equal=equivalent(refs),foreign_key_violations=len(c['foreign_key_violations'])))
  for rep in [0,1]:
   p=read(source_root/'prepared'/('repair_evaluation_v2_'+c['id']+'_r'+str(rep)+'.json'))
   aa=p['calls'].get('candidates') or {};bb=p['calls'].get('audit') or {}
   ca=[x.get('sql') for x in aa.get('candidates',[]) if isinstance(x,dict)];cb=[x.get('sql') for x in bb.get('candidates',[]) if isinstance(x,dict)]
   prep.append(dict(id=c['id'],rep=rep,first_sql_differs=bool(ca and cb and ca[0]!=cb[0]),candidate_set_differs=set(ca)!=set(cb),candidate_count=len(candidates(p['calls'])[0]),declared_unknown=bool(aa.get('unrepresented_possible') or bb.get('unrepresented_possible')),parsed_public_calls=int(bool(aa))+int(bool(bb))))
 report=dict(loss_weight_sensitivity=weights,grouped=grouped,domain_aggregation=dict(note='Post hoc domain-level descriptive sensitivity, not replacement for frozen source-database unit',**interval(domain_diff)),latency=lat,coverage=dict(replicates=len(coverage),intended_output_covered=sum(r['intended_covered'] for r in coverage),all_reference_outputs_covered=sum(r['covered_references']==r['references'] for r in coverage),suppressed=sum(r['suppressed'] for r in coverage),mismatched_suppression=sum(r['incorrect_suppression'] for r in coverage),generated_execution_failures=sum(r['verification_failures'] for r in coverage),warning='Execution-output coverage is weaker than semantic interpretation coverage'),generation_variation=prep,reference_audit=audits)
 write_json(root/'analysis/secondary.json',report)
 return report
if __name__=='__main__':run()
