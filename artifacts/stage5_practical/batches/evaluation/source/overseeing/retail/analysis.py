"""Replay, calibration, paired retail outcomes and session accounting; no inference."""
from collections import Counter, defaultdict
import copy
import csv
from datetime import datetime
import gzip
import hashlib
import json
import math
from pathlib import Path
import random

from overseeing.domain import canonical,digest
from overseeing.io import write_json,read_events,utc_now
from .risk import RetailRisk,RiskFeatures,fit_development
from .scheduler import POLICIES
from .simulation import simulate
from .upstream import ROOT,VENDOR,account_database,load_database,state_hash,invoke
from .workflow import RetailWorkflow


def csv_file(path,rows):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:path.write_text('');return
    with path.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)


def prepared_rows(root,batch):
    folder=Path(root)/'batches'/batch
    return [r for p in sorted((folder/'prepared').glob('*/workflows.json')) for r in json.loads(p.read_text())]


def audit_preparation(root,batch):
    root=Path(root);folder=root/'batches'/batch;declaration=json.loads((folder/'declaration.json').read_text())
    assert digest({k:v for k,v in declaration.items() if k!='declaration_hash'})==declaration['declaration_hash']
    for path,expected in declaration['source_hashes'].items():assert hashlib.sha256((folder/'source'/path).read_bytes()).hexdigest()==expected,path
    upstream=json.loads((VENDOR/'UPSTREAM.json').read_text())
    for path,expected in upstream['files_sha256'].items():assert hashlib.sha256((VENDOR/path).read_bytes()).hexdigest()==expected,path
    case_record=json.loads((root/'cases.json').read_text())
    assert digest({k:v for k,v in case_record.items() if k!='case_manifest_hash'})==case_record['case_manifest_hash']
    assert case_record['case_manifest_hash']==declaration['case_manifest_hash']
    cases={c['case_id']:c for c in case_record['cases']};data=load_database();checked=[];raw_finished=[]
    for bundle in declaration['bundles']:
        dest=folder/'prepared'/(bundle['bundle_id']+'_r'+str(bundle['replicate']))
        if not (dest/'workflows.json').exists():continue
        rows=json.loads((dest/'workflows.json').read_text());assert len(rows)==3
        for result in rows:
            case=cases[result['case_id']];initial=account_database(data,case['user_id'])
            assert case['partition']==declaration['partition']
            workflow=RetailWorkflow(case['customer_message'],initial,declaration['config'].get('interface_revision',0))
            raw=read_events(dest/(case['case_id'].replace(':','_')+'_raw.jsonl.gz'))
            finished=[r for r in raw if r['phase']=='attempt_finished'];raw_finished.extend(finished)
            successful=[r for r in finished if 'parsed_call' in r]
            assert len(successful)>=len(result['events'])
            for step,event in enumerate(result['events']):
                request=successful[step]
                assert request['request_hash']==digest(request['request'])
                assert request['request']['messages']==workflow.messages
                assert request['parsed_call']==event['call']
                raw_call=json.loads(json.loads(request['raw_response'])['choices'][0]['message']['content'])
                assert raw_call==event['call']
                assert request['seed']==int(digest(dict(request['metadata'],retry=request['retry']))[:8],16)
                # Exact response text preserves nested JSON property order used in
                # the subsequent assistant message; canonical event dictionaries do not.
                workflow.step(raw_call);assert workflow.events[-1]==event
            replay=workflow.result(case,initial,result['failure'])
            for key in replay:assert replay[key]==result[key],(result['case_id'],key)
            counts=result['counts']
            assert counts['scheduled_calls']==len({r['session_call_id'] for r in raw})
            assert counts['attempts']==sum(r['phase']=='inference_started' for r in raw)
            for token in ('prompt_tokens','completion_tokens'):
                assert counts[token]==sum((r.get('usage') or {}).get(token,0) for r in finished)
            checked.append(dict(bundle_id=bundle['bundle_id'],replicate=bundle['replicate'],case_id=case['case_id']))
    result=dict(status='verified',verified_utc=utc_now(),replayed_workflows=len(checked),
        planned_workflows=declaration['workflow_count'],successful_generations=sum('parsed_call' in r for r in raw_finished),
        failed_attempts=sum('error' in r for r in raw_finished),attempts=sum(r['inference_request_attempted'] for r in raw_finished),
        retries=sum(r['retry']>0 for r in raw_finished),max_input_tokens=max((r.get('input_tokens',0) for r in raw_finished),default=0),
        max_output_tokens=max(((r.get('usage') or {}).get('completion_tokens',0) for r in raw_finished),default=0))
    write_json(folder/'preparation_audit.json',result);return result


def fit(root,batches):
    root=Path(root);rows=[];provenance=[]
    path=root/'estimator.json'
    if path.exists():raise FileExistsError('Frozen application estimator already exists')
    for batch in batches:
        declaration=json.loads((root/'batches'/batch/'declaration.json').read_text())
        if declaration['partition']!='development':raise ValueError('Calibration cannot receive evaluation labels')
        audit_preparation(root,batch);batch_rows=prepared_rows(root,batch);rows.extend(batch_rows)
        provenance.append(dict(batch=batch,declaration_hash=declaration['declaration_hash'],
            prepared_rows_hash=digest(batch_rows),case_ids=sorted({r['case_id'] for r in batch_rows})))
    result=fit_development(rows,dict(batches=provenance,partition='development',fitted_utc=utc_now()))
    write_json(path,result);return result


def semantic_classes(proposal,target):
    if proposal is None:return ['unstaged_failure']
    differences=[]
    if proposal['tool']!=target['tool']:differences.append('wrong_workflow_tool')
    for key,label in [('order_id','wrong_order'),('item_ids','wrong_or_incomplete_item_list'),
        ('new_item_ids','wrong_variant_mapping'),('payment_method_id','wrong_payment_method'),('reason','wrong_cancellation_reason')]:
        a=proposal['arguments'].get(key);b=target['arguments'].get(key)
        if key=='item_ids' and a is not None and b is not None:a,b=sorted(a),sorted(b)
        if a!=b:differences.append(label)
    return differences or ['other_database_difference']


def percentile(values,q):
    values=sorted(values);pos=(len(values)-1)*q;low=int(pos);high=math.ceil(pos)
    return values[low]+(values[high]-values[low])*(pos-low)


def paired_interval(differences):
    rng=random.Random(20260915);n=len(differences)
    if not n:return [None,None]
    samples=[sum(differences[rng.randrange(n)] for _ in range(n))/n for _ in range(2000)]
    return [percentile(samples,.025),percentile(samples,.975)]


def prediction_metrics(rows,estimator):
    staged=[r for r in rows if r['proposal'] is not None]
    values=[(estimator.predict(RiskFeatures(**r['features'])),int(r['initial_error'])) for r in staged]
    positive=[p for p,y in values if y];negative=[p for p,y in values if not y]
    auc=sum(1 if a>b else .5 if a==b else 0 for a in positive for b in negative)/(len(positive)*len(negative)) if positive and negative else None
    result=dict(staged_examples=len(values),initial_errors=sum(y for p,y in values),
        initial_error_rate=sum(y for p,y in values)/len(values) if values else None,
        mean_prediction=sum(p for p,y in values)/len(values) if values else None,
        brier=sum((p-y)**2 for p,y in values)/len(values) if values else None,
        pooled_brier=sum((estimator.pooled-y)**2 for p,y in values)/len(values) if values else None,
        constant_half_brier=.25 if values else None,auroc=auc)
    bins=[]
    for family in ('cancel','modify','return_exchange'):
        for uncertain in (False,True):
            group=[r for r in staged if r['features']==dict(family=family,uncertain=uncertain)]
            bins.append(dict(family=family,uncertain=uncertain,examples=len(group),errors=sum(r['initial_error'] for r in group),
                observed_error_rate=sum(r['initial_error'] for r in group)/len(group) if group else None,
                predicted_probability=estimator.predict(RiskFeatures(family,uncertain))))
    return result,bins


def score(root,batch='evaluation',estimator_path=None):
    root=Path(root);folder=root/'batches'/batch;declaration=json.loads((folder/'declaration.json').read_text())
    estimator_record=declaration.get('estimator') or json.loads(Path(estimator_path or root/'estimator.json').read_text())
    estimator=RetailRisk.load(estimator_record)
    if declaration['partition']=='evaluation':assert estimator.estimator_hash==declaration['estimator_hash']
    cases={c['case_id']:c for c in json.loads((root/'cases.json').read_text())['cases']};data=load_database()
    output=folder/'analysis';output.mkdir(exist_ok=True);outcomes=[];job_rows=[];sequence_rows=[];all_prepared=[];missing=[];ideal=[];dispatch_rows=[]
    def without_timings(value):
        if isinstance(value,dict):return {k:without_timings(v) for k,v in value.items() if k!='planning_seconds'}
        if isinstance(value,list):return [without_timings(v) for v in value]
        return value
    for bundle in declaration['bundles']:
        key=bundle['bundle_id']+'_r'+str(bundle['replicate']);path=folder/'prepared'/key/'workflows.json'
        if not path.exists():missing.append(key);continue
        prepared=json.loads(path.read_text());all_prepared.extend(prepared)
        databases={slot['case_id']:account_database(data,cases[slot['case_id']]['user_id']) for slot in bundle['slots']}
        index=int(bundle['bundle_id'].rsplit('_',1)[1]);results={}
        for duration in declaration['duration_order'][index]:
            for policy in declaration['policy_order'][index]:
                result=simulate(bundle,prepared,cases,databases,estimator,policy,duration)
                # Store full state-changing tool responses and deterministic trace; compression is lossless.
                trace=output/'traces'/key/('s%d_%s.json.gz'%(duration,policy));trace.parent.mkdir(parents=True,exist_ok=True)
                if trace.exists():
                    saved=json.loads(gzip.decompress(trace.read_bytes()))
                    assert without_timings(result)==without_timings(saved),'Saved policy trace differs from replay'
                    result=saved  # Preserve the first measured planning times and raw trace bytes.
                else:
                    trace.write_bytes(gzip.compress((canonical(result)+'\n').encode(),mtime=0))
                    saved=json.loads(gzip.decompress(trace.read_bytes()))
                    replay=simulate(bundle,prepared,cases,databases,estimator,policy,duration)
                    assert without_timings(saved)==without_timings(replay)
                row={k:v for k,v in result.items() if k not in ('events','jobs','review_sequence')}
                dispatches=[e for e in result['events'] if e['event']=='dispatch']
                for event in dispatches:
                    dispatch_rows.append(dict(bundle_id=bundle['bundle_id'],replicate=bundle['replicate'],
                        review_duration=duration,policy=policy,tick=event['tick'],pending=len(event['public_pending']),
                        eligible=len(event['eligible']),selected=event['selected'],greedy_choice=event['greedy_choice'],
                        search_choice=event['search_choice'],edf_choice=event['edf_choice'],
                        planning_seconds=event['planning_seconds'],ordered_subsets_evaluated=event['ordered_subsets_evaluated']))
                row.update(planning_seconds=sum(e['planning_seconds'] for e in dispatches),
                    max_planning_seconds=max(e['planning_seconds'] for e in dispatches),
                    ordered_subsets_evaluated=sum(e['ordered_subsets_evaluated'] for e in dispatches))
                outcomes.append(row);results[(duration,policy)]=result
                for job in result['jobs']:
                    job_rows.append(dict(bundle_id=bundle['bundle_id'],replicate=bundle['replicate'],policy=policy,review_duration=duration,**job))
            for other in ('greedy','edf'):
                a=results[(duration,'search')];b=results[(duration,other)]
                sequence_rows.append(dict(bundle_id=bundle['bundle_id'],replicate=bundle['replicate'],review_duration=duration,
                    comparator=other,sequences_differ=a['review_sequence']!=b['review_sequence'],
                    search_sequence=';'.join(a['review_sequence']),other_sequence=';'.join(b['review_sequence']),
                    loss_difference=a['operational_loss']-b['operational_loss']))
        # Inexpensive idealized parallel-review reference: every staged request gets
        # its own perfect reviewer. No extra inference or claim of feasible staffing.
        ideal.append(dict(bundle_id=bundle['bundle_id'],replicate=bundle['replicate'],
            policy='unlimited_perfect_review',operational_loss=4*sum(r['proposal'] is None for r in prepared),
            task_completed=sum(r['proposal'] is not None for r in prepared),
            reviewers_needed=sum(r['proposal'] is not None for r in prepared),
            note='Parallel perfect reviews finish before all declared cutoffs; unstaged failures remain'))
    csv_file(output/'episodes.csv',outcomes);csv_file(output/'jobs.csv',job_rows);csv_file(output/'sequence_comparisons.csv',sequence_rows)
    csv_file(output/'dispatches.csv',dispatch_rows)
    planning=[]
    for policy in POLICIES:
        for size in range(4):
            group=[r for r in dispatch_rows if r['policy']==policy and r['eligible']==size]
            if group:
                values=[r['planning_seconds']*1000 for r in group]
                planning.append(dict(policy=policy,eligible_requests=size,dispatches=len(group),
                    mean_ms=sum(values)/len(values),p50_ms=percentile(values,.5),p95_ms=percentile(values,.95),
                    max_ms=max(values),max_ordered_subsets=max(r['ordered_subsets_evaluated'] for r in group)))
    csv_file(output/'planning_costs.csv',planning)
    csv_file(output/'unlimited_reference.csv',ideal)
    summaries=[];pairs=[];bundle_metrics=[]
    for duration in (1,2):
        for policy in POLICIES:
            group=[r for r in outcomes if r['review_duration']==duration and r['policy']==policy]
            if not group:continue
            summaries.append(dict(review_duration=duration,policy=policy,episodes=len(group),
                scenario_bundles=len({r['bundle_id'] for r in group}),
                **{k:sum(r[k] for r in group) for k in ('operational_loss','task_completed','wrong_transactions','service_failure_loss','wrong_transaction_loss','completed_reviews','corrections','expired_useful_opportunities','multi_eligible_dispatches','greedy_search_different_heads')},
                mean_loss=sum(r['operational_loss'] for r in group)/len(group),
                mean_utilization=sum(r['review_utilization'] for r in group)/len(group),
                mean_waiting=sum(r['total_waiting_ticks'] for r in group)/max(1,sum(r['completed_reviews'] for r in group)),
                max_planning_ms=max(r['max_planning_seconds'] for r in group)*1000))
        for other in ('greedy','edf','fcfs','uncertainty','no_review'):
            differences=[]
            for bundle_id in sorted({r['bundle_id'] for r in outcomes}):
                group=[r for r in outcomes if r['review_duration']==duration and r['bundle_id']==bundle_id]
                a={r['replicate']:r for r in group if r['policy']=='search'};b={r['replicate']:r for r in group if r['policy']==other}
                assert set(a)==set(b)
                diffs=[a[rep]['operational_loss']-b[rep]['operational_loss'] for rep in sorted(a)]
                if len(diffs)!=len({b['replicate'] for b in declaration['bundles']}):continue
                mean=sum(diffs)/len(diffs);differences.append(mean)
                bundle_metrics.append(dict(bundle_id=bundle_id,review_duration=duration,comparator=other,
                    mean_search_minus_other=mean,replicates=len(diffs)))
            if differences:
                ci=paired_interval(differences)
                pairs.append(dict(review_duration=duration,comparison='search-'+other,bundles=len(differences),
                    mean_difference=sum(differences)/len(differences),ci_low=ci[0],ci_high=ci[1],
                    search_wins=sum(d<0 for d in differences),ties=sum(d==0 for d in differences),search_losses=sum(d>0 for d in differences)))
    csv_file(output/'policy_outcomes.csv',summaries);csv_file(output/'paired_comparisons.csv',pairs);csv_file(output/'paired_bundle_differences.csv',bundle_metrics)
    prediction,bins=prediction_metrics(all_prepared,estimator);csv_file(output/'risk_bins.csv',bins)
    variability=[]
    for case_id in sorted({r['case_id'] for r in all_prepared}):
        group=[r for r in all_prepared if r['case_id']==case_id]
        variability.append(dict(case_id=case_id,replicates=len(group),distinct_proposals=len({canonical(r['proposal']) for r in group}),
            successful_tasks=sum(r['initial_task_success'] for r in group),staged=sum(r['proposal'] is not None for r in group)))
    csv_file(output/'generation_variability.csv',variability)
    errors=[]
    for r in all_prepared:
        if r['initial_error'] or r['proposal'] is None:
            errors.append(dict(bundle_id=r['bundle_id'],replicate=r['replicate'],case_id=r['case_id'],
                status=r['status'],error_classes=';'.join(semantic_classes(r['proposal'],cases[r['case_id']]['target_action'])),failure=r['failure']))
    csv_file(output/'workflow_errors.csv',errors)
    counts={k:sum(r['counts'][k] for r in all_prepared) for k in ('scheduled_calls','attempts','prompt_tokens','completion_tokens','unknown_token_attempts','request_wall_seconds')}
    summary=dict(status='complete' if not missing else 'incomplete',scored_policy_episodes=len(outcomes),
        unique_live_workflows=len(all_prepared),source_cases=len({r['case_id'] for r in all_prepared}),
        scenario_bundles=len({r['bundle_id'] for r in all_prepared}),
        failed_workflows=sum(r['proposal'] is None for r in all_prepared),
        staged_workflows=sum(r['proposal'] is not None for r in all_prepared),
        automatic_rejections=sum(r['automatic_rejections'] for r in all_prepared),
        policy_outcomes=summaries,paired_comparisons=pairs,predictions=prediction,
        cases_with_variable_proposals=sum(r['distinct_proposals']>1 for r in variability),
        cases_with_variable_task_success=sum(0<r['successful_tasks']<r['replicates'] for r in variability),
        counts=counts,missing_bundle_replicates=missing,estimator_hash=estimator.estimator_hash,
        all_completed_policy_traces_replayed=True,unlimited_reference_mean_loss=sum(r['operational_loss'] for r in ideal)/len(ideal) if ideal else None)
    write_json(output/'summary.json',summary);return summary
