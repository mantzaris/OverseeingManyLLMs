"""Replay every simulation command stream and retain ordinary-engine spot checks."""
import gzip,json,hashlib,time
from research.oversight_workflow.common import ROOT,read,write,digest
from research.adaptive_correction_transfer.scoring import score
from .inputs import OUT,workload
from .run import verify_freeze,environment
from .simulation import replay_trace


def main():
    started=time.perf_counter();verify_freeze();inputs=read(OUT/'inputs.json');design=read(OUT/'design.json');configs={c['id']:c for c in design['configs']};env=environment(inputs)
    expected={(c['id'],r,s,p) for c in design['configs'] for r in design['rotations'] for s in design['seeds'] for p in design['policies']};seen=set();full=0;scored=0
    results={}
    with gzip.open(OUT/'results.jsonl.gz','rt') as f:
        for line in f:
            r=json.loads(line);results[r['simulation_run_id']]=r
    with gzip.open(OUT/'traces.jsonl.gz','rt') as f:
        for n,line in enumerate(f):
            t=json.loads(line);key=(t['config'],t['rotation'],t['seed'],t['policy']);assert key not in seen;seen.add(key)
            assert t['record_kind']=='computational_simulation' and 'participant_code' not in t
            items=workload(inputs,configs[t['config']],t['rotation']);actual=replay_trace(t,items,inputs['sources'],t['policy'])
            assert actual==t['final_state_sha256'],t['simulation_run_id']
            # One common seed/rotation for every original setting and policy,
            # replayed through ordinary atomic command/deep-copy/hash machinery.
            if t['rotation']==0 and t['seed']==design['seeds'][0] and configs[t['config']]['family']=='original':
                assert replay_trace(t,items,inputs['sources'],t['policy'],True)==actual;full+=1
            states={i['id']:i['output'] if t['policy']!='M' else dict(answer=[],scale='') for i in items}
            correct=wrong=0
            for at,action,p in t['commands']:
                if action=='decide' and p['decision']=='correct':states[p['id']]=p['output']
                if action=='release':
                    joint=score(states[p['id']],env.annotations[p['id']])['joint'];correct+=joint;wrong+=1-joint;scored+=1
            r=results[t['simulation_run_id']];assert (correct,wrong)==(r['correct'],r['incorrect'])
            if (n+1)%3000==0:print('Replayed',n+1,flush=True)
    assert seen==expected and len(results)==len(seen)
    preservation=read(OUT/'preservation.json')
    for name,sha in preservation['files'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
    out=dict(record_kind='computational_simulation',status='verified',simulation_traces=len(seen),ordinary_engine_replays=full,official_release_scores_checked=scored,preserved_files=len(preservation['files']),elapsed_seconds=time.perf_counter()-started,human_records_read=0,inference_calls=0)
    write(OUT/'verification.json',out);print(json.dumps(out,indent=2))


if __name__=='__main__':main()
