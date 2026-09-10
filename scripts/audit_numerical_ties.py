#!/usr/bin/env python3
"""Exact rational audit of saved public search states; no policy changes or inference."""
import argparse
from dataclasses import replace
from fractions import Fraction
from itertools import permutations
from math import gcd
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from overseeing.domain import ReviewRequest
from overseeing.policies import eligible_requests
from overseeing.research_scheduler import ResearchScheduler
from overseeing.io import read_events,write_json,write_csv


def exact_heads(requests,tick):
    fractions=[Fraction(r.p_error).limit_denominator(1000) for r in requests]
    assert all(abs(float(p)-r.p_error)<1e-15 for p,r in zip(fractions,requests))
    scale=1
    for p in fractions:scale=scale*p.denominator//gcd(scale,p.denominator)
    weights={r.job_id:p.numerator*(scale//p.denominator) for r,p in zip(requests,fractions)}
    best_key=(0,0,());canonical=None;best=0;by_head={None:0}
    for length in range(1,len(requests)+1):
        for order in permutations(requests,length):
            completion=tick;value=0
            for r in order:completion+=r.review_ticks;value+=weights[r.job_id]*r.remaining_consequence(completion)
            head=order[0].job_id;by_head[head]=max(by_head.get(head,0),value)
            key=(-value,length,tuple(r.tie_key for r in order))
            if key<best_key:best_key=key;canonical=head;best=value
    return best,by_head,canonical,scale


def main(root,batches,label):
    root=Path(root);rows=[];uniform=0;scaling=[];regrets=[]
    for batch in batches:
        for path in sorted((root/'batches'/batch/'episodes').rglob('events.jsonl.gz')):
            events=read_events(path);proposals={e['job_id']:e for e in events if e['event']=='proposal'}
            for e in events:
                if e['event']!='planning_decision':continue
                pending=tuple(ReviewRequest(**r) for r in e['public_pending']);eligible=tuple(ReviewRequest(**r) for r in e['eligible'])
                actual=ResearchScheduler('delay',e['closure_penalty'])(pending,e['tick'])
                if e['policy']=='delay':assert actual==e['selected']
                best,heads,canonical,scale=exact_heads(eligible,e['tick'])
                regret=(best-heads[actual])/scale
                record=dict(batch=batch,path=str(path.relative_to(root)),tick=e['tick'],policy=e['policy'],eligible=len(eligible),floating_choice=actual,exact_canonical_choice=canonical,exact_regret=regret,canonical_tie_difference=actual!=canonical)
                rows.append(record)
                if regret:regrets.append(record)
                frozen=tuple(replace(r,p_error=13/89 if proposals[r.job_id]['agreement'] else 18/98) for r in pending)
                if len({r.p_error for r in frozen})!=1:continue
                uniform+=1
                a=ResearchScheduler('delay',e['closure_penalty'])(frozen,e['tick'])
                b=ResearchScheduler('delay',e['closure_penalty'])(tuple(replace(r,p_error=18/98) for r in pending),e['tick'])
                if a!=b:
                    effective=eligible_requests(tuple(replace(r,terminal_cost=r.terminal_cost+e['closure_penalty']) for r in frozen),e['tick'])
                    value,head_values,canonical,scale=exact_heads(effective,e['tick'])
                    assert head_values[a]==head_values[b]==value
                    scaling.append(dict(batch=batch,path=str(path.relative_to(root)),tick=e['tick'],frozen_choice=a,pooled_choice=b,exact_canonical_choice=canonical,both_exactly_optimal=True))
    out=root/'numerical_audits';out.mkdir(exist_ok=True)
    write_csv(out/(label+'_states.csv'),rows);write_json(out/(label+'_constant_scaling.json'),scaling)
    result=dict(label=label,batches=batches,saved_public_states=len(rows),floating_search_heads_with_exact_positive_regret=len(regrets),canonical_tie_differences=sum(r['canonical_tie_difference'] for r in rows),
        uniform_frozen_risk_states=uniform,constant_scaling_choice_differences=len(scaling),all_scaling_differences_exactly_cooptimal=True,
        interpretation='Enumeration remains exhaustive. Floating products/sums can resolve exact rational ties differently; constant risk rescaling carries no ranking information in these states. These are same-state numerical diagnostics, not new trajectories.',method_changed=False,new_generations=0)
    write_json(out/(label+'_summary.json'),result)
    assert not regrets,'A floating search choice lost exact expected value; inspect preserved state audit'
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',default='artifacts/stage4_research');parser.add_argument('--batches',nargs='+',required=True);parser.add_argument('--label',required=True);a=parser.parse_args();print(main(a.root,a.batches,a.label))
