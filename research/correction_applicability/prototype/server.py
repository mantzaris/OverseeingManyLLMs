"""Local saved-output inspection desk. No inference or private scoring endpoint."""
import argparse,copy,datetime,json,time,uuid
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from ..common import ART,read,canonical,digest
from ..experiment import METHODS
class Desk:
 def __init__(self,revision='v2',log=None):self.revision=revision;self.log=Path(log) if log else None;self.sessions={};self.contexts=read(ART/'development_manifest.json')['contexts']
 def catalog(self):
  return [dict(index=i,id=c['id'],questions=len(c['questions'])) for i,c in enumerate(self.contexts) if (ART/('development_'+self.revision)/('c%02d_patch.json'%i)).exists()]
 def open(self,index,method):
  if method not in METHODS:raise ValueError('Unknown policy')
  c=self.contexts[index];r=read(ART/('development_'+self.revision)/('c%02d_%s.json'%(index,method)));sid=uuid.uuid4().hex;self.sessions[sid]=dict(c=c,r=r,step=0);return self.record(sid,'open')
 def state(self,sid):
  s=self.sessions[sid];r=s['r'];step=s['step'];c=s['c'];ins=[e for e in r['events'] if e['kind']=='inspection'];last=ins[step-1] if step else None;answers=r['snapshots'][step]
  return dict(session=sid,kind='Replay of recorded model outputs and simulated annotation inspections. No human-study observations.',context_id=c['id'],method=r['method'],step=step,remaining=2-step,source=dict(table=c['table'],paragraphs=c['paragraphs']),questions=c['questions'],answers=answers,next_question=next((q for q in c['questions'] if step<2 and q['id']==r['inspection_ids'][step]),None),last=last)
 def record(self,sid,action):
  state=self.state(sid)
  if self.log:
   self.log.parent.mkdir(parents=True,exist_ok=True)
   with self.log.open('a') as f:f.write(canonical(dict(action=action,session=sid,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),monotonic_seconds=time.monotonic(),displayed_state=state,state_sha256=digest(state),participant=False))+'\n')
  return state
 def inspect(self,sid):
  if self.sessions[sid]['step']>=2:raise ValueError('Inspection budget exhausted')
  self.sessions[sid]['step']+=1;return self.record(sid,'inspect')

def serve(port=9035,revision='v2',log=None):
 desk=Desk(revision,log)
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def send(self,obj,status=200):
   b=json.dumps(obj).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b)
  def do_GET(self):
   if self.path=='/api/catalog':return self.send(desk.catalog())
   if self.path=='/':
    b=Path(__file__).with_name('index.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(b);return
   self.send({'error':'not found'},404)
  def do_POST(self):
   try:
    p=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))));state=desk.open(p['index'],p['method']) if self.path=='/api/open' else desk.inspect(p['session']) if self.path=='/api/inspect' else None
    if state is None:raise ValueError('Unknown action')
    self.send(state)
   except (ValueError,KeyError,IndexError) as e:self.send({'error':str(e)},400)
 ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=9035);p.add_argument('--revision',default='v2');p.add_argument('--log');a=p.parse_args();serve(a.port,a.revision,a.log)
