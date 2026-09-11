#!/usr/bin/env python3
"""A local decision desk. Uses saved development predictions; never reads labels."""
import argparse
import copy
import hashlib
import json
import sys
import threading
import time
import uuid
from datetime import datetime,timezone
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from research.decision_dependencies.client import ART,canonical
from research.decision_dependencies.records import DecisionController,extracted_records,parsed_queries
from research.decision_dependencies.application import artifact
from research.decision_dependencies.prompts import SLOTS

STATIC=Path(__file__).parent;LOCK=threading.Lock()

class Desk:
    def __init__(self,path):
        self.log=Path(path);self.log.parent.mkdir(parents=True,exist_ok=True)
        self.serial=0;self.instance_id=str(uuid.uuid4());self.shown={};self.reset();self.record('server_started',{})

    def reset(self):
        cases=json.loads((ART/'data/public_projects.json').read_text())
        self.case=next(c for c in cases if c['id']=='MUL0012.json' and c['split']=='development')
        self.prepared=json.loads((ART/'prepared/development_MUL0012_0.json').read_text())
        self.c=DecisionController(self.case['project']);self.stage=0;self.serial+=1;self.deferred=set();self.outputs={};self.overrides_pending=set();self.shown={}
        records,self.rejections=extracted_records(self.prepared['outputs']['extract0'],self.case['stages'][0])
        self.c.publish(records,'Source dialogue prefix')
        # Authored distinct roles consuming saved, fallible request interpretations.
        for agent,truekey,variant in [('Dining shortlist','restaurant.food',0),('Itinerary brief','restaurant.food',1),
                                      ('Accommodation brief','hotel.type',0),('Budget brief','restaurant.pricerange',1)]:
            i=self.case['keys'].index(truekey);q=self.case['queries'][variant][i]
            mapping=parsed_queries(self.prepared['outputs']['parse%d'%variant])
            self.c.submit(dict(id=agent.lower().replace(' ','_'),agent=agent,project=self.c.project,
                               text=q['text'],key=mapping.get(q['id']),kind='preference'))

    def state(self):
        state=self.c.snapshot();requests=[]
        for key,r in self.c.requests.items():
            a=self.c.lookup(r);task=self.c.tasks.get(key,{})
            requests.append(dict(r,answer=a,deferred=key in self.deferred,work_status=task.get('status','not_prepared'),
                                 output=self.outputs.get(key),affected=task.get('affected',[])))
        return dict(state,requests=requests,source_messages=self.case['stages'][self.stage],
                    source_stage=self.stage,rejected_candidates=self.rejections,
                    demonstration=True,participant_data=False,session_serial=self.serial)

    def record(self,kind,args,shown_epoch=None):
        now=time.monotonic();rid=args.get('id');shown=self.shown.get(rid)
        before=self.c.epoch if shown_epoch is None else shown_epoch
        elapsed=now-shown[1] if shown and shown[0]==before else None
        row=dict(record_type='development_demonstration_not_participant_data',session=self.serial,instance_id=self.instance_id,
                 utc=datetime.now(timezone.utc).isoformat(),monotonic_seconds=now,
                 action=kind,payload=args,response_seconds_since_shown=elapsed,
                 context_epoch=self.c.epoch,shown_context_epoch=before,state_sha256=hashlib.sha256(canonical(self.state()).encode()).hexdigest())
        with self.log.open('a') as f:f.write(canonical(row)+'\n')

    def act(self,args):
        before=copy.deepcopy(self.__dict__)
        try:return self._act(args)
        except (ValueError,KeyError,TypeError):
            self.__dict__.clear();self.__dict__.update(before);raise

    def _act(self,args):
        op=args.get('action');c=self.c;shown_epoch=c.epoch
        if op=='reset':self.reset()
        elif op=='submit':
            req=args.get('request',{});c.submit(req)
        elif op=='shown':
            for key in args.get('ids',[]):
                if key not in self.shown or self.shown[key][0]!=c.epoch:self.shown[key]=(c.epoch,time.monotonic())
        elif op=='answer':
            req=c.requests[args['id']]
            key=args.get('key') or req.get('key');value=args.get('value');scope=args.get('scope','request')
            if not isinstance(value,str) or not value.strip() or len(value)>200:raise ValueError('Enter a short, nonempty answer')
            if key not in {d+'.'+s for d in SLOTS for s in SLOTS[d]}:raise ValueError('Choose a supported decision type')
            req['key']=key  # Explicit human correction of the inferred scope for this request.
            # A live override is a new user event, unlike the fixed accurate
            # fallback answers in the saved-output experiment. Invalidate the
            # already prepared output before allowing it to be released again.
            if scope=='project':
                if req.get('kind','preference')!='preference':raise ValueError('Approval applies only to its original request')
                if req.get('entity') in c.records.get(key,{}).get('exceptions',[]):raise ValueError('Answer this exception only, or explicitly revise its scope')
                if key in c.records:
                    previous=c.records[key].get('quote');c.revise(key,value)
                    c.records[key].update(previous_quote=previous,quote=value,turn=None)
                else:
                    records=dict(c.records);d,s=key.split('.')
                    records[key]=dict(key=key,domain=d,slot=s,value=value.lower().strip(),kind='preference',
                                      authority='explicit_user_answer',scope_status='confirmed',quote=value,turn=None)
                    c.publish(records,'User supplied a scoped answer')
            elif scope=='request' and args['id'] in c.tasks:
                c.tasks[args['id']]['status']='needs_revalidation';self.overrides_pending.add(args['id'])
            c.answer(req,value,scope=scope,key=key)
            self.deferred.discard(args['id'])
        elif op=='prepare':
            for key,req in c.requests.items():
                if key in self.deferred:continue
                a=c.lookup(req)
                if a['status']=='available':
                    c.prepare(key,{a['key']:a})
                    self.overrides_pending.discard(key)
                    self.outputs[key]=dict(preference=a['value'],source=a.get('source'),
                        preview=artifact('dining_shortlist' if key=='dining_shortlist' else 'itinerary_brief',
                                         {a['key']:a['value']},self.databases()))
        elif op=='release':
            if args['id'] not in c.tasks:raise ValueError('Prepare the work first')
            if args['id'] in self.overrides_pending:raise ValueError('Re-prepare this draft after changing its answer')
            c.release(args['id'])
        elif op=='source_update':
            if self.stage==1:raise ValueError('The saved source update has already been released')
            self.stage=1
            records,self.rejections=extracted_records(self.prepared['outputs']['extract1'],self.case['stages'][1])
            c.publish(records,'The user changed the dining preference in the source dialogue')
        elif op=='revise':
            c.revise(args['key'],value=args.get('value'),exceptions=args.get('exceptions'),revoke=bool(args.get('revoke',False)))
            if args['key'] in c.records:
                r=c.records[args['key']];r.update(previous_quote=r.get('quote'),quote=r['value'],turn=None)
        elif op=='defer':self.deferred.add(args['id'])
        elif op=='resume':self.deferred.discard(args['id'])
        elif op=='inspect':pass
        else:raise ValueError('Unknown action')
        self.record(op,args,shown_epoch=shown_epoch);return self.state()

    @staticmethod
    def databases():
        return {d:json.loads((ART/('data/%s_db.json'%d)).read_text()) for d in ('hotel','restaurant')}

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def respond(self,payload,status=200,kind='application/json'):
        b=json.dumps(payload).encode() if kind=='application/json' else payload
        self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
    def do_GET(self):
        with LOCK:
            if self.path=='/api/state':self.respond(self.server.desk.state());return
            if self.path=='/api/log':
                p=self.server.desk.log;self.respond(p.read_bytes() if p.exists() else b'',kind='application/x-ndjson');return
            files={'/':('index.html','text/html'),'/app.js':('app.js','text/javascript'),'/style.css':('style.css','text/css')}
            if self.path not in files:self.respond({'error':'Not found'},404);return
            name,kind=files[self.path];self.respond((STATIC/name).read_bytes(),kind=kind)
    def do_POST(self):
        with LOCK:
            try:
                if self.path!='/api/action':raise ValueError('Unknown endpoint')
                host=self.headers.get('Host','');origin=self.headers.get('Origin')
                if origin and origin!='http://'+host:raise ValueError('Cross-origin changes are disabled')
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=32768:raise ValueError('Invalid request size')
                args=json.loads(self.rfile.read(size))
                if not isinstance(args,dict):raise ValueError('Expected an object')
                self.respond(self.server.desk.act(args))
            except (ValueError,KeyError,TypeError) as error:
                self.server.desk.record('rejected_action',dict(error=str(error),request=locals().get('args',{})))
                self.respond(dict(error=str(error)),400)

def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=9027);p.add_argument('--log',default='/tmp/decision-desk-demonstration.jsonl');a=p.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',a.port),Handler);server.desk=Desk(a.log)
    print('Decision desk: http://127.0.0.1:%d (saved-output demonstration)'%a.port,flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()

if __name__=='__main__':main()
