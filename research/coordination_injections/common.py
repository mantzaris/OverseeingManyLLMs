"""Paths and stable serialization for the separately authorized coordination study."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifacts/coordination_injections'
DATA=Path('/tmp/coordination-sources')
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def stable(x):
 if isinstance(x,dict):return {k:stable(v) for k,v in x.items() if k not in ['seconds','controller_seconds']}
 if isinstance(x,list):return [stable(v) for v in x]
 return x
def read(p):return json.loads(Path(p).read_text())
def write(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,sort_keys=True,indent=2,ensure_ascii=False)+'\n')
