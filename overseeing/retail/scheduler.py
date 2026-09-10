"""Expected avoidable retail processing loss on a public queue."""
from dataclasses import asdict, dataclass
from itertools import permutations
import math
import time

POLICIES = ('no_review', 'fcfs', 'edf', 'uncertainty', 'greedy', 'search')


@dataclass(frozen=True)
class TransactionRequest:
    request_id: str
    agent_id: int
    arrived: int
    cutoff: int
    review_ticks: int
    p_error: float
    wrong_transaction_cost: int
    service_failure_cost: int = 4

    @property
    def tie_key(self): return (self.arrived, self.agent_id, self.request_id)

    def benefit(self, completion):
        # A wrong posted transaction causes both a failed service request and
        # its declared processing/rework consequence. There is no downtime term.
        return self.p_error * (self.service_failure_cost + self.wrong_transaction_cost) if completion <= self.cutoff else 0.0


def choose(policy, pending, tick):
    if policy not in POLICIES: raise ValueError('Unknown retail policy')
    if len(pending) > 3 or any(type(r) is not TransactionRequest for r in pending):
        raise ValueError('Expected at most three public retail requests')
    start = time.perf_counter()
    eligible = sorted((r for r in pending if r.arrived <= tick and r.benefit(tick+r.review_ticks)>0), key=lambda r:r.tie_key)
    selected = None; examined = 0
    if eligible and policy != 'no_review':
        if policy == 'fcfs': selected = eligible[0]
        elif policy == 'edf': selected = min(eligible,key=lambda r:(r.cutoff,r.tie_key))
        elif policy == 'uncertainty': selected = min(eligible,key=lambda r:(-r.p_error,r.tie_key))
        elif policy == 'greedy': selected = min(eligible,key=lambda r:(-r.benefit(tick+r.review_ticks),r.tie_key))
        else:
            best = (0,0,()); examined = 1
            for length in range(1,len(eligible)+1):
                for order in permutations(eligible,length):
                    finish=tick; values=[]
                    for request in order:
                        finish += request.review_ticks; values.append(request.benefit(finish))
                    key=(-math.fsum(values),length,tuple(r.tie_key for r in order));examined+=1
                    if key<best: best,selected=key,order[0]
    record=dict(policy=policy,tick=tick,public_pending=[asdict(r) for r in pending],
        eligible=[r.request_id for r in eligible],selected=selected.request_id if selected else None,
        planning_seconds=time.perf_counter()-start,ordered_subsets_evaluated=examined)
    return record['selected'],record
