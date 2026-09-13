"""Public real-source inputs; no participant exports and no model inference."""
from pathlib import Path
from itertools import zip_longest
import hashlib
from research.oversight_workflow.common import ROOT,ART,read,write,digest
from research.oversight_workflow.data import task
from research.oversight_workflow.pilot.adapter import saved_output

HERE=Path(__file__).resolve().parent
OUT=ROOT/'artifacts/oversight_simulation'
POLICIES=['Q','G','Q-source-aware','Q-sticky','M']


def build_inputs():
    m=read(ROOT/'research/oversight_workflow/matched/manifest.json')
    contexts={c['id']:c for c in read(ART/'frozen/manifest.json')['contexts']}
    packets=[];items={};sources={}
    for p in m['packets']:
        groups=[]
        for cid in p['context_ids']:
            c=contexts[cid];group=[]
            for q in c['questions']:
                if q['id'] not in p['question_ids']:continue
                o,raw=saved_output(c,q)
                t=task(c,q,0);sources[cid]=t['source']
                item=dict(id=q['id'],source_id=cid,question=q['question'],agent=t['agent'],output=o,raw=raw,
                          source_characters=sum(len(str(v)) for row in c['table'] for v in row)+sum(len(x['text']) for x in c['paragraphs']))
                items[q['id']]=item;group.append(q['id'])
            groups.append(group)
        packets.append(dict(source_ids=p['context_ids'],groups=groups))
    assert len(items)==36 and len(sources)==6
    x=dict(schema='oversight-simulation-inputs-v1',record_kind='computational_simulation_inputs',matched_manifest_sha256=m['manifest_sha256'],packets=packets,items=items,sources=sources,
           provenance=dict(dataset='TAT-QA',revision='870accc41953dcde885aabeb963d94aabdc0fbc3',source='Real financial report material and original benchmark questions; already inspected matched packets',drafts='Actual saved generations, replica 0; pilot uniform display projection',arrivals='Constructed; not workplace arrivals',reviewer='Simulated; not participant or investigator-practice observations',independence='36 questions / 6 contexts / 3 packets; report independence unavailable; rotations and seeds are not new sources'))
    x['sha256']=digest(x);return x


def workload(inputs, config, rotation):
    n=config['offered'];packet_order=[(rotation+i)%3 for i in range(3)]
    groups=[g for p in packet_order for g in inputs['packets'][p]['groups']]
    groups=([g[:3] for g in groups[:2]] if n==6 else groups[:n//6])
    ids=([x for row in zip_longest(*groups) for x in row if x] if config['source_order']=='interleaved' else [x for g in groups for x in g])
    assert len(ids)==n and len(set(ids))==n
    pattern=config['arrival']
    if pattern=='two_wave':
        half=n//2;starts=[(0 if i<half else 180)+20*(i%half)/max(1,half-1) for i in range(n)]
    elif pattern=='burst':starts=[0.]*n
    elif pattern=='spread':starts=[480*i/max(1,n-1) for i in range(n)]
    else:raise ValueError(pattern)
    # The original 12-question schedule is exactly 0,4,...,20; 180,184,...,200.
    return [dict(**inputs['items'][qid],start=starts[i],arrival=starts[i]+.25,arrival_rank=i) for i,qid in enumerate(ids)]


if __name__=='__main__':
    x=build_inputs();write(OUT/'inputs.json',x);print('Saved',len(x['items']),'original questions',x['sha256'])
