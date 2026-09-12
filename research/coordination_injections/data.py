"""Official UCI source ingestion with no silent row deletion."""
import sys,sqlite3,zipfile,hashlib,collections,datetime,urllib.request
from decimal import Decimal
from pathlib import Path
from .common import DATA,ART,write
URL='https://archive.ics.uci.edu/static/public/352/online%2Bretail.zip'
DB=DATA/'retail.sqlite'
def acquire():
 DATA.mkdir(parents=True,exist_ok=True);archive=DATA/'online_retail.zip'
 if not archive.exists():
  with urllib.request.urlopen(URL,timeout=60) as r:archive.write_bytes(r.read())
 with zipfile.ZipFile(archive) as z:
  name=next(x for x in z.namelist() if x.endswith('.xlsx'));raw=z.read(name)
 xlsx=DATA/'Online Retail.xlsx';xlsx.write_bytes(raw)
 return archive,xlsx
def audit():
 try:import openpyxl
 except ImportError:
  sys.path.insert(0,'/tmp/coordination-python');import openpyxl
 archive,xlsx=acquire();wb=openpyxl.load_workbook(xlsx,read_only=True,data_only=True)
 rows=wb.active.iter_rows(values_only=True);headers=next(rows);counts=collections.Counter();countries=collections.Counter();months=collections.Counter();dates=[];seen=set();batch=[];invoices=collections.defaultdict(set);anomalies=[]
 c=sqlite3.connect(str(DB));c.execute('DROP TABLE IF EXISTS transactions');c.execute('CREATE TABLE transactions(row_id INTEGER PRIMARY KEY,invoice_no TEXT,stock_code TEXT,description TEXT,quantity INTEGER,invoice_date TEXT,unit_price_micro INTEGER,customer_id TEXT,country TEXT,is_cancel INTEGER,line_value_micro INTEGER)')
 minp=None;maxp=None;minq=None;maxq=None;precision=0
 for i,r in enumerate(rows,1):
  invoice,stock,desc,q,date,price,cust,country=r;invoice=str(invoice);stock=str(stock);q=int(q);p=Decimal(str(price));micro=p*1000000
  if micro!=micro.to_integral_value():raise ValueError('Price precision exceeds exact declared micro-GBP representation')
  key=tuple(r);counts['duplicates_beyond_first']+=key in seen;seen.add(key)
  counts['rows']+=1;cancel=invoice.upper().startswith('C');counts['cancellation_rows']+=cancel;counts['negative_quantity']+=q<0;counts['zero_quantity']+=q==0;counts['negative_unit_price']+=p<0;counts['zero_unit_price']+=p==0;counts['negative_quantity_without_cancellation']+=q<0 and not cancel;counts['positive_quantity_with_cancellation']+=q>0 and cancel
  counts['missing_customer_id']+=cust is None;counts['missing_description']+=desc is None;counts['missing_country']+=country is None;counts['missing_stock_code']+=stock=='None';counts['missing_invoice_id']+=invoice=='None'
  counts['nonnumeric_noncancellation_invoice']+=not cancel and not invoice.isdigit();countries[str(country)]+=1;months[date.strftime('%Y-%m')]+=1;dates.append(date)
  invoices[invoice].add((date.isoformat(),str(cust),str(country)));precision=max(precision,max(0,-p.as_tuple().exponent));minp=p if minp is None else min(minp,p);maxp=p if maxp is None else max(maxp,p);minq=q if minq is None else min(minq,q);maxq=q if maxq is None else max(maxq,q)
  if p<0 or (not cancel and q<0) or (cancel and q>0):
   if len(anomalies)<12:anomalies.append(dict(row_id=i,invoice_no=invoice,stock_code=stock,quantity=q,unit_price=str(p),description=desc))
  batch.append((i,invoice,stock,desc,q,date.strftime('%Y-%m-%d %H:%M:%S'),int(micro),None if cust is None else str(int(cust)),country,int(cancel),q*int(micro)))
  if len(batch)>=10000:c.executemany('INSERT INTO transactions VALUES(?,?,?,?,?,?,?,?,?,?,?)',batch);batch=[]
 if batch:c.executemany('INSERT INTO transactions VALUES(?,?,?,?,?,?,?,?,?,?,?)',batch)
 c.execute('CREATE INDEX transaction_date ON transactions(invoice_date)');c.execute('CREATE INDEX transaction_country_date ON transactions(country,invoice_date)');c.commit()
 out=dict(source_url='https://archive.ics.uci.edu/dataset/352/online%2Bretail',download_url=URL,citation='Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33',license='CC BY 4.0',retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),xlsx_sha256=hashlib.sha256(xlsx.read_bytes()).hexdigest(),headers=list(headers),counts=dict(counts),countries=dict(sorted(countries.items())),monthly_rows=dict(sorted(months.items())),min_date=min(dates).isoformat(),max_date=max(dates).isoformat(),min_quantity=minq,max_quantity=maxq,min_unit_price=str(minp),max_unit_price=str(maxp),max_price_decimal_places=precision,distinct_invoices=len(invoices),invoice_ids_with_multiple_timestamp_customer_country_tuples=sum(len(v)>1 for v in invoices.values()),anomaly_examples=anomalies,openpyxl=openpyxl.__version__,row_policy='All source rows retained. Original duplicate rows preserved. Analysis rules are explicit project parameters. Prices represented exactly in micro-GBP.',sqlite_integrity=c.execute('PRAGMA integrity_check').fetchall())
 write(ART/'data_audit.json',out);c.close();wb.close();print({k:out[k] for k in ['counts','min_date','max_date','min_unit_price','max_unit_price','max_price_decimal_places']});return out
if __name__=='__main__':audit()
