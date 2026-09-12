"""Post-freeze descriptive failure attribution, no method changes or extra inference."""
import collections,json,re
from .common import ART,read,write
from .client import parsed

def diagnose(output=None):
 per_method=collections.defaultdict(collections.Counter);examples=[]
 for path in sorted((ART/'raw').glob('evaluation_frozen*.json')):
  r=read(path);key=r['call_id']
  if '_after_ordinary_' not in key:continue
  method=next((m for m in ['global_packet','shared_state','broadcast','targeted','sparse'] if '_'+m+'_after_' in key),None)
  if method is None:continue
  try:context=json.loads(r['request']['messages'][-1]['content'].split('\n',1)[1])
  except (ValueError,IndexError):continue
  packet=context['packet'];role=packet['responsibility'];proposal=parsed(r);count=per_method[method];count['calls']+=1;count['role_'+role]+=1
  if not isinstance(proposal,dict):count['unparseable_or_transport_failure']+=1;continue
  status=proposal.get('status');count['status_'+str(status)]+=1
  if status=='keep' and context['required_action'].startswith('Create'):
   count['keep_despite_required_repair']+=1
   if len(examples)<12:examples.append(dict(call_id=key,reason='keep_despite_required_repair',public_issues=packet['observable_issues']))
  if status=='replace':
   c=packet['requirements'];expected_unit='items' if c['metric']=='units' else 'micro_GBP'
   if role in ['analysis','appendix']:
    q=proposal.get('query',{})
    if q!={k:v for k,v in c.items() if k!='scope'}:count['query_parameter_mismatch']+=1
   elif role=='chart':
    q=proposal.get('view',{})
    if isinstance(q,dict) and q.get('unit')!=expected_unit:count['wrong_unit']+=1
    if isinstance(q,dict) and q.get('limit')!=c['display_n']:count['wrong_display_count']+=1
   else:
    q=proposal.get('summary',{})
    if isinstance(q,dict) and q.get('unit')!=expected_unit:count['wrong_unit']+=1
  notify=proposal.get('notify',[])
  if isinstance(notify,list):count['invalid_forward_recipients']+=sum(x not in context['forward_only_to'] for x in notify)
 result=dict(methods={k:dict(v) for k,v in per_method.items()},first_examples=examples,classification='Descriptive post-freeze audit of public instructions and generated tool choices. Not an independent set of experiments or a causal proof. Titles/prose are not exhaustively graded.')
 narrative=[]
 for path in sorted((ART/'evaluation/frozen').glob('*.json')):
  if path.name.endswith('summary.json') or path.name.endswith('initial.json'):continue
  r=read(path);a=r.get('artifacts',{}).get('report',{});p=a.get('proposal',{});text=p.get('text','') if isinstance(p,dict) else ''
  if re.search(r'\btop\s+[35]\s+customers?\b',text,re.I):narrative.append(dict(path=str(path.relative_to(ART)),accepted_by_structured_guard=a.get('accepted'),text=text,issue='Narrative calls the ranked stock codes customers'))
 result['post_hoc_narrative_counterexamples']=narrative
 result['narrative_audit_boundary']='After a fixed sweep of all 16 targeted replica-0 reports, a wrong-grouping statement was observed. The transparent top-3/5-customers regex was then applied to all final ordinary-condition reports. This is a post hoc, incomplete prose audit, not a revised primary endpoint.'
 write(output or ART/'analysis/failure_diagnostics.json',result);return result
if __name__=='__main__':print(diagnose())
