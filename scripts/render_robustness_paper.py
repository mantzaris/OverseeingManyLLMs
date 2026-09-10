#!/usr/bin/env python3
"""Render paper tables from retained results. No inference, fitting or selection."""
import csv,json
from pathlib import Path
root=Path('artifacts/stage6_robustness');out=Path('paper/generated');out.mkdir(exist_ok=True)
POLICIES=('no_review','fcfs','edf','uncertainty','greedy','search')
NAMES=dict(no_review='No review',fcfs='FCFS',edf='EDF',uncertainty='Uncertainty',greedy='Greedy',search='Search')
VARIANTS=('reference','approve_block','complexity_time')
VN=dict(reference='Correction',approve_block='Approve/block',complexity_time='Complexity time')
def rows(cohort,name):return list(csv.DictReader((root/'analysis'/cohort/(name+'.csv')).open()))
def load(cohort,name):return json.loads((root/'analysis'/cohort/(name+'.json')).read_text())
def n(value):return float(value)
def fmt(value):return '{:.3f}'.format(n(value))
def integer(value):return str(int(n(value)))
def table_start(caption,columns,header,label=None):
    return ['\\begin{table*}[t]','\\caption{'+caption+'}',('\\label{'+label+'}' if label else '')+'\\centering\\small','\\begin{tabular}{'+columns+'}','\\toprule',header+' \\\\','\\midrule']
def table_end():return ['\\bottomrule','\\end{tabular}','\\end{table*}','']
fresh=load('fresh','summary');old=load('post_hoc_stage5','summary');audit=json.loads((root/'verification.json').read_text())
index={(r['variant'],int(r['review_duration']),r['policy']):r for r in rows('fresh','policy_outcomes')}
text=[r'\subsection{Fresh Results}',
 r'All 72 workflow attempts are retained. Fifty-one stage a transaction, 39 are initially correct and 12 stage a wrong valid transaction. Twenty-one do not stage, comprising 18 step-limit failures and three finishes without a transaction. All 675 GPU generations succeed, with no retry. Table~\ref{tab:fresh} gives every policy and condition.',
 r'The primary restricted-authority difference is $+1.667$ loss points for search minus greedy, with a 95\% paired interval of $[0.000,4.667]$. Search wins on zero bundles, ties on six and loses on two. The eight bundle-mean differences in numerical order are $0,0,0,0,0,0,1.333,12.000$. The wide interval reflects a small, sparse sample and does not establish equivalence or a general population disadvantage.',
 r'Search blocks eight wrong transactions versus greedy\textquotesingle s twelve and lets four wrong transactions post. Both complete 39 of 72 tasks because blocking cannot complete a wrong or unstaged request. Search performs 44 reviews versus 42, consuming 88 versus 84 ticks. Its loss is 172 points versus 132, or 7.167 versus 5.500 per three-case run. EDF has mean loss 7.000. The secondary search--EDF difference is $+0.167\;[0.000,0.500]$, with seven bundle ties and one loss.',
]
# ASCII apostrophe is sufficient and avoids a template-dependent command.
text=[s.replace(r'\textquotesingle s',"'s") for s in text]
text+=table_start('Fresh follow-up mean loss. Each cell represents 24 runs on eight source bundles. C and X are correct-task totals at base duration two for correction and complexity time, with denominator 72. Approve/block completes 39 tasks under every policy. No-review inputs are identical across conditions.','lrrrrrrrr',r'& \multicolumn{2}{c}{Correction} & \multicolumn{2}{c}{Approve/block} & \multicolumn{2}{c}{Complexity time} & \multicolumn{2}{c}{Correct} \\ Policy & 1 tick & 2 ticks & 1 tick & 2 ticks & 1 tick & 2 ticks & C & X','tab:fresh')
for p in POLICIES:
    vals=[fmt(index[(v,d,p)]['mean_loss']) for v in VARIANTS for d in (1,2)]
    vals += [integer(index[(v,2,p)]['task_completed']) for v in ('reference','complexity_time')]
    text.append(' & '.join([NAMES[p]]+vals)+r' \\')
text+=table_end()
text += [
 r'At one tick, every review policy prevents every staged error in all three variants. Correction and complexity time reach the 21-unstaged-failure floor of 84 loss points. Blocking instead retains unresolved service loss for all 33 initially unsuccessful requests, totaling 132 points. These distinct floors follow from corrective authority, not from a better scheduling rule.',
 r'At two ticks, full correction gives search minus greedy $+2.333\;[0.000,6.333]$. The complexity variant has the same paired difference while increasing both policies\textquotesingle\ loss by one third of a point. Only six staged proposals from four cases trigger the added tick, including two initially wrong proposals. This limited exposure bounds what the complexity null contrast establishes.',
 r'Approve/block leaves every fresh review sequence unchanged relative to correction. Its smaller search--greedy loss difference is therefore explained by the changed preventable consequence, not an observed improvement in allocation. The benefit functions can produce different rankings in arithmetic cases, but do not do so in these fresh trajectories.',
 r'\begin{figure*}[t]',
 r'\centering\includegraphics[width=0.98\textwidth]{../artifacts/stage6_robustness/analysis/fresh/figures/paired_loss.pdf}',
 r'\caption{Fresh operational sensitivity. Points are search minus greedy mean loss; bars are 95\% paired bundle-bootstrap intervals. Only approve/block at base duration two is primary. Degenerate one-tick intervals describe ties in this sample, not population equivalence.}',
 r'\label{fig:robustness}\end{figure*}',
 r'\subsection{Scheduling Mechanism and Error Ranking}',
 r'Search and greedy review sequences differ in six of 24 fresh runs at base duration two, versus one search--EDF difference. On search\textquotesingle s states, 19 dispatches have multiple eligible requests and six have different greedy/search heads. These are repeated states for descriptive analysis, not additional independent observations.',
 r'The first unfavorable example is bundle 06, replicate 2. At tick zero, search reviews a correct cancellation with cutoff two, planning to preserve both currently available opportunities. Greedy instead blocks the wrong modification by tick two. A correct exchange arrives at tick one. When search becomes free, its frozen estimate prioritizes that exchange, and the modification posts at tick five. Search loss is eight versus greedy\textquotesingle s four. The primary example rule finds no fresh search benefit. The first tie contains a blocked incomplete return and an unstaged modification, giving equal loss eight.',
 r'The frozen estimator\textquotesingle s aggregate Brier score is 0.17144, versus 0.17998 for its pooled estimate; AUROC is 0.6581. Yet modification has eight errors among 13 staged proposals, versus four among 18 returns/exchanges, while predicted risks rank those families in the opposite order. All 20 staged cancellations are correct. This retrospective evidence helps explain the unfavorable trace without granting labels to the scheduler or refitting on evaluation data. Eight source cases produce different proposals across the three replicates, and four have mixed initial correctness.',
 r'\subsection{Saved-Preparation Sensitivity}',
 r'The separate post hoc analysis replays all 1,152 original reference traces exactly and adds the declared variants on the same 288 preparations. At base duration two, restricted-authority search minus greedy is $+0.125\;[-0.167,0.500]$, with one win, 29 ties and two losses. Complexity time gives $+0.500\;[-0.083,1.250]$, with one win, 28 ties and three losses. These results do not replace the original $+0.250$ primary comparison. Blocking changes search\textquotesingle s actual sequence in only two of 96 runs relative to correction. The first saved-data benefit remains available as a trace alongside the fresh null and unfavorable examples.',
]
text=[s.replace(r'\textquotesingle s',"'s").replace(r'\textquotesingle\ ',"' ") for s in text]
(out/'stage6_results.tex').write_text('\n\n'.join(text)+'\n')
# Complete outcome and resource accounting tables belong in the companion.
text=[]
for cohort,label in [('fresh','Fresh cases'),('post_hoc_stage5','Post hoc Stage 5 preparations')]:
    data=rows(cohort,'policy_outcomes')
    text+=table_start(label+'. Absolute outcomes across three generation replicates per bundle. Totals are repeated-condition counts, not independent samples. S and W denote service and wrong-posting loss. B is blocked unresolved requests and U is unstaged failures.','llrrrrrrrrr',r'Condition / base & Policy & Loss & Mean & S & W & Correct & Wrong & B & U & Missed')
    for r in data:
        cond=VN[r['variant']]+' / '+r['review_duration']
        vals=[integer(r['operational_loss']),fmt(r['mean_loss'])]+[integer(r[k]) for k in ('service_failure_loss','wrong_transaction_loss','task_completed','wrong_transactions','blocked_unresolved','unstaged_failures','expired_useful_opportunities')]
        text.append(' & '.join([cond,NAMES[r['policy']]]+vals)+r' \\')
    text+=table_end()
    text+=table_start(label+'. Review resources. Time and waiting are summed abstract ticks. Utilization is mean occupied fraction of the processing horizon. More reviews do not necessarily imply more useful interventions.','llrrrrrr',r'Condition / base & Policy & Reviews & Corrections & Time & Waiting & Utilization & Multi-eligible')
    for r in data:
        vals=[integer(r[k]) for k in ('completed_reviews','corrections','review_busy_ticks','total_waiting_ticks')]+[fmt(r['mean_utilization']),integer(r['multi_eligible_dispatches'])]
        text.append(' & '.join([VN[r['variant']]+' / '+r['review_duration'],NAMES[r['policy']]]+vals)+r' \\')
    text+=table_end()
    text+=table_start(label+'. Search-minus-comparator loss differences. Negative favors search. Intervals resample bundles; W/T/L are scenario-bundle wins, ties and losses. Only the fresh approve/block two-tick search--greedy row is primary.','llrrll',r'Condition & Comparator & Base & Difference & 95\% interval & W/T/L')
    for r in rows(cohort,'paired_comparisons'):
        if r['metric']!='operational_loss' or r['comparison'] not in ('search-greedy','search-edf'):continue
        vals=[VN[r['variant']],r['comparison'].replace('search-',''),r['review_duration'],fmt(r['mean_difference']),'['+fmt(r['ci_low'])+', '+fmt(r['ci_high'])+']','/'.join(r[k] for k in ('wins','ties','losses'))]
        text.append(' & '.join(vals)+r' \\')
    text+=table_end()
text += [r'\begin{figure*}[t]',r'\centering\includegraphics[width=0.98\textwidth]{../artifacts/stage6_robustness/analysis/fresh/figures/primary_bundle_differences.pdf}',r'\caption{All eight fresh primary bundle differences, after averaging three generation replicates. Zero values remain explicit.}',r'\end{figure*}',r'\begin{figure*}[t]',r'\centering\includegraphics[width=0.98\textwidth]{../artifacts/stage6_robustness/analysis/post_hoc_stage5/figures/paired_loss.pdf}',r'\caption{Post hoc saved-preparation sensitivity. The 32 bundles are separate from the eight fresh bundles and are not pooled for inference.}',r'\end{figure*}']
(out/'robustness_tables.tex').write_text('\n'.join(text)+'\n')
text=[r'The fresh follow-up completes 675 ordinary generation calls and 675 attempts, with zero retries, failures or unknown-token records. Requests consume 3,495,749 prompt tokens and 58,762 completion tokens. Summed HTTP generation time is 1,149.669 seconds; the preparation worker spans 1,200.660 seconds. The longest attempt lasts 4.993 seconds. Maximum observed input/output lengths are 11,369/256 tokens, within their declared limits. Server counter deltas agree exactly with the ledger and raw attempts.',
 r'There are no repeated byte-identical request groups within this fresh run. Different seeded replicates yield different proposals on eight of 24 source cases and mixed initial correctness on four. These comparisons involve different generation seeds and often later prompt histories; they do not measure identical-request nondeterminism.',
 r'Across fresh operational conditions, actual search dispatch reaches two eligible requests. Its 114 such decisions examine five ordered subsets and average 0.04832 ms, with maximum 0.11583 ms on the recorded host. Three pending requests can appear in no-review diagnostic states; the exact planner is not truncated. These repeated state measurements are descriptive.',
 r'The stage starts at 21:18:02 UTC on 10 September 2026, with inference cutoff 01:48:02 and hard deadline 03:18:02 the next day. The last generation completes at 21:57:00.893 UTC, well before the reporting reserve. The temporary server and both experimental worker processes are verified absent at 21:59:19 UTC. The original server remains healthy with unchanged counters. No new paid resources are provisioned. Provider allocation duration, price and charge are unavailable, so request time is not converted into billed cost. The final stage and cumulative clocks are reported in the repository report. Across both Stage 1 GPU demonstrations and Stages 2--6, the recorded total is 55,384 generation attempts, including two retries. No timestamp is reset to fit the original 36-hour target.',
 r'The 13,459 historical artifact, configuration and upstream files captured at authorization remain byte-identical. All 72 new GPU workflows, 864 fresh policy traces and 3,456 post hoc traces replay. The latter include 1,152 exact matches to historical retail reference traces. No fresh public evidence requires redaction; historical redaction provenance remains disclosed.']
(out/'stage6_accounting.tex').write_text('\n\n'.join(text)+'\n')
text=[r'\subsection{Fresh Unfavorable and Tied Cases}',
 r'No fresh restricted-authority run gives search lower loss than greedy. The first unfavorable run is bundle 06, replicate 2. Modification case train:466 proposes a wrong available variant. It has arrival zero, cutoff five, processing weight four and predicted error 0.2917. Cancellation case train:356 is correct, with arrival zero, cutoff two, weight twelve and predicted error 0.04. Exchange train:177 arrives at one, is correct, and has cutoff five, weight eight and predicted error 0.4762.',
 r'Search first protects the expiring cancellation, then chooses the exchange at tick two. The modification can no longer finish review after tick four and posts at five. Its service cost four plus posting cost four yields loss eight. Greedy blocks the modification at two, leaving service loss four, then approves the exchange. The unreviewed correct cancellation posts at its cutoff without error. This illustrates how preserving an opportunity under a public expected-value model can fail to preserve an actual error.',
 r'The first tie is bundle 00, replicate 0. Both policies approve the cancellation at two and block an incomplete return proposal at four. The modification has no staged proposal. Both have loss eight, consisting of the unresolved return and the unstaged modification. The first preparation failure is that modification, train:421. It finishes without a mutation; the failure field is null because no runtime exception occurs. This is still an unsuccessful retained workflow.',
 r'\subsection{Saved-Data Benefit and Failure}',
 r'The post hoc cohort contains a first qualifying benefit at bundle 28, replicate 0, with search-minus-greedy loss $-4$. Its first unfavorable case is bundle 09, replicate 0, with difference $+4$, and its first tie is bundle 00, replicate 0. The first unstaged failure is train:062 in bundle 00, replicate 2, which exhausts all 14 tool turns. The complete source intentions, proposed and annotated actions, and tick-by-tick review and posting events are saved in the companion trace files. These examples are selected by first qualification, not effect size.']
(out/'stage6_examples.tex').write_text('\n\n'.join(text)+'\n')
print('Rendered main and supplement tables from Stage 6 saved results.')
