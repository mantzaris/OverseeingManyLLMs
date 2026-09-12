"""All plotted numbers come from saved analysis tables or recorded examples."""
import csv,json,textwrap
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from .common import ART,read,write
OUT=ART/'figures'
NAMES={'individual':'Individual','execute':'Execution only','reattempt':'Reattempt','verify':'Source verification','coarse':'Coarse transfer','patch':'Constrained patch','no_applicability':'No scope check'}
COLORS={'individual':'#666666','execute':'#56B4E9','reattempt':'#E69F00','verify':'#0072B2','coarse':'#CC79A7','patch':'#009E73','no_applicability':'#7D5A50'}
def rows(v,name):
 with (ART/f'analysis_{v}/{name}.csv').open() as f:return list(csv.DictReader(f))
def val(r,k):return float(r[k])
def save(fig,name):
 OUT.mkdir(parents=True,exist_ok=True);fig.tight_layout()
 for ext in ['pdf','svg','png']:
  p=OUT/(name+'.'+ext);fig.savefig(p,dpi=220,bbox_inches='tight',metadata={'Creator':'Saved-output correction applicability analysis'} if ext=='pdf' else None)
  if ext=='svg':p.write_text('\n'.join(x.rstrip() for x in p.read_text().splitlines())+'\n')
 plt.close(fig)
def plot():
 plt.rcParams.update({'font.size':10,'axes.titlesize':12,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','font.family':'DejaVu Sans','savefig.facecolor':'white'})
 captions={}
 fig,axes=plt.subplots(1,2,figsize=(10.2,3.7),sharex=True,sharey=True)
 for ax,v in zip(axes,['v1','v2']):
  comparisons={r['second']:r for r in rows(v,'comparisons')};paired=rows(v,'paired')
  for y,m in enumerate(['individual','verify','reattempt','coarse']):
   r=comparisons[m];xs=[100*float(x['difference']) for x in paired if x['second']==m];jitter=np.linspace(-.11,.11,len(xs));ax.scatter(xs,y+jitter,s=18,color=COLORS[m],alpha=.65)
   ax.errorbar(100*val(r,'mean'),y,xerr=[[100*(val(r,'mean')-val(r,'low'))],[100*(val(r,'high')-val(r,'mean'))]],fmt='D',color='black',capsize=4,markersize=5)
   ax.text(.98,y+.2,f"W/T/L {r['wins']}/{r['ties']}/{r['losses']}",ha='right',fontsize=8,transform=ax.get_yaxis_transform())
  ax.axvline(0,color='#666666',lw=.8);ax.set_title(v+' development');ax.set_xlabel('Patch minus control accuracy (percentage points)');ax.set_yticks(range(4));ax.set_yticklabels([NAMES[m] for m in ['individual','verify','reattempt','coarse']]);ax.set_xlim(-37,37);ax.set_ylim(3.6,-.55);ax.grid(axis='x',alpha=.15)
 save(fig,'paired_contexts');captions['paired_contexts']='Generated answers scored against TAT-QA annotations on the same 12 previously inspected development source contexts per version. Dots are context differences; diamonds and bars show means and descriptive 95% paired bootstrap intervals (2000 resamples). Positive favors patching. The two versions are not independent replicas. Degenerate zero intervals reflect identical retained outputs, not population equivalence.'
 fig,axes=plt.subplots(1,2,figsize=(11,4.4),sharey=True)
 for ax,v in zip(axes,['v1','v2']):
  rs=rows(v,'summary');x=np.arange(len(rs));initial=[val(r,'initial_em') for r in rs];direct=[val(r,'local_gain') for r in rs];helps=[val(r,'helpful_events') for r in rs];harms=[val(r,'harmful_events') for r in rs]
  ax.bar(x,initial,color='#9CAFB7',label='Initially correct');ax.bar(x,direct,bottom=initial,color='#0072B2',label='Direct inspection gains');base=np.array(initial)+direct;ax.bar(x,helps,bottom=base,color='#009E73',label='Helpful revision events');ax.bar(x,[-h for h in harms],bottom=base+helps,color='none',edgecolor='#D55E00',hatch='////',label='Harmful revision events')
  ax.scatter(x,[val(r,'em') for r in rs],color='black',s=22,zorder=4,label='Final correct');ax.set_xticks(x);ax.set_xticklabels([NAMES[r['method']] for r in rs],rotation=38,ha='right');ax.set_title(v+' development');ax.set_ylim(0,51);ax.set_ylabel('Correct answers / 72');ax.grid(axis='y',alpha=.15)
 handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,ncol=3,loc='upper center',bbox_to_anchor=(.5,1.12),frameon=False,fontsize=8);save(fig,'correctness_decomposition');captions['correctness_decomposition']='Generated answer EM decomposed into common initial correctness, simulated direct annotation corrections, and helpful/harmful revision events. Black markers give final counts. Telescoping identities are verified for every episode. These event counts are distinct from final never-inspected changes reported separately.'
 ds=read(ART/'diagnostics/summary.json');fig,axes=plt.subplots(1,2,figsize=(10.5,3.8))
 fields=['questions','executable','public_contract','supported_patches','accepted_revisions'];labels=['All questions','Executable records','Public contracts','Reusable patches','Committed transfers']
 for i,d in enumerate(ds):axes[0].barh(np.arange(5)+(.15 if i else -.15),[d[k] for k in fields],height=.28,label=d['revision'],color=['#56B4E9','#0072B2'][i]);
 axes[0].set_yticks(range(5));axes[0].set_yticklabels(labels);axes[0].invert_yaxis();axes[0].set_xlabel('Recorded count (units shown in labels)');axes[0].legend();axes[0].set_title('Representation and transfer coverage')
 rs=rows('v2','summary');x=np.arange(len(rs));axes[1].barh(x-.16,[val(r,'sibling_fixed') for r in rs],height=.3,color='#009E73',label='Newly correct');axes[1].barh(x+.16,[-val(r,'sibling_harmed') for r in rs],height=.3,color='#D55E00',label='Made wrong');axes[1].set_yticks(x);axes[1].set_yticklabels([NAMES[r['method']] for r in rs]);axes[1].invert_yaxis();axes[1].axvline(0,color='#444444',lw=.8);axes[1].set_title('v2: final never-inspected outputs');axes[1].set_xlabel('Distinct answers harmed (-) or repaired (+)');axes[1].legend(fontsize=8);save(fig,'coverage_and_transfer');captions['coverage_and_transfer']='Generated representation coverage and final never-inspected changes on development data. There are 72 questions, 24 acquired donor disclosures, and 108 attempted recipient decisions per patch method. Different funnel rows have these different denominators. The ablation also made zero commits. The 48 never-inspected answers per version are dependent within 12 source contexts.'
 fig,axes=plt.subplots(1,2,figsize=(10.5,4.4),sharey=True)
 for ax,v in zip(axes,['v1','v2']):
  rs=rows(v,'summary');x=np.arange(len(rs))
  for y,r in enumerate(rs):
   m=r['method'];common=0 if m=='individual' else val(r,'extraction_attempts');extra=val(r,'attempts');ax.barh(y,common,color='#CBD7DC');ax.barh(y,extra,left=common,color=COLORS[m]);ax.text(common+extra+2,y,f"{int(val(r,'em'))}/72",va='center',fontsize=9)
  ax.set_yticks(x);ax.set_yticklabels([NAMES[r['method']] for r in rs]);ax.invert_yaxis();ax.set_title(v+' development');ax.set_xlim(0,215);ax.set_xlabel('Actual generation attempts for standalone method')
 axes[0].legend(handles=[Patch(facecolor='#CBD7DC',label='Common representation extraction'),Patch(facecolor='#0072B2',label='Method continuations; label = correct')],loc='lower right',fontsize=8);save(fig,'correctness_cost');captions['correctness_cost']='Measured method costs and annotated correctness on development sources. Common historical initial-answer generation is a sunk cost and excluded. Representation extraction is charged once per standalone method that needs it; individual correction does not need it. Colors show extra continuations. Actual stage totals deduplicate genuinely identical requests across methods. Inspection cost is two disclosures in every episode.'
 with (ART/'synthetic/results.csv').open() as f:sr=list(csv.DictReader(f))
 cases=list(dict.fromkeys(r['case'] for r in sr));fig,ax=plt.subplots(figsize=(9.2,5.8));matrix=[]
 for case in cases:
  matrix.append([np.mean([r['correct']=='True' for r in sr if r['case']==case and r['method']==m]) for m in ['patch','no_applicability']])
 ax.imshow(matrix,vmin=0,vmax=1,cmap=matplotlib.colors.ListedColormap(['#F2C9A9','#ADD8E4']),aspect='auto')
 for y,case in enumerate(cases):
  for x,m in enumerate(['patch','no_applicability']):
   rs=[r for r in sr if r['case']==case and r['method']==m];commits=sum(r['accepted']=='True' for r in rs);correct=sum(r['correct']=='True' for r in rs);ax.text(x,y,f'{correct}/32 correct; {commits} commits',ha='center',va='center',fontsize=9)
 ax.set_xticks([0,1]);ax.set_xticklabels(['Constrained patch','Recipient checks removed']);ax.set_yticks(range(len(cases)));ax.set_yticklabels([x.replace('_',' ') for x in cases]);ax.set_title('Constructed boundary cases, not empirical prevalence');save(fig,'synthetic_boundaries');captions['synthetic_boundaries']='Authored sources, dependencies and initial errors, with 32 bounded output perturbation seeds per case. Rows are 11 mechanism cases, not independent real-world samples. Blue denotes correct final answer and scale; orange denotes incorrect. The final row retains a harmful commit that passes structural checks: a donor with denominator one does not identify the general percentage-change formula.'
 fig,axes=plt.subplots(1,2,figsize=(9,4.3));files=['shared_operand_order','local_fact_wrong_period']
 for ax,name in zip(axes,files):
  d=read(ART/'synthetic'/name/'patch.json');e=d['event'];p=d['patch'];ax.axis('off');table=ax.table(cellText=d['source']['table'],loc='upper center',cellLoc='center',colWidths=[.42,.19,.19,.19]);table.auto_set_font_size(False);table.set_fontsize(10.5);table.scale(1,1.5)
  txt='Recipient: '+d['question']['question']+'\n\nOld computation: '+d['before']['rep']['expression']+' on '+', '.join(d['before']['rep']['refs'])+'\nAcquired correction: '+str(p['feedback']['answer'])+' '+p['feedback']['scale']+'\nPatch type: '+p['kind']+'\n'
  if e['candidate']:txt+='Candidate: '+e['candidate']['rep']['expression']+' on '+', '.join(e['candidate']['rep']['refs'])+' = '+str(e['candidate']['answer'][0])+'\n'
  txt+='Decision: '+('COMMIT' if e['accepted'] else 'RETAIN ORIGINAL')+'\nReason: '+('; '.join(e['reasons']) or 'Declared checks passed')+'\nFinal answer: '+str(e['after']['answer'][0])+' '+e['after']['scale'];ax.text(0,.67,'\n'.join(textwrap.fill(x,50) for x in txt.split('\n')),va='top',fontsize=11);ax.set_title('Reusable operand-order patch' if name==files[0] else 'Wrong-period binding rejected')
 save(fig,'worked_boundaries');captions['worked_boundaries']='Constructed mechanism examples using the expense pattern identified in the historical TAT-QA failure audit. Values are millions, while the controlled wrong expressions and patch applicability cases are authored. Left: an operation template can change across periods while retaining recipient operands. Right: replacing the 2018 input with the 2019 input would produce the wrong comparison; the period check retains the original 273. No natural committed patch was observed in either pilot.'
 write(OUT/'captions.json',captions);print('Rendered',len(captions),'figures in PDF/SVG/PNG')
if __name__=='__main__':plot()
