"""One-command source verification, saved-output replay and figure regeneration."""
import argparse,hashlib,json,sqlite3,subprocess
from pathlib import Path
from .common import ART,ROOT,read,write

def verify_data(download=False):
 from .data import DB,audit,acquire
 if not DB.exists():
  if not download:raise RuntimeError('Raw snapshot absent. Add --download to retrieve the pinned official UCI archive.')
  audit()
 expected=read(ART/'data_snapshot.json');c=sqlite3.connect('file:'+str(DB)+'?mode=ro',uri=True);h=hashlib.sha256();n=0
 for row in c.execute('SELECT * FROM transactions ORDER BY row_id'):
  h.update((json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n').encode());n+=1
 integrity=c.execute('PRAGMA integrity_check').fetchall();c.close()
 if n!=expected['rows'] or h.hexdigest()!=expected['logical_rows_sha256'] or integrity!=[('ok',)]:raise AssertionError('Recorded-data snapshot mismatch')
 return dict(rows=n,logical_rows_sha256=h.hexdigest(),integrity='ok')
def reproduce(output,download=False):
 out=Path(output);out.mkdir(parents=True,exist_ok=True)
 from .freeze import verify as frozen
 from .replay import verify as replay
 from .analyze import analyze
 from .plot import figures
 from .synthetic import simulate
 from .diagnostics import diagnose
 frozen();data=verify_data(download);r=replay(output=out/'replay.json');analyze(out/'analysis');diagnose(out/'analysis/failure_diagnostics.json');simulate(out/'synthetic');figures(out/'analysis',out/'figures')
 checked=[]
 for path in (ART/'analysis').glob('*'):
  if path.suffix not in ['.csv','.json']:continue
  candidate=out/'analysis'/path.name
  if candidate.read_bytes()!=path.read_bytes():raise AssertionError('Analysis differs: '+path.name)
  checked.append(path.name)
 for name in ['rows.json','traces.json','manifest.json']:
  if (ART/'synthetic'/name).read_bytes()!=(out/'synthetic'/name).read_bytes():raise AssertionError('Synthetic replay mismatch '+name)
 result=dict(passed=True,source=data,traces=r['traces'],reconstructed_requests=r['reconstructed_call_prompts'],tables=checked,figure_families=len(list((out/'figures').glob('*.pdf'))),inference_calls=0,interpretation='Deterministic replay of fixed responses. No promise of bitwise GPU regeneration. Figure bytes can vary with plotting-library/font versions; numeric source tables must match.')
 write(out/'verification.json',result);print(json.dumps(result,indent=2));return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',default='/tmp/coordination-replay');p.add_argument('--download',action='store_true');a=p.parse_args();reproduce(a.output,a.download)
