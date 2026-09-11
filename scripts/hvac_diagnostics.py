#!/usr/bin/env python3
"""Descriptive evidence tables and a secondary risk-only policy visualization."""
import csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path('artifacts/stage7_empirical');rows=list(csv.DictReader((root/'analysis/diagnoses.csv').open()));out=[]
for label in ('normal','outdoor_damper','heating_valve','cooling_valve'):
    xs=[x for x in rows if x['truth']==label];out.append(dict(truth=label,windows=len(xs),days=len({x['run_id'] for x in xs}),proposal_correct=sum(int(x['initial_correct']) for x in xs),review_correct=sum(int(x['review_correct']) for x in xs),baseline_correct=sum(int(x['baseline_correct']) for x in xs)))
with (root/'analysis/class_diagnostics.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
t=[r'\begin{table*}[t]',r'\caption{Measured-data evaluation by experimentally annotated component category. Counts are windows, nested within experimental days on one unit. Proposed and reviewed labels are generated. The conventional baseline uses development data only.}',r'\centering\small',r'\begin{tabular}{lrrrrr}',r'\toprule',r'Condition & Days & Windows & Proposal correct & Review correct & Baseline correct \\',r'\midrule']
for r in out:t.append(' & '.join([r['truth'].replace('_',' ')]+[str(r[k]) for k in ['days','windows','proposal_correct','review_correct','baseline_correct']])+r' \\')
t += [r'\bottomrule',r'\end{tabular}',r'\end{table*}'];Path('paper/generated/hvac_class_table.tex').write_text('\n'.join(t)+'\n')
harm_wrong=sum(x['harm']=='1' and x['review']!='abstain' for x in rows);harm_abstain=sum(x['harm']=='1' and x['review']=='abstain' for x in rows)
risk=np.array([float(x['risk']) for x in rows]);error=np.array([1-int(x['initial_correct']) for x in rows]);positives=risk[error==1];negatives=risk[error==0]
auc=np.mean([int(p>n)+.5*int(p==n) for p in positives for n in negatives]);pooled=json.loads((root/'estimator.json').read_text())['pooled']['risk']
d=dict(harmful_wrong_labels=harm_wrong,harmful_abstentions=harm_abstain,auc=float(auc),brier_constant_half=float(np.mean((error-.5)**2)),brier_pooled_development=float(np.mean((error-pooled)**2)),interpretation='AUROC uses 35 incorrect versus 19 correct proposals, highly tied risks. Conditional on this single-equipment development split. Counts do not imply independent windows.')
(root/'analysis/extra_diagnostics.json').write_text(json.dumps(d,indent=2)+'\n')
summ=list(csv.DictReader((root/'analysis/policy_summary.csv').open()));pol=['no_review','fcfs','edf','uncertainty','greedy','search'];xs=[next(x for x in summ if x['policy']==p and x['reviewer']=='model_risk' and x['weights']=='heterogeneous' and x['capacity']=='1' and x['duration']=='2') for p in pol]
plt.rcParams.update({'font.size':9,'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False});fig,axes=plt.subplots(1,2,figsize=(6.8,2.8),constrained_layout=True)
colors=['#777777','#0072B2','#E69F00','#009E73','#CC79A7','#D55E00']
for ax,metric,label in [(axes[0],'mean_loss','Modeled loss / experimental day'),(axes[1],'completed_reviews','Completed simulated reviews')]:
    ax.bar(range(6),[float(x[metric]) for x in xs],color=colors);ax.set_xticks(range(6));ax.set_xticklabels(['None','FCFS','EDF','Risk','Greedy','Search'],rotation=30,ha='right');ax.set_ylabel(label)
axes[0].axhline(float(xs[0]['mean_loss']),color='black',linestyle='--',lw=.8);fig.suptitle('Secondary model-review allocation that ignores reviewer harm')
for ext in ('pdf','png'):fig.savefig(root/'figures'/('risk_only_secondary.'+ext),bbox_inches='tight',dpi=300)
print(json.dumps(d))
