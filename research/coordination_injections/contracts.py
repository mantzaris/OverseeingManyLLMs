"""Authored analysis contracts, explicit scopes and fixed project construction."""
import copy,calendar
from .common import digest
ROLES=['analysis','chart','report','appendix']
DEPENDENCIES={'analysis':[],'chart':['analysis'],'report':['chart'],'appendix':[]}
SCHEMA='transactions(row_id INTEGER, invoice_no TEXT, stock_code TEXT, description TEXT, quantity INTEGER, invoice_date TEXT, unit_price_micro INTEGER, customer_id TEXT NULL, country TEXT, is_cancel INTEGER, line_value_micro INTEGER)'
RULES='All original rows including duplicates are retained. Dates use inclusive start and exclusive end. positive means quantity>0 AND unit_price_micro>0 AND is_cancel=0. signed means unit_price_micro>0, including negative quantities and cancellation rows. customer=known means customer_id IS NOT NULL; all imposes no customer filter. country=ALL imposes no country filter. units means SUM(quantity). value_micro means SUM(line_value_micro), in millionths of GBP, not profit. Group by stock_code, order value DESC then stock_code ASC, LIMIT 5.'
def contract(project,role,epoch):
 state=project['before' if epoch==0 else 'after']
 if role=='appendix':return dict(scope='appendix',**state['appendix'])
 out=dict(scope='main',**state['main'])
 if role in ['chart','report']:out['display_n']=state['display_n']
 return out
def unit(c):return 'items' if c['metric']=='units' else 'micro_GBP'
def compile_sql(c):
 # This deterministic application comparator is public; empirical reference uses an independent Python aggregate.
 where=["invoice_date >= '"+c['start']+"'","invoice_date < '"+c['end']+"'",'unit_price_micro > 0']
 if c['inclusion']=='positive':where+=['quantity > 0','is_cancel = 0']
 if c['country']!='ALL':where.append("country = '"+c['country'].replace("'","''")+"'")
 if c['customer']=='known':where.append('customer_id IS NOT NULL')
 measure='quantity' if c['metric']=='units' else 'line_value_micro'
 return 'SELECT stock_code, SUM('+measure+') AS value FROM transactions WHERE '+' AND '.join(where)+' GROUP BY stock_code ORDER BY value DESC, stock_code ASC LIMIT 5'
def month_window(month):
 y,m=map(int,month.split('-'));return month+'-01',('%04d-%02d-01'%(y+int(m==12),m%12+1))
def project(pid,month,change,country='France'):
 start,end=month_window(month);base=dict(start=start,end=end,country='ALL',inclusion='positive',customer='all',metric='units')
 before=dict(main=copy.deepcopy(base),appendix=copy.deepcopy(base),display_n=5);after=copy.deepcopy(before)
 if change=='country':after['main']['country']=country;message='Restrict the main analysis, chart and report to '+country+'. Keep the appendix under its original all-country brief.'
 elif change=='metric':after['main']['metric']='value_micro';message='Rank the main outputs by recorded positive line value, not item quantity. Preserve the original quantity appendix.'
 elif change=='signed':after['main'].update(metric='value_micro',inclusion='signed');message='For the main report use signed recorded line value, including cancellations and negative quantities when price is positive. The appendix keeps its original positive-quantity convention.'
 elif change=='period':after['main']['start']=month+'-16';message='Use the second half of the month for the main outputs. Keep the appendix on the full original month.'
 elif change=='known_customer':after['main']['customer']='known';message='Exclude records missing a customer identifier from the main outputs only. Do not change the appendix.'
 elif change=='display':after['display_n']=3;message='Show only the first three ranked products in the chart. Update the report claims about the displayed chart; leave the five-row analysis and appendix intact.'
 else:raise ValueError(change)
 return dict(id=pid,month=month,change=change,before=before,after=after,user_change=dict(source='authorized_user',version=2,text=message,scope='main',exceptions=['appendix']),dependencies=DEPENDENCIES)
def initial_manifest():
 dev=[project('dev_'+str(i),m,k,c) for i,(m,k,c) in enumerate([('2010-12','country','United Kingdom'),('2010-12','display','Germany'),('2011-01','metric','France'),('2011-01','signed','Germany')])]
 kinds=['country','metric','period','known_customer','signed','display']
 evaluation=[]
 for m in range(2,10):
  for j in range(2):
   k=kinds[(2*(m-2)+j)%len(kinds)];evaluation.append(project('eval_%02d_%d'%(m,j),'2011-%02d'%m,k,['Germany','France'][j]))
 return dict(development=dev,evaluation=evaluation,development_months=['2010-12','2011-01'],evaluation_months=['2011-%02d'%m for m in range(2,10)],replicates=[0,1],interpretation='One retailer; eight nonoverlapping monthly evaluation data blocks. Two constructed projects per month are dependent. Replicates do not create source units.',selection='All declared projects in chronological block order, never selected by model outcomes.')
def affected(project):return [r for r in ROLES if contract(project,r,0)!=contract(project,r,1)]
