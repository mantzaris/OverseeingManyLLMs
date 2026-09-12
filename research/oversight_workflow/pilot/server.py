"""Pilot orchestration around the unchanged Desk protocol. No evaluation imports."""
import argparse,json,re,threading,time,uuid
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
from http.server import ThreadingHTTPServer
from research.oversight_workflow.prototype.server import Application,Handler
from research.oversight_workflow.protocol import Desk
from research.oversight_workflow.driver import ReplayDriver
from research.oversight_workflow.data import task
from research.oversight_workflow.common import ART,read,write,digest
from research.adaptive_correction_transfer.answers import calculate
from .materials import PILOT,VERSION
from .adapter import saved_output

def utc():return datetime.now(timezone.utc).isoformat()
def questionnaire(p):
 out={}
 for key,n,lo,hi in [('tlx',6,0,100),('control',3,1,7)]:
  xs=p.get(key,[None]*n)
  if len(xs)!=n:raise ValueError('Wrong questionnaire length')
  if any(x is not None and (isinstance(x,bool) or not isinstance(x,(int,float)) or not lo<=x<=hi) for x in xs):raise ValueError('Questionnaire value outside its scale')
  out[key]=xs
 out['comment']=str(p.get('comment',''))[:3000];out['complete']=all(x is not None for k in ('tlx','control') for x in out[k]);out['recorded_utc']=utc();return out

class Pilot(Application):
 def __init__(self,logdir,kind='investigator_practice',authorization=None):
  super().__init__(logdir);self.manifest=read(PILOT/'manifest.json');self.run=None;self.current=None;self.kind=kind;self.authorization=authorization
  if kind=='participant':
   if not authorization or authorization.get('collection_authorized') is not True or not all(authorization.get(k) for k in ('institutional_determination','consent_version','investigator','collection_authorized','record_reference')):raise ValueError('Participant collection requires an investigator authorization record; no approval is supplied by this repository')
 def journal(self):
  super().journal()
  # Preserve late refused actions and in-flight deliveries in the ended block too.
  if getattr(self,"run",None) and not getattr(self,"current",None) and self.run["sessions"] and self.run["sessions"][-1]["session_id"]==self.session:
   self.run["sessions"][-1].update(events=deepcopy(self.desk.events),state=self.desk.logical())
 def create(self,p):
  with self.lock:
   if self.run and (self.current or self.run['next_block']<4) and not self.run['withdrawn']:raise ValueError('Finish or explicitly withdraw the current run first')
   code=str(p['code']);assignment=int(p['assignment'])
   if not re.fullmatch(r'[A-Za-z0-9_-]{3,24}',code):raise ValueError('Use a pseudonymous code of 3-24 letters, digits, _ or -')
   if not 0<=assignment<len(self.manifest['assignments']):raise ValueError('Unknown assignment')
   self.run=dict(schema='oversight-pilot-export-v1',pilot_version=VERSION,manifest_sha256=self.manifest['manifest_sha256'],run_id=uuid.uuid4().hex,participant_code=code,assignment=assignment,record_kind=self.kind,created_utc=utc(),authorization=self.authorization if self.kind=='participant' else None,next_block=0,sessions=[],technical_events=[],withdrawn=False)
   self.save();return self.status()
 def save(self):
  if not self.run:return
  value=deepcopy(self.run)
  if self.current:
   value['active_session']={**deepcopy(self.current),'events':deepcopy(self.desk.events),'state':self.desk.logical()}
  path=self.logdir/(self.run['run_id']+'.pilot.json');temp=path.with_suffix('.tmp');write(temp,value);temp.replace(path)
 def status(self):
  with self.lock:
   self.ensure_cutoff();self.journal();self.save()
   return dict(kind=self.kind,version=VERSION,assignments=self.manifest['assignments'],run=deepcopy(self.run),current=deepcopy(self.current),elapsed=self.desk.view()['elapsed'] if self.current else None)
 def begin(self,p):
  with self.lock:
   if not self.run or self.current or self.run['withdrawn']:raise ValueError('No ready run, or an active session remains')
   step=self.run['next_block']
   if step>=4:raise ValueError('All blocks completed')
   if self.run['sessions'] and self.run['sessions'][-1].get('questionnaire') is None:raise ValueError('Submit the previous form, even if intentionally incomplete, before continuing')
   self.stop();cond='training' if step==0 else self.manifest['assignments'][self.run['assignment']]['blocks'][step-1]['condition']
   condition='sessions' if cond in ('C','training') else 'queue';self.desk=Desk(condition);self.session=uuid.uuid4().hex;self.journal_count=0;self.mode='pilot';items=[];raws={}
   packet=None
   if cond=='training':
    material=read(PILOT.parent/'study/training.json');cs=[material['context']];qids={q['id'] for q in material['questions']};stage='pilot';duration=self.manifest['training_seconds'];offsets=[0,1.5]
   else:
    packet=self.manifest['assignments'][self.run['assignment']]['blocks'][step-1]['packet'];spec=self.manifest['packets'][packet]
    cs=[next(c for c in self.contexts if c['id']==i) for i in spec['context_ids']];qids=set(spec['source_only_question_ids'] if cond=='S' else spec['question_ids']);stage='primary'
    duration=self.manifest['source_only_seconds'] if cond=='S' else self.manifest['review_seconds'];offsets=self.manifest['source_only_start_offsets'] if cond=='S' else self.manifest['review_start_offsets']
   # Alternate sources without changing within-source question order.
   from itertools import zip_longest
   groups=[]
   for c in cs:
    group=[]
    for q in c['questions']:
     if q['id'] not in qids:continue
     if cond=='S':out=dict(answer=[],scale='',evidence=[],derivation='Source-only task. No model proposal is shown.',issues=[]);raw=None
     else:out,raw=saved_output(c,q,stage)
     t=task(c,q,0);group.append(dict(task=t,output=out));raws[t['id']]=raw
    groups.append(group)
   items=[x for row in zip_longest(*groups) for x in row if x]
   if 'seconds' in p:
    if self.kind!='software_fixture':raise ValueError('Duration override is reserved for explicit software fixtures')
    duration=float(p['seconds']);offsets=[x*duration/(self.manifest['source_only_seconds'] if cond=='S' else self.manifest['training_seconds'] if cond=='training' else self.manifest['review_seconds']) for x in offsets]
   if not 0.2<=duration<=1000:raise ValueError('Invalid duration')
   self.current=dict(session_id=self.session,block_index=step,condition=cond,desk_condition=condition,packet=packet,duration_seconds=duration,start_utc=utc(),question_ids=[x['task']['question_id'] for x in items],source_ids=[c['id'] for c in cs],start_offsets=offsets,raw_proposals=raws,record_kind=self.kind)
   self.study=dict(duration_seconds=duration,packet=packet,status=self.kind);self.driver=ReplayDriver(self.desk,items,generation_delay=.25,start_offsets=offsets).start()
   self.timer=threading.Timer(duration,lambda:self.finish('cutoff'));self.timer.daemon=True;self.timer.start();self.save();return self.status()
 def ensure_cutoff(self):
  if self.current and time.monotonic()-self.desk.started>=self.current['duration_seconds']:self.finish('cutoff')
 def finish(self,reason):
  with self.lock:
   if not self.current:return self.status_no_check()
   self.desk.command('pilot-cutoff','close_session');self.stop()
   row={**deepcopy(self.current),'end_utc':utc(),'end_reason':reason,'events':deepcopy(self.desk.events),'state':self.desk.logical(),'questionnaire':None}
   self.run['sessions'].append(row);self.run['next_block']+=1;self.current=None;self.save();return self.status_no_check()
 def status_no_check(self):return dict(run=deepcopy(self.run),current=deepcopy(self.current),kind=self.kind,version=VERSION)
 def form(self,p):
  with self.lock:
   if self.current or not self.run or not self.run['sessions']:raise ValueError('End a session before submitting its questionnaire')
   self.run['sessions'][-1]['questionnaire']=questionnaire(p);self.save();return self.status()
 def withdraw(self):
  with self.lock:
   if not self.run:raise ValueError('No run')
   self.finish('early_withdrawal');self.run['withdrawn']=True;self.run['withdrawal_utc']=utc();self.save();return self.status()
 def view(self):
  with self.lock:
   self.ensure_cutoff();s=super().view();s['pilot']=deepcopy(self.current)
   if self.current:s['banner']=('Source-only diagnostic. Write answers directly from the original source.' if self.current['condition']=='S' else 'Review each proposed answer against its source. You may correct, reject or defer it.')+' Record type: '+self.kind.replace('_',' ')+'.'
   return s
 def export(self):
  self.status();return read(self.logdir/(self.run['run_id']+'.pilot.json'))

class PilotHandler(Handler):
 def do_GET(self):
  try:
   if self.path=='/':return self.response((PILOT/'setup.html').read_text(),ctype='text/html; charset=utf-8')
   if self.path=='/desk':
    html=(PILOT.parent/'prototype/index.html').read_text().replace('</body>','<script src="/pilot/desk.js"></script></body>');return self.response(html,ctype='text/html; charset=utf-8')
   if self.path=='/pilot/desk.js':return self.response((PILOT/'desk.js').read_text(),ctype='text/javascript')
   if self.path=='/pilot/status':return self.response(self.app.status())
   if self.path=='/pilot/export':return self.response(self.app.export())
   if self.path=='/api/catalog':return self.response([])
   if self.path=='/api/journals':return self.response([])
   if self.path in ('/api/export',):return self.response({'error':'Use the identified pilot export'},400)
   return super().do_GET()
  except Exception as e:return self.response({'error':str(e)},400)
 def do_POST(self):
  if self.path.startswith('/pilot/'):
   try:
    origin=self.headers.get('Origin')
    if origin and origin!='http://'+self.headers.get('Host'):raise ValueError('Cross-origin request refused')
    n=int(self.headers.get('Content-Length',0))
    if n>30000:raise ValueError('Request too large')
    p=json.loads(self.rfile.read(n));action=self.path.split('/')[-1]
    if action=='setup':r=self.app.create(p)
    elif action=='begin':r=self.app.begin(p)
    elif action=='finish':r=self.app.finish('early_finish')
    elif action=='questionnaire':r=self.app.form(p)
    elif action=='withdraw':r=self.app.withdraw()
    elif action=='calculate':
     r=dict(result=calculate(str(p['expression'])));self.app.desk.command('calc:'+uuid.uuid4().hex,'display',dict(action='calculator',view=self.app.desk.state['condition']));self.app.journal()
    elif action=='technical':
     self.app.run['technical_events'].append(dict(at_utc=utc(),session_id=self.app.session,detail=str(p.get('detail',''))[:2000]));self.app.save();r={'ok':True}
    else:raise ValueError('Unknown pilot operation')
    return self.response(r)
   except Exception as e:return self.response({'error':str(e)},400)
  if self.path in ('/api/start','/api/restore'):return self.response({'error':'Use the assigned pilot flow; setup is locked during tasks'},400)
  self.app.ensure_cutoff();super().do_POST()

def main():
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=9042);p.add_argument('--log-dir',default='/tmp/oversight-pilot-practice');p.add_argument('--kind',choices=['investigator_practice','software_fixture','participant'],default='investigator_practice');p.add_argument('--authorization');a=p.parse_args()
 app=Pilot(a.log_dir,a.kind,read(a.authorization) if a.authorization else None);PilotHandler.app=app;server=ThreadingHTTPServer(('127.0.0.1',a.port),PilotHandler)
 print('Pilot http://127.0.0.1:%d (%s)'%(a.port,a.kind),flush=True)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
 finally:app.stop();app.save();server.server_close()
if __name__=='__main__':main()
