"""Serial GPU-only structured tool-call client with a Stage 5 accounting ledger."""
from datetime import datetime, timedelta, timezone
import fcntl
import json
from pathlib import Path
import time
import urllib.request
import urllib.error

from overseeing.client import GPUClient
from overseeing.domain import digest
from overseeing.io import append_jsonl, utc_now, write_json
from .workflow import ACTION_SCHEMA, SCHEMAS, validate


class RetailLedger:
    def __init__(self,root,context):
        self.root=Path(root);self.context=context
        self.auth=json.loads((self.root/'authorization.json').read_text())
        start=datetime.fromisoformat(self.auth['started_utc']);finish=datetime.fromisoformat(self.auth['deadline_utc'])
        self.deadline=datetime.fromisoformat(self.auth['inference_cutoff_utc'])
        if (self.auth['name']!='stage5_practical' or self.auth['authorization']!='explicit_user_request'
            or self.auth['attempt_limit']!=30000 or finish!=start+timedelta(hours=9)
            or self.deadline!=finish-timedelta(minutes=90) or not start<=datetime.now(timezone.utc)<self.deadline):
            raise RuntimeError('Invalid or expired Stage 5 authorization')
        self.lock=(self.root/'worker.lock').open('a');fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        self.path=self.root/'ledger.jsonl'
        records=[json.loads(s) for s in self.path.read_text().splitlines()] if self.path.exists() else []
        self.calls=sum(r['kind']=='call_reserved' for r in records)
        self.attempts=sum(r['kind']=='attempt_reserved' for r in records)
        self.seen={(r['call_id'],r['retry']) for r in records if r['kind']=='attempt_reserved'}

    def check(self):
        if datetime.now(timezone.utc)>=self.deadline:raise RuntimeError('Stage 5 inference cutoff reached')
        if self.attempts>=30000:raise RuntimeError('Stage 5 30000-attempt ceiling reached')

    def reserve_call(self,metadata,sample=0):
        self.check();self.calls+=1
        append_jsonl(self.path,dict(kind='call_reserved',call_id=self.calls,metadata=metadata,
            sample=sample,context=self.context,wall_utc=utc_now()))
        return self.calls

    def reserve_attempt(self,call_id,retry):
        self.check()
        if retry not in (0,1) or (call_id,retry) in self.seen or not 1<=call_id<=self.calls:
            raise RuntimeError('Invalid retry reservation')
        self.attempts+=1;self.seen.add((call_id,retry))
        append_jsonl(self.path,dict(kind='attempt_reserved',call_id=call_id,retry=retry,
            attempt_id=self.attempts,context=self.context,wall_utc=utc_now()))

    def close(self):
        write_json(self.root/'ledger_state.json',dict(captured_utc=utc_now(),scheduled_calls=self.calls,
            attempts=self.attempts,attempt_limit=30000,inference_cutoff_utc=self.deadline.isoformat()))
        fcntl.flock(self.lock,fcntl.LOCK_UN);self.lock.close()


class RetailClient(GPUClient):
    def _http(self,url,payload):
        # Guided decoding follows schema property order. Sorting keys would put
        # arguments before tool selection, changing the executable interface.
        if not self.config.get('interface_revision'):return super()._http(url,payload)
        remaining=(min(self.deadline,self.attempt_deadline)-datetime.now(timezone.utc)).total_seconds()
        if remaining<=0:raise TimeoutError('Stage deadline reached')
        body=json.dumps(payload,separators=(',',':'),ensure_ascii=False).encode()
        request=urllib.request.Request(url,data=body,headers={'Content-Type':'application/json'})
        try:
            with self.opener.open(request,timeout=min(60,remaining)) as response:
                return response.status,response.read().decode(),response.headers.get('X-Request-Id')
        except urllib.error.HTTPError as exc:
            return exc.code,exc.read().decode(errors='replace'),exc.headers.get('X-Request-Id')

    def generate(self,messages,metadata):
        if self.counts['scheduled_calls']>=self.max_calls:raise RuntimeError('Declared workflow call cap')
        call_id=self.budget.reserve_call(metadata);self.counts['scheduled_calls']+=1
        last_error=None
        for retry in (0,1):
            self.attempt_deadline=min(self.deadline,datetime.now(timezone.utc)+timedelta(seconds=60))
            seed=int(digest(dict(metadata,retry=retry))[:8],16)
            payload=dict(model=self.config['model'],messages=messages,temperature=self.config['temperature'],
                top_p=self.config['top_p'],max_tokens=self.config['max_output_tokens'],seed=seed,
                n=1,guided_json=ACTION_SCHEMA,stream=False)
            record=dict(metadata=metadata,session_call_id=call_id,retry=retry,seed=seed,wall_utc=utc_now(),
                request=payload,request_hash=digest(payload),inference_request_attempted=False,
                evidence='live_gpu',attempt_deadline_utc=self.attempt_deadline.isoformat())
            if self.config.get('interface_revision'):
                record['serialized_request']=json.dumps(payload,separators=(',',':'),ensure_ascii=False)
            append_jsonl(self.raw_path,dict(record,phase='attempt_started'))
            start=time.monotonic();inference_start=None
            try:
                status,body,_=self._http(self.base_url[:-3]+'/tokenize',dict(model=self.config['model'],messages=messages))
                if status!=200:raise ValueError('Tokenization HTTP '+str(status))
                count=json.loads(body)['count'];record['input_tokens']=count
                if not 0<count<=self.config['max_input_tokens']:raise ValueError('Declared context exceeded: '+str(count))
                self.budget.reserve_attempt(call_id,retry);self.counts['attempts']+=1
                record['inference_request_attempted']=True
                append_jsonl(self.raw_path,dict(record,phase='inference_started'))
                inference_start=time.monotonic()
                status,body,request_id=self._http(self.base_url+'/chat/completions',payload)
                record.update(http_status=status,raw_response=body,request_id=request_id)
                if status!=200:raise ValueError('Generation HTTP '+str(status))
                response=json.loads(body);choice=response['choices'][0]
                if choice['finish_reason']!='stop':raise ValueError('Truncated generation: '+str(choice['finish_reason']))
                parsed=json.loads(choice['message']['content'])
                if set(parsed)!={'tool','arguments','confidence'} or parsed['tool'] not in SCHEMAS or parsed['confidence'] not in ('low','medium','high'):
                    raise ValueError('Invalid tool call envelope')
                validate(SCHEMAS[parsed['tool']],parsed['arguments']);record['parsed_call']=parsed
            except Exception as exc:
                last_error=type(exc).__name__+': '+str(exc);record['error']=last_error
            finally:
                if inference_start is not None:
                    elapsed=time.monotonic()-inference_start;record['inference_wall_seconds']=elapsed
                    self.counts['request_wall_seconds']+=elapsed
                    try:
                        usage=json.loads(record.get('raw_response','{}'))['usage'];record['usage']=usage
                        for name in ('prompt_tokens','completion_tokens'):self.counts[name]+=usage[name]
                    except (KeyError,ValueError,TypeError):self.counts['unknown_token_attempts']+=1;record['usage']=None
                record['attempt_wall_seconds']=time.monotonic()-start
                append_jsonl(self.raw_path,dict(record,phase='attempt_finished'))
            if 'parsed_call' in record:return record['parsed_call']
            self.budget.check()
        raise RuntimeError(last_error)
