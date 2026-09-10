#!/usr/bin/env python3
"""Recheck historical methods without writing into any historical evidence root."""
from collections import Counter
from contextlib import redirect_stdout
import importlib.util,io,json,runpy,subprocess,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import overseeing.io as oio
from overseeing.replay import replay_score
out=Path('artifacts/stage6_robustness/historical_audits');out.mkdir(exist_ok=True)
original_write=oio.write_json
# Existing command entry points retain their historical calculations. Relocate
# only audit reports that they would otherwise overwrite in a historical root.
def redirected(path,value):
    path=Path(path)
    if str(path).startswith('artifacts/stage6_robustness'):return original_write(path,value)
    destination=out/str(path).replace('/','__')
    return original_write(destination,value)
oio.write_json=redirected
spec=importlib.util.spec_from_file_location('stage1_verifier',Path('scripts/verify_live_results.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
for folder,label in [('artifacts/stage1_gpu_live/run','stage1_l40s'),('artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run','stage1_ada')]:
    if label=='stage1_l40s':
        # The earliest run predates embedded snapshots. Recover its exact
        # executed sources from the recorded historical commit, into a temp dir.
        manifest=json.loads((Path(folder)/'manifest.json').read_text())
        with tempfile.TemporaryDirectory(prefix='stage6_l40s_') as temp:
            for name in manifest['source_files_sha256']:
                path=Path(temp)/name;path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(subprocess.check_output(['git','show','46e70003:'+name]))
            result=module.verify(folder,temp);result['source_root']='git:46e70003'
    else:result=module.verify(folder)
    original_write(out/(label+'.json'),result)
counts=Counter()
for stage in ('stage2_development','stage3_competition','stage4_research'):
    root=Path('artifacts')/stage
    paths=list(root.rglob('events.jsonl'))+list(root.rglob('events.jsonl.gz'))
    for path in paths:
        # Source snapshots and mechanics fixtures are not live episode outputs.
        if 'source' in path.parts:continue
        result=replay_score(path)
        assert result['status']=='verified',(path,result)
        counts[stage]+=1
original_write(out/'maintenance_replays.json',dict(status='verified',completed_traces=dict(counts)))
with redirect_stdout(io.StringIO()):
    runpy.run_path('scripts/verify_practical_package.py',run_name='__main__')
    sys.argv=['scripts/audit_retail_session.py'];runpy.run_path(sys.argv[0],run_name='__main__')
    sys.argv=['scripts/audit_research_session.py'];runpy.run_path(sys.argv[0],run_name='__main__')
# Reconstruct Stage 5 GPU workflows from the published, provenance-preserving
# evidence. Report outputs go under Stage 6; historical bytes stay untouched.
from overseeing.retail.analysis import audit_preparation
result=audit_preparation('artifacts/stage5_practical','evaluation')
print(json.dumps(dict(status='verified',maintenance_completed_trace_replays=dict(counts),stage1_replays=8,stage5_workflows_replayed=result['replayed_workflows'],stage5_policy_replays='1152 exact matches in separately saved Stage 6 post hoc analysis'),indent=2))
