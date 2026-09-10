"""Saved-evidence audit and scenario-paired research analysis; never performs inference."""
from collections import Counter,defaultdict
from dataclasses import asdict,replace
from datetime import datetime,timedelta
import json,math
from pathlib import Path

from .client import ACTION_SCHEMA,MANUAL,parse_action
from .domain import ReviewRequest,Scenario,digest
from .estimator import file_hash
from .io import read_events,write_csv,write_json,render_trace
from .replay import replay_score
from .research_risk import ESTIMATOR_FILE_HASH,load_risk
from .research_scheduler import ResearchScheduler

COUNT_FIELDS=('scheduled_calls','attempts','retries','failed_attempts','unfinished_attempts','prompt_tokens','completion_tokens','unknown_token_attempts')
CONDITION_FIELDS=('workload','agents','review_ticks','risk','policy','closure_penalty','study')


def historical_file_status(data,expected,csv_lf_hash=None):
    """CSV line-ending portability without permitting changed values or raw evidence."""
    import hashlib
    if hashlib.sha256(data).hexdigest()==expected:return 'unchanged'
    if csv_lf_hash and hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()==csv_lf_hash:
        return 'csv_line_endings'
    return 'changed'


def existing_evidence(path):
    path=Path(path)
    return path if path.exists() else Path(str(path)+'.gz')


def audit_raw(path,config,seed):
    path=existing_evidence(path);raw=read_events(path) if path.exists() else []
    started=[r for r in raw if r['phase']=='attempt_started']
    sent=[r for r in raw if r['phase']=='inference_started']
    finished=[r for r in raw if r['phase']=='attempt_finished']
    by_id={(r['session_call_id'],r['retry']):r for r in finished}
    assert len(by_id)==len(finished),'Duplicate completed attempt'
    calls=defaultdict(list);intervals=[]
    for r in finished:
        assert r['scenario_seed']==seed and r['retry'] in (0,1) and r['sample'] in (0,1)
        metadata={k:r[k] for k in ('scenario_seed','agent_id','job_id')}
        assert r['seed']==int(digest(dict(metadata,sample=r['sample'],retry=r['retry']))[:8],16)
        assert r['request']['seed']==r['seed']
        assert r['observation_hash']==digest(json.loads(r['request']['messages'][1]['content']))
        for key,value in dict(model=config['model'],temperature=.3,top_p=1.,max_tokens=48,guided_json=ACTION_SCHEMA,n=1,stream=False).items():assert r['request'][key]==value
        assert r['request']['messages'][0]['content']==MANUAL+(' Strictly follow the one-field JSON schema; include no prose.' if r['retry'] else '')
        if 'parsed_action' in r:assert r['http_status']==200 and parse_action(r['raw_response'])==r['parsed_action']
        calls[(r['job_id'],r['sample'])].append(r)
        begin=datetime.fromisoformat(r['wall_utc']);intervals.append((begin,begin+timedelta(seconds=r['attempt_wall_seconds'])))
    for values in calls.values():assert [r['retry'] for r in values] in ([0],[0,1])
    unfinished=[r for r in started if (r['session_call_id'],r['retry']) not in by_id]
    unknown_sent=sum((r['session_call_id'],r['retry']) not in by_id for r in sent)
    counts=dict(scheduled_calls=len({r['session_call_id'] for r in started}),attempts=len(sent),
        retries=sum(r['retry']>0 for r in started),failed_attempts=sum('error' in r for r in finished),unfinished_attempts=len(unfinished),
        prompt_tokens=sum((r.get('usage') or {}).get('prompt_tokens',0) for r in finished),
        completion_tokens=sum((r.get('usage') or {}).get('completion_tokens',0) for r in finished),
        unknown_token_attempts=unknown_sent+sum(r['inference_request_attempted'] and r.get('usage') is None for r in finished))
    return counts,calls,intervals,raw


def audit_batch(root,name):
    root=Path(root);out=root/'batches'/name;analysis=out/'analysis';analysis.mkdir(exist_ok=True)
    d=json.loads((out/'declaration.json').read_text());manifest=json.loads((out/'manifest.json').read_text())
    assert digest({k:v for k,v in d.items() if k!='declaration_hash'})==d['declaration_hash']
    assert manifest['declaration_hash']==d['declaration_hash'] and d['prepared_utc']<=manifest['started_utc']
    for path,expected in d['source_files_sha256'].items():assert file_hash(out/'source'/path)==expected,path
    assert file_hash(root/'estimator.json')==ESTIMATOR_FILE_HASH
    estimates={risk:load_risk(risk,root/'estimator.json') for risk in ('frozen','pooled','analytical')}
    scenarios=json.loads((out/'scenarios.scorer-only.json').read_text())
    gpu_recheck_used=False
    for filename in ('gpu_before.json','gpu_final.json'):
        p=out/filename
        if not p.exists():assert manifest['status']!='completed';continue
        gpu=json.loads(p.read_text())
        if gpu['status']!='placement_verified' and filename=='gpu_final.json':
            # Preserve the original failed check; a separately timestamped recheck is auditable.
            assert gpu['error']=='ValueError: Server logs do not establish CUDA execution'
            recovery=json.loads((out/'gpu_final_recheck.json').read_text())
            assert recovery['captured_utc']>gpu['captured_utc']
            assert recovery['server_pid']==gpu['server_pid']
            assert recovery['serving_gpu_processes']==gpu['serving_gpu_processes']
            gpu=recovery;gpu_recheck_used=True
        assert gpu['status']=='placement_verified'
        assert gpu['model']==d['runtime_config']['model'] and gpu['revision']==d['runtime_config']['revision']
        assert gpu['cuda_runtime']['bf16_matmul_verified'] and gpu['cuda_runtime']['device_name']=='NVIDIA RTX 6000 Ada Generation'
        for flag,value in (('--dtype','bfloat16'),('--cpu-offload-gb','0'),('--swap-space','0'),('--tensor-parallel-size','1'),('--max-num-seqs','1')):assert gpu['server_arguments'][flag]==value
    episodes,predictions,agents,decisions,orders,intervals=[],[],[],[],[],[]
    request_groups=defaultdict(list);call_ids=set();attempt_ids=set();replays=0;max_context=0
    for entry in d['episodes']:
        folder=out/'episodes'/entry['run_id'];path=folder/'events.jsonl'
        counts,calls,times,raw=audit_raw(folder/'raw_requests.jsonl',d['runtime_config'],entry['seed']);intervals.extend(times)
        for r in raw:
            if r['phase']=='attempt_started':
                call_ids.add(r['session_call_id'])
            if r['phase']=='inference_started':attempt_ids.add((r['session_call_id'],r['retry']))
            if r['phase']=='attempt_finished' and 'parsed_action' in r:
                request_groups[digest(r['request'])].append(dict(run_id=entry['run_id'],call_id=r['session_call_id'],job_id=r['job_id'],sample=r['sample'],action=r['parsed_action']))
                max_context=max(max_context,json.loads(r['tokenization_response'])['count'])
        assert counts['scheduled_calls']<=entry['planned_calls'] and counts['attempts']<=2*entry['planned_calls']
        if not existing_evidence(path).exists():
            episodes.append(dict(entry,status='not_started',total_loss=None,accrued_loss=0,incorrect_jobs=None,**counts));continue
        events=read_events(path);header=events[0]
        scenario=Scenario.from_record(header['scenario']);assert scenario.hash==header['scenario_hash']==entry['scenario_hash']
        assert header['scenario']==scenarios[entry['scenario_hash']]
        assert header['policy']==entry['policy'] and header['review_ticks']==entry['review_ticks']
        assert header['planned_calls']==entry['planned_calls'] and header['estimator_hash']==estimates[entry['risk']].estimator_hash
        jobs={j.public.job_id:j for j in scenario.jobs};last=events[-1]
        complete=last['event']=='episode_finished' and last['status']=='completed'
        if last['event']=='episode_finished':
            for key in ('scheduled_calls','attempts','prompt_tokens','completion_tokens','unknown_token_attempts'):assert counts[key]==last[key],(entry['run_id'],key)
        proposals={e['job_id']:e for e in events if e['event']=='proposal'}
        observations={e['job_id']:e['public_observation'] for e in events if e['event']=='observation'}
        for job_id,e in proposals.items():
            job=jobs[job_id];obs=observations[job_id]
            assert obs['job']==json.loads(json.dumps(asdict(job.public))) and obs['tick']==job.public.release
            assert all(jobs[h['job_id']].public.agent_id==job.public.agent_id for h in obs['history'])
            assert all(h.get('review_completed_at',h.get('proposed_at'))<=job.public.release for h in obs['history'])
            a,b=(calls[(job_id,sample)][-1] for sample in (0,1))
            assert a['observation_hash']==b['observation_hash']==digest(obs)
            assert (e['primary'],e['secondary'])==(a['parsed_action'],b['parsed_action'])
            assert e['p_error']==estimates[entry['risk']].predict(job.public,e['primary'],e['secondary'])
            label=int(e['primary']!=job.correct_action)
            row=dict(entry,job_id=job_id,agent_id=job.public.agent_id,agreement=e['primary']==e['secondary'],initial_error=label,primary=e['primary'],secondary=e['secondary'],
                primary_request_hash=digest(a['request']),secondary_request_hash=digest(b['request']),observation_hash=digest(obs))
            for risk,estimator in estimates.items():
                prediction=estimator.predict(job.public,e['primary'],e['secondary']);row['p_'+risk]=prediction;row['brier_'+risk]=(prediction-label)**2
            predictions.append(row)
        replay=replay_score(path)
        if complete:assert replay['status']=='verified' and counts['scheduled_calls']==entry['planned_calls'];replays+=1
        else:assert replay['total_loss'] is None
        expired=[e for e in events if e['event']=='request_expired']
        reviews=[e for e in events if e['event']=='review_started']
        closures={e['job_id']:e for e in events if e['event']=='job_closed'}
        row=dict(entry,status='completed' if complete else 'incomplete',total_loss=last.get('total_loss') if complete else None,
            accrued_loss=last.get('accrued_loss',sum(e.get('loss',e.get('terminal_loss',0)) for e in events if e['event'] in ('interval_scored','job_closed'))),
            correct_jobs=last.get('correct_jobs') if complete else None,incorrect_jobs=entry['jobs']-last['correct_jobs'] if complete else None,
            reviews_completed=sum(e['event']=='review_completed' for e in events),corrections=sum(e['event']=='review_completed' and e['changed'] for e in events),
            review_utilization=last.get('review_busy_ticks',0)/entry['horizon'],expired_requests=len(expired),
            initially_infeasible_expiries=sum(e['category']=='infeasible_at_arrival' for e in expired),
            zero_value_expiries=sum(e['category']=='zero_value' for e in expired),
            missed_opportunities=sum(e['category']=='opportunity_lost_while_waiting' for e in expired),
            wrong_missed_opportunities=sum(e['category']=='opportunity_lost_while_waiting' and e['initial_proposal_wrong'] for e in expired),
            max_outstanding=max((len(e['pending'])+int(e['busy'] is not None) for e in events if e['event']=='queue_snapshot'),default=0),
            episode_wall_seconds=last.get('episode_wall_seconds'),request_wall_seconds=last.get('request_wall_seconds'),**counts)
        assert row['max_outstanding']<=6
        row['augmented_loss']=row['total_loss']+entry['closure_penalty']*row['incorrect_jobs'] if complete else None
        row['objective_missed_opportunities']=sum(jobs[e['job_id']].public.release+entry['review_ticks']<=jobs[e['job_id']].public.deadline and
            jobs[e['job_id']].public.cost_per_tick*(jobs[e['job_id']].public.deadline-jobs[e['job_id']].public.release-entry['review_ticks'])+jobs[e['job_id']].public.terminal_cost+entry['closure_penalty']>0 for e in expired)
        episodes.append(row)
        for agent in range(entry['agents']):
            js=[j.public.job_id for j in scenario.jobs if j.public.agent_id==agent]
            agents.append(dict(entry,agent_id=agent,status=row['status'],jobs=len(js),closed_jobs=sum(j in closures for j in js),
                loss=sum(closures[j]['job_loss'] for j in js if j in closures) if complete else None,
                incorrect_jobs=sum(not closures[j]['correct'] for j in js if j in closures) if complete else None,
                initial_errors=sum(proposals[j]['primary']!=jobs[j].correct_action for j in js if j in proposals),
                corrections=sum(e['event']=='review_completed' and e['changed'] and e['job_id'] in js for e in events)))
        orders.append(dict(entry,status=row['status'],review_order=[e['job_id'] for e in reviews],timed_order=[(e['tick'],e['job_id']) for e in reviews]))
        for e in events:
            if e['event']!='planning_decision':continue
            requests=tuple(ReviewRequest(**r) for r in e['public_pending'])
            assert all(r.requested_at<=e['tick'] for r in requests)
            for r in requests:
                p=jobs[r.job_id].public;assert (r.deadline,r.cost_per_tick,r.terminal_cost)==(p.deadline,p.cost_per_tick,p.terminal_cost)
            verifier=ResearchScheduler(entry['policy'],entry['closure_penalty'])
            assert verifier(requests,e['tick'])==e['selected']
            assert verifier.last_record['eligible']==e['eligible']
            assert verifier.last_record['ordered_subsets_evaluated']==e['ordered_subsets_evaluated']
            assert e['planning_seconds']>=0
            decision=dict(entry,tick=e['tick'],pending_count=e['pending_count'],eligible_count=e['eligible_count'],selected=e['selected'],planning_seconds=e['planning_seconds'],ordered_subsets_evaluated=e['ordered_subsets_evaluated'])
            for risk,estimator in estimates.items():
                altered=tuple(replace(r,p_error=estimator.predict(jobs[r.job_id].public,proposals[r.job_id]['primary'],proposals[r.job_id]['secondary'])) for r in requests)
                for policy in ('greedy','delay','edf'):
                    decision['choice_'+risk+'_'+policy]=ResearchScheduler(policy,entry['closure_penalty'])(altered,e['tick'])
            decisions.append(decision)
    intervals.sort();assert all(a[1]<=b[0]+timedelta(milliseconds=1) for a,b in zip(intervals,intervals[1:]))
    totals={field:sum(e[field] for e in episodes) for field in COUNT_FIELDS}
    for field in ('scheduled_calls','attempts','prompt_tokens','completion_tokens','unknown_token_attempts'):assert totals[field]==manifest[field]
    assert totals['scheduled_calls']==len(call_ids) and totals['attempts']==len(attempt_ids)
    metrics_verified=False
    if not totals['failed_attempts'] and not totals['unknown_token_attempts'] and (out/'metrics_after.txt').exists():
        def metric(suffix,metric_name):return sum(float(line.rsplit(' ',1)[1]) for line in (out/('metrics_'+suffix+'.txt')).read_text().splitlines() if line.startswith(metric_name+'{'))
        for metric_name,field in (('vllm:request_success_total','attempts'),('vllm:prompt_tokens_total','prompt_tokens'),('vllm:generation_tokens_total','completion_tokens')):assert metric('after',metric_name)-metric('before',metric_name)==totals[field]
        metrics_verified=True
    mixed=[dict(request_hash=key,observations=values) for key,values in request_groups.items() if len({r['action'] for r in values})>1]
    summary=dict(status='verified',batch=name,planned_episodes=len(d['episodes']),completed_replays=replays,counts=totals,
        source_snapshot_verified=True,estimator_hash_verified=True,serial_requests_verified=True,server_metrics_verified=metrics_verified,gpu_recheck_used=gpu_recheck_used,
        max_input_tokens=max_context,max_outstanding=max((r.get('max_outstanding',0) for r in episodes),default=0),
        max_eligible=max((r['eligible_count'] for r in decisions),default=0),max_search_orders=max((r['ordered_subsets_evaluated'] for r in decisions),default=0),
        distinct_request_groups=len(request_groups),repeated_request_groups=sum(len(v)>1 for v in request_groups.values()),mixed_action_groups=len(mixed),
        mixed_primary_groups=sum(v['observations'][0]['sample']==0 for v in mixed),
        episodes_in_mixed_groups=len({r['run_id'] for v in mixed for r in v['observations']}))
    for filename,records in (('episodes',episodes),('predictions',predictions),('per_agent',agents),('decisions',decisions),('review_orders',orders)):write_csv(analysis/(filename+'.csv'),records)
    write_json(analysis/'audit.json',summary);write_json(analysis/'request_variation.json',mixed)
    return summary


def read_csv(path):
    import csv
    with Path(path).open(newline='') as handle:return list(csv.DictReader(handle))


def numeric_records(path):
    rows=read_csv(path)
    integers=('seed','agents','review_ticks','closure_penalty','jobs','horizon','execution_index','planned_calls','correct_jobs','incorrect_jobs','reviews_completed','corrections','expired_requests','initially_infeasible_expiries','zero_value_expiries','missed_opportunities','wrong_missed_opportunities','objective_missed_opportunities','max_outstanding','agent_id','closed_jobs','initial_errors','tick','pending_count','eligible_count','ordered_subsets_evaluated','initial_error')+COUNT_FIELDS
    for row in rows:
        for key,value in list(row.items()):
            if value=='':row[key]=None
            elif key in integers:row[key]=int(value)
            elif key in ('total_loss','accrued_loss','loss_upper_bound','augmented_loss','review_utilization','episode_wall_seconds','request_wall_seconds','planning_seconds','loss') or key.startswith(('p_','brier_')):row[key]=float(value)
            elif key=='agreement':row[key]=(value=='True')
    return rows


def condition(row):
    study=row.get('study') or ('objective' if row.get('phase','').startswith('objective_') else 'core')
    return tuple(row[key] for key in CONDITION_FIELDS[:-1])+(study,)


def condition_label(key):
    return '{}|a{}|s{}|{}|{}|lambda{}'.format(*key[:6])+('' if key[6]=='core' else '|'+key[6])


_BOOTSTRAP_INDICES={}
def paired_interval(values,seeds):
    """Same scenario-index draws for every comparison on the same scenario prefix."""
    import numpy as np
    if not values:return (None,None)
    key=tuple(seeds)
    if key not in _BOOTSTRAP_INDICES:
        _BOOTSTRAP_INDICES[key]=np.random.RandomState(20260910).randint(0,len(seeds),size=(2000,len(seeds)))
    averages=np.asarray(values,dtype=float)[_BOOTSTRAP_INDICES[key]].mean(axis=1)
    return tuple(float(x) for x in np.percentile(averages,[2.5,97.5]))


def summarize_batches(root,names,label):
    import numpy as np
    root=Path(root);out=root/'summaries'/label;out.mkdir(parents=True,exist_ok=True)
    episodes,predictions,agents,decisions,orders=[],[],[],[],[]
    for name in names:
        folder=root/'batches'/name/'analysis'
        episodes+=numeric_records(folder/'episodes.csv');predictions+=numeric_records(folder/'predictions.csv')
        agents+=numeric_records(folder/'per_agent.csv');decisions+=numeric_records(folder/'decisions.csv');orders+=read_csv(folder/'review_orders.csv')
    groups=defaultdict(list)
    for row in episodes:groups[condition(row)].append(row)
    outcomes=[]
    for key,group in sorted(groups.items()):
        if len(group)!=len({r['seed'] for r in group}):
            raise ValueError('Duplicate scenario within a study condition: '+condition_label(key))
        complete=[r for r in group if r['status']=='completed'];n=len(complete)
        losses=[r['total_loss'] for r in complete];seeds=[r['seed'] for r in complete]
        low,high=paired_interval(losses,seeds)
        ds=[r for r in decisions if condition(r)==key and r['eligible_count']>0]
        ag=[r for r in agents if condition(r)==key and r['status']=='completed']
        total_jobs=sum(r['jobs'] for r in complete)
        row=dict(zip(CONDITION_FIELDS,key),planned_episodes=len(group),completed_episodes=n,total_loss=sum(losses),mean_loss=sum(losses)/n if n else None,
            mean_loss_ci_low=low,mean_loss_ci_high=high,mean_loss_per_job=sum(losses)/total_jobs if total_jobs else None,
            correct_jobs=sum(r['correct_jobs'] for r in complete),incorrect_jobs=sum(r['incorrect_jobs'] for r in complete),jobs=total_jobs,
            mean_incorrect_jobs=sum(r['incorrect_jobs'] for r in complete)/n if n else None,
            corrections=sum(r['corrections'] for r in complete),reviews_completed=sum(r['reviews_completed'] for r in complete),
            review_utilization=sum(r['review_utilization'] for r in complete)/n if n else None,
            initially_infeasible_expiries=sum(r['initially_infeasible_expiries'] for r in complete),
            zero_value_expiries=sum(r['zero_value_expiries'] for r in complete),
            missed_opportunities=sum(r['missed_opportunities'] for r in complete),wrong_missed_opportunities=sum(r['wrong_missed_opportunities'] for r in complete),
            objective_missed_opportunities=sum(r['objective_missed_opportunities'] for r in complete),
            mean_augmented_loss=sum(r['augmented_loss'] for r in complete)/n if n else None,
            dispatch_opportunities=len(ds),competitive_dispatches=sum(r['eligible_count']>=2 for r in ds),
            same_state_search_greedy_differences=sum(r['choice_'+key[3]+'_delay']!=r['choice_'+key[3]+'_greedy'] for r in ds),
            same_state_search_edf_differences=sum(r['choice_'+key[3]+'_delay']!=r['choice_'+key[3]+'_edf'] for r in ds),
            analytical_search_choice_changes=sum(r['choice_frozen_delay']!=r['choice_analytical_delay'] for r in ds),
            pooled_search_choice_changes=sum(r['choice_frozen_delay']!=r['choice_pooled_delay'] for r in ds),
            max_agent_loss=max((r['loss'] for r in ag),default=None),max_agent_incorrect=max((r['incorrect_jobs'] for r in ag),default=None))
        for weight in (0,4,8):row['mean_common_objective_'+str(weight)]=sum(r['total_loss']+weight*r['incorrect_jobs'] for r in complete)/n if n else None
        outcomes.append(row)
    prediction_summary=[];reliability=[]
    pgroups=defaultdict(list)
    for row in predictions:pgroups[condition(row)].append(row)
    for key,group in sorted(pgroups.items()):
        for scoring_risk in ('frozen','pooled','analytical'):
            for agreement in ('all','agree','disagree'):
                selected=[r for r in group if agreement=='all' or r['agreement']==(agreement=='agree')]
                n=len(selected)
                prediction_summary.append(dict(zip(CONDITION_FIELDS,key),scoring_risk=scoring_risk,agreement_bin=agreement,examples=n,
                    errors=sum(r['initial_error'] for r in selected),observed_error_rate=sum(r['initial_error'] for r in selected)/n if n else None,
                    mean_prediction=sum(r['p_'+scoring_risk] for r in selected)/n if n else None,brier=sum(r['brier_'+scoring_risk] for r in selected)/n if n else None))
            bins=defaultdict(list)
            for row in group:bins[round(row['p_'+scoring_risk],12)].append(row)
            for prediction,selected in sorted(bins.items()):reliability.append(dict(zip(CONDITION_FIELDS,key),scoring_risk=scoring_risk,prediction=prediction,examples=len(selected),observed_error_rate=sum(r['initial_error'] for r in selected)/len(selected)))
    # Include reference rows from replication when comparing the ablation prefix.
    by_condition={key:{r['seed']:r for r in values} for key,values in groups.items()}
    by_actions=defaultdict(lambda:defaultdict(dict))
    for row in predictions:by_actions[condition(row)][row['seed']][row['job_id']]=row
    by_order={condition(r):{} for r in episodes}
    for row in orders:
        for field in ('agents','review_ticks','closure_penalty','seed'):row[field]=int(row[field])
        # CSV serializes a Python list; parse only saved local evidence, never eval().
        import ast
        by_order[condition(row)][row['seed']]=ast.literal_eval(row['review_order'])
    comparisons,paired=[],[]
    comparison_keys=[]
    for key in groups:
        workload,agent_count,duration,risk,policy,penalty,study=key
        if policy=='delay':
            for comparator in ('greedy','edf','fcfs','uncertainty','myopic'):
                other=(workload,agent_count,duration,risk,comparator,penalty,study)
                if other in groups:comparison_keys.append(('policy',key,other))
        if risk in ('pooled','analytical'):
            other=(workload,agent_count,duration,'frozen',policy,penalty,study)
            if other in groups:comparison_keys.append(('risk',key,other))
        if penalty in (4,8):
            other=(workload,agent_count,duration,risk,policy,0,study)
            if other in groups:comparison_keys.append(('objective',key,other))
        if duration==2:
            other=(workload,agent_count,1,risk,policy,penalty,study)
            if other in groups:comparison_keys.append(('duration',key,other))
        if agent_count==6:
            other=(workload,3,duration,risk,policy,penalty,study)
            if other in groups:comparison_keys.append(('capacity',key,other))
    for kind,left,right in sorted(set(comparison_keys)):
        common=sorted(set(by_condition[left])&set(by_condition[right]));valid=[];losses=[];wrong=[];norm=[];seq=[]
        for seed in common:
            a,b=by_condition[left][seed],by_condition[right][seed]
            complete=a['status']==b['status']=='completed'
            delta=a['total_loss']-b['total_loss'] if complete else None
            item=dict(kind=kind,study=left[6],workload=left[0],seed=seed,left=condition_label(left),right=condition_label(right),review_ticks=left[2],risk=left[3],agents=left[1],
                loss_difference=delta,incorrect_difference=a['incorrect_jobs']-b['incorrect_jobs'] if complete else None,
                loss_per_job_difference=a['total_loss']/a['jobs']-b['total_loss']/b['jobs'] if complete else None,
                lower_bound=delta if complete else (a['accrued_loss'] or 0)-b['loss_upper_bound'],
                upper_bound=delta if complete else a['loss_upper_bound']-(b['accrued_loss'] or 0))
            aj,bj=by_actions[left][seed],by_actions[right][seed]
            common_jobs=sorted(set(aj)&set(bj))
            item.update(paired_jobs=len(common_jobs),
                primary_action_differences=sum(aj[j]['primary']!=bj[j]['primary'] for j in common_jobs),
                secondary_action_differences=sum(aj[j]['secondary']!=bj[j]['secondary'] for j in common_jobs),
                different_observations=sum(aj[j]['observation_hash']!=bj[j]['observation_hash'] for j in common_jobs),
                identical_request_primary_differences=sum(aj[j]['primary_request_hash']==bj[j]['primary_request_hash'] and aj[j]['primary']!=bj[j]['primary'] for j in common_jobs))
            paired.append(item)
            if complete:
                valid.append(seed);losses.append(delta);wrong.append(item['incorrect_difference']);norm.append(item['loss_per_job_difference'])
                seq.append(by_order[left][seed]!=by_order[right][seed])
        low,high=paired_interval(losses,valid);wl,wh=paired_interval(wrong,valid);nl,nh=paired_interval(norm,valid)
        primary=kind=='policy' and left[0] in ('original','competition') and left[2]==2 and left[3]=='frozen' and right[4]=='greedy' and left[5]==0 and left[6]=='core'
        comparison=dict(kind=kind,study=left[6],workload=left[0],agents=left[1],review_ticks=left[2],risk=left[3],left=condition_label(left),right=condition_label(right),primary=primary,
            planned_pairs=len(common),completed_pairs=len(valid),mean_loss_difference=sum(losses)/len(losses) if losses else None,ci_low=low,ci_high=high,
            left_wins=sum(x<0 for x in losses),ties=sum(x==0 for x in losses),left_losses=sum(x>0 for x in losses),actual_order_differences=sum(seq),
            mean_incorrect_difference=sum(wrong)/len(wrong) if wrong else None,incorrect_ci_low=wl,incorrect_ci_high=wh,
            mean_loss_per_job_difference=sum(norm)/len(norm) if norm else None,per_job_ci_low=nl,per_job_ci_high=nh,
            lower_loss_more_incorrect=sum(x<0 and y>0 for x,y in zip(losses,wrong)),
            lower_incorrect_higher_loss=sum(x>0 and y<0 for x,y in zip(losses,wrong)))
        for weight in (0,4,8):
            values=[loss+weight*incorrect for loss,incorrect in zip(losses,wrong)]
            l,u=paired_interval(values,valid)
            comparison.update({'common_objective_'+str(weight)+'_difference':sum(values)/len(values) if values else None,
                'common_objective_'+str(weight)+'_ci_low':l,'common_objective_'+str(weight)+'_ci_high':u})
        comparisons.append(comparison)
    planning=[];pg=defaultdict(list)
    for row in decisions:pg[(row['policy'],row['pending_count'],row['eligible_count'])].append(row)
    for key,group in sorted(pg.items()):
        times=[r['planning_seconds'] for r in group]
        planning.append(dict(policy=key[0],pending_count=key[1],eligible_count=key[2],decisions=len(group),mean_seconds=float(np.mean(times)),p50_seconds=float(np.percentile(times,50)),p95_seconds=float(np.percentile(times,95)),max_seconds=max(times),
            mean_orders=sum(r['ordered_subsets_evaluated'] for r in group)/len(group),max_orders=max(r['ordered_subsets_evaluated'] for r in group)))
    per_agent=[];agroups=defaultdict(list)
    for row in agents:
        if row['status']=='completed':agroups[(condition(row),row['agent_id'])].append(row)
    for (key,agent),group in sorted(agroups.items()):
        per_agent.append(dict(zip(CONDITION_FIELDS,key),agent_id=agent,episodes=len(group),total_loss=sum(r['loss'] for r in group),mean_loss=float(np.mean([r['loss'] for r in group])),
            p90_loss=float(np.percentile([r['loss'] for r in group],90)),max_loss=max(r['loss'] for r in group),incorrect_jobs=sum(r['incorrect_jobs'] for r in group),
            mean_incorrect_jobs=float(np.mean([r['incorrect_jobs'] for r in group])),max_incorrect_jobs=max(r['incorrect_jobs'] for r in group)))
    for name,rows in (('policy_outcomes',outcomes),('prediction_quality',prediction_summary),('reliability',reliability),('paired_comparisons',comparisons),('paired_scenarios',paired),('planning_effort',planning),('per_agent_summary',per_agent)):
        write_csv(out/(name+'.csv'),rows)
    summary=dict(label=label,batches=names,planned_episodes=len(episodes),completed_episodes=sum(r['status']=='completed' for r in episodes),
        counts={key:sum(r[key] for r in episodes) for key in COUNT_FIELDS},bootstrap_resamples=2000,bootstrap_seed=20260910,bootstrap_unit='scenario; paired conditions resampled together',
        primary_comparisons=[r for r in comparisons if r['primary']],policy_outcomes=outcomes,
        note='Workload distributions analyzed separately. Secondary comparisons are exploratory; percentile 95% intervals are not multiplicity-adjusted.')
    write_json(out/'summary.json',summary)
    return summary
