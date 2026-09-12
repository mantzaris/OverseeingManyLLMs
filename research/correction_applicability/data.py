"""Source provenance and exclusion audit. Does not select cases by model performance."""
import hashlib
from pathlib import Path
from research.adaptive_correction_transfer.data import context,normalized,SOURCE
from research.adaptive_correction_transfer.answers import source_text
from .common import ART,OLD,ROOT,read,write,digest

def audit():
 provenance=read(OLD/'provenance.json')
 for f in provenance['files']:
  p=SOURCE/f['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],p
 historical=[OLD/'development_manifest.json',OLD/'frozen/manifest.json'];used={};tables=set();paras=set();manifest_records=[]
 for p in historical:
  m=read(p);manifest_records.append(dict(path=str(p.relative_to(ROOT)),sha256=digest(m)))
  for c in m['contexts']:
   used[c['id']]=str(p.relative_to(ROOT));tables.add(digest([[normalized(x) for x in row] for row in c['table']]));paras.update(normalized(p['text']) for p in c['paragraphs'] if len(normalized(p['text']))>=160)
 # Historical audit contexts are a subset of previous evaluation; no new source IDs are introduced.
 used_audit={e['context_id'] for e in read(ART/'historical_audit.json')['events']};assert used_audit<=set(used)
 records=[];available=[];seen={}
 for split in ['train','dev','test_gold']:
  for i,raw in enumerate(read(SOURCE/'dataset_raw'/('tatqa_dataset_'+split+'.json'))):
   c=context(raw,split,i);th=digest([[normalized(x) for x in row] for row in c['table']]);duplicate=seen.get(th);seen.setdefault(th,[split,i]);reason='previously_used_context' if c['id'] in used else 'duplicated_previous_table' if th in tables else 'duplicated_previous_long_paragraph' if any(normalized(p['text']) in paras for p in c['paragraphs'] if len(normalized(p['text']))>=160) else 'cross_split_table_duplicate' if duplicate else 'question_count' if not 4<=len(c['questions'])<=8 else 'source_length' if len(source_text(c))>3600 else None
   row=dict(id=c['id'],split=split,index=i,table_hash=th,reason=reason,questions=len(c['questions']),source_characters=len(source_text(c)));records.append(row)
   if reason is None and split=='test_gold':available.append(dict(id=c['id'],index=i,questions=len(c['questions'])))
 write(ART/'source_pool_audit.json',dict(previous_manifests=manifest_records,used_contexts=used,historical_audit_subset=True,records=records,unused_test_candidates=available,note='Availability audit only. Public source-order identifiers are not a frozen evaluation selection. No new source labels or model outcomes inspected here. Reliable report identifiers absent.'))
 print('Previously used contexts',len(used),'unused technically eligible test contexts',len(available))
if __name__=='__main__':audit()
