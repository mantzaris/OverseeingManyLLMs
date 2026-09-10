"""A bounded discrete-time simulator; inference latency never advances a tick."""

from dataclasses import asdict
from pathlib import Path
import time

from .domain import ACTIONS, ReviewRequest, observation
from .io import append_jsonl, utc_now
from .policies import choose, eligible_requests


class ProposalFailure(RuntimeError):
    pass


class StipulatedProposals:
    """Mechanics only. This provider never claims or performs LLM inference."""

    evidence = "stipulated_mechanics_only"

    def __init__(self, actions):
        self.actions = dict(actions)
        self.observations = []

    def pair(self, public_observation, metadata):
        self.observations.append(public_observation)
        action = self.actions[metadata["job_id"]]
        return action, action

    def stats(self):
        return {"scheduled_calls": 0, "attempts": 0, "prompt_tokens": 0,
                "completion_tokens": 0, "unknown_token_attempts": 0,
                "request_wall_seconds": 0.0}


def run_episode(scenario, policy, provider, events_path, review_ticks=2,
                fixture_probabilities=None, fixture_dispatch=None, estimator=None, record_dispatch=False):
    if review_ticks < 1:
        raise ValueError("Reviews require nonzero duration")
    if (fixture_probabilities is not None or fixture_dispatch is not None) and provider.evidence != "stipulated_mechanics_only":
        raise ValueError("Fixture overrides are not permitted for live inference")
    path = Path(events_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=False)
    started = time.monotonic()
    sequence = 0

    def emit(kind, tick, **fields):
        nonlocal sequence
        append_jsonl(path, dict(seq=sequence, event=kind, tick=tick, wall_utc=utc_now(), **fields))
        sequence += 1

    emit("episode_started", 0, policy=policy, evidence=provider.evidence,
         scenario=scenario.record(), scenario_hash=scenario.hash,
         review_ticks=review_ticks, p_error=("frozen_agreement" if estimator else
                                           "fixture_override" if fixture_probabilities else 0.5),
         estimator_hash=estimator.estimator_hash if estimator else None,
         planned_calls=12 if provider.evidence in ("live_a100", "live_l40s", "live_gpu") else 0)
    private = {j.public.job_id: j for j in scenario.jobs}
    histories = {j.public.agent_id: [] for j in scenario.jobs}
    states, pending = {}, {}
    busy = None
    accrued_loss, correct_jobs = 0, 0
    starts, completions, corrections, late, expired, busy_ticks = 0, 0, 0, 0, 0, 0
    status, error, tick = "completed", None, 0
    try:
        for tick in range(scenario.horizon + 1):
            # 1. Complete reviews. Truth is consulted only here and in scoring.
            if busy is not None and busy["finish"] == tick:
                job_id = busy["job_id"]
                job = private[job_id]
                state = states[job_id]
                response = job.correct_action
                applied = not state["closed"] and tick <= job.public.deadline
                changed = applied and state["action"] != response
                completions += 1
                corrections += int(changed)
                late += int(not applied)
                if applied:
                    state["action"] = response
                # A late response is still feedback, but cannot reopen the job.
                histories[job.public.agent_id].append({
                    "job_id": job_id, "review_completed_at": tick,
                    "instructed_action": response, "applied": applied,
                })
                emit("review_completed", tick, job_id=job_id, instructed_action=response,
                     applied=applied, changed=bool(changed), late=not applied)
                busy = None

            # 2. Close due jobs; accrued loss is never returned as agent feedback.
            for job in sorted(scenario.jobs, key=lambda j: j.public.job_id):
                p = job.public
                if p.deadline != tick:
                    continue
                state = states[p.job_id]
                wrong = state["action"] != job.correct_action
                terminal_loss = p.terminal_cost * wrong
                accrued_loss += terminal_loss
                state["loss"] += terminal_loss
                state["closed"] = True
                correct_jobs += int(not wrong)
                if p.job_id in pending:
                    request = pending.pop(p.job_id)
                    expired += 1
                    if p.cost_per_tick == 0 and p.terminal_cost == 0:
                        category = "zero_value"
                    elif request.remaining_consequence(p.release + review_ticks) <= 0:
                        category = "infeasible_at_arrival"
                    else:
                        category = "opportunity_lost_while_waiting"
                    emit("request_expired", tick, job_id=p.job_id, category=category,
                         initial_proposal_wrong=state["initial"] != job.correct_action)
                emit("job_closed", tick, job_id=p.job_id, action=state["action"],
                     correct=not wrong, terminal_loss=terminal_loss, job_loss=state["loss"])

            # 3. Release jobs. All calls at this tick finish before any dispatch.
            for job in sorted(scenario.jobs, key=lambda j: (j.public.agent_id, j.public.job_id)):
                p = job.public
                if p.release != tick:
                    continue
                public_observation = observation(p, tick, histories[p.agent_id])
                emit("observation", tick, job_id=p.job_id, public_observation=public_observation)
                primary, secondary = provider.pair(public_observation, {
                    "scenario_seed": scenario.seed, "agent_id": p.agent_id, "job_id": p.job_id,
                })
                if primary not in ACTIONS or secondary not in ACTIONS:
                    raise ProposalFailure("Provider returned an invalid action")
                states[p.job_id] = {"initial": primary, "action": primary, "closed": False, "loss": 0}
                histories[p.agent_id].append({"job_id": p.job_id, "proposed_at": tick, "action": primary})
                request = ReviewRequest(p.job_id, p.agent_id, tick, p.deadline, p.cost_per_tick,
                                        p.terminal_cost, review_ticks,
                                        (estimator.predict(primary, secondary) if estimator else
                                         (fixture_probabilities or {}).get(p.job_id, 0.5)), primary)
                pending[p.job_id] = request
                emit("proposal", tick, job_id=p.job_id, primary=primary, secondary=secondary,
                     agreement=primary == secondary, p_error=request.p_error,
                     evidence=provider.evidence)
                emit("request_queued", tick, request=asdict(request))

            # 4. Dispatch using freshly copied, immutable public records only.
            if tick < scenario.horizon and busy is None:
                records = tuple(pending.values())
                selected = fixture_dispatch(records, tick) if fixture_dispatch else choose(policy, records, tick)
                if record_dispatch:
                    emit("dispatch_considered", tick, selected=selected,
                         eligible=[asdict(r) for r in eligible_requests(records, tick)])
                if selected is not None:
                    request = pending.pop(selected)
                    busy = {"job_id": selected, "start": tick, "finish": tick + request.review_ticks}
                    starts += 1
                    emit("review_started", tick, **busy)
            emit("queue_snapshot", tick, pending=sorted(pending), busy=dict(busy) if busy else None)

            # 5. Accrue loss over [tick, tick+1), never after the horizon.
            if tick < scenario.horizon:
                busy_ticks += int(busy is not None)
                for job_id, state in states.items():
                    if not state["closed"]:
                        job = private[job_id]
                        loss = job.public.cost_per_tick * (state["action"] != job.correct_action)
                        state["loss"] += loss
                        accrued_loss += loss
                        emit("interval_scored", tick, job_id=job_id, loss=loss)
    except Exception as exc:
        status = "failed"
        error = "{}: {}".format(type(exc).__name__, exc)
        emit("episode_failed", tick, error=error)

    if status == "completed" and any(not s["closed"] for s in states.values()):
        status, error = "failed", "Episode ended with open jobs"
    result = {
        "policy": policy, "seed": scenario.seed, "scenario_hash": scenario.hash,
        "evidence": provider.evidence, "status": status, "error": error,
        "planned_calls": 12 if provider.evidence in ("live_a100", "live_l40s", "live_gpu") else 0,
        "total_loss": accrued_loss if status == "completed" else None,
        "accrued_loss": accrued_loss,
        "loss_upper_bound": sum(j.public.cost_per_tick * (j.public.deadline - j.public.release)
                                + j.public.terminal_cost for j in scenario.jobs),
        "correct_jobs": correct_jobs if status == "completed" else None,
        "jobs_closed": sum(s["closed"] for s in states.values()),
        "reviews_started": starts, "reviews_completed": completions,
        "corrections": corrections, "late_returns": late, "expired_requests": expired,
        "review_busy_ticks": busy_ticks, "simulated_ticks_completed": scenario.horizon if status == "completed" else tick,
        "incomplete_service": busy["job_id"] if busy else None,
        "episode_wall_seconds": round(time.monotonic() - started, 6),
    }
    result.update(provider.stats())
    emit("episode_finished", tick, **result)
    return result
