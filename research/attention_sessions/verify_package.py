"""Verify saved-output reproduction and preservation, without inference or writes to historical results."""
import contextlib,io,json,subprocess,tempfile,hashlib
from pathlib import Path
from . import analyze
from .data import ROOT,save_json
from .evaluate import run
from .verify_ui_log import verify as verify_ui

BASELINE='8ee1a973a1ad3d5debca4442c6a37ce53d9c6416'

def main():
    run('evaluation',verify=True)
    root=ROOT.resolve();names=['policy_summary.csv','paired.csv','bundle_differences.csv','dominance.csv','summary.json','example_selection.json']
    original=analyze.ROOT
    with tempfile.TemporaryDirectory(prefix='attention_reproduction_') as directory:
        temp=Path(directory)
        for name in ('declaration.json','evaluation'):(temp/name).symlink_to(root/name)
        try:
            analyze.ROOT=temp
            with contextlib.redirect_stdout(io.StringIO()):analyze.analyze()
        finally:analyze.ROOT=original
        for name in names:
            assert (temp/'analysis'/name).read_text()==(root/'analysis'/name).read_text(),name
    changed=subprocess.check_output(['git','diff','--name-only',BASELINE],text=True).splitlines()
    allowed=('research/','artifacts/attention_sessions/')
    assert all(p.startswith(allowed) for p in changed),changed
    # No baseline file is permitted to change, including the submission PDF.
    tracked=set(subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE],text=True).splitlines())
    assert not set(changed)&tracked,'Historical tracked file changed'
    pdfs={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('paper').glob('*.pdf')}
    result=dict(status='verified',baseline=BASELINE,main_replays=4500,exact_analysis_files=names,
                historical_tracked_files_unchanged=True,manuscript_pdf_hashes=pdfs,
                ui=verify_ui(ROOT/'ui_verified_demonstration.jsonl'),new_inference=0)
    save_json(ROOT/'package_verification.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':main()
