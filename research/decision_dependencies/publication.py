"""Readable presentation of the saved comparison; no policy or scoring changes."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from .client import ART, write_json
from .analyze import LABELS,COLORS


def make(output=None):
    target=Path(output) if output else ART/'publication'
    target.mkdir(parents=True,exist_ok=True)
    summaries=list(csv.DictReader((ART/'evaluation/analysis/policy_summary.csv').open()))
    def get(m,d=6,b='unlimited'):
        return next(r for r in summaries if r['method']==m and r['demand']==str(d) and r['budget']==b)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
        'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none','legend.frameon':False})
    def save(fig,name):
        fig.tight_layout()
        for ext in ['pdf','svg','png']:fig.savefig(target/(name+'.'+ext),dpi=300,bbox_inches='tight')
        plt.close(fig)

    fig,axes=plt.subplots(1,2,figsize=(9,4.1))
    methods=['full_history','semantic_memory','records_read','dependency_barrier','confirm_records','independent']
    for ax,metric,title in zip(axes,['project_correct','artifact_accuracy'],['Whole projects correct','Local artifacts correct']):
        for m in methods:
            r=get(m);x=float(r['questions']);y=100*float(r[metric])
            label='Global / selective checks' if m=='dependency_barrier' else LABELS[m]
            ax.errorbar(x,y,xerr=[[x-float(r['questions_lo'])],[float(r['questions_hi'])-x]],
                yerr=[[y-100*float(r[metric+'_lo'])],[100*float(r[metric+'_hi'])-y]],
                fmt='s' if m=='dependency_barrier' else 'o',color=COLORS[m],capsize=2,ms=6,label=label)
        ax.set(xlabel='Additional questions per project',ylabel='Correct (%)',ylim=(35,104),title=title)
        ax.grid(axis='y',alpha=.2)
    axes[1].legend(loc='lower right',fontsize=8)
    axes[0].annotate('Fewer questions at equal\nwhole-project quality',xy=(1.21,91.67),xytext=(5,66),
                     fontsize=8,arrowprops={'arrowstyle':'->','color':'#555555'})
    save(fig,'quality_and_questions')

    fig,axes=plt.subplots(1,2,figsize=(9,4))
    main=['full_history','semantic_memory','dependency_barrier','confirm_records']
    for m in main:
        axes[0].plot([2,4,6],[float(get(m,d)['questions']) for d in [2,4,6]],
                     marker='o',color=COLORS[m],label=LABELS[m])
        axes[1].plot(range(4),[100*float(get(m,6,b)['project_correct']) for b in ['0','2','6','unlimited']],
                     marker='o',color=COLORS[m])
    axes[0].set(xlabel='Active role cap',ylabel='Additional questions per project',xticks=[2,4,6],title='Demand with unlimited responses')
    axes[1].set(xlabel='Available additional user answers',ylabel='Whole projects correct (%)',xticks=range(4),
                 xticklabels=['0','2','6','Unlimited'],ylim=(-3,103),title='Six-role response-budget sensitivity')
    axes[0].legend(fontsize=8);axes[1].grid(axis='y',alpha=.2)
    save(fig,'demand_and_budget')

    fig,axes=plt.subplots(1,3,figsize=(10,4.3))
    methods=['semantic_memory','records_read','global_barrier','dependency_barrier','no_source_guard','no_scope','confirm_records']
    labels=[LABELS[m] for m in methods];ys=np.arange(len(methods))
    for ax,metric,title in zip(axes,['project_correct','questions','revalidation_reads'],
                              ['Whole projects correct (%)','Additional questions','Machine value rereads']):
        vals=[float(get(m)[metric])*(100 if metric=='project_correct' else 1) for m in methods]
        ax.barh(ys,vals,color=[COLORS[m] for m in methods]);ax.invert_yaxis()
        ax.set(yticks=ys,yticklabels=labels if ax==axes[0] else [],title=title)
        for y,v in zip(ys,vals):ax.text(v+.08,y,'%0.1f'%v,va='center',fontsize=8)
        ax.set_xlim(0,108 if metric=='project_correct' else max(vals)*1.25)
        if metric=='project_correct':ax.set_xticks([0,25,50,75,100])
    save(fig,'consistency_ablations')

    challenge=json.loads((ART/'challenge_results.json').read_text())
    ids=sorted({r['id'] for r in challenge});methods=['full_history','semantic_memory','global_barrier','dependency_barrier']
    a=np.zeros((len(ids),len(methods)));labels=[];counts=[]
    for i,key in enumerate(ids):
        label=next(r['family'] for r in challenge if r['id']==key).replace('_',' ');labels.append(label)
        for j,m in enumerate(methods):
            group=[r for r in challenge if r['id']==key and r['method']==m]
            wrong=sum(r['incorrect_transfer'] for r in group);extra=sum(r['extra_question'] for r in group)
            a[i,j]=2 if wrong else 1 if extra else 0
            counts.append((i,j,('%d/2 wrong'%wrong) if wrong else ('%d/2 asks'%extra) if extra else '2/2 valid'))
    fig,ax=plt.subplots(figsize=(8.4,5.4));ax.imshow(a,cmap=ListedColormap(['#d6ece6','#fff0c2','#f1cbc5']),vmin=0,vmax=2,aspect='auto')
    for i,j,t in counts:ax.text(j,i,t,ha='center',va='center',fontsize=9)
    ax.set(yticks=range(len(ids)),yticklabels=labels,xticks=range(len(methods)),
           xticklabels=['Full history','Semantic memory','Global check','Selective check'],title='Authored scope challenges: two generations per case')
    ax.tick_params(length=0);save(fig,'scope_challenges')

    traces=json.loads((ART/'interpretation/example_traces.json').read_text())
    fig,axes=plt.subplots(2,2,figsize=(10,6.4),sharex=True)
    for column,name in enumerate(['benefit','more_questions_same_quality']):
        group=[t for t in traces if t['example']==name]
        for row,t in enumerate(group):
            ax=axes[row,column];r=t['row'];roles=[a['role'] for a in t['artifacts']]
            for y,a in enumerate(t['artifacts']):
                q=[sum(x['role']==a['role'] and x['stage']==stage for x in t['questions']) for stage in [0,1]]
                ax.plot([0,2],[y,y],color='#cccccc',lw=1.5)
                for x,n in zip([.2,1.25],q):
                    if n:ax.scatter(x,y,s=40,color='#0072B2');ax.text(x+.09,y,str(n),va='center',fontsize=8)
                ax.scatter(2,y,s=45,marker='s',color='#009E73' if a['status']=='correct' else '#D55E00')
            ax.axvline(.8,color='#777777',ls='--',lw=1)
            ax.set(yticks=range(len(roles)),yticklabels=[x.replace('_',' ') for x in roles],
                   title=r['id']+' | '+LABELS[r['method']],xlim=(-.1,2.25));ax.invert_yaxis()
            ax.set_xticks([.2,.8,1.25,2]);ax.set_xticklabels(['Prepare','Update','Recheck','Release'],fontsize=8)
            ax.text(.99,-.25,'%d %s; %d/%d artifacts correct'%(r['questions'],'question' if r['questions']==1 else 'questions',r['correct_artifacts'],r['artifact_goals']),
                    transform=ax.transAxes,ha='right',fontsize=8)
    save(fig,'instruction_change_examples')

    captions={
      'quality_and_questions':'Frozen comparison on 24 source dialogues, two GPU replicates averaged within dialogue, up to six roles, unlimited scripted answers. Points show generated task interpretations and simulated additional questions. Intervals use 2,000 stratified dialogue-level bootstrap resamples. Global and selective checks coincide and are shown once. Independent requests are mean-dominated by confirming shared records on these two axes. Other tradeoffs remain visible; machine costs and actual human effort are separate.',
      'demand_and_budget':'Constructed role demand and accurate scripted response budgets reuse identical saved interpretations. Existing source utterances are not additional responses. Unresolved artifacts count against project correctness. Global checks coincide with selective checks. No user time or mental workload was measured.',
      'consistency_ablations':'Frozen controller ablations at six roles and unlimited answers. Questions are additional simulated user requests. Rereads are host operations, not evidence inspections by people. Global/selective quality and question equality is expected under the implementation; selective checking saves only machine reads here.',
      'scope_challenges':'Twelve separately authored cases with two GPU generations each, not twelve human participants or MultiWOZ source dialogues. Valid means either the correct answer or appropriate abstention when no authoritative answer exists. Yellow denotes an unnecessary request when the answer exists. Red denotes an incorrect transfer. The model can omit a revocation or paraphrased exception even with a valid earlier source quotation.',
      'instruction_change_examples':'Logical event diagrams of the same source dialogue and saved preparation across methods. Left is the first declared benefit over records without a release check. Right is the first quality tie with more questions than semantic memory. Blue numerals count clarification requests per role and phase. Green/red squares are correctly/incorrectly released local artifacts. Horizontal spacing is not observed time. Source utterances are task-elicited, interpretations generated, and agent work/questions constructed.'}
    write_json(target/'captions.json',captions)
    sources=['evaluation/analysis/policy_summary.csv','challenge_results.json','interpretation/example_traces.json']
    write_json(target/'figure_sources.json',dict(script='research/decision_dependencies/publication.py',
         script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         source_sha256={s:hashlib.sha256((ART/s).read_bytes()).hexdigest() for s in sources},new_inference_calls=0,
         formats=['vector PDF','vector SVG','300 dpi PNG'],figures=list(captions)))
    print('Publication figures:',target)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args();make(a.output)
