"""Secondary diagnostics on the frozen trajectories; no policy updates."""
import collections,json,re
import numpy as np,pandas as pd
from .common import ART,read,write,digest
from .scoring import score
from .client import parsed
from .answers import prepare
from .results import csvout

def analyze():
 m=read(ART/'frozen/manifest.json');gold=read(ART/'frozen/evaluator_annotations.json');initial=[];transitions=[];feedback=[];ctx={c['id']:c for c in m['contexts']}
 for c in m['contexts']:
  for rep in m['replicates']:
   p=ART/'evaluation/initial'/('%s_r%d.json'%(c['id'],rep))
   if not p.exists():continue
   r=read(p)
   for q in c['questions']:
    a=r['answers'][q['id']];s=score(a,gold[c['id']][q['id']]);initial.append(dict(context=c['id'],rep=rep,question=q['id'],**s,valid=a.get('valid',False),usable_evidence=len(a.get('evidence',[])),invalid_citations=len(a.get('invalid_evidence',[])),operation=a.get('operation','other'),derivation_present=bool(a.get('derivation')),requested_fields_present=bool(a.get('valid') and a.get('evidence') and a.get('derivation') and a.get('operation') in ['lookup','sum','difference','average','ratio','count','other'])))
   for method in m['methods']:
    p=ART/'evaluation/runs'/('%s_r%d_%s_b2.json'%(c['id'],rep,method))
    if not p.exists():continue
    r=read(p)
    for e in r['events']:
     dg=gold[c['id']][e['inspected']];donor_initial=score(r['snapshots'][0][e['inspected']],dg)['em'];donor_current=score(e['current_before'],dg)['em']
     feedback.append(dict(context=c['id'],rep=rep,method=method,step=e['step'],donor_initial_correct=donor_initial,donor_current_correct=donor_current,reused=bool(e['repairs']),recipients=len(e['repairs'])))
     for h in e['repairs']:
      g=gold[c['id']][h['id']];before=score(h['before'],g);after=score(h['after'],g)
      transitions.append(dict(context=c['id'],rep=rep,method=method,step=e['step'],donor=e['inspected'],recipient=h['id'],donor_initial_correct=donor_initial,donor_current_correct=donor_current,help=int(after['em']>before['em']),harm=int(after['em']<before['em']),scale_fixed=int(after['scale']>before['scale']),scale_harmed=int(after['scale']<before['scale']),relation=h['relation']['bin']))
 signatures=collections.defaultdict(list)
 for p in sorted((ART/'raw').glob('evaluation_*.json')):
  r=read(p)
  if r['status']!='ok':continue
  x=parsed(r);key=digest(dict(answer=x.get('answer'),scale=x.get('scale'))) if isinstance(x,dict) else 'malformed';ci=int(re.search(r'evaluation_c(\d+)',r['call_id']).group(1));qn=int(re.search(r'_q(\d+)(?:_|$)',r['call_id']).group(1));cc=m['contexts'][ci];qq=cc['questions'][qn];metric=score(prepare(x,cc),gold[cc['id']][qq['id']])
  signatures[r['request_sha256']].append(dict(call_id=r['call_id'],output_signature=key,em=metric['em'],f1=metric['f1']))
 duplicates=[dict(request_sha256=k,requests=v,variants=len({r['output_signature'] for r in v})) for k,v in signatures.items() if len(v)>1]
 csvout(ART/'analysis/initial_answers.csv',initial);csvout(ART/'analysis/transfer_types.csv',transitions);csvout(ART/'analysis/feedback.csv',feedback)
 i=pd.DataFrame(initial);out=dict(initial_answers=len(initial),initial_em=float(i.em.sum()),initial_f1=float(i.f1.sum()),initial_scale=int(i.scale.sum()),initial_joint=int(i.joint.sum()),initial_unfinished=int(i.unfinished.sum()),initial_valid=int(i.valid.sum()),initial_with_usable_evidence=int((i.usable_evidence>0).sum()),initial_derivation_present=int(i.derivation_present.sum()),initial_requested_fields_present=int(i.requested_fields_present.sum()),duplicate_request_groups=len(duplicates),varying_answer_scale_groups=sum(d['variants']>1 for d in duplicates),varying_em_groups=sum(len({r['em'] for r in d['requests']})>1 for d in duplicates),duplicates=duplicates,interpretation='Identical requests use the same model, full messages, decoding and seed; different returns are retained. Requests with changed disclosures or histories are not identical. This diagnostic adds no generations. Co-occurring errors alone do not identify a shared root cause.')
 write(ART/'analysis/mechanisms.json',out);print({k:v for k,v in out.items() if k not in ['duplicates','interpretation']})
if __name__=='__main__':analyze()
