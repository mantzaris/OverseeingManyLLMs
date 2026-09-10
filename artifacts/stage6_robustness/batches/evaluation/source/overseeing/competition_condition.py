"""Constructed development condition; independent public and hidden random streams."""

import random
from .domain import PrivateJob, PublicJob, Scenario, digest


GENERATOR_SPEC = {
    "agents": 3, "jobs_per_agent": 2, "horizon": 12, "releases": [0, 6],
    "deadline_windows": [2, 4, 5], "terminal_penalties": [4, 8, 12], "downtime_cost": 0,
    "fault_prior": {"filter": 0.5, "sensor": 0.5}, "clue_accuracies": [0.8, 0.6],
    "random_streams": "SHA256(seed, wave, component); independent deadlines, penalties, faults/clues streams",
    "inclusion": "All seeds 300-315; no conditioning on actions, errors, or outcomes",
}


def component_rng(seed, wave, component):
    return random.Random(int(digest({"seed": seed, "wave": wave, "component": component}), 16))


def hidden_fault_and_clues(rng):
    fault = rng.choice(("filter", "sensor"))
    opposite = "sensor" if fault == "filter" else "filter"
    clues = tuple(fault if rng.random() < accuracy else opposite for accuracy in (0.8, 0.6))
    return fault, clues


def generate_competition_scenario(seed):
    jobs = []
    for wave, release in enumerate((0, 6)):
        windows, penalties = [2, 4, 5], [4, 8, 12]
        component_rng(seed, wave, "deadlines").shuffle(windows)
        component_rng(seed, wave, "penalties").shuffle(penalties)
        hidden_rng = component_rng(seed, wave, "faults_and_clues")
        for agent in range(3):
            fault, clues = hidden_fault_and_clues(hidden_rng)
            public = PublicJob("a{}j{}".format(agent, wave), agent, release,
                               release + windows[agent], 0, penalties[agent], clues)
            jobs.append(PrivateJob(public, fault))
    return Scenario(seed, tuple(jobs))
