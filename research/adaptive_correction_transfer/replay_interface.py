"""Verify saved displayed states for the scripted inspection walkthrough."""
import json
from .common import ART,read,write,digest
from .prototype.server import Desk

def verify():
 p=ART/'interface/interactions.jsonl';records=[json.loads(x) for x in p.read_text().splitlines()];desk=Desk('/tmp/unused-adaptive-interface-replay.jsonl');contexts={c['id']:c for c in read(ART/'frozen/manifest.json')['contexts']};count=0
 for e in records:
  action=e['action'];payload=e['payload'];sid=payload.get('session')
  if action=='shown_initial':
   c=contexts[payload['context']];r=read(ART/'evaluation/runs'/('%s_r0_%s_b2.json'%(c['id'],payload['method'])));desk.sessions[sid]=dict(context=c,run=r,step=0)
  elif action=='inspect_and_replay_transfer':
   assert desk.sessions[sid]['step']+1==payload['step'];desk.sessions[sid]['step']+=1;assert desk.sessions[sid]['step']<=2
  else:continue
  state=desk.state(sid);assert digest(state)==e['display_sha256'],action;count+=1
 result=dict(passed=True,displayed_states=count,sessions=len(desk.sessions),participant_observations=0);write(ART/'interface/replay.json',result);print(result)
if __name__=='__main__':verify()
