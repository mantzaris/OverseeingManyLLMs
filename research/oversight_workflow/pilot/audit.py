"""Offline audit only. These rows and annotations never enter the pilot server."""
import csv
from collections import Counter,defaultdict
from research.oversight_workflow.common import ART,read,write,digest
from research.oversight_workflow.offline import labels
from research.oversight_workflow.transport import client
from research.adaptive_correction_transfer.scoring import score
from .adapter import normalize
from .materials import OUT

def main():
 m=read(ART/'frozen/manifest.json');gold=labels();rows=[];details=[]
 for c in m['contexts']:
  for rep in range(2):
   for q in c['questions']:
    cid=f"primary_r{rep}_{q['id']}";r=client.parsed(read(ART/'raw'/(cid+'.json')));old=read(ART/'prepared'/(cid+'.json'))['output'];new,changes=normalize(r,c);g=gold[c['id']][q['id']]
    sc=score(old,g);sn=score(new,g);empty_reason=''
    if not old['answer']:
     empty_reason='absent_answer_field' if 'answer' not in r else 'explicit_empty_model_answer' if r['answer']==[] else 'nested_list_rejected' if 'answer_shape' in old['issues'] else 'unsupported_calculator_expression'
    row=dict(call_id=cid,context_id=c['id'],question_id=q['id'],replica=rep,answer_type=g.get('answer_type','unknown'),question=q['question'],old_em=sc['em'],old_f1=sc['f1'],old_joint=sc['joint'],old_scale=sc['scale'],old_empty=sc['unfinished'],new_em=sn['em'],new_f1=sn['f1'],new_joint=sn['joint'],new_empty=sn['unfinished'],empty_reason=empty_reason,evidence_flag=int('evidence_shape' in old['issues']),changes=';'.join(changes))
    rows.append(row);details.append(dict(**row,raw=r,displayed_original=old,displayed_pilot=new,annotation=g,source=c))
 with (OUT/'answer_audit.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 samples=[]
 for typ in sorted({r['answer_type'] for r in rows}):
  for correct in (False,True):
   pool=sorted([r for r in details if r['replica']==0 and not r['old_empty'] and r['answer_type']==typ and bool(r['old_joint'])==correct],key=lambda r:digest(r['question_id']))
   seen=set()
   for r in pool:
    if r['context_id'] in seen:continue
    samples.append(r);seen.add(r['context_id'])
    if len(seen)==3:break
 write(OUT/'bounded_nonempty_audit.json',dict(rule='Replica zero; within each benchmark answer type and initial joint-correct/error stratum, first three distinct source contexts by SHA-256(question ID). At most 24 cases. Not population adjudication.',cases=samples))
 write(OUT/'empty_audit.json',dict(cases=[r for r in details if r['old_empty']],kind='Offline annotation-informed developer audit; not independent human adjudication'))
 summary=dict(n=290,contexts=24,empty_causes=dict(Counter(r['empty_reason'] for r in rows if r['old_empty'])),evidence_flagged=sum(r['evidence_flag'] for r in rows),correct_with_evidence_flag=sum(r['old_joint'] for r in rows if r['evidence_flag']),
  sums={k:sum(r[k] for r in rows) for k in ['old_em','old_f1','old_joint','old_scale','old_empty','new_em','new_f1','new_joint','new_empty']},sample=len(samples),affected=[r['call_id'] for r in rows if r['changes']],nested_affected=[r['call_id'] for r in rows if 'nested' in r['changes']],annotation_use='Offline audit only; no semantic rescoring or promotion of explanation text',source_inspection='See bounded nonempty and empty case files; qualitative notes are developer review, not independent adjudication.')
 write(OUT/'audit_summary.json',summary);print(summary)
 for r in samples:print(r['question_id'],r['answer_type'],r['old_joint'],r['question'],'\nMODEL',r['displayed_original']['answer'],r['displayed_original']['scale'],'\nGOLD',r['annotation']['answer'],r['annotation']['scale'],'DERIV',r['annotation'].get('derivation',''))
if __name__=='__main__':main()
