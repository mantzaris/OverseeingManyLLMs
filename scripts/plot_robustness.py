#!/usr/bin/env python3
"""Render frozen contrasts and individual bundles; no fit or data selection."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path('artifacts/stage6_robustness/analysis')
plt.rcParams.update({'font.size':9,'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
for cohort in ('fresh','post_hoc_stage5'):
    folder=root/cohort
    if not (folder/'summary.json').exists():continue
    figures=folder/'figures';figures.mkdir(exist_ok=True)
    rows=list(csv.DictReader((folder/'paired_comparisons.csv').open()))
    fig,axes=plt.subplots(1,2,figsize=(7.0,2.65),sharex=True)
    for ax,duration in zip(axes,(1,2)):
        group=[r for r in rows if int(r['review_duration'])==duration and r['comparison']=='search-greedy' and r['metric']=='operational_loss']
        for i,r in enumerate(group):
            mean=float(r['mean_difference']);lo=float(r['ci_low']);hi=float(r['ci_high'])
            ax.errorbar(mean,i,xerr=[[max(0,mean-lo)],[max(0,hi-mean)]],fmt='o',color='#1b4965',capsize=3)
        ax.set_yticks(range(len(group)));ax.set_yticklabels([{'reference':'Correction','approve_block':'Approve/block','complexity_time':'Complexity time'}[r['variant']] for r in group]);ax.axvline(0,color='.6',lw=.8)
        ax.set_title('Base review: %d tick%s'%(duration,'' if duration==1 else 's'));ax.set_xlabel('Search minus greedy loss');ax.invert_yaxis()
    fig.tight_layout()
    for ext in ('pdf','png'):fig.savefig(figures/('paired_loss.'+ext),dpi=220,bbox_inches='tight')
    plt.close(fig)
    rows=list(csv.DictReader((folder/'bundle_differences.csv').open()))
    group=[r for r in rows if r['variant']=='approve_block' and r['review_duration']=='2' and r['comparison']=='search-greedy' and r['metric']=='operational_loss']
    fig,ax=plt.subplots(figsize=(6.8,2.4));values=[float(r['difference']) for r in group]
    ax.bar(range(len(group)),values,color=['#2a7f62' if v<0 else '#b44b45' if v>0 else '.6' for v in values]);ax.axhline(0,color='.5',lw=.8)
    ax.set_xticks(range(len(group)));ax.set_xticklabels([r['bundle_id'].rsplit('_',1)[1] for r in group],fontsize=8)
    ax.set_xlabel('Source bundle (three replicates averaged)');ax.set_ylabel('Search minus greedy loss');fig.tight_layout()
    for ext in ('pdf','png'):fig.savefig(figures/('primary_bundle_differences.'+ext),dpi=220,bbox_inches='tight')
    plt.close(fig)
