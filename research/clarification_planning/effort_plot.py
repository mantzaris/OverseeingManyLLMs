"""Quality-demand tradeoff including the explicitly secondary stronger baseline."""
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .common import ART
from .analyze import rows,interval,SEED,RESAMPLES
from .plot import save,COLORS,LABELS

def run(root=None):
    global ART
    if root is not None:
        from pathlib import Path
        ART=Path(root)
    data=rows(ART/'evaluation/episodes.csv')+rows(ART/'completion_audit/episodes.csv')
    ids=sorted({r['id'] for r in data});ind=np.random.default_rng(SEED).integers(0,len(ids),(RESAMPLES,len(ids)))
    methods=['full_history','semantic_memory','one_step','completion','depth2','minimum_completion']
    colors=dict(COLORS,minimum_completion='#7B6940');labels=dict(LABELS,minimum_completion='Minimum sufficient*')
    fig,axes=plt.subplots(1,2,figsize=(7.5,4.0))
    offsets={'full_history':(4,-15),'semantic_memory':(-77,5),'one_step':(-58,-19),'completion':(-65,-20),'depth2':(-26,-24),'minimum_completion':(-53,9)}
    for method in methods:
        grouped=defaultdict(list)
        for r in data:
            if r['method']==method and r['budget']==2 and r['error_weight']==4:grouped[r['id']].append(r)
        x=[np.mean([r['questions'] for r in grouped[id]]) for id in ids];xm,xl,xh=interval(x,ind)
        for ax,metric in zip(axes,['correct','loss']):
            y=[np.mean([r[metric] for r in grouped[id]]) for id in ids];ym,yl,yh=interval(y,ind)
            ax.errorbar(xm,ym,xerr=[[xm-xl],[xh-xm]],yerr=[[ym-yl],[yh-ym]],fmt={'full_history':'s','semantic_memory':'o','one_step':'^','completion':'v','depth2':'P','minimum_completion':'D'}[method],ms=5,color=colors[method],alpha=.8,capsize=2,lw=1,label=labels[method])
            xytext=offsets[method]
            if metric=='loss':xytext={'full_history':(4,8),'semantic_memory':(-90,4),'one_step':(-50,10),'completion':(-75,-17),'depth2':(-45,-20),'minimum_completion':(-83,-32)}[method]

        for ax in axes:ax.set_xlabel('Additional answers per dialogue');ax.grid(alpha=.15);ax.set_xlim(-.1,2.25)
    axes[0].set_ylabel('Correct shortlists per dialogue');axes[1].set_ylabel('Declared loss per dialogue')
    axes[0].set_title('More complete work is better');axes[1].set_title('Lower modeled loss is better')
    fig.suptitle('Empirical budget two: quality and supervisory demand are separate outcomes',fontsize=10)
    fig.text(.5,.005,'* Minimum sufficient completion is a post-freeze comparator audit. Intervals resample 48 dialogue means.',ha='center',fontsize=8)
    fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',bbox_to_anchor=(.5,.055),ncol=3,fontsize=8.5,frameon=False)
    fig.tight_layout(rect=(0,.23,1,.91));save(fig,ART/'figures','quality_effort_audit')
if __name__=='__main__':run()
