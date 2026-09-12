"""Constructed transfer mechanisms, separate from natural TAT-QA evidence."""
import copy,random
from .common import ART,read,write
from .controller import run
from .feedback import Inspector
from .answers import prepare
from .scoring import score
from .tests import C,G
from .analyze import csvout
CASES=['independent','shared_scale','partial_applicability','misleading_similarity','scale_invariant_ratio','incorrect_diagnosis','ineffective','correlated_error']
def fixture(case,seed):
 rng=random.Random(seed);c=copy.deepcopy(C);c['id']=case+'_'+str(seed);a={}
 common=rng.random()<.65
 for i,q in enumerate(c['questions']):
  wrong=common if case=='correlated_error' else rng.random()<.5
  gold=G[q['id']];scale=gold['scale'];value=gold['answer']
  if wrong:
   if case in ['shared_scale','scale_invariant_ratio','partial_applicability']:scale='billion' if scale=='million' else ''
   else:value=str(float(value)+7)
  ev=['T1C1'] if i<3 or case=='misleading_similarity' else ['T2C2']
  a[q['id']]=prepare(dict(answer=[value],scale=scale,evidence=ev,operation='ratio' if i==2 else 'lookup',derivation='Authored synthetic proposal'),c)
 def generator(q,old,corrections,step,retry):
  new=copy.deepcopy(old);i=int(q['id'][1:]);donor=corrections[-1]['question'] if corrections else '';f=corrections[-1] if corrections else None
  if not retry and f:
   if case in ['shared_scale','correlated_error']:
    if case=='correlated_error':new=prepare(dict(answer=[G[q['id']]['answer']],scale=G[q['id']]['scale'],evidence=old['evidence'],operation=old['operation']),c)
    elif old['operation']!='ratio' and f['scale']=='million':new['scale']='million'
   elif case=='partial_applicability' and i==1:new['scale']='million'
   elif case in ['misleading_similarity','incorrect_diagnosis']:
    new['answer']=[str(float(new['answer'][0])*1000)];new['scale']=f['scale']
   elif case=='scale_invariant_ratio':new['scale']=f['scale']
  return new,dict(call_id=case+'_'+str(seed)+'_'+str(step)+'_'+q['id'],request_sha256='synthetic',status='scripted',attempts=0,tokens=0,seconds=0)
 return c,a,generator

def evaluate():
 spec=read(ART/'frozen/synthetic_spec.json');params=read(ART/'initial_model.json');rows=[];examples=[]
 for case in spec['cases']:
  for seed in spec['seeds']:
   c,a,gen=fixture(case,seed)
   for method in spec['methods']:
    r=run(c,a,params,Inspector(G,2),gen,seed,method,2)
    for b,ans in enumerate(r['snapshots']):
     events=r['events'][:b];inspected={e['inspected'] for e in events};never=set(ans)-inspected
     rows.append(dict(case=case,seed=seed,method=method,budget=b,correct=sum(score(v,G[q])['em'] for q,v in ans.items()),questions=4,inspections=b,calls=sum(len(e['repairs']) for e in events),sibling_gain=sum(score(ans[q],G[q])['em']-score(a[q],G[q])['em'] for q in never),harms=sum(score(h['after'],G[h['id']])['em']<score(h['before'],G[h['id']])['em'] for e in events for h in e['repairs'])))
    if seed==spec['seeds'][0]:examples.append(r)
 csvout(ART/'synthetic/results.csv',rows);write(ART/'synthetic/examples.json',examples);print('Synthetic rows',len(rows))
if __name__=='__main__':evaluate()
