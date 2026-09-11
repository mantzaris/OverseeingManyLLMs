import hashlib,subprocess
from datetime import datetime,timezone
from .common import ART as BASE,ROOT,read,write_json
ART=BASE/'repair'
CORE=['repair_data.py','repair_collect.py','repair_evaluate.py','repair_freeze.py','test_ordering.py','REPAIR_PROTOCOL.md']
def verify():
 from .freeze import verify as original
 original();d=read(ART/'frozen.json')
 for p,h in d['hashes'].items():
  if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h:raise RuntimeError('Repaired frozen source changed '+p)
 if subprocess.check_output(['git','show','HEAD:artifacts/verification_escalation/repair/frozen.json'])!=(ART/'frozen.json').read_bytes():raise RuntimeError('Repair declaration not committed')
 return d

def freeze():
 if (ART/'frozen.json').exists():raise RuntimeError('Already frozen')
 paths=[ROOT/'research/verification_escalation'/x for x in CORE]+[ART/'split_manifest.json']
 write_json(ART/'frozen.json',dict(frozen_utc=datetime.now(timezone.utc).isoformat(),hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},cases_hash=hashlib.sha256((ART/'private/cases.json').read_bytes()).hexdigest(),source_databases=24,replicates=2,additional_scheduled_calls=156,expected_session_calls=540,source_recovery_databases=6,prior_run_status='Preserved; blanket unordered contract invalid for explicit-order tasks 2842 and 2863',purpose='Correctness repair with a fresh, disjoint source set; no outcome-driven method tuning'))
 print('Follow-up frozen')
if __name__=='__main__':freeze()
