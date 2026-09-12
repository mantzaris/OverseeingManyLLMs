"""Publication figures from saved numerical evidence, with explicit units."""
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
 plt.rcParams.update({'font.size':11,'axes.titlesize':12,'axes.labelsize':11,'legend.fontsize':10,'font.family':'DejaVu Sans','pdf.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
def save(fig,path):
 if not getattr(fig,'manual_layout',False):fig.tight_layout()
 for ext in ['pdf','svg','png']:
  p=path.with_suffix('.'+ext);fig.savefig(str(p),dpi=240,bbox_inches='tight')
  if ext=='svg':p.write_text('\n'.join(x.rstrip() for x in p.read_text().splitlines())+'\n')
 plt.close(fig)
def avg(rows,key):return np.mean([r[key] for r in rows]) if rows else 0

def run(root=ART,synthetic_root=None):
 from .secondary_analysis import interval
 root=Path(root);synthetic_root=Path(synthetic_root or (root if (root/'synthetic').exists() else ART));out=root/'figures';out.mkdir(parents=True,exist_ok=True);style()
 rows=load(root/'evaluation/episodes.csv');syn=load(synthetic_root/'synthetic/episodes.csv')
 def sel(m,b=1,condition='generated'):return [r for r in rows if r['method']==m and r['budget']==b and r['condition']==condition]
 def layout(fig,**kwargs):fig.manual_layout=True;fig.subplots_adjust(**kwargs)
 fig,axes=plt.subplots(1,2,figsize=(8,4.5));layout(fig,left=.10,right=.97,bottom=.32,top=.85,wspace=.30)
 for ax,cond,title in zip(axes,['generated','source_recovery'],['Generated candidates','Available instruction']):
  n=len({r['id'] for r in sel('verification',1,cond)})
  for j,m in enumerate(MAIN):
   rr=sel(m,1,cond);ids=sorted({r['id'] for r in rr});v={k:interval([avg([r for r in rr if r['id']==i],k) for i in ids]) for k in ['questions','correct']};x=v['questions'];y=v['correct']
   ax.errorbar(x['mean'],y['mean'],xerr=[[max(0,x['mean']-x['low'])],[max(0,x['high']-x['mean'])]],yerr=[[max(0,y['mean']-y['low'])],[max(0,y['high']-y['mean'])]],color=COLORS[m],marker=['o','s','^','D'][j],markersize=6,capsize=3,label=LABEL[m],alpha=.85)
  if cond=='source_recovery' and (root/'analysis/direct_source_reader.json').exists():
   rr=read(root/'analysis/direct_source_reader.json');ids=sorted({r['id'] for r in rr});v=interval([avg([r for r in rr if r['id']==i],'correct') for i in ids])
   ax.errorbar(0,v['mean'],yerr=[[max(0,v['mean']-v['low'])],[max(0,v['high']-v['mean'])]],fmt='*',color='#222222',markersize=10,capsize=3,label='Direct reading (secondary)')
  ax.set(xlabel='Intent answers per task',title=title+'\n'+str(n)+' source databases',xlim=(-.08,1.08),ylim=(-.03,1.03),xticks=[0,.5,1],yticks=[0,.25,.5,.75,1]);ax.grid(alpha=.15)
 axes[0].set_ylabel('Reference-table agreement');axes[1].tick_params(labelleft=False)
 h,l=axes[1].get_legend_handles_labels();fig.legend(h,l,loc='lower center',bbox_to_anchor=(.55,.005),ncol=2,frameon=False,fontsize=10)
 save(fig,out/'quality_vs_questions')
 fig,axes=plt.subplots(1,2,figsize=(8,3.8));layout(fig,left=.10,right=.97,bottom=.27,top=.88,wspace=.25)
 for ax,k,title in zip(axes,['wrong','unfinished'],['Released table mismatches','Unfinished deliverables']):
  for m in MAIN:ax.plot([0,1,2],[avg(sel(m,b),k) for b in [0,1,2]],'-o',color=COLORS[m],label=LABEL[m],markersize=5)
  ax.set(title=title,xlabel='Available intent-answer budget',xticks=[0,1,2],ylim=(-.03,1.03));ax.grid(alpha=.15)
 axes[0].set_ylabel('Fraction of planned tasks');h,l=axes[0].get_legend_handles_labels();fig.legend(h,l,loc='lower center',ncol=2,frameon=False,fontsize=10);save(fig,out/'failures_and_budget')
 fig,axes=plt.subplots(1,2,figsize=(8,3.7));layout(fig,left=.26,right=.98,bottom=.31,top=.88,wspace=.18)
 for ax,cond,title in zip(axes,['generated','source_recovery'],['Generated candidates','Available instruction']):
  vals=[]
  for m in MAIN:
   rr=sel(m,1,cond);v=[avg(rr,k) for k in ['recovered','suppressed','questions']];vals.append(v+[1-sum(v)])
  vals=np.array(vals);left=np.zeros(4)
  for i,(label,color) in enumerate(zip(['Recovered','Conditional equality','User asked','Other / unfinished'],['#56B4E9','#009E73','#E69F00','#BBBBBB'])):
   ax.barh(range(4),vals[:,i],left=left,color=color,label=label);left+=vals[:,i]
  ax.set_yticks(range(4));ax.set_yticklabels([LABEL[m] for m in MAIN] if cond=='generated' else ['']*4,fontsize=10);ax.set(title=title,xlabel='Fraction of replicas',xlim=(0,1),xticks=[0,.5,1])
 h,l=axes[0].get_legend_handles_labels();fig.legend(h,l,loc='lower center',bbox_to_anchor=(.6,0),ncol=2,frameon=False,fontsize=10);save(fig,out/'resolution_routes')
 fig,axes=plt.subplots(1,2,figsize=(8.5,4));layout(fig,left=.10,right=.97,bottom=.28,top=.87,wspace=.40)
 for m in ['verification','no_coverage_guard','matched_checking']:
  rr=sel(m);covered=[r for r in rr if r['intended_covered']==1];omitted=[r for r in rr if r['intended_covered']==0]
  axes[0].plot([0,1],[avg(omitted,'wrong'),avg(covered,'wrong')],'-o',color=COLORS[m],label=LABEL[m]);axes[1].scatter(avg(rr,'executions'),avg(sel('recovery_completion'),'questions')-avg(rr,'questions'),s=50,c=COLORS[m],label=LABEL[m])
 axes[0].set_xticks([0,1]);axes[0].set_xticklabels(['Absent\n(n='+str(len(omitted))+')','Covered\n(n='+str(len(covered))+')'],fontsize=10);axes[0].set(ylabel='Released mismatch fraction',title='Reference-output coverage',ylim=(-.03,1.03))
 axes[1].set(xlabel='SQL executions per task',ylabel='Intent answers saved per task',title='Machine cost versus demand');h,l=axes[0].get_legend_handles_labels();fig.legend(h,l,loc='lower center',ncol=3,frameon=False,fontsize=10);save(fig,out/'coverage_and_cost')
 families=['equal_snapshot','shared_decision','scope_exception','unaffected_work','omitted_intent','correlated_omission','snapshot_change','failed_query','empty_trap','process_requirement'];methods=['verification','no_coverage_guard','no_sharing','all_wait'];mats=[[],[]]
 for f in families:
  baseline=[r for r in syn if r['family']==f and r['budget']==1 and r['method']=='recovery_completion']
  for mat,key in zip(mats,['loss','questions']):mat.append([avg([r for r in syn if r['family']==f and r['budget']==1 and r['method']==m],key)-avg(baseline,key) for m in methods])
 fig,axes=plt.subplots(1,2,figsize=(9,4.7));layout(fig,left=.22,right=.97,bottom=.22,top=.86,wspace=.27)
 for j,(ax,data,title) in enumerate(zip(axes,mats,['Loss difference\nnegative is better','Answer difference\nnegative is fewer'])):
  lim=max(.01,np.max(np.abs(data)));im=ax.imshow(data,cmap='RdBu_r',vmin=-lim,vmax=lim,aspect='auto');ax.set_yticks(range(10));ax.set_yticklabels([f.replace('_',' ') for f in families] if j==0 else ['']*10,fontsize=10);ax.set_xticks(range(4));ax.set_xticklabels(['Verify','No guard','No sharing','Wait all'],rotation=30,ha='right',fontsize=10);ax.set_title('Synthetic '+title,fontsize=11)
  for i,row in enumerate(data):
   for k,v in enumerate(row):ax.text(k,i,f'{v:+.1f}',ha='center',va='center',fontsize=11,color='white' if abs(v)>lim*.6 else '#222222')
  fig.colorbar(im,ax=ax,shrink=.7,pad=.03)
 save(fig,out/'synthetic_ablations')
 traces=read(synthetic_root/'synthetic/example_traces.json');fig,axes=plt.subplots(2,1,figsize=(8,5.6));layout(fig,left=.20,right=.96,bottom=.16,top=.90,hspace=.58)
 for ax,family,title in zip(axes,['unaffected_work','correlated_omission'],['Authored shared scope with independent progress','Authored correlated omission']):
  for j,m in enumerate(['recovery_completion','verification']):
   events=[e for e in traces[family+'|'+m+'|1']['events'] if e['event'] in ['release','show_question','answer','answer_result']]
   for i,e in enumerate(events):
    color='#0072B2' if e['event'] in ['release','answer_result'] else '#E69F00';ax.scatter(i,j,c=color,s=40);word={'release':'released','show_question':'question','answer':'answered','answer_result':'updated'}[e['event']];ax.annotate(word+'\n'+e.get('task',''),(i,j),xytext=(0,12 if j else -27),textcoords='offset points',fontsize=10,ha='center')
  ax.set_yticks([0,1]);ax.set_yticklabels(['Completion','Verification'],fontsize=10);ax.set(title=title,ylim=(-.85,1.9));ax.margins(x=.08);ax.grid(axis='x',alpha=.12)
 axes[1].set_xlabel('Controller event order (not human time)');save(fig,out/'synthetic_event_examples')
 paired=read(root/'analysis/paired.json');p=next(x for x in paired if x['condition']=='generated' and x['budget']==1 and x['baseline']=='recovery_completion' and x['metric']=='loss');d=p['differences'];fig,axes=plt.subplots(1,2,figsize=(8.5,3.6),gridspec_kw={'width_ratios':[1.4,1]});layout(fig,left=.08,right=.98,bottom=.24,top=.85,wspace=.65)
 axes[0].bar(range(len(d)),d,color=['#0072B2' if x<0 else '#D55E00' if x>0 else '#999999' for x in d]);axes[0].axhline(0,c='black',lw=.8);positions=[i for i,x in enumerate(d) if x];axes[0].set_xticks(positions);axes[0].set_xticklabels([p['source_ids'][i] for i in positions],fontsize=10);axes[0].set(xlabel=str(len(d))+' databases in frozen ID order',ylabel='Loss difference',title=f"{p['negative']} wins, {p['ties']} ties, {p['positive']} losses")
 for i,k in enumerate(['questions','correct','wrong','unfinished']):
  z=next(x for x in paired if x['condition']=='generated' and x['budget']==1 and x['baseline']=='recovery_completion' and x['metric']==k);axes[1].errorbar(z['mean'],i,xerr=[[max(0,z['mean']-z['low'])],[max(0,z['high']-z['mean'])]],fmt='o',color='#0072B2',capsize=3)
 axes[1].axvline(0,c='black',lw=.8);axes[1].set_yticks(range(4));axes[1].set_yticklabels(['Answers','Matching','Mismatched','Unfinished'],fontsize=10);axes[1].set(xlabel='Paired difference per task',title='Outcome changes (95% intervals)');axes[1].grid(axis='x',alpha=.15);save(fig,out/'paired_differences')
 (out/'README.txt').write_text('Plots derive from saved CSV and JSON. Full captions: research/verification_escalation/FIGURES.md. Generated panels use human-authored requests/annotations with generated databases/SQL and simulated answers/policies. Synthetic panels are authored mechanism tests. No measured human workload. The original 48-database adapter was defective and remains separate from the corrected 24-database follow-up.\n')
 print('Seven figures in',out)
if __name__=='__main__':run()
