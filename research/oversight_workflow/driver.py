"""Wall-clock workload delivery. Both adapters call the same request protocol."""
import threading
import time
import uuid
from .common import ART,read,write
from .data import task

class ReplayDriver:
    def __init__(self, desk, items, interval=.15, generation_delay=.04, revision=None):
        self.desk=desk;self.items=items;self.interval=interval;self.delay=generation_delay
        self.revision=revision;self.stop_event=threading.Event();self.thread=None
        self.timings=[];self.errors=[];self.run_id=uuid.uuid4().hex[:10]
    def cmd(self,action,p):
        r=self.desk.command(self.run_id+':'+str(len(self.desk.events))+':'+action,action,p)
        if not r['ok']:self.errors.append(dict(action=action,error=r['error']))
        return r
    def start(self):
        for item in self.items:self.cmd('offer',item['task'])
        self.thread=threading.Thread(target=self.run,name='saved-output-delivery',daemon=True);self.thread.start();return self
    def run(self):
        begin=time.monotonic();next_task=0;inflight=[];revised=False
        while not self.stop_event.is_set():
            now=time.monotonic()-begin
            if next_task<len(self.items) and now>=next_task*self.interval and not self.desk.logical()['paused'] and len(inflight)<3:
                item=self.items[next_task];rid=item['task']['id']
                if self.cmd('admit',{'id':rid})['ok'] and self.cmd('start',{'id':rid})['ok']:
                    inflight.append((now+self.delay,item));next_task+=1
            for due,item in list(inflight):
                if now>=due:
                    self.cmd('receive',dict(id=item['task']['id'],output=item['output'],origin='saved_model_output'))
                    self.timings.append(dict(id=item['task']['id'],eligible_start=(next(i for i,x in enumerate(self.items) if x is item))*self.interval,
                        intended_delivery_after_start=self.delay,delivery_lateness_ms=(now-due)*1000))
                    inflight.remove((due,item))
            if self.revision and not revised and now>=self.revision['at'] and self.revision['id'] in self.desk.logical()['requests']:
                self.cmd('revise',dict(id=self.revision['id'],output=self.revision['output'],origin='saved_model_revision'))
                revised=True
            if next_task==len(self.items) and not inflight and (not self.revision or revised):break
            self.stop_event.wait(.002)
    def stop(self):
        self.stop_event.set()
        if self.thread:self.thread.join(timeout=2)
        if self.thread and self.thread.is_alive():raise RuntimeError('Replay worker did not stop')

class LiveDriver:
    """Independent task-worker prompts; one existing serial GPU server."""
    def __init__(self,desk,contexts,replica=0,stage='primary'):
        self.desk=desk;self.contexts=contexts;self.replica=replica;self.stage=stage
        self.stop_event=threading.Event();self.threads=[];self.jobs=[];self.job_lock=threading.Lock();self.rows=[];self.errors=[]
    def start(self):
        for c in self.contexts:
            for q in c['questions']:
                t=task(c,q,self.replica);self.desk.command('offer:'+t['id'],'offer',t)
                self.jobs.append((c,q,t))
        for i in range(3):
            th=threading.Thread(target=self.worker,name=f'live-task-worker-{i+1}',daemon=True);th.start();self.threads.append(th)
        return self
    def worker(self):
        from .inference import answer
        while not self.stop_event.is_set():
            with self.desk.lock:
                if self.desk.state['paused']:job=None
                else:
                    with self.job_lock:job=self.jobs.pop(0) if self.jobs else None
                    if job:
                        c,q,t=job
                        for action in ('admit','start'):
                            r=self.desk.command(action+':'+t['id'],action,{'id':t['id']})
                            if not r['ok']:raise RuntimeError(r)
            if not job:
                with self.job_lock:
                    if not self.jobs:return
                self.stop_event.wait(.01);continue
            try:row=answer(c,q,self.replica,self.stage);self.rows.append(row);output=row['output']
            except Exception as e:
                self.errors.append(dict(id=t['id'],error=repr(e)));output=dict(answer=[],scale='',issues=['worker_failure'],derivation=str(e))
            self.desk.command('receive:'+t['id'],'receive',dict(id=t['id'],output=output,origin='live_model_output'))
    def done(self):return all(not t.is_alive() for t in self.threads)
    def stop(self):
        self.stop_event.set()
        for t in self.threads:t.join(timeout=65)
        if any(t.is_alive() for t in self.threads):raise RuntimeError('Live worker still finishing a bounded call')

def items_for(contexts,replica=0):
    items=[]
    for c in contexts:
        for q in c['questions']:
            row=read(ART/'prepared'/f"primary_r{replica}_{q['id']}.json")
            items.append(dict(task=task(c,q,replica),output=row['output']))
    return items
