import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifacts/adaptive_correction_transfer'
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
def stable(x):
 if isinstance(x,dict):return {k:stable(v) for k,v in x.items() if k not in ['seconds','elapsed_seconds','wall_seconds']}
 if isinstance(x,list):return [stable(v) for v in x]
 return x
