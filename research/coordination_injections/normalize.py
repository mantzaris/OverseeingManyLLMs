"""Accept explicit equivalent tool envelopes, never infer missing task parameters."""
import copy
TOOLS={'analysis':'aggregate','appendix':'aggregate','chart':'bar_chart','report':'summarize'}
FIELDS={'analysis':('query',['start','end','country','inclusion','customer','metric']),'appendix':('query',['start','end','country','inclusion','customer','metric']),'chart':('view',['source','limit','unit']),'report':('summary',['source','unit'])}
def normalize(proposal,role):
 if not isinstance(proposal,dict) or 'status' in proposal:return copy.deepcopy(proposal)
 if proposal.get('tool')!=TOOLS[role] or not isinstance(proposal.get('params'),dict):return copy.deepcopy(proposal)
 params=proposal['params'];name,fields=FIELDS[role];nested=params.get(name)
 if nested is None:
  if any(k not in params for k in fields):return copy.deepcopy(proposal)
  selected={k:params[k] for k in fields}
 else:
  if not isinstance(nested,dict) or any(k not in nested for k in fields):return copy.deepcopy(proposal)
  if any(k in params and params[k]!=nested[k] for k in fields):return copy.deepcopy(proposal)
  selected=copy.deepcopy(nested)
 status=params.get('status','replace')
 if status!='replace':return copy.deepcopy(proposal)
 out=dict(status='replace',**{name:selected})
 for k in ['notify','title','text','plan']:
  if k in params:out[k]=copy.deepcopy(params[k])
  elif k in proposal:out[k]=copy.deepcopy(proposal[k])
 if 'notify' not in out:out['notify']=[]
 return out
