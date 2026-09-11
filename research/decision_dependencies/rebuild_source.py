"""Reconstruct the pinned source selection outside the preserved artifact tree."""
import argparse
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path
from .client import ART,ROOT,write_json
from . import data

def rebuild(output):
    target=Path(output).resolve()
    if target==ART.resolve() or ART.resolve() in target.parents:
        raise ValueError('Choose an external output directory to preserve the original source snapshot')
    target.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((ROOT/'research/decision_dependencies/data_provenance.json').read_text())
    for entry in manifest['downloads']:
        if entry['path'] not in ['LICENSE','data/MULTIWOZ2.4.zip']:continue
        path=target/Path(entry['path']).name
        if not path.exists():
            with urllib.request.urlopen(entry['url'],timeout=60) as response:path.write_bytes(response.read())
        assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
    with zipfile.ZipFile(target/'MULTIWOZ2.4.zip') as z:
        for name in z.namelist():
            dest=(target/'upstream'/name).resolve()
            if target not in dest.parents:raise ValueError('Unsafe archive member')
        z.extractall(target/'upstream')
    sources=list((target/'upstream').rglob('data.json'))
    if len(sources)!=1:raise ValueError('Unexpected archive layout')
    old=data.ART
    try:data.ART=target;data.build(sources[0].parent)
    finally:data.ART=old
    # Frozen builder's optional legacy license path is not a reproduction dependency.
    (target/'data/UPSTREAM_LICENSE.txt').write_bytes((target/'LICENSE').read_bytes())
    original=json.loads((ART/'data/manifest.json').read_text())
    actual={name:hashlib.sha256((target/'data'/name).read_bytes()).hexdigest() for name in original['files']}
    assert actual==original['files'],'Selected source bytes changed'
    regenerated=json.loads((target/'data/manifest.json').read_text());regenerated['files']=actual
    assert regenerated==original
    write_json(target/'data/manifest.json',regenerated)
    source_data=json.loads(sources[0].read_text())
    probe=json.loads((ART/'development/probe_declaration.json').read_text())
    ids=original['selected']['val']+original['selected']['test']
    ids+=sorted({x[0] for x in probe['cases']}-set(ids))
    goal_rows=[];by_hash={}
    for key in ids:
        goal={d:{f:source_data[key]['goal'].get(d,{}).get(f,{})
                 for f in ['info','book','fail_info','fail_book']} for d in ['hotel','restaurant']}
        digest=hashlib.sha256(json.dumps(goal,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        goal_rows.append(dict(id=key,goal_sha256=digest));by_hash.setdefault(digest,[]).append(key)
    expected=json.loads((ART/'expanded_source_audit.json').read_text())
    assert goal_rows==expected['rows']
    assert [v for v in by_hash.values() if len(v)>1]==expected['exact_goal_duplicates']==[]
    write_json(target/'source_verification.json',dict(status='passed',files=len(actual),
                  exact_selection=True,all_development_and_evaluation_goal_signatures=len(goal_rows),
                  exact_goal_duplicates=0,source_revision=manifest['revision'],new_inference_calls=0))
    print('Pinned source selection matches:',target)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='/tmp/decision-source-rebuild');a=p.parse_args();rebuild(a.output)
