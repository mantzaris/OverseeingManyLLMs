"""Local Decision desk extension: inspect saved GPU adaptation or try a deterministic change."""
import argparse,json,time,copy,threading
from datetime import datetime,timezone
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from research.coordination_injections.common import ART,read,canonical,digest
from research.coordination_injections.contracts import contract,ROLES,affected
from research.coordination_injections.pipeline import pipeline
from research.coordination_injections.api import validate_project
STATIC=Path(__file__).parent
class Desk:
 def __init__(self,log):self.log=Path(log);self.log.parent.mkdir(parents=True,exist_ok=True);self.lock=threading.Lock();self.last=time.monotonic();self.events=[]
 def record(self,action,payload,state=None):
  now=time.monotonic();row=dict(type='local_software_demonstration_not_participant_data',utc=datetime.now(timezone.utc).isoformat(),action=action,payload=payload,seconds_since_previous_event=now-self.last,displayed_state_sha256=digest(state) if state else None);self.last=now
  with self.lock:
   self.events.append(row)
   with self.log.open('a') as f:f.write(canonical(row)+'\n')
 def cases(self):
  m=read(ART/'frozen/manifest.json');root=ART/'evaluation/frozen'
  return [dict(id=p['id'],month=p['month'],change=p['change'],instruction=p['user_change']['text']) for p in m['evaluation'] if (root/(p['id']+'_r0_targeted.json')).exists()]
 def state(self,pid,method,study="primary"):
  if method not in ['targeted','shared_state','broadcast','sparse','pipeline','global_packet']:raise ValueError('Unknown method')
  p=next(p for p in read(ART/'frozen/manifest.json')['evaluation'] if p['id']==pid);root=ART/'evaluation/frozen';initial=read(root/(pid+'_r0_initial.json'));result_path=root/(pid+'_r0_'+method+'.json')
  if method=='global_packet':result_path=root/'secondary'/(pid+'_r0_global_packet_ordinary.json')
  if study=='parser_followup' and method!='pipeline':result_path=ART/'parser_followup/runs'/(pid+'_r0_'+method+'.json')
  if study not in ['primary','parser_followup']:raise ValueError('Unknown study')
  result=read(result_path)
  # These are public execution checks, not evaluator reference labels.
  return dict(project=p,before=initial,after=result,affected=affected(p),scope='Main report only. The appendix retains its original requirements.',evidence='Recorded UCI Online Retail transactions. Authored brief and change. Saved GPU tool calls; simulated delivery rounds. Acceptance reports public checks, not a human review.',model='Qwen2.5-7B-Instruct, BF16',mode='saved_gpu_replay',study=study)
 def custom(self,payload):
  base=self.state(payload['id'],'targeted');p=copy.deepcopy(base['project']);fields=payload['fields']
  allowed={'country','metric','inclusion','customer'}
  if set(fields)-allowed:raise ValueError('Only supported main-scope fields may change')
  if fields.get('metric','units') not in ['units','value_micro'] or fields.get('inclusion','positive') not in ['positive','signed'] or fields.get('customer','all') not in ['all','known']:raise ValueError('Unsupported option')
  if fields.get('country','ALL') not in ['ALL','France','Germany','United Kingdom']:raise ValueError('Unsupported country')
  p['after']=copy.deepcopy(p['before']);p['after']['main'].update(fields);p['user_change']=dict(source='authorized_local_user',version=2,scope='main',exceptions=['appendix'],text='Apply these main-report selections: '+canonical(fields)+'. Preserve the original appendix.')
  validate_project(p);out=pipeline(p,0,base['before']['artifacts']);return dict(base,project=p,after=out,affected=affected(p),mode='deterministic_parameterized_demo',evidence='A new local change executed by the deterministic comparator. No model generation or participant evidence. Recorded transaction data; appendix preserved.')
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def send_json(self,obj,status=200):
  b=json.dumps(obj).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
 def do_GET(self):
  if self.path=='/api/cases':return self.send_json(self.server.desk.cases())
  if self.path=='/api/log':return self.send_json(self.server.desk.events)
  if self.path in ['/','/index.html']:
   b=(STATIC/'index.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html');self.send_header('Content-Length',str(len(b)));self.end_headers();return self.wfile.write(b)
  self.send_json(dict(error='Not found'),404)
 def do_POST(self):
  try:
   length=int(self.headers.get('Content-Length','0'))
   if length>20000:raise ValueError('Request too large')
   payload=json.loads(self.rfile.read(length));desk=self.server.desk
   if self.path=='/api/load':state=desk.state(payload['id'],payload['method'],payload.get('study','primary'));desk.record('shown_project',payload,state);return self.send_json(state)
   if self.path=='/api/custom':state=desk.custom(payload);desk.record('user_change_once',payload,state);return self.send_json(state)
   if self.path=='/api/event':desk.record(payload['action'],payload.get('payload',{}));return self.send_json(dict(ok=True))
   self.send_json(dict(error='Not found'),404)
  except (ValueError,KeyError,StopIteration,FileNotFoundError) as e:self.send_json(dict(error=str(e)),400)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=9033);p.add_argument('--log',default='/tmp/coordination-desk-events.jsonl');a=p.parse_args();s=ThreadingHTTPServer(('127.0.0.1',a.port),Handler);s.desk=Desk(a.log);print('Decision desk at http://127.0.0.1:'+str(a.port),flush=True)
 try:s.serve_forever()
 except KeyboardInterrupt:pass
 finally:s.server_close()
