"""Deterministic saved-output replay, without any model generations."""
import argparse,csv,json,shutil
from pathlib import Path
from .common import ART,ROOT,read,write_json,digest
from .freeze import verify
from .provenance_tools import source
from .evaluate import run as empirical_run
from .synthetic import run as synthetic_run
from .analyze import run as analyze

def compare_csv(a,b,ignore=()):
 x=list(csv.DictReader(Path(a).open()));y=list(csv.DictReader(Path(b).open()))
 for rows in [x,y]:
  for r in rows:
   for k in ignore:r.pop(k,None)
 if x!=y:
  index=next((i for i,(u,v) in enumerate(zip(x,y)) if u!=v),None);raise AssertionError('Replay differs at '+str(index)+' '+str(a))
 return len(x)

def run(out):
 out=Path(out).resolve()
 if out==ROOT or ROOT in out.parents:raise ValueError('Replay output must be outside the repository')
 if out.exists() and any(out.iterdir()):raise ValueError('Use an empty replay directory')
 out.mkdir(parents=True,exist_ok=True);verify();source()
 empirical_run('evaluation',out/'evaluation');synthetic_run(out/'synthetic')
 n=compare_csv(ART/'evaluation/episodes.csv',out/'evaluation/episodes.csv',['controller_seconds']);m=compare_csv(ART/'synthetic/episodes.csv',out/'synthetic/episodes.csv')
 # Keep original measured latency rather than presenting replay latency as new evidence.
 shutil.copyfile(ART/'evaluation/episodes.csv',out/'evaluation/episodes.csv')
 analyze(out)
 for name in ['summary.json','paired.json','coverage.json','examples.json']:
  if read(ART/'analysis'/name)!=read(out/'analysis'/name):raise AssertionError('Analysis differs '+name)
 if read(ART/'evaluation/traces.json')!=read(out/'evaluation/traces.json'):raise AssertionError('Event replay differs')
 if read(ART/'synthetic/example_traces.json')!=read(out/'synthetic/example_traces.json'):raise AssertionError('Synthetic events differ')
 from .plot import run as plot
 plot(out)
 report=dict(status='passed',empirical_rows=n,synthetic_rows=m,policy_and_event_replay=True,analysis_tables=4,new_model_calls=0,output=str(out))
 write_json(out/'verification.json',report);print(json.dumps(report,indent=2));return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();run(a.output)
