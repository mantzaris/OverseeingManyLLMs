"""Serial bounded calls to the existing GPU server; append-only attempt accounting."""
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'artifacts/decision_dependencies'
MODEL = 'Qwen/Qwen2.5-7B-Instruct'
REVISION = 'a09a35458c702b33eeacc393d103063234e8bc28'

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))

def write_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n')

def http(path, payload=None, timeout=60):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request('http://127.0.0.1:8017' + path, data=data,
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.load(response)

def generate(call_id, messages, seed, max_tokens=768, json_object=False):
    auth = json.loads((ART / 'authorization.json').read_text())
    payload = dict(model=MODEL, messages=messages, temperature=0.3, top_p=1.0,
                   max_tokens=max_tokens, seed=seed)
    if json_object:
        payload['response_format'] = {'type': 'json_object'}
    fingerprint = hashlib.sha256(canonical(payload).encode()).hexdigest()
    target = ART / 'raw' / (call_id + '.json')
    if target.exists():
        saved = json.loads(target.read_text())
        if saved['request_sha256'] != fingerprint:
            raise ValueError('Cache key used for a different request: ' + call_id)
        return saved
    now = datetime.now(timezone.utc)
    if now >= datetime.fromisoformat(auth['inference_cutoff_utc']):
        raise RuntimeError('New inference cutoff reached')
    ledger = ART / 'attempts.jsonl'
    attempts = []
    tokenized = http('/tokenize', dict(model=MODEL, messages=messages,
                                      add_generation_prompt=True))
    input_count = tokenized.get('count', len(tokenized.get('tokens', [])))
    if input_count + max_tokens > 2048:
        saved = dict(call_id=call_id, request=payload, request_sha256=fingerprint,
                     status='context_limit', prompt_tokens=input_count, attempts=[])
        write_json(target, saved)
        return saved
    for index in range(2):
        started = datetime.now(timezone.utc)
        if started >= datetime.fromisoformat(auth['inference_cutoff_utc']):
            break
        used = sum(1 for _ in ledger.open()) if ledger.exists() else 0
        if used >= auth['attempt_ceiling']:
            raise RuntimeError('Session attempt ceiling reached')
        intent = dict(call_id=call_id, attempt=index + 1, request_sha256=fingerprint,
                      started_utc=started.isoformat(), scheduled_attempt=used + 1)
        with ledger.open('a') as f:
            f.write(canonical(intent) + '\n')
        start = time.monotonic()
        try:
            response = http('/v1/chat/completions', payload)
            item = dict(intent, response=response, elapsed_seconds=time.monotonic()-start,
                        status='ok')
        except Exception as error:
            item = dict(intent, error=repr(error), elapsed_seconds=time.monotonic()-start,
                        status='failed')
        attempts.append(item)
        saved = dict(call_id=call_id, request=payload, request_sha256=fingerprint,
                     status=item['status'], prompt_tokens=input_count, attempts=attempts)
        write_json(target, saved)
        if item['status'] == 'ok':
            return saved
    return saved

def parsed(saved):
    if saved['status'] != 'ok':
        return None
    try:
        text = saved['attempts'][-1]['response']['choices'][0]['message']['content'].strip()
        if text.startswith('```'):
            text = text.split('\n', 1)[1].rsplit('```', 1)[0]
        return json.loads(text)
    except (KeyError, IndexError, ValueError):
        return None
