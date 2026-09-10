#!/usr/bin/env python3
"""Publication figures from audited saved episodes; no inference or outcome selection."""
import argparse
from collections import defaultdict
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from overseeing.research_analysis import numeric_records,paired_interval
from overseeing.io import write_csv,write_json

POLICIES=('fcfs','uncertainty','myopic','greedy','edf','delay')
LABELS=dict(fcfs='FCFS',uncertainty='Uncertainty',myopic='Myopic',greedy='Greedy',edf='EDF',delay='Search')
COLORS=dict(zip(POLICIES,('#7f7f7f','#cc79a7','#e69f00','#d55e00','#009e73','#0072b2')))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.labelsize':9,'axes.titlesize':10,'pdf.fonttype':42,'ps.fonttype':42,'savefig.dpi':300})

def interval(rows,metric):
    rows=sorted(rows,key=lambda r:r['seed']);values=[metric(r) for r in rows]
    mean=float(np.mean(values));lo,hi=paired_interval(values,[r['seed'] for r in rows])
    return mean,mean-lo,hi-mean

def finish(fig,path,caption):
    fig.tight_layout()
    for suffix in ('png','pdf','svg'):fig.savefig(str(path)+'.'+suffix,bbox_inches='tight')
    path.with_suffix('.txt').write_text(caption+'\n');plt.close(fig)

def main(root,batch,label):
    root=Path(root);summary=root/'summaries'/label;out=summary/'figures';out.mkdir(parents=True,exist_ok=True)
    rows=[r for r in numeric_records(root/'batches'/batch/'analysis/episodes.csv') if r['status']=='completed']
    core=[r for r in rows if r['phase'] in ('replication','capacity') and r['risk']=='frozen']
    fig,axs=plt.subplots(2,2,figsize=(8.2,5.5),sharex=True)
    for wi,workload in enumerate(('original','competition')):
        for di,duration in enumerate((1,2)):
            ax=axs[wi,di]
            for i,policy in enumerate(POLICIES):
                rs=[r for r in core if r['workload']==workload and r['review_ticks']==duration and r['policy']==policy]
                if rs:
                    m,l,u=interval(rs,lambda r:r['total_loss']);ax.errorbar(i,m,yerr=[[l],[u]],fmt='o',capsize=3,color=COLORS[policy])
            ax.set_title('{}; {}-tick reviews'.format(workload.capitalize(),duration));ax.set_ylabel('Mean loss / scenario')
            ax.set_xticks(range(6));ax.set_xticklabels([LABELS[p] for p in POLICIES],rotation=25,ha='right');ax.grid(axis='y',alpha=.2);ax.set_ylim(bottom=-.1)
    finish(fig,out/'policy_losses','Frozen estimator; 64 paired scenarios per workload. Dots are means, bars are 95% percentile intervals from 2,000 scenario bootstrap resamples. Panels use separate workload distributions; intervals are not multiplicity-adjusted.')
    fig,axs=plt.subplots(2,2,figsize=(7.5,5.5))
    for di,duration in enumerate((1,2)):
        for mi,metric in enumerate((lambda r:r['total_loss']/r['jobs'],lambda r:r['incorrect_jobs']/r['jobs'])):
            ax=axs[mi,di]
            for policy in ('fcfs','edf','greedy','delay'):
                values=[];low=[];high=[]
                for agents in (3,6):
                    rs=[r for r in core if r['workload']=='larger' and r['agents']==agents and r['review_ticks']==duration and r['policy']==policy]
                    m,l,u=interval(rs,metric);values.append(m);low.append(l);high.append(u)
                ax.errorbar([3,6],values,yerr=[low,high],marker='o',capsize=2,label=LABELS[policy],color=COLORS[policy])
            ax.set_xticks([3,6]);ax.set_xlabel('Agents sharing one supervisor');ax.set_title('{}-tick reviews'.format(duration));ax.grid(alpha=.2)
            ax.set_ylabel('Mean loss / job' if mi==0 else 'Incorrect closure fraction');ax.set_ylim(bottom=0)
    axs[0,0].legend(ncol=2,fontsize=8)
    finish(fig,out/'capacity','Larger workload, frozen estimator, 32 nested paired scenarios. Three jobs per agent; first three agents have matching exogenous jobs across team sizes. Means and 95% scenario bootstrap intervals. Lines connect conditions, not temporal trajectories.')
    matched=[r for r in rows if r['phase'] in ('replication','risk_ablation') and r['policy'] in ('greedy','delay') and r['seed']<(10032 if r['workload']=='original' else 11032)]
    predictions=numeric_records(root/'batches'/batch/'analysis/predictions.csv')
    pg=defaultdict(list)
    for p in predictions:pg[p['run_id']].append(p)
    tables=[]
    for r in matched:
        ps=pg[r['run_id']];r['own_brier']=sum(p['brier_'+r['risk']] for p in ps)/len(ps)
    fig,axs=plt.subplots(2,2,figsize=(7.5,5.5))
    for wi,workload in enumerate(('original','competition')):
        for policy in ('greedy','delay'):
            loss=[];brier=[];lo=[];hi=[]
            for risk in ('frozen','pooled','analytical'):
                for duration in (1,2):
                    rs=[r for r in matched if r['workload']==workload and r['policy']==policy and r['risk']==risk and r['review_ticks']==duration]
                    m,l,u=interval(rs,lambda r:r['total_loss']);bm,bl,bu=interval(rs,lambda r:r['own_brier'])
                    tables.append(dict(workload=workload,policy=policy,risk=risk,review_ticks=duration,scenarios=len(rs),mean_loss=m,ci_low=m-l,ci_high=m+u,mean_brier=bm,brier_ci_low=bm-bl,brier_ci_high=bm+bu))
                    if duration==2:loss.append(m);lo.append(l);hi.append(u);brier.append(bm)
            axs[wi,0].errorbar(range(3),loss,yerr=[lo,hi],marker='o',capsize=2,color=COLORS[policy],label=LABELS[policy])
            axs[wi,1].plot(range(3),brier,'o-',color=COLORS[policy],label=LABELS[policy])
        for col in (0,1):
            axs[wi,col].set_xticks(range(3));axs[wi,col].set_xticklabels(['Agreement','Pooled','Analytical']);axs[wi,col].grid(alpha=.2);axs[wi,col].set_title(workload.capitalize()+'; 2-tick reviews')
        axs[wi,0].set_ylabel('Mean loss / scenario');axs[wi,1].set_ylabel('Brier on own trajectories')
    axs[0,0].legend()
    write_csv(summary/'risk_matched_outcomes.csv',tables)
    finish(fig,out/'risk_estimates','First 32 declared scenarios per workload, matched across all three estimators. Frozen reference rows are reused from replication. Each alternative estimator uses fresh policy rollouts. Loss bars are 95% scenario bootstrap intervals. Brier scores concern each condition\'s observed trajectories; pointwise alternatives on the same outputs are in prediction_quality.csv. Analytical risk knows the synthetic likelihood model.')
    fig,axs=plt.subplots(2,2,figsize=(7.5,5.5))
    branch=[r for r in rows if r['phase']=='objective_evaluation']
    for wi,workload in enumerate(('competition','larger')):
        for di,duration in enumerate((1,2)):
            ax=axs[wi,di];xs=[];ys=[]
            for penalty in (0,4,8):
                rs=[r for r in branch if r['workload']==workload and r['review_ticks']==duration and r['closure_penalty']==penalty]
                x=np.mean([r['incorrect_jobs'] for r in rs]);y=np.mean([r['total_loss'] for r in rs]);xs.append(x);ys.append(y)
                ax.annotate('λ='+str(penalty),(x,y),xytext=(4,4+penalty),textcoords='offset points',fontsize=8)
            ax.plot(xs,ys,'o-',color=COLORS['delay']);ax.set_xlabel('Mean incorrect closures / scenario');ax.set_ylabel('Mean original loss / scenario');ax.set_title('{}; {}-tick reviews'.format(workload.capitalize(),duration));ax.grid(alpha=.2);ax.margins(.25)
    finish(fig,out/'objective_tradeoff','Exploratory extension: 16 new paired scenarios per workload, competition with three agents and larger workload with six. Search uses λ=0,4,8; axes always show original maintenance loss and incorrect closures separately. Lines follow the declared grid and do not assert a Pareto frontier. Scenario-paired intervals and common-objective comparisons are in paired_comparisons.csv.')
    write_json(out/'manifest.json',dict(source_batch=batch,source_label=label,figures=['policy_losses','capacity','risk_estimates','objective_tradeoff'],matplotlib=matplotlib.__version__,numpy=np.__version__,no_new_inference=True))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',default='artifacts/stage4_research');parser.add_argument('--batch',default='evaluation');parser.add_argument('--label',default='evaluation');args=parser.parse_args();main(args.root,args.batch,args.label)
