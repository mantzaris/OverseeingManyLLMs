"""Cache shared source extraction, request interpretation and strong text baselines."""
import argparse
import hashlib
import json
from .client import ART, canonical, generate, parsed, write_json
from .prompts import EXTRACT, PARSE, HISTORY, MEMORY, dialogue_text
from .records import extracted_records

def messages(system,payload):
    return [dict(role='system',content=system),dict(role='user',content=payload)]

def case_calls(case,replicate):
    prefix=case['split']+'_'+case['project']+'_'+str(replicate)
    seed=81000+replicate*100000+int(hashlib.sha256(case['id'].encode()).hexdigest()[:6],16)%90000
    cache={};calls=[]
    def call(kind,prompt,offset,limit):
        result=generate(prefix+'_'+kind,prompt,seed+offset,limit,True)
        calls.append(dict(id=result['call_id'],kind=kind,status=result['status'],
                          parsed=parsed(result),request_sha256=result['request_sha256']))
        return parsed(result)
    for stage in range(2):
        cache['extract%d'%stage]=call('extract%d'%stage,
                    messages(EXTRACT,dialogue_text(case['stages'][stage])),stage,768)
    for variant in range(2):
        cache['parse%d'%variant]=call('parse%d'%variant,
                    messages(PARSE,canonical(dict(queries=case['queries'][variant]))),10+variant,384)
    for stage in range(2):
        current,_=extracted_records(cache['extract%d'%stage],case['stages'][stage],False)
        memories=list(current.values())
        for variant in range(2):
            queries=case['queries'][variant]
            cache['history%d_%d'%(stage,variant)]=call('history%d_%d'%(stage,variant),
               messages(HISTORY,dialogue_text(case['stages'][stage])+'\nQUESTIONS\n'+canonical(queries)),20+stage*2+variant,384)
            cache['memory%d_%d'%(stage,variant)]=call('memory%d_%d'%(stage,variant),
               messages(MEMORY,canonical(dict(memories=memories,queries=queries))),30+stage*2+variant,384)
    result=dict(id=case['id'],split=case['split'],replicate=replicate,outputs=cache,calls=calls)
    write_json(ART/'prepared'/(prefix+'.json'),result)
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--split',choices=['development','evaluation'],required=True)
    parser.add_argument('--replicates',type=int,required=True);args=parser.parse_args()
    cases=[x for x in json.loads((ART/'data/public_projects.json').read_text()) if x['split']==args.split]
    if args.split=='evaluation':
        from .freeze import verify_frozen
        verify_frozen()
        declaration=json.loads((ART/'frozen/declaration.json').read_text())
        if declaration['replicates']!=args.replicates or declaration['evaluation_ids']!=[x['id'] for x in cases]:
            raise RuntimeError('Evaluation differs from declaration')
        # The frozen marker is recorded only after its declaration commit exists.
        marker=json.loads((ART/'frozen/commit.json').read_text())
        if not marker.get('commit'):raise RuntimeError('Missing frozen declaration commit')
    for case in cases:
        for replicate in range(args.replicates):
            result=case_calls(case,replicate)
            print(case['id'],replicate,len(result['calls']),sum(x['status']!='ok' for x in result['calls']),flush=True)

if __name__=='__main__':main()
