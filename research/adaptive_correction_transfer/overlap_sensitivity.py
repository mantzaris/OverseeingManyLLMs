"""Exploratory uncertainty check using observed exact-paragraph components."""
import pandas as pd,numpy as np
from .common import ART,read
from .results import csvout

def analyze():
 p=pd.read_csv(ART/'analysis/paired.csv');groups=read(ART/'analysis/source_dependence.json')['public_text_components'];rows=[]
 for a,b in [('adaptive','fixed_audit'),('adaptive','individual_risk'),('source_rule','reattempt')]:
  z=p[(p['first']==a)&(p['second']==b)&(p.budget==2)].set_index('context');cs=[g for g in groups if all(cid in z.index for cid in g)]
  if sum(map(len,cs))!=24:continue
  sums=np.array([sum(z.loc[cid,'difference'] for cid in g) for g in cs]);sizes=np.array(list(map(len,cs)));rng=np.random.default_rng(91844);ix=rng.integers(0,len(cs),(2000,len(cs)));bs=sums[ix].sum(axis=1)/sizes[ix].sum(axis=1)
  rows.append(dict(first=a,second=b,budget=2,contexts=24,components=len(cs),mean=sums.sum()/sizes.sum(),low=np.quantile(bs,.025),high=np.quantile(bs,.975),status='Post hoc public-overlap sensitivity; components are not verified report identities'))
 csvout(ART/'analysis/overlap_sensitivity.csv',rows);print('Exploratory overlap comparisons',len(rows))
if __name__=='__main__':analyze()
