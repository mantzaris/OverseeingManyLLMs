"""Pilot diagnostics; no source selection from observed outcomes."""
from collections import Counter,defaultdict
from .common import ART,read,write

def analyze():
 summaries=[]
 for rev,path in [('v1','development'),('v2','development_v2'),('v3','development_v3'),('v4','development_v4')]:
  rs=[read(p) for p in sorted((ART/path).glob('c*.json'))];ts=[t for r in rs for t in r['transfers']];scores=[s for r in rs for s in r['initial_scores'].values()];after=lambda t:t['after_score'] if t['after'].get('valid') else t['before_score'];retry=lambda t:t['retry_score'] if t['retry'].get('valid') else t['before_score']
  bins={}
  for b in ['context','lexical','evidence']:
   xs=[t for t in ts if t['relation']['bin']==b];bins[b]=dict(trials=len(xs),help=sum(after(t)['em']>t['before_score']['em'] for t in xs),harm=sum(after(t)['em']<t['before_score']['em'] for t in xs),wrong_before=sum(t['before_score']['em']==0 for t in xs))
  r=dict(revision=rev,contexts=len(rs),answers=len(scores),initial_em=sum(s['em'] for s in scores),initial_scale=sum(s['scale'] for s in scores),trials=len(ts),helps=sum(after(t)['em']>t['before_score']['em'] for t in ts),harms=sum(after(t)['em']<t['before_score']['em'] for t in ts),retry_helps=sum(retry(t)['em']>t['before_score']['em'] for t in ts),retry_harms=sum(retry(t)['em']<t['before_score']['em'] for t in ts),invalid_repairs=sum(not t['after'].get('valid') for t in ts),bins=bins)
  summaries.append(r)
 write(ART/'development_summary.json',summaries)
 for r in summaries:print(r)
 return summaries
if __name__=='__main__':analyze()
