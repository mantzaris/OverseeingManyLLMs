from .client import generate,parsed
from .answers import prepare,messages
from .common import digest

def request(call_id,c,q,seed,current=None,corrections=None,reattempt=False):
 prompt=messages(c,q,current,corrections,reattempt);raw=generate(call_id,prompt,seed,288);a=prepare(parsed(raw),c)
 usage=dict(call_id=call_id,request_sha256=raw['request_sha256'],status=raw['status'],attempts=len(raw['attempts']),tokens=sum(x.get('response',{}).get('usage',{}).get('total_tokens',0) for x in raw['attempts']),seconds=sum(x.get('elapsed_seconds',0) for x in raw['attempts']))
 return a,usage
