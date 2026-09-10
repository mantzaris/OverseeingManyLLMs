#!/usr/bin/env python3
"""Quantify the documented numerical repair on historical public states only."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from overseeing.io import read_events,write_json,write_csv
from overseeing.domain import ReviewRequest
from overseeing.policies import choose
from overseeing.research_scheduler import ResearchScheduler
rows=[]
for path in sorted(Path('artifacts/stage3_competition/run').rglob('events.jsonl')):
    events=read_events(path);header=events[0]
    for event in events:
        if event['event']!='dispatch_considered':continue
        requests=tuple(ReviewRequest(**r) for r in event['eligible'])
        old=choose('delay',requests,event['tick']);new=ResearchScheduler('delay')(requests,event['tick'])
        rows.append(dict(path=str(path),seed=header['scenario']['seed'],policy=header['policy'],review_ticks=header['review_ticks'],tick=event['tick'],eligible=len(requests),historical_choice=old,stable_sum_choice=new,changed=old!=new))
root=Path('artifacts/stage4_research/offline_risk')
write_csv(root/'search_summation_choices.csv',rows)
result=dict(states=len(rows),changed=sum(r['changed'] for r in rows),changed_s1=sum(r['changed'] and r['review_ticks']==1 for r in rows),changed_s2=sum(r['changed'] and r['review_ticks']==2 for r in rows),meaning='Same saved public states, no new trajectories or inference; historical outputs preserved.')
write_json(root/'search_summation_summary.json',result);print(result)
