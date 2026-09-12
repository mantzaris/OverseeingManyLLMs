from itertools import permutations
import re
from research.oversight_workflow.common import ART,ROOT,read,write,digest
PILOT=ROOT/'research/oversight_workflow/pilot'
OUT=ART/'pilot_preparation'
VERSION='formative-v1'

def arithmetic(q):return bool(re.search(r'average|difference|percent|ratio|increase|decrease|change|total|sum',q['question'],re.I))
def shared_definition(q):
 text=q['question'].lower()
 if text.startswith('how ') and 'share' in text and ('computed' in text or 'calculated' in text):
  if 'basic' in text:return 'basic_earnings_per_share_definition'
  if 'diluted' in text:return 'diluted_earnings_per_share_definition'
 return None

def main():
 cs=read(ART/'frozen/manifest.json')['contexts']
 eligible=[c for c in cs if len(c['questions'])==6 and sum(len(r) for r in c['table'])<=60 and max(map(len,c['table']))<=7 and any(arithmetic(q) for q in c['questions'])]
 ordered=sorted(eligible,key=lambda c:(len(str(c['table'])+str(c['paragraphs'])),c['source_index']))
 k=(len(ordered)-6)//2;selected=[];definitions=set();exclusions=[]
 for c in ordered[k:]+ordered[:k]:
  ds={shared_definition(q) for q in c['questions']}-{None}
  if ds & definitions:
   exclusions.append(dict(context_id=c['id'],source_index=c['source_index'],reason='Repeated public earnings-per-share definition in another selected context'));continue
  selected.append(c);definitions|=ds
  if len(selected)==6:break
 selected.sort(key=lambda c:(len(str(c['table'])+str(c['paragraphs'])),c['source_index']))
 assert len(selected)==6
 def pairings(xs):
  if not xs:yield [];return
  for j in range(1,len(xs)):
   for rest in pairings(xs[1:j]+xs[j+1:]):yield [(xs[0],xs[j])]+rest
 def balance(pairs):
  counts=[sum(arithmetic(q) for c in p for q in c['questions']) for p in pairs]
  lengths=[sum(len(str(c['table'])+str(c['paragraphs'])) for c in p) for p in pairs]
  return (max(counts)-min(counts),max(lengths)-min(lengths),[(a['source_index'],b['source_index']) for a,b in pairs])
 pairs=min(pairings(selected),key=balance)
 packets=[]
 for i,pair in enumerate(pairs):
  qs=[]
  for c in pair:
   candidates=c['questions'];chosen=[]
   for pred in [lambda q:not arithmetic(q),arithmetic,lambda q:True]:
    q=next((q for q in candidates if pred(q) and q['id'] not in chosen),None)
    if q:chosen.append(q['id'])
   qs+=chosen
  packets.append(dict(id=i,context_ids=[c['id'] for c in pair],question_ids=[q['id'] for c in pair for q in c['questions']],source_only_question_ids=qs,
   source_characters=sum(len(str(c['table'])+str(c['paragraphs'])) for c in pair),table_cells=sum(sum(len(r) for r in c['table']) for c in pair),arithmetic_wording=sum(arithmetic(q) for c in pair for q in c['questions'])))
 assignments=[]
 for order in permutations(['B','C','S']):
  for shift in range(3):assignments.append(dict(id=len(assignments),blocks=[dict(condition=cond,packet=(pos+shift)%3) for pos,cond in enumerate(order)]))
 manifest=dict(version=VERSION,selection_rule='Among original 24 contexts with exactly six questions, at most 60 table cells/seven columns and at least one arithmetic-wording question, sort by public source-character length and source index; start at the central-six lower index and scan forward for six, skipping repeated public basic/diluted earnings-per-share definitions; pair by minimum arithmetic-wording count range, then public source-character range, then source-index ties. No generated answers or annotations loaded.',eligible=len(eligible),public_exclusions=exclusions,packets=packets,assignments=assignments,example_six_run_assignment_ids=[0,3,7,11,13,17],
 review_seconds=540,source_only_seconds=240,training_seconds=240,replica=0,review_start_offsets=[0,4,8,12,16,20,180,184,188,192,196,200],source_only_start_offsets=[0,4,8,12,16,20],generation_delay=.25,
 scope='Formative B/C workflow bundle; source-only is a task-feasibility diagnostic. No inferential comparison of source-only throughput to longer review blocks.',question_cost='No modeled cognitive cost. Clock durations are design choices.',responses='No participant responses exist at freeze.',normalization='pilot adapter flattens nested answer arrays without inventing spans; preserves explicit empty answers and original scoring separately.')
 manifest['manifest_sha256']=digest(manifest);write(PILOT/'manifest.json',manifest)
 import csv
 selected_ids={c['id'] for c in selected};excluded_ids={c['context_id'] for c in exclusions};audit=[]
 for c in cs:
  reasons=[]
  if len(c['questions'])!=6:reasons.append('question_count_not_six')
  if sum(len(r) for r in c['table'])>60:reasons.append('more_than_60_cells')
  if max(map(len,c['table']))>7:reasons.append('more_than_seven_columns')
  if not any(arithmetic(q) for q in c['questions']):reasons.append('no_arithmetic_wording')
  if c['id'] in excluded_ids:reasons.append('duplicate_public_definition')
  if not reasons and c['id'] not in selected_ids:reasons.append('outside_declared_selection_scan')
  audit.append(dict(context_id=c['id'],source_index=c['source_index'],questions=len(c['questions']),cells=sum(len(r) for r in c['table']),source_characters=len(str(c['table'])+str(c['paragraphs'])),selected=int(c['id'] in selected_ids),reasons=';'.join(reasons)))
 with (OUT/'packet_selection_audit.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(audit[0]));w.writeheader();w.writerows(audit)
 print([(p['id'],p['source_characters'],p['table_cells'],p['arithmetic_wording']) for p in packets])
if __name__=='__main__':main()
