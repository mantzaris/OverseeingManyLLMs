"""Deterministic source selection and constructed planning roles. No inference."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from .client import ART, canonical, write_json

SLOTS={'hotel':['area','pricerange','stars','type'],
       'restaurant':['area','pricerange','food']}
PHRASES={
 'hotel.area':['Which part of town should the hotel be in?', 'For the lodging search, what location does the user want?'],
 'hotel.pricerange':['What price range should the hotel match?', 'Which spending band applies to accommodation?'],
 'hotel.stars':['How many stars should the hotel have?', 'What star rating is wanted for the lodging?'],
 'hotel.type':['Should the accommodation be a hotel or a guesthouse?', 'Which kind of lodging did the user request?'],
 'restaurant.area':['Which part of town should the restaurant be in?', 'What location applies to dining?'],
 'restaurant.pricerange':['What price range should the restaurant match?', 'Which spending band applies to eating out?'],
 'restaurant.food':['What food should the restaurant serve?', 'Which cuisine does the user want for dining?'],
}
ROLES=['lodging_shortlist','dining_shortlist','budget_brief','location_brief','itinerary_brief','stay_specification']

def normalize(value):
    return str(value).lower().strip().replace('guest house','guesthouse').replace('city centre','centre').replace('center','centre')

def annotated_state(log,index):
    return {domain+'.'+slot:normalize(log[index]['metadata'][domain]['semi'].get(slot,''))
            for domain in SLOTS for slot in SLOTS[domain]
            if normalize(log[index]['metadata'][domain]['semi'].get(slot,''))
            not in ('','not mentioned','dontcare','dont care','do not care','none')}

def supported(log,index,state):
    # A conservative source-screen, not an entailment oracle: keep only annotation
    # values mentioned in user text. Domain attribution remains an annotation limit.
    texts=[(i,normalize(t['text'])) for i,t in enumerate(log) if i<=index and i%2==0]
    result={};proof={}
    for key,value in state.items():
        alternatives=[value]
        if key.endswith('.stars'):
            word={'0':'zero','1':'one','2':'two','3':'three','4':'four','5':'five'}.get(value,'invalid')
            alternatives=[value+' star',value+'-star',word+' star',word+'-star']
        found=[i for i,t in texts if any(v in t for v in alternatives)]
        if found:result[key]=value;proof[key]=found
    return result,proof

def candidates(data,ids):
    accepted=[];excluded=[]
    for key in sorted(ids):
        log=data[key]['log'];prev={};changes=[]
        for i in range(1,len(log),2):
            state,_=supported(log,i,annotated_state(log,i))
            if any(k in prev and v!=prev[k] for k,v in state.items()):changes.append(i)
            prev=state
        final,proof=supported(log,len(log)-1,annotated_state(log,len(log)-1))
        if len(final)<4 or not all(any(k.startswith(d+'.') for k in final) for d in SLOTS):
            excluded.append(dict(id=key,reason='Fewer than four supported final fields or missing workflow domain'));continue
        before=changes[-1]-2 if changes else max(1,(len(log)//4)*2-1)
        first,first_proof=supported(log,before,annotated_state(log,before))
        changed=sorted(k for k in final if k in first and first[k]!=final[k])
        if changes and not changed:
            excluded.append(dict(id=key,reason='Intermediate change not retained in final supported state'));continue
        accepted.append(dict(id=key,before=before,changed=changed,
                             states=[first,final],proof=[first_proof,proof]))
    return accepted,excluded

def queries(keys):
    return [[dict(id='q%d_%d'%(variant,i),text=PHRASES[k][variant])
             for i,k in enumerate(sorted(keys))] for variant in range(2)]

def role_keys(role,keys):
    if role=='lodging_shortlist':return [k for k in keys if k.startswith('hotel.')]
    if role=='dining_shortlist':return [k for k in keys if k.startswith('restaurant.')]
    if role=='budget_brief':return [k for k in keys if k.endswith('.pricerange')]
    if role=='location_brief':return [k for k in keys if k.endswith('.area')]
    if role=='stay_specification':return [k for k in keys if k.startswith('hotel.') and not k.endswith('.area')]
    return list(keys)

def build(source):
    source=Path(source);data=json.load((source/'data.json').open());selection={};audit={}
    for split,n in [('val',4),('test',12)]:
        ids=(source/(split+'ListFile.json')).read_text().split()
        pool,excluded=candidates(data,ids)
        selected=sorted([x for changed in (False,True) for x in [r for r in pool if bool(r['changed'])==changed][:n]],key=lambda x:x['id'])
        selection[split]=selected;audit[split]=dict(eligible=len(pool),eligible_changed=sum(bool(x['changed']) for x in pool),
                                                 excluded=excluded,selection_rule='First %d sorted eligible IDs in each unchanged/changed stratum'%n)
    assert not set(x['id'] for x in selection['val']) & set(x['id'] for x in selection['test'])
    public=[];private=[]
    for split in ('val','test'):
        for row in selection[split]:
            log=data[row['id']]['log'];keys=sorted(PHRASES)
            messages=[dict(turn=i,role='user' if i%2==0 else 'assistant',text=t['text']) for i,t in enumerate(log)]
            public.append(dict(id=row['id'],split='development' if split=='val' else 'evaluation',
                               project=row['id'][:-5],stages=[messages[:row['before']+1],messages],
                               queries=queries(keys),keys=keys,
                               # These are constructed public artifact requirements, not hidden answer values.
                               available_fields=[sorted(s) for s in row['states']]))
            private.append(dict(id=row['id'],split=split,before=row['before'],changed_fields=row['changed'],
                                annotation_states=row['states'],lexical_support_turns=row['proof']))
    dest=ART/'data';dest.mkdir(parents=True,exist_ok=True)
    write_json(dest/'public_projects.json',public);write_json(dest/'evaluation_only.json',private)
    write_json(dest/'source_audit.json',audit)
    for name in ('hotel_db.json','restaurant_db.json'):
        shutil.copyfile(source/name,dest/name)
    license_path=Path('/tmp/decision-sources/multiwoz24_LICENSE')
    if license_path.exists():shutil.copyfile(license_path,dest/'UPSTREAM_LICENSE.txt')
    write_json(dest/'manifest.json',dict(source_revision='6807c1d85f547fcaae10494d26991d2d37c90a63',
        selected={k:[x['id'] for x in v] for k,v in selection.items()},
        files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.iterdir()) if p.name!='manifest.json'},
        evidence='Human task-elicited dialogues; corrected benchmark states and database records; authored agent roles. No observed use of this interface.'))
    print('Prepared',len(public),'source projects', {k:len(v) for k,v in selection.items()})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);build(p.parse_args().source)
