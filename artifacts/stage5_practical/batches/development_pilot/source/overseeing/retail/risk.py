"""Development-only empirical transaction error risk, frozen before scheduling."""
from dataclasses import dataclass
from overseeing.domain import digest


@dataclass(frozen=True)
class RiskFeatures:
    family: str
    uncertain: bool


@dataclass(frozen=True)
class RetailRisk:
    # Tuples rather than a caller-mutable dictionary enforce runtime freezing.
    probabilities: tuple
    pooled: float
    estimator_hash: str

    def predict(self, features):
        if type(features) is not RiskFeatures: raise TypeError('Risk prediction accepts only public features')
        return dict(self.probabilities).get(features.family+':'+str(int(features.uncertain)),self.pooled)

    @classmethod
    def load(cls, record):
        body={k:v for k,v in record.items() if k!='estimator_hash'}
        if digest(body)!=record['estimator_hash']: raise ValueError('Estimator hash mismatch')
        return cls(tuple(sorted((k,v['probability']) for k,v in record['bins'].items())),
                   record['pooled_probability'],record['estimator_hash'])


def fit_development(rows, provenance, minimum=10):
    # All successfully staged jobs are labelled, including unreviewed proposals.
    # Failed workflows cannot be repaired by this reviewer and are reported separately.
    examples=[r for r in rows if r['proposal'] is not None]
    errors=sum(r['initial_error'] for r in examples); pooled=(errors+1)/(len(examples)+2)
    bins={}
    for family in ('cancel','modify','return_exchange'):
        for uncertain in (False,True):
            group=[r for r in examples if r['features']==dict(family=family,uncertain=uncertain)]
            n=len(group);e=sum(r['initial_error'] for r in group)
            bins[family+':'+str(int(uncertain))]=dict(examples=n,errors=e,fallback=n<minimum,
                probability=pooled if n<minimum else (e+1)/(n+2))
    record=dict(method='Laplace-smoothed family x public uncertainty bins',minimum_bin_examples=minimum,
        bins=bins,examples=len(examples),errors=errors,pooled_probability=pooled,
        excluded_unstaged_workflows=len(rows)-len(examples),provenance=provenance,
        label='Proposed transaction yields a database different from annotated target, before review',
        feature='family; uncertain if model confidence is not high or an automatic check previously rejected an action')
    record['estimator_hash']=digest(record);return record
