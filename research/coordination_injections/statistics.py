"""Paired monthly-block analysis with replicas kept together."""
import numpy as np
SEED=91843
RESAMPLES=2000
def paired(rows,left,right,metric):
 blocks=sorted({r['month'] for r in rows});diffs=[]
 for b in blocks:
  a={ (r['project_id'],r['rep']):r[metric] for r in rows if r['month']==b and r['method']==left}
  z={ (r['project_id'],r['rep']):r[metric] for r in rows if r['month']==b and r['method']==right}
  if set(a)!=set(z) or not a:raise ValueError('Unpaired condition in '+b)
  diffs.append(float(np.mean([a[k]-z[k] for k in sorted(a)])))
 rng=np.random.RandomState(SEED);d=np.array(diffs);samples=np.mean(d[rng.randint(0,len(d),(RESAMPLES,len(d)))],axis=1)
 return dict(left=left,right=right,metric=metric,mean=float(np.mean(d)),interval95=[float(x) for x in np.percentile(samples,[2.5,97.5])],blocks=blocks,differences=diffs,negative=int(sum(d<0)),ties=int(sum(d==0)),positive=int(sum(d>0)),resamples=RESAMPLES,analysis_seed=SEED)
