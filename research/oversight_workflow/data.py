"""Public source projection and pre-generation selection; private scoring is elsewhere."""
import hashlib
from research.adaptive_correction_transfer.data import SOURCE, context, normalized
from research.adaptive_correction_transfer.answers import source_text
from .common import ROOT, ART, digest, read, write

def source(c):
    p={k:c[k] for k in ('id','table','paragraphs')}
    return dict(**p,sha256=digest(p),provenance=dict(dataset='TAT-QA',revision='870accc41953dcde885aabeb963d94aabdc0fbc3',
        split=c['source_split'],index=c['source_index'],origin='Real financial report table and text; benchmark question'))

def task(c,q,replica):
    return dict(id=f"r{replica}/{q['id']}",agent=f"Worker {q['order']%3+1}",question_id=q['id'],
                question=q['question'],source=source(c),dependencies=[])

def select():
    provenance=read(ART/'provenance.json')
    for f in provenance['files']:
        assert hashlib.sha256((SOURCE/f['path']).read_bytes()).hexdigest()==f['sha256']
    old=read(ROOT/'artifacts/correction_applicability/source_pool_audit.json')
    previous=old['used_contexts']
    raw=read(SOURCE/'dataset_raw/tatqa_dataset_test_gold.json')
    selected=[];tables=set();paragraphs=set();selection_log=[]
    for item in old['unused_test_candidates']:
        c=context(raw[item['index']],'test_gold',item['index'])
        th=digest([[normalized(v) for v in row] for row in c['table']])
        ps={normalized(p['text']) for p in c['paragraphs'] if len(normalized(p['text']))>=160}
        reason='duplicate_selected_source' if th in tables or ps&paragraphs else None
        selection_log.append(dict(id=c['id'],source_index=item['index'],exclusion=reason))
        if reason:continue
        assert c['id'] not in previous
        tables.add(th);paragraphs.update(ps);selected.append(c)
        if len(selected)==24:break
    assert len(selected)==24
    write(ART/'selection.json',dict(contexts=selected,questions=sum(len(c['questions']) for c in selected),replicas=2,
        selection_rule='First 24 unused eligible public-test-gold contexts in original source order; exclude normalized table or >=160-character paragraph duplicates with historical or already selected contexts.',
        prior_source_audit_sha256=digest(old),previous_context_ids=sorted(previous),selection_log=selection_log,
        label_policy='This file contains public source and questions only. No annotation, derivation or answer fields projected.',
        independence='24 source contexts, not 24 independently identified reports or companies. Exact duplicate screening cannot establish report independence.'))
    print('Selected',len(selected),'contexts',sum(len(c['questions']) for c in selected),'questions')

if __name__=='__main__': select()
