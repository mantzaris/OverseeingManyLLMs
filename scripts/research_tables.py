#!/usr/bin/env python3
"""Compact Markdown tables from the complete, audited evaluation summaries."""
import argparse,csv
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from overseeing.research_analysis import numeric_records
from overseeing.io import write_csv
import numpy as np


def read(path):
    with Path(path).open(newline='') as handle:return list(csv.DictReader(handle))

def f(value,digits=3):
    if value in ('',None):return '—'
    return ('{:.'+str(digits)+'f}').format(float(value))

def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---' for _ in headers)+' |']+['| '+' | '.join(map(str,r))+' |' for r in rows])+'\n'

def main(root,batch,label):
    root=Path(root);summary=root/'summaries'/label;out=summary/'tables';out.mkdir(exist_ok=True)
    outcomes=read(summary/'policy_outcomes.csv');pairs=read(summary/'paired_comparisons.csv')
    core=[r for r in outcomes if r['workload'] in ('original','competition') and r['risk']=='frozen' and r['closure_penalty']=='0' and r['planned_episodes']=='64']
    (out/'replication.md').write_text(table(['Workload','Review ticks','Policy','Mean loss','Correct / jobs','Corrections','Utilization','Missed opportunities'],[[r['workload'],r['review_ticks'],r['policy'],f(r['mean_loss']),r['correct_jobs']+' / '+r['jobs'],r['corrections'],f(r['review_utilization']),r['missed_opportunities']] for r in core]))
    selected=[r for r in pairs if r['kind']=='policy' and r['workload'] in ('original','competition') and r['risk']=='frozen' and (r['right'].endswith('|greedy|lambda0') or r['right'].endswith('|edf|lambda0')) and r['planned_pairs']=='64']
    (out/'paired_replication.md').write_text(table(['Workload','Ticks','Comparator','Search − comparator','95% paired interval','Search W/T/L','Different review orders'],[[r['workload'],r['review_ticks'],r['right'].split('|')[4],f(r['mean_loss_difference']),'['+f(r['ci_low'])+', '+f(r['ci_high'])+']',r['left_wins']+'/'+r['ties']+'/'+r['left_losses'],r['actual_order_differences']+' / '+r['completed_pairs']] for r in selected]))
    capacity=[r for r in outcomes if r['workload']=='larger' and r['planned_episodes']=='32']
    (out/'capacity.md').write_text(table(['Agents','Ticks','Policy','Mean loss','Loss / job','Incorrect / jobs','Corrections','Utilization'],[[r['agents'],r['review_ticks'],r['policy'],f(r['mean_loss']),f(r['mean_loss_per_job']),r['incorrect_jobs']+' / '+r['jobs'],r['corrections'],f(r['review_utilization'])] for r in capacity]))
    branch=[r for r in outcomes if r['planned_episodes']=='16' and r['policy']=='delay']
    (out/'objective.md').write_text(table(['Workload','Ticks','λ','Mean original loss','Mean incorrect','Mean L+4U','Mean L+8U'],[[r['workload'],r['review_ticks'],r['closure_penalty'],f(r['mean_loss']),f(r['mean_incorrect_jobs']),f(r['mean_common_objective_4']),f(r['mean_common_objective_8'])] for r in branch]))
    risks=read(summary/'risk_matched_outcomes.csv')
    (out/'risk_rollouts.md').write_text(table(['Workload','Ticks','Policy','Risk','Mean loss','Brier on own trajectories'],[[r['workload'],r['review_ticks'],r['policy'],r['risk'],f(r['mean_loss']),f(r['mean_brier'],5)] for r in risks]))
    decisions=numeric_records(root/'batches'/batch/'analysis/decisions.csv');planning=[]
    for size in range(7):
        rows=[r for r in decisions if r['policy']=='delay' and r['eligible_count']==size]
        if rows:planning.append(dict(eligible_requests=size,decisions=len(rows),mean_ms=float(np.mean([r['planning_seconds']*1000 for r in rows])),p95_ms=float(np.percentile([r['planning_seconds']*1000 for r in rows],95)),max_ms=max(r['planning_seconds']*1000 for r in rows),ordered_subsets=min(r['ordered_subsets_evaluated'] for r in rows)))
    write_csv(summary/'search_latency_by_eligible.csv',planning)
    (out/'search_latency.md').write_text(table(['Eligible requests','Decisions','Mean ms','95th percentile ms','Max ms','Ordered subsets'],[[r['eligible_requests'],r['decisions'],f(r['mean_ms']),f(r['p95_ms']),f(r['max_ms']),r['ordered_subsets']] for r in planning]))
    quality=read(summary/'prediction_quality.csv')
    keys=('workload','agents','review_ticks','risk','policy','closure_penalty','study')
    prediction_rows=[]
    for outcome in outcomes:
        group=[r for r in quality if all(r[k]==outcome[k] for k in keys)]
        scores={r['scoring_risk']:r for r in group if r['agreement_bin']=='all'}
        bins={r['agreement_bin']:r for r in group if r['scoring_risk']=='frozen'}
        label='{} {} a{} s{} {} {} λ{}'.format(outcome['study'],outcome['workload'],outcome['agents'],outcome['review_ticks'],outcome['risk'],outcome['policy'],outcome['closure_penalty'])
        prediction_rows.append([label,bins['agree']['errors']+' / '+bins['agree']['examples'],bins['disagree']['errors']+' / '+bins['disagree']['examples'],f(scores['frozen']['observed_error_rate']),*[f(scores[k]['brier'],5) for k in ('frozen','pooled','analytical')]])
    (out/'prediction_diagnostics.md').write_text('Initial-action labels on each saved condition; alternatives score the same outputs. Repeated policy/job rows are not independent scenarios.\n\n'+table(['Condition','Agree errors / n','Disagree errors / n','Initial error rate','Frozen Brier','Pooled Brier','Analytical Brier'],prediction_rows))
    print('Wrote tables to',out)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',default='artifacts/stage4_research');parser.add_argument('--batch',default='evaluation');parser.add_argument('--label',default='evaluation');args=parser.parse_args();main(args.root,args.batch,args.label)
