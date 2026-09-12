"""Telescoping outcome accounting and parameter-ablation action comparison."""
import collections
from .common import ART,read,write
from .scoring import score
from .feedback import verified_answer
from .results import csvout

def analyze():
 gold=read(ART/'frozen/evaluator_annotations.json');rows=[];runs={};availability=[]
 for p in (ART/'evaluation/runs').glob('*.json'):
  r=read(p);g=gold[r['context_id']];initial=sum(score(a,g[q])['em'] for q,a in r['snapshots'][0].items());final=sum(score(a,g[q])['em'] for q,a in r['answers'].items());local=helped=harmed=0
  history=collections.Counter();known=0
  for e in r['events']:
   known+=history[e['inspected']]
   if r['budget']==2:availability.append(dict(context=r['context_id'],rep=r['rep'],method=r['method'],step=e['step'],available_transfer_labels=known))
   for h in e['repairs']:history[h['id']]+=1
   q=e['inspected'];local+=score(verified_answer(e['disclosure']),g[q])['em']-score(e['current_before'],g[q])['em']
   for h in e['repairs']:
    before=score(h['before'],g[h['id']])['em'];after=score(h['after'],g[h['id']])['em'];helped+=after>before;harmed+=after<before
  assert initial+local+helped-harmed==final,p
  rows.append(dict(context=r['context_id'],rep=r['rep'],method=r['method'],budget=r['budget'],initial=initial,local_correction_gain=local,helpful_events=helped,harmful_events=harmed,final=final));runs[(r['context_id'],r['rep'],r['method'],r['budget'])]=r
 checks=[]
 for (cid,rep,method,budget),r in runs.items():
  if method!='frozen_model':continue
  a=runs[(cid,rep,'adaptive',budget)];checks.append(dict(context=cid,inspections_differ=[e['inspected'] for e in a['events']]!=[e['inspected'] for e in r['events']],recipient_membership_differs=any(set(x['recipients'])!=set(y['recipients']) for x,y in zip(a['events'],r['events'])),recipient_order_differs=any(x['recipients']!=y['recipients'] for x,y in zip(a['events'],r['events']))))
 csvout(ART/'analysis/decomposition.csv',rows);csvout(ART/'analysis/feedback_availability.csv',availability);csvout(ART/'analysis/parameter_ablation_actions.csv',checks);write(ART/'analysis/decomposition_audit.json',dict(passed=True,traces=len(rows),ablation_episodes=len(checks),inspection_changes=sum(x['inspections_differ'] for x in checks),recipient_membership_changes=sum(x['recipient_membership_differs'] for x in checks),recipient_order_changes=sum(x['recipient_order_differs'] for x in checks)))
 print('Outcome identities checked:',len(rows))
if __name__=='__main__':analyze()
