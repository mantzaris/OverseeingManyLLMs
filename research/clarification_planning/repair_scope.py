"""Explicit post-freeze oracle consistency repair for two synthetic families.

The original source, rows and traces remain intact. A question about an exception
must return that task's effective preference, even when a shared instruction
applies. No planner beliefs, seeds, weights, selection or GPU outputs are changed.
"""
import argparse
from pathlib import Path
from .common import ART,write_json
from .synthetic import generate,decode
from .planner import Planner
from .evaluate import run,finish,unshare,SYNTHETIC_METHODS,BUDGETS

def repaired_case(family,seed):
    case,gold=generate(family,seed)
    if family in ['scope_exception','wrong_sharing']:
        gold['truth']['exception.preference']=gold['targets']['exception_implementation']['value']
    return case,gold

def evaluate(out=None):
    out=Path(out or ART/'scope_consistency_repair');out.mkdir(parents=True,exist_ok=True)
    rows=[];traces=[];costs=[];changed=[]
    for family in ['scope_exception','wrong_sharing']:
        for seed in range(5000,5020):
            _,old=generate(family,seed);case,gold=repaired_case(family,seed)
            if old!=gold:changed.append(dict(family=family,seed=seed,old_local_answer=old['truth']['exception.preference'],corrected_local_answer=gold['truth']['exception.preference']))
            f,t=decode(case)
            for method in SYNTHETIC_METHODS:
                for budget in BUDGETS:
                    p=Planner(f,t,case['response_error'],case['unresolved_probability'])
                    if method=='request_specific':p=unshare(p)
                    row,trace,stats=run(p,gold['targets'],gold['truth'],'depth2' if method=='request_specific' else method,budget,seed)
                    meta=dict(id=case['id'],family=family,seed=seed,method=method,budget=budget)
                    row=dict(meta,**row);rows.append(row);traces.append(dict(meta,row=row,**trace));costs.append(dict(meta,**stats))
    finish(out,rows,traces,costs)
    write_json(out/'repair_manifest.json',dict(reason='Perfect local value responder could contradict effective task target when scope applied.',
        original_affected_source='synthetic/episodes.csv and synthetic/traces.jsonl.gz, scope_exception and wrong_sharing families',
        source_instances=40,instances_with_inconsistent_potential_answer=len(changed),changed=changed,
        new_rows=len(rows),new_inference=0,planner_changed=False,priors_changed=False,
        interpretation='Post-freeze semantic consistency repair; original scope-family results are not valid outcome evidence. Corrected local truth is correlated with shared preference and applicability. Planner factor independence is an approximation in these two families, even when marginal parameters are specified.',
        untouched_frozen_empirical=True,remaining_original_synthetic_instances=348))
    print('Repaired',len(changed),'of 40 potential local answers;',len(rows),'matched replay rows')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output');evaluate(p.parse_args().output)
