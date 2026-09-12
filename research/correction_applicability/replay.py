"""Exact saved-request and state replay using only recorded inspection disclosures."""
import copy
from .common import ART,OLD,read,write,digest,stable
from .backend import load
from .experiment import run,rank
from .transport import parsed,MODEL
class RecordedInspector:
 def __init__(self,events):self.events=[e for e in events if e['kind']=='inspection'];self.used=0
 def inspect(self,q):
  if self.used>=2:raise RuntimeError('Budget')
  e=self.events[self.used];assert e['inspected']==q['id'];self.used+=1;f=copy.deepcopy(e['disclosure']);f.pop('previous',None);return f

def request_saved(call_id,c,q,seed,old,mode,feedback,engine):
 raw=read(ART/'raw'/(call_id+'.json'));payload=dict(model=MODEL,messages=engine.messages(c,q,old,mode,feedback),temperature=.3,top_p=1.,max_tokens=440,seed=seed,response_format={'type':'json_object'});assert digest(payload)==raw['request_sha256'],call_id
 u=dict(call_id=call_id,request_sha256=raw['request_sha256'],status=raw['status'],attempts=len(raw['attempts']),tokens=sum(a.get('response',{}).get('usage',{}).get('total_tokens',0) for a in raw['attempts']),seconds=sum(a['elapsed_seconds'] for a in raw['attempts']));return engine.parse(parsed(raw),c),u

def replay(revision='v1',partial=False):
 engine=load(revision);cs=read(ART/'development_manifest.json')['contexts'];count=0;requests=set()
 for i,c in enumerate(cs):
  p=ART/('development_'+revision)/('c%02d_initial.json'%i)
  if not p.exists():continue
  saved=read(p);old=read(OLD/'development_v4'/('c%02d.json'%i))['initial'];actual={};uses=[]
  for n,q in enumerate(c['questions']):
   callid='dev_'+revision+'_c%02d_q%02d_extract'%(i,n);a,u=request_saved(callid,c,q,931000+i*100+n,old[q['id']],'extract',None,engine);requests.add(callid);b=copy.deepcopy(old[q['id']]);b.update({k:a[k] for k in ['rep','representation_errors','representation_valid']});b['extraction_proposal']=a;actual[q['id']]=b;uses.append(u)
  assert actual==saved['answers'];assert uses==saved['calls'];order=rank(c,actual);qi={q['id']:n for n,q in enumerate(c['questions'])}
  for p in sorted((ART/('development_'+revision)).glob('c%02d_*.json'%i)):
   if p.name.endswith('_initial.json'):continue
   r=read(p)
   def gen(mode,q,old,feedback,step):
    callid='dev_'+revision+'_c%02d_%s_s%d_q%02d'%(i,mode,step,qi[q['id']]);requests.add(callid);return request_saved(callid,c,q,941000+i*100+step*10+qi[q['id']],old,mode,feedback,engine)
   a=run(c,actual,order,RecordedInspector(r['events']),gen,r['method'],engine);a['source_index']=i;assert stable(a)==stable(r),p;count+=1
 if not partial:assert count==len(cs)*7,(count,len(cs)*7)
 out=dict(passed=True,revision=revision,traces=count,unique_requests=len(requests),private_sibling_annotations_loaded=False);write(ART/('replay_'+revision+'.json'),out);print(out);return out
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--revision',default='v1');p.add_argument('--partial',action='store_true');a=p.parse_args();replay(a.revision,a.partial)
