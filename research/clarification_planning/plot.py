"""Programmatic vector figures and high-resolution previews from saved evidence."""
import argparse
import gzip
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
from matplotlib.colors import Normalize
from .common import ART,read
from .analyze import rows

COLORS={'depth2':'#007F7B','one_step':'#C26B22','semantic_memory':'#556A8A','completion':'#955DA5','full_history':'#343A40','depth3':'#519A39',
        'depth1':'#C26B22','no_scope':'#B04D5D','request_specific':'#9C8A49','generic2':'#589CB2'}
LABELS={'depth2':'Two-step planner','one_step':'One-step VoI','depth1':'One-step VoI','semantic_memory':'Semantic memory','completion':'Fewest answers',
        'full_history':'Full history','depth3':'Three-step planner','no_scope':'No scope questions','request_specific':'No shared answers','generic2':'Generic two-step'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,'axes.labelsize':9,'legend.fontsize':8,
    'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42,'savefig.dpi':240,'axes.axisbelow':True})


def save(fig,out,name):
    fig.savefig(out/(name+'.pdf'),bbox_inches='tight');fig.savefig(out/(name+'.svg'),bbox_inches='tight');fig.savefig(out/(name+'.png'),bbox_inches='tight',dpi=240);plt.close(fig)
    svg=out/(name+'.svg');svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')

def line(ax,data,metric,methods,error=4):
    budgets=[0,1,2,4,6,'unlimited'];x=np.arange(6)
    for method in methods:
        group=[next(r for r in data if r['method']==method and r['metric']==metric and r['budget']==b and r['error_weight']==error) for b in budgets]
        y=np.array([r['mean'] for r in group]);lo=[r['lo'] for r in group];hi=[r['hi'] for r in group]
        ax.plot(x,y,'o-',color=COLORS[method],label=LABELS[method],ms=3,lw=1.5);ax.fill_between(x,lo,hi,color=COLORS[method],alpha=.10)
    ax.set_xticks(x);ax.set_xticklabels(['0','1','2','4','6','All']);ax.set_xlabel('Additional response budget');ax.grid(axis='y',alpha=.18)

def dependency(out):
    fig,ax=plt.subplots(figsize=(7.3,3.5));ax.set_xlim(0,10);ax.set_ylim(0,4);ax.axis('off')
    nodes={'q1':(.4,3.1,'Format?'),'q2':(.4,1.8,'Accessibility?'),'scope':(.4,.35,'Applies to partner?'),
           'a':(5.9,3.2,'Implementation'),'b':(5.9,2.2,'Test plan'),'c':(5.9,1.2,'Publishing guide'),'d':(5.9,.15,'Partner export')}
    for key,(x,y,label) in nodes.items():
        ax.add_patch(FancyBboxPatch((x,y),2.35,.52,boxstyle='round,pad=.08',facecolor='#E7F2F0' if key in ['q1','q2','scope'] else '#F0F2F6',edgecolor='#698287'))
        ax.text(x+1.175,y+.26,label,ha='center',va='center',fontsize=9)
    for q in ['q1','q2']:
        for task in ['a','b','c']:
            x,y,_=nodes[q];xx,yy,_=nodes[task]
            ax.add_patch(FancyArrowPatch((x+2.4,y+.26),(xx-.1,yy+.26),arrowstyle='->',mutation_scale=9,color='#197D79',alpha=.65))
    ax.annotate('Both answers required',xy=(4.2,2.45),ha='center',bbox=dict(facecolor='white',edgecolor='none',pad=3),fontsize=9)
    ax.add_patch(FancyArrowPatch((2.85,.61),(5.75,.41),arrowstyle='->',mutation_scale=9,color='#B16A25',linestyle='--'))
    ax.text(4.4,.02,'A separate applicability decision;\nno automatic answer transfer',ha='center',va='bottom',fontsize=8,color='#8C5D22')
    ax.set_title('Constructed mechanism example: shared context does not grant shared authority',loc='left',pad=12)
    save(fig,out,'dependency_example')

def performance(out,data):
    methods=['semantic_memory','full_history','one_step','completion','depth2']
    fig,axes=plt.subplots(1,2,figsize=(7.4,3));line(axes[0],data,'correct',methods);line(axes[1],data,'loss',methods)
    axes[0].set_ylabel('Correct shortlists per dialogue');axes[1].set_ylabel('Declared terminal loss per dialogue')
    axes[0].set_title('Source-grounded task correctness');axes[1].set_title('Simulated wrong / unfinished loss')
    handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=3,bbox_to_anchor=(.5,.005),frameon=False)
    fig.tight_layout(rect=(0,.18,1,1));save(fig,out,'empirical_quality_budget')
    fig,axes=plt.subplots(1,3,figsize=(8.2,3.35))
    for ax,metric,label in zip(axes,['incorrect','unfinished','questions'],['Incorrect releases / dialogue','Unfinished tasks / dialogue','Additional answers / dialogue']):
        line(ax,data,metric,['semantic_memory','one_step','completion','depth2']);ax.set_ylabel(label)
    fig.suptitle('Empirical components: generated interpretation, simulated clarification',fontsize=10)
    fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',ncol=4,bbox_to_anchor=(.5,.005),frameon=False)
    fig.tight_layout(rect=(0,.13,1,.88));save(fig,out,'empirical_components')


def synthetic_map(out,root):
    d=rows(root/'analysis/synthetic_valid_paired.csv');fig,axes=plt.subplots(1,2,figsize=(7.3,3.3))
    for ax,b,base in zip(axes,[2,4],['depth1','completion']):
        mat=np.array([[next(r['loss_difference'] for r in d if r['family']=='grid_%s_arity_%d'%(o,a) and r['budget']==b and r['baseline']==base) for o in ['none','one','full']] for a in [1,2,3]])
        lim=max(1,np.abs(mat).max());im=ax.imshow(mat,cmap='BrBG_r',norm=Normalize(vmin=-lim,vmax=lim))
        for y in range(3):
            for x in range(3):ax.text(x,y,'%+.2f'%mat[y,x],ha='center',va='center',color='white' if abs(mat[y,x])>lim*.6 else '#202020')
        ax.set_xticks(range(3));ax.set_xticklabels(['None','One','All']);ax.set_yticks(range(3));ax.set_yticklabels(['1','2','3']);ax.set_xlabel('Decision factors shared across tasks');ax.set_ylabel('Required factors per task')
        ax.set_title('Planner minus %s\nBudget %d'%(LABELS[base],b));fig.colorbar(im,ax=ax,fraction=.046,pad=.04,label='Loss difference; negative favors planner')
    fig.suptitle('Synthetic overlap and complementarity: 12 sampled intents per cell',fontsize=10);fig.tight_layout(rect=(0,0,1,.87));save(fig,out,'synthetic_overlap_map')


def paired(out,root):
    d=rows(root/'analysis/individual.csv');fig,axes=plt.subplots(1,3,figsize=(8.2,3.1))
    for ax,base in zip(axes,['one_step','semantic_memory','completion']):
        v=[r['loss_difference'] for r in d if r['baseline']==base and r['budget']==2 and r['error_weight']==4];v=sorted(v)
        ax.axhline(0,color='#777777',lw=.8);ax.bar(range(len(v)),v,color=[COLORS['depth2'] if x<0 else '#BD6946' if x>0 else '#AAAAAA' for x in v],width=.9)
        ax.set_title('vs '+LABELS[base]);ax.set_xlabel('Dialogue rank');ax.set_ylabel('Paired loss difference')
        ax.set_xlabel('Dialogue rank\nWins / ties / losses: %d / %d / %d'%(sum(x<0 for x in v),sum(x==0 for x in v),sum(x>0 for x in v)),fontsize=8)
    fig.suptitle('Empirical primary budget: two answers; replicate means stay within dialogue',fontsize=10);fig.tight_layout(rect=(0,0,1,.88));save(fig,out,'paired_differences')


def ablations(out,root):
    d=rows(root/'analysis/synthetic_valid_summary.csv');families=['complementary','wrong_sharing','noisy_response','unresolved_response']
    methods=['depth1','completion','depth2','depth3','no_scope','request_specific'];fig,axes=plt.subplots(1,4,figsize=(8.6,3))
    for ax,family in zip(axes,families):
        vals=[next(r['loss'] for r in d if r['family']==family and r['method']==m and r['budget']==2) for m in methods]
        ax.bar(range(len(methods)),vals,color=[COLORS[m] for m in methods]);ax.set_xticks(range(len(methods)));ax.set_xticklabels(['1 step','Finish','2 step','3 step','No scope','No share'],rotation=60,ha='right',fontsize=7)
        ax.set_title(family.replace('_',' '));ax.set_ylabel('Mean declared loss');ax.grid(axis='y',alpha=.15)
    fig.suptitle('Synthetic ablations at budget two, including misspecified scope and ineffective answers',fontsize=10);fig.tight_layout(rect=(0,0,1,.88));save(fig,out,'synthetic_ablations')


def diagnostics(out,root):
    data=rows(root/'analysis/benefit_forecast.csv');g={}
    for r in data:
        g.setdefault(r['id'],[]).append(r)
    x=[np.mean([r['predicted_net_benefit'] for r in rs]) for rs in g.values()];y=[np.mean([r['realized_net_benefit'] for r in rs]) for rs in g.values()]
    fig,axes=plt.subplots(1,2,figsize=(7.2,3.2));axes[0].scatter(x,y,s=24,color=COLORS['depth2'],alpha=.6)
    lo=min(0,min(x),min(y));hi=max(x+y)+.1;axes[0].plot([lo,hi],[lo,hi],':',color='#555555');axes[0].set_xlabel('Predicted net clarification benefit');axes[0].set_ylabel('Realized net clarification benefit');axes[0].set_title('48 dialogue means, budget two')
    d=rows(root/'analysis/conditional_prediction_quality.csv')
    axes[1].bar(range(len(d)),[r['conditional_brier'] for r in d],color=['#BBA06D','#556A8A','#343A40']);axes[1].set_xticks(range(len(d)));axes[1].set_xticklabels([r['backend'].capitalize() for r in d]);axes[1].set_ylabel('Brier score (lower is better)');axes[1].set_title('Supplied values only; counts shown')
    for i,r in enumerate(d):axes[1].text(i,r['conditional_brier']+.003,'n=%d'%r['supplied_fields'],ha='center',fontsize=8)
    axes[1].set_ylim(0,max(r['conditional_brier'] for r in d)*1.3);fig.tight_layout();save(fig,out,'belief_diagnostics')


def overhead(out,root):
    d=rows(root/'analysis/computation.csv');g=[r for r in d if r['application']=='evaluation' and r['method'] in ['one_step','completion','depth2','depth3']]
    ref=rows(root/'synthetic/exact_reference.csv');fig,axes=plt.subplots(1,2,figsize=(7.2,3.2))
    axes[0].bar(range(len(g)),[r['mean_episode_ms'] for r in g],color=[COLORS[r['method']] for r in g]);axes[0].set_xticks(range(len(g)));axes[0].set_xticklabels([LABELS[r['method']] for r in g],rotation=20,ha='right');axes[0].set_ylabel('CPU replay time (ms)');axes[0].set_title('Mean empirical controller time')
    for i,r in enumerate(g):axes[0].text(i,r['mean_episode_ms']+.05,'%.2f'%r['mean_episode_ms'],ha='center',fontsize=8)
    for i,w in enumerate([2,8]):
        vals=[r['pruning_gap'] for r in ref if r['width']==w and r['depth']==2 and r['construction']=='dependency'];axes[1].scatter(np.arange(len(vals))/max(1,len(vals)-1)*.5+i-.25,vals,s=8,alpha=.35,color=COLORS['depth2'])
        axes[1].plot([i-.25,i+.25],[np.mean(vals),np.mean(vals)],color='#202020',lw=2)
    axes[1].set_xticks([0,1]);axes[1].set_xticklabels(['Width 2','Width 8']);axes[1].set_ylabel('Expected loss gap to exact depth two');axes[1].set_title('Small-instance pruning diagnostic');axes[1].axhline(0,color='#777777',lw=.5);fig.tight_layout();save(fig,out,'planning_cost_gap')


def examples(out,root):
    selected=read(root/'analysis/examples.json')['selection'];lookup={}
    keys=set(x for x in selected.values() if x)
    with gzip.open(root/'evaluation/traces.jsonl.gz','rt') as f:
        for line in f:
            t=json.loads(line)
            if t['id'] in keys and t['budget']==2 and t['error_weight']==4 and t['method'] in ['depth2','one_step','semantic_memory','completion']:lookup[(t['id'],t['method'],t['replicate'])]=t
    chosen=[]
    for kind in ['benefit','tie','unfavorable']:
        key='one_step_'+kind;id=selected[key]
        if id is None:
            key='completion_'+kind;id=selected[key]
        if id:chosen.append((kind,id,'one_step' if key.startswith('one_step') else 'completion'))
    fig,axes=plt.subplots(len(chosen),1,figsize=(7.4,2.8*len(chosen)),squeeze=False)
    for ax,(kind,id,base) in zip(axes[:,0],chosen):
        for y,(method,rep) in enumerate([(base,0),('depth2',0),(base,1),('depth2',1)]):
            t=lookup[(id,method,rep)];qs=[e['question']['id'] for e in t['events'] if e['kind']=='question_shown']
            ax.text(-.2,y,LABELS[method]+'\nreplicate '+str(rep),ha='right',va='center',fontsize=8)
            for i,q in enumerate(qs):
                ax.add_patch(FancyBboxPatch((i*2.25,y-.18),2.05,.36,boxstyle='round,pad=.06',facecolor=COLORS[method],edgecolor='none'))
                ax.text(i*2.25+1.02,y,q.replace('.','\n'),ha='center',va='center',color='white',fontsize=8)
            summary=', '.join('%s: %s'%(o['task'].replace('_shortlist',''),o['status']) for o in t['outcomes'])
            ax.text(4.65,y,summary,va='center',fontsize=8)
        ax.set_xlim(-.1,9);ax.set_ylim(-.6,3.6);ax.axis('off');ax.set_title('%s example · %s · first qualifying dialogue, both replicates'%(kind.capitalize(),id),loc='left')
    fig.tight_layout();save(fig,out,'matched_questions')


def main(root=None):
    root=Path(root or ART);out=root/'figures';out.mkdir(exist_ok=True)
    dependency(out);performance(out,rows(root/'analysis/summary.csv'));synthetic_map(out,root);paired(out,root);ablations(out,root);diagnostics(out,root);overhead(out,root);examples(out,root)
    print('Nine vector figure sets:',out)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root');main(p.parse_args().root)
