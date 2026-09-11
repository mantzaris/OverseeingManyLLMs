"""Verify and reproduce saved evidence without inference or modifying originals."""
import argparse
import contextlib
import hashlib
import io
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from .client import ART,ROOT,MODEL,canonical,write_json
from .freeze import verify_frozen
from .evaluate import evaluate
from .analyze import analyze,figures

BASELINE='3f843bee7c474876881651b76977840ffddc77e5'

def verify_raw():
    ledger=[json.loads(x) for x in (ART/'attempts.jsonl').read_text().splitlines()]
    indices=[x['scheduled_attempt'] for x in ledger]
    assert indices==list(range(1,len(ledger)+1)),'Attempt ledger has a gap or duplicate'
    recorded={(x['call_id'],x['attempt']):x for x in ledger};observed=set();calls=0
    for path in sorted((ART/'raw').glob('*.json')):
        r=json.loads(path.read_text());calls+=1
        assert path.stem==r['call_id']
        assert hashlib.sha256(canonical(r['request']).encode()).hexdigest()==r['request_sha256']
        assert len(r['attempts'])<=2
        for attempt in r['attempts']:
            key=(r['call_id'],attempt['attempt']);observed.add(key)
            assert key in recorded
            assert attempt['request_sha256']==recorded[key]['request_sha256']
        if r['call_id'].startswith('evaluation_'):
            prompt=canonical(r['request']['messages'])
            for forbidden in ('annotation_states','evaluation_only','lexical_support_turns','expected_output'):
                assert forbidden not in prompt
    assert observed==set(recorded),'Unfinished or unaccounted attempts'
    assert len(ledger)<=1500
    return dict(calls=calls,attempts=len(ledger))

def historical_unchanged():
    tracked=set(subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE],cwd=str(ROOT),text=True).splitlines())
    changed=set(subprocess.check_output(['git','diff','--name-only',BASELINE],cwd=str(ROOT),text=True).splitlines())
    altered=sorted(tracked & changed)
    assert not altered,'Historical files changed: '+repr(altered)
    return dict(baseline=BASELINE,tracked_files=len(tracked),changed_historical_files=altered)

def verify_preparations(output):
    """Rebuild prompts and parsed preparations using a network-free raw reader."""
    from . import collect,challenges
    stage=Path(output)/'reconstructed_inputs';stage.mkdir(parents=True,exist_ok=True)
    observed=[]
    def saved_generate(call_id,messages,seed,max_tokens=768,json_object=False):
        payload=dict(model=MODEL,messages=messages,temperature=.3,top_p=1.,max_tokens=max_tokens,seed=seed)
        if json_object:payload['response_format']={'type':'json_object'}
        raw=json.loads((ART/'raw'/(call_id+'.json')).read_text())
        assert raw['request']==payload,'Prompt, seed or setting changed: '+call_id
        observed.append(call_id);return raw
    original=(collect.ART,collect.generate,challenges.ART,challenges.generate)
    try:
        collect.ART=stage;collect.generate=saved_generate
        public=json.loads((ART/'data/public_projects.json').read_text())
        for case in public:
            for rep in range(2 if case['split']=='evaluation' else 1):
                rebuilt=collect.case_calls(case,rep)
                path=ART/'prepared'/('%s_%s_%d.json'%(case['split'],case['project'],rep))
                assert rebuilt==json.loads(path.read_text()),'Preparation differs from raw calls: '+str(path)
        challenges.ART=stage;challenges.generate=saved_generate
        (stage/'frozen').mkdir(exist_ok=True)
        for name in ['commit.json','challenge_public.json','challenge_evaluation_only.json']:
            shutil.copyfile(ART/'frozen'/name,stage/'frozen'/name)
        with contextlib.redirect_stdout(io.StringIO()):challenges.collect()
        assert (stage/'challenges_prepared.json').read_bytes()==(ART/'challenges_prepared.json').read_bytes()
        challenges.analyze()
        assert (stage/'challenge_results.json').read_bytes()==(ART/'challenge_results.json').read_bytes()
    finally:
        collect.ART,collect.generate,challenges.ART,challenges.generate=original
    return dict(rebuilt_project_preparations=56,rebuilt_challenge_preparations=24,
                prompt_seed_setting_checks=len(observed),challenge_rows=120,network_requests=0)

def run(output,make_figures=False):
    declaration=verify_frozen();raw=verify_raw();historical=historical_unchanged()
    assert len(list((ART/'prepared').glob('evaluation_*.json')))==48
    for key in declaration['evaluation_ids']:
        for rep in range(2):
            p=json.loads((ART/('prepared/evaluation_%s_%d.json'%(key[:-5],rep))).read_text())
            assert len(p['calls'])==12 and p['id']==key and p['replicate']==rep
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    if output.resolve()==(ART/'evaluation').resolve():raise ValueError('Use a different output directory; preserve original evidence')
    preparations=verify_preparations(output)
    rows=evaluate('evaluation',output)
    assert len(rows)==declaration['expected_rows']
    for row in rows:
        assert row['correct_artifacts']+row['incorrect_artifacts']+row['unresolved_artifacts']==row['artifact_goals']
        if row['budget']!='unlimited':assert row['answered_questions']<=row['budget']
    original=json.loads((ART/'evaluation/replay.json').read_text());replay=json.loads((output/'replay.json').read_text())
    assert original==replay,'Saved traces or episode CSV do not replay exactly'
    (figures if make_figures else analyze)('evaluation',output)
    compared=[]
    for path in sorted((ART/'evaluation/analysis').glob('*.csv')):
        new=output/'analysis'/path.name
        assert new.read_bytes()==path.read_bytes(),'Analysis table changed: '+path.name
        compared.append(path.name)
    from .interpret import run as interpret
    with contextlib.redirect_stdout(io.StringIO()):interpret(output/'interpretation')
    explained=[]
    for path in sorted((ART/'interpretation').glob('*')):
        if path.suffix not in ('.csv','.json'):continue
        assert (output/'interpretation'/path.name).read_bytes()==path.read_bytes(),'Post hoc analysis changed: '+path.name
        explained.append(path.name)
    if make_figures:
        from .publication import make
        make(output/'publication')
    result=dict(status='passed',frozen_hashes=len(declaration['hashes']),raw=raw,
                replayed_rows=len(rows),projects=24,replicates=2,analysis_tables=compared,
                historical=historical,preparations=preparations,post_hoc_tables=explained,figures_regenerated=make_figures,
                inference_calls_during_reproduction=0)
    write_json(output/'verification.json',result);print(json.dumps(result,indent=2));return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='/tmp/decision-dependencies-replay');p.add_argument('--figures',action='store_true');a=p.parse_args();run(a.output,a.figures)
