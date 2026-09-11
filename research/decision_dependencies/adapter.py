"""Tiny standard-library client for the local decision desk."""
import json
import urllib.request

class DecisionDesk:
    def __init__(self,url='http://127.0.0.1:9027'):self.url=url.rstrip('/')
    def state(self):
        with urllib.request.urlopen(self.url+'/api/state',timeout=5) as r:return json.load(r)
    def action(self,action,**payload):
        body=json.dumps(dict(action=action,**payload)).encode()
        request=urllib.request.Request(self.url+'/api/action',data=body,headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(request,timeout=5) as r:return json.load(r)
    def submit(self,id,agent,text,candidate_scope=None,entity=None,kind='preference'):
        state=self.state()
        return self.action('submit',request=dict(id=id,agent=agent,text=text,project=state['project'],
                                                key=candidate_scope,entity=entity,kind=kind))
    def status(self,id):return next(r for r in self.state()['requests'] if r['id']==id)
    def prepare_available(self):return self.action('prepare')
    def release(self,id):
        state=self.action('release',id=id)
        return state['tasks'][id]['status']
