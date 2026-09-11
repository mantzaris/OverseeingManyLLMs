#!/usr/bin/env python3
"""Publication figures exclusively from frozen sensor summaries and saved outputs."""
import csv,gzip,json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
ROOT=Path('artifacts/stage7_empirical');OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':9,'axes.titlesize':10,'axes.labelsize':9,'legend.fontsize':8,'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':300})
COLORS=['#777777','#0072B2','#E69F00','#009E73','#CC79A7','#D55E00'];POL=['no_review','fcfs','edf','uncertainty','greedy','search'];NAMES=['None','FCFS','EDF','Risk','Greedy','Search']
def read(name):return list(csv.DictReader((ROOT/'analysis'/name).open()))
def save(name,fig):
    fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight');fig.savefig(OUT/(name+'.png'),bbox_inches='tight',dpi=300);plt.close(fig)
summary=read('policy_summary.csv');pair=read('paired.csv');jobs=read('diagnoses.csv');cases=json.loads((ROOT/'cases.json').read_text());ev=[c for c in cases if c['split']=='evaluation']
def primary(r):return r['weights']=='heterogeneous' and r['capacity']=='1' and r['duration']=='2'
# First source-order evaluation window; all annotation is analysis-only.
c=ev[0];j=next(j for j in jobs if j['case_id']==c['case_id']);x=np.arange(60)
fig,axes=plt.subplots(2,1,figsize=(6.6,3.8),sharex=True,constrained_layout=True)
for name,label,col in [('sat','Supply',COLORS[5]),('mixed','Mixed',COLORS[1]),('cool_sp','Cooling setpoint',COLORS[2]),('return','Return',COLORS[3])]:axes[0].plot(x,c['signals'][name],label=label,color=col,lw=1.5)
axes[0].set_ylabel('Temperature (deg F)');axes[0].legend(ncol=4,loc='upper center',bbox_to_anchor=(.5,1.24));axes[0].set_title('Recorded window; annotation: '+c['source_label'].replace('_',' '),pad=24)
for name,label,col in [('cool_valve','Cooling valve',COLORS[1]),('heat_valve','Heating valve',COLORS[5]),('damper','Outdoor damper',COLORS[3])]:axes[1].plot(x,c['signals'][name],label=label,color=col)
axes[1].set_ylabel('Control command (fraction)');axes[1].set_xlabel('Minutes after '+c['public']['window_start']+'; one-minute samples');axes[1].legend(ncol=3)
fig.suptitle('Generated proposal: '+j['proposal'].replace('_',' ')+' | review: '+j['review'].replace('_',' '),fontsize=10)
save('measured_example',fig)
fig,axes=plt.subplots(2,2,figsize=(7.0,4.6),constrained_layout=True)
for col,reviewer in enumerate(('model','ideal')):
    rows=[next(r for r in summary if primary(r) and r['reviewer']==reviewer and r['policy']==p) for p in POL]
    for row,metric,lo,hi,label in [(0,'mean_loss','ci_low','ci_high','Modeled loss / experimental day'),(1,'correct_rate','correct_low','correct_high','Correct diagnosis fraction')]:
        y=np.array([float(r[metric]) for r in rows]);low=np.array([float(r[lo]) for r in rows]);high=np.array([float(r[hi]) for r in rows])
        axes[row,col].bar(np.arange(6),y,color=COLORS,width=.65);axes[row,col].errorbar(np.arange(6),y,yerr=[y-low,high-y],fmt='none',ecolor='black',capsize=2,lw=.8)
        axes[row,col].set_xticks(np.arange(6));axes[row,col].set_xticklabels(NAMES,rotation=30,ha='right');axes[row,col].set_ylabel(label)
        if row==1:axes[row,col].set_ylim(0,1.05)
    axes[0,col].set_title('Saved model review' if reviewer=='model' else 'Ideal review upper bound')
save('policy_performance',fig)
diff=read('bundle_differences.csv');fig,axes=plt.subplots(1,2,figsize=(6.8,2.8),sharey=True,constrained_layout=True)
for ax,reviewer in zip(axes,('model','ideal')):
    rows=[r for r in diff if primary(r) and r['reviewer']==reviewer and r['comparison']=='search-greedy'];y=[float(r['difference']) for r in rows]
    ax.axhline(0,color='#555555',lw=.8);ax.scatter(range(len(y)),y,c=[COLORS[1] if v<0 else COLORS[5] if v>0 else '#777777' for v in y],s=30)
    stat=next(r for r in pair if primary(r) and r['reviewer']==reviewer and r['comparison']=='search-greedy')
    ax.set_title(reviewer+' review; W/T/L '+ '/'.join(stat[k] for k in ('wins','ties','losses')));ax.set_xlabel('Experimental day (source order)')
axes[0].set_ylabel('Search minus greedy loss\nNegative favors search');save('paired_differences',fig)
fig,axes=plt.subplots(1,2,figsize=(6.8,2.7),constrained_layout=True);arrays=[]
for reviewer in ('model','ideal'):
    arrays.append(np.array([[float(next(r for r in pair if r['reviewer']==reviewer and r['weights']=='heterogeneous' and r['capacity']==str(cap) and r['duration']==str(dur) and r['comparison']=='search-greedy')['mean_difference']) for dur in (1,2,3)] for cap in (1,2)]))
limit=max(1,max(abs(a).max() for a in arrays))
for ax,reviewer,a in zip(axes,('model','ideal'),arrays):
    im=ax.imshow(a,cmap='RdBu_r',norm=TwoSlopeNorm(0,-limit,limit));ax.set_xticks(range(3));ax.set_xticklabels([1,2,3]);ax.set_yticks(range(2));ax.set_yticklabels([1,2]);ax.set_xlabel('Assumed service duration (ticks)');ax.set_ylabel('Reviewer slots');ax.set_title(reviewer+' review')
    for i in range(2):
        for k in range(3):ax.text(k,i,'%.2f'%a[i,k],ha='center',va='center',color='white' if abs(a[i,k])>.65*limit else 'black')
fig.colorbar(im,ax=axes,label='Mean search minus greedy loss',shrink=.85);save('capacity_sensitivity',fig)
fig,axes=plt.subplots(1,2,figsize=(6.8,2.8),constrained_layout=True)
trans=[sum(int(j[k]) for j in jobs) for k in ('correction','unresolved_wrong','preserved_correct','harm','abstention')]
axes[0].barh(['Wrong -> correct','Wrong unresolved','Correct preserved','Correct -> wrong','Review abstains'],trans,color=[COLORS[3],COLORS[0],COLORS[1],COLORS[5],COLORS[2]])
for i,n in enumerate(trans):axes[0].text(n+.15,i,str(n),va='center')
axes[0].set_xlim(0,max(trans)+5);axes[0].set_xlabel('Saved proposal/review pairs (n=54)');axes[0].set_title('Generated reviewer transitions')
axes[1].plot([0,1],[0,1],'--',color='gray')
for label in sorted({j['proposal'] for j in jobs}):
    xs=[j for j in jobs if j['proposal']==label];p=np.mean([float(j['risk']) for j in xs]);err=np.mean([1-int(j['initial_correct']) for j in xs]);axes[1].scatter(p,err,s=30+len(xs)*3,label=label.replace('_',' ')+' (n='+str(len(xs))+')')
axes[1].set(xlim=(-.05,1.05),ylim=(-.05,1.05),xlabel='Frozen predicted error probability',ylabel='Observed initial-error fraction',title='Development-fitted risk');axes[1].legend(fontsize=7,loc='best');save('reviewer_risk',fig)
with gzip.open(ROOT/'policy_traces.jsonl.gz','rt') as f:traces=[json.loads(s) for s in f]
examples=[]
for reviewer in ('model','ideal'):
    rows=[r for r in diff if primary(r) and r['reviewer']==reviewer and r['comparison']=='search-greedy']
    for kind,test in [('benefit',lambda v:v<0),('tie',lambda v:v==0),('unfavorable',lambda v:v>0)]:
        row=next((r for r in rows if test(float(r['difference']))),None)
        if not row:examples.append(dict(reviewer=reviewer,kind=kind,available=False));continue
        run=row['run_id'];fig,axes=plt.subplots(2,1,figsize=(6.4,3.5),sharex=True,constrained_layout=True)
        for ax,policy in zip(axes,('greedy','search')):
            t=next(t for t in traces if t['run_id']==run and t['reviewer']==reviewer and t['weights']=='heterogeneous' and t['duration']==2 and t['capacity']==1 and t['policy']==policy)
            for i,job in enumerate(t['jobs']):
                ax.plot([0,job['cutoff']],[i,i],color='gray',lw=.8);ax.scatter([0],[i],marker='o',color='black',s=20);ax.scatter([job['cutoff']],[i],marker='x',color=COLORS[5],s=40)
                start=next((e for e in t['events'] if e['event']=='review_started' and e['case_id']==job['case_id']),None)
                if start:ax.barh(i,start['finish']-start['tick'],left=start['tick'],height=.4,color=COLORS[1]);ax.scatter([start['finish']],[i],marker='s',color=COLORS[3],s=18)
            ax.set_yticks(range(3));ax.set_yticklabels(['Window '+str(i+1) for i in range(3)]);ax.set_title(policy+'; loss '+str(t['loss']));ax.set_xlim(-.2,6.4)
        axes[-1].set_xlabel('Simulated ticks; circle = arrival, bar = review, square = completion, x = cutoff')
        name='queue_'+reviewer+'_'+kind;save(name,fig);examples.append(dict(reviewer=reviewer,kind=kind,available=True,run_id=run,difference=float(row['difference']),figure=name))
(ROOT/'examples.json').write_text(json.dumps(examples,indent=2)+'\n')
print('Generated vector PDFs and 300 dpi PNG previews:',len(list(OUT.glob('*.pdf'))))
