"""Regenerate tables from immutable outputs and replay all recorded logical events."""
import csv
import json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from .offline import labels
from research.adaptive_correction_transfer.scoring import score
from .common import ART,ROOT,read,write,digest
from .protocol import replay
from .inference import messages
from .transport import client
from research.adaptive_correction_transfer.answers import prepare

def table(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    if not rows:path.write_text('');return
    with path.open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def interval(values,seed=91273):
    a=np.array(values,float);rng=np.random.default_rng(seed)
    samples=a[rng.integers(len(a),size=(2000,len(a)))].mean(axis=1)
    return [float(x) for x in np.quantile(samples,[.025,.975])]

def quantiles(x):
    return dict(n=len(x),median=float(np.median(x)) if x else None,p95=float(np.quantile(x,.95)) if x else None,max=float(max(x)) if x else None)

def main():
    m=read(ART/'frozen/manifest.json');gold=labels();quality=[]
    for c in m['contexts']:
        for rep in range(2):
            for q in c['questions']:
                row=read(ART/'prepared'/f"primary_r{rep}_{q['id']}.json")
                raw=read(ART/'raw'/(row['call_id']+'.json'));assert raw['request']['messages']==messages(c,q);assert raw['request_sha256']==digest(raw['request']);assert prepare(client.parsed(raw),c)==row['output']
                sc=score(row['output'],gold[c['id']][q['id']]);quality.append(dict(context_id=c['id'],question_id=q['id'],replica=rep,**sc,
                    parse_valid=int(row['output']['valid']),generation_seconds=row['generation_seconds'],prompt_tokens=row['prompt_tokens'],completion_tokens=row['completion_tokens']))
    table(ART/'tables/answer_quality.csv',quality)
    means=[]
    for c in m['contexts']:
        rows=[q for q in quality if q['context_id']==c['id']];means.append(sum(q['joint'] for q in rows)/len(rows))
    answers=dict(source_contexts=24,original_questions=len(quality)//2,generated_answers=len(quality),
        **{key:sum(q[key] for q in quality) for key in ['em','f1','joint','scale','unfinished','parse_valid']},
        context_mean_joint=float(np.mean(means)),context_mean_joint_95=interval(means))
    write(ART/'tables/answer_summary.json',answers)
    runs=[];checkpoints=[];verified=0;events=0;cutoff_verified=0
    for p in sorted((ART/'scenarios').glob('*.json*')):
        d=read(p);s=d['summary'];midpoint=.45
        middle=replay([e for e in d['events'] if e['at']<=midpoint],s['condition'])
        checkpoints.append(dict(bundle=s['bundle'],replica=s['replica'],condition=s['condition'],load=s['load'],at=midpoint,**middle.counts()))
        desk=replay(d['events'],s['condition']);assert digest(desk.logical())==s['final_sha256']
        cutoff=replay(d['events'][:d['cutoff_sequence']],s['condition']);assert digest(cutoff.logical())==d['cutoff_state_sha256'];assert cutoff.counts()==s['counts']
        # Verify released answers from the event state, without trusting saved summary totals.
        correct=wrong=0
        for rid,r in cutoff.state['requests'].items():
            if cutoff.current_released(rid):
                t=cutoff.state['tasks'][rid];sc=score(r['versions'][str(r['current_version'])]['output'],gold[t['source']['id']][t['question_id']]);correct+=sc['joint'];wrong+=1-sc['joint']
        assert correct==s['correct_released'] and wrong==s['wrong_released']
        verified+=1;cutoff_verified+=1;events+=len(d['events']);runs.append(s)
    assert len({q['question_id'] for q in quality})==145
    assert len(runs)==144,('Incomplete declared matrix',len(runs))
    write(ART/'software_summary.json',runs)
    table(ART/'tables/pause_checkpoint.csv',checkpoints)
    flat=[dict(bundle=s['bundle'],replica=s['replica'],condition=s['condition'],load=s['load'],**s['counts'],correct_released=s['correct_released'],wrong_released=s['wrong_released'],peak_queued=s['peak_queued'],mean_wait_seconds=s['mean_wait_seconds'],events=s['events'],stable_checks=s['active_stability_checks'],stability_failures=s['active_stability_checks']-s['active_stability_passed']) for s in runs]
    table(ART/'tables/scenarios.csv',flat)
    grouped=[]
    for cond in ('threads','queue','sessions'):
        for load in ('lower','higher'):
            ss=[s for s in runs if s['condition']==cond and s['load']==load]
            row=dict(condition=cond,load=load,episodes=len(ss),source_contexts=24)
            for key in ['offered','admitted','started','received','unstarted','in_flight','queued','active','deferred','unresolved','resolved','withdrawn','released','remaining']:row[key]=sum(s['counts'][key] for s in ss)
            row.update(correct_released=sum(s['correct_released'] for s in ss),wrong_released=sum(s['wrong_released'] for s in ss),mean_peak_queued=float(np.mean([s['peak_queued'] for s in ss])),mean_wait_seconds=float(np.mean([s['mean_wait_seconds'] for s in ss])),command_errors=sum(len(s['command_errors'])+len(s['driver_errors']) for s in ss))
            grouped.append(row)
    table(ART/'tables/conditions.csv',grouped)
    paired=[];contrasts=[]
    for load in ('lower','higher'):
        for metric in ('correct_released','remaining','peak_queued'):
            ds=[]
            for bundle in range(12):
                def mean(cond):
                    ss=[s for s in runs if s['condition']==cond and s['load']==load and s['bundle']==bundle]
                    return np.mean([s[metric] if metric in s else s['counts'][metric] for s in ss])
                delta=float(mean('sessions')-mean('queue'));ds.append(delta);paired.append(dict(bundle=bundle,load=load,metric=metric,sessions_minus_queue=delta))
            contrasts.append(dict(load=load,metric=metric,mean=float(np.mean(ds)),ci95=interval(ds),positive=sum(d>0 for d in ds),ties=sum(d==0 for d in ds),negative=sum(d<0 for d in ds),units=12))
    table(ART/'tables/paired_bundles.csv',paired);write(ART/'tables/contrasts.json',contrasts)
    browser=read(ART/'browser_final_verified/verification.json')
    browser_release=0
    for p in (ART/'browser_final_verified').glob('*_events.json'):
        d=read(p);assert replay(d['events'],d['condition']).logical()==d['state'];browser_release+=1
    walk=read(ART/'walkthrough/events.json');assert replay(walk['events'],walk['condition']).logical()==walk['state']
    live=read(ART/'live/events.json');assert replay(live,'sessions').logical()=={k:v for k,v in read(ART/'live/final.json').items() if k not in ['sequence','elapsed','counts','state_sha256']}
    latencies=dict(protocol_handler_ms=quantiles([v for s in runs for v in s['handler_ms']]),
        replay_delivery_lateness_ms=quantiles([v for s in runs for v in s['delivery_lateness_ms']]),
        browser_http_roundtrip_ms=quantiles(browser['http_roundtrip_ms']))
    browser_events=[e for p in (ART/'browser_final_verified').glob('*_events.json') for e in read(p)['events']]
    latencies['browser_received_to_render_ms']=quantiles([e['payload']['received_to_render_ms'] for e in browser_events if e['action']=='display' and 'received_to_render_ms' in e['payload']])
    write(ART/'tables/latency.json',latencies)
    audit=dict(completed_scenarios=verified,cutoffs_verified=cutoff_verified,scenario_events=events,live_replayed=True,walkthrough_replayed=True,browser_runs_replayed=browser_release,
        browser_checks=len(browser['checks']),initial_requests_verified=len(quality),generation_replica_note='Two replicas paired within each source; 145 unique question IDs.',stable_checks=sum(s['active_stability_checks'] for s in runs),stability_failures=sum(s['active_stability_checks']-s['active_stability_passed'] for s in runs),
        command_errors=sum(len(s['command_errors'])+len(s['driver_errors']) for s in runs),all_planned_sources_retained=True,
        declared_matrix='12 two-context bundles x 2 answer replicas x 3 interfaces x 2 constructed loads',
        conclusion='Software validation only. Source contexts=24; constructed matched bundles=12. No participant observations.')
    write(ART/'verification.json',audit)
    print(json.dumps(dict(answers=answers,conditions=grouped,contrasts=contrasts,verification=audit,latency=latencies),indent=2))

if __name__=='__main__':main()
