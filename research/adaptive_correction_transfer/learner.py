"""Small development-initialized transition model; updates require purchased labels."""
import copy,math
from .features import risk_key,relation
class Learner:
 def __init__(self,params,learn=True):self.params=copy.deepcopy(params);self.learn=learn;self.updates=[]
 @staticmethod
 def mean(pair):return pair[0]/sum(pair)
 def base(self,q,a):return self.mean(self.params['risk'].get(risk_key(q,a),self.params['risk']['pooled']))
 def error(self,q,initial,questions,observations,repairs):
  e=self.base(q,initial[q['id']]);matches=[]
  for obs in observations:
   other=questions[obs['id']];rel=relation(other,initial[obs['id']],q,initial[q['id']]);key=rel['bin']+'_'+str(obs['original_error']);pair=self.params['conditional'].get(key)
   if pair:matches.append((['context','lexical','evidence'].index(rel['bin']),obs['step'],pair))
  if matches:
   pair=max(matches,key=lambda x:(x[0],x[1]))[2];n=max(0,sum(pair)-2);w=n/(n+20);e=(1-w)*e+w*self.mean(pair)
  if repairs:
   h=repairs[-1];f,harm=self.rates(h['relation']['bin']);prior=h['predicted_before_error'];e=prior*(1-f)+(1-prior)*harm
  return min(.99,max(.01,e))
 def rates(self,bin):
  t=self.params['transfer'].get(bin,self.params['transfer']['pooled']);return self.mean(t['fix']),self.mean(t['harm'])
 def gain(self,error,rel):
  fix,harm=self.rates(rel['bin']);return error*fix-(1-error)*harm-self.params['machine_cost']
 def update_inspection(self,q,before,original_error,current_error,history):
  if not self.learn:return
  key=risk_key(q,before);p=self.params['risk'].setdefault(key,[1.,1.]);p[0]+=original_error;p[1]+=1-original_error
  self.updates.append(dict(kind='risk',question=q['id'],error=original_error,key=key))
  for h in history:
   # Only controller-supplied scores from THIS purchased question may enter.
   b=h['before_error'];after=h['after_error'];bin=h['relation']['bin'];t=self.params['transfer'][bin]
   if b:t['fix'][0]+=1-after;t['fix'][1]+=after
   else:t['harm'][0]+=after;t['harm'][1]+=1-after
   self.updates.append(dict(kind='transfer',question=q['id'],donor=h['donor'],bin=bin,before_error=b,after_error=after))
 def update_pair(self,donor,q,initial,donor_error,target_error):
  if not self.learn:return
  key=relation(donor,initial[donor['id']],q,initial[q['id']])['bin']+'_'+str(donor_error);p=self.params['conditional'].setdefault(key,[1.,1.]);p[0]+=target_error;p[1]+=1-target_error
