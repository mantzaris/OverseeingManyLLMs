"""Verify the frozen preparation and saved logical traces, without inference."""
import hashlib,json
from research.oversight_workflow.common import ROOT,read,digest
from research.oversight_workflow.protocol import replay
from .materials import PILOT,OUT

def main():
 f=read(OUT/'preparation_freeze.json')
 for rel,expected in f['files'].items():
  if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=expected:raise ValueError('Preparation changed: '+rel)
 m=read(PILOT/'manifest.json');given=m.pop('manifest_sha256')
 if digest(m)!=given or given!=f['manifest_sha256']:raise ValueError('Manifest digest mismatch')
 # Include preserved pre-collection attempts under their original protocol states.
 counts={}
 for p in sorted((OUT/'test_data').rglob('*.pilot.json')):
  r=read(p)
  if r['record_kind']!='software_fixture':raise ValueError('Non-fixture in software test namespace')
  for s in r['sessions']:
   d=replay(s['events'],s['desk_condition'])
   if d.logical()!=s['state']:raise ValueError('Logical replay mismatch')
  counts[str(p.relative_to(ROOT))]=dict(blocks=len(r['sessions']),events=sum(len(s['events']) for s in r['sessions']))
 print(json.dumps(dict(freeze='verified',manifest_sha256=given,saved_fixture_replay=counts,human_observations=0,new_inference=0),indent=2))
if __name__=='__main__':main()
