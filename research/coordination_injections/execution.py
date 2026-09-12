"""Bounded SELECT execution and public contract probes; no evaluator targets."""
import sqlite3,time,collections,datetime
from .common import digest
from .data import DB
from .contracts import compile_sql,unit
COLS='row_id,invoice_no,stock_code,description,quantity,invoice_date,unit_price_micro,customer_id,country,is_cancel,line_value_micro'
CREATE='CREATE TABLE transactions(row_id INTEGER,invoice_no TEXT,stock_code TEXT,description TEXT,quantity INTEGER,invoice_date TEXT,unit_price_micro INTEGER,customer_id TEXT,country TEXT,is_cancel INTEGER,line_value_micro INTEGER)'
def execute(sql,rows=None):
 started=time.perf_counter();c=None
 try:
  if not isinstance(sql,str) or not sql.strip().upper().startswith(('SELECT','WITH')):raise ValueError('Only a SELECT is supported')
  if rows is None:c=sqlite3.connect('file:'+str(DB)+'?mode=ro',uri=True)
  else:
   c=sqlite3.connect(':memory:');c.execute(CREATE);c.executemany('INSERT INTO transactions VALUES(?,?,?,?,?,?,?,?,?,?,?)',rows)
  allowed={sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_FUNCTION}
  if hasattr(sqlite3,'SQLITE_RECURSIVE'):allowed.add(sqlite3.SQLITE_RECURSIVE)
  c.set_authorizer(lambda op,a,b,db,trigger:sqlite3.SQLITE_OK if op in allowed else sqlite3.SQLITE_DENY)
  ticks=[0]
  def progress():ticks[0]+=1;return int(ticks[0]>25000)
  c.set_progress_handler(progress,1000);cursor=c.execute(sql);out=cursor.fetchmany(7)
  if len(out)>5:raise ValueError('Output exceeds five-row contract')
  if cursor.description is None or len(cursor.description)!=2:raise ValueError('Expected two columns: stock_code, value')
  if any(not isinstance(r[0],str) or not isinstance(r[1],int) for r in out):raise ValueError('Expected text stock_code and exact integer value')
  return dict(status='ok',rows=[list(r) for r in out],table_hash=digest(out),seconds=time.perf_counter()-started)
 except Exception as e:return dict(status='failed',error=str(e),seconds=time.perf_counter()-started)
 finally:
  if c is not None:c.close()
def probe_rows(c):
 # Authored public counterexamples, not withheld real-data answers.
 day=c['start']+' 12:00:00';prior=(datetime.date.fromisoformat(c['start'])-datetime.timedelta(days=1)).isoformat()+' 12:00:00';end=c['end']+' 00:00:00';country='France' if c['country']=='ALL' else c['country'];other='Germany' if country!='Germany' else 'France'
 vals=[('A',2,4000000,day,country,0,'1'),('B',7,1000000,day,country,0,'2'),('A',-1,4000000,day,country,1,'1'),('C',20,2000000,day,other,0,'3'),('D',30,3000000,prior,country,0,'4'),('E',40,4000000,end,country,0,'5'),('F',11,2000000,day,country,0,None),('G',50,0,day,country,0,'6'),('H',-5,1000000,day,country,0,'7'),('I',9,2000000,day,country,1,'8'),('J',3,-1000000,day,country,0,'9')]
 return [(i,'C1' if cancel else str(i),s,'Public contract probe',q,d,p,cust,n,cancel,q*p) for i,(s,q,p,d,n,cancel,cust) in enumerate(vals,1)]
def python_aggregate(rows,c):
 counts=collections.defaultdict(int)
 for row in rows:
  _,invoice,stock,description,q,date,price,cust,country,cancel,value=row
  if not c['start']<=date<c['end'] or price<=0:continue
  if c['country']!='ALL' and country!=c['country']:continue
  if c['customer']=='known' and cust is None:continue
  if c['inclusion']=='positive' and (q<=0 or cancel):continue
  counts[stock]+=q if c['metric']=='units' else value
 return [[k,v] for k,v in sorted(counts.items(),key=lambda x:(-x[1],x[0]))[:5]]
def probe(sql,c):
 rows=probe_rows(c);got=execute(sql,rows);expected=python_aggregate(rows,c)
 return dict(status='passed' if got['status']=='ok' and got['rows']==expected else 'failed',reason=None if got['status']=='ok' and got['rows']==expected else 'Public synthetic probe mismatch (not real-data reference): expected '+str(expected)+'; got '+str(got.get('rows',got.get('error')))+'. Check the explicit requirements.',execution=got)
def expected_claims(points):
 return dict(top_stock=points[0][0] if points else None,top_value=points[0][1] if points else None,displayed_total=sum(p[1] for p in points),displayed_products=len(points))
