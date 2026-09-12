"""Pilot-only tolerant display projection. No annotations or scorer imported."""
from copy import deepcopy
import re
from research.oversight_workflow.common import ART,read
from research.oversight_workflow.transport import client
from research.adaptive_correction_transfer.answers import prepare

def normalize(raw,context):
 p=deepcopy(raw);changes=[]
 a=p.get('answer') if isinstance(p,dict) else None
 if isinstance(a,list) and any(isinstance(x,list) for x in a) and all(isinstance(y,(str,int,float)) and not isinstance(y,bool) for x in a for y in (x if isinstance(x,list) else [x])):
  p['answer']=[y for x in a for y in (x if isinstance(x,list) else [x])];changes.append('nested_answer_list_flattened_without_semantic_rewording')
 if isinstance(p,dict) and isinstance(p.get('evidence'),str):
  p['evidence']=re.findall(r'\b(?:T\d+C\d+|P\d+)\b',p['evidence']);changes.append('literal_citation_ids_extracted_from_string')
 out=prepare(p,context)
 return out,changes

def saved_output(c,q,stage='primary'):
 cid=f"{stage}_r0_{q['id']}";raw=client.parsed(read(ART/'raw'/(cid+'.json')))
 output,changes=normalize(raw,c)
 return output,dict(call_id=cid,raw_response=raw,display_transformations=changes)
