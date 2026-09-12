"""Separately frozen, post hoc parser sensitivity with actual fresh continuations."""
import argparse,hashlib,subprocess
from datetime import datetime,timezone
from .common import ROOT,ART,read,write,digest,stable
from .controller import run
from .agents import call,messages
from .normalize import normalize
from .evaluate import score
from .statistics import paired
from .freeze import verify
METHODS=['shared_state','broadcast','targeted','sparse','global_packet']
FILES=['normalize.py','parser_followup.py']
def hashes():return {p:hashlib.sha256((ROOT/'research/coordination_injections'/p).read_bytes()).hexdigest() for p in FILES}
def declare():
 verify();path=ART/'parser_followup/manifest.json'
 if path.exists():raise RuntimeError('Already declared')
 m=read(ART/'frozen/manifest.json');write(path,dict(declared_utc=datetime.now(timezone.utc).isoformat(),kind='Post hoc exploratory parser sensitivity on already inspected source cases, not new held-out evidence',projects=[p['id'] for p in m['evaluation']],replicates=[0],methods=METHODS,policy_order='rotate by project index, unchanged from frozen deterministic rule generalized to five methods',change='Normalize only recognized explicit tool/params envelopes using supplied values. Never fill task parameters from the contract or evaluator.',initial='Reuse the same correct frozen replica-0 checkpoint',actual_policy_specific_generations=True,scheduled_call_cap=320,session_ceiling_unchanged=True,comparisons=[['targeted','shared_state'],['targeted','broadcast'],['targeted','global_packet']],metrics=['project_correct','calls','accepted_wrong','unfinished','tokens'],statistics='Eight paired monthly blocks, 2000 bootstrap resamples, seed 91843; exploratory.',source_hashes=hashes(),primary_source_hashes=m['source_hashes'],failure_rule='Retain every malformed/incomplete response; same two rounds and per-role two-call cap; no source replacement or extra repair. Stop at 320 new calls or existing session cutoff.',forecast='80 continuations, about 260 calls, roughly 10 minutes with margin. All 16 replica-0 projects, no selection by prior success or method gains.'))
 print('Parser follow-up declared')
def verify_followup():
 verify();m=read(ART/'parser_followup/manifest.json')
 if m['source_hashes']!=hashes():raise RuntimeError('Follow-up code changed')
 rel='artifacts/coordination_injections/parser_followup/manifest.json';commit=subprocess.check_output(['git','log','-1','--format=%H','--',rel],cwd=str(ROOT)).decode().strip()
 if not commit or subprocess.check_output(['git','show',commit+':'+rel],cwd=str(ROOT))!=(ART/'parser_followup/manifest.json').read_bytes():raise RuntimeError('Commit the declaration before inference')
 return m

def normalized_call(*args):
 used=len(list((ART/'raw').glob('parser_followup_*.json')))
 if used>=320:raise RuntimeError('Parser follow-up ceiling')
 proposal,usage=call(*args);return normalize(proposal,args[1]),usage

def collect():
 m=verify_followup();root=ART/'parser_followup';rows=[];projects={p['id']:p for p in read(ART/'frozen/manifest.json')['evaluation']}
 for idx,pid in enumerate(m['projects']):
  p=projects[pid];initial=read(ART/'evaluation/frozen'/(pid+'_r0_initial.json'))['artifacts'];order=METHODS[idx%5:]+METHODS[:idx%5]
  for method in order:
   path=root/'runs'/(pid+'_r0_'+method+'.json')
   if path.exists():r=read(path)
   else:r=run(p,0,method,initial,normalized_call,phase='parser_followup');write(path,r)
   rows.append(score(p,r,initial));write(root/'rows.json',rows);print(pid,method,rows[-1]['project_correct'],rows[-1]['calls'],flush=True)
 comparisons=[paired(rows,left,right,metric) for left,right in m['comparisons'] for metric in m['metrics']];write(root/'comparisons.json',comparisons)
 return rows

def replay():
 from .replay import saved_call
 m=verify_followup();root=ART/'parser_followup';projects={p['id']:p for p in read(ART/'frozen/manifest.json')['evaluation']};rows=[];n=0;calls=0
 def replay_call(*args):
  proposal,usage=saved_call(*args);return normalize(proposal,args[1]),usage
 for pid in m['projects']:
  p=projects[pid];initial=read(ART/'evaluation/frozen'/(pid+'_r0_initial.json'))['artifacts']
  for method in METHODS:
   saved=read(root/'runs'/(pid+'_r0_'+method+'.json'));actual=run(p,0,method,initial,replay_call,phase='parser_followup')
   if stable(actual)!=stable(saved):raise AssertionError('Parser replay mismatch '+pid+' '+method)
   rows.append(score(p,saved,initial));n+=1;calls+=len(saved['calls'])
 expected=sorted(read(root/'rows.json'),key=lambda r:(r['project_id'],r['method']));observed=sorted(rows,key=lambda r:(r['project_id'],r['method']))
 if expected!=observed:raise AssertionError('Follow-up score replay differs')
 write(root/'replay.json',dict(passed=True,traces=n,requests=calls,inference_calls=0));print(n,'parser traces replayed',calls,'requests')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['declare','collect','replay']);a=p.parse_args();globals()[a.action]()
