"""Private all-output evaluation, plus the same metric restricted to disclosed audits."""
from .vendor.tatqa_metric import TaTQAEmAndF1

def score(answer,gold):
 m=TaTQAEmAndF1();a=answer.get('answer',[]) if isinstance(answer,dict) else [];scale=answer.get('scale','') if isinstance(answer,dict) else ''
 try:
  m(gold,a,scale);em,f1,_,_=m.get_overall_metric()
 except (ValueError,TypeError,KeyError,AssertionError,OverflowError):em=f1=0.
 return dict(em=em,f1=f1,scale=int(scale==gold['scale']),joint=int(em==1 and scale==gold['scale']),unfinished=int(not a))
