#!/usr/bin/env python3
"""Descriptive diagnostics from saved preparations and declared policy states."""
from collections import Counter
import csv,gzip,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.retail.analysis import csv_file,semantic_classes,percentile
from overseeing.io import write_json
root=Path('artifacts/stage6_robustness')
for cohort in ('fresh','post_hoc_stage5'):
    out=root/'analysis'/cohort
    if not (out/'summary.json').exists():continue
    source=root if cohort=='fresh' else Path('artifacts/stage5_practical')
    cases={c['case_id']:c for c in json.loads((source/'cases.json').read_text())['cases']}
    preps=[r for p in sorted((source/'batches/evaluation/prepared').glob('*/workflows.json')) for r in json.loads(p.read_text())]
    failures=Counter(r['failure'] or 'finished_without_staging' for r in preps if r['proposal'] is None)
    classes=Counter(c for r in preps if r['initial_error'] for c in semantic_classes(r['proposal'],cases[r['case_id']]['target_action']))
    tools=Counter(e['call']['tool'] for r in preps for e in r['events'])
    affected=[r for r in preps if r['proposal'] and len(r['proposal']['arguments'].get('item_ids',[]))>=2]
    ds=list(csv.DictReader((out/'dispatches.csv').open()));planning=[]
    for policy in ('no_review','fcfs','edf','uncertainty','greedy','search'):
        for size in range(4):
            group=[r for r in ds if r['policy']==policy and int(r['eligible'])==size]
            if not group:continue
            values=[float(r['planning_seconds'])*1000 for r in group]
            planning.append(dict(policy=policy,eligible=size,dispatches=len(group),mean_ms=sum(values)/len(values),p95_ms=percentile(values,.95),max_ms=max(values),max_ordered_subsets=max(int(r['ordered_subsets_evaluated']) for r in group)))
    csv_file(out/'planning_costs.csv',planning)
    seq=list(csv.DictReader((out/'sequence_comparisons.csv').open()));differences=[]
    for variant in ('reference','approve_block','complexity_time'):
        for duration in ('1','2'):
            states=[r for r in ds if (r['variant'],r['review_duration'],r['policy'])==(variant,duration,'search')]
            for comparator in ('greedy','edf'):
                group=[r for r in seq if (r['variant'],r['review_duration'],r['comparator'])==(variant,duration,comparator)]
                differences.append(dict(variant=variant,review_duration=int(duration),comparator=comparator,
                    actual_sequences_differ=sum(r['sequences_differ']=='True' for r in group),paired_replicates=len(group),
                    search_path_multi_eligible=sum(int(r['eligible'])>=2 for r in states),
                    search_path_greedy_search_different_heads=sum(r['greedy_choice']!=r['search_choice'] for r in states)))
    csv_file(out/'scheduling_differences.csv',differences)
    variant_orders=[]
    for variant in ('approve_block','complexity_time'):
        for duration in (1,2):
            for policy in ('no_review','fcfs','edf','uncertainty','greedy','search'):
                different=0;total=0
                for directory in sorted((out/'traces').iterdir()):
                    a=json.loads(gzip.decompress((directory/('reference_s%d_%s.json.gz'%(duration,policy))).read_bytes()))
                    b=json.loads(gzip.decompress((directory/('%s_s%d_%s.json.gz'%(variant,duration,policy))).read_bytes()))
                    different+=a['review_sequence']!=b['review_sequence'];total+=1
                variant_orders.append(dict(variant=variant,review_duration=duration,policy=policy,sequences_differ_from_reference=different,paired_replicates=total))
    csv_file(out/'variant_review_orders.csv',variant_orders)
    variability=list(csv.DictReader((out/'generation_variability.csv').open()))
    record=dict(failure_reasons=dict(failures),initial_error_classes=dict(classes),tool_calls=dict(tools),
        automatic_rejections=sum(r['automatic_rejections'] for r in preps),multi_item_proposals=len(affected),multi_item_initial_errors=sum(r['initial_error'] for r in affected),
        multi_item_source_cases=len({r['case_id'] for r in affected}),cases_with_different_proposals=sum(int(r['distinct_proposals'])>1 for r in variability),
        cases_with_mixed_initial_correctness=sum(0<int(r['initially_correct'])<3 for r in variability),
        definition='Diagnostics condition on saved preparations. Error classes may overlap. Dispatch counts are descriptive repeated states, not independent observations.')
    write_json(out/'mechanism_diagnostics.json',record)
