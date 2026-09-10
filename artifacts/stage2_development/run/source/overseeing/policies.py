"""Public-record schedulers; no simulator, scorer, or hidden-state imports."""

from itertools import permutations
from .domain import POLICIES, ReviewRequest


def eligible_requests(pending, tick):
    if any(type(r) is not ReviewRequest for r in pending):
        raise TypeError("Schedulers accept public ReviewRequest records only")
    return tuple(r for r in pending if r.p_error * r.remaining_consequence(tick + r.review_ticks) > 0)


def choose(policy, pending, tick):
    if policy not in POLICIES:
        raise ValueError("Unknown policy: " + policy)
    eligible = eligible_requests(pending, tick)
    if not eligible:
        return None
    if policy == "fcfs":
        return min(eligible, key=lambda r: r.tie_key).job_id
    if policy == "uncertainty":
        return min(eligible, key=lambda r: (-r.p_error, r.tie_key)).job_id
    if policy == "myopic":
        return min(eligible, key=lambda r: (-r.p_error * r.remaining_consequence(tick), r.tie_key)).job_id
    if policy == "greedy":
        return min(eligible, key=lambda r: (-r.p_error * r.remaining_consequence(tick + r.review_ticks),
                                            r.tie_key)).job_id
    # Includes empty, then all ordered subsets (16 total for three requests).
    best_key, best = (0, 0, ()), None
    for length in range(1, len(eligible) + 1):
        for order in permutations(eligible, length):
            completion, value = tick, 0.0
            for request in order:
                completion += request.review_ticks
                value += request.p_error * request.remaining_consequence(completion)
            key = (-value, length, tuple(r.tie_key for r in order))
            if key < best_key:
                best_key, best = key, order[0].job_id
    return best
