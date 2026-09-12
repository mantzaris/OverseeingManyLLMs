"""First-qualifying examples and complete final-score-change audit, offline only."""
from .common import ART,read,write
from research.adaptive_correction_transfer.scoring import score

def select():
 cs=read(ART/'development_manifest.json')['contexts'];gold=read(ART/'offline_development_annotations.json')['annotations'];examples={};changes=[]
 for v in ['v1','v2']:
  for i,c in enumerate(cs):
   qs={q['id']:q for q in c['questions']}
   for method in ['coarse','reattempt']:
    r=read(ART/f'development_{v}/c{i:02d}_{method}.json')
    if method=='coarse':
     for e in r['events']:
      for h in e['revisions']:
       b=score(h['before'],gold[c['id']][h['recipient']])['em'];a=score(h['after'],gold[c['id']][h['recipient']])['em'];kind='help' if a>b else 'harm' if a<b else 'tie';key=v+'_'+kind
       if key not in examples:examples[key]=dict(version=v,source_index=i,source=c,question=qs[h['recipient']],inspection=e['disclosure'],event=h,offline_reference=gold[c['id']][h['recipient']],before_em=b,after_em=a,selection='First qualifying coarse-transfer event in version/source/step/question order, regardless of effect size. Offline labels shown for analysis only.')
    for qid,a in r['answers'].items():
     if qid in r['inspection_ids']:continue
     b=r['initial'][qid];bb=score(b,gold[c['id']][qid])['em'];aa=score(a,gold[c['id']][qid])['em']
     if bb!=aa:changes.append(dict(version=v,source_index=i,context=c['id'],method=method,question=qs[qid],before=b,after=a,reference=gold[c['id']][qid],before_em=bb,after_em=aa,answer_unchanged=b['answer']==a['answer'],scale_changed=b['scale']!=a['scale']))
 write(ART/'diagnostics/transfer_examples.json',examples);write(ART/'diagnostics/final_score_changes.json',changes)
if __name__=='__main__':select()
