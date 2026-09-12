"""Fixed inspections with paired controls. Private annotations enter only Inspector."""
import copy,time
from research.adaptive_correction_transfer.learner import Learner
from research.adaptive_correction_transfer.feedback import Inspector,verified_answer
from research.adaptive_correction_transfer.data import annotations
from .common import ART,OLD,read,write,digest,stable
from .representation import messages,parse,contract,executed_answer
from .patches import infer,apply_to_state
from .transport import request
METHODS=['individual','execute','reattempt','verify','coarse','patch','no_applicability']

def rank(c,initial):
 model=Learner(read(OLD/'initial_model.json'),learn=False)
 return [q['id'] for q in sorted(c['questions'],key=lambda q:(-model.base(q,initial[q['id']]),q['order'],q['id']))][:2]

def generate(cid,c,q,seed,old,mode,feedback=None,engine=None):
 from .backend import load
 engine=engine or load('v1')
 p,u=request(cid,engine.messages(c,q,old,mode,feedback),seed);return engine.parse(p,c),u

def run(c,initial,inspection_ids,inspector,generate_fn,method,engine=None):
 from .backend import load
 engine=engine or load('v1');contract=engine.contract;executed_answer=engine.executed_answer;infer=engine.infer;apply_to_state=engine.apply_to_state
 start=time.monotonic();state=copy.deepcopy(initial);questions={q['id']:q for q in c['questions']};calls=[];events=[];seen=[];feedbacks=[];snapshots=[copy.deepcopy(state)]
 # Independent execution/verification policies operate on every not-to-be-inspected output,
 # selected without correction information. This is a fixed budget-two protocol.
 if method in ['execute','verify']:
  revisions=[]
  for q in c['questions']:
   if q['id'] in inspection_ids:continue
   old=copy.deepcopy(state[q['id']]);candidate=copy.deepcopy(old);usage=None
   if method=='verify':candidate,usage=generate_fn('verify',q,old,None,0);calls.append(usage)
   reasons=contract(c,q,candidate.get('rep'))
   if not reasons:
    try:candidate=executed_answer(candidate,c)
    except Exception as e:reasons.append('execution:'+str(e))
   if method=='verify' and reasons==['unsupported_representation'] and getattr(engine,'supported_spans',lambda c,a:False)(c,candidate):reasons=[]
   if not reasons:state[q['id']]=candidate
   revisions.append(dict(recipient=q['id'],before=old,candidate=candidate,after=copy.deepcopy(state[q['id']]),accepted=not reasons,reasons=reasons,usage=usage))
  events.append(dict(kind='independent_verification',revisions=revisions))
 for step,qid in enumerate(inspection_ids):
  q=questions[qid];f=inspector.inspect(q);f['previous']={k:initial[qid].get(k) for k in ['answer','scale','derivation']};before=copy.deepcopy(state[qid]);state[qid]=verified_answer(f);seen.append(qid);feedbacks.append(f)
  event=dict(kind='inspection',step=step+1,inspected=qid,disclosure=f,before=before,revisions=[],patch=None)
  if method in ['patch','no_applicability']:
   corrected,u=generate_fn('corrected',q,initial[qid],f,step);calls.append(u);patch=infer(c,q,initial[qid],corrected,f);event.update(patch=patch,corrected_representation=corrected,usage=u)
   state,revisions=apply_to_state(c,c['questions'],state,patch,seen,method=='patch');event['revisions']=revisions
  elif method in ['coarse','reattempt']:
   for j in c['questions']:
    if j['id'] in seen:continue
    old=copy.deepcopy(state[j['id']]);new,u=generate_fn(method,j,old,feedbacks if method=='coarse' else None,step);calls.append(u);accepted=new.get('valid',False)
    if accepted:state[j['id']]=new
    event['revisions'].append(dict(recipient=j['id'],before=old,candidate=new,after=copy.deepcopy(state[j['id']]),accepted=accepted,reasons=[] if accepted else ['invalid_answer'],usage=u))
  events.append(event);snapshots.append(copy.deepcopy(state))
 return dict(context_id=c['id'],method=method,inspection_ids=inspection_ids,inspections=len(seen),initial=initial,answers=state,events=events,snapshots=snapshots,calls=calls,seconds=time.monotonic()-start)

def pilot(revision='v1',limit=12):
 from .backend import load
 engine=load(revision)
 contexts=read(ART/'development_manifest.json')['contexts'][:limit];gold=annotations('train')
 for i,c in enumerate(contexts):
  path=ART/('development_'+revision)/('c%02d_initial.json'%i)
  if path.exists():initial=read(path)['answers']
  else:
   old=read(OLD/'development_v4'/('c%02d.json'%i))['initial'];initial={};calls=[]
   for n,q in enumerate(c['questions']):
    extracted,u=generate('dev_'+revision+'_c%02d_q%02d_extract'%(i,n),c,q,931000+i*100+n,old[q['id']],'extract',engine=engine);a=copy.deepcopy(old[q['id']]);a.update({k:extracted[k] for k in ['rep','representation_errors','representation_valid']});a['extraction_proposal']=extracted;initial[q['id']]=a;calls.append(u)
   write(path,dict(context_id=c['id'],answers=initial,calls=calls,original_initial_source='adaptive_correction_transfer/development_v4/c%02d.json'%i))
  order=rank(c,initial);qindex={q['id']:n for n,q in enumerate(c['questions'])}
  for method in METHODS:
   output=ART/('development_'+revision)/('c%02d_%s.json'%(i,method))
   if output.exists():continue
   def gen(mode,q,old,feedback,step):
    callid='dev_'+revision+'_c%02d_%s_s%d_q%02d'%(i,mode,step,qindex[q['id']]);return generate(callid,c,q,941000+i*100+step*10+qindex[q['id']],old,mode,feedback,engine=engine)
   result=run(c,initial,order,Inspector(gold[c['id']],2),gen,method,engine);result['source_index']=i;write(output,result)
  print('Completed development context',i+1,'/',limit,flush=True)
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--revision',default='v1');p.add_argument('--limit',type=int,default=12);a=p.parse_args();pilot(a.revision,a.limit)
