"""Frozen public-action prediction; truth is used only by offline extraction/fitting."""

from dataclasses import dataclass
import hashlib
from pathlib import Path

from .domain import ACTIONS, Scenario, digest
from .io import read_events, utc_now


def calibration_examples(path):
    """Include every collected pair, reviewed or not, even in a partial episode."""
    events = read_events(path)
    if not events or events[0]["event"] != "episode_started":
        return []
    scenario = Scenario.from_record(events[0]["scenario"])
    if scenario.hash != events[0]["scenario_hash"]:
        raise ValueError("Calibration scenario hash mismatch")
    truth = {j.public.job_id: j.correct_action for j in scenario.jobs}
    reviewed = {e["job_id"] for e in events if e["event"] == "review_completed"}
    examples, seen = [], set()
    for e in events:
        if e["event"] != "proposal":
            continue
        if e["job_id"] in seen or e["primary"] not in ACTIONS or e["secondary"] not in ACTIONS:
            raise ValueError("Invalid or duplicate calibration proposal")
        seen.add(e["job_id"])
        examples.append({"seed": scenario.seed, "policy": events[0]["policy"], "job_id": e["job_id"],
                         "agreement": e["primary"] == e["secondary"],
                         "initial_error": int(e["primary"] != truth[e["job_id"]]),
                         "primary": e["primary"], "secondary": e["secondary"],
                         "p_error": e["p_error"], "reviewed": e["job_id"] in reviewed})
    return examples


def fit_estimator(examples, provenance):
    if not examples:
        raise ValueError("No successfully collected calibration pairs")
    pooled_n = len(examples)
    pooled_errors = sum(e["initial_error"] for e in examples)
    pooled = (pooled_errors + 1) / (pooled_n + 2)
    bins = {}
    for name, agreement in (("agree", True), ("disagree", False)):
        selected = [e for e in examples if e["agreement"] == agreement]
        n, errors = len(selected), sum(e["initial_error"] for e in selected)
        estimate = (errors + 1) / (n + 2)
        bins[name] = {"example_count": n, "error_count": errors, "bin_smoothed_estimate": estimate,
                      "pooled_fallback": n < 10, "probability": pooled if n < 10 else estimate}
    record = {"version": 1, "fitted_utc": utc_now(), "feature": "primary_equals_secondary",
              "label": "first_proposal_wrong_before_any_correction", "minimum_bin_count": 10,
              "pooled": {"example_count": pooled_n, "error_count": pooled_errors, "probability": pooled},
              "bins": bins, "provenance": provenance}
    record["estimator_hash"] = digest(record)
    return record


@dataclass(frozen=True)
class AgreementEstimator:
    agree_probability: float
    disagree_probability: float
    estimator_hash: str

    def __post_init__(self):
        if not all(0 <= p <= 1 for p in (self.agree_probability, self.disagree_probability)):
            raise ValueError("Invalid error probability")

    @classmethod
    def from_record(cls, record):
        if digest({k: v for k, v in record.items() if k != "estimator_hash"}) != record["estimator_hash"]:
            raise ValueError("Frozen estimator hash mismatch")
        return cls(record["bins"]["agree"]["probability"], record["bins"]["disagree"]["probability"],
                   record["estimator_hash"])

    def predict(self, primary, secondary):
        # No observation, hidden label, review status, or simulator object is accepted.
        if type(primary) is not str or type(secondary) is not str or primary not in ACTIONS or secondary not in ACTIONS:
            raise TypeError("Estimator accepts two sampled action strings only")
        return self.agree_probability if primary == secondary else self.disagree_probability


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
