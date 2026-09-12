"""Authored mechanism and stress cases; deterministic responses are not GPU or human data."""
import copy,random,sqlite3,tempfile
from pathlib import Path
from unittest.mock import patch
from .common import ART,write,stable
from .contracts import project,contract
from .controller import run,METHODS
from .pipeline import deterministic_call
from .execution import CREATE
from .evaluate import score,reference
SCENARIOS=['ordinary_shared','local_display','unchanged','exception_generalization','delayed_notification','stale_acknowledgment','correlated_wrong_definition','irrelevant_forwarding']
def simulate(output=None):
 rows=[];traces=[]
 with tempfile.TemporaryDirectory() as temp:
  db=Path(temp)/'synthetic.sqlite';c=sqlite3.connect(str(db));c.execute(CREATE)
  rng=random.Random(7500);data=[]
  for i in range(60):
   quantity=rng.randint(-3,15);price=rng.choice([0,1000000,2500000]);data.append((i,str(i),'SKU'+str(i%9),'Authored row',quantity,'2011-02-%02d 12:00:00'%(1+i%28),price,None if i%4==0 else str(i),['France','Germany','United Kingdom'][i%3],int(quantity<0),quantity*price))
  c.executemany('INSERT INTO transactions VALUES(?,?,?,?,?,?,?,?,?,?,?)',data);c.commit();c.close()
  with patch('research.coordination_injections.execution.DB',db),patch('research.coordination_injections.evaluate.DB',db):
   reference.cache_clear()
   for case in SCENARIOS:
    p=project('synthetic_'+case,'2011-02','display' if case=='local_display' else 'country','France')
    if case=='unchanged':p['after']=copy.deepcopy(p['before'])
    initial=run(p,0,generate_fn=deterministic_call,phase='synthetic')
    def responder(*args):
     proposal,usage=deterministic_call(*args);role=args[1]
     if case=='delayed_notification':proposal['notify']=[]
     if case=='stale_acknowledgment':proposal=dict(status='keep',notify=[])
     if case=='correlated_wrong_definition' and role in ['analysis','appendix']:proposal['query']['country']='ALL'
     if case=='irrelevant_forwarding':proposal['notify']=['appendix','unregistered_role']
     return proposal,usage
    for method in METHODS:
     result=run(p,0,method,initial['artifacts'],responder,phase='synthetic',stress='exception_generalization' if case=='exception_generalization' else None)
     r=score(p,result,initial['artifacts']);r['scenario']=case;r['logical_response_opportunities']=r['calls'];r['gpu_calls']=0;rows.append(r);traces.append(dict(scenario=case,project=p,initial=stable(initial),result=stable(result)))
   reference.cache_clear()
 out=Path(output) if output else ART/'synthetic';out.mkdir(parents=True,exist_ok=True);write(out/'rows.json',rows);write(out/'traces.json',traces);write(out/'manifest.json',dict(seed=7500,scenarios=SCENARIOS,source='Entirely authored 60-row transaction table and controlled responses; not independent real source cases.',gpu_calls=0,rows=data))
 print('synthetic rows',len(rows));return rows
if __name__=='__main__':simulate()
