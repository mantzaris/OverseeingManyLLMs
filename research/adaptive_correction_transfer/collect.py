"""Serial actual policy continuations with shared pre-inspection checkpoints."""
import argparse,copy,time
from .common import ART,read,write,digest
from .data import annotations
from .feedback import Inspector
from .controller import run,METHODS
from .inference import request

def initial(c,index,rep,prefix):
 target=ART/prefix/'initial'/('%s_r%d.json'%(c['id'],rep))
 if target.exists():return read(target)
 answers={};calls=[]
 for n,q in enumerate(c['questions']):
  a,u=request('%s_c%02d_r%d_q%02d_initial'%(prefix,index,rep,n),c,q,861000+index*100+rep*10+n);answers[q['id']]=a;calls.append(u)
 result=dict(context_id=c['id'],rep=rep,answers=answers,calls=calls);write(target,result);return result

def episode(c,index,rep,prefix,method,params,initial_outputs,gold,budget=2):
 target=ART/prefix/'runs'/('%s_r%d_%s_b%d.json'%(c['id'],rep,method,budget))
 if target.exists():return read(target)
 qindex={q['id']:i for i,q in enumerate(c['questions'])}
 def generate(q,current,corrections,step,retry):
  n=qindex[q['id']];cid='%s_c%02d_r%d_%s_s%d_q%02d'%(prefix,index,rep,method,step,n)
  return request(cid,c,q,871000+index*100+rep*30+step*10+n,current,None if retry else corrections,retry)
 result=run(c,initial_outputs,params,Inspector(gold,budget),generate,881000+index*100+rep,method,budget);result['rep']=rep;result['source_index']=index
 write(target,result);return result

def collect(development=False):
 if development:
  manifest=dict(contexts=read(ART/'development_manifest.json')['contexts'][:4],replicates=[0],methods=['individual','memory','source_rule','fixed_audit','adaptive','reattempt','individual_risk'],prefix='development_protocol')
 else:
  from .freeze import verify
  verify();manifest=read(ART/'frozen/manifest.json')
 params=read(ART/'initial_model.json');gold=annotations('train' if development else 'test_gold');prefix=manifest['prefix'];records=[]
 for i,c in enumerate(manifest['contexts']):
  for rep in manifest['replicates']:
   prepared=initial(c,i,rep,prefix);methods=manifest['methods'];rotation=(i+rep)%len(methods);order=methods[rotation:]+methods[:rotation]
   for method in order:
    r=episode(c,i,rep,prefix,method,params,prepared['answers'],gold[c['id']],2);records.append(dict(context_id=c['id'],rep=rep,method=method,path=str((ART/prefix/'runs'/('%s_r%d_%s_b2.json'%(c['id'],rep,method))).relative_to(ART))))
   print(prefix,'completed context',i+1,'rep',rep,flush=True);write(ART/prefix/'completed.json',records)
 if not development:
  for i,c in enumerate(manifest['contexts']):
   prepared=initial(c,i,0,prefix)
   if i<manifest['frozen_model_contexts']:episode(c,i,0,prefix,'frozen_model',params,prepared['answers'],gold[c['id']],2)
   if i<manifest['budget3_contexts']:
    for method in ['adaptive','fixed_audit']:episode(c,i,0,prefix,method,params,prepared['answers'],gold[c['id']],3)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--development',action='store_true');a=p.parse_args();collect(a.development)
