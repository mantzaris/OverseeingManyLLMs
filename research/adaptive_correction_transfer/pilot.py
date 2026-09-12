"""Fixed development source order, actual independent transfer and retry prompts."""
import argparse,time
from .common import ART,read,write
from .data import annotations
from .inference import request
from .feedback import Inspector,verified_answer
from .features import initial_rank,relation,fixed_eligible
from .scoring import score

def pilot(limit=12,revision="v2"):
 contexts=read(ART/'development_manifest.json')['contexts'][:limit];gold=annotations('train');out=[]
 for i,c in enumerate(contexts):
  target=ART/('development_'+revision)/('c%02d.json'%i)
  if target.exists():out.append(read(target));continue
  initial={};calls=[]
  for n,q in enumerate(c['questions']):
   a,u=request(('dev_'+revision+'_c%02d_q%02d_initial')%(i,n),c,q,821000+i*100+n);initial[q['id']]=a;calls.append(u)
  ranked=initial_rank(c,initial);qid=ranked[0];q=next(q for q in c['questions'] if q['id']==qid);f=Inspector(gold[c['id']],1).inspect(q);f['previous']={k:initial[qid].get(k) for k in ['answer','scale','evidence','operation']};transfers=[]
  for n,j in enumerate(c['questions']):
   if j['id']==qid:continue
   rel=relation(q,initial[qid],j,initial[j['id']]);updated,u=request(('dev_'+revision+'_c%02d_q%02d_transfer')%(i,n),c,j,831000+i*100+n,initial[j['id']],[f]);calls.append(u)
   retry,u=request(('dev_'+revision+'_c%02d_q%02d_retry')%(i,n),c,j,831000+i*100+n,initial[j['id']],None,True);calls.append(u)
   transfers.append(dict(id=j['id'],relation=rel,eligible=fixed_eligible(rel),before=initial[j['id']],after=updated,retry=retry,before_score=score(initial[j['id']],gold[c['id']][j['id']]),after_score=score(updated,gold[c['id']][j['id']]),retry_score=score(retry,gold[c['id']][j['id']])))
  r=dict(context_id=c['id'],initial=initial,initial_scores={q['id']:score(initial[q['id']],gold[c['id']][q['id']]) for q in c['questions']},inspection=f,transfers=transfers,calls=calls);write(target,r);out.append(r)
  print('Development',i+1,'initial EM',sum(x['em'] for x in r['initial_scores'].values()),'/',len(initial),'transfers',sum(t['after_score']['em']-t['before_score']['em'] for t in transfers),flush=True)
 write(ART/'development/summary.json',out)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--limit',type=int,default=12);p.add_argument('--revision',default='v4');a=p.parse_args();pilot(a.limit,a.revision)
