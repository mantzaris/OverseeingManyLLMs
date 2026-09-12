"""Publication plots from saved tables; no hand-entered numerical outcomes."""
import json,collections
from pathlib import Path
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .common import ART,read,write
LABEL={'adaptive':'Adaptive','fixed_audit':'Fixed acquisition','memory':'Context memory','source_rule':'Source rule','reattempt':'Reattempt','individual':'Individual','individual_risk':'Risk-only individual','frozen_model':'Frozen parameters'}
COLOR={'adaptive':'#007a78','fixed_audit':'#d46b24','memory':'#7261a8','source_rule':'#4078b2','reattempt':'#9a607d','individual':'#777777','individual_risk':'#252a31','frozen_model':'#bd9253'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelsize':10,'legend.fontsize':8,'svg.hashsalt':'adaptive-correction-transfer','pdf.fonttype':42,'ps.fonttype':42,'savefig.facecolor':'white'})
OUT=ART/'figures';OUT.mkdir(exist_ok=True);captions={}
def save(fig,name,caption):
 fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight',metadata={'CreationDate':None});fig.savefig(OUT/(name+'.svg'),bbox_inches='tight',metadata={'Date':None});fig.savefig(OUT/(name+'.png'),dpi=220,bbox_inches='tight');plt.close(fig);captions[name]=caption

def draw():
 s=pd.read_csv(ART/'analysis/summary.csv');e=pd.read_csv(ART/'analysis/episodes.csv');t=pd.read_csv(ART/'analysis/transfers.csv');p=pd.read_csv(ART/'analysis/paired.csv');a=pd.read_csv(ART/'analysis/audits.csv');d=pd.read_csv(ART/'analysis/disagreement.csv');m=read(ART/'frozen/manifest.json');ids=[c['id'] for c in m['contexts']];n=len(ids);methods=m['methods'];final=s[(s.budget==2)&s.method.isin(methods)].set_index('method')
 fig,ax=plt.subplots(1,2,figsize=(10.5,4.6));core=['individual_risk','memory','fixed_audit','adaptive']
 for k in core:
  z=s[(s.method==k)&(s.budget<=2)].sort_values('budget');ax[0].plot(z.budget,100*z.accuracy,'o-',color=COLOR[k],label=LABEL[k]);ax[0].fill_between(z.budget,100*z.accuracy_low,100*z.accuracy_high,alpha=.07,color=COLOR[k])
 ax[0].set(xlabel='Inspections per source context',ylabel='Official answer EM (%)',xticks=[0,1,2],title='Generated answers + ideal inspections');ax[0].legend(loc='upper left',ncol=2)
 offsets={'individual':(5,-12),'individual_risk':(5,7),'source_rule':(5,-12),'reattempt':(5,6),'fixed_audit':(5,-13),'adaptive':(5,7),'memory':(-80,6)}
 for k,r in final.iterrows():
  x=r.calls/r.episodes;y=100*r.accuracy;ax[1].scatter(x,y,s=70,facecolors='none',edgecolors=COLOR[k],marker=dict(adaptive='*',fixed_audit='^',memory='P',source_rule='v',reattempt='D',individual='o',individual_risk='s')[k],linewidths=1.6,zorder=3,label=LABEL[k])
 ax[1].set(xlabel='Recipient generations per context / replica',ylabel='Official answer EM (%)',title='Two inspections: correctness and machine cost');ax[1].margins(x=.2,y=.3);ax[1].legend(loc='upper center',bbox_to_anchor=(.5,-.23),ncol=2,frameon=False);fig.tight_layout();save(fig,'quality_cost',f'Natural held-out TAT-QA questions in {n} source contexts, two generated replicas. Left bands are descriptive 95% context-bootstrap intervals. Right shows additional GPU generations, excluding six common initial answers. Annotation inspection is idealized; machine cost is not human workload.')
 fig,ax=plt.subplots(1,2,figsize=(10.5,3.7));x=np.arange(len(methods));fixed=[];harmed=[];eventshelp=[];eventsharm=[]
 for k in methods:
  r=final.loc[k];fixed.append(r.sibling_fixed);harmed.append(r.sibling_damaged);z=t[(t.method==k)&(t.step<=2)];eventshelp.append(z['help'].sum());eventsharm.append(z.harm.sum())
 for panel,good,bad,title in [(ax[0],fixed,harmed,'Final answers never directly inspected'),(ax[1],eventshelp,eventsharm,'All regeneration events, including repeated repairs')]:
  panel.bar(x-.18,good,.36,label='Errors corrected',color='#007a78');panel.bar(x+.18,bad,.36,label='Correct answers damaged',color='#c76534');panel.set_xticks(x);panel.set_xticklabels([LABEL[k] for k in methods],rotation=35,ha='right',fontsize=8);panel.set(ylabel='Answer count',title=title);panel.legend()
 fig.tight_layout();save(fig,'transfer_and_harm','Generated sibling changes on held-out sources at two ideal inspections. Left compares final uninspected answers with their common initial states. Right counts transitions, so one output may contribute more than once. Format-invalid proposals retain the prior answer; valid harmful changes remain included.')
 fig,ax=plt.subplots(1,2,figsize=(10.5,3.8),sharey=True)
 for panel,pair in zip(ax,[('adaptive','fixed_audit'),('source_rule','reattempt')]):
  z=p[(p['first']==pair[0])&(p['second']==pair[1])&(p.budget==2)].set_index('context');v=np.array([z.loc[c,'difference'] if c in z.index else np.nan for c in ids])*100;panel.bar(np.arange(1,n+1),v,color=np.where(v>=0,'#007a78','#c76534'));panel.axhline(0,color='#333333',lw=.8);panel.set(xlabel='Source context in frozen order',ylabel='Paired EM difference (percentage points)',title=LABEL[pair[0]]+' minus '+LABEL[pair[1]]);panel.text(.03,.97,f'W / T / L: {(v>1e-7).sum()} / {(abs(v)<=1e-7).sum()} / {(v< -1e-7).sum()}',transform=panel.transAxes,va='top',fontsize=9)
 fig.tight_layout();save(fig,'paired_sources','Each bar averages two generation replicas within one source context. Positive differences favor the first method. Left isolates adaptive acquisition from fixed acquisition with the same transfer model. Right compares corrections with a matched no-correction reattempt under identical inspections and recipient lists.')
 fig,ax=plt.subplots(1,2,figsize=(10.5,3.6));
 for k in ['adaptive','fixed_audit','frozen_model']:
  z=a[(a.method==k)&(a.step<=2)].groupby('step').agg(recipients=('recipients','mean'),updates=('transfer_updates','mean'));ax[0].plot(z.index,z.recipients,'o-',color=COLOR[k],label=LABEL[k]);ax[1].plot(z.index,z.updates,'o-',color=COLOR[k],label=LABEL[k])
 ax[0].set(xlabel='Inspection step',ylabel='Mean regenerated siblings',xticks=[1,2],title='Reuse after sequential inspections');ax[1].set(xlabel='Inspection step',ylabel='Mean acquired transfer labels (cumulative)',xticks=[1,2],title='Learning requires another purchased inspection');ax[0].legend();ax[1].legend();fig.tight_layout();save(fig,'sequential_adaptation','Generated primary-policy traces from 24 contexts and frozen-parameter diagnostic from the declared first 12, replica zero. Transfer labels become available only when a regenerated answer is itself inspected. Lines connect two discrete protocol steps and do not imply continuous learning curves.')
 fig,ax=plt.subplots(1,2,figsize=(10.5,3.7));z=t[(t.method=='adaptive')&(t.step<=2)]
 bins=['context','lexical','evidence'];labels=[]
 for i,b in enumerate(bins):
  r=z[z['bin']==b];wrong=r[r.before==0];correct=r[r.before==1];f=wrong['help'].mean() if len(wrong) else 0;h=correct.harm.mean() if len(correct) else 0;ax[0].bar(i-.18,100*f,.36,color='#007a78');ax[0].bar(i+.18,100*h,.36,color='#c76534');labels.append(f'{b}\nwrong n={len(wrong)}, correct n={len(correct)}')
 ax[0].set_xticks(range(3));ax[0].set_xticklabels(labels,fontsize=8);ax[0].set(ylabel='Conditional event rate (%)',title='Adaptive regeneration: correction and harm');ax[0].legend(['Repair if previously wrong','Harm if previously correct'],fontsize=8)
 intervals=[(-1,0),(0,.1),(.1,.2),(.2,1)];xx=[];yy=[];nn=[]
 for lo,hi in intervals:
  r=z[(z.predicted_gain>lo)&(z.predicted_gain<=hi)]
  if len(r):xx.append(r.predicted_gain.mean());yy.append(r.gain.mean());nn.append(len(r))
 ax[1].plot([-.2,.5],[-.2,.5],color='#999999',ls='--');ax[1].scatter(xx,yy,s=np.array(nn)*2+30,color='#007a78');
 for x,y,count in zip(xx,yy,nn):ax[1].annotate('n='+str(count),(x,y),xytext=(5,5),textcoords='offset points',fontsize=8)
 ax[1].set(xlabel='Predicted net correctness gain',ylabel='Observed mean correctness change',title='Selected-action diagnostic, not calibration');ax[1].margins(.25);fig.tight_layout();save(fig,'transition_diagnostics','Evaluation annotations are used only offline in this figure. Relations are inferred from public question text and generated citations. Repeated transitions are dependent; counts and descriptive rates are shown without pretending that events are independent source units. Predicted versus realized gain is selection-biased and cannot establish calibrated risk.')
 syn=pd.read_csv(ART/'synthetic/results.csv');fig,ax=plt.subplots(figsize=(9.5,4));v=syn[syn.budget==2].groupby(['case','method']).correct.mean().unstack();cases=list(v.index);comp=['memory','source_rule','fixed_audit','adaptive'];arr=np.column_stack([(v[k]-v.individual).values for k in comp]);lim=max(.1,abs(arr).max());im=ax.imshow(arr,aspect='auto',cmap='BrBG',vmin=-lim,vmax=lim);ax.set_yticks(range(len(cases)));ax.set_yticklabels([x.replace('_',' ') for x in cases]);ax.set_xticks(range(len(comp)));ax.set_xticklabels([LABEL[k] for k in comp]);
 for i in range(len(cases)):
  for j in range(len(comp)):ax.text(j,i,f'{arr[i,j]:+.2f}',ha='center',va='center',color='white' if abs(arr[i,j])>.7*lim else '#172b33',fontsize=9)
 fig.colorbar(im,ax=ax,label='Correct answers minus individual correction (of four)');fig.tight_layout();save(fig,'synthetic_boundaries','Entirely constructed arithmetic tasks, initial errors and repair responses. Each row includes 32 fixed synthetic seeds and four distinct goals. Positive and harmful regimes are retained. This isolates protocol boundaries and does not estimate their natural prevalence or demonstrate superior model competence.')
 # Frozen first-qualifying examples, with no magnitude-based selection.
 selected={};ctxmap={c['id']:c for c in m['contexts']}
 for category,condition in [('transfer_help',lambda r:r['help']==1),('transfer_harm',lambda r:r['harm']==1),('transfer_tie',lambda r:r['gain']==0)]:
  found=None
  for method in ['adaptive','memory']:
   rows=t[(t.method==method)&(t.step<=2)].to_dict('records');rows.sort(key=lambda r:(ids.index(r['context']),r['rep'],r['step'],next(q['order'] for q in ctxmap[r['context']]['questions'] if q['id']==r['recipient'])))
   found=next((r for r in rows if condition(r)),None)
   if found:break
  if found:selected[category]=found
 for name,sgn in [('paired_help',1),('paired_tie',0),('paired_harm',-1)]:
  z=p[(p['first']=='adaptive')&(p['second']=='fixed_audit')&(p.budget==2)]
  for cid in ids:
   r=z[z.context==cid]
   if len(r) and int(np.sign(r.iloc[0].difference))==sgn:selected[name]=r.iloc[0].to_dict();break
 write(ART/'analysis/examples.json',selected)
 fig,ax=plt.subplots(3,1,figsize=(10,7.5));
 for panel,key in zip(ax,['transfer_help','transfer_tie','transfer_harm']):
  panel.axis('off');r=selected.get(key)
  if not r:panel.text(0,.8,key.replace('_',' ').title()+': none observed');continue
  c=ctxmap[r['context']];qs={q['id']:q for q in c['questions']};run=read(ART/'evaluation/runs'/('%s_r%d_%s_b2.json'%(c['id'],r['rep'],r['method'])));event=run['events'][int(r['step'])-1];repair=next(h for h in event['repairs'] if h['id']==r['recipient']);f=event['disclosure'];before=repair['before'];after=repair['after'];import textwrap
  lines=[key.replace('_',' ').title()+f' | source {ids.index(c["id"])+1} | {LABEL[r["method"]]}', 'Inspected: '+f['question'],'Verified answer: '+str(f['answer'])+' '+f['scale'],'Recipient: '+qs[r['recipient']]['question'],'Before: '+str(before['answer'])+' '+before['scale']+'   →   After: '+str(after['answer'])+' '+after['scale'],f'Official EM: {r["before"]:.0f} → {r["after"]:.0f}; inferred relation: {r["bin"]}']
  panel.text(0,.98,'\n'.join(textwrap.fill(x,110) for x in lines),va='top',fontsize=9,linespacing=1.4)
 fig.tight_layout();save(fig,'worked_examples','First qualifying helpful, unchanged and harmful accepted transfer in frozen source order, then replica, inspection and recipient order. Adaptive is preferred; context memory is used only if that category is absent. Source questions are human-written, proposals and repairs generated, annotations evaluator-provided, and inspections simulated. The full table, paragraph evidence and traces remain saved.')
 write(OUT/'captions.json',captions);print('Plotted',len(captions),'figure families')
if __name__=='__main__':draw()
