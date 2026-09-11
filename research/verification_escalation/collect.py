"""Serial paired generation. Unasked response material remains evaluator-only."""
import argparse,time
from .common import ART,read,write_json,digest
from .client import generate,parsed
from .data import public_task,intent_index
SYSTEM='You are a careful SQLite analytics assistant. Use only the supplied request, current source instructions and database. Return JSON. Never invent columns or treat schema facts as a user preference.'
CANDIDATES='Identify plausible meanings, including alternative attachment, quantifier scope or entity meanings if relevant. Return {"candidates":[{"meaning":"concise interpretation","sql":"SELECT ..."}],"source_quote":"exact full source instruction resolving the intent, or empty","unrepresented_possible":false}. Give up to three genuinely different supported interpretations. A single supported interpretation is allowed. Do not ask the user in this response. An explicit source instruction overrides ambiguity in the earlier request. Set unrepresented_possible=true if you suspect a plausible meaning is missing or unsupported; false is not a coverage guarantee.'
AUDIT='Independently read the entire request and database. Check for overlooked meanings, including quantifier scope, modifier attachment and entity interpretation. Return {"candidates":[{"meaning":"interpretation","sql":"SELECT ..."}],"source_quote":"exact full source instruction resolving intent or empty","unrepresented_possible":false}. Include up to three valid alternatives, or one if the supplied instruction resolves the ambiguity. Set unrepresented_possible=true for suspected missing or unsupported alternatives.'
RESOLVED='The user has now clarified the request below. Produce one SQL query implementing this instruction using the supplied database. Return {"sql":"SELECT ..."}. Return {"sql":null} if unsupported.'

def messages(task,prompt,clarification=None):
    content={'request':task['request'],'available_instructions':task['sources'],'database':__import__('json').loads(task['schema']),'output_contract':'A result table on this snapshot, not a reusable program. Preserve duplicates, columns and NULL. Row ordering is not required.'}
    if clarification is not None:content['user_clarification']=clarification
    return [{'role':'system','content':SYSTEM},{'role':'user','content':prompt+'\n'+__import__('json').dumps(content,ensure_ascii=False,separators=(',',':'))}]

def run(split,reps=2):
    if split=='evaluation':
        from .freeze import verify
        verify()
    cases=read(ART/'private'/'cases.json')[split]
    for n,case in enumerate(cases):
        for rep in range(reps):
            task=public_task(case,rep);key=split+'_v2_'+case['id']+'_r'+str(rep);out={'id':case['id'],'rep':rep,'split':split,'calls':{},'public_hash':digest(task)}
            for name,prompt in [('candidates',CANDIDATES),('audit',AUDIT)]:
                saved=generate(key+'_'+name,messages(task,prompt),930000+int(case['id'])*10+rep*2+(name=='audit'),512);out['calls'][name]=parsed(saved)
            # Potential reply cache: not passed to the controller until it spends one answer.
            answer=case['clarifications'][intent_index(case,rep)]
            saved=generate(key+'_answered',messages(task,RESOLVED,answer),940000+int(case['id'])*10+rep,256);out['answered']=parsed(saved)
            # Source recovery diagnostic on first four cases of each 16-case type block.
            if split=='development' or n%16<4:
                recovery=public_task(case,rep,True)
                saved=generate(key+'_recovery',messages(recovery,CANDIDATES),950000+int(case['id'])*10+rep,512);out['recovery']=parsed(saved)
            for obj in list(out['calls'].values())+[out.get('recovery')]:
                if isinstance(obj,dict) and 'source_quote' in obj:obj['source_quote_sha256']=digest(obj.pop('source_quote'))
            write_json(ART/'prepared'/(key+'.json'),out)
            print(key,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('split',choices=['development','evaluation']);p.add_argument('--reps',type=int,default=2);a=p.parse_args();run(a.split,a.reps)
