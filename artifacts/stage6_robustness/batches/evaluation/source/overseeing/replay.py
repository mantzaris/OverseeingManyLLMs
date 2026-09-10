"""Score saved action trajectories independently of the simulator's loss ledger."""

from .domain import ACTIONS, Scenario
from .io import read_events


def replay_score(path):
    events = read_events(path)
    if not events or events[0]["event"] != "episode_started":
        return {"status": "not_run", "total_loss": None}
    scenario = Scenario.from_record(events[0]["scenario"])
    if scenario.hash != events[0]["scenario_hash"]:
        raise ValueError("Scenario hash mismatch")
    finished = [e for e in events if e["event"] == "episode_finished"]
    if not finished or finished[-1]["status"] != "completed":
        return {"status": "incomplete", "total_loss": None}
    total, correct = 0, 0
    for job in scenario.jobs:
        p = job.public
        proposals = [e for e in events if e["event"] == "proposal" and e["job_id"] == p.job_id]
        if len(proposals) != 1 or proposals[0]["tick"] != p.release:
            raise ValueError("Missing/duplicate/mistimed proposal: " + p.job_id)
        action = proposals[0]["primary"]
        if action not in ACTIONS:
            raise ValueError("Invalid saved action")
        responses = [e for e in events if e["event"] == "review_completed" and e["job_id"] == p.job_id]
        losses = 0
        for tick in range(p.release, p.deadline + 1):
            for response in responses:
                if response["tick"] == tick:
                    # Arrival at the deadline precedes terminal scoring.
                    if response["instructed_action"] != job.correct_action or not response["applied"]:
                        raise ValueError("Invalid timely supervisor response")
                    action = response["instructed_action"]
            wrong = action != job.correct_action
            losses += (p.terminal_cost if tick == p.deadline else p.cost_per_tick) * wrong
        if any(r["applied"] for r in responses if r["tick"] > p.deadline):
            raise ValueError("A late review reopened a closed job")
        closed = [e for e in events if e["event"] == "job_closed" and e["job_id"] == p.job_id]
        if len(closed) != 1 or closed[0]["tick"] != p.deadline or closed[0]["job_loss"] != losses:
            raise ValueError("Job scoring mismatch: " + p.job_id)
        correct += int(action == job.correct_action)
        total += losses
    if finished[-1]["total_loss"] != total or finished[-1]["correct_jobs"] != correct:
        raise ValueError("Saved aggregate does not match replayed actions")
    return {"status": "verified", "total_loss": total, "correct_jobs": correct,
            "scenario_hash": scenario.hash, "evidence": events[0]["evidence"]}
