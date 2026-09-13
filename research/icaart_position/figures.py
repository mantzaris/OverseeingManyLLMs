"""Four print-size vector figure groups, derived only from frozen saved results."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / 'artifacts/oversight_simulation'
ART = ROOT / 'artifacts/icaart_position/figures'
PDF = ROOT / 'paper/icaart_position/figures'
C = pd.read_csv(OLD / 'analysis/cell_means.csv')
P = pd.read_csv(OLD / 'analysis/paired_differences.csv')
D = json.loads((OLD / 'design.json').read_text())['configs']
POLICIES = ['Q','G','Q-source-aware','Q-sticky','M']
LABELS = ['FIFO (Q)','Grouping (G)','Bounded source queue','Sticky source queue','Manual (M)']
COLORS = ['#555555','#A64B82','#0072B2','#009E73','#D58B00']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.titlesize':9,'axes.labelsize':8.5,
    'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':8,'pdf.fonttype':42,'ps.fonttype':42,
    'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':240,'svg.hashsalt':'icaart-position-fixed'})


def row(config, policy, metric='correct'):
    return C[(C.config==config)&(C.policy==policy)&(C.metric==metric)].iloc[0]


def pair(config, contrast, metric='correct'):
    return P[(P.config==config)&(P.contrast==contrast)&(P.metric==metric)].iloc[0]


def save(fig, name):
    PDF.mkdir(parents=True, exist_ok=True); ART.mkdir(parents=True, exist_ok=True)
    fig.savefig(PDF/(name+'.pdf'), metadata={'CreationDate':None,'ModDate':None})
    fig.savefig(ART/(name+'.png'))
    fig.savefig(ART/(name+'.svg'), metadata={'Date':None})
    p=ART/(name+'.svg');p.write_text('\n'.join(s.rstrip() for s in p.read_text().splitlines())+'\n')
    plt.close(fig)


def workflow():
    fig,ax=plt.subplots(figsize=(6.22,2.50));fig.subplots_adjust(left=.015,right=.99,bottom=.015,top=.98)
    ax.set(xlim=(-1,101),ylim=(0,42));ax.axis('off')
    def box(x,y,w,h,text,color='#EFF4F7'):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.3,rounding_size=1',fc=color,ec='#546673',lw=.8))
        ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=8.3,linespacing=1.4)
    def arrow(a,b,label=None,offset=(0,0),style='-'):
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=9,lw=.85,color='#46515A',linestyle=style))
        if label:ax.text((a[0]+b[0])/2+offset[0],(a[1]+b[1])/2+offset[1],label,ha='center',va='center',fontsize=7.4)
    box(0,23,17,13,'Concurrent\ntask workers\nA • B • C')
    box(23,23,20,13,'Visible queue\nPending + deferred\nAll work counted')
    box(49,23,23,13,'Active review\nSource + draft v3\nSeparate decision','#E6F2EF')
    box(79,23,20,13,'Approve v3\nthen release v3','#F4EAF1')
    arrow((17,30),(23,30));arrow((43,30),(49,30));arrow((72,30),(79,30))
    ax.text(20,39,'Arrivals continue; the active source and version remain fixed',ha='left',fontsize=8.4,weight='bold')
    box(24,2,20,12,'Defer / resume\nKeep notes, source\nand prior draft','#FFF4DD')
    box(49,2,23,12,'Optional source session\nUp to 3 questions\nNo shared approval')
    box(79,2,20,12,'Revision v4\nReview again\nv3 approval retained','#F4EAF1')
    arrow((53,23),(42,14),'defer',offset=(-4,0));arrow((34,14),(34,23),'resume',offset=(-6,0))
    arrow((60,14),(60,23));arrow((89,23),(89,14))
    ax.text(1,12,'Full original\ntable + text\navailable',fontsize=8,va='top',color='#46515A')
    save(fig,'workflow')


def reference():
    fig,(a,b)=plt.subplots(1,2,figsize=(6.22,2.55),gridspec_kw={'width_ratios':[1.52,1]})
    fig.subplots_adjust(left=.25,right=.985,bottom=.22,top=.85,wspace=.6)
    y=np.arange(5);left=np.zeros(5)
    for metric,label,color in [('correct','Correct','#009E73'),('incorrect','Incorrect','#D55E00'),('unfinished','Unfinished','#D8DEE3')]:
        vals=np.array([row('015_o25_high_long',p,metric)['mean'] for p in POLICIES]);a.barh(y,vals,left=left,height=.62,color=color,label=label)
        if metric=='correct':
            for k,v in enumerate(vals):a.text(v/2,k,'%.2f'%v,color='white',ha='center',va='center',fontsize=8,weight='bold')
        left+=vals
    a.set(yticks=y,yticklabels=LABELS,xlim=(0,12),xticks=[0,4,8,12],xlabel='Answers per 12 offered');a.invert_yaxis()
    a.set_title('(a) Outcomes',loc='left');fig.legend(*a.get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.54,1.015),ncol=3,frameon=False,columnspacing=1.3,handlelength=1.2)
    others=['Q','Q-source-aware','Q-sticky','M'];short=['FIFO','Bounded','Sticky','Manual']
    for i,p in enumerate(others):
        r=pair('015_o25_high_long','G_minus_'+p)
        b.errorbar(r['mean'],i,xerr=[[r['mean']-r.mc_low],[r.mc_high-r['mean']]],fmt='o',color=COLORS[1],capsize=2,ms=4)
    b.axvline(0,color='#888888',lw=.8);b.set(yticks=np.arange(4),yticklabels=short,xlim=(-.53,.42),xticks=[-.4,0,.4],xlabel='G minus comparator');b.invert_yaxis();b.set_title('(b) Correct-release differences',loc='right',fontsize=8.3)
    save(fig,'reference')


def heat(ax, values, lim, columns, rows, title, xlabel):
    im=ax.imshow(values,cmap='PuOr',vmin=-lim,vmax=lim,aspect='auto')
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            v=values[i,j];ax.text(j,i,('%+.2f'%v).replace('+0.00','0.00'),ha='center',va='center',fontsize=8,color='white' if abs(v)>.65*lim else '#202020')
    ax.set(xticks=range(len(columns)),xticklabels=columns,yticks=range(len(rows)),yticklabels=rows,xlabel=xlabel)
    ax.tick_params(length=0);ax.set_title(title,loc='left',pad=7)
    return im


def orientation():
    fig,axes=plt.subplots(2,2,figsize=(6.22,3.55));fig.subplots_adjust(left=.13,right=.93,bottom=.16,top=.9,hspace=.72,wspace=.38)
    for i,other in enumerate(['Q','Q-source-aware']):
        for j,mem in enumerate(['short','long']):
            vals=np.array([[pair(next(c['id'] for c in D if c['family']=='original' and c['orientation']==s and c['effectiveness']==e and c['memory']==mem),'G_minus_'+other)['mean'] for s in [0,5,25,75]] for e in ['ideal','high','limited']])
            im=heat(axes[i,j],vals,1.5,[0,5,25,75],['Ideal','Higher','Limited'],('G − FIFO' if i==0 else 'G − bounded queue')+'; '+mem+' memory','Orientation coefficient S (s)')
    cb=fig.colorbar(im,ax=axes.ravel().tolist(),orientation='horizontal',fraction=.04,pad=.19,aspect=35)
    cb.set_label('Difference in correct releases per 12 offered (positive favors G)')
    save(fig,'orientation')


def tradeoffs():
    fig,axes=plt.subplots(1,3,figsize=(6.22,2.85));fig.subplots_adjust(left=.08,right=.98,bottom=.29,top=.78,wspace=.53)
    a,b,c=axes
    for pol,color,label,mark in zip(POLICIES,COLORS,['Q','G','Bounded','Sticky','M'],['o','s','^','D','v']):
        rs=[row(next(x['id'] for x in D if x['family']=='demand' and x['offered']==n and x['horizon']==540),pol) for n in [6,12,24,36]]
        a.errorbar([6,12,24,36],[100*r['mean']/n for r,n in zip(rs,[6,12,24,36])],yerr=[100*1.96*r.mc_se/n for r,n in zip(rs,[6,12,24,36])],color=color,marker=mark,ms=3,lw=.9,label=label)
    a.set(xlabel='Offered questions',ylabel='Correct releases (%)',xticks=[6,12,24,36],ylim=(0,100));a.set_title('(a) Fixed 9-minute budget',loc='left')
    fig.legend(*a.get_legend_handles_labels(),ncol=5,loc='upper center',bbox_to_anchor=(.5,1.015),frameon=False,handlelength=1,columnspacing=.8)
    for metric,color,label in [('correct','#009E73','Correct'),('incorrect','#D55E00','Incorrect')]:
        rr=[pair('0%d_long_c%d'%(60+i,v),'G_minus_Q',metric) for i,v in enumerate([0,8,20])]
        b.errorbar([0,8,20],[r['mean'] for r in rr],yerr=[1.96*r.mc_se for r in rr],color=color,marker='o',ms=3,lw=1,capsize=2,label=label)
    b.axhline(0,color='#777777',lw=.6);b.set(xticks=[0,8,20],xlabel='Carryover chance (%)',ylabel='G − Q releases',ylim=(-1.05,.85));b.set_title('(b) Carryover risk',loc='left');b.legend(frameon=False,loc='lower left',fontsize=7)
    vals=np.array([[pair(next(d['id'] for d in D if d['family']=='task_cost' and d['verify_seconds']==v and d['manual_seconds']==m),'Q_minus_M')['mean'] for m in [20,45,90]] for v in [8,18,40]])
    im=heat(c,vals,4.5,[20,45,90],[8,18,40],'(c) Q − M correct','Manual cost (s)');c.set_ylabel('Verification cost (s)')
    c.text(.5,-.43,'Cell: difference per\n12 offered',transform=c.transAxes,ha='center',va='top',fontsize=7.6)
    save(fig,'tradeoffs')


if __name__=='__main__':
    workflow();reference();orientation();tradeoffs()
    (ART/'metadata.json').write_text(json.dumps(dict(record_kind='publication_figures',numerical_sources=['artifacts/oversight_simulation/analysis/cell_means.csv','artifacts/oversight_simulation/analysis/paired_differences.csv'],figures=['workflow','reference','orientation','tradeoffs'],units='Simulated releases and assumed seconds; no human observations',uncertainty='95% normal Monte Carlo intervals over 32 seed blocks; 3 rotations averaged within seed',figure_1='Protocol schematic, not an observed interaction or screenshot'),indent=2)+'\n')
