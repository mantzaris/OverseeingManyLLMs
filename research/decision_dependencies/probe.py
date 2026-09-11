"""Declared development probes. Source labels are never passed into prompts."""
import argparse
import json
from pathlib import Path
from .client import ART, generate, parsed, write_json
from .prompts import extraction_messages

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);a=p.parse_args()
    data=json.load((Path(a.source)/'data.json').open())
    # Deterministic first development examples with ordinary scope and actual revisions.
    cases=[('MUL0012.json',9),('MUL0012.json',17),('MUL0095.json',13),
           ('MUL0095.json',23),('MUL0013.json',999),('MUL0016.json',999)]
    declaration={'probe':'A: source extraction and scope, two seeds per snapshot',
                 'cases':cases,'seeds':[80401,80402],'calls':12,
                 'selection':'Development dialogue IDs inspected for source feasibility; no outcomes used.'}
    path=ART/'development/probe_declaration.json'
    if path.exists() and json.loads(path.read_text()) != json.loads(json.dumps(declaration)):
        raise ValueError('Existing declaration differs')
    write_json(path,declaration)
    rows=[]
    for n,(key,stop) in enumerate(cases):
        messages=[{'turn':i,'role':'user' if i%2==0 else 'assistant','text':x['text']}
                  for i,x in enumerate(data[key]['log']) if i<=stop]
        for rep,seed in enumerate(declaration['seeds']):
            saved=generate('probe_%02d_%d'%(n,rep),extraction_messages(messages),seed,768)
            row=dict(dialogue=key,stop=stop,replicate=rep,status=saved['status'],
                     parsed=parsed(saved),attempts=len(saved['attempts']),
                     seconds=sum(x['elapsed_seconds'] for x in saved['attempts']))
            rows.append(row);write_json(ART/'development/probe_results.json',rows)
            print(key,stop,rep,saved['status'],round(row['seconds'],2),flush=True)

if __name__=='__main__':main()
