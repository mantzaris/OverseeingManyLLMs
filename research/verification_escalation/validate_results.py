"""Check complete declared rows, accounting identities, pairing and source isolation."""
from collections import Counter
from .common import ART,read,write_json
from .analyze import load
from .controller import METHODS
from .repair_data import public_task
from .repair_freeze import verify

def run():
 verify();root=ART/'repair';cases=read(root/'private/cases.json')['evaluation'];rows=load(root/'evaluation/episodes.csv');checks=[]
 manifest=read(root/'split_manifest.json');dbs={c['db'] for c in cases}
 assert len(dbs)==24 and not dbs&set(manifest['excluded_prior_databases']);checks.append('24 source databases disjoint from all 57 earlier cases')
 expected=set();source_cases=0
 for c in cases:
  for rep in [0,1]:
   p=read(root/'prepared'/('repair_evaluation_v2_'+c['id']+'_r'+str(rep)+'.json'))
   task=public_task(c,rep)
   assert all(k not in task for k in ['refs','clarifications','intent_indices','kind','domain'])
   assert task['sources']==[]
   conditions=['generated','reference_candidates']+(['source_recovery'] if 'recovery' in p else [])
   source_cases+=int('recovery' in p)
   for cond in conditions:
    for m in METHODS:
     for b in [0,1,2]:expected.add((c['id'],rep,cond,m,b))
 actual=[(r['id'],int(r['rep']),r['condition'],r['method'],int(r['budget'])) for r in rows]
 assert len(actual)==len(set(actual)) and set(actual)==expected
 assert len(rows)==3240 and source_cases==12;checks.append('All 3240 frozen condition rows present, unique, and paired')
 for r in rows:
  assert r['correct']+r['wrong']+r['unfinished']==1
  assert 0<=r['questions']<=r['budget'] and 0<=r['executions']<=24
  assert r['project_correct']==r['correct']
  assert r['loss']==4*r['wrong']+r['unfinished']
  assert r['incorrect_suppression']<=r['suppressed'] and r['incorrect_suppression']<=r['wrong']
 checks.append('Every planned task remains in outcome, budget and loss accounting')
 for c in cases:
  for rep in [0,1]:
   for cond in ['generated','reference_candidates']:
    for b in [0,1,2]:
     z=[r for r in rows if r['id']==c['id'] and r['rep']==rep and r['condition']==cond and r['budget']==b]
     a=next(r for r in z if r['method']=='recovery_completion');d=next(r for r in z if r['method']=='recovery_depth2')
     assert all(a[k]==d[k] for k in ['correct','wrong','unfinished','questions','loss'])
 checks.append('Depth-two and minimum-completion equivalence checked in every one-intent case')
 ledger=read(ART/'resource_ledger.json');assert ledger['scheduled_calls']==540 and ledger['attempts']==534
 generated=read(ART/'generation_manifest.json');repair=[r for r in generated if r['call_id'].startswith('repair_')]
 assert len(repair)==156 and sum(len(r['attempts']) for r in repair)==156
 checks.append('156 corrected follow-up calls; 540 session schedules and 534 GPU attempts')
 out=dict(status='passed',checks=checks,primary_source_units=24,replicates=48,policy_rows=3240,new_calls_during_audit=0)
 write_json(root/'validation.json',out);print(out);return out
if __name__=='__main__':run()
