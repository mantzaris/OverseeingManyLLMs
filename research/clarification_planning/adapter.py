"""Small public agent API client. No model, labels or dataset dependency."""
import json
import urllib.request

class ClarificationDesk:
    def __init__(self,url='http://127.0.0.1:9031'):self.url=url.rstrip('/')
    def state(self):
        with urllib.request.urlopen(self.url+'/api/state',timeout=10) as r:return json.load(r)
    def act(self,action,**payload):
        request=urllib.request.Request(self.url+'/api/action',data=json.dumps(dict(action=action,**payload)).encode(),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(request,timeout=10) as r:return json.load(r)
    def next_question(self):return self.act('next')['question']
    def answer(self,value,only_task=None):return self.act('answer',value=value,only_task=only_task)
    def defer(self):return self.act('defer')
    def work(self):return self.state()['work']
    def revise(self,id,value=None,revoke=False,exceptions=None):return self.act('revise',id=id,value=value,revoke=revoke,exceptions=exceptions)
