"""Instrumented exact public-queue planning, with order-invariant value summation."""
from dataclasses import asdict,replace
from itertools import permutations
import math
import time

from .domain import ReviewRequest
from .policies import choose,eligible_requests


class ResearchScheduler:
    def __init__(self,policy,closure_penalty=0):
        if closure_penalty not in (0,4,8):raise ValueError('Undeclared objective penalty')
        self.policy,self.closure_penalty=policy,closure_penalty
        self.last_record=None

    def __call__(self,pending,tick):
        if len(pending)>6 or any(type(r) is not ReviewRequest for r in pending):
            raise ValueError('Exact research scheduler requires at most six public requests')
        adjusted=tuple(replace(r,terminal_cost=r.terminal_cost+self.closure_penalty) for r in pending)
        start=time.perf_counter();eligible=eligible_requests(adjusted,tick)
        examined=0
        if self.policy!='delay':
            selected=choose(self.policy,adjusted,tick)
        else:
            # Empty subset plus every ordered subset; no pruning, truncation, or approximation.
            best_key,selected=(0,0,()),None
            examined=1
            for length in range(1,len(eligible)+1):
                for order in permutations(eligible,length):
                    completion=tick;terms=[]
                    for request in order:
                        completion+=request.review_ticks
                        terms.append(request.p_error*request.remaining_consequence(completion))
                    value=math.fsum(terms)
                    key=(-value,length,tuple(r.tie_key for r in order))
                    examined+=1
                    if key<best_key:best_key,selected=key,order[0].job_id
        elapsed=time.perf_counter()-start
        self.last_record=dict(policy=self.policy,closure_penalty=self.closure_penalty,pending_count=len(pending),eligible_count=len(eligible),
            eligible=[asdict(r) for r in eligible],public_pending=[asdict(r) for r in pending],selected=selected,
            planning_seconds=elapsed,ordered_subsets_evaluated=examined,
            summation='math.fsum; historical sequential-addition implementation retained for historical commands')
        return selected
