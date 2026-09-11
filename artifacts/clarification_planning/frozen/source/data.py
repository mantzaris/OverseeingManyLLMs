"""Pinned-source screening. Annotation values stay in a separate evaluator file."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from collections import Counter
from .common import ART, ROOT, read, write_json, canonical
from research.decision_dependencies.data import normalize, supported

SLOTS={'hotel':['area','pricerange','stars','type'],
       'restaurant':['area','pricerange','food'], 'attraction':['area','type']}

def norm(v):
    v=normalize(v)
    return {'center of town':'centre','centre of town':'centre','guest-house':'guesthouse'}.get(v,v)

def state(log,index):
    result={}
    for domain,slots in SLOTS.items():
        for slot in slots:
            v=norm(log[index].get('metadata',{}).get(domain,{}).get('semi',{}).get(slot,''))
            if v not in ('','not mentioned','dontcare','dont care','do not care','none'):
                result[domain+'.'+slot]=v
    return supported(log,index,result)

def prior_exclusions():
    old=ROOT/'artifacts/decision_dependencies';ids={c['id'] for c in read(old/'data/public_projects.json')}
    ids.update(x[0] for x in read(old/'development/probe_declaration.json')['cases'])
    # Also audit all saved generated requests, preparations, UI and manually selected
    # examples for actual source IDs. Exclusion lists alone are not outcome inspection.
    paths=list((old/'prepared').glob('*.json'))+list((old/'raw').glob('*.json'))
    paths+=list((old/'interpretation').glob('*example*.json'))
    pattern=re.compile(r'\b(?:P?MUL|SNG|SSNG|WOZ|PMUL)\d+(?:\.json)?\b')
    for p in paths:
        ids.update(m if m.endswith('.json') else m+'.json' for m in pattern.findall(p.name+' '+p.read_text()))
    return ids

def build(source,development=12,evaluation=48):
    source=Path(source);raw=read(source/'data.json');excluded=prior_exclusions()
    by_text={hashlib.sha256(canonical(v['log']).encode()).hexdigest():k for k,v in raw.items() if k in excluded}
    goals=set();public=[];private=[];audit=[];counts={}
    for split,n in [('val',development),('test',evaluation)]:
        candidates=[]
        for id in sorted((source/(split+'ListFile.json')).read_text().split()):
            log=raw[id]['log'];prefix=log # No artificial withholding of known source facts.
            target,proof=state(log,len(log)-1)
            signature=hashlib.sha256(canonical({d:raw[id]['goal'].get(d,{}) for d in SLOTS}).encode()).hexdigest()
            textsha=hashlib.sha256(canonical(log).encode()).hexdigest()
            reason=''
            if id in excluded:reason='previously_used_or_inspected'
            elif textsha in by_text:reason='exact_dialogue_duplicate_of_previous'
            elif len({k.split('.')[0] for k in target})<2:reason='fewer_than_two_supported_domains'
            # Selection uses source text length, not a generated tokenizer/outcome.
            elif sum(len(t['text']) for t in log)>4500:reason='source_text_over_4500_characters'
            elif signature in goals:reason='duplicate_selected_project_goal'
            if reason:audit.append(dict(id=id,split=split,reason=reason));continue
            candidates.append((id,target,proof,signature,textsha))
        counts[split]=dict(eligible=len(candidates),required_fields_histogram=dict(Counter(len(c[1]) for c in candidates)),
                          domains_histogram=dict(Counter(len({k.split('.')[0] for k in c[1]}) for c in candidates)))
        selected=[]
        for row in candidates:
            if len(selected)>=n:break
            if row[3] in goals:
                audit.append(dict(id=row[0],split=split,reason='duplicate_selected_project_goal'));continue
            goals.add(row[3]);selected.append(row)
        if len(selected)!=n:raise ValueError('Insufficient source pool')
        for id,target,proof,signature,textsha in selected:
            log=raw[id]['log'];messages=[dict(turn=i,role='user' if i%2==0 else 'assistant',text=t['text']) for i,t in enumerate(log)]
            tasks=[dict(id=d+'_shortlist',domain=d,required=sorted(k for k in target if k.startswith(d+'.')),
                        error_weight=4.,defer_weight=1.) for d in SLOTS if any(k.startswith(d+'.') for k in target)]
            public.append(dict(id=id,split='development' if split=='val' else 'evaluation',messages=messages,
                               fields=sorted(target),tasks=tasks))
            private.append(dict(id=id,target=target,lexical_support_turns=proof,source_split=split,
                                goal_sha256=signature,dialogue_sha256=textsha))
    dest=ART/'data';dest.mkdir(parents=True,exist_ok=True)
    write_json(dest/'public.json',public);write_json(dest/'evaluation_only.json',private)
    write_json(dest/'audit.json',dict(previously_exposed_ids=sorted(excluded),pool=counts,exclusions=audit,
         selection='First eligible source IDs in lexicographic order, 12 official val / 48 official test, with at least two supported domains, without change/complementarity strata; no model outcome filtering',
         independence='Dialogue is unit. Shared benchmark databases/templates and unidentified source participants remain dependence limits.',
         task_construction='One distinct executable shortlist per supported domain. Public required field names derive from current annotations with user lexical support. Correct values evaluator-only.',
         cross_domain_sharing='Not inferred from equal values. Main source adapter has domain-specific decisions; authored scope/exception challenges are separate.',
         source_revision='6807c1d85f547fcaae10494d26991d2d37c90a63'))
    for domain in SLOTS:shutil.copyfile(source/(domain+'_db.json'),dest/(domain+'_db.json'))
    shutil.copyfile(ROOT/'research/decision_dependencies/data_provenance.json',dest/'upstream_provenance.json')
    shutil.copyfile(ROOT/'artifacts/decision_dependencies/data/UPSTREAM_LICENSE.txt',dest/'UPSTREAM_LICENSE.txt')
    write_json(dest/'hashes.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.iterdir() if p.name!='hashes.json'})
    print('Selected',len(public),'dialogues, prior exclusions',len(excluded),counts)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',default='/tmp/decision-source-rebuild/upstream/MULTIWOZ2.4');build(p.parse_args().source)
