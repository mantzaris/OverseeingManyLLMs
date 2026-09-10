#!/usr/bin/env python3
"""Publication-size figures from saved retail outcomes; no inference."""
import csv
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.retail.analysis import paired_interval
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(sys.argv[1] if len(sys.argv)>1 else 'artifacts/stage5_practical/batches/evaluation/analysis')
out=root/'figures';out.mkdir(exist_ok=True)
def read(name):return list(csv.DictReader((root/name).open()))
rows=read('episodes.csv');policies=['no_review','fcfs','edf','uncertainty','greedy','search']
labels=['No review','FCFS','EDF','Risk first','Greedy','Search']
plt.rcParams.update({'font.size':8,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42})
def save(fig,name):
    fig.tight_layout()
    for suffix in ['png','pdf']:fig.savefig(out/(name+'.'+suffix),dpi=220,bbox_inches='tight')
    plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(7.2,2.8),sharey=True)
for ax,duration in zip(axes,[1,2]):
    for i,policy in enumerate(policies):
        group=[r for r in rows if int(r['review_duration'])==duration and r['policy']==policy]
        n=len(group);service=sum(float(r['service_failure_loss']) for r in group)/n;wrong=sum(float(r['wrong_transaction_loss']) for r in group)/n
        by_bundle=[sum(float(r['operational_loss']) for r in group if r['bundle_id']==b)/sum(r['bundle_id']==b for r in group) for b in sorted({r['bundle_id'] for r in group})]
        low,high=paired_interval(by_bundle);mean=service+wrong
        ax.bar(i,service,color='#4477AA',label='Unresolved service' if i==0 else None)
        ax.bar(i,wrong,bottom=service,color='#CC6677',label='Wrong processing' if i==0 else None)
        ax.errorbar(i,mean,yerr=[[max(0,mean-low)],[max(0,high-mean)]],color='black',capsize=2,linewidth=.7)
    ax.set_xticks(range(6));ax.set_xticklabels(labels,rotation=40,ha='right');ax.set_title('Review duration = %d'%duration)
axes[0].set_ylabel('Mean operational loss per bundle');axes[1].legend(fontsize=7,frameon=False)
save(fig,'policy_loss_components')

paired=read('paired_bundle_differences.csv');fig,ax=plt.subplots(figsize=(7.0,2.6))
for offset,other,color,marker in [(-.12,'greedy','#4477AA','o'),(.12,'edf','#CC6677','s')]:
    group=sorted([r for r in paired if r['review_duration']=='2' and r['comparator']==other],key=lambda r:r['bundle_id'])
    ax.scatter([i+offset for i in range(len(group))],[float(r['mean_search_minus_other']) for r in group],s=18,label='Search − '+other.upper(),color=color,marker=marker)
ax.axhline(0,color='.4',linewidth=.7);ax.set_xlabel('Source-disjoint scenario bundle (ascending ID)')
ax.set_ylabel('Paired loss difference\n(three-replicate mean)');ax.legend(frameon=False,ncol=2,fontsize=7)
save(fig,'paired_loss')

bins=[r for r in read('risk_bins.csv') if int(r['examples'])];variation=read('generation_variability.csv')
fig,axes=plt.subplots(1,2,figsize=(7.1,2.8))
for i,r in enumerate(bins):
    axes[0].plot([i,i],[float(r['predicted_probability']),float(r['observed_error_rate'])],color='.7',linewidth=1)
    axes[0].scatter(i,float(r['predicted_probability']),marker='s',color='#4477AA',label='Frozen prediction' if i==0 else None)
    axes[0].scatter(i,float(r['observed_error_rate']),marker='o',color='#CC6677',label='Observed error rate' if i==0 else None)
    axes[0].annotate('n='+r['examples'],(i,max(float(r['predicted_probability']),float(r['observed_error_rate']))),xytext=(0,6),textcoords='offset points',ha='center',fontsize=6)
axes[0].set_xticks(range(len(bins)));axes[0].set_xticklabels([r['family'].replace('return_exchange','return/exch')+'\n'+('flagged' if r['uncertain']=='True' else 'high/no flag') for r in bins],fontsize=6)
axes[0].set_ylim(0,min(1,max([float(r['observed_error_rate']) for r in bins]+[.2])+.15));axes[0].set_ylabel('Error probability');axes[0].legend(fontsize=6,frameon=False)
counts=[sum(int(r['successful_tasks'])==i for r in variation) for i in range(4)]
axes[1].bar(range(4),counts,color='#228833');axes[1].set_xticks(range(4));axes[1].set_xlabel('Correct preparations among 3 replicates');axes[1].set_ylabel('Distinct evaluation source cases')
save(fig,'risk_and_generation_variability')
