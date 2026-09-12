"""Empirical pairing, disclosure and raw-request integrity checks."""
import collections,copy,subprocess
from .common import ART,ROOT,read,write,digest
from .freeze import verify as verify_freeze
from .feedback import Inspector
from .answers import messages

def audit(partial=False):
 verify_freeze();m=read(ART/'frozen/manifest.json');gold=read(ART/'frozen/evaluator_annotations.json');checked=0;counter=collections.Counter();raws={p.stem:read(p) for p in (ART/'raw').glob('*.json')};attempts=[]
 for cid,r in raws.items():
  assert digest(r['request'])==r['request_sha256'];assert len(r['attempts'])<=2
  attempts.extend((cid,a['attempt']) for a in r['attempts'])
  for a in r['attempts']:
   assert a['request_sha256']==r['request_sha256']
   if cid.startswith('evaluation_'):assert a['started_utc']>=m['created_utc']
 frozen_time=subprocess.check_output(['git','show','-s','--format=%cI','18dbae40'],cwd=ROOT,text=True).strip()
 import datetime
 for r in raws.values():
  if r['call_id'].startswith('evaluation_'):
   for a in r['attempts']:assert datetime.datetime.fromisoformat(a['started_utc'])>=datetime.datetime.fromisoformat(frozen_time)
 for c in m['contexts']:
  for rep in m['replicates']:
   rs={}
   for method in m['methods']:
    p=ART/'evaluation/runs'/('%s_r%d_%s_b2.json'%(c['id'],rep,method))
    if p.exists():rs[method]=read(p)
    elif not partial:raise AssertionError('Missing '+str(p))
   if len(rs)!=len(m['methods']):continue
   fixed=['individual','memory','source_rule','fixed_audit','reattempt'];seqs=[[e['inspected'] for e in rs[k]['events']] for k in fixed];assert all(s==seqs[0] for s in seqs)
   disclosure=[[e['disclosure'] for e in rs[k]['events']] for k in fixed];assert all(s==disclosure[0] for s in disclosure)
   assert [e['recipients'] for e in rs['source_rule']['events']]==[e['recipients'] for e in rs['reattempt']['events']]
   for method,r in rs.items():
    seen=[]
    for e in r['events']:
     seen.append(e['inspected']);permitted=Inspector(gold[c['id']],2).inspect(next(q for q in c['questions'] if q['id']==e['inspected']));f=copy.deepcopy(e['disclosure']);f.pop('previous');assert f==permitted
     assert all(u['question'] in seen for u in e['updates']);assert not(set(h['id'] for h in e['repairs'])&set(seen));counter['inspections']+=1
     for h in e['repairs']:
      if not h['accepted']:assert h['after']==h['before'];counter['retained_failed_repairs']+=1
      counter['repair_events']+=1
    assert r['inspections']==2
   checked+=1
 out=dict(passed=True,paired_source_replicas=checked,raw_requests=len(raws),attempt_records=len(attempts),freeze_commit='18dbae40',counter=dict(counter),rules='Identical fixed inspection disclosures; identical source-rule/reattempt recipients; every update uses acquired question; failed repair retains prior; inspected outputs protected; raw payload hashes and post-commit timing.');write(ART/'integrity_audit.json',out);print(out)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--partial',action='store_true');a=p.parse_args();audit(a.partial)
