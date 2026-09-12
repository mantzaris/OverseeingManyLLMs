"""Reconstruct public prompts and controller transitions without private sibling labels."""
import copy,hashlib,time,statistics
from .common import ART,read,write,digest,stable
from .answers import messages,prepare
from .client import parsed,MODEL
from .controller import run
class RecordedInspector:
 def __init__(self,events,budget):self.events=events;self.used=0;self.budget=budget
 def inspect(self,q):
  if self.used>=self.budget:raise RuntimeError('Replay budget')
  e=self.events[self.used];assert q['id']==e['inspected'],'Different online inspection';self.used+=1
  f=copy.deepcopy(e['disclosure']);f.pop('previous',None);return f

def saved_request(call_id,c,q,seed,current=None,corrections=None,retry=False):
 raw=read(ART/'raw'/(call_id+'.json'));payload=dict(model=MODEL,messages=messages(c,q,current,corrections,retry),temperature=.3,top_p=1.,max_tokens=288,seed=seed,response_format={'type':'json_object'})
 assert digest(payload)==raw['request_sha256'],call_id+' prompt mismatch';a=prepare(parsed(raw),c)
 usage=dict(call_id=call_id,request_sha256=raw['request_sha256'],status=raw['status'],attempts=len(raw['attempts']),tokens=sum(x.get('response',{}).get('usage',{}).get('total_tokens',0) for x in raw['attempts']),seconds=sum(x.get('elapsed_seconds',0) for x in raw['attempts']))
 return a,usage

def verify(prefix='evaluation',partial=False):
 m=read(ART/'frozen/manifest.json') if prefix=='evaluation' else read(ART/'development_manifest.json');contexts={c['id']:c for c in m['contexts']};params=read(ART/'initial_model.json');traces=0;requests=set();errors=[];durations=[];start=time.monotonic()
 for path in sorted((ART/prefix/'initial').glob('*.json')):
  r=read(path);c=contexts[r['context_id']];i=next(i for i,x in enumerate(m['contexts']) if x['id']==c['id']);answers={};calls=[]
  for n,q in enumerate(c['questions']):
   cid='%s_c%02d_r%d_q%02d_initial'%(prefix,i,r['rep'],n);a,u=saved_request(cid,c,q,861000+i*100+r['rep']*10+n);answers[q['id']]=a;calls.append(u);requests.add(cid)
  assert answers==r['answers'] and calls==r['calls'],path
 for path in sorted((ART/prefix/'runs').glob('*.json')):
  saved=read(path);c=contexts[saved['context_id']];i=saved['source_index'];rep=saved['rep'];method=saved['method'];initial=read(ART/prefix/'initial'/('%s_r%d.json'%(c['id'],rep)))['answers'];qi={q['id']:n for n,q in enumerate(c['questions'])}
  def generate(q,old,corrections,step,retry):
   n=qi[q['id']];cid='%s_c%02d_r%d_%s_s%d_q%02d'%(prefix,i,rep,method,step,n);requests.add(cid)
   return saved_request(cid,c,q,871000+i*100+rep*30+step*10+n,old,None if retry else corrections,retry)
  actual=run(c,initial,params,RecordedInspector(saved['events'],saved['budget']),generate,881000+i*100+rep,method,saved['budget']);actual.update(rep=rep,source_index=i);durations.append(actual['seconds'])
  if stable(actual)!=stable(saved):errors.append(dict(path=path.name,different=[k for k in saved if stable(actual.get(k))!=stable(saved[k])]))
  traces+=1
 result=dict(prefix=prefix,traces=traces,unique_reconstructed_requests=len(requests),errors=errors,passed=not errors,private_annotations_used=False,replay_wall_seconds=time.monotonic()-start,median_trace_replay_ms=1000*statistics.median(durations) if durations else None,p95_trace_replay_ms=1000*sorted(durations)[int(.95*len(durations))] if durations else None,timing_scope='Controller, official scoring of purchased feedback, saved-request disk reads and prompt/parse reconstruction; excludes GPU inference.')
 if prefix=='evaluation' and not partial:
  expected=len(m['contexts'])*len(m['replicates'])*len(m['methods'])+m['frozen_model_contexts']+2*m['budget3_contexts'];result['expected_traces']=expected
  assert traces==expected,(traces,expected)
 write(ART/('replay_'+prefix+'.json'),result);assert not errors,errors[:3];print(result)
 return result
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--prefix',default='evaluation');p.add_argument('--partial',action='store_true');a=p.parse_args();verify(a.prefix,a.partial)
