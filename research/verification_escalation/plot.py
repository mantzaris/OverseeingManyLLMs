"""All numerical figures derive from saved paired rows; PDF/SVG/PNG exports."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .common import ART,read
from .analyze import load
COLORS={'recovery_completion':'#0072B2','verification':'#009E73','full_context':'#D55E00','matched_checking':'#CC79A7','no_coverage_guard':'#E69F00','no_recovery':'#666666','no_sharing':'#56B4E9','all_wait':'#777777'}
LABEL={'recovery_completion':'Recovery + completion','verification':'Verification','full_context':'Full-context proposal','matched_checking':'Matched checking','no_coverage_guard':'No coverage guard','no_recovery':'No source recovery','no_sharing':'No sharing','all_wait':'Global wait'}
MAIN=['recovery_completion','verification','full_context','matched_checking']
def style():
 plt.rcParams.update({'font.size':10,'axes.titlesize':11,'axes.labelsize':10,'legend.fontsize':8,'font.family':'DejaVu Sans','pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
def save(fig,path):
 fig.tight_layout()
 for suffix in ['pdf','svg','png']:
  p=path.with_suffix('.'+suffix);fig.savefig(str(p),dpi=240,bbox_inches='tight')
  if suffix=='svg':p.write_text('\n'.join(x.rstrip() for x in p.read_text().splitlines())+'\n')
 plt.close(fig)
def avg(rr,k):return np.mean([r[k] for r in rr]) if rr else 0

def run(root=ART):
 root=Path(root);out=root/'figures';out.mkdir(parents=True,exist_ok=True);style();rows=load(root/'evaluation/episodes.csv');syn=load(root/'synthetic/episodes.csv')
 def sel(method,b=1,condition='generated'):return [r for r in rows if r['method']==method and r['budget']==b and r['condition']==condition]
 fig,ax=plt.subplots(1,2,figsize=(10,3.7))
 for axis,cond,title in zip(ax,['generated','source_recovery'],['Generated candidates: 48 source databases','Source availability diagnostic: 12 databases']):
  for j,m in enumerate(MAIN):
   rr=sel(m,1,cond);x=avg(rr,'questions');y=avg(rr,'correct');axis.scatter(x,y,s=60,c=COLORS[m],marker=['o','s','^','D'][j],label=LABEL[m],zorder=5)
   axis.annotate(LABEL[m],(x,y),xytext=(-5,-18-j*11 if abs(y-.5)<.02 else 8+j*10),textcoords='offset points',fontsize=8,ha='right' if x>.6 else 'left')
  axis.set(xlabel='Additional intent answers per task',ylabel='Correct table fraction',title=title,xlim=(-.1,1.15),ylim=(-.05,1.18));axis.grid(alpha=.15)
 save(fig,out/'quality_vs_questions')
 fig,ax=plt.subplots(1,2,figsize=(9,3.5))
 for axis,k,title in zip(ax,['wrong','unfinished'],['Incorrect releases','Unfinished deliverables']):
  for m in MAIN:axis.plot([0,1,2],[avg(sel(m,b),k) for b in [0,1,2]],marker='o',label=LABEL[m],color=COLORS[m])
  axis.set(title=title,xlabel='Available answer budget per task',ylabel='Fraction of planned tasks',xticks=[0,1,2],ylim=(-.03,1.05));axis.grid(alpha=.15)
 ax[1].legend();save(fig,out/'failures_and_budget')
 fig,ax=plt.subplots(1,2,figsize=(9.5,3.6))
 for axis,cond in zip(ax,['generated','source_recovery']):
  vals=[]
  for m in MAIN:
   rr=sel(m,1,cond);vals.append([avg(rr,'recovered'),avg(rr,'suppressed'),avg(rr,'questions'),1-avg(rr,'recovered')-avg(rr,'suppressed')-avg(rr,'questions')])
  vals=np.array(vals);left=np.zeros(len(MAIN))
  for i,(label,color) in enumerate(zip(['Recovered','Verified equal','User asked','Other release / unfinished'],['#56B4E9','#009E73','#E69F00','#BBBBBB'])):
   axis.barh(range(len(MAIN)),vals[:,i],left=left,color=color,label=label);left+=vals[:,i]
  axis.set_yticks(range(len(MAIN)));axis.set_yticklabels([LABEL[m] for m in MAIN]);axis.set(title=cond.replace('_',' '),xlabel='Fraction of task replicas',xlim=(0,1))
 ax[1].legend(loc='upper center',bbox_to_anchor=(.2,-.2),ncol=2);save(fig,out/'resolution_routes')
 fig,ax=plt.subplots(1,2,figsize=(9.5,3.6))
 for m in ['verification','no_coverage_guard','matched_checking']:
  rr=sel(m);covered=[r for r in rr if r['intended_covered']==1];omitted=[r for r in rr if r['intended_covered']==0]
  ax[0].plot([0,1],[avg(omitted,'wrong'),avg(covered,'wrong')],'-o',color=COLORS[m],label=LABEL[m]);ax[1].scatter(avg(rr,'executions'),avg(sel('recovery_completion'),'questions')-avg(rr,'questions'),s=60,c=COLORS[m],label=LABEL[m]);ax[1].annotate(LABEL[m],(avg(rr,'executions'),avg(sel('recovery_completion'),'questions')-avg(rr,'questions')),xytext=(4,4),textcoords='offset points',fontsize=8)
 ax[0].set_xticks([0,1]);ax[0].set_xticklabels(['Intended output absent','Intended output covered']);ax[0].set(ylabel='Incorrect release fraction',title='Generated-candidate diagnostic',ylim=(-.03,1.05));ax[0].legend(fontsize=8)
 ax[1].set(xlabel='SQL executions per task',ylabel='Answers saved versus completion',title='Machine effort and interaction demand');save(fig,out/'coverage_and_cost')
 families=['equal_snapshot','shared_decision','scope_exception','unaffected_work','omitted_intent','correlated_omission','snapshot_change','failed_query','empty_trap','process_requirement']
 methods=['verification','no_coverage_guard','no_sharing','all_wait']
 fig,ax=plt.subplots(1,2,figsize=(11,4.6));mat=[];qs=[]
 for f in families:
  base=[r for r in syn if r['family']==f and r['budget']==1 and r['method']=='recovery_completion']
  mat.append([avg([r for r in syn if r['family']==f and r['budget']==1 and r['method']==m],'loss')-avg(base,'loss') for m in methods])
  qs.append([avg([r for r in syn if r['family']==f and r['budget']==1 and r['method']==m],'questions')-avg(base,'questions') for m in methods])
 for axis,data,title in zip(ax,[mat,qs],['Loss difference (negative is better)','Answer difference (negative is fewer)']):
  lim=max(.01,np.max(np.abs(data)));im=axis.imshow(data,cmap='RdBu_r',vmin=-lim,vmax=lim,aspect='auto');axis.set_yticks(range(len(families)));axis.set_yticklabels([f.replace('_',' ') for f in families]);axis.set_xticks(range(len(methods)));axis.set_xticklabels([LABEL[m] for m in methods],rotation=30,ha='right');axis.set_title('Synthetic: '+title)
  for i,row in enumerate(data):
   for j,v in enumerate(row):axis.text(j,i,f'{v:+.1f}',ha='center',va='center',fontsize=9,color='white' if abs(v)>lim*.6 else '#222222')
  fig.colorbar(im,ax=axis,shrink=.65)
 save(fig,out/'synthetic_ablations')
 # Prespecified synthetic example reveals a benefit and a correlated-error failure.
 traces=read(root/'synthetic/example_traces.json');fig,ax=plt.subplots(1,2,figsize=(10,3.8))
 for axis,fam,title in zip(ax,['unaffected_work','correlated_omission'],['Independent progress with a shared decision','A shared mistake can suppress the question']):
  for j,m in enumerate(['recovery_completion','verification']):
   tr=traces[fam+'|'+m+'|1'];events=tr['events'];visible=[e for e in events if e['event'] in ['release','show_question','answer','answer_result']]
   for i,e in enumerate(visible):
    color='#009E73' if e['event'] in ['release','answer_result'] else '#E69F00';axis.scatter(i,j,c=color,s=65);axis.annotate(e['event'].replace('_',' ')+'\n'+e.get('task',''),(i,j),xytext=(0,15 if j else -28),textcoords='offset points',fontsize=7,ha='center')
  axis.set_yticks([0,1]);axis.set_yticklabels(['Completion','Verification']);axis.set(title=title,xlabel='Controller event order (not human time)',ylim=(-.8,1.8));axis.grid(axis='x',alpha=.2)
 save(fig,out/'synthetic_event_examples')
 write_json=root/'figures/README.txt';write_json.write_text('All plots generated by research.verification_escalation.plot. Empirical = human-authored AMBROSIA requests, generated databases and Qwen proposals, simulated answers/policy replay. Synthetic panels are authored controlled SQL workloads. No measured human effort. Table hashes measure snapshot-output agreement only.\n')
 print('Six figures in',out)
if __name__=='__main__':run()
