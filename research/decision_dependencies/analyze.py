"""Frozen paired analysis and programmatic figure generation from saved outputs."""
import argparse
import csv
import gzip
import json
from collections import defaultdict
from pathlib import Path
import numpy as np
from .client import ART, canonical, write_json
from .evaluate import METHODS
from .records import extracted_records, parsed_queries, model_answers

LABELS={'independent':'Independent requests','full_history':'Full history','semantic_memory':'Semantic memory',
        'records_read':'Records at read','global_barrier':'Global version check',
        'dependency_barrier':'Selective dependencies','no_source_guard':'No source guard',
        'no_scope':'No domain scope','confirm_records':'Confirm every record'}
COLORS=dict(zip(METHODS,['#777777','#0072B2','#009E73','#D55E00','#CC79A7','#E69F00','#56B4E9','#884488','#222222']))
METRICS=['project_correct','artifact_accuracy','correct_artifacts','incorrect_artifacts','unresolved_artifacts',
         'questions','answered_questions','distinct_decisions_requested','repeated_decision_questions',
         'incorrect_reuse','reused_answers','maximum_error_fanout','revalidation_reads','version_checks',
         'candidate_sources','scope_confirmations','changed_instruction_recoveries','changed_instruction_failures',
         'failed_generation_calls','final_wrong_fields']

def read_rows(path):
    rows=list(csv.DictReader(Path(path).open()))
    for row in rows:
        for k in list(row):
            if k not in ('id','method','budget'):row[k]=float(row[k])
    return rows

def project_means(rows):
    groups=defaultdict(list)
    for r in rows:groups[(r['id'],r['method'],int(r['demand']),str(r['budget']))].append(r)
    return {key:{metric:float(np.mean([r[metric] for r in values])) for metric in METRICS}
            for key,values in groups.items()}

def resamples(ids,strata,seed=91831,n=2000):
    random=np.random.RandomState(seed);blocks=[]
    for state in sorted(set(strata.values())):
        idx=np.array([i for i,key in enumerate(ids) if strata[key]==state],dtype=int)
        blocks.append(random.choice(idx,size=(n,len(idx)),replace=True))
    return np.concatenate(blocks,axis=1)

def interval(values,samples):
    values=np.asarray(values,dtype=float)
    return [float(x) for x in np.percentile(values[samples].mean(axis=1),[2.5,97.5])]

def table_csv(path,rows):
    if not rows:return
    with Path(path).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def diagnostics(split):
    public={x['id']:x for x in json.loads((ART/'data/public_projects.json').read_text()) if x['split']==split}
    private={x['id']:x for x in json.loads((ART/'data/evaluation_only.json').read_text())}
    rows=[];variability=[]
    for key,case in public.items():
        paths=sorted((ART/'prepared').glob(split+'_'+case['project']+'_*.json'));signatures=[]
        for path in paths:
            prepared=json.loads(path.read_text());out=prepared['outputs'];signature=[]
            for stage in range(2):
                truth=private[key]['annotation_states'][stage]
                for guarded in (False,True):
                    records,rejected=extracted_records(out.get('extract%d'%stage),case['stages'][stage],guarded)
                    supplied={k:r['value'] for k,r in records.items() if k in truth and r.get('value') is not None}
                    rows.append(dict(id=key,replicate=prepared['replicate'],stage=stage,kind='guarded_records' if guarded else 'raw_records',
                                     fields=len(truth),supplied=len(supplied),correct=sum(v==truth[k] for k,v in supplied.items()),
                                     incorrect=sum(v!=truth[k] for k,v in supplied.items()),rejected=len(rejected)))
                    if guarded:signature.append(supplied)
                for kind,prefix in [('full_history','history'),('semantic_memory','memory')]:
                    for v in range(2):
                        answered=model_answers(out.get('%s%d_%d'%(prefix,stage,v)))
                        values={k:answered.get(case['queries'][v][i]['id']) for i,k in enumerate(case['keys']) if k in truth}
                        supplied={k:v for k,v in values.items() if v is not None}
                        rows.append(dict(id=key,replicate=prepared['replicate'],stage=stage,kind=kind,
                                         fields=len(truth),supplied=len(supplied),correct=sum(v==truth[k] for k,v in supplied.items()),
                                         incorrect=sum(v!=truth[k] for k,v in supplied.items()),rejected=0))
            for v in range(2):
                mapping=parsed_queries(out.get('parse%d'%v))
                rows.append(dict(id=key,replicate=prepared['replicate'],stage=v,kind='request_parser',fields=len(case['keys']),
                    supplied=sum(mapping.get(q['id']) is not None for q in case['queries'][v]),
                    correct=sum(mapping.get(q['id'])==k for q,k in zip(case['queries'][v],case['keys'])),
                    incorrect=sum(mapping.get(q['id']) is not None and mapping.get(q['id'])!=k for q,k in zip(case['queries'][v],case['keys'])),rejected=0))
            signatures.append(signature)
        if len(signatures)==2:
            variability.append(dict(id=key,guarded_state_differs=signatures[0]!=signatures[1],
                                    comparable_fields=sum(len(set(a)|set(b)) for a,b in zip(*signatures)),
                                    differing_fields=sum(sum(a.get(k)!=b.get(k) for k in set(a)|set(b)) for a,b in zip(*signatures))))
    return rows,variability

def analyze(split,source_dir=None):
    source=Path(source_dir) if source_dir else ART/split;out=source/'analysis';out.mkdir(parents=True,exist_ok=True)
    rows=read_rows(source/'episodes.csv');means=project_means(rows)
    ids=sorted(set(r['id'] for r in rows));strata={r['id']:int(r['changed']) for r in rows};samples=resamples(ids,strata)
    summaries=[]
    for method in METHODS:
        for demand in (2,4,6):
            for budget in ('0','2','6','unlimited'):
                record=dict(method=method,demand=demand,budget=budget,projects=len(ids))
                for metric in METRICS:
                    values=[means[(i,method,demand,budget)][metric] for i in ids]
                    record[metric]=float(np.mean(values));lo,hi=interval(values,samples)
                    record[metric+'_lo']=lo;record[metric+'_hi']=hi
                summaries.append(record)
    pairs=[];individual=[]
    for comparison in ('semantic_memory','full_history','global_barrier','records_read'):
        for demand in (2,4,6):
            for budget in ('0','2','6','unlimited'):
                for metric in ('project_correct','artifact_accuracy','questions','answered_questions','revalidation_reads'):
                    values=[means[(i,'dependency_barrier',demand,budget)][metric]-means[(i,comparison,demand,budget)][metric] for i in ids]
                    lo,hi=interval(values,samples)
                    pairs.append(dict(comparison='dependency_barrier minus '+comparison,demand=demand,budget=budget,metric=metric,
                                      mean=float(np.mean(values)),lo=lo,hi=hi,negative=int(sum(x<0 for x in values)),
                                      ties=int(sum(x==0 for x in values)),positive=int(sum(x>0 for x in values)),projects=len(ids)))
                    if demand==6 and budget=='unlimited':
                        individual.extend(dict(id=i,comparison=comparison,metric=metric,difference=v) for i,v in zip(ids,values))
    table_csv(out/'policy_summary.csv',summaries);table_csv(out/'paired_comparisons.csv',pairs);table_csv(out/'individual_differences.csv',individual)
    diag,var=diagnostics(split);table_csv(out/'prediction_diagnostics.csv',diag);table_csv(out/'generation_variation.csv',var)
    selected={}
    for name,other,sign in [('benefit','records_read',1),('unfavorable','semantic_memory',-1),('tie','semantic_memory',0)]:
        for i in ids:
            delta=means[(i,'dependency_barrier',6,'unlimited')]['artifact_accuracy']-means[(i,other,6,'unlimited')]['artifact_accuracy']
            if (delta>0 if sign==1 else delta<0 if sign==-1 else delta==0):
                selected[name]=dict(id=i,comparator=other,difference=delta,replicate=0);break
    write_json(out/'examples.json',dict(rule='First source ID in numerical/lexicographic order satisfying each contrast, six roles, unlimited responses; never maximum effect.',selected=selected))
    write_json(out/'analysis_manifest.json',dict(projects=len(ids),rows=len(rows),replicates=sorted(set(int(r['replicate']) for r in rows)),
               resamples=2000,analysis_seed=91831,stratified_by='retained preference change',
               primary=[p for p in pairs if p['comparison']=='dependency_barrier minus semantic_memory' and p['demand']==6 and p['budget']=='unlimited' and p['metric'] in ('project_correct','questions')],
               interpretation='Additional questions and project quality are separate co-primary descriptive outcomes; no scalar utility or human workload inference.'))
    return summaries,pairs,individual,selected

def figures(split,source_dir=None):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    source=Path(source_dir) if source_dir else ART/split;out=source/'analysis';figdir=source/'figures';figdir.mkdir(exist_ok=True)
    summaries,pairs,individual,selected=analyze(split,source)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                         'pdf.fonttype':42,'svg.fonttype':'none','axes.titleweight':'bold','legend.frameon':False})
    def save(fig,name):
        fig.tight_layout()
        for ext in ('pdf','svg','png'):fig.savefig(figdir/(name+'.'+ext),dpi=300,bbox_inches='tight')
        plt.close(fig)
    def get(method,demand=6,budget='unlimited'):
        return next(s for s in summaries if s['method']==method and s['demand']==demand and s['budget']==budget)
    primary=['full_history','semantic_memory','records_read','global_barrier','dependency_barrier','confirm_records','independent']
    fig,ax=plt.subplots(figsize=(8.6,4.8))
    for n,m in enumerate(primary):
        s=get(m);x=s['questions'];y=100*s['artifact_accuracy']
        ax.errorbar(x,y,xerr=[[x-s['questions_lo']],[s['questions_hi']-x]],
                    yerr=[[y-100*s['artifact_accuracy_lo']],[100*s['artifact_accuracy_hi']-y]],
                    fmt='o',markersize=7,color=COLORS[m],capsize=3,label=LABELS[m],alpha=.9)
    ax.set(xlabel='Additional clarification requests per project',ylabel='Correct local artifacts (%)',
           title='Quality and supervisory demand are separate outcomes',ylim=(-3,105))
    ax.legend(loc='lower left',fontsize=9);ax.grid(axis='y',alpha=.2)
    save(fig,'quality_vs_questions')
    fig,axes=plt.subplots(1,2,figsize=(9.2,4.0))
    for m in ['full_history','semantic_memory','records_read','global_barrier','dependency_barrier']:
        axes[0].plot([2,4,6],[get(m,d)['questions'] for d in (2,4,6)],'o-',color=COLORS[m],label=LABELS[m])
        axes[1].plot([2,4,6],[100*get(m,d,'2')['artifact_accuracy'] for d in (2,4,6)],'o-',color=COLORS[m])
    axes[0].set(title='Unlimited response reference',xlabel='Active planning roles',ylabel='Additional questions per project',xticks=[2,4,6])
    axes[1].set(title='Budget: two additional answers',xlabel='Active planning roles',ylabel='Correct local artifacts (%)',xticks=[2,4,6],ylim=(-3,105))
    axes[0].legend(fontsize=8);save(fig,'demand_and_response_budget')
    fig,axes=plt.subplots(1,2,figsize=(9.2,4.1))
    quality={r['id']:r['difference'] for r in individual if r['comparison']=='semantic_memory' and r['metric']=='artifact_accuracy'}
    questions={r['id']:r['difference'] for r in individual if r['comparison']=='semantic_memory' and r['metric']=='questions'}
    ordered=sorted(quality);vals=[100*quality[k] for k in ordered]
    axes[0].bar(range(len(ordered)),vals,color=['#009E73' if v>0 else '#D55E00' if v<0 else '#999999' for v in vals])
    axes[0].axhline(0,color='black',linewidth=.8);axes[0].set(xlabel='Source dialogue in declared order',ylabel='Correct artifact difference (points)',title='Selective minus semantic memory')
    axes[1].scatter([questions[k] for k in ordered],vals,c=['#009E73' if v>0 else '#D55E00' if v<0 else '#777777' for v in vals],s=40,alpha=.7)
    axes[1].axhline(0,color='black',linewidth=.8);axes[1].axvline(0,color='black',linewidth=.8)
    axes[1].set(xlabel='Additional question difference',ylabel='Correct artifact difference (points)',title='Upper left improves both outcomes')
    save(fig,'paired_quality_and_demand')
    fig,axes=plt.subplots(1,2,figsize=(9.2,4.2));ab=['records_read','global_barrier','dependency_barrier','no_source_guard','no_scope','confirm_records']
    y=np.arange(len(ab));names=[LABELS[m] for m in ab]
    axes[0].barh(y,[100*get(m)['artifact_accuracy'] for m in ab],color=[COLORS[m] for m in ab]);axes[0].set(yticks=y,yticklabels=names,xlabel='Correct artifacts (%)',xlim=(0,105),title='Quality ablations');axes[0].invert_yaxis()
    axes[1].barh(y,[get(m)['revalidation_reads'] for m in ab],color=[COLORS[m] for m in ab]);axes[1].set(yticks=y,yticklabels=[],xlabel='Repeat value reads per project',title='Machine work, not human inspections');axes[1].invert_yaxis()
    save(fig,'scope_and_release_ablations')
    # A concrete replay timeline with logical phases, not fabricated human seconds.
    chosen=selected.get('benefit') or selected.get('tie')
    if chosen:
        wanted={};methods=[chosen['comparator'],'dependency_barrier']
        with gzip.open(source/'traces.jsonl.gz','rt') as f:
            for line in f:
                t=json.loads(line);r=t['row']
                if r['id']==chosen['id'] and r['replicate']==0 and r['demand']==6 and r['budget']=='unlimited' and r['method'] in methods:wanted[r['method']]=t
        fig,axes=plt.subplots(2,1,figsize=(9.2,5.2),sharex=True)
        for ax,m in zip(axes,methods):
            t=wanted[m];roles=[a['role'] for a in t['artifacts']]
            for i,a in enumerate(t['artifacts']):
                color='#009E73' if a['status']=='correct' else '#D55E00' if a['status']=='incorrect' else '#777777'
                ax.plot([0,1,2],[i,i,i],color='#cccccc',linewidth=2)
                ax.scatter(2,i,color=color,s=45,marker='s')
            for q in t['questions']:
                i=roles.index(q['role']);x=.15 if q['stage']==0 else 1.5
                ax.scatter(x,i,color='#0072B2',s=18,alpha=.5)
            ax.axvline(1,color='#444444',linestyle='--');ax.set(yticks=range(len(roles)),yticklabels=[x.replace('_',' ') for x in roles],title=LABELS[m]);ax.invert_yaxis()
        axes[-1].set(xticks=[0,1,2],xticklabels=['Prepare from initial source','User source update','Release local artifacts'])
        fig.suptitle(chosen['id']+': blue dots are clarification requests; red squares are incorrect artifacts',fontsize=10,y=1.02)
        save(fig,'changed_instruction_timeline')
    write_json(figdir/'captions.json',{
      'quality_vs_questions':'Generated interpretations and simulated additional user responses on task-elicited source dialogues. Up to six nonempty roles; unlimited responses. Intervals are paired, dialogue-level stratified bootstrap intervals. Artifact correctness is checked against benchmark constraints and executable local outputs, not actual travel success.',
      'demand_and_response_budget':'Constructed role demand and response budgets applied to the same saved GPU outputs. User time and mental workload were not observed.',
      'paired_quality_and_demand':'Each point/bar is one source dialogue after averaging two generation replicates. Positive vertical differences favor selective checking; negative horizontal differences mean fewer questions. No policy replay is an independent sample.',
      'scope_and_release_ablations':'Saved-output controller ablations. Repeat reads measure host computation, not human evidence inspection. Equal global/selective quality is expected from their version semantics.',
      'changed_instruction_timeline':'First qualifying source ID with a selective-versus-read-only quality benefit, otherwise first tie. This is a logical event diagram. Source utterances are observed task-elicited dialogue, proposals are generated, and work release/questions are simulated; horizontal spacing is not measured response time.'})
    print('Analysis and figures saved to',source)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--split',choices=['development','evaluation'],required=True);p.add_argument('--source-dir');p.add_argument('--figures',action='store_true');a=p.parse_args()
    (figures if a.figures else analyze)(a.split,a.source_dir)
