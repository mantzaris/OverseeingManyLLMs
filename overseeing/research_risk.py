"""Frozen historical predictions and a public generative-model reference, never truth."""
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path

from .domain import ACTIONS, PublicJob, digest
from .estimator import AgreementEstimator, file_hash

ESTIMATOR_HASH = '54d9a97e25f5cb22cf0df216293303ea5c945713032c6bc1282c55fcf327e085'
ESTIMATOR_FILE_HASH = '4ce8309bce27b70cdab1bd707bc3468f1039e88d4c30632541231efd6dde0d9d'


def analytical_error(public_job, primary):
    if type(public_job) is not PublicJob or primary not in ACTIONS:
        raise TypeError('Analytical reference accepts PublicJob and a valid first action only')
    if len(public_job.clues) != 2 or any(c not in ('filter', 'sensor') for c in public_job.clues):
        raise ValueError('Unknown public clue')
    weights = {}
    for fault in ('filter', 'sensor'):
        likelihood = Fraction(1, 2)
        for clue, accuracy in zip(public_job.clues, (Fraction(4, 5), Fraction(3, 5))):
            likelihood *= accuracy if clue == fault else 1-accuracy
        weights[fault] = likelihood
    chosen_fault = 'filter' if primary == 'replace_filter' else 'sensor'
    return float(1 - weights[chosen_fault] / sum(weights.values()))


@dataclass(frozen=True)
class PublicRiskEstimator:
    name: str
    agreement: AgreementEstimator
    pooled_probability: float
    estimator_hash: str

    def predict(self, public_job, primary, secondary):
        if type(public_job) is not PublicJob or type(primary) is not str or type(secondary) is not str or primary not in ACTIONS or secondary not in ACTIONS:
            raise TypeError('Risk prediction accepts only a public job and two valid sampled actions')
        if self.name == 'frozen':
            return self.agreement.predict(primary, secondary)
        if self.name == 'pooled':
            return self.pooled_probability
        if self.name == 'analytical':
            return analytical_error(public_job, primary)
        raise ValueError('Unknown risk estimate')


def load_risk(name, path):
    if name not in ('frozen', 'pooled', 'analytical') or file_hash(path) != ESTIMATOR_FILE_HASH:
        raise ValueError('Unknown estimate or historical estimator hash mismatch')
    record = json.loads(Path(path).read_text())
    agreement = AgreementEstimator.from_record(record)
    if agreement.estimator_hash != ESTIMATOR_HASH:
        raise ValueError('Historical estimator identity mismatch')
    identity = digest({'name': name, 'historical_estimator': ESTIMATOR_HASH,
                       'clue_accuracies': [0.8, 0.6], 'fault_prior': [0.5, 0.5], 'version': 1})
    return PublicRiskEstimator(name, agreement, record['pooled']['probability'], identity)
