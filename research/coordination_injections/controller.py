"""Registered-scope adaptation with public execution feedback and bounded routing."""
import copy,time
from .common import digest,stable
from .contracts import ROLES,DEPENDENCIES,contract,unit,affected,compile_sql
from .execution import execute,probe,expected_claims
from .agents import call
METHODS=['shared_state','broadcast','targeted','sparse']
def artifact_hash(a):return digest(stable({k:v for k,v in a.items() if k not in ['call','online_issues','accepted']}))
def build_artifact(role,proposal,c,upstream,old=None):
 if isinstance(proposal,dict) and proposal.get('status')=='keep' and old is not None:return copy.deepcopy(old)
 a=dict(role=role,proposal=proposal,consumed_contract_hash=digest(c),dependencies={r:v['hash'] for r,v in upstream.items()},revision=1 if old is None else old['revision']+1)
 if isinstance(proposal,dict) and proposal.get('status')=='replace':
  try:
   if role in ['analysis','appendix']:
    q=proposal.get('query');validate_query(q);a['sql']=compile_sql(q);a['execution']=execute(a['sql'])
   elif role=='chart':
    v=proposal['view'];n=v['limit']
    if v['source']!='analysis' or type(n)!=int or n<1 or n>5:raise ValueError('Unsupported chart source or limit')
    a['points']=upstream['analysis']['rows'][:n];a['unit']=v['unit']
   else:
    v=proposal['summary']
    if v['source']!='chart':raise ValueError('Summary must consume chart')
    a['claims']=expected_claims(upstream['chart']['rows']);a['unit']=v['unit']
  except (ValueError,TypeError,KeyError,IndexError) as e:a['tool_error']=str(e)
 return a
def validate_query(q):
 import datetime
 keys={'start','end','country','inclusion','customer','metric'}
 if not isinstance(q,dict) or set(q)!=keys:raise ValueError('Query must supply exactly '+str(sorted(keys)))
 if q['inclusion'] not in ['positive','signed'] or q['customer'] not in ['all','known'] or q['metric'] not in ['units','value_micro']:raise ValueError('Unsupported query option')
 if not isinstance(q['country'],str) or len(q['country'])>80:raise ValueError('Invalid country')
 for k in ['start','end']:datetime.date.fromisoformat(q[k])
 if q['start']>=q['end']:raise ValueError('Invalid period')
def public_check(role,a,c,artifacts,check_log):
 issues=[];check_log.append(dict(kind='artifact_check',role=role))
 if a is None:return ['missing_artifact']
 p=a.get('proposal')
 if not isinstance(p,dict) or p.get('status')!='replace':return ['malformed_or_blocked']
 if a.get('consumed_contract_hash')!=digest(c):issues.append('stale_instruction')
 if a.get('tool_error'):issues.append('tool_failed:'+a['tool_error'])
 for dep in DEPENDENCIES[role]:
  parent=artifacts.get(dep)
  if parent is None or not parent.get('accepted'):issues.append('unaccepted_dependency:'+dep)
  if parent is None or a.get('dependencies',{}).get(dep)!=artifact_hash(parent):issues.append('stale_dependency:'+dep)
 if role in ['analysis','appendix']:
  if p.get('query')!={k:v for k,v in c.items() if k!='scope'}:issues.append('query_parameters_do_not_match_applicable_contract')
  result=a.get('execution',{})
  if result.get('status')!='ok':issues.append('query_failed:'+result.get('error','missing SELECT'))
  test=probe(a.get('sql'),c);check_log.append(dict(kind='public_probe',role=role,status=test['status']))
  if test['status']!='passed':issues.append(test['reason'])
 elif role=='chart':
  if a.get('unit')!=unit(c):issues.append('unit_mismatch')
  expected=artifacts.get('analysis',{}).get('execution',{}).get('rows')
  if p.get('view',{}).get('limit')!=c['display_n'] or expected is None or a.get('points')!=expected[:c['display_n']]:issues.append('chart_does_not_match_current_analysis')
 else:
  if a.get('unit')!=unit(c):issues.append('unit_mismatch')
  points=artifacts.get('chart',{}).get('points')
  try:expected=expected_claims(points)
  except (TypeError,IndexError):expected=None
  if expected is None or a.get('claims')!=expected:issues.append('report_claims_do_not_match_chart')
 return issues
def inspect(project,epoch,artifacts,check_log):
 for r in ROLES:
  if r in artifacts:
   a=artifacts[r];a['online_issues']=public_check(r,a,contract(project,r,epoch),artifacts,check_log);a['accepted']=not a['online_issues']
 return {r:artifacts.get(r,{}).get('online_issues',['missing_artifact']) for r in ROLES}
def upstream_state(role,artifacts):
 out={}
 for r in DEPENDENCIES[role]:
  a=artifacts.get(r,{})
  p=a.get('proposal');out[r]=dict(hash=artifact_hash(a),accepted=a.get('accepted',False),proposal=p if isinstance(p,dict) else None,rows=a.get('execution',{}).get('rows') if r=='analysis' else a.get('points'))
 return out
def snapshot(event,round_id,artifacts,extra=None):
 return dict(event=event,round=round_id,artifacts=copy.deepcopy(artifacts),extra=extra or {})
def run(project,rep,method='targeted',initial=None,generate_fn=call,phase='evaluation',stress=None,round_limit=2):
 validate_graph(project.get('dependencies',DEPENDENCIES))
 started=time.perf_counter();artifacts=copy.deepcopy(initial or {});calls=[];events=[];checks=[];routes=[]
 epoch=0 if initial is None else 1
 if stress=='exception_generalization':
  # Matched stress: a peer modifies protected appendix output, never the user's scope.
  if artifacts.get('appendix',{}).get('execution',{}).get('rows'):
   artifacts['appendix']['execution']['rows'][0][1]+=1
   artifacts['appendix']['proposal']['query']['country']='peer_scope_error'
  events.append(snapshot('constructed_disturbance',-1,artifacts,dict(type=stress)))
 if stress=='stale_peer':
  # Same controlled disturbance for every policy: a peer draft changes a chart field, never authority.
  if artifacts.get('chart',{}).get('proposal'):
   artifacts['chart']['unit']='peer_suggested_wrong_unit'
  events.append(snapshot('constructed_disturbance',-1,artifacts,dict(type=stress)))
 inspect(project,epoch,artifacts,checks);events.append(snapshot('initial' if epoch==0 else 'user_change',-1,artifacts,project.get('user_change') if epoch else None))
 recipients=set(ROLES if epoch==0 or method=='broadcast' else affected(project))
 if epoch and method=='sparse':recipients={r for r in recipients if not any(p in recipients for p in DEPENDENCIES[r])}
 attempts_by_role={r:0 for r in ROLES};direct=set();forwarded=0
 for round_id in range(round_limit):
  if method in ['shared_state','global_packet'] or round_id>0:
   issues=inspect(project,epoch,artifacts,checks);recipients={r for r in ROLES if issues[r]}
  if not recipients:break
  called=[];expanded=set(recipients)
  for role in ROLES:
   if role not in expanded or attempts_by_role[role]>=round_limit:continue
   issues=inspect(project,epoch,artifacts,checks)[role]
   if round_id>0 and not issues:continue
   if any(not artifacts.get(p,{}).get('accepted') for p in DEPENDENCIES[role]):
    events.append(snapshot('dependency_wait',round_id,artifacts,dict(role=role)));continue
   delivery='shared_state' if method=='shared_state' else 'forwarded' if role not in recipients else 'direct'
   if delivery=='forwarded':forwarded+=1
   else:direct.add(role)
   old=artifacts.get(role);style='state' if method=='shared_state' else 'packet';feedback=[] if method=='targeted_no_feedback' else issues
   seed=170000+rep*1000+sum(ord(x) for x in project['id'])*10+ROLES.index(role)*2+round_id
   key='_'.join(map(str,[phase,project['id'],'r'+str(rep),method,'before' if epoch==0 else 'after',stress or 'ordinary',round_id,role]))
   proposal,usage=generate_fn(key,role,project,epoch,old,upstream_state(role,artifacts),feedback,seed,style,delivery)
   calls.append(usage);attempts_by_role[role]+=1;called.append(role);routes.append(dict(round=round_id,role=role,delivery=delivery,feedback=feedback,source='authorized_user',scope=contract(project,role,epoch)['scope']))
   artifacts[role]=build_artifact(role,proposal,contract(project,role,epoch),upstream_state(role,artifacts),old)
   inspect(project,epoch,artifacts,checks);events.append(snapshot('agent_continuation',round_id,artifacts,dict(role=role,delivery=delivery,call_id=key)))
   if method=='sparse' and isinstance(proposal,dict):
    for dst in proposal.get('notify',[]) if isinstance(proposal.get('notify'),list) else []:
     if dst in DEPENDENCIES and role in DEPENDENCIES[dst] and dst not in called:expanded.add(dst)
  inspect(project,epoch,artifacts,checks);events.append(snapshot('round_complete',round_id,artifacts))
 inspect(project,epoch,artifacts,checks)
 return dict(project_id=project['id'],month=project['month'],rep=rep,method=method,epoch=epoch,stress=stress or 'ordinary',artifacts=artifacts,events=events,calls=calls,routes=routes,checks=checks,direct_recipients=sorted(direct),forwarded_messages=forwarded,seconds=time.perf_counter()-started,user_changes=epoch,user_questions=0)

def validate_graph(graph):
 if set(graph)!=set(ROLES):raise ValueError('Unknown responsibility')
 done=set()
 for r in ROLES:
  if any(d not in done for d in graph[r]):raise ValueError('Dependency cycle or non-topological registration')
  done.add(r)
 if graph!=DEPENDENCIES:raise ValueError('Only the frozen dependency graph is supported')
