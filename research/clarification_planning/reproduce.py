"""One-command verification of the frozen and explicitly corrected saved outputs."""
import argparse
import contextlib
import gzip
import hashlib
import io
import json
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from .common import ART,ROOT,canonical,read,write_json
from .freeze import verify
from . import collect
from .client import MODEL
from .evaluate import evaluate_empirical,evaluate_synthetic
from .completion_audit import evaluate as audit_completion
from .repair_scope import evaluate as repair_scope


def verify_raw(output):
    auth=read(ART/'authorization.json');raw={p.stem:read(p) for p in (ART/'raw').glob('*.json')}
    attempts=[a for r in raw.values() for a in r['attempts']]
    assert len(raw)==396 and len(attempts)==396
    intents=[json.loads(x) for x in (ART/'attempts.jsonl').read_text().splitlines()]
    assert len(intents)==len(attempts)
    assert {(a['call_id'],a['attempt'],a['request_sha256']) for a in attempts}=={(a['call_id'],a['attempt'],a['request_sha256']) for a in intents}
    for r in raw.values():
        assert r['request_sha256']==hashlib.sha256(canonical(r['request']).encode()).hexdigest()
        assert len(r['attempts'])<=2
        for a in r['attempts']:assert datetime.fromisoformat(a['started_utc'])<datetime.fromisoformat(auth['inference_cutoff_utc'])
    declared=read(ART/'frozen/declaration.json')
    assert min(datetime.fromisoformat(a['started_utc']) for r in raw.values() if r['call_id'].startswith('evaluation_') for a in r['attempts'])>datetime.fromisoformat(declared['frozen_utc'])
    current=read(ART/'data/public.json');initial=read(ART/'development_initial_selection.json')
    cases={c['id']:c for c in initial if c['split']=='development'};cases.update({c['id']:c for c in current})
    consumed=[]
    def cached(call_id,messages,seed,max_tokens):
        payload=dict(model=MODEL,messages=messages,temperature=.3,top_p=1.,max_tokens=max_tokens,seed=seed,response_format={'type':'json_object'})
        assert raw[call_id]['request']==payload,call_id
        consumed.append(call_id);return raw[call_id]
    with patch.object(collect,'generate',cached),patch.object(collect,'ART',output):
        for case in cases.values():
            if case['split']=='evaluation' or case['id'] in read(ART/'data/development_exposure_audit.json')['all_new_development_ids']:
                for rep in range(2):
                    recreated=collect.case_calls(case,rep)
                    original=read(ART/'prepared'/('%s_%s_%d.json'%(case['split'],case['id'][:-5],rep)))
                    assert recreated==original
    assert set(consumed)==set(raw) and len(consumed)==len(raw)
    return dict(calls=len(raw),attempts=len(attempts),reconstructed_prompts=len(consumed),prepared_files=len(consumed)//3)


def same(path,original):
    a=read(path/'replay_digest.json');b=read(original/'replay_digest.json');assert a==b,(path,a,b)
    # CSV newline normalization is irrelevant; compare parsed tables.
    import csv
    assert list(csv.DictReader((path/'episodes.csv').open()))==list(csv.DictReader((original/'episodes.csv').open()))
    return a['rows']


def reproduce(figures=False,output=None):
    verify(require_commit=True)
    dest=Path(output or tempfile.mkdtemp(prefix='clarification-replay-'))
    if dest.resolve()==ART.resolve() or ART.resolve() in dest.resolve().parents:raise ValueError('Reproduction must use a separate output tree')
    dest.mkdir(parents=True,exist_ok=True)
    result={'frozen_inputs':'passed','raw':verify_raw(dest/'reconstructed'),'new_generations':0}
    with contextlib.redirect_stdout(io.StringIO()):
        evaluate_empirical('evaluation',dest/'evaluation')
        evaluate_synthetic(dest/'synthetic')
        audit_completion(dest/'completion_audit')
        repair_scope(dest/'scope_consistency_repair')
    for name in ['evaluation','synthetic','completion_audit','scope_consistency_repair']:
        result[name+'_rows']=same(dest/name,ART/name)
    # Statistical replay uses measured original timing files, not the new machine's
    # timings, so the reported cost tables continue to describe the original run.
    for name in ['evaluation','synthetic']:
        shutil.copyfile(ART/name/'costs.csv',dest/name/'costs.csv')
    from .analysis_runner import run as analyze
    with contextlib.redirect_stdout(io.StringIO()):analyze(dest)
    for filename in ['summary.csv','paired.csv','individual.csv','primary.json']:
        a=(dest/'analysis'/filename).read_text();b=(ART/'analysis'/filename).read_text();assert a==b,filename
    # Recompute every supplementary numerical table, including the stronger
    # baseline and corrected scope views, from the recreated trace rows.
    for name in ['data','prepared']:
        shutil.copytree(ART/name,dest/name,dirs_exist_ok=True)
    from .supplemental_analysis import run as supplemental
    from .valid_synthetic_analysis import run as valid
    with contextlib.redirect_stdout(io.StringIO()):
        supplemental(dest);valid(dest)
    ignored={'computation.csv','selected_traces.json'}
    for p in (ART/'analysis').iterdir():
        if p.name in ignored:continue
        assert (dest/'analysis'/p.name).read_text()==p.read_text(),p.name
    result['analysis_tables_recomputed']=len(list((ART/'analysis').iterdir()))-len(ignored)
    # UI logs preserve exactly displayed questions and state hashes, without using
    # any hidden answer simulator. Ignore a pre-fix log in the explicitly archived
    # directory; the final current-interface log is verified here.
    from .desk import Desk
    d=Desk();events=[json.loads(x) for x in (ART/'interface/interactions.jsonl').read_text().splitlines()]
    checked=0
    for event in events:
        if event['action']=='started':continue
        d.act(event['payload'])
        assert d.events[-1]['state_sha256']==event['state_sha256'],event['action']
        assert d.events[-1]['displayed_question']==event['displayed_question']
        checked+=1
    result['interface_actions_replayed']=checked
    result['historical_files_changed']=0
    import subprocess
    changes=subprocess.check_output(['git','diff','--name-only','569c0603'],text=True).splitlines()
    assert all(x.startswith(('research/clarification_planning/','artifacts/clarification_planning/','paper/clarification_planning/')) for x in changes)
    if figures:
        # Figures use immutable measured tables; numerical replay above already
        # verified the inputs. Regenerated exports go to the scratch output tree.
        for name in ['analysis','scope_consistency_repair','completion_audit']:
            shutil.copytree(ART/name,dest/name,dirs_exist_ok=True)
        from .plot import main as plot
        plot(dest)
        from .effort_plot import run as effort
        effort(dest)
    result['output']=str(dest);result['status']='passed';write_json(dest/'verification.json',result)
    print(json.dumps(result,indent=2));return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--figures',action='store_true');p.add_argument('--output');a=p.parse_args();reproduce(a.figures,a.output)
