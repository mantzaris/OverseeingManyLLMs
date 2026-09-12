"""Inspection oracle. Only a purchased question is disclosed to the controller."""
import copy
class Inspector:
 def __init__(self,gold,budget):self._gold=gold;self.budget=budget;self.disclosed=[]
 def inspect(self,q):
  if len(self.disclosed)>=self.budget:raise RuntimeError('Inspection budget')
  if q['id'] in [f['id'] for f in self.disclosed]:raise ValueError('Already verified')
  g=self._gold[q['id']];f=dict(id=q['id'],question=q['question'],answer=copy.deepcopy(g['answer']),scale=g['scale'],derivation=g.get('derivation',''),answer_type=g['answer_type'],source='TAT-QA annotation disclosed by this inspection only')
  self.disclosed.append(f);return copy.deepcopy(f)
def verified_answer(f):
 a=f['answer'] if isinstance(f['answer'],list) else [str(f['answer'])]
 return dict(answer=[str(x) for x in a],scale=f['scale'],derivation=f['derivation'],evidence=[],operation='verified',valid=True,issues=[],verified=True)
