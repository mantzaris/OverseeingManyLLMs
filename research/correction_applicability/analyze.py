"""Offline annotation scoring, never imported by the controller."""
import csv,collections
from pathlib import Path
import numpy as np
from research.adaptive_correction_transfer.scoring import score
from .common import ART,read,write
from .representation import contract
from .experiment import METHODS

def csvout(p,rows):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 if not rows:return
 with p.open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def interval(vals):
 a=np.array(vals,float);rng=np.random.default_rng(92112);b=a[rng.integers(0,len(a),(2000,len(a)))].mean(axis=1)
 return dict(mean=float(a.mean()),low=float(np.quantile(b,.025)),high=float(np.quantile(b,.975)),wins=int((a>1e-9).sum()),ties=int((abs(a)<=1e-9).sum()),losses=int((a< -1e-9).sum()),contexts=len(a))

def analyze(revision='v1'):
 from .backend import load
 contract=load(revision).contract
 cs=read(ART/'development_manifest.json')['contexts'];gold=read(ART/'offline_development_annotations.json')['annotations'];rows=[];changes=[];patches=[];representations=[];missing=[]
 for i,c in enumerate(cs):
  g=gold[c['id']];initial_path=ART/('development_'+revision)/('c%02d_initial.json'%i)
  if initial_path.exists():
   init=read(initial_path)
   for q in c['questions']:
    a=init['answers'][q['id']];representations.append(dict(context=c['id'],question=q['id'],valid=a['representation_valid'],contract_valid=not contract(c,q,a.get('rep')),errors=';'.join(contract(c,q,a.get('rep'))),initial_em=score(a,g[q['id']])['em']))
  for method in METHODS:
   p=ART/('development_'+revision)/('c%02d_%s.json'%(i,method))
   if not p.exists():missing.append([i,method]);continue
   r=read(p);base=r['initial'];final=r['answers'];inspected=set(r['inspection_ids']);never=set(final)-inspected;initial_em=sum(score(a,g[q])['em'] for q,a in base.items());local=helped=harmed=accepted=rejected=0
   for e in r['events']:
    if e['kind']=='inspection':local+=score(final[e['inspected']],g[e['inspected']])['em']-score(e['before'],g[e['inspected']])['em']
    if e.get('patch'):patches.append(dict(context=c['id'],method=method,step=e['step'],donor=e['inspected'],kind=e['patch']['kind'],supported=e['patch']['supported'],reasons=';'.join(e['patch']['reasons'])))
    for h in e['revisions']:
     q=h['recipient'];b=score(h['before'],g[q])['em'];a=score(h['after'],g[q])['em'];cand=score(h['candidate'],g[q])['em'] if h['candidate'] is not None else b;helped+=a>b;harmed+=a<b;accepted+=h['accepted'];rejected+=not h['accepted']
     changes.append(dict(context=c['id'],source_index=i,method=method,step=e.get('step',0),recipient=q,before=b,after=a,candidate=cand,help=int(a>b),harm=int(a<b),accepted=h['accepted'],rejected_harm=int(not h['accepted'] and cand<b),reasons=';'.join(h['reasons']),kind=h.get('kind','generated')))
   scores={q:score(a,g[q]) for q,a in final.items()};em=sum(s['em'] for s in scores.values());assert initial_em+local+helped-harmed==em,p
   row=dict(context=c['id'],source_index=i,method=method,answers=len(final),initial_em=initial_em,em=em,f1=sum(s['f1'] for s in scores.values()),scale=sum(s['scale'] for s in scores.values()),joint=sum(s['joint'] for s in scores.values()),whole_context=int(all(s['em'] for s in scores.values())),unfinished=sum(s['unfinished'] for s in scores.values()),inspections=r['inspections'],local_gain=local,helpful_events=helped,harmful_events=harmed,accepted=accepted,rejected=rejected,sibling_fixed=sum(score(base[q],g[q])['em']==0 and scores[q]['em']==1 for q in never),sibling_harmed=sum(score(base[q],g[q])['em']==1 and scores[q]['em']==0 for q in never),calls=len(r['calls']),tokens=sum(u['tokens'] for u in r['calls']),seconds=sum(u['seconds'] for u in r['calls']))
   row.update(attempts=sum(u['attempts'] for u in r['calls']),extraction_calls=len(init['calls']),extraction_attempts=sum(u['attempts'] for u in init['calls']),extraction_tokens=sum(u['tokens'] for u in init['calls']),extraction_seconds=sum(u['seconds'] for u in init['calls']))
   row['accuracy']=em/len(final);rows.append(row)
 summary=[]
 for method in METHODS:
  rs=[r for r in rows if r['method']==method]
  if not rs:continue
  s=dict(method=method,contexts=len(rs))
  for k in list(rs[0])[3:-1]:s[k]=sum(r[k] for r in rs)
  s['accuracy']=s['em']/s['answers'];summary.append(s)
 comparisons=[];pairs=[]
 for other in [x for x in METHODS if x!='patch']:
  a={r['context']:r['accuracy'] for r in rows if r['method']=='patch'};b={r['context']:r['accuracy'] for r in rows if r['method']==other};ids=[c['id'] for c in cs if c['id'] in a and c['id'] in b]
  if ids:
   vals=[a[c]-b[c] for c in ids];comparisons.append(dict(first='patch',second=other,**interval(vals)))
   pairs.extend(dict(context=c,first='patch',second=other,difference=a[c]-b[c]) for c in ids)
 out=ART/('analysis_'+revision)
 for name,data in [('episodes',rows),('summary',summary),('changes',changes),('patches',patches),('representations',representations),('comparisons',comparisons),('paired',pairs)]:csvout(out/(name+'.csv'),data)
 write(out/'audit.json',dict(completed=len(rows),expected=len(cs)*len(METHODS),missing=missing,identities_checked=True,kind='Reused development source contexts; descriptive paired intervals are exploratory, not held-out inference.'))
 print('Development',revision,'completed',len(rows),'missing',len(missing))
 for r in summary:print(r['method'],'EM',r['em'],'/',r['answers'],'net sibling',r['sibling_fixed']-r['sibling_harmed'],'accepted/rejected',r['accepted'],r['rejected'])
 print('Representation',sum(r['valid'] for r in representations),'contract',sum(r['contract_valid'] for r in representations),'/',len(representations))
 return summary
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--revision',default='v1');a=p.parse_args();analyze(a.revision)
