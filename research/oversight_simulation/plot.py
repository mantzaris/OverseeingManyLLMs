"""Vector figures from saved simulation tables. No human performance plots."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from research.oversight_workflow.common import read,write
from .inputs import OUT,POLICIES

COLORS={'Q':'#666666','G':'#D55E00','Q-source-aware':'#0072B2','Q-sticky':'#009E73','M':'#CC79A7'}
LABELS={'Q':'FIFO Q','G':'Grouped G','Q-source-aware':'Source-aware Q','Q-sticky':'Sticky Q','M':'Manual M'}
plt.rcParams.update({'font.size':11,'axes.titlesize':12,'axes.labelsize':11,'legend.fontsize':9,'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':130})
FOOT='SIMULATION | 6 real TAT-QA sources; saved drafts | 32 Monte Carlo seeds; no participants'
CAPTIONS={}


def save(fig,name,caption):
    dest=OUT/'figures';dest.mkdir(exist_ok=True)
    fig.text(.5,.01,FOOT,ha='center',fontsize=7)
    fig.tight_layout(rect=[0,.045,1,.97])
    for ext in ('pdf','svg','png'):fig.savefig(dest/(name+'.'+ext),dpi=240)
    plt.close(fig);CAPTIONS[name]=dict(record_kind='computational_simulation',caption=caption,inputs='Saved numerical results from real-source tasks and actual drafts; all plotted timing and reviewer outcomes simulated')


def main():
    d=read(OUT/'design.json');configs=pd.DataFrame(d['configs']).set_index('id')
    means=pd.read_csv(OUT/'analysis/cell_means.csv');pairs=pd.read_csv(OUT/'analysis/paired_differences.csv')
    def value(cid,p,metric):return float(means[(means.config==cid)&(means.policy==p)&(means.metric==metric)]['mean'].iloc[0])
    def delta(cid,a,b,metric='correct'):
        return pairs[(pairs.config==cid)&(pairs.contrast==a+'_minus_'+b)&(pairs.metric==metric)].iloc[0]
    def ids(family):return configs[configs.family==family]
    baseline=next(c['id'] for c in d['configs'] if c['family']=='original' and c['orientation']==25 and c['effectiveness']=='high' and c['memory']=='long')
    # Demand: identical offered sets within every comparison; distinct-goal unions.
    fig,axes=plt.subplots(1,3,figsize=(10,3.3),sharey=True)
    for ax,h in zip(axes,(270,540,900)):
        cs=ids('demand');cs=cs[cs.horizon==h].sort_values('offered')
        for p in POLICIES:
            x=cs.offered.to_numpy();y=[];err=[]
            for cid,n in zip(cs.index,x):
                row=means[(means.config==cid)&(means.policy==p)&(means.metric=='correct')].iloc[0]
                y.append(row['mean']/n);err.append(1.96*row['mc_se']/n)
            ax.errorbar(x,y,yerr=err,label=LABELS[p],color=COLORS[p],marker='o',ms=3,lw=1,capsize=2)
        ax.set(title='%g-minute review budget'%(h/60),xlabel='Distinct questions offered',xticks=[6,12,24,36],ylim=(-.02,1.05))
    axes[0].set_ylabel('Correct releases / all offered');axes[-1].legend(loc='upper right',fontsize=9)
    save(fig,'demand','Simulated correct-release fractions by offered demand and review capacity. Higher-effectiveness reviewer, orientation coefficient S=25 s and long memory. Error bars are 95% normal Monte Carlo intervals over 32 paired seed blocks, averaged across three reused packet rotations. They do not represent human-population uncertainty.')
    # Reference outcome composition.
    fig,ax=plt.subplots(figsize=(6.7,3.6));bottom=np.zeros(5)
    for metric,label,color in [('correct','Correct release','#009E73'),('incorrect','Incorrect release','#D55E00'),('unfinished','Unfinished','#D4D4D4')]:
        vals=np.array([value(baseline,p,metric) for p in POLICIES]);ax.bar(range(5),vals,bottom=bottom,color=color,label=label)
        for i,v in enumerate(vals):
            if v>.45:ax.text(i,bottom[i]+v/2,'%.2f'%v,ha='center',va='center',fontsize=8)
        bottom+=vals
    ax.set(xticks=range(5),xticklabels=[LABELS[p] for p in POLICIES],ylabel='Questions per 12 offered',ylim=(0,14),title='Nine-minute reference setting: simulated outcomes')
    ax.legend(loc='upper center',ncol=3)
    save(fig,'outcomes','Simulated mean correct, incorrect and unfinished questions in the original 12-question / 540-second schedule, orientation coefficient S=25 s, higher effectiveness and long memory. All offered work remains in the denominator. Drafts are actual generations; review and repairs are modeled. Rejection and unreleased approval remain unfinished.')
    # Zero-centered adverse regions visible against both relevant queue controls.
    fig,axes=plt.subplots(2,2,figsize=(7.8,5.6),sharex=True,sharey=True)
    mats=[]
    for comparator in ('Q','Q-source-aware'):
        for mem in ('short','long'):
            z=np.empty((3,4))
            for iy,e in enumerate(('ideal','high','limited')):
                for ix,o in enumerate((0,5,25,75)):
                    cid=next(c['id'] for c in d['configs'] if c['family']=='original' and c['orientation']==o and c['effectiveness']==e and c['memory']==mem)
                    z[iy,ix]=delta(cid,'G',comparator)['mean']
            mats.append(z)
    limit=max(.1,max(abs(z).max() for z in mats))
    for index,(ax,z) in enumerate(zip(axes.flat,mats)):
        im=ax.imshow(z,cmap='RdBu',vmin=-limit,vmax=limit,aspect='auto')
        comparator=('Q','Q-source-aware')[index//2];mem=('short','long')[index%2]
        ax.set(title='G minus %s\n%s memory'%(LABELS[comparator],mem),xticks=range(4),xticklabels=[0,5,25,75],yticks=range(3),yticklabels=['Ideal','Higher','Limited'])
        for (i,j),v in np.ndenumerate(z):ax.text(j,i,'%+.2f'%v,ha='center',va='center',fontsize=8,color='white' if abs(v)>.6*limit else 'black')
        if index//2:ax.set_xlabel('Orientation coefficient S (s)')
    fig.subplots_adjust(left=.09,right=.82,bottom=.12,top=.92,hspace=.42,wspace=.22)
    cax=fig.add_axes([.86,.20,.025,.60]);fig.colorbar(im,cax=cax,label='Additional correct releases (G minus queue)')
    # tight_layout with a shared colorbar is avoided in this one figure.
    dest=OUT/'figures';dest.mkdir(exist_ok=True);fig.text(.5,.01,FOOT,ha='center',fontsize=7)

    for ext in ('pdf','svg','png'):fig.savefig(dest/('orientation_effectiveness.'+ext),dpi=240)
    plt.close(fig);CAPTIONS['orientation_effectiveness']=dict(record_kind='computational_simulation',caption='Simulated G-minus-queue differences in correct releases across the original workload grid. Positive blue favors G; negative red favors the comparator. Shared symmetric color scale preserves adverse regions. Reviewer rates and memory parameters are assumptions; source inputs and initial drafts are fixed real-data evidence. All six sources have size factor 0.75, so unfamiliar orientation is 0.75 times S.')
    # Direct interface control across every declared cell.
    fig,ax=plt.subplots(figsize=(5.9,4.4));markers=['o','s','^','D','v','P']
    for (family,cs),marker in zip(configs.groupby('family',sort=False),markers):
        x=[value(cid,'Q-source-aware','correct')/c['offered'] for cid,c in cs.iterrows()]
        y=[value(cid,'G','correct')/c['offered'] for cid,c in cs.iterrows()]
        ax.scatter(x,y,label=family.replace('_',' '),marker=marker,s=28,alpha=.72)
    ax.plot([0,1],[0,1],color='black',ls='--',lw=1)
    ax.set(xlabel='Source-aware Q: correct releases / offered',ylabel='Grouped G: correct releases / offered',xlim=(0,1.02),ylim=(0,1.02),title='Computational interface control; all 66 cells')
    ax.legend(loc='upper left',fontsize=7)
    save(fig,'source_aware_control','Simulated cell means for G and the queue with identical bounded source-aware navigation. Each point is a parameter setting, not an independent source or person. The diagonal is a tie. At zero group overhead, equality follows mechanically from the model and is checked against saved outputs.')
    # Full time accounting, not continuous reading measurements.
    fig,ax=plt.subplots(figsize=(7,3.6));bottom=np.zeros(5)
    phases=[('orientation','Source orientation','#56B4E9'),('question','Question','#E69F00'),('verification','Verification','#0072B2'),('construction','Construction','#009E73'),('interaction','Decision','#999999'),('release','Release','#CC79A7'),('grouping','Group interaction','#D55E00'),('idle','Idle','#EEEEEE')]
    for name,label,color in phases:
        vals=np.array([value(baseline,p,'time_'+name) for p in POLICIES]);ax.bar(range(5),vals,bottom=bottom,label=label,color=color);bottom+=vals
    ax.set(xticks=range(5),xticklabels=[LABELS[p] for p in POLICIES],ylabel='Simulated seconds (budget 540)',ylim=(0,650),title='Reference setting: charged phase time including partial work')
    ax.legend(ncol=4,loc='upper center',fontsize=7)
    save(fig,'time_decomposition','Simulated time components in the reference setting. The components plus idle sum to the 540-second budget; an interrupted last review is charged only through cutoff. These are assigned model phases, not observed reading or interaction time. Different policies may reach different task subsets.')
    # Common carryover risk applies to consecutive sources in every method.
    fig,axes=plt.subplots(1,3,figsize=(9.7,3.4),sharey=True)
    for ax,mem in zip(axes,('short','long','persistent')):
        cs=ids('carryover');cs=cs[cs.memory==mem].sort_values('carryover')
        for p in POLICIES:ax.plot(cs.carryover.to_numpy(),[value(cid,p,'correct') for cid in cs.index],color=COLORS[p],marker='o',ms=3,label=LABELS[p])
        ax.set(title=mem.title()+' source memory',xlabel='Assumed carryover-error probability',xticks=[0,.08,.2],ylim=(0,12))
    axes[0].set_ylabel('Simulated correct releases / 12');axes[-1].legend(fontsize=9)
    save(fig,'memory_carryover','Simulated correctness when a same-source predecessor can spoil an otherwise correct answer. The hazard is shared by every policy, including manual work, rather than attached only to G. Memory persistence and probabilities are unvalidated assumptions. Lines connect only declared settings.')
    fig,axes=plt.subplots(1,2,figsize=(7.2,3.7),sharex=True,sharey=True);zs=[]
    for p in ('Q','G'):
        z=np.empty((3,3))
        for i,v in enumerate((8,18,40)):
            for j,m in enumerate((20,45,90)):
                cid=next(c['id'] for c in d['configs'] if c['family']=='task_cost' and c['verify_seconds']==v and c['manual_seconds']==m)
                z[i,j]=delta(cid,p,'M')['mean']
        zs.append(z)
    lim=max(abs(z).max() for z in zs)
    for ax,z,p in zip(axes,zs,('Q','G')):
        ax.imshow(z,cmap='RdBu',vmin=-lim,vmax=lim,aspect='auto');ax.set(title=LABELS[p]+' minus Manual M',xlabel='Assumed manual construction (s)',xticks=range(3),xticklabels=[20,45,90],yticks=range(3),yticklabels=[8,18,40])
        for (i,j),v in np.ndenumerate(z):ax.text(j,i,'%+.2f'%v,ha='center',va='center',color='white' if abs(v)>.65*lim else 'black')
    axes[0].set_ylabel('Assumed draft verification (s)')
    save(fig,'draft_assistance','Simulated assistance boundaries: additional correct releases relative to manual work across verification/manual-construction costs. Positive values favor assistance; negative values favor manual. Correction cost stays 45 seconds. These conditional outcomes use the low-quality saved drafts and assumed reviewer effectiveness, not measured human assistance effects.')
    # Selected timelines. Colors show modeled correctness; orientation is hatched.
    traces=read(OUT/'analysis/example_traces.json.gz');selection=read(OUT/'analysis/example_selection.json')
    for label,ident in selection.items():
        if label=='tie':continue
        ts=[t for t in traces if all(t[k]==ident[k] for k in ('config','rotation','seed'))]
        cs=configs.loc[ident['config']];h=cs.horizon
        fig,ax=plt.subplots(figsize=(9,3.8));srcmap={}
        for row,p in enumerate(('Q','G','Q-source-aware')):
            t=next(t for t in ts if t['policy']==p);out={x['id']:x for x in t['observed_outcomes']}
            release_at={payload['id']:at for at,action,payload in t['commands'] if action=='release'}
            for r in t['reviews']:
                sid=r['source_id'];srcmap.setdefault(sid,'S'+str(len(srcmap)+1))
                # A deferred attempt must not inherit a later attempt's release.
                observed=out.get(r['id']) if release_at.get(r['id'])==r['end'] else None
                color='#BBBBBB' if observed is None else '#009E73' if observed['correct'] else '#D55E00'
                right=min(h,r['end']);ax.barh(row,right-r['start'],left=r['start'],height=.5,color=color,edgecolor='white',lw=.7)
                if right-r['start']>16:ax.text((right+r['start'])/2,row,srcmap[sid],ha='center',va='center',fontsize=9)
                for name,a,b in r['segments']:
                    if name in ('orientation','grouping') and a<h:
                        ax.barh(row,min(h,b)-a,left=a,height=.5,facecolor='none',hatch='////' if name=='orientation' else 'xxxx',edgecolor='#333333',lw=.4)
            # Arrival ticks from actual constructed schedule.
            from .inputs import workload
            items=workload(read(OUT/'inputs.json'),dict(cs),ident['rotation'])
            ax.plot([x['arrival'] for x in items if x['arrival']<=h],[row+.36]*sum(x['arrival']<=h for x in items),marker='|',ls='',color='black',ms=4)
        ax.axvline(h,color='black',ls='--');ax.set(yticks=range(3),yticklabels=[LABELS[p] for p in ('Q','G','Q-source-aware')],xlabel='Simulated seconds from offered workload',xlim=(0,h+5),ylim=(2.65,-.9),title='%s paired example: %s; rotation %s; seed %s'%(label.title(),ident['config'],ident['rotation'],ident['seed']))
        ax.legend(handles=[Patch(color='#009E73',label='Correct release'),Patch(color='#D55E00',label='Incorrect release'),Patch(color='#BBBBBB',label='Unreleased'),Patch(facecolor='white',hatch='////',label='Orientation'),Patch(facecolor='white',hatch='xxxx',label='Group overhead')],loc='upper center',bbox_to_anchor=(.5,1.01),ncol=5,fontsize=9)
        save(fig,'timeline_'+label,'Simulated paired timeline selected by first qualifying declaration-order configuration, rotation and seed, not effect size. Black ticks show constructed arrivals; hatching shows assigned orientation/group overhead. S labels refer to actual source identities. Green/red reflect modeled correct/incorrect released versions; gray is unfinished. All tasks remain in accounting. Selection: '+json.dumps(ident))
    # Matplotlib 3.1 emits trailing blanks in SVG paths; normalize whitespace
    # without changing coordinates or rerendering any numerical result.
    for path in (OUT/'figures').glob('*.svg'):
        path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
    write(OUT/'figures/captions.json',CAPTIONS)
    print('Wrote',len(CAPTIONS),'simulation figures in PDF/SVG/PNG')


if __name__=='__main__':main()
