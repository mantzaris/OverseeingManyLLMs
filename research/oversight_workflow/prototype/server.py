"""Local research desk. No benchmark annotations are loaded by this server."""
import argparse
from copy import deepcopy
import json
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs
from research.oversight_workflow.common import ART,read,write,digest
from research.oversight_workflow.protocol import Desk,replay
from research.oversight_workflow.data import task
from research.oversight_workflow.driver import ReplayDriver,LiveDriver,ordered_items

class Application:
    def __init__(self,logdir=None):
        self.lock=threading.RLock();self.desk=Desk();self.driver=None;self.mode='Not started'
        self.logdir=Path(logdir or '/tmp/oversight-workflow-interactions');self.logdir.mkdir(parents=True,exist_ok=True)
        self.session=uuid.uuid4().hex;self.journal_count=0;self.timer=None;self.study=None
        self.contexts=read(ART/'frozen/manifest.json')['contexts']
    def journal(self):
        # Append each accepted or refused command once, before HTTP acknowledgement.
        # This is not claimed as an fsync-backed crash-atomic database.
        with self.lock,self.desk.lock:
            new=self.desk.events[self.journal_count:]
            if new:
                with (self.logdir/(self.session+'.jsonl')).open('a') as f:
                    for e in new:f.write(json.dumps({**e,'condition':self.desk.state['condition']},ensure_ascii=False)+'\n')
                self.journal_count=len(self.desk.events)
    def stop(self):
        if self.timer:self.timer.cancel();self.timer=None
        if self.driver:self.driver.stop();self.driver=None
        self.journal()
    def start(self,p):
        with self.lock:
            self.stop();self.desk=Desk(p.get('condition','sessions'));self.session=uuid.uuid4().hex;self.journal_count=0;self.study=None
            if 'study_packet' in p:
                packets=read(Path(__file__).parents[1]/'study/packets.json')['packets']
                ids=packets[int(p['study_packet'])]['context_ids']
                pair=[c for c in self.contexts if c['id'] in ids]
            else:
                pair=self.contexts[p.get('bundle',0)*2:p.get('bundle',0)*2+2]
                if len(pair)!=2:raise ValueError('Unknown source packet')
            mode=p.get('mode','replay');self.mode=mode
            if mode=='replay':
                items=ordered_items(pair,p.get('replica',0))
                first=pair[0]['questions'][0];path=ART/'prepared'/f"revision_r0_{first['id']}.json"
                revision=None
                if p.get('revision',True) and p.get('replica',0)==0 and path.exists():
                    revision=dict(id=items[0]['task']['id'],at=float(p.get('revision_at',18)),output=read(path)['output'])
                offsets=None
                if 'study_packet' in p:
                    duration=float(p.get('study_seconds',720));load=p.get('load','lower')
                    if not 1<=duration<=3600:raise ValueError('Study session length must be 1-3600 seconds')
                    n=len(items)
                    offsets=[i*duration*.94/max(1,n-1) for i in range(n)] if load=='lower' else [(i//13)*(duration/3)+(i%13)*duration/720 for i in range(n)]
                    self.study=dict(packet=p['study_packet'],load=load,duration_seconds=duration,started_utc=datetime.now(timezone.utc).isoformat(),start_offsets=offsets,status='Prospective study preview; no participant identity or data asserted')
                    write(self.logdir/(self.session+'.meta.json'),self.study)
                    current=self.desk
                    self.timer=threading.Timer(duration,lambda:current.command('study-cutoff','close_session'))
                    self.timer.daemon=True;self.timer.start()
                self.driver=ReplayDriver(self.desk,items,interval=float(p.get('interval',1.5)),generation_delay=.25,revision=revision,start_offsets=offsets).start()
            elif mode=='training':
                material=read(Path(__file__).parents[1]/'study/training.json');c=material['context']
                items=[dict(task=task(c,q,0),output=read(ART/'prepared'/f"pilot_r0_{q['id']}.json")['output']) for q in material['questions']]
                revision=dict(id=items[0]['task']['id'],at=float(p.get('revision_at',18)),output=items[0]['output'],origin='training_same_answer_new_version_fixture') if p.get('revision',True) else None
                self.driver=ReplayDriver(self.desk,items,interval=1.5,generation_delay=.25,revision=revision).start()
            elif mode=='live':
                # Uses the existing stage ceiling/cutoff. Restarting is cached only
                # for identical stage-specific request IDs and complete prompts.
                self.driver=LiveDriver(self.desk,pair,p.get('replica',0),'desk_live').start()
            elif mode=='manual':self.driver=None
            else:raise ValueError('Unknown mode')
            self.journal();return self.view()
    def view(self):
        with self.lock:
            self.journal();s=self.desk.view();s.update(session_id=self.session,mode=self.mode,study=self.study,next_request=self.desk.next_request(),
                banner='Replay of actual model answers; arrival timing is constructed. No participant observations.' if self.mode=='replay' else 'Live task workers using the shared pinned GPU model.' if self.mode=='live' else 'Practice with previously inspected development material. The new-version event is an authored training fixture; no participant observations.' if self.mode=='training' else 'Manual protocol session.')
            return s
    def restore(self,name):
        with self.lock:
            # Read only journals within the configured log directory, never arbitrary paths.
            if Path(name).name!=name:raise ValueError('Invalid journal name')
            rows=[json.loads(x) for x in (self.logdir/name).read_text().splitlines()]
            self.stop();self.desk=replay(rows,rows[0]['condition'] if rows else 'sessions');self.session=uuid.uuid4().hex;self.journal_count=0;self.mode='restored';self.study=None
            if rows:
                gap=max(0,(datetime.now(timezone.utc)-datetime.fromisoformat(rows[-1]['utc'])).total_seconds())
                self.desk.started=time.monotonic()-rows[-1]['at']-gap
            self.journal();return self.view()

class Handler(BaseHTTPRequestHandler):
    app=None
    def log_message(self,*a):pass
    def response(self,data,status=200,ctype='application/json'):
        b=data.encode() if isinstance(data,str) else json.dumps(data,ensure_ascii=False).encode()
        self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(b)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(b)
    def do_GET(self):
        try:
            path=urlparse(self.path).path
            if path=='/':return self.response((Path(__file__).parent/'index.html').read_text(),ctype='text/html; charset=utf-8')
            if path=='/api/state':return self.response(self.app.view())
            if path=='/api/catalog':return self.response([dict(bundle=i,contexts=[c['id'] for c in self.app.contexts[2*i:2*i+2]],questions=sum(len(c['questions']) for c in self.app.contexts[2*i:2*i+2])) for i in range(12)])
            if path=='/api/export':
                with self.app.lock,self.app.desk.lock:
                    snapshot=dict(condition=self.app.desk.state['condition'],events=deepcopy(self.app.desk.events),state=self.app.desk.logical())
                return self.response(snapshot)
            if path=='/api/journals':return self.response([p.name for p in sorted(self.app.logdir.glob('*.jsonl'))])
            self.response({'error':'Not found'},404)
        except Exception as e:self.response({'error':str(e)},400)
    def do_POST(self):
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n>250000:raise ValueError('Request too large')
            p=json.loads(self.rfile.read(n));path=urlparse(self.path).path
            # Local same-origin UI. An optional Origin from another site is refused.
            origin=self.headers.get('Origin')
            if origin and origin!=f'http://{self.headers.get("Host")}':raise ValueError('Cross-origin command refused')
            if path=='/api/start':return self.response(self.app.start(p))
            if path=='/api/restore':return self.response(self.app.restore(p['name']))
            if path=='/api/command':
                with self.app.lock:
                    if p.get('session_id')!=self.app.session:raise ValueError('Session changed; reload before acting')
                    r=self.app.desk.command(p['event_id'],p['action'],p.get('payload',{}));self.app.journal()
                return self.response(dict(receipt=r,state=self.app.view()),200 if r['ok'] else 409)
            self.response({'error':'Not found'},404)
        except Exception as e:self.response({'error':str(e)},400)

def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=9041);p.add_argument('--log-dir');a=p.parse_args()
    app=Application(a.log_dir);Handler.app=app;server=ThreadingHTTPServer(('127.0.0.1',a.port),Handler)
    print(f'Review desk http://127.0.0.1:{a.port}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:app.stop();server.server_close()

if __name__=='__main__':main()
