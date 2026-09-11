"""Commit gate for this new authorization and experiment, never historical files."""
import hashlib,subprocess,json
from datetime import datetime,timezone
from .common import ART,ROOT,write_json,read
CORE=['common.py','client.py','data.py','collect.py','engine.py','controller.py','evaluate.py','synthetic.py','analyze.py','test_protocol.py','METHOD.md','PLAN.md','freeze.py']
def verify():
 d=read(ART/'frozen.json')
 for p,h in d['hashes'].items():
  if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h:raise RuntimeError('Frozen source changed '+p)
 if subprocess.check_output(['git','show','HEAD:artifacts/verification_escalation/frozen.json'])!=(ART/'frozen.json').read_bytes():raise RuntimeError('Declaration is not committed')
 return d

def freeze():
 p=ART/'frozen.json'
 if p.exists():raise RuntimeError('Already frozen')
 paths=[ROOT/'research/verification_escalation'/x for x in CORE]+[ART/'authorization.json',ART/'split_manifest.json']
 raws=[read(x) for x in (ART/'raw').glob('*.json')];att=[a for x in raws for a in x['attempts']]
 write_json(p,dict(frozen_utc=datetime.now(timezone.utc).isoformat(),hashes={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths},cases_hash=hashlib.sha256((ART/'private/cases.json').read_bytes()).hexdigest(),expected_evaluation_calls=312,expected_preparations=96,prior_scheduled=len(raws),prior_attempts=len(att),attempt_seconds=sum(x['elapsed_seconds'] for x in att),forecast_seconds=312*sum(x['elapsed_seconds'] for x in att)/max(1,len(att))*2,source_units=48,development_units=9,replicates=2,seed=86421,bootstrap=2000,synthetic_seeds=list(range(7200,7216)),source_ids=read(ART/'split_manifest.json')['evaluation'],private_source_provenance='AMBROSIA CC BY4.0, authors request no dataset upload; raw prompts local excluded, generated outputs and execution digests published.'))
 print('Frozen',p)
if __name__=='__main__':freeze()
