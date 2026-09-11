"""Commit-gated final declaration, source snapshots and hash verification."""
import hashlib
import json
import shutil
import subprocess
from datetime import datetime,timezone
from .common import ART,ROOT,read,write_json
from .evaluate import EMPIRICAL_METHODS,SYNTHETIC_METHODS,BUDGETS
from .synthetic import FAMILIES

CORE=['common.py','client.py','data.py','collect.py','planner.py','exact.py','empirical.py','synthetic.py','evaluate.py','analyze.py','freeze.py','METHOD.md','test_planner.py']

def verify(require_commit=False):
    d=read(ART/'frozen/declaration.json')
    for path,sha in d['hashes'].items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=sha:raise ValueError('Frozen source changed: '+path)
    if require_commit:
        # A declaration in HEAD is required, not merely an uncommitted timestamp.
        rel=str((ART/'frozen/declaration.json').relative_to(ROOT))
        committed=subprocess.check_output(['git','show','HEAD:'+rel])
        if committed!=(ART/'frozen/declaration.json').read_bytes():raise ValueError('Declaration not committed')
    return d

def freeze():
    dest=ART/'frozen'
    if (dest/'declaration.json').exists():raise ValueError('Already frozen')
    dest.mkdir(exist_ok=True);public=read(ART/'data/public.json')
    paths=[ROOT/'research/clarification_planning'/n for n in CORE]+[ART/'estimator.json',ART/'authorization.json']+list((ART/'data').iterdir())
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    for name in CORE:
        p=dest/'source'/name;p.parent.mkdir(exist_ok=True);shutil.copyfile(ROOT/'research/clarification_planning'/name,p)
    raw=[read(p) for p in (ART/'raw').glob('*.json')];attempts=[a for r in raw for a in r['attempts']]
    mean=sum(a['elapsed_seconds'] for a in attempts)/len(attempts)
    d=dict(frozen_utc=datetime.now(timezone.utc).isoformat(),baseline=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        evaluation_ids=[c['id'] for c in public if c['split']=='evaluation'],development_ids=[c['id'] for c in public if c['split']=='development'],
        all_development_ids=read(ART/'data/development_exposure_audit.json')['all_new_development_ids'],generation_replicates=2,
        task_rule='At least two supported requested domains. One distinct executable shortlist per domain, no masked evidence, no selection on generated errors or complementary gains.',
        empirical_methods=EMPIRICAL_METHODS,response_budgets=BUDGETS,error_weights=[2,4,8],defer_weight=1,question_cost=1,question_penalty=.05,
        primary=dict(budget=2,error_weight=4,contrasts=['depth2 minus one_step','depth2 minus semantic_memory'],outcome='terminal loss; report correct/incorrect/unfinished tasks, project correctness and additional responses separately',independent_unit='source dialogue'),
        analysis=dict(seed=82164,bootstrap_resamples=2000,replicates_averaged_before_resampling=True,all_matched_conditions_resampled_together=True,
                      intervals='paired percentile 95%, two prespecified descriptive primary comparisons, no significance-based selection or multiplicity claim',
                      examples='First lexicographic qualifying dialogue for favorable, tied, unfavorable primary loss contrasts; replicate zero display'),
        synthetic=dict(families=FAMILIES,development_seeds=list(range(2000,2004)),evaluation_seeds=list(range(5000,5020)),
                       grid=dict(overlap=['none','one','full'],arity=[1,2,3],development_seeds=[2100,2101],evaluation_seeds=list(range(6000,6012))),
                       methods=SYNTHETIC_METHODS,instances=388,expected_rows=23280,response_conditions='accurate; separate 0.2 symmetric errors and 0.3 unresolved; misspecified value/scope priors are separate families'),
        expected_empirical_rows=48*2*3*10*6,additional_generation_calls=288,prior_development_calls=len(raw),
        total_forecast_calls=len(raw)+288,attempt_ceiling=1200,scheduled_call_ceiling=600,
        forecast=dict(measured_development_mean_attempt_seconds=mean,remaining_generation_seconds=288*mean,conservative_seconds=288*mean*2,
                      analysis_reserve_minutes=45,inference_cutoff_utc=read(ART/'authorization.json')['inference_cutoff_utc']),
        model=dict(name='Qwen/Qwen2.5-7B-Instruct',revision='a09a35458c702b33eeacc393d103063234e8bc28',dtype='bfloat16',gpu='RTX 6000 Ada',cpu_offload_gb=0,
                   temperature=.3,top_p=1,max_model_len=2048,output_tokens_extract=640,output_tokens_other=256,serial=True),
        search=dict(depths=[1,2,3],candidate_width=8,completion_block_size=3,node_limit=25000,exact_factor_limit=6,exact_budget_limit=6,small_pruning_sensitivity_width=2),
        failure_handling='At most one transport retry; no reruns for poor answers. Preserve parse/context/transport failures, unresolved responses, incorrect releases and unfinished tasks. No replacement source IDs.',
        estimator_hash=read(ART/'estimator.json')['sha256'],hashes=hashes)
    write_json(dest/'declaration.json',d);print(json.dumps({k:v for k,v in d.items() if k not in ['hashes','evaluation_ids','all_development_ids','development_ids']},indent=2))
if __name__=='__main__':freeze()
