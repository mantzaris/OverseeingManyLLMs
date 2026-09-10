"""Five accepted arithmetic cases; explicitly stipulated, never GPU evidence."""

from .domain import PrivateJob, PublicJob, Scenario


def job(job_id, agent, deadline, cost, terminal, fault="filter", clues=("sensor", "sensor")):
    return PrivateJob(PublicJob(job_id, agent, 0, deadline, cost, terminal, clues), fault)


def cases():
    return {
        "easy": (Scenario(-1, (job("easy", 0, 5, 1, 8, clues=("filter", "filter")),)),
                 {"easy": "replace_filter"}, {}, {"fcfs": 0, "uncertainty": 0, "myopic": 0, "delay": 0}),
        "correctable": (Scenario(-2, (job("correctable", 0, 5, 1, 8),)),
                        {"correctable": "reset_sensor"}, {}, {"fcfs": 2, "uncertainty": 2, "myopic": 2, "delay": 2}),
        "competition": (Scenario(-3, (job("A", 0, 2, 0, 8), job("B", 1, 5, 0, 12))),
                        {"A": "reset_sensor", "B": "reset_sensor"}, {},
                        {"fcfs": 0, "uncertainty": 0, "myopic": 8, "greedy": 8, "delay": 0}),
        "expiry": (Scenario(-4, (job("expiry", 0, 1, 1, 8),)),
                   {"expiry": "reset_sensor"}, {}, {"fcfs": 9, "uncertainty": 9, "myopic": 9, "delay": 9}),
        "baseline_wins": (Scenario(-5, (job("B", 0, 2, 0, 12), job("A", 1, 2, 0, 8))),
                          {"A": "replace_filter", "B": "reset_sensor"}, {"A": 0.5, "B": 0.2},
                          {"fcfs": 0, "uncertainty": 12, "myopic": 12, "delay": 12}),
    }
