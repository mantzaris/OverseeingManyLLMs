"""Disjoint follow-up after discovering the blanket unordered-contract defect."""
import ast,re,json,hashlib
from collections import defaultdict
from .common import ART as BASE,read,write_json,digest
from .data import load,compact,intent_index
ART=BASE/'repair'
ORDER_PATTERN=r'\b(?:sort(?:ed|ing)?|rank(?:ed|ing)?)\b|\border(?:ed)?\s+by\b|\b(?:ascending|descending|alphabetical|chronological|increasing|decreasing|highest|lowest|shortest|longest)\b|\btop\s+\d+'

def select():
 old=read(BASE/'private/cases.json');excluded={c['db'] for group in old.values() for c in group};groups=defaultdict(list)
 for r in load():groups[(r['db_file'],r['ambig_question'])].append(r)
 available=[];seen=set();exclusions=[]
 for (db,q),group in groups.items():
  if db in excluded or db in seen:continue
  amb=next((r for r in group if r['question_type']=='ambig' and r['split']=='test'),None)
  if not amb:continue
  refs=ast.literal_eval(amb['ambig_queries']);clear=[]
  for sql in refs:
   r=next((r for r in group if r['question_type']=='unambig' and ''.join(r['gold_queries'].split()).lower()==''.join(sql.split()).lower()),None);clear.append(r['question'] if r else None)
  schema,fk=compact(amb['db_dump'])
  if not all(clear) or len(refs)>3 or len(schema)>4900:exclusions.append(db);continue
  seen.add(db);c=dict(id=amb[''],db=db,domain=amb['domain'],kind=amb['ambig_type'],split=amb['split'],question=q,schema=schema,snapshot=amb['db_dump'],refs=refs,clarifications=clear,foreign_key_violations=fk)
  offset=int(digest({'id':c['id'],'intent_seed':8301})[:8],16)%len(refs);c['intent_indices']=[offset,(offset+1)%len(refs)];available.append(c)
 cases=[]
 for kind in ['attachment','scope','vague']:cases.extend([c for c in available if c['kind']==kind][:8])
 assert len(cases)==24 and len({c['db'] for c in cases})==24 and not {c['db'] for c in cases}&excluded
 write_json(ART/'private/cases.json',dict(evaluation=cases))
 write_json(ART/'split_manifest.json',dict(evaluation=[{k:c[k] for k in ['id','db','domain','kind','split']} for c in cases],excluded_prior_databases=sorted(excluded),eligibility_exclusions=exclusions,rule='First eight remaining test databases per type in source CSV order, exclude all 57 previously used/inspected databases; no model outcome selection.',order_pattern=ORDER_PATTERN))
 return cases

def public_task(case,rep,recovery=False):
 from .data import public_task as original
 task=original(case,rep,recovery)
 text=task['request']+' '+(' '.join(s['text'] for s in task['sources']))
 task['contract']['ordered']=bool(re.search(ORDER_PATTERN,text,re.I))
 return task
if __name__=='__main__':print('Selected follow-up databases',len(select()))
