"""Declare and verify the final exploratory comparison before new generations."""
import hashlib
import json
import shutil
from datetime import datetime,timezone
from .client import ART,ROOT,write_json
from .challenges import declaration as challenge_declaration
from .evaluate import METHODS,DEMANDS,BUDGETS

CORE=['client.py','prompts.py','records.py','application.py','data.py','collect.py',
      'evaluate.py','analyze.py','challenges.py','test_decisions.py','freeze.py','METHOD.md']

def verify_frozen():
    declaration=json.loads((ART/'frozen/declaration.json').read_text())
    for path,digest in declaration['hashes'].items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Frozen input changed: '+path)
    return declaration

def freeze():
    out=ART/'frozen'
    if (out/'declaration.json').exists():raise RuntimeError('Do not overwrite a frozen declaration')
    challenge_declaration()
    public=json.loads((ART/'data/public_projects.json').read_text());hashes={}
    paths=[ROOT/'research/decision_dependencies'/p for p in CORE]+sorted((ART/'data').iterdir())
    paths+=[out/'challenge_public.json',out/'challenge_evaluation_only.json']
    for path in paths:hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    snapshot=out/'source_snapshot';snapshot.mkdir(parents=True,exist_ok=True)
    for name in CORE:shutil.copyfile(ROOT/'research/decision_dependencies'/name,snapshot/name)
    write_json(out/'declaration.json',dict(
        frozen_utc=datetime.now(timezone.utc).isoformat(),
        evaluation_ids=[x['id'] for x in public if x['split']=='evaluation'],
        development_ids=[x['id'] for x in public if x['split']=='development'],replicates=2,
        source_selection='First 12 sorted eligible test IDs per retained-change stratum; no generated outcome selection',
        methods=METHODS,role_caps=DEMANDS,response_budgets=BUDGETS,
        primary='Selective dependencies minus semantic memory, up to six nonempty roles, unlimited responses: project correctness and additional clarification requests reported separately',
        secondary='Full history; global barrier equivalence; lower demand; finite response budgets; scope and source/release ablations; authored scope challenges',
        expected_rows=24*2*len(METHODS)*len(DEMANDS)*len(BUDGETS),
        dialogue_generation_calls=576,challenge_generation_calls=96,additional_scheduled_calls=672,
        prior_actual_attempts=112,session_attempt_ceiling=1500,
        final_generation_seeds='collect.case_calls and challenges.collect are hashed; independent of replay policy and demand',
        model=dict(name='Qwen/Qwen2.5-7B-Instruct',revision='a09a35458c702b33eeacc393d103063234e8bc28',
                   dtype='bfloat16',gpu='RTX 6000 Ada',cpu_offload_gb=0,temperature=.3,top_p=1,
                   max_model_len=2048,max_tokens_extraction=768,max_tokens_other=384,response_format='json_object'),
        analysis=dict(bootstrap_resamples=2000,seed=91831,unit='source dialogue',stratified=True,
                      average_generation_replicates_first=True,shared_resample_indices=True),
        failure_handling='At most one retry for a transport attempt. No retry for parse, scope, source or context failures; retain them and request clarification or leave dependent work unresolved.',
        forecast='112 attempts averaged 2.733 seconds; 672 additional calls forecast 30.6 minutes, 45.9 minutes with 50% margin; hard inference cutoff 09:46:21 UTC.',
        human_data='None. Accurate extra responses and finite response budgets are simulation assumptions.',
        nonempty_artifacts='Do not count roles with no supported final input fields; two test dialogues omit location brief and one omits stay specification.',
        hashes=hashes))
    print('Frozen 24 dialogues x 2 replicates; 672 additional calls; 5184 controller rows')

if __name__=='__main__':freeze()
