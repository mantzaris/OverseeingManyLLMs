"""Freeze the new comparison without altering historical declarations."""
import hashlib
from pathlib import Path
from research.oversight_workflow.common import ROOT, ART, read, write, digest
from .materials import HERE, OUT, VERSION


def runtime_files():
    files=list(HERE.glob('*.py'))
    files += [ROOT/'research/oversight_workflow'/p for p in (
        'protocol.py','driver.py','data.py','common.py','prototype/server.py','prototype/index.html',
        'pilot/server.py','pilot/setup.html','pilot/desk.js','pilot/adapter.py','pilot/materials.py',
        'pilot/analysis.py','study/training.json')]
    files += [ART/'frozen/manifest.json',HERE/'manifest.json']
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))}


def runtime_fingerprint():return digest(runtime_files())


def verify():
    if not (OUT/'freeze.json').exists():
        raise ValueError('Matched comparison has not been frozen for participant use')
    f=read(OUT/'freeze.json')
    for rel,expected in f['files'].items():
        if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=expected:
            raise ValueError('Frozen comparison changed: '+rel)
    if runtime_fingerprint()!=f['runtime_sha256']:raise ValueError('Runtime fingerprint changed')
    old=read(OUT/'historical_preservation.json')
    for rel,expected in old['files'].items():
        if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=expected:
            raise ValueError('Historical pilot or manuscript changed: '+rel)
    m=read(HERE/'manifest.json');given=m.pop('manifest_sha256')
    if digest(m)!=given or given!=f['manifest_sha256']:raise ValueError('Manifest digest mismatch')
    return dict(status='verified',version=VERSION,runtime_sha256=f['runtime_sha256'],manifest_sha256=given,
                historical_files_unchanged=len(old['files']),frozen_files=len(f['files']),new_inference=0)


def main():
    import argparse,datetime,json,subprocess
    p=argparse.ArgumentParser();p.add_argument('--create',action='store_true');args=p.parse_args()
    if args.create:
        if (OUT/'freeze.json').exists():raise ValueError('Refusing to overwrite an existing freeze')
        files=runtime_files()
        for path in [p for p in HERE.glob('*.md') if p.name != 'REPORT.md']+list(HERE.glob('*.json'))+list(HERE.glob('*.mjs'))+list((HERE/'tests').glob('*.py')):
            files[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
        manifest=read(HERE/'manifest.json')
        f=dict(version=VERSION,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               baseline_commit=read(OUT/'ledger.json')['baseline_commit'],manifest_sha256=manifest['manifest_sha256'],runtime_sha256=runtime_fingerprint(),files=files,
               boundary='Frozen before any matched participant outcomes. Software fixtures are not observations.',
               participant_results='Unpopulated',collection_registration='Responsible investigator must register authorized tranche and schedule separately; no powered sample size claimed')
        write(OUT/'freeze.json',f)
    print(json.dumps(verify(),indent=2))


if __name__=='__main__':main()
