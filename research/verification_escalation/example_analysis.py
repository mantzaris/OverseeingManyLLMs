"""Prespecified matched examples, with explicit synthetic/empirical separation."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .common import ART,read,write_json
from .analyze import load
from .plot import style,save

def run(root=ART/'repair',synthetic_root=ART):
 root=Path(root);synthetic_root=Path(synthetic_root);rows=load(root/'evaluation/episodes.csv');tr=read(root/'evaluation/traces.json');chosen=read(root/'analysis/examples.json')['selected'];examples=[]
 for outcome in ['tie','unfavorable']:
  cid=chosen[outcome]
  if cid is None:continue
  for rep in [0,1]:
   for m in ['recovery_completion','verification']:
    r=next(x for x in rows if x['id']==cid and x['rep']==rep and x['condition']=='generated' and x['method']==m and x['budget']==1)
    record=tr['|'.join(map(str,[cid,rep,'generated',m,1]))]['records'][cid]
    examples.append(dict(category=outcome,id=cid,rep=rep,method=m,questions=r['questions'],correct=r['correct'],wrong=r['wrong'],unfinished=r['unfinished'],reason=record['reason'],sql=record.get('sql'),row_count=record.get('result',{}).get('row_count'),table_hash=record.get('result',{}).get('table_hash')))
 write_json(root/'analysis/matched_examples.json',dict(selection=chosen,rule='Frozen first lexicographic ID by mean loss sign; both replicas retained. No empirical favorable loss case exists. Synthetic success uses the predeclared equal_snapshot family, seed 7200.',rows=examples))
 style();fig,axes=plt.subplots(3,1,figsize=(7.5,5.8));syn=load(synthetic_root/'synthetic/episodes.csv')
 for axis,label,cid in zip(axes,['Synthetic success','Source tie','Source unfavorable'],[None,chosen['tie'],chosen['unfavorable']]):
  axis.set_xlim(0,1);axis.set_ylim(0,1);axis.axis('off');axis.set_title(label+(' (ID '+cid+')' if cid else ' (equal snapshot)'),fontsize=12,loc='left')
  for j,m in enumerate(['recovery_completion','verification']):
   x=.03+j*.50;y=.56;axis.text(x,y+.24,'Completion' if j==0 else 'Verification',fontweight='bold',fontsize=11)
   if cid:
    z=[r for r in examples if r['id']==cid and r['method']==m]
    answer='Answers: '+', '.join(str(int(r['questions'])) for r in z)+' (replicas 0, 1)'
    result='Tables: '+', '.join('match' if r['correct'] else 'mismatch' if r['wrong'] else 'unfinished' for r in z)
   else:
    r=next(x for x in syn if x['family']=='equal_snapshot' and x['seed']==7200 and x['method']==m and x['budget']==1)
    answer='Answers: '+str(int(r['questions']));result='One matching table' if r['correct']==1 else 'Unfinished or wrong'
   axis.text(x,y,answer+'\n'+result,fontsize=11,va='center',linespacing=1.6,bbox=dict(boxstyle='round,pad=.5',fc='#EAF3F5' if j==0 else '#E8F1EB',ec='none'))
  text={'1475':'One clarified query still misses\nthe common-to-all requirement.','1484':'The missing collective interpretation\nchanges a six-row join into one\ncommon-program result.'}.get(cid,'Two represented rules return the\nsame IDs on the authored snapshot.')
  axis.text(.03,.12,text.replace('\n',' '),fontsize=9,va='top')
 save(fig,root/'figures/matched_examples');return examples
if __name__=='__main__':run()
