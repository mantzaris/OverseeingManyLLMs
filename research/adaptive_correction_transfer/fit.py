"""Offline development fitting only, never called from an evaluation episode."""
from collections import defaultdict
from .common import ART,read,write,digest
from .features import risk_key,relation
from .scoring import score

def fit(revision='v4'):
 contexts={c['id']:c for c in read(ART/'development_manifest.json')['contexts']};rows=[read(p) for p in sorted((ART/('development_'+revision)).glob('c*.json'))];risk=defaultdict(lambda:[1.,1.]);cond=defaultdict(lambda:[1.,1.]);transfer={k:dict(fix=[1.,1.],harm=[1.,1.]) for k in ['pooled','context','lexical','evidence']};counts=[]
 for r in rows:
  c=contexts[r['context_id']];initial=r['initial'];scores=r['initial_scores'];qs=c['questions']
  for q in qs:
   err=1-scores[q['id']]['em']
   for key in ['pooled',risk_key(q,initial[q['id']])]:risk[key][0]+=err;risk[key][1]+=1-err
   for j in qs:
    if q['id']==j['id']:continue
    rel=relation(q,initial[q['id']],j,initial[j['id']]);key=rel['bin']+'_'+str(int(err));e=1-scores[j['id']]['em'];cond[key][0]+=e;cond[key][1]+=1-e
  for t in r['transfers']:
   b=1-t['before_score']['em'];after=t['after_score']['em'] if t['after'].get('valid') else t['before_score']['em'];kind='fix' if b else 'harm';value=after if b else 1-after
   for key in ['pooled',t['relation']['bin']]:transfer[key][kind][0]+=value;transfer[key][kind][1]+=1-value
   counts.append(dict(context_id=c['id'],bin=t['relation']['bin'],before=t['before_score'],after=t['after_score'],retry=t['retry_score'],eligible=t['eligible']))
 # Sparse groups shrink toward pooled rates with four virtual observations.
 for key in list(risk):
  if key!='pooled':
   m=risk['pooled'][0]/sum(risk['pooled']);risk[key][0]+=4*m;risk[key][1]+=4*(1-m)
 for key in ['context','lexical','evidence']:
  for outcome in ['fix','harm']:
   p=transfer['pooled'][outcome];m=p[0]/sum(p);transfer[key][outcome][0]+=4*m;transfer[key][outcome][1]+=4*(1-m)
 params=dict(risk=dict(risk),conditional=dict(cond),transfer=transfer,machine_cost=.01,epsilon=.05,recipient_cap=3,revision=revision,development_context_ids=list(contexts),source='Development initial answers and single inspected-question transfer pilot only. Beta smoothing and four-observation pooled shrinkage, not calibrated bounds.')
 write(ART/'initial_model.json',params);write(ART/'development_transfer_rows.json',counts);write(ART/'model_hash.json',dict(sha256=digest(params)));print('Fitted',len(rows),'contexts',len(counts),'transfer trials');return params
if __name__=='__main__':fit()
