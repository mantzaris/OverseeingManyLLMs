#!/usr/bin/env python3
"""Localhost-only Decision desk extension, with inspectable interaction logs."""
import argparse,json,sys,threading
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from research.verification_escalation.desk import Desk
from research.verification_escalation.common import canonical
ROOT=Path(__file__).parent;LOCK=threading.Lock()

def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=9032);p.add_argument('--log',default='/tmp/verification-desk-interactions.jsonl');a=p.parse_args();desk=Desk(a.log)
    class Handler(BaseHTTPRequestHandler):
        def send(self,status,body,kind='application/json'):
            data=body.encode() if isinstance(body,str) else body
            self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
        def do_GET(self):
            with LOCK:
                if self.path=='/api/state':return self.send(200,canonical(desk.state()))
                if self.path=='/api/log':return self.send(200,'\n'.join(canonical(e) for e in desk.events)+'\n','application/x-ndjson')
                names={'/':'index.html','/app.js':'app.js','/style.css':'style.css'}
                name=names.get(self.path)
                if not name:return self.send(404,'Not found','text/plain')
                self.send(200,(ROOT/name).read_bytes(),{'html':'text/html','js':'application/javascript','css':'text/css'}[name.split('.')[-1]])
        def do_POST(self):
            if self.path!='/api/action':return self.send(404,'{}')
            origin=self.headers.get('Origin')
            if origin and origin not in ['http://127.0.0.1:'+str(a.port),'http://localhost:'+str(a.port)]:return self.send(403,'{"error":"Local interface only"}')
            with LOCK:
                try:
                    n=int(self.headers.get('Content-Length','0'))
                    if not 0<n<=65536:raise ValueError('Invalid request length')
                    args=json.loads(self.rfile.read(n));result=desk.act(args);self.send(200,canonical(result))
                except (ValueError,KeyError,TypeError) as e:self.send(400,canonical({'error':str(e)}))
        def log_message(self,*args):pass
    print('Verification desk: http://127.0.0.1:'+str(a.port),flush=True)
    ThreadingHTTPServer(('127.0.0.1',a.port),Handler).serve_forever()
if __name__=='__main__':main()
