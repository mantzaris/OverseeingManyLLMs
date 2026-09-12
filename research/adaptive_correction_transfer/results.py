"""Private saved-output evaluation. Never imported by the online controller."""
import csv,collections
from pathlib import Path
import numpy as np
from .common import ART,read,write
from .scoring import score

def csvout(path,rows):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 if not rows:return
 with path.open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def interval(values,seed=91844):
 a=np.array(values,float);rng=np.random.default_rng(seed)
 b=a[rng.integers(0,len(a),size=(2000,len(a)))].mean(axis=1)
 return dict(mean=float(a.mean()),low=float(np.quantile(b,.025)),high=float(np.quantile(b,.975)),wins=int((a>1e-9).sum()),ties=int((abs(a)<=1e-9).sum()),losses=int((a< -1e-9).sum()),n=len(a))
def analyze(prefix='evaluation'):
 manifest=read(ART/'frozen/manifest.json');gold=read(ART/'frozen/evaluator_annotations.json');rows=[];transfers=[];audits=[];runs={};missing=[]
 for i,c in enumerate(manifest['contexts']):
  for rep in manifest['replicates']:
   for method in manifest['methods']:
    path=ART/prefix/'runs'/('%s_r%d_%s_b2.json'%(c['id'],rep,method))
    if not path.exists():missing.append(dict(context=c['id'],rep=rep,method=method));continue
    runs[(c['id'],rep,method,2)]=read(path)
  for method,b in [('frozen_model',2),('adaptive',3),('fixed_audit',3)]:
   if i >= (manifest['frozen_model_contexts'] if method=='frozen_model' else manifest['budget3_contexts']):continue
   path=ART/prefix/'runs'/('%s_r0_%s_b%d.json'%(c['id'],method,b))
   if path.exists():runs[(c['id'],0,method,b)]=read(path)
   else:missing.append(dict(context=c['id'],rep=0,method=method,budget=b))
 for (cid,rep,method,ceiling),r in runs.items():
  g=gold[cid];base=r['snapshots'][0];events=r['events']
  for b,answers in enumerate(r['snapshots']):
   if ceiling==3 and b<3:continue
   inspected={e['inspected'] for e in events[:b]};s={q:score(a,g[q]) for q,a in answers.items()};never=[q for q in s if q not in inspected];repairs=[h for e in events[:b] for h in e['repairs']]
   row=dict(context=cid,rep=rep,method=method,budget=b,answers=len(s),em=sum(x['em'] for x in s.values()),f1=sum(x['f1'] for x in s.values()),scale=sum(x['scale'] for x in s.values()),joint=sum(x['joint'] for x in s.values()),project_correct=int(all(x['em'] for x in s.values())),unfinished=sum(x['unfinished'] for x in s.values()),inspections=len(inspected),inspected_correct=sum(s[q]['em'] for q in inspected),never_inspected=len(never),never_correct=sum(s[q]['em'] for q in never),sibling_net=sum(s[q]['em']-score(base[q],g[q])['em'] for q in never),sibling_fixed=sum(score(base[q],g[q])['em']==0 and s[q]['em']==1 for q in never),sibling_damaged=sum(score(base[q],g[q])['em']==1 and s[q]['em']==0 for q in never),calls=len(repairs),tokens=sum(h['usage']['tokens'] for h in repairs),inference_seconds=sum(h['usage']['seconds'] for h in repairs),failed_repairs=sum(not h['accepted'] for h in repairs),reused_corrections=sum(bool(e['repairs']) for e in events[:b]),local_gain=sum(1-score(e['current_before'],g[e['inspected']])['em'] for e in events[:b]),controller_total_seconds=r['seconds'])
   row['accuracy']=row['em']/row['answers'];rows.append(row)
  # Only the longest run per method contributes transition counts.
  if ceiling==2 and (cid,rep,method,3) in runs:pass
  for e in events:
   if ceiling==3 and e['step']<=2:continue
   audits.append(dict(context=cid,rep=rep,method=method,step=e['step'],question=e['inspected'],probability=e['selection_probability'],recipients=len(e['repairs']),parameter_updates=len(e['updates']),transfer_updates=sum(u['kind']=='transfer' for u in e['updates']),original_error=e['observations'][-1]['original_error']))
   for h in e['repairs']:
    before=score(h['before'],g[h['id']])['em'];after=score(h['after'],g[h['id']])['em'];raw=score(h['proposal'],g[h['id']])['em'];option=next(x for x in e['candidates'] if x['id']==h['id'])
    transfers.append(dict(context=cid,rep=rep,method=method,step=e['step'],donor=e['inspected'],recipient=h['id'],bin=h['relation']['bin'],before=before,after=after,raw_after=raw,help=int(after>before),harm=int(after<before),gain=after-before,predicted_gain=option['gain']+.01,accepted=h['accepted'],call_id=h['usage']['call_id']))
 groups=collections.defaultdict(list)
 for r in rows:groups[(r['method'],r['budget'])].append(r)
 summaries=[]
 for (method,b),rs in sorted(groups.items()):
  out=dict(method=method,budget=b,episodes=len(rs),contexts=len({r['context'] for r in rs}))
  for k in ['answers','em','f1','scale','joint','project_correct','unfinished','inspections','inspected_correct','never_inspected','never_correct','sibling_net','sibling_fixed','sibling_damaged','calls','tokens','inference_seconds','failed_repairs','reused_corrections','local_gain']:out[k]=sum(r[k] for r in rs)
  source=collections.defaultdict(list)
  for r in rs:source[r['context']].append(r['accuracy'])
  ci=interval([np.mean(x) for x in source.values()]);out.update(accuracy=out['em']/out['answers'],accuracy_low=ci['low'],accuracy_high=ci['high']);summaries.append(out)
 comparisons=[];paired=[]
 for a,b in [('adaptive','fixed_audit'),('adaptive','individual'),('adaptive','individual_risk'),('adaptive','memory'),('adaptive','source_rule'),('source_rule','reattempt'),('memory','individual'),('adaptive','frozen_model')]:
  for budget in [1,2,3]:
   by=collections.defaultdict(dict)
   for r in rows:
    if r['budget']==budget and r['method'] in [a,b]:by[(r['context'],r['rep'])][r['method']]=r['accuracy']
   dif=collections.defaultdict(list)
   for (cid,rep),x in by.items():
    if a in x and b in x:dif[cid].append(x[a]-x[b])
   if not dif:continue
   vals=[float(np.mean(v)) for v in dif.values()];ci=interval(vals);comparisons.append(dict(first=a,second=b,budget=budget,**ci))
   for cid,v in dif.items():paired.append(dict(context=cid,first=a,second=b,budget=budget,difference=float(np.mean(v))))
 disagreement=[]
 for a,b in [('adaptive','fixed_audit'),('adaptive','frozen_model'),('source_rule','reattempt'),('individual','memory')]:
  for (cid,rep,m,cap),r in runs.items():
   if m!=a or cap!=2 or (cid,rep,b,2) not in runs:continue
   s=runs[(cid,rep,b,2)];aa=[e['inspected'] for e in r['events']];bb=[e['inspected'] for e in s['events']]
   disagreement.append(dict(context=cid,rep=rep,first=a,second=b,different=int(aa!=bb),first_different=int(aa[0]!=bb[0]),recipients_different=int([e['recipients'] for e in r['events']]!=[e['recipients'] for e in s['events']])))
 out=ART/'analysis'
 for name,data in [('episodes',rows),('transfers',transfers),('audits',audits),('summary',summaries),('comparisons',comparisons),('paired',paired),('disagreement',disagreement)]:csvout(out/(name+'.csv'),data)
 write(out/'results.json',dict(summary=summaries,comparisons=comparisons,missing=missing,source_units=len(manifest['contexts']),bootstrap='2000 paired context resamples, seed91844, replicas averaged inside context; intervals descriptive, no multiplicity adjustment. Nonidentical contexts may share a report.'))
 print('Analyzed',len(runs),'runs; missing',len(missing))
if __name__=='__main__':analyze()
