"""AMBROSIA adapter. Source annotations stay in evaluator records, not public tasks."""
import ast,csv,json,sqlite3,hashlib
from pathlib import Path
from collections import defaultdict
from .common import ART,write_json,digest
SOURCE=Path('/tmp/verification-sources/ambrosia/data/ambrosia.csv')

def compact(dump):
    c=sqlite3.connect(':memory:');c.executescript(dump);tables=[]
    for (name,) in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"):
        q='"'+name.replace('"','""')+'"';cols=list(c.execute('PRAGMA table_info('+q+')'))
        tables.append({'table':name,'columns':[[x[1],x[2]] for x in cols], 'foreign_keys':list(c.execute('PRAGMA foreign_key_list('+q+')')),'rows':list(c.execute('SELECT * FROM '+q))})
    try:fk=list(c.execute('PRAGMA foreign_key_check'))
    except sqlite3.Error as e:fk=[['schema_error',str(e)]]
    c.close()
    return json.dumps(tables,separators=(',',':')),fk

def load():return list(csv.DictReader(SOURCE.open()))

def select():
    rows=load();by=defaultdict(list)
    for r in rows:by[(r['db_file'],r['ambig_question'])].append(r)
    chosen=[];excluded=[];seen=set()
    # Source order, one question per database, no outcome-based selection.
    for (db,q),group in by.items():
        if db in seen:continue
        amb=next((r for r in group if r['question_type']=='ambig'),None)
        if not amb:continue
        refs=ast.literal_eval(amb['ambig_queries']);clear=[]
        for sql in refs:
            match=next((r for r in group if r['question_type']=='unambig' and ''.join(r['gold_queries'].split()).lower()==''.join(sql.split()).lower()),None)
            clear.append(match['question'] if match else None)
        schema,fk=compact(amb['db_dump'])
        reason=None
        if not all(clear):reason='missing_matching_human_interpretation'
        elif len(refs)>3:reason='more_than_three_alternatives'
        elif len(schema)>4900:reason='public_context_character_cap'
        if reason:excluded.append(dict(id=amb[''],db=db,reason=reason));continue
        seen.add(db)
        chosen.append(dict(id=amb[''],db=db,domain=amb['domain'],kind=amb['ambig_type'],split=amb['split'],question=q,schema=schema,snapshot=amb['db_dump'],refs=refs,clarifications=clear,foreign_key_violations=fk))
    dev=[];evaluation=[]
    for kind in ['attachment','scope','vague']:
        group=[x for x in chosen if x['kind']==kind]
        local=[x for x in group if x['split']=='few_shot_examples'][:3]
        for x in group:
            if len(local)>=3:break
            if x not in local:local.append(x)
        dev.extend(local)
        evaluation.extend([x for x in group if x not in local and x['split']=='test'][:16])
    for x in evaluation:
        offset=int(digest({'id':x['id'],'intent_seed':8301})[:8],16)%len(x['refs'])
        x['intent_indices']=[offset,(offset+1)%len(x['refs'])]
    write_json(ART/'private'/'cases.json',dict(development=dev,evaluation=evaluation))
    public=lambda x:{k:x[k] for k in ['id','db','domain','kind','split']}
    write_json(ART/'split_manifest.json',dict(development=[public(x) for x in dev],evaluation=[public(x) for x in evaluation],exclusions=excluded,eligible_databases=len(chosen),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),rule='Source CSV order; first eligible ambiguous question per database. Three development databases and first 16 remaining test databases per ambiguity type. No outcomes used.',foreign_key_defect_counts={x['id']:len(x['foreign_key_violations']) for x in dev+evaluation}))
    return dev,evaluation

def intent_index(case,rep):return case.get('intent_indices',[0,1])[rep]%len(case['refs'])

def public_task(case,rep,recovery=False):
    task=dict(id=case['id'],request=case['question'],schema=case['schema'],snapshot=case['snapshot'],scope='query/'+case['id'],version=1,exceptions=[],contract={'kind':'snapshot_table','ordered':False,'empty_acceptable':True},sources=[])
    if recovery:task['sources']=[{'id':'S1','text':case['clarifications'][intent_index(case,rep)],'scope':task['scope'],'status':'explicit_user_requirement','version':1}]
    return task

if __name__=='__main__':
    a,b=select();print('Selected',len(a),len(b));print([(x['id'],x['kind'],len(x['schema'])) for x in a])
