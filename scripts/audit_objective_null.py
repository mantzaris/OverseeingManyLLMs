#!/usr/bin/env python3
"""Check the competition extension's structural null with exact public arithmetic."""
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from overseeing.io import write_json


def audit():
    states=0;checks=0
    for deadlines in permutations((2,4,5)):
        for penalties in permutations((4,8,12)):
            for risks in product((Fraction(13,89),Fraction(18,98)),repeat=3):
                states+=1
                for duration in (1,2):
                    expected=frozenset(range(3)) if duration==1 else frozenset(i for i,k in enumerate(penalties) if k>=8)
                    for extra in (0,4,8):
                        best=Fraction(0);sets=set()
                        for length in range(1,4):
                            for order in permutations(range(3),length):
                                served=frozenset(i for position,i in enumerate(order,1) if duration*position<=deadlines[i])
                                value=sum((risks[i]*(penalties[i]+extra) for i in served),Fraction(0))
                                if value>best:best=value;sets={served}
                                elif value==best:sets.add(served)
                        assert sets=={expected},(deadlines,penalties,risks,duration,extra,sets)
                        checks+=1
    result=dict(status='verified',public_wave_states=states,duration_objective_checks=checks,
        risks=['13/89','18/98'],deadlines=[2,4,5],penalties=[4,8,12],review_durations=[1,2],closure_penalties=[0,4,8],
        one_tick='Every exact-optimal plan serves all three jobs before their deadlines.',
        two_ticks='Every exact-optimal plan usefully serves the cost-eight and cost-twelve jobs.',
        interpretation='No lambda-dependent change in the exact-optimal served set for this competition grid. Floating ties and fresh actions/history changes are separate mechanisms.',
        hidden_labels_used=False,new_generations=0,method_changed=False)
    write_json(Path('artifacts/stage4_research/numerical_audits/objective_structural_null.json'),result)
    return result

if __name__=='__main__':print(audit())
