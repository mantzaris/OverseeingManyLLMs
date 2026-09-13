"""Conditional Monte Carlo analysis; never participant data or population inference."""
import json,gzip,math
from pathlib import Path
import numpy as np
import pandas as pd
from research.oversight_workflow.common import read,write
from .inputs import OUT

METRICS=['correct','incorrect','unfinished','released','never_selected','unstarted','deferred','blocked','approved_unreleased','review_attempts','repairs','damage','carryover_harms','mean_wait','unrelated_wait_sum','source_switches','source_returns','groups','time_orientation','time_question','time_verification','time_construction','time_interaction','time_release','time_grouping','time_idle']


def run_analysis():
    design=read(OUT/'design.json')
    rows=pd.read_json(OUT/'results.jsonl.gz',lines=True)
    assert set(rows.record_kind)=={'computational_simulation'}
    assert not rows.simulation_run_id.duplicated().any()
    assert (rows.correct+rows.incorrect+rows.unfinished==rows.offered).all()
    expected=len(design['configs'])*len(design['seeds'])*len(design['rotations'])*len(design['policies'])
    assert len(rows)==expected,'Incomplete batch; preserve partial files and declared rows, do not silently analyze a complete matrix'
    configs=pd.DataFrame(design['configs']).set_index('id')
    summaries=[];pairs=[];seed_pairs=[]
    for cid,cell in rows.groupby('config',sort=False):
        for policy,sub in cell.groupby('policy',sort=False):
            seedmeans=sub.groupby('seed')[METRICS].mean()
            for metric in METRICS:
                x=seedmeans[metric].to_numpy();mean=float(x.mean());se=float(x.std(ddof=1)/math.sqrt(len(x)))
                summaries.append(dict(record_kind='computational_simulation',config=cid,family=configs.loc[cid,'family'],policy=policy,metric=metric,mean=mean,mc_se=se,mc_low=mean-1.96*se,mc_high=mean+1.96*se,seeds=len(x),rotations=3))
        for a,b in [('G','Q'),('G','Q-source-aware'),('G','Q-sticky'),('G','M'),('Q','M'),('Q-source-aware','Q'),('Q-sticky','Q')]:
            av=cell[cell.policy==a].set_index(['seed','rotation'])[METRICS];bv=cell[cell.policy==b].set_index(['seed','rotation'])[METRICS]
            delta=av-bv;d=delta.groupby('seed').mean()
            for seed,row in d.iterrows():seed_pairs.append(dict(record_kind='computational_simulation',config=cid,seed=int(seed),contrast=a+'_minus_'+b,**row.to_dict()))
            for metric in METRICS:
                x=d[metric].to_numpy();mean=float(x.mean());se=float(x.std(ddof=1)/math.sqrt(len(x)))
                raw=delta[metric].to_numpy()
                pairs.append(dict(record_kind='computational_simulation',config=cid,family=configs.loc[cid,'family'],contrast=a+'_minus_'+b,metric=metric,mean=mean,mc_se=se,mc_low=mean-1.96*se,mc_high=mean+1.96*se,seed_positive=int((x>1e-9).sum()),seed_ties=int((abs(x)<=1e-9).sum()),seed_negative=int((x< -1e-9).sum()),raw_positive=int((raw>1e-9).sum()),raw_ties=int((abs(raw)<=1e-9).sum()),raw_negative=int((raw< -1e-9).sum()),seeds=len(x)))
    dest=OUT/'analysis';dest.mkdir(exist_ok=True)
    pd.DataFrame(summaries).to_csv(dest/'cell_means.csv',index=False)
    paired=pd.DataFrame(pairs);paired.to_csv(dest/'paired_differences.csv',index=False)
    pd.DataFrame(seed_pairs).to_csv(dest/'paired_seed_blocks.csv.gz',index=False,compression='gzip')
    # Freeze rule: first config, then rotation, then seed, independent of magnitude.
    selected={}
    for cfg in design['configs']:
        cell=rows[rows.config==cfg['id']]
        for rotation in design['rotations']:
            for seed in design['seeds']:
                rs=cell[(cell.rotation==rotation)&(cell.seed==seed)].set_index('policy')
                diff=int(rs.loc['G','correct']-rs.loc['Q','correct']);label='beneficial' if diff>0 else 'unfavorable' if diff<0 else 'tie'
                if label not in selected:selected[label]=dict(config=cfg['id'],rotation=rotation,seed=seed,G_minus_Q_correct=diff,rule='First declaration-order config, then rotation, then seed; not largest effect')
    selected_traces=[]
    wanted={(x['config'],x['rotation'],x['seed']) for x in selected.values()}
    with gzip.open(OUT/'traces.jsonl.gz','rt') as f:
        for line in f:
            t=json.loads(line)
            if (t['config'],t['rotation'],t['seed']) in wanted and t['policy'] in ('Q','G','Q-source-aware','Q-sticky','M'):selected_traces.append(t)
    write(dest/'example_selection.json',selected)
    with gzip.open(dest/'example_traces.json.gz','wt') as f:json.dump(selected_traces,f,separators=(',',':'))
    zero=[c['id'] for c in design['configs'] if c['group_seconds']==0]
    zero_rows=paired[(paired.config.isin(zero))&(paired.contrast=='G_minus_Q-source-aware')]
    outcome_metrics=['correct','incorrect','unfinished','time_orientation','time_verification','time_construction']
    assert (abs(zero_rows[zero_rows.metric.isin(outcome_metrics)]['mean'])<1e-9).all(),'Zero-cost navigation identity failed'
    summary=dict(record_kind='computational_simulation',simulations=len(rows),configurations=len(design['configs']),source_contexts=6,questions=36,monte_carlo_seeds=32,human_observations=0,selected_examples=selected,
                 uncertainty='Monte Carlo numerical uncertainty conditional on unvalidated parameters and reused inputs; not human population uncertainty',zero_group_cost_identity='Verified in declared zero-overhead cells')
    write(dest/'summary.json',summary)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':run_analysis()
