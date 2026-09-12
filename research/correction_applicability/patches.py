"""Inferred corrections and atomic, scope-checked revision. No private evaluator input."""
import copy,re
from .common import digest
from .representation import contract,evaluate,executed_answer,version,number,cell,period_evidence
from research.adaptive_correction_transfer.features import kind,words

REQUIRED={'refs','expression','op','scale','unit','entity','metric','periods','source_id','source_version'}
def complete(rep):return isinstance(rep,dict) and REQUIRED<=set(rep)
def rebind(c,rep):return rep

def compact_text(s):return ' '.join(re.findall(r'[a-z0-9]+',str(s).lower()))
def same_number(answer,rep,c):
 try:
  xs=answer['answer'] if isinstance(answer['answer'],list) else [answer['answer']]
  return len(xs)==1 and abs(number(xs[0])-evaluate(rep,c))<=.011 and answer['scale']==rep['scale']
 except Exception:return False

def infer(c,q,old,corrected,disclosure):
 a=old.get('rep');b=corrected.get('rep');out=dict(donor=q['id'],source_id=c['id'],source_version=version(c),question=q['question'],feedback=copy.deepcopy(disclosure),old_rep=copy.deepcopy(a),new_rep=copy.deepcopy(b),kind='local',supported=False,reasons=[],generalizes=[],protected=['source','recipient_question','metric','entity','periods','unaffected_refs'])
 if not complete(a) or not complete(b):out['reasons']=['missing_donor_representation'];return out
 try:evaluate(a,c)
 except Exception as e:out['reasons']=['unsupported_prior_computation:'+str(e)];return out
 if contract(c,q,b):out['reasons']=['corrected_donor_contract']+contract(c,q,b);return out
 if not same_number(disclosure,b,c):out['reasons']=['annotation_not_explained'];return out
 if same_number(disclosure,a,c):out['reasons']=['prior_computation_already_explains_annotation'];return out
 if a==b or (a.get('refs')==b.get('refs') and a.get('expression')==b.get('expression') and a.get('scale')==b.get('scale')):out['reasons']=['no_reusable_computation_change'];return out
 ar=a.get('refs',[]);br=b.get('refs',[])
 if len(ar)==len(br) and set(ar)==set(br):
  mapping={i:ar.index(ref) for i,ref in enumerate(br)};expr=re.sub(r'\bx(\d+)\b',lambda m:'x'+str(mapping[int(m[1])]),b['expression'])
  if expr!=a.get('expression') or b['op']!=a.get('op'):
   out.update(kind='operation',supported=True,from_expression=a['expression'],to_expression=expr,from_op=a['op'],to_op=b['op'],intent=kind(q['question']),generalizes=['periods with the same question operation and metric'],protected=['source','recipient_question','metric','entity','periods','refs','unit','scale'])
  elif b['scale']!=a.get('scale'):
   out.update(kind='scale',supported=True,from_scale=a['scale'],to_scale=b['scale'],generalizes=['period with same amount metric and source-unit evidence'],protected=['source','recipient_question','metric','entity','periods','refs','expression','op','unit'])
 elif len(ar)==len(br) and sum(x!=y for x,y in zip(ar,br))==1:
  x,y=next((x,y) for x,y in zip(ar,br) if x!=y);out.update(kind='fact_binding',supported=True,from_ref=x,to_ref=y,protected=['source','recipient_question','entity','unit','scale','expression','op'],generalizes=['only a recipient actually using this old source element; its own contract must support replacement'])
 if not out['supported']:out['reasons']=['multiple_or_unsupported_changes']
 out['id']=digest(out);return out

def propose(c,q,old,patch,check_scope=True):
 event=dict(patch_id=patch.get('id'),kind=patch['kind'],recipient=q['id'],accepted=False,reasons=[],before=copy.deepcopy(old),candidate=None,after=copy.deepcopy(old))
 def reject(reason):event['reasons']=sorted(set(event['reasons']+[reason]));return event
 if not patch.get('supported'):return reject('local_or_unsupported_patch')
 r=old.get('rep')
 if not complete(r):return reject('unsupported_recipient')
 if patch['source_id']!=c['id'] or patch['source_version']!=version(c) or r.get('source_version')!=version(c):return reject('source_version')
 try:evaluate(r,c)
 except Exception as e:return reject('unsupported_recipient:'+str(e))
 new=copy.deepcopy(r);a=patch['old_rep'];b=patch['new_rep']
 if patch['kind']=='operation':
  if len(r['refs'])!=len(a['refs']):return reject('operand_arity')
  if check_scope and (r['op']!=patch['from_op'] or re.sub(r'\s','',r['expression'])!=re.sub(r'\s','',patch['from_expression'])):return reject('operation_dependency')
  if check_scope and kind(q['question'])!=patch['intent']:return reject('different_question_operation')
  if check_scope and len(r['refs'])>1:
   def roles(rep):
    ys=[period_evidence(c,ref) for ref in rep['refs']]
    if not all(len(y)==1 for y in ys):return None
    years=[int(y[0]) for y in ys]
    if len(set(years))!=len(years):return None
    return [sorted(years).index(y) for y in years]
   if r['refs']!=a['refs'] and (roles(r) is None or roles(a) is None or roles(r)!=roles(a)):return reject('operand_role_mismatch_or_unknown')
  new.update(expression=patch['to_expression'],op=patch['to_op'])
 elif patch['kind']=='scale':
  if check_scope and (r['scale']!=patch['from_scale'] or r['unit']=='dimensionless'):return reject('scale_dependency')
  new['scale']=patch['to_scale']
 elif patch['kind']=='fact_binding':
  if patch['from_ref'] not in r['refs']:return reject('no_source_dependency')
  new['refs']=[patch['to_ref'] if x==patch['from_ref'] else x for x in r['refs']]
  # Source-derived binding metadata must follow the changed dependency; the question stays fixed.
  try:new=rebind(c,new)
  except Exception as e:return reject('binding_refresh:'+str(e))
 else:return reject('unknown_patch')
 if check_scope:
  if not words(r['metric'])&words(b['metric']):event['reasons'].append('different_metric')
  if compact_text(r['entity'])!=compact_text(b['entity']):event['reasons'].append('different_entity')
  if r['unit']!=b['unit']:event['reasons'].append('different_unit')
  if patch['kind']=='operation' and r['scale']!=b['scale']:event['reasons'].append('different_scale')
  event['reasons']+=contract(c,q,new)
  # Patches may never silently change a recipient's declared intent fields.
  for k in patch['protected']:
   if k in r and new[k]!=r[k]:event['reasons'].append('protected_'+k)
 try:
  cand=copy.deepcopy(old);cand['rep']=new;cand=executed_answer(cand,c);event['candidate']=cand
 except Exception as e:return reject('candidate_execution:'+str(e))
 if event['reasons']:return event
 if cand['answer']==old['answer'] and cand['scale']==old['scale']:return reject('no_answer_change')
 event.update(accepted=True,after=copy.deepcopy(cand));return event

def apply_to_state(c,questions,state,patch,inspected,check_scope=True):
 result=copy.deepcopy(state);events=[]
 for q in questions:
  if q['id'] in inspected:continue
  e=propose(c,q,state[q['id']],patch,check_scope);events.append(e)
  if e['accepted']:result[q['id']]=e['after']
 return result,events
