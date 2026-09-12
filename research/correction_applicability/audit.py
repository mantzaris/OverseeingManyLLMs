"""Reproducible development-only sampling of historical transfer events."""
import csv
from .common import ART,OLD,read,write

def build():
 m=read(OLD/'frozen/manifest.json');ids=[c['id'] for c in m['contexts']];cs={c['id']:c for c in m['contexts']};rows=list(csv.DictReader((OLD/'analysis/transfers.csv').open()));chosen=[]
 for category in ['help','harm','tie']:
  eligible=[r for r in rows if r['method']=='adaptive' and int(r['step'])<=2 and (float(r['gain'])==0 if category=='tie' else int(r[category])==1)]
  eligible.sort(key=lambda r:(ids.index(r['context']),int(r['rep']),int(r['step']),next(q['order'] for q in cs[r['context']]['questions'] if q['id']==r['recipient'])))
  for r in eligible[:3]:
   c=cs[r['context']];run=read(OLD/'evaluation/runs'/('%s_r%s_adaptive_b2.json'%(r['context'],r['rep'])));e=run['events'][int(r['step'])-1];h=next(x for x in e['repairs'] if x['id']==r['recipient']);q=next(q for q in c['questions'] if q['id']==r['recipient'])
   chosen.append(dict(category=category,source_number=ids.index(c['id'])+1,context_id=c['id'],rep=int(r['rep']),step=int(r['step']),recipient=q,disclosure=e['disclosure'],repair=h,source=c,offline_metric=r))
 write(ART/'historical_audit.json',dict(selection='First three helpful, harmful and score-tied adaptive accepted transfers in frozen source, replica, step, recipient order. These prior evaluation sources are now development evidence, not fresh.',events=chosen))
 for i,e in enumerate(chosen):
  print(i,e['category'],'source',e['source_number']);print('DONOR:',e['disclosure']['question'],e['disclosure']['answer'],e['disclosure']['scale']);print('TARGET:',e['recipient']['question']);print('BEFORE',e['repair']['before']['answer'],e['repair']['before']['derivation']);print('AFTER',e['repair']['after']['answer'],e['repair']['after']['derivation']);print('TABLE',e['source']['table'])
if __name__=='__main__':build()
