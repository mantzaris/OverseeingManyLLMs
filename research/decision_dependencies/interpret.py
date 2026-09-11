"""Post hoc diagnosis of frozen results, without changing decisions or raw evidence."""
import argparse
import csv
import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from .client import ART, write_json, parsed
from .analyze import read_rows, table_csv, project_means, resamples, interval
from .application import artifact


def run(output=None):
    out=Path(output) if output else ART/'interpretation'
    out.mkdir(parents=True,exist_ok=True)
    rows=read_rows(ART/'evaluation/episodes.csv')
    primary=[r for r in rows if r['demand']==6 and r['budget']=='unlimited']
    metrics=['artifact_goals','project_correct','correct_artifacts','incorrect_artifacts',
             'unresolved_artifacts','questions','answered_questions','distinct_decisions_requested',
             'repeated_decision_questions','incorrect_reuse','reused_answers','revalidation_reads',
             'version_checks','candidate_sources','scope_confirmations',
             'changed_instruction_recoveries','changed_instruction_failures']
    totals=[]
    for m in dict.fromkeys(r['method'] for r in primary):
        group=[r for r in primary if r['method']==m]
        totals.append(dict(method=m,source_dialogues=24,generation_replicates=2,
                           **{k:int(sum(r[k] for r in group)) for k in metrics}))
    table_csv(out/'primary_totals.csv',totals)

    challenge=json.loads((ART/'challenge_results.json').read_text());cr=[]
    for m in dict.fromkeys(r['method'] for r in challenge):
        group=[r for r in challenge if r['method']==m]
        cr.append(dict(method=m,authored_cases=12,generation_replicates=2,
              **{k:sum(r[k] for r in group) for k in
                 ['correct_auto_answer','appropriate_abstention','incorrect_transfer','extra_question']}))
    table_csv(out/'challenge_summary.csv',cr)
    diag=list(csv.DictReader((ART/'evaluation/analysis/prediction_diagnostics.csv').open()))
    dr=[]
    for k in dict.fromkeys(r['kind'] for r in diag):
        group=[r for r in diag if r['kind']==k]
        dr.append(dict(kind=k,**{name:sum(int(r[name]) for r in group)
                               for name in ['fields','supplied','correct','incorrect','rejected']}))
    table_csv(out/'interpretation_diagnostics.csv',dr)
    generations=defaultdict(list);malformed=[]
    for path in sorted((ART/'raw').glob('*.json')):
        raw=json.loads(path.read_text());key=raw['call_id']
        phase='final_dialogue' if key.startswith('evaluation_') else 'authored_challenge' if key.startswith('challenge_') else 'development'
        generations[phase].append(raw)
        if parsed(raw) is None:
            malformed.append(dict(call_id=key,status=raw['status'],
                finish_reason=raw['attempts'][-1].get('response',{}).get('choices',[{}])[0].get('finish_reason'),
                attempts=len(raw['attempts'])))
    timing=[]
    for phase,group in sorted(generations.items()):
        attempts=[a for r in group for a in r['attempts']]
        seconds=[a['elapsed_seconds'] for a in attempts]
        usage=[a.get('response',{}).get('usage',{}) for a in attempts]
        timing.append(dict(phase=phase,calls=len(group),attempts=len(attempts),
            mean_seconds=float(np.mean(seconds)),median_seconds=float(np.median(seconds)),
            p95_interpolated_seconds=float(np.percentile(seconds,95)),
            summed_attempt_seconds=sum(seconds),
            prompt_tokens=sum(u.get('prompt_tokens',0) for u in usage),
            completion_tokens=sum(u.get('completion_tokens',0) for u in usage)))
    table_csv(out/'generation_costs.csv',timing)
    write_json(out/'malformed_calls.json',malformed)

    selected={};failures=[];alias_rows=[];wrong_fields=Counter();questions=Counter()
    db={d:json.loads((ART/('data/'+d+'_db.json')).read_text()) for d in ['hotel','restaurant']}
    with gzip.open(ART/'evaluation/traces.jsonl.gz','rt') as f:
        for line in f:
            trace=json.loads(line);r=trace['row']
            if r['demand']!=6 or r['budget']!='unlimited':continue
            for q in trace['questions']:questions[(r['method'],q['reason'])]+=1
            improved=[];alias_fixed=0;remaining_wrong=0
            for a in trace['artifacts']:
                values=dict(a['values'])
                for k,v in list(values.items()):
                    if k.endswith('.area') and v=='center of town':values[k]='centre'
                revised=artifact(a['role'],values,db) if not a['missing'] else None
                correct=not a['missing'] and values==a['expected'] and revised==a['expected_output']
                improved.append(correct)
                alias_fixed+=int(correct and a['status']=='incorrect')
                remaining_wrong+=int(not correct and a['status']=='incorrect')
                if a['status']=='incorrect':
                    for k,v in a['values'].items():
                        if v!=a['expected'].get(k):wrong_fields[(r['method'],k,v,a['expected'].get(k))]+=1
                    if r['method'] in ['dependency_barrier','semantic_memory']:
                        failures.append(dict(id=r['id'],replicate=r['replicate'],method=r['method'],
                            role=a['role'],values=a['values'],expected=a['expected'],output=a['output'],
                            alias_repair_suffices=correct))
            alias_rows.append(dict(id=r['id'],replicate=r['replicate'],method=r['method'],
                original_correct=r['correct_artifacts'],recomputed_correct=sum(improved),
                recomputed_project_correct=int(all(improved)),alias_fixed=alias_fixed,
                remaining_incorrect=remaining_wrong,unresolved=r['unresolved_artifacts'],
                questions=r['questions']))
            if r['replicate']==0 and r['method'] in ['dependency_barrier','semantic_memory','records_read']:
                selected[(r['id'],r['method'])]=trace
    table_csv(out/'area_alias_sensitivity_rows.csv',alias_rows)
    alias_summary=[]
    for m in dict.fromkeys(r['method'] for r in alias_rows):
        g=[r for r in alias_rows if r['method']==m]
        alias_summary.append(dict(method=m,**{k:sum(r[k] for r in g) for k in
              ['original_correct','recomputed_correct','recomputed_project_correct','alias_fixed',
               'remaining_incorrect','unresolved','questions']}))
    table_csv(out/'area_alias_sensitivity.csv',alias_summary)
    table_csv(out/'question_reasons.csv',[dict(method=m,reason=q,count=n)
                         for (m,q),n in sorted(questions.items())])
    table_csv(out/'wrong_value_uses.csv',[dict(method=m,key=k,returned=v,expected=t,count=n)
                         for (m,k,v,t),n in sorted(wrong_fields.items())])
    write_json(out/'failed_artifacts.json',failures)

    means=project_means(rows);ids=sorted({r['id'] for r in primary})
    strata={r['id']:int(r['changed']) for r in primary};samples=resamples(ids,strata)
    burden=[]
    for coefficient in [0,.25,1]:
        for method in ['semantic_memory','global_barrier','dependency_barrier','full_history']:
            values=[means[(i,method,6,'unlimited')]['questions']+
                    coefficient*means[(i,method,6,'unlimited')]['candidate_sources'] for i in ids]
            lo,hi=interval(values,samples)
            burden.append(dict(method=method,assumed_cost_per_candidate=coefficient,
                               mean=np.mean(values),lo=lo,hi=hi))
    table_csv(out/'inspection_cost_sensitivity.csv',burden)
    examples=json.loads((ART/'evaluation/analysis/examples.json').read_text())['selected']
    for i in ids:
        p=means[(i,'dependency_barrier',6,'unlimited')];b=means[(i,'semantic_memory',6,'unlimited')]
        if p['artifact_accuracy']==b['artifact_accuracy'] and p['questions']>b['questions']:
            examples['more_questions_same_quality']=dict(id=i,comparator='semantic_memory',replicate=0)
            break
    write_json(out/'example_selection.json',dict(
        extra_rule='First source ID with more questions and equal artifact quality, comparing dialogue means; show replicate 0.',
        primary_frozen_examples_unchanged=True,selected=examples))
    details=[]
    for name,item in examples.items():
        for method in [item['comparator'],'dependency_barrier']:
            t=selected[(item['id'],method)]
            details.append(dict(example=name,**t))
    write_json(out/'example_traces.json',details)
    manifest=dict(label='Post hoc explanation and hypothetical adapter normalization, not a new evaluation',
          source='evaluation/traces.jsonl.gz',changed_alias={'*.area: center of town':'centre'},
          controller_decisions_changed=False,new_generations=0,
          figures_or_tables_must_not_replace_frozen_primary=True,
          independent_units=24,replicates_averaged_for_intervals=2)
    write_json(out/'manifest.json',manifest)
    print(json.dumps(dict(output=str(out),totals=totals,challenge=cr,alias=alias_summary),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args();run(a.output)
