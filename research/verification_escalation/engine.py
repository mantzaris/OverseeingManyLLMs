"""Read-only, bounded snapshot execution and exact table comparisons."""
import sqlite3,time,re,decimal
from dataclasses import dataclass
from .common import digest

@dataclass
class MachineBudget:
    limit:int=24
    used:int=0
    def charge(self):
        if self.used>=self.limit:raise RuntimeError('execution_budget')
        self.used+=1

def cell(x):
    if x is None:return ['null',None]
    if isinstance(x,(int,float)):
        if isinstance(x,float) and not __import__('math').isfinite(x):raise ValueError('nonfinite')
        return ['number',str(decimal.Decimal(str(x)).normalize())]
    if isinstance(x,bytes):return ['bytes',x.hex()]
    return ['text',x]

def execute(snapshot,sql,budget,ordered=False):
    start=time.perf_counter()
    try:budget.charge()
    except RuntimeError as e:return {'status':'failed','error':str(e),'seconds':time.perf_counter()-start}
    c=sqlite3.connect(':memory:')
    try:
        # The snapshot is trusted adapter material, NEVER generated candidate SQL.
        c.executescript(snapshot)
        c.execute('PRAGMA query_only=ON')
        allow={sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_FUNCTION}
        if hasattr(sqlite3,'SQLITE_RECURSIVE'):allow.add(sqlite3.SQLITE_RECURSIVE)
        c.set_authorizer(lambda action,*args:sqlite3.SQLITE_OK if action in allow else sqlite3.SQLITE_DENY)
        ticks=[0]
        def progress():
            ticks[0]+=1
            return ticks[0]>1000
        c.set_progress_handler(progress,100)
        if not isinstance(sql,str) or not re.match(r'^\s*(SELECT|WITH)\b',sql,re.I):raise ValueError('read_only_query_required')
        cur=c.execute(sql);rows=cur.fetchmany(501)
        if len(rows)>500:raise ValueError('row_limit')
        if cur.description is None:raise ValueError('table_required')
        rows=[[cell(x) for x in row] for row in rows]
        if not ordered:rows=sorted(rows,key=repr)
        table={'width':len(cur.description),'rows':rows,'ordered':ordered}
        return dict(status='ok',table=table,table_hash=digest(table),row_count=len(rows),seconds=time.perf_counter()-start)
    except Exception as e:return dict(status='failed',error=type(e).__name__+': '+str(e),seconds=time.perf_counter()-start)
    finally:c.close()

def equivalent(results):
    return bool(results) and all(x.get('status')=='ok' for x in results) and len({x['table_hash'] for x in results})==1

def verification_key(task,candidates):
    return digest(dict(dependencies={k:task.get(k) for k in ['id','request','schema','decision_id','snapshot','contract','sources','scope','version','exceptions']},candidates=candidates))
