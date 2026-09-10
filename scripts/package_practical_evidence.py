#!/usr/bin/env python3
"""Publish replayable evidence with generated credential-like values redacted.

Originals remain on the pod and in a Git-ignored local folder. Public prompt and
auxiliary tool-argument text may be redacted; original payload/response hashes
are retained. Staged transactions, backend states, labels and counts must not change.
"""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.domain import digest
from overseeing.io import write_json,utc_now
root=Path('artifacts/stage5_practical');private=Path('artifacts/stage5_practical_private')
pattern=re.compile(r'("([A-Za-z0-9_]*(?:api_key|api_token|access_token|password|secret)[A-Za-z0-9_]*)"\s*:\s*")([^"\n]*)(?="|$)',re.I)
replacement='[REDACTED_GENERATED_CREDENTIAL_LIKE_TEXT]'
raw_paths=sorted((root/'batches').glob('*/prepared/*/*_raw.jsonl.gz'))
if '--complete' in sys.argv:
    finished=json.loads((root/'batches/evaluation/run_finished.json').read_text())
    assert finished['status']=='completed'
    declared=json.loads((root/'batches/evaluation/declaration.json').read_text())
    actual=sum(len(json.loads(p.read_text())) for p in (root/'batches/evaluation/prepared').glob('*/workflows.json'))
    assert actual==declared['workflow_count']
    inventory=root/'evidence_original_hashes.json'
    if not inventory.exists():
        paths=raw_paths+sorted((root/'batches').glob('*/prepared/*/workflows.json'))
        write_json(inventory,dict(created_utc=utc_now(),scope='Original complete GPU preparation evidence before publication redaction',
            files={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}))
values=set();responses=[]
for path in raw_paths:
    for line in gzip.decompress(path.read_bytes()).splitlines():
        record=json.loads(line)
        if record.get('phase')!='attempt_finished' or 'raw_response' not in record:continue
        body=json.loads(record['raw_response'])
        found=[m for c in body.get('choices',[]) for m in pattern.finditer(c.get('message',{}).get('content') or '')
               if len(m.group(3))>=8 and m.group(3)!=replacement]
        if found:
            values.update(m.group(3) for m in found)
            responses.append(dict(path=str(path.relative_to(root)),call_id=record['session_call_id'],retry=record['retry'],
                fields=dict(Counter(m.group(2) for m in found)),parsed='parsed_call' in record,error=record.get('error')))
values=sorted(values,key=len,reverse=True)
def redact(value):
    if isinstance(value,str):
        for text in values:value=value.replace(text,replacement)
        return value
    if isinstance(value,list):return [redact(v) for v in value]
    if isinstance(value,dict):return {k:redact(v) for k,v in value.items()}
    return value
prepared_paths=sorted((root/'batches').glob('*/prepared/*/workflows.json'))
for path in prepared_paths:
    for workflow in json.loads(path.read_text()):
        assert redact(workflow['proposal'])==workflow['proposal'],'A staged transaction requires a separate publication decision'
        for key in ('counts','initial_state_hash','proposed_state_hash','target_state_hash','initial_error','features','failure'):
            assert redact(workflow[key])==workflow[key],(path,key)
manifest_path=root/'publication_redactions.json'
manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else dict(files=[],model_responses=[])
files=[];request_keys=set();response_keys=set();tool_event_changes=0
for path in raw_paths+prepared_paths:
    original=path.read_bytes()
    if path.suffix=='.gz':
        lines=gzip.decompress(original).splitlines(keepends=True);changed=False
        for index,line in enumerate(lines):
            before=json.loads(line);after=redact(before)
            if before==after:continue
            changed=True;meta=dict(reason='Unsolicited model-generated credential-like text; never used for authentication')
            if before['request']!=after['request']:
                after['original_request_hash']=before.get('original_request_hash',before['request_hash'])
                after['request_hash']=digest(after['request']);request_keys.add((after['session_call_id'],after['retry']))
                meta['public_request_hash']=after['request_hash']
            if before.get('raw_response')!=after.get('raw_response'):
                meta['original_raw_response_sha256']=hashlib.sha256(before['raw_response'].encode()).hexdigest()
                response_keys.add((after['session_call_id'],after['retry']))
            after['public_redaction']=meta
            lines[index]=(json.dumps(after,sort_keys=True,ensure_ascii=False)+'\n').encode()
        public=gzip.compress(b''.join(lines),mtime=0) if changed else original
    else:
        before=json.loads(original);after=redact(before)
        if before==after:continue
        tool_event_changes+=sum(a['events']!=b['events'] for a,b in zip(before,after))
        public=(json.dumps(after,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
    if original==public:continue
    target=private/path.relative_to(root);target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():assert target.read_bytes()==original
    else:target.write_bytes(original)
    target.chmod(0o600)
    for directory in [target.parent,*target.parent.parents]:
        if directory==private.parent:break
        directory.chmod(0o700)
    path.write_bytes(public)
    files.append(dict(path=str(path.relative_to(root)),original_sha256=hashlib.sha256(original).hexdigest(),
        public_sha256=hashlib.sha256(public).hexdigest(),original_pod_path='/workspace/OverseeingManyLLMs-rtx6000-ada-20260910T002404Z/'+str(path)))
for entry in files:
    existing=next((r for r in manifest['files'] if r['path']==entry['path']),None)
    if existing:assert existing['original_sha256']==entry['original_sha256'];existing.update(entry)
    else:manifest['files'].append(entry)
for entry in responses:
    if entry not in manifest['model_responses']:manifest['model_responses'].append(entry)
if values:
    manifest.update(redacted_request_attempts=len(request_keys),redacted_response_attempts=len(response_keys),
        workflows_with_auxiliary_trace_redactions=tool_event_changes)
manifest.update(packaged_utc=utc_now(),policy='Generated credential-like values are redacted from public auxiliary arguments, responses and subsequent prompts. Original live request hashes and raw-response hashes are retained. Original evidence remains on the pod and in Git-ignored artifacts/stage5_practical_private/.',
    staged_transactions_changed=0,backend_states_changed=0,labels_changed=0,token_accounting_changed=0,generations_added=0)
write_json(manifest_path,manifest)
print(json.dumps(manifest,indent=2))
