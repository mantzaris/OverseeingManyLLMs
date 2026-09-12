"""Source-order partitions; public projection excludes every answer annotation."""
import re,hashlib,subprocess,collections
from pathlib import Path
from .common import ART,read,write,digest
from .answers import source_text,messages
SOURCE=Path('/tmp/adaptive-transfer-sources/tat-qa')
REVISION='870accc41953dcde885aabeb963d94aabdc0fbc3'
def normalized(s):return ' '.join(re.findall(r'\w+',str(s).lower()))
def context(c,split,index):return dict(id=c['table']['uid'],source_split=split,source_index=index,table=c['table']['table'],paragraphs=[dict(order=p['order'],text=p['text']) for p in c['paragraphs']],questions=[dict(id=q['uid'],order=q['order'],question=q['question']) for q in c['questions']])
def audit():
 sources={s:read(SOURCE/'dataset_raw'/('tatqa_dataset_'+s+'.json')) for s in ['train','dev','test_gold']};table_seen={};texts_seen={};records=[];manifest={};selected={}
 for split,cs in sources.items():
  eligible=[]
  for i,c in enumerate(cs):
   pub=context(c,split,i);th=digest([[normalized(x) for x in row] for row in pub['table']]);fh=digest(normalized(source_text(pub)));prev=table_seen.get(th) or texts_seen.get(fh)
   table_seen.setdefault(th,[split,i]);texts_seen.setdefault(fh,[split,i]);n=len(pub['questions']);chars=len(source_text(pub));reason='duplicate_table_or_context' if prev else 'question_count' if not 4<=n<=8 else 'context_length' if chars>3600 else None
   records.append(dict(split=split,index=i,id=pub['id'],table_hash=th,context_hash=fh,questions=n,source_characters=chars,excluded=reason,duplicate_of=prev))
   if reason is None:eligible.append(pub)
  manifest[split]=dict(contexts=len(cs),questions=sum(len(c['questions']) for c in cs),eligible=len(eligible));selected[split]=eligible
 write(ART/'source_audit.json',dict(revision=REVISION,splits=manifest,contexts=records,report_identifiers='Raw contexts have table UUID and paragraph UUID, no report/company document identifier. Exact normalized table/context duplicate exclusion is conservative; nonidentical material from one report may remain.',license='Dataset CC BY 4.0 per upstream README; code MIT per LICENSE.',test_release='Labeled test_gold is public since Jan2024. 277 labeled contexts/1663 questions versus 278/1669 unlabeled; unavailable label group not imputed.'))
 files=[SOURCE/'dataset_raw'/('tatqa_dataset_'+s+'.json') for s in ['train','dev','test','test_gold']]+[SOURCE/x for x in ['README.md','LICENSE','tatqa_metric.py','tatqa_utils.py']]
 write(ART/'provenance.json',dict(repository='https://github.com/NExTplusplus/tat-qa',revision=REVISION,files=[dict(path=str(p.relative_to(SOURCE)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in files],metric_modification='Only relative tatqa_utils import; metric implementation otherwise unchanged.'))
 # Development only. Held-out source selection is frozen after feasibility without looking at its labels.
 write(ART/'development_manifest.json',dict(selection='First 12 eligible train contexts in released order; exact table/context duplicates excluded across released split order; 3600 source-character cap and 4-8 questions, independent of outputs.',contexts=selected['train'][:12]))
 write(ART/'eligible_public.json',selected);print(manifest)
def annotations(split):return {c['table']['uid']:{q['uid']:q for q in c['questions']} for c in read(SOURCE/'dataset_raw'/('tatqa_dataset_'+split+'.json'))}
if __name__=='__main__':audit()
