"""Bounded acquisitions with selective, fallible transfer. No all-output gold access."""
import copy,random,time
from .common import digest
from .learner import Learner
from .features import relation,fixed_eligible
from .feedback import verified_answer
from .scoring import score
METHODS=['individual','memory','source_rule','fixed_audit','adaptive','reattempt','individual_risk']

def run(c,initial,params,inspector,generate_fn,seed,method='adaptive',budget=2,call_limit=None):
 start=time.monotonic();qs={q['id']:q for q in c['questions']};answers=copy.deepcopy(initial);learner=Learner(params,learn=method in ['adaptive','fixed_audit']);observations=[];history={q:[] for q in qs};audited=[];corrections=[];events=[];calls=[];rng=random.Random(seed);max_calls=call_limit if call_limit is not None else budget*(len(qs)-1)
 def errors():return {qid:learner.error(q,initial,qs,observations,history[qid]) for qid,q in qs.items()}
 def candidates(donor,e):
  result=[]
  for qid,q in qs.items():
   if qid in audited or qid==donor:continue
   rel=relation(qs[donor],answers[donor],q,answers[qid]);gain=learner.gain(e[qid],rel)
   result.append(dict(id=qid,relation=rel,gain=gain,predicted_before_error=e[qid]))
  return sorted(result,key=lambda x:(-x['gain'],qs[x['id']]['order'],x['id']))
 def audit_ranking(e):
  rows=[]
  for qid in qs:
   if qid in audited:continue
   extra=sum(max(0,x['gain']) for x in candidates(qid,e)[:params['recipient_cap']]);rows.append(dict(id=qid,expected_gain=e[qid]+extra,error=e[qid],expected_transfer=extra))
  return sorted(rows,key=lambda x:(-x['expected_gain'],qs[x['id']]['order'],x['id']))
 static_rank=audit_ranking(errors());static_ids=[x['id'] for x in static_rank]
 if method=='individual_risk':static_ids=sorted(qs,key=lambda q:(-learner.base(qs[q],initial[q]),qs[q]['order'],q))
 snapshots=[copy.deepcopy(answers)]
 for step in range(min(budget,len(qs))):
  e=errors();rank=audit_ranking(e);available=[x for x in static_ids if x not in audited]
  adaptive=method in ['adaptive','frozen_model'];top=rank[0]['id'] if adaptive else available[0]
  # Common randomized first choice; later randomization applies only to adaptive acquisition.
  explore=(step==0 or adaptive) and rng.random()<params['epsilon'];qid=sorted(qs.keys()-set(audited))[rng.randrange(len(available))] if explore else top
  prob=(params['epsilon']/len(available)+(1-params['epsilon'] if qid==top else 0)) if (step==0 or adaptive) else 1.
  if step==0 and not adaptive:static_ids=[qid]+[x for x in static_ids if x!=qid]
  q=qs[qid];before=copy.deepcopy(answers[qid]);f=inspector.inspect(q);f['previous']={k:initial[qid].get(k) for k in ['answer','scale','evidence','operation']};audited.append(qid);original_error=int(1-score(initial[qid],f)['em']);current_error=int(1-score(before,f)['em'])
  measured=[]
  for h in history[qid]:measured.append(dict(h,before_error=int(1-score(h['before'],f)['em']),after_error=int(1-score(h['after'],f)['em'])))
  learner.update_inspection(q,initial[qid],original_error,current_error,measured)
  for obs in observations:learner.update_pair(qs[obs['id']],q,initial,obs['original_error'],original_error)
  observations.append(dict(id=qid,original_error=original_error,current_error=current_error,step=step));corrections.append(f);answers[qid]=verified_answer(f)
  # Recipient relations use the inspected pre-replacement proposal, since verified answers have no gold evidence map.
  verified=answers[qid];answers[qid]=before;e=errors();options=candidates(qid,e);answers[qid]=verified
  if method in ['individual','individual_risk']:selected=[]
  elif method=='memory':selected=options
  elif method in ['source_rule','reattempt']:
   eligible=[x for x in options if fixed_eligible(relation(q,initial[qid],qs[x['id']],initial[x['id']]))]
   selected=sorted(eligible,key=lambda x:(-relation(q,initial[qid],qs[x['id']],initial[x['id']])['evidence_overlap'],-relation(q,initial[qid],qs[x['id']],initial[x['id']])['lexical_similarity'],qs[x['id']]['order'],x['id']))[:params['recipient_cap']]
  else:selected=[x for x in options if x['gain']>0][:params['recipient_cap']]
  event=dict(step=step+1,inspected=qid,selection_probability=prob,exploration=explore,audit_ranking=rank,disclosure=f,current_before=before,observations=copy.deepcopy(observations),model_after=digest(learner.params),updates=copy.deepcopy(learner.updates),candidates=options,recipients=[x['id'] for x in selected],repairs=[])
  for x in selected:
   if len(calls)>=max_calls:break
   j=x['id'];old=copy.deepcopy(answers[j]);new,u=generate_fn(qs[j],old,corrections,step,method=='reattempt');calls.append(u)
   accepted=new.get('valid',False)
   if accepted:answers[j]=new
   h=dict(donor=qid,relation=x['relation'],predicted_before_error=x['predicted_before_error'],before=old,after=copy.deepcopy(answers[j]),proposal=new,accepted=accepted);history[j].append(h);event['repairs'].append(dict(h,id=j,usage=u))
  events.append(event);snapshots.append(copy.deepcopy(answers))
 return dict(context_id=c['id'],method=method,seed=seed,budget=budget,inspections=len(audited),calls=calls,events=events,snapshots=snapshots,answers=answers,learner=learner.params,updates=learner.updates,seconds=time.monotonic()-start)
