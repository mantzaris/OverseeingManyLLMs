"""No-inference package checks, including versioned replay and feedback isolation."""
import collections,copy,json
from .common import ART,read,write,stable,digest
from .backend import load
from .experiment import run,rank
from .replay import request_saved,RecordedInspector

def verify():
 cs=read(ART/'development_manifest.json')['contexts'];checked=0;guard_changed=[]
 for revision in ['v1','v2']:
  for i,c in enumerate(cs):
   initial=read(ART/f'development_{revision}/c{i:02d}_initial.json')['answers'];order=rank(c,initial)
   for p in sorted((ART/f'development_{revision}').glob(f'c{i:02d}_*.json')):
    if p.name.endswith('_initial.json'):continue
    r=read(p);assert r['initial']==initial;assert r['inspection_ids']==order;assert r['inspections']==2
    assert set(r['answers'])=={q['id'] for q in c['questions']}
    if r['method'] in ['patch','no_applicability']:
     for e in r['events']:
      for x in e['revisions']:
       if not x['accepted']:assert x['before']==x['after']
    checked+=1
   # The later schema guard must not be used to back-edit historical event reasons.
   if revision=='v2':
    engine=load('v2_guarded');qi={q['id']:n for n,q in enumerate(c['questions'])}
    for method in ['patch','no_applicability']:
     saved=read(ART/f'development_v2/c{i:02d}_{method}.json')
     def gen(mode,q,old,feedback,step):return request_saved('dev_v2_c%02d_%s_s%d_q%02d'%(i,mode,step,qi[q['id']]),c,q,941000+i*100+step*10+qi[q['id']],old,mode,feedback,engine)
     out=run(c,initial,order,RecordedInspector(saved['events']),gen,method,engine)
     assert out['answers']==saved['answers'];assert out['snapshots']==saved['snapshots'];assert out['calls']==saved['calls']
     if out['events']!=saved['events']:guard_changed.append(dict(source_index=i,method=method,terminal_outputs_identical=True,old_reasons=[e['patch']['reasons'] for e in saved['events']],guarded_reasons=[e['patch']['reasons'] for e in out['events']]))
 raw=[read(p) for p in (ART/'raw').glob('*.json')];intents=[json.loads(s) for s in (ART/'attempts.jsonl').read_text().splitlines()];assert len(raw)==720;assert len(intents)==sum(len(r['attempts']) for r in raw);assert not any(r['status']=='pending' for r in raw)
 for r in raw:assert len(r['attempts'])<=2;assert digest(r['request'])==r['request_sha256']
 log=ART/'interface/interactions.jsonl';shown=0
 if log.exists():
  for line in log.read_text().splitlines():
   r=json.loads(line);assert digest(r['displayed_state'])==r['state_sha256'];assert r['participant'] is False;assert 0<=r['displayed_state']['remaining']<=2;shown+=1
 write(ART/'verification.json',dict(passed=True,traces=checked,unique_scheduled_requests=len(raw),attempts=len(intents),rollback_checked=True,common_fixed_inspections=True,guarded_diagnostic_changed_events=guard_changed,guarded_diagnostic_changed_outcomes=0,logged_displays=shown,private_gold_used_for_online_checks=False));print('Verified',checked,'traces;',len(raw),'requests;',len(guard_changed),'guard-only diagnostic reason changes; no outcome changes.')
if __name__=='__main__':verify()
