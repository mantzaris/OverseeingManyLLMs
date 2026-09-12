"""Saved-output analysis; no GPU, no changes to collected outcomes."""
import csv,copy,collections,math
from pathlib import Path
import numpy as np
from .common import ART,read,write,stable
from .contracts import ROLES,contract
from .controller import METHODS,artifact_hash
from .evaluate import score
from .statistics import paired

def csv_write(path,rows):
 if not rows:return
 fields=[k for k in rows[0] if not isinstance(rows[0][k],(dict,list))]
 with path.open('w') as f:
  w=csv.DictWriter(f,fields,extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows)
def summarize(rows):
 result=[]
 for method in METHODS+['pipeline','global_packet','targeted_no_feedback']:
  rr=[r for r in rows if r['method']==method]
  if not rr:continue
  out=dict(method=method,runs=len(rr))
  for k in ['project_correct','accepted_correct','accepted_wrong','unfinished','raw_correct','requirement_violations','dependency_inconsistencies','unnecessary_modifications','appendix_correct','calls','attempts','tokens','inference_seconds','rounds','repair_repeats','direct_recipients','forwarded_messages','public_probe_executions','V']:
   out[k+'_total']=sum(r[k] for r in rr);out[k+'_mean']=float(np.mean([r[k] for r in rr]))
  result.append(out)
 return result

def analyze(output=None):
 m=read(ART/'frozen/manifest.json');root=ART/'evaluation/frozen';out=Path(output) if output else ART/'analysis';out.mkdir(exist_ok=True);rows=[];secondary=[];initials=[];artrows=[];eventrows=[];missing=[];runs={}
 for p in m['evaluation']:
  for rep in m['replicates']:
   ip=root/(p['id']+'_r'+str(rep)+'_initial.json')
   if not ip.exists():missing.append(str(ip));continue
   initial=read(ip);initials.append(score(p,initial))
   for method in METHODS+['pipeline']:
    path=root/(p['id']+'_r'+str(rep)+'_'+method+'.json')
    if not path.exists():missing.append(str(path));continue
    r=read(path);row=score(p,r,initial['artifacts']);rows.append(row);runs[(p['id'],rep,method)]=r
    for role in ROLES:
     a=r['artifacts'].get(role,{});artrows.append(dict(project_id=p['id'],month=p['month'],rep=rep,method=method,role=role,snapshot_correct=row['artifact_correct'][role],accepted=row['artifact_accepted'][role],issues=' | '.join(a.get('online_issues',['missing_artifact'])),revision=a.get('revision',0),unaffected=contract(p,role,0)==contract(p,role,1),modified=artifact_hash(a)!=artifact_hash(initial['artifacts'].get(role,{}))))
    step=0
    for index,e in enumerate(r['events']):
     if e['event']=='agent_continuation':step+=1
     tmp=copy.copy(r);tmp.update(artifacts=e['artifacts'],calls=[],routes=[],checks=[])
     s=score(p,tmp);pubissues=[x for a in e['artifacts'].values() for x in a.get('online_issues',[])];public_r=sum(any(not x.startswith(('unaccepted_dependency','stale_dependency')) for x in e['artifacts'].get(role,{}).get('online_issues',['missing_artifact'])) for role in ROLES)
     eventrows.append(dict(project_id=p['id'],month=p['month'],rep=rep,method=method,index=index,step=step,event=e['event'],round=e['round'],role=e['extra'].get('role',''),V=s['V'],public_V=public_r/4+s['dependency_inconsistencies']/4+s['unfinished']/4,correct=s['accepted_correct'],unfinished=s['unfinished']))
 for path in sorted((root/'secondary').glob('*.json')):
  r=read(path);p=next(p for p in m['evaluation'] if p['id']==r['project_id']);initial=read(root/(p['id']+'_r0_initial.json'));sr=score(p,r,initial['artifacts']);sr['unaffected_rewrites']=sr['unnecessary_modifications'];sr['rewrite_interpretation']='Includes necessary restoration of the corrupted appendix; not all rewrites are unnecessary.' if r['stress']!='ordinary' else 'Intact contract-unaffected artifacts rewritten.';secondary.append(sr)
 stress=[r for r in secondary if r['stress']!='ordinary'];global_rows=[r for r in secondary if r['method']=='global_packet']
 comparisons=[]
 for left,right in m['comparisons']:
  for metric in m['metrics']:comparisons.append(paired(rows,left,right,metric))
 # Same project IDs and replica 0 for the matched packet-format control.
 subset=[r for r in rows if r['rep']==0]+global_rows
 for metric in ['project_correct','calls','tokens']:
  comparisons.append(paired(subset,'targeted','global_packet',metric))
 stress_comparisons=[]
 if len(stress)==40:
  for right in ['broadcast','shared_state','sparse','targeted_no_feedback']:
   for metric in ['project_correct','calls','unnecessary_modifications']:
    stress_comparisons.append(paired(stress,'targeted',right,metric))
 examples={}
 for label,sign in [('favorable',1),('tie',0),('unfavorable',-1)]:
  for p in m['evaluation']:
   a=next(r for r in rows if r['project_id']==p['id'] and r['rep']==0 and r['method']=='targeted');b=next(r for r in rows if r['project_id']==p['id'] and r['rep']==0 and r['method']=='broadcast')
   d=a['project_correct']-b['project_correct']
   if (d>0 if sign==1 else d<0 if sign==-1 else d==0):examples[label]=dict(project_id=p['id'],rep=0,criterion='project_correct',targeted=a['project_correct'],broadcast=b['project_correct']);break
  if label not in examples:
   for p in m['evaluation']:
    a=next(r for r in rows if r['project_id']==p['id'] and r['rep']==0 and r['method']=='targeted');b=next(r for r in rows if r['project_id']==p['id'] and r['rep']==0 and r['method']=='broadcast');d=b['calls']-a['calls']
    if (d>0 if sign==1 else d<0 if sign==-1 else d==0):examples[label]=dict(project_id=p['id'],rep=0,criterion='calls_saved',targeted=a['calls'],broadcast=b['calls']);break
 for p in m['evaluation']:
  found=False
  for method in METHODS:
   rr=next(r for r in rows if r['project_id']==p['id'] and r['rep']==0 and r['method']==method)
   if not rr['project_correct']:examples['failure']=dict(project_id=p['id'],rep=0,method=method);found=True;break
  if found:break
 write(out/'primary_rows.json',rows);write(out/'secondary_rows.json',secondary);write(out/'initial_rows.json',initials);write(out/'comparisons.json',comparisons);write(out/'stress_comparisons.json',stress_comparisons);write(out/'examples.json',examples)
 csv_write(out/'episodes.csv',rows);csv_write(out/'secondary.csv',secondary);csv_write(out/'artifacts.csv',artrows);csv_write(out/'events.csv',eventrows)
 sums=summarize(rows);ss=summarize(stress);gs=summarize(global_rows)
 write(out/'summary.json',dict(primary=sums,stress=ss,global_packet=gs,initial=dict(runs=len(initials),correct_projects=sum(r['project_correct'] for r in initials),correct_artifacts=sum(r['accepted_correct'] for r in initials)),missing=missing,source_blocks=8,retailers=1))
 csv_write(out/'policy_summary.csv',sums)
 from .client import parsed
 grouped=collections.defaultdict(list)
 for path in sorted((ART/'raw').glob('evaluation_frozen*.json')):
  raw=read(path)
  if raw['status']=='ok':grouped[raw['request_sha256']].append(raw)
 variation=[]
 for key,group in sorted(grouped.items()):
  if len(group)<2:continue
  decoded=[parsed(r) for r in group]
  semantic=[{k:p.get(k) for k in ['status','query','view','summary','notify']} if isinstance(p,dict) else p for p in decoded]
  from .common import digest
  from .normalize import normalize
  import json
  role=json.loads(group[0]['request']['messages'][-1]['content'].split('\n',1)[1])['packet']['responsibility']
  normalized=[normalize(p,role) for p in decoded]
  normalized_choices=[{k:p.get(k) for k in ['status','query','view','summary','notify']} if isinstance(p,dict) else p for p in normalized]
  variation.append(dict(distinct_normalized_tool_choices=len({digest(p) for p in normalized_choices}),request_sha256=key,calls=[r['call_id'] for r in group],responses=len(group),distinct_parsed_outputs=len({digest(p) for p in decoded}),distinct_tool_choices=len({digest(p) for p in semantic})))
 write(out/'request_variation.json',dict(groups=variation,repeated_request_groups=len(variation),groups_with_different_parsed_outputs=sum(g['distinct_parsed_outputs']>1 for g in variation),groups_with_different_tool_choices=sum(g['distinct_tool_choices']>1 for g in variation),groups_with_different_normalized_tool_choices=sum(g['distinct_normalized_tool_choices']>1 for g in variation),interpretation='Identical full payload including sampling seed. The legacy tool-choice field is a projection of schema fields, so envelope differences can count. The added normalized comparison accepts equivalent explicit envelopes. Both exclude free-form titles/prose and retain notify recipients. Fresh GPU calls are not promised deterministic.'))

 print('initial',len(initials),sum(r['project_correct'] for r in initials),'missing',len(missing))
 for r in sums:print(r['method'],r['project_correct_total'],'/',r['runs'],'correct; calls',r['calls_total'],'tokens',r['tokens_total'])
 return rows
if __name__=='__main__':analyze()
