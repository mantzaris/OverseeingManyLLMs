"""Immutable declared evaluation and source identity; no outcome-based selection."""
import argparse,hashlib,subprocess,time,sys
from datetime import datetime,timezone
from .common import ROOT,ART,read,write,digest
from .contracts import initial_manifest
from .controller import METHODS
FILES=['agents.py','client.py','common.py','contracts.py','controller.py','execution.py','evaluate.py','pipeline.py','statistics.py','collect.py','freeze.py']
def source_hashes():return {name:hashlib.sha256((ROOT/'research/coordination_injections'/name).read_bytes()).hexdigest() for name in FILES}
def declare():
 if (ART/'frozen/manifest.json').exists():raise RuntimeError('Freeze already exists')
 manifest=initial_manifest();dev=read(ART/'development/v5/summary.json');raw=[read(p) for p in (ART/'raw').glob('*.json')]
 good=[r for r in dev if r['epoch']==0];calls=[a['elapsed_seconds'] for r in raw for a in r['attempts']]
 manifest.update(protocol='coordination_injections_v5',frozen_utc=datetime.now(timezone.utc).isoformat(),methods=METHODS,round_limit=2,per_role_call_limit=2,stage_authorization_sha256=digest(read(ART/'authorization.json')),source_hashes=source_hashes(),data_sha256=read(ART/'downloads.json')[0]['sha256'] if False else 'f5385cbb54bbebf7196389109c6b0621faab0c304e3702548165e71c84aede8b',model=dict(name='Qwen/Qwen2.5-7B-Instruct',revision='a09a35458c702b33eeacc393d103063234e8bc28',dtype='bfloat16',temperature=.3,top_p=1,max_tokens=384,max_model_len=2048,serial=True,cpu_offload=0),primary='Targeted minus broadcast in mean continuation calls, with project correctness and its paired difference reported alongside; no noninferiority or equivalence claim.',comparisons=[['targeted','broadcast'],['targeted','shared_state'],['sparse','targeted']],metrics=['project_correct','accepted_correct','accepted_wrong','unfinished','requirement_violations','dependency_inconsistencies','V','calls','tokens','unnecessary_modifications','rounds','inference_seconds'],statistics=dict(unit='monthly data block; average both constructed projects and both replicas inside block',resamples=2000,seed=91843,interval='paired percentile bootstrap, all conditions kept together',limitations='Eight months from one retailer; serial dependence and one-organization generalization remain unresolved.'),secondary=dict(global_packet=dict(projects=[p['id'] for p in manifest['evaluation']],replicates=[0]),stress=dict(type='exception_generalization',projects=[p['id'] for p in manifest['evaluation'][::2]],replicates=[0],methods=METHODS),no_feedback=dict(projects=[p['id'] for p in manifest['evaluation'][::2]],replicates=[0],stress='exception_generalization')),failure_rules='Keep every predeclared project, failed generation, timeout, blocked artifact and incomplete run. No replacement or outcome-dependent extra repair. A cutoff retains pending rows as incomplete, never successful.',examples='First project in numeric ID order, replica 0, with targeted better/tied/worse project correctness than broadcast; if absent use first corresponding calls difference. First failure under any method is retained. No maximum-effect selection.',forecast=dict(development_raw_calls=len(raw),development_initial_correct_projects=sum(r['project_correct'] for r in good),development_initial_projects=len(good),mean_attempt_seconds=sum(calls)/len(calls),planned_initial_workflows=32,planned_primary_continuations=128,planned_secondary_continuations=56,expected_new_calls=760,conservative_new_calls=1150,expected_seconds_with_50percent_margin=760*sum(calls)/len(calls)*1.5,hard_ceiling_can_retain_incomplete=True))
 write(ART/'frozen/manifest.json',manifest)
 # A compact source snapshot preserves the collection implementation independently of future utility edits.
 import tarfile
 with tarfile.open(ART/'frozen/source.tar.gz','w:gz') as tar:
  for name in FILES:tar.add(ROOT/'research/coordination_injections'/name,arcname=name)
 print(manifest['forecast'])
def verify():
 m=read(ART/'frozen/manifest.json')
 if source_hashes()!=m['source_hashes']:raise RuntimeError('Frozen collection source changed')
 if digest(read(ART/'authorization.json'))!=m['stage_authorization_sha256']:raise RuntimeError('Authorization changed')
 rel='artifacts/coordination_injections/frozen/manifest.json'
 commit=subprocess.check_output(['git','log','-1','--format=%H','--',rel],cwd=str(ROOT)).decode().strip()
 if not commit:raise RuntimeError('Commit the freeze before evaluation')
 committed=subprocess.check_output(['git','show',commit+':'+rel],cwd=str(ROOT))
 if committed!=(ART/'frozen/manifest.json').read_bytes():raise RuntimeError('Uncommitted freeze')
 return m
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['declare','verify']);a=p.parse_args();declare() if a.action=='declare' else print(verify()['frozen_utc'])
