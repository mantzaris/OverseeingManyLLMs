"""Deterministic saved-output replay, without any model generations."""
import argparse,csv,json,shutil
from pathlib import Path
from .common import ART,ROOT,read,write_json,digest
from .freeze import verify
from .provenance_tools import source,repaired_source
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
 from .repair_freeze import verify as repair_verify
 from .repair_evaluate import run as repair_run
 repair_verify();repaired_source();repair_run('evaluation',out/'repair/evaluation')
 repaired_n=compare_csv(ART/'repair/evaluation/episodes.csv',out/'repair/evaluation/episodes.csv',['controller_seconds'])
 shutil.copyfile(ART/'repair/evaluation/episodes.csv',out/'repair/evaluation/episodes.csv')
 analyze(out/'repair')
 for name in ['summary.json','paired.json','coverage.json','examples.json']:
  if read(ART/'repair/analysis'/name)!=read(out/'repair/analysis'/name):raise AssertionError('Repaired analysis differs '+name)
 if read(ART/'repair/evaluation/traces.json')!=read(out/'repair/evaluation/traces.json'):raise AssertionError('Repaired events differ')
 from .secondary_analysis import run as secondary
 secondary(out/'repair',source_root=ART/'repair')
 from .source_reader_audit import run as reader
 reader(True,output=out/'repair/analysis/direct_source_reader.json')
 plot(out/'repair',synthetic_root=out)
 from .example_analysis import run as examples
 examples(out/'repair',synthetic_root=out)
 for name in ['secondary.json','direct_source_reader.json','matched_examples.json']:
  if read(ART/'repair/analysis'/name)!=read(out/'repair/analysis'/name):raise AssertionError('Secondary analysis differs '+name)
 from .direct_reader import evaluate as direct_evaluate
 from .direct_analysis import run as direct_analysis
 direct_evaluate(out/'direct_reader_audit');direct_analysis(out/'direct_reader_audit',out/'repair')
 direct_n=compare_csv(ART/'direct_reader_audit/episodes.csv',out/'direct_reader_audit/episodes.csv')
 for name in ['traces.json','analysis.json']:
  if read(ART/'direct_reader_audit'/name)!=read(out/'direct_reader_audit'/name):raise AssertionError('Direct-reader audit differs '+name)
 from .integrity_sensitivity import run as quarantine
 quarantine(out/'integrity_sensitivity')
 integrity_n=compare_csv(ART/'integrity_sensitivity/episodes.csv',out/'integrity_sensitivity/episodes.csv')
 if read(ART/'integrity_sensitivity/analysis.json')!=read(out/'integrity_sensitivity/analysis.json'):raise AssertionError('Integrity sensitivity differs')
 report=dict(status='passed',initial_flawed_adapter_rows=n,repaired_empirical_rows=repaired_n,synthetic_rows=m,policy_and_event_replay=True,analysis_tables=8,secondary_tables=3,posthoc_direct_reader_rows=direct_n,integrity_sensitivity_rows=integrity_n,numerical_figures=8,new_model_calls=0,output=str(out))
 write_json(out/'verification.json',report);print(json.dumps(report,indent=2));return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();run(a.output)
