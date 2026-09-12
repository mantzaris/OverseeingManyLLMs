"""Inspection replay UI. No generation and no undisclosed sibling labels."""
import argparse,json,time,threading,uuid
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from datetime import datetime,timezone
from ..common import ART,read,digest,canonical
STATIC=Path(__file__).parent
class Desk:
 def __init__(self,log):self.log=Path(log);self.sessions={};self.lock=threading.Lock()
 def record(self,action,payload,state):
  row=dict(kind='software_demonstration_not_participant_data',utc=datetime.now(timezone.utc).isoformat(),monotonic=time.monotonic(),action=action,payload=payload,display_sha256=digest(state))
  with self.lock:
   self.log.parent.mkdir(parents=True,exist_ok=True)
   with self.log.open('a') as f:f.write(canonical(row)+'\n')
 def cases(self):
  m=read(ART/'frozen/manifest.json');return [dict(id=c['id'],index=i+1,questions=len(c['questions'])) for i,c in enumerate(m['contexts']) if (ART/'evaluation/runs'/(c['id']+'_r0_adaptive_b2.json')).exists()]
 def open(self,cid,method):
  if method not in ['adaptive','fixed_audit','memory','source_rule','individual','individual_risk','reattempt']:raise ValueError('Unknown policy')
  c=next(c for c in read(ART/'frozen/manifest.json')['contexts'] if c['id']==cid);r=read(ART/'evaluation/runs'/(cid+'_r0_'+method+'_b2.json'));sid=str(uuid.uuid4());self.sessions[sid]=dict(context=c,run=r,step=0);state=self.state(sid);self.record('shown_initial',dict(session=sid,context=cid,method=method),state);return state
 def state(self,sid):
  s=self.sessions[sid];c=s['context'];r=s['run'];step=s['step'];event=r['events'][step] if step<len(r['events']) else None
  # No future disclosure, result, private correctness, or recipient list before inspection.
  next_item=None
  if event:
   rank=next(x for x in event['audit_ranking'] if x['id']==event['inspected']);q=next(q for q in c['questions'] if q['id']==event['inspected']);next_item=dict(question=q,reason='Inspect this answer to resolve its uncertainty and obtain an example that may help related answers.',technical=rank)
  return dict(session=sid,context=c,method=r['method'],step=step,budget=r['budget'],remaining=r['budget']-step,answers=r['snapshots'][step],next=next_item,last=r['events'][step-1] if step else None,mode='Saved GPU continuation replay. The inspection reveals a benchmark annotation, not a participant response. Uninspected answer correctness is withheld.')
 def inspect(self,sid):
  s=self.sessions[sid]
  if s['step']>=s['run']['budget']:raise ValueError('Inspection budget exhausted')
  s['step']+=1;state=self.state(sid);self.record('inspect_and_replay_transfer',dict(session=sid,step=s['step']),state);return state
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def send(self,obj,status=200):
  b=json.dumps(obj).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
 def do_GET(self):
  if self.path=='/api/cases':return self.send(self.server.desk.cases())
  if self.path=='/':
   b=(STATIC/'index.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.end_headers();return self.wfile.write(b)
  self.send(dict(error='Not found'),404)
 def do_POST(self):
  try:
   n=int(self.headers.get('Content-Length',0))
   if n>10000:raise ValueError('Oversize request')
   p=json.loads(self.rfile.read(n))
   if self.path=='/api/open':return self.send(self.server.desk.open(p['id'],p['method']))
   if self.path=='/api/inspect':return self.send(self.server.desk.inspect(p['session']))
   if self.path=='/api/event':self.server.desk.record(p['action'],p.get('payload',{}),p.get('display',{}));return self.send(dict(ok=True))
   self.send(dict(error='Not found'),404)
  except (KeyError,ValueError,StopIteration,FileNotFoundError) as e:self.send(dict(error=str(e)),400)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=9034);p.add_argument('--log',default='/tmp/adaptive-correction-desk.jsonl');a=p.parse_args();s=ThreadingHTTPServer(('127.0.0.1',a.port),Handler);s.desk=Desk(a.log);print('http://127.0.0.1:'+str(a.port),flush=True)
 try:s.serve_forever()
 except KeyboardInterrupt:pass
 finally:s.server_close()
