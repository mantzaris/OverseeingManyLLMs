"""Evaluator-only real-data references; never imported by the controller or prompts."""
import sqlite3,functools
from .common import digest,canonical
from .contracts import ROLES,contract,unit
from .controller import artifact_hash
from .execution import COLS,python_aggregate,expected_claims
from .data import DB
@functools.lru_cache(maxsize=128)
def reference(key):
 import json
 c=json.loads(key);conn=sqlite3.connect('file:'+str(DB)+'?mode=ro',uri=True)
 # Only bound the date for speed. All remaining evaluation aggregation is independent Python.
 rows=conn.execute('SELECT '+COLS+' FROM transactions WHERE invoice_date >= ? AND invoice_date < ?',(c['start'],c['end'])).fetchall();conn.close()
 return python_aggregate(rows,c)
def artifact_correct(project,epoch,role,a):
 c=contract(project,role,epoch);p=a.get('proposal') if a else None
 if not isinstance(p,dict) or p.get('status')!='replace':return False
 main=reference(canonical(c));points=main[:c.get('display_n',5)]
 if role in ['analysis','appendix']:return a.get('execution',{}).get('status')=='ok' and a['execution']['rows']==main
 if a.get('unit')!=unit(c):return False
 if role=='chart':return a.get('points')==points
 return a.get('claims')==expected_claims(points)
def score(project,run,initial=None):
 epoch=run['epoch'];arts=run['artifacts'];flags={r:artifact_correct(project,epoch,r,arts.get(r)) for r in ROLES};accepted={r:arts.get(r,{}).get('accepted',False) for r in ROLES}
 issues=[x for a in arts.values() for x in a.get('online_issues',[])];dependency=sum(x.startswith(('unaccepted_dependency','stale_dependency')) for x in issues)
 violations=sum(not flags[r] or any(not x.startswith(('unaccepted_dependency','stale_dependency')) for x in arts.get(r,{}).get('online_issues',['missing_artifact'])) for r in ROLES);unfinished=sum(not accepted[r] for r in ROLES)
 changes=0;unaffected=[]
 if initial is not None:
  unaffected=[r for r in ROLES if contract(project,r,0)==contract(project,r,1)]
  changes=sum(artifact_hash(arts.get(r,{}))!=artifact_hash(initial.get(r,{})) for r in unaffected)
 calls=run['calls'];rounds=max([r['round']+1 for r in run['routes']]+[0]);query_calls=sum(1 for route in run['routes'] if route['role'] in ['analysis','appendix'])
 out=dict(project_id=project['id'],month=project['month'],change=project['change'],rep=run['rep'],method=run['method'],epoch=epoch,stress=run['stress'],raw_correct=sum(flags.values()),raw_project_correct=int(all(flags.values())),accepted_correct=sum(flags[r] and accepted[r] for r in ROLES),accepted_wrong=sum(not flags[r] and accepted[r] for r in ROLES),unfinished=unfinished,project_correct=int(all(flags[r] and accepted[r] for r in ROLES)),requirement_violations=violations,dependency_inconsistencies=dependency,V=violations/4+min(dependency,4)/4+unfinished/4,unaffected_artifacts=len(unaffected),unnecessary_modifications=changes,appendix_correct=int(flags['appendix']),calls=len(calls),attempts=sum(c['attempts'] for c in calls),tokens=sum(c['tokens'] for c in calls),inference_seconds=sum(c['seconds'] for c in calls),wall_seconds=run['seconds'],rounds=rounds,repair_repeats=sum(max(0,sum(x['role']==r for x in run['routes'])-1) for r in ROLES),direct_recipients=len(run['direct_recipients']),forwarded_messages=run['forwarded_messages'],messages=len(run['routes']),checks=len(run['checks']),public_probe_executions=sum(x['kind']=='public_probe' for x in run['checks']),real_query_opportunities=query_calls,user_changes=run['user_changes'],user_questions=run['user_questions'],artifact_correct=flags,artifact_accepted=accepted)
 return out
