#!/usr/bin/env python3
"""Exact-rational audit of saved public queue choices; no labels or inference."""
from fractions import Fraction
from itertools import permutations
import gzip
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.domain import digest
from overseeing.io import write_json
root=Path('artifacts/stage5_practical');out=root/'batches/evaluation/analysis'
estimator=json.loads((root/'estimator.json').read_text())
pooled=Fraction(estimator['errors']+1,estimator['examples']+2)
risks={str(estimator['pooled_probability']):pooled}
for bin in estimator['bins'].values():
    risks[str(bin['probability'])]=pooled if bin['fallback'] else Fraction(bin['errors']+1,bin['examples']+2)
checked=0;unique=set();regrets=[];ties=[];max_size=0;max_subsets=0
for path in sorted((out/'traces').glob('*/*.json.gz')):
    result=json.loads(gzip.decompress(path.read_bytes()))
    for event in result['events']:
        if event['event']!='dispatch':continue
        tick=event['tick'];pending=event['public_pending']
        assert all(r['arrived']<=tick for r in pending)
        eligible=[r for r in pending if tick+r['review_ticks']<=r['cutoff'] and r['p_error']>0]
        def key(r):return (r['arrived'],r['agent_id'],r['request_id'])
        values=[]
        for n in range(len(eligible)+1):
            for order in permutations(eligible,n):
                finish=tick;benefit=Fraction(0)
                for r in order:
                    finish+=r['review_ticks']
                    if finish<=r['cutoff']:
                        benefit+=risks[str(r['p_error'])]*(r['wrong_transaction_cost']+r['service_failure_cost'])
                values.append((benefit,order))
        best=max(v for v,o in values)
        canonical=min((o for v,o in values if v==best),key=lambda o:(len(o),tuple(key(r) for r in o)))
        exact=canonical[0]['request_id'] if canonical else None
        selected=event['search_choice']
        head=max((v for v,o in values if (o[0]['request_id'] if o else None)==selected),default=Fraction(0))
        record=dict(trace=str(path.relative_to(root)),tick=tick,selected=selected,exact_tie_head=exact,
            best_expected_benefit=str(best),selected_head_expected_benefit=str(head))
        if head<best:regrets.append(record)
        elif selected!=exact:ties.append(record)
        checked+=1;unique.add(digest(dict(tick=tick,pending=sorted(pending,key=key))))
        max_size=max(max_size,len(eligible));max_subsets=max(max_subsets,len(values))
result=dict(label='Post-freeze exact-rational public-state audit; frozen choices retained',
    dispatch_records=checked,unique_public_states=len(unique),maximum_eligible_requests=max_size,
    maximum_enumerated_ordered_subsets=max_subsets,positive_head_value_regret_states=len(regrets),
    exact_canonical_tie_differences=len(ties),regret_records=regrets,tie_records=ties,
    note='Probabilities reconstructed from frozen smoothed counts. No realized task labels or future arrivals used. This audits the current-queue objective, not realized policy superiority.')
write_json(out/'rational_scheduling_audit.json',result);print(json.dumps(result,indent=2))
