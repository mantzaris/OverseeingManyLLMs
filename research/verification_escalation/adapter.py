"""Small localhost client for the authored Decision desk demonstration."""
import json,urllib.request
class Client:
 def __init__(self,url='http://127.0.0.1:9032'):self.url=url.rstrip('/')
 def state(self):return json.load(urllib.request.urlopen(self.url+'/api/state'))
 def act(self,**payload):
  r=urllib.request.Request(self.url+'/api/action',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
  return json.load(urllib.request.urlopen(r))
