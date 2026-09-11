"""Three GPU interpretations per project, cached for every policy comparison."""
import argparse
import hashlib
from .common import ART, read, write_json, canonical
from .client import generate, parsed
from .data import norm
EXTRACT='''Extract CURRENT travel preferences actually stated or accepted by the USER. Return JSON {"records":[{"key":"hotel.area","value":"centre","turn":0,"quote":"exact USER substring"}]}. Keys: hotel.area, hotel.pricerange, hotel.stars, hotel.type, restaurant.area, restaurant.pricerange, restaurant.food, attraction.area, attraction.type. Respect domain, changes and references. Assistant suggestions alone are not user decisions. Normalize area centre/north/south/east/west; price cheap/moderate/expensive; stars digits; lodging type hotel/guesthouse; other values lower-case. Omit unknown/no-preference. At most nine records, short exact source quotations. Do not supply confidence scores.'''
HISTORY='''Answer the listed CURRENT travel preference fields from the supplied USER dialogue. Respect domains, changes, exceptions and explicit references. Assistant suggestions alone are not user decisions. Return JSON {"answers":{"hotel.area":"centre"}} keyed by every requested field; use UNKNOWN when unsupported. Normalize area centre/north/south/east/west; price cheap/moderate/expensive; stars digits; lodging type hotel/guesthouse; cuisine and attraction type lower-case. No confidence scores.'''
MEMORY='''Answer the requested travel preference fields from ALL supplied current shared memories. Select by domain and attribute; do not transfer a similar value across domains. Memories were extracted from a user dialogue and may be incomplete or wrong. Return JSON {"answers":{"hotel.area":"centre"}}, every requested field, UNKNOWN when absent/conflicting. Normalize area centre/north/south/east/west; price cheap/moderate/expensive; stars digits; lodging hotel/guesthouse; others lower-case. No confidence scores.'''

def text(case):return '\n'.join('%d %s: %s'%(t['turn'],t['role'].upper(),t['text']) for t in case['messages'])

def records(output,case):
    rows=output.get('records',[]) if isinstance(output,dict) else [];out={};reject=[]
    turns={m['turn']:m for m in case['messages']}
    if not isinstance(rows,list):return {},['bad_records']
    for row in rows:
        if not isinstance(row,dict):reject.append('bad_record');continue
        key=row.get('key');value=norm(row.get('value',''));source=turns.get(row.get('turn')) if isinstance(row.get('turn'),int) else None;quote=row.get('quote','')
        if key not in case['fields'] or not value or value in ('unknown','none','dontcare'):continue
        if not source or source['role']!='user' or not isinstance(quote,str) or not quote or quote.lower() not in source['text'].lower():
            reject.append(dict(record=row,reason='source_guard'));continue
        out[key]=dict(row,value=value)
    return out,reject

def answers(output):
    rows=output.get('answers',output) if isinstance(output,dict) else {}
    if not isinstance(rows,dict):return {}
    return {k:norm(v) for k,v in rows.items() if isinstance(v,str) and norm(v) not in ('unknown','','none','dontcare')}

def case_calls(case,replicate):
    prefix='%s_%s_%d'%(case['split'],case['id'][:-5],replicate)
    seed=910000+replicate*100000+int(hashlib.sha256(case['id'].encode()).hexdigest()[:6],16)%90000
    outputs={};calls=[]
    for i,kind in enumerate(['extract','history','memory']):
        prompt={'extract':EXTRACT,'history':HISTORY,'memory':MEMORY}[kind]
        payload=text(case) if kind=='extract' else text(case)+'\nFIELDS '+canonical(case['fields']) if kind=='history' else canonical(dict(memories=list(records(outputs['extract'],case)[0].values()),fields=case['fields']))
        raw=generate(prefix+'_'+kind,[dict(role='system',content=prompt),dict(role='user',content=payload)],seed+i,640 if kind=='extract' else 256)
        outputs[kind]=parsed(raw);calls.append(dict(id=raw['call_id'],status=raw['status'],parsed=outputs[kind] is not None))
    prepared=dict(id=case['id'],replicate=replicate,outputs=outputs,calls=calls)
    write_json(ART/'prepared'/(prefix+'.json'),prepared)
    return prepared

def main():
    p=argparse.ArgumentParser();p.add_argument('--split',choices=['development','evaluation'],required=True);a=p.parse_args()
    if a.split=='evaluation':
        from .freeze import verify
        verify(require_commit=True)
    for case in read(ART/'data/public.json'):
        if case['split']!=a.split:continue
        for replicate in range(2):
            r=case_calls(case,replicate);print(case['id'],replicate,[(c['status'],c['parsed']) for c in r['calls']],flush=True)
if __name__=='__main__':main()
