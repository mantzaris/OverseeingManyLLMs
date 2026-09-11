"""Independent exhaustive contingent tree recursion for small reference cases."""
from functools import lru_cache

def solve(planner,state,budget,horizon=None):
    if len(planner.factors)>6 or budget>6:raise ValueError('Reference limited to six factors and six unit budget')
    horizon=budget if horizon is None else horizon
    @lru_cache(None)
    def visit(s,b,h):
        stop=planner.terminal(s)[0];options=[(stop,None)]
        if h:
            for i in planner.available(s,b):
                c=planner.factors[i].cost
                expected=planner.question_penalty*c
                for _,prob,posterior in planner.response_branches(s,i):
                    expected+=prob*visit(posterior,b-c,h-1)[0]
                options.append((expected,i))
        best=options[0]
        for expected,i in options[1:]:
            if expected<best[0]-1e-10 or (abs(expected-best[0])<=1e-10 and best[1] is not None and planner.factors[i].id<planner.factors[best[1]].id):best=(expected,i)
        return best
    v,a=visit(state,budget,horizon)
    return dict(value=v,action=a,nodes=visit.cache_info().misses,cache_hits=visit.cache_info().hits)
