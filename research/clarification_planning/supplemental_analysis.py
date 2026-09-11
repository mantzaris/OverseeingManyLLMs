"""Secondary baseline audit and richer descriptive diagnostics on saved outputs."""
import csv
import gzip
import json
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np
from .common import ART,read,write_json,digest
from .analyze import rows,interval,SEED,RESAMPLES
from .evaluate import csv_write
from .collect import records,answers
from .empirical import predictions

def run(root=None):
    global ART
    if root is not None:
        from pathlib import Path
        ART=Path(root)
    out=ART/'analysis';core=rows(ART/'evaluation/episodes.csv');extra=rows(ART/'completion_audit/episodes.csv')
    combined=core+extra;ids=sorted({r['id'] for r in core});ind=np.random.default_rng(SEED).integers(0,len(ids),(RESAMPLES,len(ids)))
    contrasts=[];totals=[]
    for ew in [2.,4.,8.]:
        for budget in [0.,1.,2.,4.,6.,'unlimited']:
            a={};b={}
            for id in ids:
                a[id]=[r for r in core if r['id']==id and r['method']=='depth2' and r['budget']==budget and r['error_weight']==ew]
                b[id]=[r for r in extra if r['id']==id and r['budget']==budget and r['error_weight']==ew]
            for metric in ['loss','project_correct','correct','incorrect','unfinished','questions']:
                diff=[np.mean([r[metric] for r in a[id]])-np.mean([r[metric] for r in b[id]]) for id in ids]
                mean,lo,hi=interval(diff,ind)
                contrasts.append(dict(budget=budget,error_weight=ew,metric=metric,difference=mean,lo=lo,hi=hi,
                    negative=int(sum(x<-1e-10 for x in diff)),ties=int(sum(abs(x)<=1e-10 for x in diff)),positive=int(sum(x>1e-10 for x in diff))))
    csv_write(out/'minimum_completion_paired.csv',contrasts)
    for method in sorted({r['method'] for r in combined}):
        rs=[r for r in combined if r['method']==method and r['budget']==2 and r['error_weight']==4]
        totals.append(dict(method=method,preparations=len(rs),dialogues=len(ids),**{m:sum(r[m] for r in rs) for m in ['tasks','loss','project_correct','correct','incorrect','unfinished','questions','repeated_questions','incorrect_scope_transfers','failed_calls']}))
    csv_write(out/'primary_totals.csv',totals)
    case_map={c['id']:c for c in read(ART/'data/public.json') if c['split']=='evaluation'}
    structure=rows(out/'structure.csv');audit=[];rejections=[];records_flat=[]
    for case in case_map.values():
        audit.append(dict(id=case['id'],domains=','.join(t['domain'] for t in case['tasks']),tasks=len(case['tasks']),fields=len(case['fields']),multi_field_tasks=sum(len(t['required'])>=2 for t in case['tasks'])))
        for rep in range(2):
            prep=read(ART/'prepared'/('evaluation_'+case['id'][:-5]+'_'+str(rep)+'.json'))
            accepted,rejected=records(prep['outputs']['extract'],case)
            for r in rejected:rejections.append(dict(id=case['id'],replicate=rep,reason=r['reason'] if isinstance(r,dict) else r,record=r.get('record') if isinstance(r,dict) else None))
            raw=prep['outputs'].get('extract',{});raw_records=raw.get('records',[]) if isinstance(raw,dict) else []
            records_flat.append(dict(id=case['id'],replicate=rep,raw_records=len(raw_records),accepted=len(accepted),rejected=len(rejected),required=len(case['fields'])))
    csv_write(out/'source_task_structure.csv',audit);csv_write(out/'source_guard_counts.csv',records_flat);write_json(out/'source_guard_rejections.json',rejections)
    write_json(out/'structure_summary.json',dict(dialogues=len(ids),domain_combinations=dict(Counter(r['domains'] for r in audit)),tasks=sum(r['tasks'] for r in audit),
        multi_field_tasks=sum(r['multi_field_tasks'] for r in audit),fields=sum(r['fields'] for r in audit),
        preparations=len(structure),preparations_different_first_question=int(sum(r['first_question_differs'] for r in structure)),
        preparations_myopic_stop_but_depth2_asks=int(sum(r['zero_one_step_positive_two_step'] for r in structure)),
        dialogue_count_any_different_question=len({r['id'] for r in structure if r['first_question_differs']}),
        dialogue_count_any_myopic_stop=len({r['id'] for r in structure if r['zero_one_step_positive_two_step']}),
        task_preparations_missing_at_least_two_values=int(sum(r['tasks_missing_two_values'] for r in structure)),
        legitimate_cross_task_shared_decisions=0,all_source_required_values_already_stated=True,
        note='Multi-field tasks are source-derived; unresolved interpretation is model/guard-induced. No cross-domain scope annotation was manufactured.'))
    # Conditional Brier avoids crediting an abstention as a correct prediction of
    # its own lack of a supplied answer. Both unconditional and conditional shown.
    pred=rows(out/'prediction_fields.csv');quality=[]
    for backend in ['extract','memory','history']:
        g=[r for r in pred if r['backend']==backend and r['supplied']]
        quality.append(dict(backend=backend,supplied_fields=len(g),correct=sum(r['correct'] for r in g),accuracy=np.mean([r['correct'] for r in g]),
                            conditional_brier=np.mean([r['brier'] for r in g]),mean_predicted_correct=np.mean([r['probability'] for r in g])))
    csv_write(out/'conditional_prediction_quality.csv',quality)
    refs=rows(ART/'synthetic/exact_reference.csv');gaps=[]
    for width in [2,8]:
        r=[r for r in refs if r['depth']==2 and r['construction']=='dependency' and r['width']==width]
        gaps.append(dict(width=width,comparisons=len(r),positive_pruning_gaps=sum(x['pruning_gap']>1e-8 for x in r),max_gap=max(x['pruning_gap'] for x in r),mean_gap=np.mean([x['pruning_gap'] for x in r])))
    csv_write(out/'pruning_summary.csv',gaps)
    variation=[]
    for case in case_map.values():
        preps=[read(ART/'prepared'/('evaluation_'+case['id'][:-5]+'_'+str(rep)+'.json')) for rep in range(2)]
        for backend in ['extract','memory','history']:
            values=[predictions(case,p,backend) for p in preps]
            variation.append(dict(id=case['id'],backend=backend,changed_fields=sum(values[0].get(k)!=values[1].get(k) for k in case['fields']),fields=len(case['fields'])))
    csv_write(out/'generation_variation.csv',variation)
    distribution=[]
    for method in ['depth2','one_step','semantic_memory','full_history','completion']:
        for case in case_map.values():
            pair=sorted([r for r in core if r['id']==case['id'] and r['method']==method and r['budget']==2 and r['error_weight']==4],key=lambda r:r['replicate'])
            distribution.append(dict(id=case['id'],method=method,replicate0_loss=pair[0]['loss'],replicate1_loss=pair[1]['loss'],difference=pair[1]['loss']-pair[0]['loss']))
    csv_write(out/'replicate_variation.csv',distribution)
    # Save the actual trace details behind all first-qualifying selections.
    selected=read(out/'examples.json')['selection'];wanted=set(x for x in selected.values() if x);examples=[]
    with gzip.open(ART/'evaluation/traces.jsonl.gz','rt') as f:
        for line in f:
            t=json.loads(line)
            if t['id'] in wanted and t['replicate']==0 and t['budget']==2 and t['error_weight']==4 and t['method'] in ['depth2','one_step','semantic_memory','completion','full_history']:examples.append(t)
    write_json(out/'selected_traces.json',examples)
    forecasts=[]
    with gzip.open(ART/'evaluation/traces.jsonl.gz','rt') as f:
        for line in f:
            t=json.loads(line)
            if t['method']=='depth2' and t['budget']==2 and t['error_weight']==4:
                first=t['plans'][0]
                forecasts.append(dict(id=t['id'],replicate=t['replicate'],predicted_net_benefit=first['expected_terminal_now']-first['expected_plan_loss'],realized_net_benefit=t['row']['realized_benefit']-.05*t['row']['questions']))
    csv_write(out/'benefit_forecast.csv',forecasts)
    print('MINIMUM COMPLETION PRIMARY',json.dumps([r for r in contrasts if r['budget']==2 and r['error_weight']==4],indent=2))
    print('TOTALS',json.dumps(totals,indent=2))

if __name__=='__main__':run()
