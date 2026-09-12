"""Post hoc direct-reading comparator; separate from the frozen primary study."""
import argparse,hashlib,subprocess,csv,json
from pathlib import Path
from datetime import datetime,timezone
from .common import ART,ROOT,read,write_json,digest
from .client import generate,parsed
from .repair_collect import messages
from .repair_data import public_task,intent_index
from .engine import execute,MachineBudget
ROOT_AUDIT=ART/'direct_reader_audit'
PROMPT='Read all supplied instructions and database context. Recover any answer already available. Return one JSON object with status ready, clarify, or unsupported; sql (string or null); and question (string or null). If the request has one justified actionable interpretation, use ready and implement its requested table. If a genuine unresolved user-intent distinction changes which result is appropriate, use clarify and ask a concise targeted question. Do not silently choose a user preference from a database pattern. If the work cannot be implemented, use unsupported. Do not ask the user merely to repair an SQL syntax error. Respect scope and any explicit sorting. Do not enumerate speculative alternative outputs when one answer is available.'

def freeze():
 if (ROOT_AUDIT/'frozen.json').exists():raise RuntimeError('Already frozen')
 dev=read(ART/'private/cases.json')['development'][:4];evaluation=read(ART/'repair/private/cases.json')['evaluation']
 doc=dict(status='Post hoc comparator audit on already inspected source cases; NOT a fresh held-out evaluation',reason='The frozen full-context comparator takes a first candidate from an enumeration prompt. Test a direct source-reading answer-or-ask prompt without changing the primary controller or selecting favorable cases.',frozen_utc=datetime.now(timezone.utc).isoformat(),development_ids=[c['id'] for c in dev],source_ids=[c['id'] for c in evaluation],replicates=2,scheduled_calls=52,expected_session_calls=592,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),model='Unchanged pinned Qwen BF16 server, temperature .3, top_p 1, 256 output tokens',decisions='No method tuning after this declaration. Invalid outputs/SQL stay unfinished; only status clarify consumes an intent response. All budgets 0/1/2; 24 source databases, replicas averaged before fixed-seed paired analysis. Primary frozen results remain unchanged.')
 write_json(ROOT_AUDIT/'frozen.json',doc)

def verify():
 d=read(ROOT_AUDIT/'frozen.json');assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==d['code_sha256']
 assert subprocess.check_output(['git','show','HEAD:artifacts/verification_escalation/direct_reader_audit/frozen.json'])==(ROOT_AUDIT/'frozen.json').read_bytes()
 return d

def collect():
 d=verify();cases=read(ART/'private/cases.json')['development'][:4]
 groups=[('development',cases,1),('inspected_comparison',read(ART/'repair/private/cases.json')['evaluation'],2)]
 for phase,cc,nrep in groups:
  for c in cc:
   for rep in range(nrep):
    key='direct_reader_'+phase+'_'+c['id']+'_r'+str(rep)
    t=public_task(c,rep);saved=generate(key,messages(t,PROMPT),960000+int(c['id'])*10+rep,256)
    write_json(ROOT_AUDIT/'prepared'/(key+'.json'),dict(id=c['id'],rep=rep,phase=phase,public_hash=digest(t),response=parsed(saved)))
    print(key,flush=True)

def evaluate(output=None):
 verify();dest=Path(output) if output else ROOT_AUDIT;rows=[];traces={}
 for c in read(ART/'repair/private/cases.json')['evaluation']:
  for rep in [0,1]:
   key='direct_reader_inspected_comparison_'+c['id']+'_r'+str(rep);obj=read(ROOT_AUDIT/'prepared'/(key+'.json'))['response'] or {}
   answered=read(ART/'repair/prepared'/('repair_evaluation_v2_'+c['id']+'_r'+str(rep)+'.json')).get('answered') or {}
   task=public_task(c,rep)
   for b in [0,1,2]:
    m=MachineBudget(24);q=0;sql=None;result={'status':'not_run'}
    if obj.get('status')=='ready':sql=obj.get('sql');result=execute(task['snapshot'],sql,m,task['contract']['ordered'])
    elif obj.get('status')=='clarify' and b>0:q=1;sql=answered.get('sql');result=execute(task['snapshot'],sql,m,task['contract']['ordered'])
    target=execute(c['snapshot'],c['refs'][intent_index(c,rep)],MachineBudget(1),task['contract']['ordered'])
    released=result['status']=='ok';correct=released and result['table_hash']==target.get('table_hash')
    rows.append(dict(id=c['id'],db=c['db'],domain=c['domain'],kind=c['kind'],rep=rep,budget=b,method='direct_reader_answer_or_ask',status=obj.get('status','parse_failure'),questions=q,correct=int(correct),wrong=int(released and not correct),unfinished=int(not released),loss=4*int(released and not correct)+int(not released),executions=m.used))
    result.pop('seconds',None);result.pop('table',None);traces[c['id']+'|'+str(rep)+'|'+str(b)]=dict(displayed_question=obj.get('question') if q else None,response_requested=bool(q),sql=sql,result=result)
 dest.mkdir(parents=True,exist_ok=True)
 with (dest/'episodes.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 write_json(dest/'traces.json',traces)
 return rows

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['freeze','collect','evaluate']);a=p.parse_args();globals()[a.action]()
