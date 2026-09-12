"""Versioned development backends; v1 remains replayable."""
import importlib.util
from types import SimpleNamespace,ModuleType
from .common import ROOT,ART,read,digest
from . import representation,patches

def recorded_patch(revision):
 snapshot=read(ART/('development_'+revision+'_source.json'));assert digest(snapshot['files'])==snapshot['sha256']
 p=ModuleType('research.correction_applicability._'+revision+'_patch_snapshot');p.__package__='research.correction_applicability';exec(compile(snapshot['files']['patches.py'],'development_'+revision+'_source:patches.py','exec'),p.__dict__);return p

def load(revision):
 if revision=='v1':
  p=recorded_patch('v1')
  return SimpleNamespace(messages=representation.messages,parse=representation.parse,contract=representation.contract,executed_answer=representation.executed_answer,infer=p.infer,apply_to_state=p.apply_to_state)
 if revision not in ['v2','v2_guarded']:raise ValueError('Unknown recorded backend')
 from . import representation_v2 as r
 if revision=='v2':
  p=recorded_patch('v2')
 else:
  spec=importlib.util.spec_from_file_location('research.correction_applicability._patches_guarded',ROOT/'research/correction_applicability/patches.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
 p.contract=r.contract;p.rebind=r.rebind;p.period_evidence=lambda c,ref:r.binding(c,ref)["periods"]
 return SimpleNamespace(messages=r.messages,parse=r.parse,contract=r.contract,executed_answer=r.executed_answer,infer=p.infer,apply_to_state=p.apply_to_state,supported_spans=r.supported_spans)
