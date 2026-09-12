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
 plt.rcParams.update({'font.size':12,'axes.titlesize':12,'axes.labelsize':11,'legend.fontsize':10,'font.family':'DejaVu Sans','pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
def save(fig,path):
 fig.tight_layout()
 for suffix in ['pdf','svg','png']:
  p=path.with_suffix('.'+suffix);fig.savefig(str(p),dpi=240,bbox_inches='tight')
  if suffix=='svg':p.write_text('\n'.join(x.rstrip() for x in p.read_text().splitlines())+'\n')
 plt.close(fig)
def avg(rr,k):return np.mean([r[k] for r in rr]) if rr else 0

def run(root=ART,synthetic_root=None):
 root=Path(root);out=root/'figures';out.mkdir(parents=True,exist_ok=True);style();rows=load(root/'evaluation/episodes.csv');synthetic_root=Path(synthetic_root or (root if (root/'synthetic').exists() else ART));syn=load(synthetic_root/'synthetic/episodes.csv')
 def sel(method,b=1,condition='generated'):return [r for r in rows if r['method']==method and r['budget']==b and r['condition']==condition]
 fig,ax=plt.subplots(1,2,figsize=(10,4.2))
 from .secondary_analysis import interval
 for axis,cond,label in zip(ax,['generated','source_recovery'],['Generated candidates','Source availability diagnostic']):
  n=len({r['id'] for r in sel('verification',1,cond)})
  for j,m in enumerate(MAIN):
   rr=sel(m,1,cond);ids=sorted({r['id'] for r in rr});values={k:[avg([r for r in rr if r['id']==i],k) for i in ids] for k in ['questions','correct']}
   x=interval(values['questions']);y=interval(values['correct'])
   axis.errorbar(x['mean'],y['mean'],xerr=[[max(0,x['mean']-x['low'])],[max(0,x['high']-x['mean'])]],yerr=[[max(0,y['mean']-y['low'])],[max(0,y['high']-y['mean'])]],color=COLORS[m],marker=['o','s','^','D'][j],markersize=7,capsize=3,label=LABEL[m],alpha=.85)
  axis.set(xlabel='Additional intent answers per task',ylabel='Reference-table agreement fraction',title=label+' ('+str(n)+' databases)',xlim=(-.08,1.1),ylim=(-.03,1.03));axis.grid(alpha=.15)
 ax[1].legend(loc='upper center',bbox_to_anchor=(-.1,-.2),ncol=2)
 save(fig,out/'quality_vs_questions')
 fig,ax=plt.subplots(1,2,figsize=(9,3.5))
 for axis,k,title in zip(ax,['wrong','unfinished'],['Released table mismatches','Unfinished deliverables']):
  for m in MAIN:axis.plot([0,1,2],[avg(sel(m,b),k) for b in [0,1,2]],marker='o',label=LABEL[m],color=COLORS[m])
  axis.set(title=title,xlabel='Available answer budget per task',ylabel='Fraction of planned tasks',xticks=[0,1,2],ylim=(-.03,1.05));axis.grid(alpha=.15)
 ax[1].legend();save(fig,out/'failures_and_budget')
 fig,ax=plt.subplots(1,2,figsize=(9.5,3.6))
 for axis,cond in zip(ax,['generated','source_recovery']):
  vals=[]
  for m in MAIN:
   rr=sel(m,1,cond);vals.append([avg(rr,'recovered'),avg(rr,'suppressed'),avg(rr,'questions'),1-avg(rr,'recovered')-avg(rr,'suppressed')-avg(rr,'questions')])
  vals=np.array(vals);left=np.zeros(len(MAIN))
  for i,(label,color) in enumerate(zip(['Recovered','Conditional equality','User asked','Other release / unfinished'],['#56B4E9','#009E73','#E69F00','#BBBBBB'])):
   axis.barh(range(len(MAIN)),vals[:,i],left=left,color=color,label=label);left+=vals[:,i]
  axis.set_yticks(range(len(MAIN)));axis.set_yticklabels([LABEL[m] for m in MAIN]);axis.set(title=cond.replace('_',' '),xlabel='Fraction of task replicas',xlim=(0,1))
 ax[1].legend(loc='upper center',bbox_to_anchor=(.2,-.2),ncol=2);save(fig,out/'resolution_routes')
 fig,ax=plt.subplots(1,2,figsize=(9.5,3.6))
 for m in ['verification','no_coverage_guard','matched_checking']:
  rr=sel(m);covered=[r for r in rr if r['intended_covered']==1];omitted=[r for r in rr if r['intended_covered']==0]
  ax[0].plot([0,1],[avg(omitted,'wrong'),avg(covered,'wrong')],'-o',color=COLORS[m],label=LABEL[m]);ax[1].scatter(avg(rr,'executions'),avg(sel('recovery_completion'),'questions')-avg(rr,'questions'),s=60,c=COLORS[m],label=LABEL[m])

 ax[0].set_xticks([0,1]);ax[0].set_xticklabels(['Reference output absent','Reference output covered']);ax[0].set(ylabel='Released table mismatch fraction',title='Generated-candidate diagnostic',ylim=(-.03,1.05));ax[0].legend(fontsize=8)
 ax[1].set(xlabel='SQL executions per task',ylabel='Answers saved versus completion',title='Machine effort and interaction demand');ax[1].legend(fontsize=8);save(fig,out/'coverage_and_cost')
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
 traces=read(synthetic_root/'synthetic/example_traces.json');fig,ax=plt.subplots(1,2,figsize=(10,3.8))
 for axis,fam,title in zip(ax,['unaffected_work','correlated_omission'],['Independent progress with a shared decision','A shared mistake can suppress the question']):
  for j,m in enumerate(['recovery_completion','verification']):
   tr=traces[fam+'|'+m+'|1'];events=tr['events'];visible=[e for e in events if e['event'] in ['release','show_question','answer','answer_result']]
   for i,e in enumerate(visible):
    color='#009E73' if e['event'] in ['release','answer_result'] else '#E69F00';axis.scatter(i,j,c=color,s=65);axis.annotate({'release':'released','show_question':'question','answer':'answered','answer_result':'updated'}[e['event']]+'\n'+e.get('task',''),(i,j),xytext=(0,16 if j else -34),textcoords='offset points',fontsize=9,ha='center')
  axis.set_yticks([0,1]);axis.set_yticklabels(['Completion','Verification']);axis.set(title=title,xlabel='Controller event order (not human time)',ylim=(-.8,1.8));axis.grid(axis='x',alpha=.2)
 save(fig,out/'synthetic_event_examples')
 write_json=root/'figures/README.txt';write_json.write_text('All plots generated by research.verification_escalation.plot. Empirical = human-authored AMBROSIA requests, generated databases and Qwen proposals, simulated answers/policy replay. Synthetic panels are authored controlled SQL workloads. No measured human effort. Table hashes measure snapshot-output agreement only.\n')
 paired=read(root/'analysis/paired.json')
 p=next(x for x in paired if x['condition']=='generated' and x['budget']==1 and x['baseline']=='recovery_completion' and x['metric']=='loss')
 fig,ax=plt.subplots(1,2,figsize=(11,3.8),gridspec_kw={'width_ratios':[2,1]})
 d=p['differences'];ax[0].bar(range(len(d)),d,color=['#0072B2' if x<0 else '#D55E00' if x>0 else '#999999' for x in d]);ax[0].axhline(0,c='black',lw=.8);ax[0].set_xticks(range(len(d)));ax[0].set_xticklabels(p['source_ids'],rotation=90,fontsize=7);ax[0].set(xlabel='Source database (paired unit), ID',ylabel='Verification minus completion loss',title=f"Generated: {p['negative']} wins, {p['ties']} ties, {p['positive']} losses")
 metrics=['questions','correct','wrong','unfinished'];names=['Intent answers','Matching tables','Released mismatches','Unfinished']
 for i,k in enumerate(metrics):
  z=next(x for x in paired if x['condition']=='generated' and x['budget']==1 and x['baseline']=='recovery_completion' and x['metric']==k)
  ax[1].errorbar(z['mean'],i,xerr=[[max(0,z['mean']-z['low'])],[max(0,z['high']-z['mean'])]],fmt='o',color='#0072B2',capsize=4)
 ax[1].axvline(0,c='black',lw=.8);ax[1].set_yticks(range(4));ax[1].set_yticklabels(names);ax[1].set(xlabel='Paired difference per task (95% interval)',title='Replicas averaged within source database');ax[1].grid(axis='x',alpha=.15)
 save(fig,out/'paired_differences')
 print('Seven figures in',out)
if __name__=='__main__':run()
