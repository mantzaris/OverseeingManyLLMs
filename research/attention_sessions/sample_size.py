"""Planning sensitivity only: no human variance estimates are available."""
import math,csv
from pathlib import Path
out=Path('artifacts/attention_sessions/human_sample_size_sensitivity.csv')
rows=[]
for sd in (.10,.15,.20):
    n=math.ceil((1.95996398454+.84162123357)**2*sd**2/.05**2)
    rows.append(dict(assumed_paired_sd=sd,proposed_quality_margin=.05,normal_approximation_n=n,
                     counterbalanced_n=4*math.ceil(n/4),with_10pct_attrition=4*math.ceil(n/.9/4),
                     status='hypothetical planning, not estimated from participants'))
with out.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print(rows)
