"""Secondary source-reading audit using cached SQL with exactly the available intent.

The source-availability condition puts the same human instruction in public input
that the cached answered generation received. This is a prompt-style diagnostic,
not an additional GPU trajectory or a primary frozen policy.
"""
from .common import ART,read,write_json,digest
from .data import public_task,intent_index
from .engine import execute,MachineBudget

def run(repaired=False,output=None):
    root=ART/'repair' if repaired else ART
    if repaired:
        from .repair_data import public_task as task_builder
    else:task_builder=public_task
    rows=[]
    for c in read(root/'private/cases.json')['evaluation']:
        for rep in [0,1]:
            p=root/'prepared'/('repair_'*repaired+'evaluation_v2_'+c['id']+'_r'+str(rep)+'.json')
            if not p.exists():continue
            prep=read(p)
            if 'recovery' not in prep:continue
            task=task_builder(c,rep,True);text=task['sources'][0]['text']
            # Audit that the cache received this same authoritative instruction.
            assert text==c['clarifications'][intent_index(c,rep)]
            sql=(prep.get('answered') or {}).get('sql');result=execute(task['snapshot'],sql,MachineBudget(1),task['contract']['ordered']);target=execute(task['snapshot'],c['refs'][intent_index(c,rep)],MachineBudget(1),task['contract']['ordered'])
            released=result['status']=='ok';correct=released and target['status']=='ok' and result['table_hash']==target['table_hash']
            rows.append(dict(id=c['id'],rep=rep,questions=0,executions=1,correct=int(correct),wrong=int(released and not correct),unfinished=int(not released),source_hash=digest(text),generated_sql=sql,classification='secondary_cached_full_instruction_prompt_diagnostic'))
    write_json(output or root/'analysis/direct_source_reader.json',rows)
    return rows
if __name__=='__main__':
 r=run();print({k:sum(x[k] for x in r) for k in ['questions','correct','wrong','unfinished']})
