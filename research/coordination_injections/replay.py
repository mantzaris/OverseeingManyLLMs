"""Reconstruct actual displayed prompts, tool executions and routing without inference."""
import argparse,copy
from .common import ART,read,write,stable,digest
from .controller import run
from .agents import messages
from .client import parsed,MODEL
from .pipeline import pipeline
from .evaluate import score

def saved_call(key,role,project,epoch,old,upstream,issues,seed,style,delivery):
 saved=read(ART/'raw'/(key+'.json'))
 payload=dict(model=MODEL,messages=messages(role,project,epoch,old,upstream,issues,style,delivery),temperature=.3,top_p=1.,max_tokens=384,seed=seed,response_format={'type':'json_object'})
 if digest(payload)!=saved['request_sha256']:raise AssertionError('Prompt or seed differs: '+key)
 return parsed(saved),dict(call_id=key,status=saved['status'],request_sha256=saved['request_sha256'],attempts=len(saved['attempts']),tokens=sum(a.get('response',{}).get('usage',{}).get('total_tokens',0) for a in saved['attempts']),seconds=sum(a['elapsed_seconds'] for a in saved['attempts']))
def verify(split='evaluation',revision='frozen',output=None):
 manifest=read(ART/'frozen/manifest.json');projects={p['id']:p for p in manifest[split]};root=ART/split/revision;count=0;calls=0;errors=[]
 for path in sorted(root.glob('**/*.json')):
  if path.name.endswith('summary.json'):continue
  saved=read(path)
  if not isinstance(saved,dict) or 'artifacts' not in saved:continue
  project=projects[saved['project_id']];initial=None
  if saved['epoch']:initial=read(root/(project['id']+'_r'+str(saved['rep'])+'_initial.json'))['artifacts']
  if saved['method']=='pipeline':actual=pipeline(project,saved['rep'],initial)
  else:actual=run(project,saved['rep'],saved['method'],initial,saved_call,phase=split+'_'+revision,stress=None if saved['stress']=='ordinary' else saved['stress'])
  if stable(actual)!=stable(saved):
   different=[k for k in saved if stable(actual.get(k))!=stable(saved[k])];errors.append(dict(path=str(path.relative_to(ART)),keys=different))
  if score(project,actual,initial)['project_correct']!=score(project,saved,initial)['project_correct']:raise AssertionError('Replay score mismatch')
  count+=1;calls+=len(saved['calls'])
  if count%20==0:print('replayed',count,flush=True)
 out=dict(split=split,revision=revision,traces=count,reconstructed_call_prompts=calls,errors=errors,passed=not errors)
 write(output or ART/('replay_'+split+'_'+revision+'.json'),out)
 if errors:raise AssertionError(errors[:3])
 print(out);return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--split',default='evaluation');p.add_argument('--revision',default='frozen');a=p.parse_args();verify(a.split,a.revision)
