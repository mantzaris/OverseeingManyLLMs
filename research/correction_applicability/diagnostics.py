"""Saved-output failure diagnosis and development gate; no new model requests."""
import collections,copy
from .common import ART,read,write
from .analyze import csvout
from .backend import load
from .representation import evaluate
from . import representation_v2
from research.adaptive_correction_transfer.scoring import score

def analyze():
 cs=read(ART/'development_manifest.json')['contexts'];gold=read(ART/'offline_development_annotations.json')['annotations'];rows=[];donors=[];examples={};summaries=[]
 for revision in ['v1','v2']:
  engine=load(revision);types=collections.Counter();failures=collections.Counter();counts=collections.Counter()
  for i,c in enumerate(cs):
   init=read(ART/('development_'+revision)/('c%02d_initial.json'%i));r=read(ART/('development_'+revision)/('c%02d_patch.json'%i))
   for q in c['questions']:
    a=init['answers'][q['id']];rep=a.get('rep');errs=engine.contract(c,q,rep);counts['questions']+=1;counts['executable']+=a['representation_valid'];counts['public_contract']+=not errs;types[gold[c['id']][q['id']]['answer_type']]+=1
    reason='unsupported' if rep is None else ';'.join(a['representation_errors']) if not a['representation_valid'] else ';'.join(errs) if errs else 'passes_public_contract'
    failures[reason]+=1
    # Post hoc, representation-only diagnostic. Reuse the generated v1 operand hypotheses,
    # read their metadata from public cells under v2, but never replace the evaluated v1 run.
    normalized=None
    if revision=='v1' and isinstance(rep,dict):
     p=representation_v2.parse({'rep':{k:rep.get(k) for k in ['op','refs','expression','scale']}},c);normalized=not representation_v2.contract(c,q,p.get('rep'));counts['metadata_only_contract']+=normalized
    rows.append(dict(revision=revision,context=c['id'],question=q['id'],answer_type=gold[c['id']][q['id']]['answer_type'],executable=a['representation_valid'],public_contract=not errs,reason=reason,metadata_only_contract=normalized))
    key=revision+':'+reason
    if key not in examples:examples[key]=dict(source_index=i,question=q,answer=a,kind='First qualifying development source/question in fixed order; not a fresh case.')
   for e in r['events']:
    if e['kind']!='inspection':continue
    p=e['patch'];counts['inspections']+=1;counts['supported_patches']+=p['supported'];counts['accepted_revisions']+=sum(x['accepted'] for x in e['revisions']);old=p.get('old_rep');new=p.get('new_rep')
    old_exec=new_exec=False
    try:evaluate(old,c);old_exec=True
    except Exception:pass
    try:evaluate(new,c);new_exec=True
    except Exception:pass
    donors.append(dict(revision=revision,context=c['id'],question=e['inspected'],answer_type=gold[c['id']][e['inspected']]['answer_type'],old_exec=old_exec,new_exec=new_exec,supported=p['supported'],reason=';'.join(p['reasons'])))
  summaries.append(dict(revision=revision,**counts,answer_types=dict(types),failure_categories=dict(failures)))
 csvout(ART/'diagnostics/representations.csv',rows);csvout(ART/'diagnostics/donors.csv',donors);write(ART/'diagnostics/summary.json',summaries);write(ART/'diagnostics/first_examples.json',examples)
 gate=dict(decision='STOP_FRESH_EVALUATION',basis='The completed two development versions generated zero reusable patches and zero commits. No correction-dependent sibling improvement was observed; generic verification and the scope ablation were also coverage-limited. A zero-revision method has not solved reuse.',fresh_heldout_contexts=0,untouched_pool_available=len(read(ART/'source_pool_audit.json')['unused_test_candidates']),development_contexts=12,development_questions=72,versions=2,refinements=2,source='Previously inspected training contexts, one generation set per version; versions are not independent replicas.',next_action='Complete diagnostics, structural tests, replay, interface and report. Do not spend remaining authorized calls on unsupported expansion.')
 write(ART/'development_gate.json',gate);print(summaries);print(gate['decision'])
if __name__=='__main__':analyze()
