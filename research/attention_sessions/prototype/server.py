#!/usr/bin/env python3
"""Local-only demonstration UI. No model calls, arbitrary files, or external writes."""
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import sys,json,argparse,time,hashlib,threading
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from research.attention_sessions.data import load,bundles,workload,settings,response
from research.attention_sessions.controller import Controller
from research.attention_sessions.method import POLICIES,certificate

STATIC=Path(__file__).parent
LOCK=threading.Lock()
class Session:
    def __init__(self,log):
        self.log=Path(log);self.log.parent.mkdir(parents=True,exist_ok=True);self.serial=0;self.reset({})
        self.record('server_initialized',{'action':'server_initialized'})
    def reset(self,args):
        self.cases,self.records,self.estimator=load();self.bundle=int(args.get('bundle',0))
        if not 0<=self.bundle<6:raise ValueError('Bundle out of range')
        self.config=dict(load=args.get('load','high'),setup=1,budget=12,reviewer=args.get('reviewer','ideal'),contexts='related')
        if self.config['load'] not in ('low','high') or self.config['reviewer'] not in ('ideal','model','model_risk'):raise ValueError('Unknown condition')
        p=args.get('policy','guarded')
        if p not in POLICIES:raise ValueError('Unknown policy')
        self.public,self.private=workload(bundles(self.cases)[self.bundle],self.cases,self.records,self.estimator,self.config)
        self.controller=Controller(self.public,settings(self.config),p);self.serial+=1
    def state(self):
        snapshot=self.controller.snapshot()
        if self.controller.session:
            group=[self.controller.requests[k] for k in self.controller.session if self.controller.status[k]=='pending']
            snapshot['information']=dict(snapshot['information'],certificate=certificate(group,self.controller.pending(),self.controller.now,self.controller.context,self.controller.settings,self.controller.settings.budget-self.controller.used,position=self.controller.position))
        return dict(snapshot,bundle=self.bundle,reviewer=self.config['reviewer'],load=self.config['load'],
                    demo=True,participant=False,session_serial=self.serial,policies=POLICIES)
    def record(self,action,payload,ok=True,error=None):
        row=dict(record_type='development_demonstration_not_participant_data',wall_utc=datetime.now(timezone.utc).isoformat(),
                 monotonic_seconds=time.monotonic(),session_serial=self.serial,simulated_tick=self.controller.now,
                 action=action,payload=payload,ok=ok,error=error,public_state_sha256=hashlib.sha256(json.dumps(self.state(),sort_keys=True).encode()).hexdigest())
        with self.log.open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n')
    def action(self,args):
        op=args.get('action');c=self.controller
        if op=='reset':self.reset(args)
        elif op=='start':c.start(args.get('ids'),bool(args.get('override',False)))
        elif op=='decision':
            if not c.session:raise ValueError('Start a review session first')
            if args.get('request_id')!=c.session[0]:raise ValueError('Decision applies only to the current card')
            if args.get('diagnosis') not in ('normal','outdoor_damper','heating_valve','cooling_valve','abstain'):raise ValueError('Select a valid diagnosis or abstention')
            c.complete(args['diagnosis'])
        elif op=='defer':c.defer(args['request_id'],float(args['until']))
        elif op=='end':c.end('User rejected or ended proposed group')
        elif op=='wait':
            if c.session:raise ValueError('End the session before waiting')
            events=[t for r in c.requests.values() for t in (r.arrival,r.deadline) if t>c.now]+[t for t in c.not_before.values() if t>c.now]
            if events:c.advance(min(events))
        elif op=='replay':c.step(lambda key:response(self.private,self.config['reviewer'],key))
        elif op=='policy':
            if args.get('policy') not in POLICIES:raise ValueError('Unknown policy')
            c.end('Policy changed by user');c.policy=args['policy']
        elif op=='interaction':pass
        else:raise ValueError('Unknown action')
        self.record(op,args);return self.state()

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def respond(self,data,status=200,kind='application/json'):
        blob=json.dumps(data).encode() if kind=='application/json' else data
        self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(blob)));self.end_headers();self.wfile.write(blob)
    def do_GET(self):
        with LOCK:
            if self.path=='/api/state':self.respond(self.server.session.state());return
            if self.path=='/api/log':
                p=self.server.session.log;self.respond(p.read_bytes() if p.exists() else b'',kind='application/x-ndjson');return
            paths={'/':('index.html','text/html'),'/app.js':('app.js','text/javascript'),'/style.css':('style.css','text/css')}
            if self.path not in paths:self.respond({'error':'Not found'},404);return
            name,kind=paths[self.path];self.respond((STATIC/name).read_bytes(),kind=kind)
    def do_POST(self):
        with LOCK:
            try:
                if self.path!='/api/action':raise ValueError('Unknown endpoint')
                host=self.headers.get('Host','');origin=self.headers.get('Origin')
                if origin and origin!='http://'+host:raise ValueError('Cross-origin actions are disabled')
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=32768:raise ValueError('Invalid request size')
                args=json.loads(self.rfile.read(size))
                if not isinstance(args,dict):raise ValueError('Expected an action object')
                self.respond(self.server.session.action(args))
            except (ValueError,KeyError,TypeError) as e:
                self.server.session.record('rejected_action',locals().get('args',{}),False,str(e));self.respond({'error':str(e)},400)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=9017);p.add_argument('--log',default='/tmp/attention-session-demo.jsonl');a=p.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',a.port),Handler);server.session=Session(a.log)
    print('Local demonstration: http://127.0.0.1:%d ; log %s'%(a.port,a.log),flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
