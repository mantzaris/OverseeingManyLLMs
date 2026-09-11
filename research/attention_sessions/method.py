"""Public-only bounded review sessions with local EDF opportunity preservation.

This module contains no dataset labels, stored review answers, or evaluator API.
All time quantities are assumed abstract units. Classical family setups are shared
by every policy, including consecutive singleton reviews.
"""
from dataclasses import dataclass, asdict
from itertools import combinations
import math

POLICIES = ('no_review', 'fifo', 'edf', 'greedy', 'density', 'fixed_window',
            'unguarded', 'sticky_edf', 'allocation', 'guarded')

@dataclass(frozen=True)
class Request:
    request_id: str
    context: str
    suggested_context: str
    arrival: float
    deadline: float
    weight: float
    risk: float
    gain: float
    proposal: str
    evidence: dict
    scope: str = ''

    def __post_init__(self):
        for x in (self.arrival, self.deadline, self.weight, self.risk, self.gain):
            if not math.isfinite(x): raise ValueError('Non-finite public input')
        if self.deadline < self.arrival or self.weight < 0: raise ValueError('Invalid request')
        if not 0 <= self.risk <= 1 or not -1 <= self.gain <= 1: raise ValueError('Invalid probability')
        allowed={'equipment_mode','window_start','window_end','sample_interval_minutes','n_samples','units','statistic_order','readings'}
        if set(self.evidence)-allowed: raise ValueError('Evidence must use the public observation schema')

    @property
    def value(self): return self.weight * self.gain
    @property
    def tie(self): return self.arrival, self.request_id

@dataclass(frozen=True)
class Settings:
    setup: float = 1
    switch: float = .25
    decision: float = 1
    coordination: float = .25
    budget: float = 12
    max_group: int = 3
    reuse: bool = True
    reconsider: bool = True
    fixed_window: float = 2

    def __post_init__(self):
        if self.decision <= 0 or self.max_group not in (1, 2, 3): raise ValueError('Invalid bound')
        if any(not math.isfinite(x) or x < 0 for x in
               (self.setup, self.switch, self.decision, self.coordination, self.budget)):
            raise ValueError('Invalid time')


def parts(request, context, settings, position=0):
    changed = context != request.context
    return dict(setup=settings.setup if changed or not settings.reuse else 0,
                switch=settings.switch if changed and context is not None else 0,
                decision=settings.decision,
                coordination=settings.coordination if position else 0)


def schedule(order, now, context, settings, remaining, group=False, position=0):
    """Return exact per-item completion times, never batch-end completion."""
    rows=[]; used=0
    for i, r in enumerate(order):
        p=parts(r, context, settings, i+position if group else 0)
        d=math.fsum(p.values()); used+=d; now+=d
        rows.append(dict(request_id=r.request_id, finish=now, parts=p,
                         timely=now <= r.deadline + 1e-9 and used <= remaining + 1e-9))
        context=r.context
    return rows


def edf_plan(requests, now, context, settings, remaining):
    """Deterministic feasible EDF continuation; it can skip impossible items."""
    selected=[]
    for r in sorted(requests, key=lambda r:(r.deadline,r.tie)):
        rows=schedule(selected+[r],now,context,settings,remaining)
        if rows[-1]['timely']: selected.append(r)
    return selected


def certificate(group, requests, now, context, settings, remaining, position=0):
    protected=edf_plan(requests,now,context,settings,remaining)
    own=schedule(group,now,context,settings,remaining,group=True,position=position)
    if not own or not all(x['timely'] for x in own):
        return dict(valid=False, protected=[r.request_id for r in protected], lost=['session infeasible'], slack={})
    ids={r.request_id for r in group};spent=own[-1]['finish']-now
    tail=[r for r in protected if r.request_id not in ids]
    rows=schedule(tail,own[-1]['finish'],group[-1].context,settings,remaining-spent)
    lost=[x['request_id'] for x in rows if not x['timely']]
    return dict(valid=not lost, protected=[r.request_id for r in protected], lost=lost,
                slack={r.request_id:round(r.deadline-x['finish'],6) for r,x in zip(tail,rows)})


def candidates(requests, max_group):
    # Suggestion similarity is never sufficient: canonical context must agree.
    keys=sorted({(r.context,r.suggested_context) for r in requests})
    for key in keys:
        group=sorted([r for r in requests if (r.context,r.suggested_context)==key],key=lambda r:(r.deadline,r.tie))
        for n in range(1,min(max_group,len(group))+1):
            for sub in combinations(group,n): yield list(sub)


def select(policy, requests, now, context, settings, remaining):
    if policy not in POLICIES: raise ValueError('Unknown policy')
    if any(type(r) is not Request or r.arrival > now+1e-9 for r in requests):
        raise ValueError('Only released public Request objects may be scheduled')
    eligible=[r for r in requests if r.value > 0 and schedule([r],now,context,settings,remaining)[0]['timely']]
    info=dict(policy=policy, eligible=[r.request_id for r in eligible], checked=0, rejected=0)
    if policy=='no_review' or not eligible: return [],dict(info,reason='No positive feasible intervention' if policy!='no_review' else 'No-review control')
    order=lambda r:(r.deadline,r.tie)
    if policy=='fifo': group=[min(eligible,key=lambda r:r.tie)]
    elif policy=='edf': group=[min(eligible,key=order)]
    elif policy=='greedy': group=[min(eligible,key=lambda r:(-r.value,r.tie))]
    elif policy=='density': group=[min(eligible,key=lambda r:(-r.value/sum(parts(r,context,settings).values()),r.tie))]
    elif policy=='sticky_edf':
        sticky=sorted([r for r in eligible if r.context==context],key=order)
        group=next(([r] for r in sticky if certificate([r],eligible,now,context,settings,remaining)['valid']),[min(eligible,key=order)])
    elif policy=='allocation':
        # Single-expert reduction of global cost/capacity assignment. Conservative
        # independent costs, then EDF. No claim to reproduce DeCCaF's HEM/quotas.
        best=None;group=[]
        for n in range(1,len(eligible)+1):
            for sub in combinations(eligible,n):
                effort=sum(settings.setup+settings.decision for r in sub)
                if effort>remaining+1e-9:continue
                key=(-sum(r.value for r in sub),effort,tuple(r.request_id for r in sub))
                if best is None or key<best:best=key;group=[min(sub,key=order)]
        if not group:group=[min(eligible,key=order)]
    elif policy=='fixed_window':
        if now/settings.fixed_window < math.ceil(now/settings.fixed_window)-1e-9:
            return [],dict(info,reason='Wait for fixed notification window',wake=math.ceil(now/settings.fixed_window)*settings.fixed_window)
        first=min(eligible,key=lambda r:r.tie)
        group=sorted([r for r in eligible if r.context==first.context and r.suggested_context==first.suggested_context],key=lambda r:r.tie)[:settings.max_group]
        while group and not all(x['timely'] for x in schedule(group,now,context,settings,remaining,True)):group.pop()
    else:
        best=None;group=[]
        for sub in candidates(eligible,settings.max_group):
            info['checked']+=1
            rows=schedule(sub,now,context,settings,remaining,True)
            if not all(x['timely'] for x in rows):continue
            cert=certificate(sub,eligible,now,context,settings,remaining)
            if policy=='guarded' and not cert['valid']:info['rejected']+=1;continue
            duration=rows[-1]['finish']-now;value=math.fsum(r.value for r in sub)
            key=(-value/duration,-value,duration,tuple(r.request_id for r in sub))
            if best is None or key<best:best=key;group=sub
        if not group:group=[min(eligible,key=order)]
    cert=certificate(group,eligible,now,context,settings,remaining) if group else {}
    return group,dict(info,reason=('Preserves the feasible EDF continuation' if policy=='guarded' else 'Selection rule: '+policy),certificate=cert)


def validate_shared_answer(requests, declared_scope, exact_ids):
    """Only explicit matching scope may share an answer; context is insufficient.
    Main HVAC replay supplies no shared decision scopes, so this always rejects
    propagation there. This guard is exercised only in separate mechanics tests.
    """
    if not declared_scope or set(exact_ids)!={r.request_id for r in requests}:
        raise ValueError('Shared answer needs explicit exact recipient scope')
    if not requests or any(r.scope!=declared_scope for r in requests):
        raise ValueError('Context similarity is not a shared decision dependency')
    return tuple(sorted(exact_ids))
