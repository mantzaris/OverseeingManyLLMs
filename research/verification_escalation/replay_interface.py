"""Replay actually displayed authored desk interactions, excluding clock latency."""
from .desk import Desk,strip_time
from .common import ART,read,write_json,digest
import json

def run(path=None):
 path=path or ART/'interface/interactions.jsonl';events=[json.loads(s) for s in path.read_text().splitlines()];d=None;n=0
 for e in events:
  if e['action']=='started':d=Desk()
  else:d.act(e['payload'])
  if digest(strip_time(d.state()))!=e['state_hash']:raise AssertionError('Displayed replay differs at '+str(n)+' '+e['action'])
  if strip_time(d.state()['question'])!=e['shown']:raise AssertionError('Question differs')
  n+=1
 out=dict(status='passed',interactions=n,participant_data=False);write_json(ART/'interface/replay_verification.json',out);print(out);return out
if __name__=='__main__':run()
