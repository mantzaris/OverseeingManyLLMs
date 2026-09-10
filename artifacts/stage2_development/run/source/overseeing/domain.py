"""Deterministic synthetic jobs and explicit public/private information boundaries."""

from dataclasses import asdict, dataclass
import hashlib
import json
import random
from typing import Tuple

ACTIONS = ("replace_filter", "reset_sensor")
CORRECT_ACTION = {"filter": ACTIONS[0], "sensor": ACTIONS[1]}
STAGE1_POLICIES = ("fcfs", "uncertainty", "myopic", "delay")
POLICIES = ("fcfs", "uncertainty", "myopic", "greedy", "delay")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class PublicJob:
    job_id: str
    agent_id: int
    release: int
    deadline: int
    cost_per_tick: int
    terminal_cost: int
    clues: Tuple[str, str]


@dataclass(frozen=True)
class PrivateJob:
    public: PublicJob
    fault: str

    @property
    def correct_action(self):
        return CORRECT_ACTION[self.fault]


@dataclass(frozen=True)
class Scenario:
    seed: int
    jobs: Tuple[PrivateJob, ...]
    horizon: int = 12

    def __post_init__(self):
        ids = [j.public.job_id for j in self.jobs]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate job IDs")
        for job in self.jobs:
            p = job.public
            if job.fault not in CORRECT_ACTION or not 0 <= p.release < p.deadline <= self.horizon:
                raise ValueError("Invalid fault or job window")
            if p.cost_per_tick < 0 or p.terminal_cost < 0:
                raise ValueError("Negative costs")

    def record(self):
        # Full trace metadata is scorer-only; never send this to a model or scheduler.
        return asdict(self)

    @property
    def hash(self):
        return digest(self.record())

    @classmethod
    def from_record(cls, record):
        jobs = []
        for entry in record["jobs"]:
            public = dict(entry["public"])
            public["clues"] = tuple(public["clues"])
            jobs.append(PrivateJob(PublicJob(**public), entry["fault"]))
        return cls(record["seed"], tuple(jobs), record["horizon"])


def generate_scenario(seed=100):
    rng = random.Random(seed)
    jobs = []
    for agent_id in range(3):
        for job_number in range(2):
            release = 6 * job_number + rng.randrange(2)
            fault = rng.choice(("filter", "sensor"))
            opposite = "sensor" if fault == "filter" else "filter"
            clues = tuple(fault if rng.random() < accuracy else opposite for accuracy in (0.8, 0.6))
            public = PublicJob(
                "a{}j{}".format(agent_id, job_number), agent_id, release,
                release + rng.choice((1, 2, 5)), rng.choice((0, 1, 3)),
                rng.choice((0, 8)), clues,
            )
            jobs.append(PrivateJob(public, fault))
    return Scenario(seed, tuple(jobs))


@dataclass(frozen=True)
class ReviewRequest:
    job_id: str
    agent_id: int
    requested_at: int
    deadline: int
    cost_per_tick: int
    terminal_cost: int
    review_ticks: int
    p_error: float
    proposal: str

    def __post_init__(self):
        if self.review_ticks < 1 or not 0 <= self.p_error <= 1:
            raise ValueError("Invalid review duration or probability")

    def remaining_consequence(self, completion):
        if completion > self.deadline:
            return 0
        return self.cost_per_tick * (self.deadline - completion) + self.terminal_cost

    @property
    def tie_key(self):
        return (self.requested_at, self.agent_id, self.job_id)


def observation(job, tick, history):
    if not isinstance(job, PublicJob):
        raise TypeError("Observations accept PublicJob only")
    # Serialize a new value: no mutable references to any agent's stored history.
    return json.loads(canonical({"tick": tick, "job": asdict(job), "history": history}))
