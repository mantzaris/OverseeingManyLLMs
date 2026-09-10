"""Paired source-bundle analysis for Stage 6; never changes the estimator."""
from collections import defaultdict
import copy
import gzip
import json
from pathlib import Path
import random

from overseeing.domain import canonical,digest
from overseeing.io import write_json
from .analysis import csv_file,percentile,prediction_metrics,prepared_rows
from .risk import RetailRisk
from .robustness import VARIANTS,simulate,without_timing
from .scheduler import POLICIES
from .upstream import account_database,load_database

METRICS=('operational_loss','task_completed','wrong_transactions','blocked_unresolved','unstaged_failures',
    'service_failure_loss','wrong_transaction_loss','completed_reviews','corrections','expired_useful_opportunities',
    'review_busy_ticks','total_waiting_ticks','multi_eligible_dispatches','greedy_search_different_heads')


def bundle_means(rows,metric):
    values=defaultdict(dict)
    for r in rows:
        key=(r['variant'],r['review_duration'],r['policy'])
        bucket=values[(r['bundle_id'],key)]
        if r['replicate'] in bucket:raise ValueError('Duplicate generation replicate')
        bucket[r['replicate']]=r[metric]
    result={}
    for key,group in values.items():
        if set(group)!={0,1,2}:raise ValueError('Paired analysis requires all three declared replicates')
        result[key]=sum(group.values())/3
    return result


def paired_summary(values,indices):
    if not values:return dict(mean_difference=None,ci_low=None,ci_high=None,wins=0,ties=0,losses=0)
    samples=[sum(values[i] for i in draw)/len(values) for draw in indices]
    return dict(mean_difference=sum(values)/len(values),ci_low=percentile(samples,.025),ci_high=percentile(samples,.975),
        wins=sum(v<0 for v in values),ties=sum(v==0 for v in values),losses=sum(v>0 for v in values))


def analyze(cohort):
    root=Path('artifacts/stage6_robustness');out=root/'analysis'/cohort;out.mkdir(parents=True,exist_ok=True)
    source=root if cohort=='fresh' else Path('artifacts/stage5_practical')
    folder=source/'batches/evaluation';declaration=json.loads((folder/'declaration.json').read_text())
    cases={c['case_id']:c for c in json.loads((source/'cases.json').read_text())['cases']}
    estimator=RetailRisk.load(json.loads((root/'estimator.json').read_text()))
    assert estimator.estimator_hash==declaration['estimator_hash']
    data=load_database();outcomes=[];jobs=[];dispatches=[];sequences=[];missing=[];all_prepared=[];historical_matches=0
    for bundle in declaration['bundles']:
        key=bundle['bundle_id']+'_r'+str(bundle['replicate']);prepared_path=folder/'prepared'/key/'workflows.json'
        if not prepared_path.exists():
            missing.append(key)
            continue
        prepared=json.loads(prepared_path.read_text());all_prepared.extend(prepared)
        databases={s['case_id']:account_database(data,cases[s['case_id']]['user_id']) for s in bundle['slots']}
        index=int(bundle['bundle_id'].rsplit('_',1)[1]);results={}
        for variant in VARIANTS:
            for duration in declaration['duration_order'][index]:
                for policy in declaration['policy_order'][index]:
                    result=simulate(bundle,prepared,cases,databases,estimator,policy,duration,variant)
                    trace=out/'traces'/key/(variant+'_s%d_%s.json.gz'%(duration,policy));trace.parent.mkdir(parents=True,exist_ok=True)
                    if cohort=='post_hoc_stage5' and variant=='reference':
                        old=json.loads(gzip.decompress((folder/'analysis/traces'/key/('s%d_%s.json.gz'%(duration,policy))).read_bytes()))
                        comparable=copy.deepcopy(result)
                        for k in ('variant','blocked_unresolved','unstaged_failures'):comparable.pop(k)
                        for row in comparable['jobs']:row.pop('blocked_unresolved')
                        assert without_timing(comparable)==without_timing(old)
                        historical_matches+=1
                    if trace.exists():
                        saved=json.loads(gzip.decompress(trace.read_bytes()));assert without_timing(saved)==without_timing(result);result=saved
                    else:
                        trace.write_bytes(gzip.compress((canonical(result)+'\n').encode(),mtime=0))
                        replay=simulate(bundle,prepared,cases,databases,estimator,policy,duration,variant)
                        assert without_timing(result)==without_timing(replay)
                    results[(variant,duration,policy)]=result
                    row={k:v for k,v in result.items() if k not in ('events','jobs','review_sequence')}
                    ds=[e for e in result['events'] if e['event']=='dispatch']
                    row['planning_seconds']=sum(e['planning_seconds'] for e in ds)
                    row['max_planning_seconds']=max(e['planning_seconds'] for e in ds)
                    outcomes.append(row)
                    for job in result['jobs']:jobs.append(dict(bundle_id=bundle['bundle_id'],replicate=bundle['replicate'],variant=variant,review_duration=duration,policy=policy,**job))
                    for e in ds:
                        assert all('initial_error' not in r and 'target_action' not in r for r in e['public_pending'])
                        dispatches.append(dict(bundle_id=bundle['bundle_id'],replicate=bundle['replicate'],variant=variant,review_duration=duration,policy=policy,
                            tick=e['tick'],eligible=len(e['eligible']),selected=e['selected'],greedy_choice=e['greedy_choice'],search_choice=e['search_choice'],
                            planning_seconds=e['planning_seconds'],ordered_subsets_evaluated=e['ordered_subsets_evaluated']))
                for other in ('greedy','edf'):
                    a=results[(variant,duration,'search')];b=results[(variant,duration,other)]
                    sequences.append(dict(bundle_id=bundle['bundle_id'],replicate=bundle['replicate'],variant=variant,review_duration=duration,
                        comparator=other,sequences_differ=a['review_sequence']!=b['review_sequence'],search_sequence=';'.join(a['review_sequence']),other_sequence=';'.join(b['review_sequence'])))
        initial_correct=sum(p['initial_task_success'] for p in prepared)
        for duration in (1,2):
            original=results[('reference',duration,'no_review')]
            for variant in VARIANTS:
                other=results[(variant,duration,'no_review')]
                for m in METRICS:
                    if m not in ('multi_eligible_dispatches','greedy_search_different_heads'):assert original[m]==other[m],(variant,m)
            for policy in POLICIES:
                restricted=results[('approve_block',duration,policy)]
                assert restricted['task_completed']==initial_correct and restricted['corrections']==0
                assert restricted['service_failure_loss']==4*(3-initial_correct)
                assert all(not j['blocked_unresolved'] or (j['initial_error'] and not j['task_completed'] and not j['wrong_transaction_committed']) for j in restricted['jobs'])
    csv_file(out/'episodes.csv',outcomes);csv_file(out/'jobs.csv',jobs);csv_file(out/'dispatches.csv',dispatches);csv_file(out/'sequence_comparisons.csv',sequences)
    planned=[dict(bundle_id=b['bundle_id'],replicate=b['replicate'],case_id=s['case_id'],preparation_status='incomplete' if b['bundle_id']+'_r'+str(b['replicate']) in missing else 'retained') for b in declaration['bundles'] for s in b['slots']]
    csv_file(out/'planned_workflows.csv',planned)
    complete_bundles=[b for b in sorted({r['bundle_id'] for r in outcomes}) if len([r for r in outcomes if r['bundle_id']==b])==3*3*2*6]
    complete=[r for r in outcomes if r['bundle_id'] in complete_bundles]
    means={metric:bundle_means(complete,metric) for metric in METRICS}
    rng=random.Random(20260916);indices=[[rng.randrange(len(complete_bundles)) for _ in complete_bundles] for _ in range(2000)] if complete_bundles else []
    summaries=[];pairs=[];differences=[]
    for variant in VARIANTS:
        for duration in (1,2):
            for policy in POLICIES:
                group=[r for r in outcomes if (r['variant'],r['review_duration'],r['policy'])==(variant,duration,policy)]
                if not group:continue
                summaries.append(dict(variant=variant,review_duration=duration,policy=policy,episodes=len(group),
                    **{m:sum(r[m] for r in group) for m in METRICS},mean_loss=sum(r['operational_loss'] for r in group)/len(group),
                    mean_utilization=sum(r['review_utilization'] for r in group)/len(group)))
            for other in ('greedy','edf','fcfs','uncertainty','no_review'):
                for metric in ('operational_loss','task_completed','wrong_transactions','review_busy_ticks'):
                    diffs=[means[metric][(b,(variant,duration,'search'))]-means[metric][(b,(variant,duration,other))] for b in complete_bundles]
                    result=paired_summary(diffs,indices)
                    pairs.append(dict(variant=variant,review_duration=duration,comparison='search-'+other,metric=metric,bundles=len(diffs),**result))
                    for b,d in zip(complete_bundles,diffs):differences.append(dict(bundle_id=b,variant=variant,review_duration=duration,comparison='search-'+other,metric=metric,difference=d))
    changes=[]
    for variant in ('approve_block','complexity_time'):
        for duration in (1,2):
            for policy in POLICIES:
                for metric in ('operational_loss','task_completed','wrong_transactions','review_busy_ticks'):
                    ds=[means[metric][(b,(variant,duration,policy))]-means[metric][(b,('reference',duration,policy))] for b in complete_bundles]
                    changes.append(dict(variant=variant,review_duration=duration,policy=policy,metric=metric,bundles=len(ds),**paired_summary(ds,indices)))
    csv_file(out/'policy_outcomes.csv',summaries);csv_file(out/'paired_comparisons.csv',pairs);csv_file(out/'bundle_differences.csv',differences);csv_file(out/'variant_changes.csv',changes)
    prediction,bins=prediction_metrics(all_prepared,estimator);csv_file(out/'risk_bins.csv',bins)
    variability=[]
    for case_id in sorted({r['case_id'] for r in all_prepared}):
        group=[r for r in all_prepared if r['case_id']==case_id]
        variability.append(dict(case_id=case_id,replicates=len(group),distinct_proposals=len({canonical(r['proposal']) for r in group}),
            initially_correct=sum(r['initial_task_success'] for r in group),staged=sum(r['proposal'] is not None for r in group)))
    csv_file(out/'generation_variability.csv',variability)
    primary=next((r for r in pairs if r['variant']=='approve_block' and r['review_duration']==2 and r['comparison']=='search-greedy' and r['metric']=='operational_loss'),None)
    summary=dict(status='complete' if not missing else 'incomplete',cohort=cohort,fresh_source_cases=cohort=='fresh',
        workflow_attempts=len(all_prepared),source_cases=len({r['case_id'] for r in all_prepared}),complete_bundles=len(complete_bundles),
        policy_episodes=len(outcomes),missing_bundle_replicates=missing,staged=sum(p['proposal'] is not None for p in all_prepared),
        initial_errors=sum(p['initial_error'] for p in all_prepared),unstaged=sum(p['proposal'] is None for p in all_prepared),
        initial_correct=sum(p['initial_task_success'] for p in all_prepared),primary=primary,predictions=prediction,
        historical_reference_traces_matched=historical_matches,all_policy_traces_replayed=True,
        invariances_verified=['no-review outcome invariant across variants','approve/block completion equals initially correct staging','blocking leaves service unresolved and state unchanged'],
        estimator_hash=estimator.estimator_hash,bootstrap_seed=20260916,bootstrap_resamples=2000,
        independent_unit='source-disjoint bundle; average generation replicates, common bootstrap indices across matched conditions')
    write_json(out/'summary.json',summary);return summary
