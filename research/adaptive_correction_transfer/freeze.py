"""Freeze public source-order selection, model, analysis and execution limits."""
import hashlib,subprocess,datetime
from .common import ART,ROOT,read,write,digest
from .answers import messages
from .client import http,MODEL,REVISION
from .data import annotations,normalized
CODE=['answers.py','client.py','collect.py','controller.py','data.py','features.py','feedback.py','inference.py','learner.py','scoring.py','common.py','analyze.py','freeze.py','vendor/tatqa_metric.py','vendor/tatqa_utils.py']
def hashes():
 return {p:hashlib.sha256((ROOT/'research/adaptive_correction_transfer'/p).read_bytes()).hexdigest() for p in CODE}
def build():
 if (ART/'frozen/manifest.json').exists():raise RuntimeError('Freeze exists')
 dev=read(ART/'development_manifest.json')['contexts'];paragraphs={normalized(p['text']) for c in dev for p in c['paragraphs'] if len(normalized(p['text']))>=160};selected=[];audit=[]
 for c in read(ART/'eligible_public.json')['test_gold']:
  duplicate=any(normalized(p['text']) in paragraphs for p in c['paragraphs'] if len(normalized(p['text']))>=160)
  counts=[]
  if not duplicate:
   for q in c['questions']:
    t=http('/tokenize',dict(model=MODEL,messages=messages(c,q),add_generation_prompt=True));counts.append(t.get('count',len(t.get('tokens',[]))))
  reason='exact_long_development_paragraph' if duplicate else 'initial_prompt_over_1200_tokens' if max(counts)>1200 else None
  audit.append(dict(id=c['id'],source_index=c['source_index'],excluded=reason,initial_tokens=counts))
  if reason is None:selected.append(c)
  if len(selected)==24:break
 if len(selected)!=24:raise RuntimeError('Insufficient public eligible contexts')
 # Formula uses actual question counts, two replicas, two inspections, four capped repair policies and broad memory.
 primary=sum(2*(len(c['questions'])+2*len(c['questions'])-3+4*6) for c in selected)
 raw=list((ART/'raw').glob('*.json'));used=len(raw)
 # Reserve the unfinished development protocol, not a forecast selected from evaluation outcomes.
 frozen_n=12;budget3_n=8;upper=primary+frozen_n*6+budget3_n*2*3
 auth=read(ART/'authorization.json')
 if used+160+upper>auth['scheduled_call_ceiling']:raise RuntimeError('Forecast exceeds ceiling: '+str((used,upper)))
 times=[x['elapsed_seconds'] for p in raw for x in read(p)['attempts'] if x['status']=='ok'];times.sort();mean=sum(times)/len(times);p90=times[int(.9*len(times))]
 manifest=dict(stage='adaptive_correction_transfer',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),prefix='evaluation',contexts=selected,replicates=[0,1],methods=['individual','memory','source_rule','fixed_audit','adaptive','reattempt','individual_risk'],budgets=[0,1,2],frozen_model_contexts=frozen_n,budget3_contexts=budget3_n,budget3_methods=['adaptive','fixed_audit'],model=dict(name=MODEL,revision=REVISION,dtype='bfloat16',gpu='RTX6000Ada',cpu_offload=0,temperature=.3,top_p=1,max_tokens=288,max_context=2048),initial_model_sha256=digest(read(ART/'initial_model.json')),selection='First24 eligible released test_gold contexts in source order; original technical eligibility preserved, exact long paragraph overlap with development excluded, every initial prompt <=1200 model tokens. No performance selection.',order='Rotate seven policies by (source_index_in_manifest+replica) modulo7; all initial checkpoints shared. Fresh continuations by policy; identical full requests reused only for an unchanged budget-prefix.',seeds='Initial 861000+i*100+rep*10+q; repair 871000+i*100+rep*30+step*10+q; selection881000+i*100+rep. Independent of policy execution order.',inspection='One unit reveals only selected question answer, scale, derivation and answer_type; direct reference replacement. No sibling gold or recipient list. B2 primary, B1 prefix, B3 first8 replica0 secondary.',primary='At budget2, adaptive minus fixed_audit official exact-match proportion, paired context means averaging two replicas. Adaptive vs individual_risk is the practical no-transfer comparison; all other declared contrasts secondary.',analysis='Official EM/F1 plus exact scale, joint correctness, inspected and never-inspected outcomes, accepted and proposed harm, unfinished, calls/tokens. 2000 paired context bootstrap resamples seed91844; replicas averaged before sampling; W/T/L at context level. No noninferiority/equivalence claim or multiplicity-adjusted significance.',comparisons=['adaptive-fixed_audit','adaptive-individual_risk','adaptive-individual','adaptive-memory','adaptive-source_rule','source_rule-reattempt','memory-individual','adaptive-frozen_model'],failure='Keep every selected context and initial output. Malformed/failed generations score zero initially; failed repairs retain prior answer with raw failure recorded. No gold rescue. Missing planned outcomes explicit; never replace a source or rerun based on results.',examples='For helpful, neutral and harmful transfer, choose first qualifying source in manifest order, then replica, step, recipient source order, under adaptive; if absent use memory and label it. Paired examples first positive, tied, negative adaptive-fixed_audit context.',forecast=dict(existing_calls=used,development_protocol_reserve=160,evaluation_call_upper=upper,primary_call_upper=primary,mean_generation_seconds=mean,p90_generation_seconds=p90,conservative_seconds=upper*max(mean*1.5,p90),note='Serial generation. Preflight context failures consume scheduled calls but no generation attempts. Final runtime reserve protected by authorization cutoff.'),ceilings=auth,source_hashes=hashes())
 write(ART/'frozen/manifest.json',manifest);write(ART/'frozen/selection_audit.json',audit)
 gold=annotations('test_gold');write(ART/'frozen/evaluator_annotations.json',{c['id']:gold[c['id']] for c in selected})
 write(ART/'frozen/integrity.json',dict(manifest=digest(manifest),evaluator_annotations=digest(read(ART/'frozen/evaluator_annotations.json'))))
 print('Frozen',len(selected),'contexts',sum(len(c['questions']) for c in selected),'questions',manifest['forecast'])
def verify():
 m=read(ART/'frozen/manifest.json');i=read(ART/'frozen/integrity.json')
 assert digest(m)==i['manifest'];assert digest(read(ART/'frozen/evaluator_annotations.json'))==i['evaluator_annotations'];assert hashes()==m['source_hashes'];assert digest(read(ART/'initial_model.json'))==m['initial_model_sha256']
 # Require a committed declaration before any evaluation generation.
 path='artifacts/adaptive_correction_transfer/frozen/manifest.json'
 b=subprocess.check_output(['git','show','HEAD:'+path],cwd=ROOT)
 assert b==(ROOT/path).read_bytes(),'Frozen declaration must be committed'
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');a=p.parse_args();verify() if a.verify else build()
