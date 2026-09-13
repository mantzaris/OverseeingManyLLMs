"""Read-only reconciliation of the frozen evidence used in the position paper."""
import gzip
import hashlib
import json
from pathlib import Path
import pandas as pd
from research.oversight_simulation.run import environment, verify_freeze

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / 'artifacts/oversight_simulation'
OUT = ROOT / 'artifacts/icaart_position'


def collect():
    freeze = verify_freeze()
    inputs = json.loads((OLD / 'inputs.json').read_text())
    design = json.loads((OLD / 'design.json').read_text())
    means = pd.read_csv(OLD / 'analysis/cell_means.csv')
    pairs = pd.read_csv(OLD / 'analysis/paired_differences.csv')
    env = environment(inputs)
    reference = means[means.config == '015_o25_high_long'].pivot(index='policy', columns='metric', values='mean')
    counts = {}
    for other in ['Q', 'Q-source-aware', 'Q-sticky']:
        vals = pairs[(pairs.contrast == 'G_minus_' + other) & (pairs.metric == 'correct')]['mean']
        counts[other] = dict(positive=int((vals > 1e-10).sum()), tied=int((abs(vals) <= 1e-10).sum()), negative=int((vals < -1e-10).sum()))
    assert counts['Q'] == dict(positive=24, tied=2, negative=40)
    assert counts['Q-source-aware'] == dict(positive=0, tied=4, negative=62)
    batch = json.loads((OLD / 'batch.json').read_text())
    assert batch['complete'] and batch['simulations'] == 31680
    assert len(inputs['items']) == 36 and len(inputs['sources']) == 6
    assert sum(env.initial_correct.values()) == 7
    assert sum(not x['output']['answer'] for x in inputs['items'].values()) == 5
    # All reported means are independently re-aggregated from saved runs. No simulation rerun.
    with gzip.open(OLD / 'results.jsonl.gz', 'rt') as f:
        raw = pd.DataFrame(json.loads(line) for line in f)
    for metric in ['correct', 'incorrect', 'unfinished']:
        actual = raw.groupby(['config', 'policy'])[metric].mean()
        saved = means[means.metric == metric].set_index(['config', 'policy'])['mean']
        assert (abs(actual - saved) < 1e-10).all()
    interval_checks = 0
    for metric in ['correct', 'incorrect', 'unfinished']:
        blocks = raw.groupby(['config', 'seed', 'policy'])[metric].mean().unstack('policy')
        for contrast in pairs.contrast.unique():
            lhs, rhs = contrast.split('_minus_')
            delta = blocks[lhs] - blocks[rhs]
            stats = delta.groupby('config').agg(['mean', 'std', 'count'])
            se = stats['std'] / stats['count']**0.5
            saved = pairs[(pairs.metric == metric) & (pairs.contrast == contrast)].set_index('config')
            for key, values in [('mean', stats['mean']), ('mc_se', se), ('mc_low', stats['mean']-1.96*se), ('mc_high', stats['mean']+1.96*se)]:
                assert (abs(values-saved[key]) < 1e-10).all(), (metric,contrast,key)
                interval_checks += len(values)
    assert ((raw.correct + raw.incorrect + raw.unfinished) == raw.offered).all()
    for key, group in raw.groupby('config'):
        assert len(group) == 480
    workflow = json.loads((ROOT / 'artifacts/oversight_workflow/tables/answer_summary.json').read_text())
    scenarios = pd.read_csv(ROOT / 'artifacts/oversight_workflow/tables/scenarios.csv')
    result = dict(record_kind='publication_evidence_audit', human_observations=0,
        paired_statistic_checks=interval_checks, simulations=len(raw), settings=len(design['configs']), seeds=len(design['seeds']), rotations=len(design['rotations']),
        input_questions=len(inputs['items']), input_sources=len(inputs['sources']), initial_joint_correct=sum(env.initial_correct.values()),
        empty_fields=sum(not x['output']['answer'] for x in inputs['items'].values()),
        setting_sign_counts=counts, reference=reference.to_dict(orient='index'),
        reference_contrasts=pairs[(pairs.config == '015_o25_high_long') & (pairs.metric == 'correct')].to_dict(orient='records'),
        historical_answers=workflow,
        workflow_scenarios=len(scenarios), workflow_events=int(scenarios.events.sum()),
        active_checks=int(scenarios.stable_checks.sum()), active_failures=int(scenarios.stability_failures.sum()),
        reconciliation='Frozen reviewer.py computes orientation AFTER grouping overhead, not at selection as the historical REPORT.md says. Figures and this paper describe executed code. Historical results and report are preserved.',
        sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [OLD/'inputs.json', OLD/'design.json', OLD/'results.jsonl.gz', OLD/'analysis/cell_means.csv', OLD/'analysis/paired_differences.csv']})
    (OUT / 'claims.json').write_text(json.dumps(result, indent=2) + '\n')
    return result

if __name__ == '__main__':
    r = collect()
    print(json.dumps({k:r[k] for k in ['simulations','settings','initial_joint_correct','empty_fields','setting_sign_counts','workflow_events','active_checks']}))
