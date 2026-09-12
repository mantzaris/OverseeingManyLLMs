"""Development and frozen continuation collection with retained failures."""
import argparse,time,copy
from pathlib import Path
from .common import ART,read,write,stable
from .contracts import initial_manifest
from .controller import run,METHODS
from .evaluate import score
def collect(split,revision='v1',limit=None):
 if split=='evaluation':
  from .freeze import verify
  if limit is not None:raise ValueError('No evaluation prefix changes after freeze')
  manifest=verify()
 else:manifest=initial_manifest()
 projects=manifest[split];projects=projects if limit is None else projects[:limit]
 root=ART/split/revision;root.mkdir(parents=True,exist_ok=True);summary=[]
 for project in projects:
  reps=[0] if split=='development' else manifest['replicates']
  for rep in reps:
   prefix=split+'_'+revision
   p=root/(project['id']+'_r'+str(rep)+'_initial.json')
   if p.exists():initial=read(p)
   else:initial=run(project,rep,'targeted',phase=prefix);write(p,initial)
   summary.append(score(project,initial))
   methods=METHODS if split!='development' else ['shared_state','broadcast','targeted','sparse']
   # Rotate execution order independent of generated outcomes.
   offset=(projects.index(project)+rep)%len(methods);methods=methods[offset:]+methods[:offset]
   for method in methods:
    p=root/(project['id']+'_r'+str(rep)+'_'+method+'.json')
    if p.exists():result=read(p)
    else:result=run(project,rep,method,initial['artifacts'],phase=prefix);write(p,result)
    row=score(project,result,initial['artifacts']);summary.append(row);write(root/'summary.json',summary)
    print(project['id'],rep,method,'initial correct',score(project,initial)['raw_correct'],'final',row['raw_correct'],row['accepted_correct'],'calls',row['calls'],flush=True)
 if split=='evaluation':
  from .pipeline import pipeline
  for project in projects:
   for rep in manifest['replicates']:
    initial=read(root/(project['id']+'_r'+str(rep)+'_initial.json'))
    result=pipeline(project,rep,initial['artifacts']);write(root/(project['id']+'_r'+str(rep)+'_pipeline.json'),result)
    summary.append(score(project,result,initial['artifacts']))
  secondary=[]
  for project in projects:
   initial=read(root/(project['id']+'_r0_initial.json'))
   conditions=[('global_packet',None)]
   if project['id'] in manifest['secondary']['stress']['projects']:
    conditions += [(m,'exception_generalization') for m in METHODS]+[('targeted_no_feedback','exception_generalization')]
   for method,stress in conditions:
    p=root/'secondary'/(project['id']+'_r0_'+method+'_'+(stress or 'ordinary')+'.json')
    if p.exists():result=read(p)
    else:result=run(project,0,method,initial['artifacts'],phase=split+'_'+revision,stress=stress);write(p,result)
    secondary.append(score(project,result,initial['artifacts']));write(root/'secondary_summary.json',secondary)
    print('secondary',project['id'],method,stress,secondary[-1]['project_correct'],secondary[-1]['calls'],flush=True)
 write(root/'summary.json',summary);return summary
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('split',choices=['development','evaluation']);p.add_argument('--revision',default='v1');p.add_argument('--limit',type=int);a=p.parse_args();collect(a.split,a.revision,a.limit)
