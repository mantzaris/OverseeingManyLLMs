"""Bounded serial GPU transport with a separate authorization and cache."""
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from .common import ART, canonical, write_json, read
MODEL='Qwen/Qwen2.5-7B-Instruct'
REVISION='a09a35458c702b33eeacc393d103063234e8bc28'

def http(path,payload=None,timeout=60):
    req=urllib.request.Request('http://127.0.0.1:8019'+path,
        data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=timeout) as r:return json.load(r)

def parsed(saved):
    try:
        if saved['status']!='ok':return None
        s=saved['attempts'][-1]['response']['choices'][0]['message']['content'].strip()
        if s.startswith('```'):s=s.split('\n',1)[1].rsplit('```',1)[0]
        return json.loads(s)
    except (KeyError,IndexError,ValueError,TypeError):return None

def generate(call_id,messages,seed,max_tokens):
    payload=dict(model=MODEL,messages=messages,temperature=.3,top_p=1.,max_tokens=max_tokens,
                 seed=seed,response_format={'type':'json_object'})
    fingerprint=hashlib.sha256(canonical(payload).encode()).hexdigest()
    target=ART/'raw'/(call_id+'.json');auth=read(ART/'authorization.json')
    if target.exists():
        saved=read(target)
        if saved['request_sha256']!=fingerprint:raise ValueError('Changed cached request '+call_id)
        return saved
    if datetime.now(timezone.utc)>=datetime.fromisoformat(auth['inference_cutoff_utc']):raise RuntimeError('Inference cutoff')
    if len(list((ART/'raw').glob('*.json')))>=auth['scheduled_call_ceiling']:raise RuntimeError('Scheduled ceiling')
    saved=dict(call_id=call_id,request=payload,request_sha256=fingerprint,status='pending',attempts=[])
    # Record the scheduled request before any networking, including tokenize failures.
    write_json(target,saved)
    try:
        tokens=http('/tokenize',dict(model=MODEL,messages=messages,add_generation_prompt=True))
        saved['input_tokens']=tokens.get('count',len(tokens.get('tokens',[])))
    except Exception as e:
        saved.update(status='tokenize_failed',error=repr(e));write_json(target,saved);return saved
    if saved['input_tokens']+max_tokens>2048:
        saved['status']='context_limit';write_json(target,saved);return saved
    ledger=ART/'attempts.jsonl'
    for i in range(2):
        now=datetime.now(timezone.utc)
        used=len(ledger.read_text().splitlines()) if ledger.exists() else 0
        if now>=datetime.fromisoformat(auth['inference_cutoff_utc']) or used>=auth['attempt_ceiling']:
            saved['status']='bounded_incomplete';write_json(target,saved);return saved
        intent=dict(call_id=call_id,attempt=i+1,started_utc=now.isoformat(),request_sha256=fingerprint)
        with ledger.open('a') as f:f.write(canonical(intent)+'\n')
        start=time.monotonic()
        try:item=dict(intent,status='ok',response=http('/v1/chat/completions',payload))
        except Exception as e:item=dict(intent,status='failed',error=repr(e))
        item['elapsed_seconds']=time.monotonic()-start;saved['attempts'].append(item)
        saved['status']=item['status'];write_json(target,saved)
        if item['status']=='ok':break
    return saved
