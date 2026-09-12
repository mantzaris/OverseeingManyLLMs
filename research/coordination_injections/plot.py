"""Publication figures derived exclusively from saved numerical evidence."""
import os,csv,json,collections
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from .common import ART,read,write,digest
from .contracts import ROLES,contract
from .controller import METHODS
COLORS={'shared_state':'#0072B2','broadcast':'#CC79A7','targeted':'#009E73','sparse':'#D55E00','pipeline':'#333333','global_packet':'#56B4E9','targeted_no_feedback':'#A6761D'}
SHORT={'shared_state':'Global','broadcast':'Broadcast','targeted':'Targeted','sparse':'Sparse','global_packet':'Global\npacket','targeted_no_feedback':'No detail'}
NAMES={'shared_state':'Global state','broadcast':'Broadcast','targeted':'Targeted','sparse':'Sparse + fallback','pipeline':'Pipeline','global_packet':'Global, same packet','targeted_no_feedback':'Targeted, no detail'}
plt.rcParams.update({'font.size':11,'axes.titlesize':12,'axes.labelsize':11,'legend.fontsize':10,'figure.dpi':140,'savefig.dpi':220,'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'svg.hashsalt':'coordination_injections_frozen','pdf.fonttype':42})
STAMP=datetime(2026,9,12,tzinfo=timezone.utc)
def save(fig,out,name,caption):
 fig.tight_layout();fig.savefig(out/(name+'.pdf'),bbox_inches='tight',metadata={'CreationDate':STAMP,'ModDate':STAMP});fig.savefig(out/(name+'.svg'),bbox_inches='tight',metadata={'Date':'2026-09-12'});fig.savefig(out/(name+'.png'),bbox_inches='tight');plt.close(fig)
 svg=out/(name+'.svg');svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
 with (out/'CAPTIONS.md').open('a') as f:f.write('## '+name+'\n\n'+caption+'\n\n')
def block_values(rows,method,metric):
 return np.array([np.mean([r[metric] for r in rows if r['month']==b and r['method']==method]) for b in sorted({r['month'] for r in rows})])
def interval(v):
 rng=np.random.RandomState(91843);z=v[rng.randint(0,len(v),(2000,len(v)))].mean(1);return np.percentile(z,[2.5,97.5])
def figures(analysis=None,output=None):
 analysis=Path(analysis) if analysis else ART/'analysis';out=Path(output) if output else ART/'figures';out.mkdir(parents=True,exist_ok=True);(out/'CAPTIONS.md').write_text('# Figure provenance and interpretation\n\n')
 rows=read(analysis/'primary_rows.json');secondary=read(analysis/'secondary_rows.json');comparisons=read(analysis/'comparisons.json');manifest=read(ART/'frozen/manifest.json');examples=read(analysis/'examples.json');events=list(csv.DictReader((analysis/'events.csv').open()));methods=METHODS+['pipeline']
 # A: Separate quality and inference cost with monthly-cluster uncertainty.
 fig,axs=plt.subplots(1,2,figsize=(8.4,3.6))
 for m in methods:
  x=block_values(rows,m,'calls');y=block_values(rows,m,'project_correct')*100;xi=interval(x);yi=interval(y)
  axs[0].errorbar(x.mean(),y.mean(),xerr=[[x.mean()-xi[0]],[xi[1]-x.mean()]],yerr=[[y.mean()-yi[0]],[yi[1]-y.mean()]],fmt='o',color=COLORS[m],capsize=3,label=NAMES[m])
  i=methods.index(m);a=block_values(rows,m,'accepted_correct');f=block_values(rows,m,'unfinished');w=block_values(rows,m,'accepted_wrong');axs[1].barh(i,a.mean(),color=COLORS[m]);axs[1].barh(i,w.mean(),left=a.mean(),color='#E69F00');axs[1].barh(i,f.mean(),left=a.mean()+w.mean(),color='#dddddd')
 axs[0].set(xlabel='LLM continuation calls per project',ylabel='All four structured artifacts correct (%)',ylim=(-3,108),title='Quality and communication cost');axs[0].grid(alpha=.18);axs[0].legend(loc='lower right')
 axs[1].set(yticks=range(len(methods)),yticklabels=[NAMES[m] for m in methods],xlabel='Required artifacts per project',xlim=(0,4.02),title='Accepted correct / unfinished (gray)');axs[1].invert_yaxis()
 save(fig,out,'quality_cost','Frozen strict-parser condition: real recorded transaction data, authored projects and changes, GPU-generated tool choices with deterministic guards. The parser follow-up diagnoses an interface confound. n=16 projects in eight monthly blocks, two generation replicas (32 continuations per method). Bars separate correct accepted artifacts from unfinished work. Error bars are paired-block bootstrap marginal intervals, not equivalence tests. The zero-inference pipeline selects parameters deterministically. Prose semantics are outside the structured correctness endpoint.')
 # B: Each paired monthly difference, never policy runs as independent units.
 fig,axs=plt.subplots(1,2,figsize=(8.4,3.5))
 for idx,right in enumerate(['broadcast','shared_state']):
  for col,metric in enumerate(['project_correct','calls']):
   d=next(c for c in comparisons if c['left']=='targeted' and c['right']==right and c['metric']==metric);v=np.array(d['differences']);v=v*100 if col==0 else v
   axs[col].scatter(v,np.arange(len(v))+(idx-.5)*.17,s=32,label='Targeted - '+NAMES[right],color=COLORS[right]);axs[col].axvline(0,color='#555555',lw=.8);axs[col].set_yticks(range(8));axs[col].set_yticklabels([x[5:] for x in d['blocks']]);axs[col].set_ylabel('2011 month block')
 axs[0].set_xlabel('Correct-project difference (percentage points)\nPositive favors targeted');axs[1].set_xlabel('Continuation-call difference\nNegative favors targeted');axs[0].legend(loc='lower left',bbox_to_anchor=(0,1.12),ncol=2,frameon=False,fontsize=9);axs[0].set_title('Paired quality');axs[1].set_title('Paired cost')
 save(fig,out,'paired_blocks','Paired outcomes on real-data project blocks, averaged across two constructed projects and two generation replicas within each month. One retailer, eight source blocks. No policy run or replica is an independent source organization. Zero and unfavorable differences remain visible.')
 # C: No interpolation in time; step paths indexed by actual completed calls.
 fig,ax=plt.subplots(figsize=(6.4,3.5))
 for m in METHODS:
  paths=[]
  for p in manifest['evaluation']:
   for rep in manifest['replicates']:
    er=[e for e in events if e['project_id']==p['id'] and int(e['rep'])==rep and e['method']==m]
    by={int(e['step']):float(e['V']) for e in er};last=by.get(0,3);curve=[]
    for t in range(9):last=by.get(t,last);curve.append(last)
    paths.append(curve)
  ax.step(range(9),np.mean(paths,axis=0),where='post',label=NAMES[m],color=COLORS[m],marker='o',ms=3)
 ax.axvline(0,color='#777777',ls=':');ax.set(xlabel='Completed agent continuations after user change',ylabel='Mean coordination error V (0 to 3)',title='Correctness requires uptake, not acknowledgment',ylim=(-.05,3.05));ax.legend(ncol=2);ax.xaxis.set_major_locator(MaxNLocator(integer=True));ax.grid(alpha=.16)
 save(fig,out,'coordination_error','Authored V combines contract violations, dependency inconsistencies and unfinished artifacts. The user change occurs at step zero. Each step is a completed GPU continuation, not human time. All 32 paired project replicas contribute at every step; a stopped run retains its final value. Decreasing V is descriptive and does not prove a contraction property or causal value over natural completion.')
 # D: Scope preservation, structural overhead, and format/feedback controls.
 fig,axs=plt.subplots(1,3,figsize=(8.4,3.9))
 for i,m in enumerate(METHODS):
  rr=[r for r in rows if r['method']==m];axs[0].bar(i,np.mean([r['unnecessary_modifications'] for r in rr]),color=COLORS[m]);axs[1].scatter([r['direct_recipients'] for r in rr],[r['wall_seconds'] for r in rr],s=18,alpha=.4,color=COLORS[m],label=NAMES[m])
 axs[0].set_xticks(range(4));axs[0].set_xticklabels([SHORT[m] for m in METHODS],rotation=30,ha='right');axs[0].set(ylabel='Unaffected artifacts rewritten / project',title='Unaffected work')
 axs[1].set(xlabel='Distinct direct recipients',ylabel='Measured adaptation time (seconds)',title='Measured recovery');axs[1].xaxis.set_major_locator(MaxNLocator(integer=True));axs[1].legend(fontsize=9)
 control=[r for r in secondary if r['method']=='global_packet'];tr=[r for r in rows if r['method']=='targeted' and r['rep']==0]
 for i,(rr,label) in enumerate([(tr,'Targeted'),(control,'Global\nsame packet')]):axs[2].bar(i,np.mean([r['project_correct'] for r in rr])*100,color=['#009E73','#56B4E9'][i]);axs[2].text(i,3,'%.2f calls'%np.mean([r['calls'] for r in rr]),ha='center',fontsize=9)
 axs[2].set(xticks=[0,1],xticklabels=['Targeted','Global\nsame packet'],ylim=(0,108),ylabel='Correct projects (%)',title='Matched packet control')
 save(fig,out,'scope_and_controls','Real-data ordinary adaptation, except the explicitly labeled matched-format control uses replica 0 only (16 constructed projects). Artifact identity includes proposed content and dependency hashes, so an unnecessary rewrite can count even if numbers remain equal. Recovery scatter shows measured orchestration plus tool and inference latency, not human review time. It is descriptive, not an effect of recipient count randomized independently.')
 # E: Stress and detail ablation shown separately from natural adaptation.
 stress=[r for r in secondary if r['stress']=='exception_generalization'];fig,axs=plt.subplots(1,2,figsize=(8.7,3.2));sm=METHODS+['targeted_no_feedback']
 for i,m in enumerate(sm):
  rr=[r for r in stress if r['method']==m];axs[0].bar(i,np.mean([r['project_correct'] for r in rr])*100,color=COLORS[m]);axs[1].bar(i,np.mean([r['calls'] for r in rr]),color=COLORS[m])
 for ax in axs:ax.set_xticks(range(len(sm)));ax.set_xticklabels([SHORT[m] for m in sm],rotation=30,ha='right')
 axs[0].set(ylabel='Correct projects (%)',ylim=(0,108),title='Matched exception corruption');axs[1].set(ylabel='LLM calls per continuation',title='Cost including bounded repair')
 save(fig,out,'stress_ablation','Secondary constructed disturbance on recorded-data artifacts: the same protected-appendix parameter and value corruption is introduced into every method’s initial state. Eight selected-in-advance projects, one per month, replica 0. Fresh method-specific GPU repairs. Removing detailed issue feedback preserves current requirements, allowed actions and the acceptance guard. These are not naturally observed retailer failures.')
 # F: Actual saved timeline and role validity for first qualifying examples.
 for label in ['favorable','tie','unfavorable']:
  if label not in examples:continue
  ex=examples[label];pid=ex['project_id'];fig,axs=plt.subplots(2,1,figsize=(8,4.8))
  for ax,method in zip(axs,['broadcast','targeted']):
   run=read(ART/'evaluation/frozen'/(pid+'_r0_'+method+'.json'));ev=[e for e in run['events'] if e['event'] in ['user_change','agent_continuation']];data=np.array([[int(e['artifacts'].get(role,{}).get('accepted',False)) for e in ev] for role in ROLES]);ax.imshow(data,aspect='auto',vmin=0,vmax=1,cmap=matplotlib.colors.ListedColormap(['#e9b59b','#b8decf']))
   for x,e in enumerate(ev):
    for y,role in enumerate(ROLES):
     a=e['artifacts'].get(role,{});project=next(p for p in manifest['evaluation'] if p['id']==pid);version=1 if a.get('consumed_contract_hash')==digest(contract(project,role,0)) else 2 if a.get('consumed_contract_hash')==digest(contract(project,role,1)) else '?';s='I'+str(version)+'/A'+str(a.get('revision','-'));ax.text(x,y,s,ha='center',va='center',fontsize=8)
   ax.set_yticks(range(4));ax.set_yticklabels(ROLES);ax.set_xticks(range(len(ev)));ax.set_xticklabels(['Change']+[e['extra'].get('role','') for e in ev[1:]],rotation=0);ax.set_title(NAMES[method]+' · '+pid)
  save(fig,out,'timeline_'+label,'Saved GPU adaptation on the first '+label+' example under the frozen numerical-ID rule: '+json.dumps(ex)+'. Columns show actual user-change/response events. Green means public checks passed; orange means unfinished/invalid. I denotes the original (1) or revised (2) consumed contract; unchanged contracts retain 1. A denotes artifact revision. These are not correctness votes or global conversation-turn numbers. Exact scope and instruction hashes are in the underlying trace. Events are simulated execution order, not human service times.')
 # G: Actual before/after aggregate and chart.
 ex=examples.get('favorable',examples.get('tie'));pid=ex['project_id'];p=next(p for p in manifest['evaluation'] if p['id']==pid);before=read(ART/'evaluation/frozen'/(pid+'_r0_initial.json'));after=read(ART/'evaluation/frozen'/(pid+'_r0_targeted.json'));fig,axs=plt.subplots(1,2,figsize=(8.4,3.6))
 for ax,run,epoch,title in zip(axs,[before,after],[0,1],['Original requirement','Revised main requirement']):
  points=run['artifacts'].get('chart',{}).get('points',[]);c=contract(p,'chart',epoch);scale=1e6 if c['metric']=='value_micro' else 1;ax.bar([x[0] for x in points],[x[1]/scale for x in points],color='#538eaa');ax.set(ylabel='Recorded line value (GBP)' if scale>1 else 'Recorded quantity (items)',title=title+'\n'+c['country']+'; '+c['start']+' to\n'+c['end']+' (exclusive)');ax.tick_params(axis='x',rotation=35)
 save(fig,out,'worked_transaction_example','Actual aggregate values from UCI Online Retail, displayed through the generated chart specifications before and after a constructed user change ('+pid+'). No repair success, accounting profit or measured user benefit is inferred. The complete SQL, structured claims and protected appendix appear in the walkthrough and saved trace.')
 # H: Controlled synthetic cases.
 syn=read(ART/'synthetic/rows.json');cases=list(dict.fromkeys(r['scenario'] for r in syn));fig,axs=plt.subplots(1,2,figsize=(8.4,4.2))
 for ax,metric,title in zip(axs,['accepted_correct','logical_response_opportunities'],['Accepted correct artifacts (out of four)','Controlled response opportunities']):
  mat=np.array([[next(r[metric] for r in syn if r['scenario']==c and r['method']==m) for m in METHODS] for c in cases]);im=ax.imshow(mat,aspect='auto',cmap='Blues',vmin=0,vmax=4 if metric=='accepted_correct' else 8)
  for y in range(len(cases)):
   for x in range(4):ax.text(x,y,str(int(mat[y,x])),ha='center',va='center',fontsize=10,color='white' if mat[y,x]>(2 if metric=='accepted_correct' else 4) else '#152c3c')
  ax.set_xticks(range(4));ax.set_xticklabels([SHORT[m] for m in METHODS],rotation=30,ha='right');ax.set_yticks(range(len(cases)));ax.set_yticklabels([c.replace('_',' ') for c in cases] if ax is axs[0] else ['']*len(cases),fontsize=9.5);ax.set_title(title)
 save(fig,out,'synthetic_boundaries','Entirely authored transaction rows, scopes, changes and controlled responses. Zero GPU calls and no human observations. These mechanism cases expose delayed notification, false acknowledgment, correlated wrong definitions and irrelevant forwarding. They do not estimate prevalence in real agent use.')
 print('figure families',len(list(out.glob('*.pdf'))));return out
if __name__=='__main__':
 figures()
 if (ART/'parser_followup/rows.json').exists():
  from .followup_analysis import analyze
  analyze()
