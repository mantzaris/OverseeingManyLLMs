"""Fixed paired analysis. Bundle, not replay row, is the sampling unit."""
import csv,json,gzip
from pathlib import Path
import numpy as np
from .data import ROOT,save_json
from .evaluate import METRICS,csv_write
from .method import POLICIES

PRIMARY='core_high_1_12_ideal'


def read_rows():
    rows=list(csv.DictReader((ROOT/'evaluation/episodes.csv').open()))
    for r in rows:
        r['bundle']=int(r['bundle'])
        for k in METRICS+('planning_and_controller_seconds',):r[k]=float(r[k])
    return rows


def analyze():
    declaration=json.loads((ROOT/'declaration.json').read_text());rows=read_rows()
    assert len(rows)==declaration['expected_rows']
    lookup={(r['condition_id'],r['bundle'],r['policy']):r for r in rows}
    assert len(lookup)==len(rows)
    for c in declaration['conditions']:
        for b in range(6):assert len({lookup[c['condition_id'],b,p]['input_hash'] for p in POLICIES})==1
    rng=np.random.default_rng(declaration['bootstrap_seed']);indices=rng.integers(0,6,size=(2000,6))
    summaries=[];comparisons=[];individual=[];dominance=[]
    for config in declaration['conditions']:
        cid=config['condition_id'];condition_rows=[]
        for policy in POLICIES:
            group=[lookup[cid,b,policy] for b in range(6)]
            d=dict(condition_id=cid,policy=policy,n_bundles=6)
            for metric in METRICS:
                vals=np.array([r[metric] for r in group]);ci=np.quantile(vals[indices].mean(1),[.025,.975])
                d[metric]=float(vals.mean());d[metric+'_low']=float(ci[0]);d[metric+'_high']=float(ci[1])
            summaries.append(d);condition_rows.append(d)
        for comparator in ('sticky_edf','greedy','edf','density','unguarded','no_review'):
            d=dict(condition_id=cid,comparison='guarded-'+comparator)
            for metric in ('loss','active_time','session_offers','correct','missed_useful','harms'):
                values=np.array([lookup[cid,b,'guarded'][metric]-lookup[cid,b,comparator][metric] for b in range(6)])
                ci=np.quantile(values[indices].mean(1),[.025,.975]);d[metric]=float(values.mean());d[metric+'_low']=float(ci[0]);d[metric+'_high']=float(ci[1])
                if metric=='loss':d.update(wins=int(sum(values<0)),ties=int(sum(values==0)),losses=int(sum(values>0)))
            comparisons.append(d)
            for b in range(6):individual.append(dict(condition_id=cid,comparison='guarded-'+comparator,bundle=b,
                loss_difference=lookup[cid,b,'guarded']['loss']-lookup[cid,b,comparator]['loss'],
                effort_difference=lookup[cid,b,'guarded']['active_time']-lookup[cid,b,comparator]['active_time']))
        for row in condition_rows:
            dominates=[x['policy'] for x in condition_rows if x['policy']!=row['policy'] and x['loss']<=row['loss']+1e-9 and x['active_time']<=row['active_time']+1e-9 and (x['loss']<row['loss']-1e-9 or x['active_time']<row['active_time']-1e-9)]
            dominance.append(dict(condition_id=cid,policy=row['policy'],dominated_by=';'.join(dominates)))
    out=ROOT/'analysis';out.mkdir(exist_ok=True)
    csv_write(out/'policy_summary.csv',summaries);csv_write(out/'paired.csv',comparisons)
    csv_write(out/'bundle_differences.csv',individual);csv_write(out/'dominance.csv',dominance)
    # First qualifying numerical bundle, never maximum effect.
    examples={}
    for cid in (PRIMARY,'core_high_1_12_model_risk'):
        for category,sign in [('favorable',-1),('tied',0),('unfavorable',1)]:
            selected=next((b for b in range(6) if np.sign(lookup[cid,b,'guarded']['loss']-lookup[cid,b,'sticky_edf']['loss'])==sign),None)
            examples[cid+'_'+category]=selected
    save_json(out/'example_selection.json',dict(rule='First numerical bundle of each loss-difference sign, guarded versus sticky EDF, at declared primary timing. Missing categories stay absent.',selected=examples))
    summary=dict(primary=[r for r in comparisons if r['condition_id']==PRIMARY],source_units='18 historical day blocks grouped into six non-overlapping constructed queues, one apparatus',
                 primary_policies=[r for r in summaries if r['condition_id']==PRIMARY],
                 model_zero_reviews=all(r['reviews']==0 for r in rows if r['reviewer']=='model'),
                 all_cases=54,new_inference=0,rows=len(rows),paired_input_hashes_verified=True,
                 controller_seconds=sum(r['planning_and_controller_seconds'] for r in rows),controller_max_ms=1000*max(r['planning_and_controller_seconds'] for r in rows),
                 statistical_scope='Conditional six-bundle bootstrap only; no equipment-population inference or equivalence claim.')
    save_json(out/'summary.json',summary)
    print(json.dumps(dict(rows=len(rows),primary=summary['primary'],model_zero_reviews=summary['model_zero_reviews']),indent=2))

if __name__=='__main__':analyze()
