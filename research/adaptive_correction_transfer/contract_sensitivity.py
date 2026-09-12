"""Post hoc output-contract sensitivity; does not change online labels or trajectories."""
import collections
import numpy as np
from .common import ART,read,write
from .scoring import score
from .results import csvout,interval

def analyze():
 m=read(ART/'frozen/manifest.json');g=read(ART/'frozen/evaluator_annotations.json');rows=[];credit=[]
 for c in m['contexts']:
  for rep in m['replicates']:
   ip=ART/'evaluation/initial'/('%s_r%d.json'%(c['id'],rep))
   if not ip.exists():continue
   init=read(ip)['answers']
   for q,a in init.items():
    s=score(a,g[c['id']][q])
    if s['em'] and not a.get('valid'):credit.append(dict(context=c['id'],rep=rep,question=q,answer=a,official_score=s))
   for method in m['methods']:
    p=ART/'evaluation/runs'/('%s_r%d_%s_b2.json'%(c['id'],rep,method))
    if not p.exists():continue
    r=read(p);answers=r['answers'];scores={q:score(a,g[c['id']][q]) for q,a in answers.items()};valid={q:bool(a.get('valid')) for q,a in answers.items()}
    rows.append(dict(context=c['id'],rep=rep,method=method,official_em=sum(s['em'] for s in scores.values()),strict_em=sum(scores[q]['em']*valid[q] for q in scores),schema_invalid=sum(not x for x in valid.values()),strict_project=int(all(scores[q]['em'] and valid[q] for q in scores)),n=len(scores)))
 pairs=[]
 for b in ['fixed_audit','individual_risk','source_rule']:
  by=collections.defaultdict(dict);ds=collections.defaultdict(list)
  for r in rows:
   if r['method'] in ['adaptive',b]:by[(r['context'],r['rep'])][r['method']]=r['strict_em']/r['n']
  for (cid,rep),d in by.items():
   if 'adaptive' in d and b in d:ds[cid].append(d['adaptive']-d[b])
  if ds:pairs.append(dict(first='adaptive',second=b,**interval([np.mean(v) for v in ds.values()])))
 csvout(ART/'analysis/contract_sensitivity.csv',rows);csvout(ART/'analysis/contract_comparisons.csv',pairs)
 write(ART/'analysis/contract_audit.json',dict(initial_schema_invalid_credited=len(credit),cases=credit,interpretation='Reporting clarification after freeze: official metric scores extracted answer and normalized scale even when another parser field is invalid. The frozen failure description was too broad. Primary recorded scoring and online updates remain unchanged. Strict schema sensitivity zeros invalid outputs without pretending those alternative labels drove the recorded policy. Complete requested evidence fields are a separate, stricter criterion.'))
 print('Initial schema-invalid answers credited by official metric:',len(credit))
if __name__=='__main__':analyze()
