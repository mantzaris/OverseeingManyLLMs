#!/usr/bin/env python3
"""Post-run integrity audit of frozen methods, chronology and complete paired rows.

This reads saved evidence only. It does not select cases, change scores or refit risk.
"""
from collections import Counter
from datetime import datetime,timedelta
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.domain import digest
from overseeing.io import read_events,write_json,utc_now
from overseeing.retail.risk import RetailRisk

root=Path('artifacts/stage5_practical');batch=root/'batches/evaluation'
freeze=json.loads((root/'evaluation_freeze.json').read_text())
declaration=json.loads((batch/'declaration.json').read_text())
commit=(root/'freeze_commit.txt').read_text().strip()
committed=subprocess.check_output(['git','show',commit+':'+str(batch/'declaration.json')])
assert committed==(batch/'declaration.json').read_bytes()
commit_time=subprocess.check_output(['git','show','-s','--format=%cI',commit],text=True).strip()
assert declaration['declaration_hash']==freeze['declaration_hash']
assert digest({k:v for k,v in declaration.items() if k!='declaration_hash'})==freeze['declaration_hash']
presentation=json.loads((root/'presentation_adjustments.json').read_text())['changes']
assert {r['path'] for r in presentation}=={'scripts/plot_retail.py','scripts/retail_traces.py'}
rendering={r['path']:r for r in presentation}
for name,expected in freeze['source_hashes'].items():
    if name in rendering:
        assert rendering[name]['before_sha256']==expected
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==rendering[name]['after_sha256']
    else:assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==expected,name
    assert hashlib.sha256((batch/'source'/name).read_bytes()).hexdigest()==expected,name
estimator=json.loads((root/'estimator.json').read_text())
assert estimator==declaration['estimator']
assert RetailRisk.load(estimator).estimator_hash==freeze['estimator_hash']
assert hashlib.sha256((root/'authorization.json').read_bytes()).hexdigest()==freeze['authorization_sha256']
ledger=read_events(root/'ledger.jsonl')
evaluation_calls=[r for r in ledger if r['kind']=='call_reserved' and r['context']=='evaluation']
first=evaluation_calls[0]['wall_utc'];last=evaluation_calls[-1]['wall_utc']
assert datetime.fromisoformat(freeze['frozen_utc'])<=datetime.fromisoformat(commit_time)<datetime.fromisoformat(first)
assert len(evaluation_calls)<=declaration['max_scheduled_calls']
ids={r['call_id'] for r in evaluation_calls}
assert sum(r['kind']=='attempt_reserved' and r['call_id'] in ids for r in ledger)<=declaration['max_attempts']
planned={(b['bundle_id'],b['replicate'],s['case_id']) for b in declaration['bundles'] for s in b['slots']}
actual=[]
for path in sorted((batch/'prepared').glob('*/workflows.json')):
    actual.extend((r['bundle_id'],r['replicate'],r['case_id']) for r in json.loads(path.read_text()))
assert len(actual)==len(set(actual)) and set(actual)==planned
rows=list(csv.DictReader((batch/'analysis/episodes.csv').open()))
expected={(b['bundle_id'],str(b['replicate']),str(d),p) for b in declaration['bundles'] for d in (1,2) for p in declaration['config']['policies']}
keys=[(r['bundle_id'],r['replicate'],r['review_duration'],r['policy']) for r in rows]
assert len(keys)==len(set(keys)) and set(keys)==expected
assert all(r['status']=='completed' for r in rows)
assert len(list((batch/'analysis/traces').glob('*/*.json.gz')))==len(expected)
assert len(list(csv.DictReader((batch/'analysis/unlimited_reference.csv').open())))==96
summary=json.loads((batch/'analysis/summary.json').read_text())
assert summary['all_completed_policy_traces_replayed'] and not summary['missing_bundle_replicates']
inventory=json.loads((root/'evidence_original_hashes.json').read_text())['files']
redactions=json.loads((root/'publication_redactions.json').read_text())
public_hashes={r['path']:r['public_sha256'] for r in redactions['files']}
private_verified=0
for name,expected_hash in inventory.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==public_hashes.get(name,expected_hash),name
for entry in redactions['files']:
    assert inventory[entry['path']]==entry['original_sha256']
    original=Path('artifacts/stage5_practical_private')/entry['path']
    if original.exists():
        assert hashlib.sha256(original.read_bytes()).hexdigest()==entry['original_sha256']
        private_verified+=1
finished=[r for p in sorted((root/'batches').glob('*/prepared/*/*_raw.jsonl.gz'))
          for r in read_events(p) if r['phase']=='attempt_finished']
finished.sort(key=lambda r:(r['session_call_id'],r['retry']))
input_matches=0;overlaps=[];previous_end=None
for r in finished:
    if r.get('usage'):
        assert r['input_tokens']==r['usage']['prompt_tokens']
        input_matches+=1
    began=datetime.fromisoformat(r['wall_utc'])
    if previous_end and began+timedelta(milliseconds=1)<previous_end:
        overlaps.append(dict(call_id=r['session_call_id'],retry=r['retry']))
    previous_end=began+timedelta(seconds=r['attempt_wall_seconds'])
assert not overlaps,overlaps
result=dict(status='verified',verified_utc=utc_now(),freeze_commit=commit,freeze_commit_utc=commit_time,
    first_evaluation_call_utc=first,last_evaluation_call_utc=last,estimator_hash=freeze['estimator_hash'],
    unchanged_frozen_source_files=len(freeze['source_hashes'])-len(rendering),frozen_source_snapshots_verified=len(freeze['source_hashes']),presentation_only_changes=sorted(rendering),planned_and_retained_workflows=len(planned),
    planned_and_replayed_policy_episodes=len(expected),scenario_bundles=32,replicates_per_bundle=3,
    evaluation_source_cases=96,scheduled_evaluation_calls=len(evaluation_calls),
    original_evidence_files_inventoried=len(inventory),publication_redacted_files=len(public_hashes),private_original_files_verified=private_verified,
    tokenization_usage_matches=input_matches,overlapping_attempt_intervals=overlaps,
    maximum_input_tokens=max(r.get('input_tokens',0) for r in finished),
    maximum_output_tokens=max((r.get('usage') or {}).get('completion_tokens',0) for r in finished),
    note='Frozen execution/scoring methods and estimator unchanged; two documented rendering-only corrections. All failed preparations remain included; no replacement cases or extra policy rows.')
write_json(root/'final_integrity_audit.json',result)
print(json.dumps(result,indent=2))
