"""Generate the result table and concise research note from completed saved evidence."""
from pathlib import Path
import pandas as pd
from .common import ART,ROOT,read,write
from .plot import LABEL

def pct(x):return f'{100*x:.1f}'
def elapsed(s):return f'{int(s)//3600}h {int(s)%3600//60}m {int(s)%60}s'
def generate():
 r=read(ART/'analysis/results.json');assert not r['missing'],'Complete the declared matrix before writing the final report'
 m=read(ART/'frozen/manifest.json');mech=read(ART/'analysis/mechanisms.json');ledger=read(ART/'resource_ledger.json');contract_audit=read(ART/'analysis/contract_audit.json');replay=read(ART/'replay_evaluation.json');aud=read(ART/'integrity_audit.json');s={x['method']:x for x in r['summary'] if x['budget']==2 and x['method'] in m['methods']};c={(x['first'],x['second'],x['budget']):x for x in r['comparisons']};primary=c['adaptive','fixed_audit',2];practical=c['adaptive','individual_risk',2];transfer=c['source_rule','reattempt',2];a=s['adaptive'];fixed=s['fixed_audit'];best=max(s,key=lambda k:(s[k]['accuracy'],-s[k]['calls']));t=pd.read_csv(ART/'analysis/transfers.csv');d=pd.read_csv(ART/'analysis/disagreement.csv');u=pd.read_csv(ART/'analysis/audits.csv');feedback=pd.read_csv(ART/'analysis/feedback.csv');z=t[(t.method=='adaptive')&(t.step<=2)];changes=d[(d['first']=='adaptive')&(d['second']=='fixed_audit')];frozen=c.get(('adaptive','frozen_model',2));b3=c.get(('adaptive','fixed_audit',3))
 def comparison(x):return f"{100*x['mean']:+.2f} percentage points, 95% paired interval [{100*x['low']:.2f}, {100*x['high']:.2f}], wins/ties/losses {x['wins']}/{x['ties']}/{x['losses']} across {x['n']} contexts"
 table='| Policy | Official EM | F1 | Answer + exact scale | Whole contexts correct / 48 | Never-inspected fixed / harmed | Recipient calls | Unfinished |\n|---|---:|---:|---:|---:|---:|---:|---:|\n'
 for k in m['methods']:
  x=s[k];table+=f"| {LABEL[k]} | {x['em']:.0f}/{x['answers']} ({pct(x['accuracy'])}%) | {100*x['f1']/x['answers']:.1f}% | {x['joint']}/{x['answers']} | {x['project_correct']} | {x['sibling_fixed']}/{x['sibling_damaged']} | {x['calls']} | {x['unfinished']} |\n"
 conclusion=('The adaptive method has a positive primary paired interval in this bounded study.' if primary['low']>0 else 'Adaptive acquisition reduced correctness relative to fixed acquisition under the declared primary comparison.' if primary['high']<0 else 'This study does not establish a correctness advantage for adaptive acquisition over fixed acquisition with the same transfer mechanism.')
 practical_conclusion=('It also improves on risk-only individual inspection in the declared practical comparison.' if practical['low']>0 else 'Risk-only individual correction achieved higher correctness with no recipient-regeneration cost under the declared practical comparison.' if practical['high']<0 else 'A practical improvement over risk-only individual correction is not established.')
 q=feedback[feedback.method=='adaptive'];wrong=q[q.donor_current_correct==0];learn=u[(u.method=='adaptive')&(u.step==2)]
 report=f'''# Adaptive acquisition and reuse of verified corrections

{conclusion} {practical_conclusion} The highest observed two-inspection EM is {LABEL[best]} at {pct(s[best]['accuracy'])}%. These observations do not establish equivalence between methods.

## What was implemented

A bounded controller chooses an answer to inspect, obtains only its answer/scale/derivation annotation, and selectively regenerates related answers. It estimates initial error, beneficial repair and harmful repair separately. A later inspection may reveal a previous recipient's before/after correctness and update those transition estimates. Uninspected private labels never become rewards. This is a harm-aware Bayesian heuristic with a five-percent randomized acquisition component, not a new bandit algorithm or an optimal policy.

The Decision desk replays current answers, source evidence, the proposed inspection, purchased feedback, uncertain recipient eligibility, actual generated repairs and the remaining budget. It withholds future disclosures and uninspected correctness. Users can demonstrate an inspection and see its consequences; arbitrary new human corrections were not evaluated. All interaction logs are scripted software demonstrations.

## Data, feasibility and freeze

TAT-QA supplies real financial-report tables/prose and human-written benchmark questions. Agent assignments, source-context episodes and unit-cost inspections are constructed. The experiment uses ideal annotation supervision and fallible Qwen-generated repairs, not measured human review. The public source revision is `870accc41953dcde885aabeb963d94aabdc0fbc3`, dataset CC BY 4.0 and code MIT.

Twelve source-order train contexts were development-only. All four answer-interface versions are retained. The final pilot obtained 20/72 initial EM. Among 60 transfer trials, nine helped and six harmed accepted sibling answers; matched reattempts helped seven and harmed three. Four additional reused development contexts exercised sequential acquisition. No further method revision followed that smoke pilot.

The protocol was committed at `18dbae40` before held-out inference. Evaluation contains **24 new source contexts, 144 distinct questions, two generation replicas and 288 common initial answers**. Seven core policies produce 336 paired runs at two inspections, with budget-zero/one prefixes. Twelve contexts at replica zero add the frozen-parameter diagnostic; eight add third-inspection adaptive/fixed comparisons, for **364 completed traces**. No case was replaced. Selection followed released test_gold order, exact duplicate exclusions, source size and a 1200-token public-prompt cap. No selection used model outcomes.

The released data lack reliable report identifiers. Contexts are the paired units, but different contexts may originate from one report. Consequently 24 contexts do not imply 24 independent companies or reports. One long paragraph is shared by two evaluation contexts, producing 23 exact-text components. A separately labeled post hoc component-bootstrap sensitivity is saved in `analysis/overlap_sensitivity.csv`; these components still do not identify all shared reports. Repeated generations and policy runs are not independent observations. Public benchmark exposure during model training cannot be excluded.

## Primary outcomes at two inspections

{table}

Each method uses 96 ideal inspections across 48 context/replica episodes. Inspected outputs are replaced directly, so their correctness is not evidence of model repair. The table's sibling counts compare final **never-directly-inspected** answers with their original states. They differ from event counts, which may count a repeatedly regenerated answer more than once. Official EM/F1 and separate exact-scale/joint scores follow the released evaluator.

- **Primary, adaptive minus fixed acquisition:** {comparison(primary)}.
- **Practical, adaptive minus risk-only individual:** {comparison(practical)}.
- **Correction versus extra generation, source rule minus reattempt:** {comparison(transfer)}.

Intervals use 2000 paired context bootstrap resamples with seed 91844 after averaging replicas within context. They are descriptive for this small sample and are not multiplicity-adjusted. No noninferiority margin was declared, so an interval crossing zero cannot establish preserved quality or equivalence. All prespecified comparisons are in `analysis/comparisons.csv`.

## What explains the outcomes

Initial answers achieved {mech['initial_em']:.0f}/{mech['initial_answers']} official EM and {mech['initial_joint']}/{mech['initial_answers']} joint answer/scale correctness. There were {mech['initial_unfinished']} unfinished initial answers. Only {mech['initial_with_usable_evidence']} had usable generated evidence IDs, and {mech['initial_requested_fields_present']} supplied all requested output fields. The format guard validates answer shape, scale and explicit arithmetic; it does not require complete evidence or certify that a citation supports the answer. Individual financial QA competence and evidence localization remain substantial bottlenecks; these are not coordination failures.

Adaptive transfer produced **{int(z['help'].sum())} helpful and {int(z.harm.sum())} harmful regeneration events** in {len(z)} attempts at the primary budget. Its final never-inspected answers included **{a['sibling_fixed']} additional correct answers and {a['sibling_damaged']} newly wrong answers**, or {a['sibling_fixed']/a['inspections']:.3f} additional sibling fixes per inspection before subtracting harm. {len(wrong)} of its inspections found a currently incorrect answer; {int(wrong.reused.sum())} of those actual corrections were reused. Confirmations of already correct answers are counted separately in `analysis/feedback.csv`.

Adaptive and fixed acquisition selected different inspection sequences in {int(changes.different.sum())}/{len(changes)} matched episodes. Thus this is not an experiment where the policies are identical by construction. However a different action is not itself a benefit. By the second inspection, {int((learn.transfer_updates>0).sum())}/{len(learn)} adaptive episodes had acquired at least one label for an earlier transfer. Such feedback can affect second-step recipients; only the third-inspection diagnostic can let it influence a subsequent acquisition.

A telescoping score accounting clarifies the primary gap. Adaptive corrected {a['local_gain']:.0f} currently wrong inspected answers, versus {fixed['local_gain']:.0f} for fixed acquisition. Their regeneration events contributed net -8 and -10 correct answers, respectively. Starting from the same 92 correct answers, this gives 156 versus 162. Thus the observed gap reflects weaker local inspection gains despite slightly less net regeneration damage; fresh-generation variation remains part of the comparison.

The frozen-parameter diagnostic gave {comparison(frozen) if frozen else 'no completed contrast'}. The three-inspection adaptive-minus-fixed diagnostic gave {comparison(b3) if b3 else 'no completed contrast'}. These use the smaller prespecified subsets and are secondary. Disabling parameter updates changed no inspection or recipient membership in the twelve diagnostic episodes. One recipient execution order changed, without changing official correctness. The action changes in the main comparison therefore should not be credited to demonstrated parameter-learning benefits. The third-inspection result is unfavorable rather than a rescue for the primary finding.

There were {mech['duplicate_request_groups']} groups of genuinely identical full model requests, of which {mech['varying_answer_scale_groups']} returned different answer/scale pairs. Of those identical-request groups, {mech['varying_em_groups']} also varied in official correctness. Seeds did not provide bitwise reproducibility. Changed feedback/history prompts are excluded from this count. Each primary policy received actual continuations, and all variation was retained. Sampling variability can contribute to differences even when a policy's decisions coincide.

The transition predictor uses only 60 development transfer trials, with sparse relation bins and selected feedback. Its probabilities are not calibrated. Applicability and successful repair conditional on applicability cannot be separately identified from these labels. Correctness gains cannot automatically be attributed to a shared root cause rather than better attention to the source or another generation. The matched reattempt comparison is essential for this reason.

## Synthetic boundaries and qualitative evidence

Eight authored mechanisms each use 32 fixed seeds, four distinct arithmetic tasks and six methods, producing 1536 zero-inference episodes. They include independent and correlated errors, scale-sensitive amounts, scale-invariant ratios, partial applicability, misleading similarity, an incorrect inferred diagnosis, and ineffective transfer. The final development initialization is reused without synthetic tuning. These cases demonstrate both helpful and harmful regimes; they do not estimate their prevalence in real work or rescue an unfavorable empirical comparison.

`analysis/examples.json` selects the first helpful, score-tied and harmful transfer in frozen source order, followed by replica, step and recipient order. Adaptive is used first, with context memory only if a category is absent. Paired examples similarly use the first positive, tied and negative adaptive-minus-fixed context. Figures display the actual source questions, disclosed answer, generated before/after answer and privately evaluated outcome. No magnitude-based example selection is used.

## Closest prior mechanism and supported claims

Agent Gym already implements scoped correction rules and collateral-match handling. One Human, N Agents studies how correlated audit feedback informs error beliefs. MACE adapts peer interactions using ground-truth quality rewards, while ExpeL retrieves reusable experiential feedback. Our protocol combines acquired-question feedback with fallible sibling regeneration and permits transfer learning only when a recipient label is purchased. It extends those mechanisms at the feedback boundary; generic auditing, memory, Bayesian acquisition and correction reuse are not claimed as new.

| Claim | Evidence | Limit |
|---|---|---|
| A correction can change a distinct sibling answer, positively or negatively | `analysis/transfers.csv`, raw continuations, first-qualifying examples | Does not certify a common root cause |
| The online controller learns only from inspected questions | `integrity_audit.json`, replay with `RecordedInspector`, hidden-label mutation tests | Represented context and registered history only |
| Adaptive and fixed policies make nonidentical decisions | `analysis/disagreement.csv` | Difference is not superiority |
| Held-out correctness and costs can be compared fairly | Frozen declaration, common initial outputs, fixed-disclosure and matched-recipient audits | Ideal feedback, one model, context-level dependence |
| Human workload or multi-agent architectural superiority | Not measured | No participants or single-agent architecture comparison |

**Recommendation:** {conclusion} {practical_conclusion} Retain the protocol as a reproducible audit-and-transfer baseline. Do not make adaptive correction transfer the central methodological claim without a supported gain over the strongest simple comparator. The next useful experiment is to establish reliable recipient applicability and individual answer competence, with matched correction-versus-reattempt trials, before adding more acquisition complexity. A single orchestrator could run the same protocol; this experiment does not establish that splitting answer generation into agent roles adds value.

## Failures, verification and resources

Every declared trace completed. Failed and malformed generations remain in the main accounting, and malformed repairs retain the previous answer. The reporting implementation initially requested `scale_exact` from a wrapper that exposes `scale`; it raised before writing tables. `results.py` fixes only that reporting lookup. The frozen original and `analysis_implementation_note.json` preserve the defect. No controller, estimator or source selection changed after freeze. A separate reporting audit found {contract_audit['initial_schema_invalid_credited']} initial answers with invalid auxiliary/scale-schema fields that still received official answer credit. The frozen statement that malformed outputs score zero was too broad: the implemented metric scores the extracted answer even when another field is invalid. Primary recorded scores and online updates are preserved. `analysis/contract_sensitivity.csv` and `contract_comparisons.csv` additionally zero schema-invalid outputs; this post hoc rescore does not claim those stricter labels drove the saved trajectories.

Replay verified {replay['traces']} complete evaluation traces and {replay['unique_reconstructed_requests']} unique actual prompts without loading private sibling annotations. Integrity checks verified {aud['paired_source_replicas']} complete matched context/replica blocks. Sixteen focused protocol/UI tests, 51 relevant historical tests, and nine browser workflow checks passed. Replay median was {replay['median_trace_replay_ms']:.2f} ms per trace and p95 {replay['p95_trace_replay_ms']:.2f} ms, including saved-request reads, parsing and scoring of purchased feedback; this is not pure planner latency.

At this ledger checkpoint the stage used {ledger['scheduled_calls']} scheduled calls, {ledger['attempts']} attempt intents, {ledger['returned_attempts']} returned GPU generations, {ledger['failed_attempts']} failed transport attempts and {ledger['retries']} retries. Statuses: `{ledger['call_statuses']}`. Eight returned responses were unparseable JSON; these are separate from transport failures. Tokens: {ledger['prompt_tokens']} input and {ledger['completion_tokens']} output. Development, failed preflight checks, primary evaluation and diagnostics are all included. Final resource closure is recorded in `resource_ledger.json`.

Stage elapsed: {elapsed(ledger['stage_elapsed_seconds'])}. Cumulative wall since the original start, including gaps: {elapsed(ledger['cumulative_wall_seconds'])}; overrun beyond the original 36-hour target: {elapsed(ledger['original_36h_overrun_seconds'])}. This stage has separate explicit authorization and is not backdated into the original budget. Existing Qwen2.5-7B BF16 RTX6000Ada service was reused without CPU offloading. No paid resources, human participants or outbound messages were added.

## Reproduce and demonstrate

```bash
bash research/adaptive_correction_transfer/reproduce.sh
bash paper/adaptive_correction_transfer/build.sh
python3 -m research.adaptive_correction_transfer.prototype.server --port 9034
```

The first command reconstructs saved evidence without inference. The last starts the local replay desk at http://127.0.0.1:9034/. See README.md for the collection provenance, official data download, API and exact GPU configuration. Scientific figures are generated from CSV tables as PDF, SVG and PNG. The separate illustrated note is `paper/adaptive_correction_transfer/main.pdf`; historical manuscript sources remain unchanged.
'''
 (ROOT/'research/adaptive_correction_transfer/REPORT.md').write_text(report)
 # Short illustrated note, deliberately not a replacement submission.
 def tex(x):
  return str(x).replace('\\','\\textbackslash{}').replace('&','\\&').replace('%','\\%').replace('_','\\_').replace('#','\\#')
 rows='\n'.join(f"{tex(LABEL[k])} & {s[k]['em']:.0f}/288 & {s[k]['sibling_fixed']}/{s[k]['sibling_damaged']} & {s[k]['calls']} \\\\" for k in m['methods'])
 note=r'''\documentclass[10pt]{article}
\usepackage[margin=0.85in]{geometry}\usepackage[T1]{fontenc}\usepackage{lmodern,graphicx,booktabs,amsmath,xcolor,url}\usepackage[colorlinks=true,allcolors=blue]{hyperref}
\title{Acquiring Corrections Without Free Sibling Labels\\\large A bounded audit-and-transfer experiment on financial question answering}
\author{OverseeingManyLLMs research prototype}\date{12 September 2026}
\begin{document}\maketitle
\begin{abstract}
A correction obtained for one answer may help related work, but it may also damage an answer that was already correct. We implement a sequential protocol that chooses an answer to inspect, discloses only that question's annotation, and selectively regenerates related answers. Transfer outcomes become available to the learner only if their recipient is subsequently inspected. A frozen comparison uses 24 previously uninspected TAT-QA source contexts, 144 human-written questions, and two generated replicas. At two inspections, adaptive acquisition minus fixed acquisition changed official exact match by PRIMARY. The method produced HELP helpful and HARM harmful regeneration events. CONCLUSION This result distinguishes a functioning feedback protocol from a demonstrated algorithmic advance.
\end{abstract}
\section{Question and protocol}
Users supervising several outputs may be able to reuse one correction, but shared source material does not establish shared error. Budgeted audit allocation and information acquisition are established ideas \cite{fleet,knowledge}. Agent Gym already provides scoped correction rules and collateral-match handling \cite{gym}. ExpeL retrieves reusable feedback \cite{expel}, while MACE adaptively selects peer interactions using quality rewards \cite{mace}. The present distinction is the feedback boundary. An uninspected recipient's private score cannot become an online reward.

For each question, the public state contains the source, generated answer and scale, inferred evidence references and acquired correction history. An inspection discloses only that question's answer, scale and derivation and directly replaces its answer. This is ideal annotation supervision. Siblings receive fallible generated continuations. A subsequent inspection may score that recipient's saved before/after states and update the model.

Let $e_j$ estimate error and let $f_r,h_r$ estimate repair and harm for an inferred relation. The recipient gain is
\[g(j,r)=e_j f_r-(1-e_j)h_r-0.01.\]
The last term is an assumed machine-cost preference. Acquisition ranks estimated local gain plus up to three positive recipient gains. Five-percent randomized selection is logged. Beta-smoothed development estimates initialize each episode; only purchased labels update them. Applicability and successful repair are not separately identifiable. This is an interpretable heuristic, without calibrated-confidence or regret guarantees.

At two inspections, the first disclosure can alter the next acquisition through error and co-error beliefs. A transition label acquired at the second inspection can affect its subsequent recipient choices, but not retrospectively select that inspection. A smaller three-inspection diagnostic tests a later acquisition. The format guard retains a previous answer when regeneration is malformed; it does not reject a valid wrong answer using private truth.

\section{Source, design and outcomes}
TAT-QA provides real report tables/prose and human-written benchmark questions \cite{tatqa}. Agent assignments, inspection episodes and supervision costs are constructed. We retain original question wording, disclose no sibling annotations and evaluate with the official EM/F1 code. Twelve training contexts support development. The final development pilot had 20/72 exact matches; 60 sibling transfers repaired nine errors and damaged six correct answers, compared with seven repairs and three harms from matched reattempts.

The held-out declaration was committed before generation. It fixes 24 public test-gold contexts, two replicas, seven methods and two inspections, plus small parameter-update and three-inspection diagnostics. Initial outputs are shared, while changed prompts receive actual GPU continuations. Seeds do not guarantee identical answers. Official scoring credits extracted answers, including CONTRACTCOUNT initial answers with invalid auxiliary or scale-schema fields. A separately labeled strict-schema rescore retains this ambiguity without changing the recorded online updates. The 24 source contexts are paired units; missing report identifiers prevent stronger report-level independence claims. No source was replaced after failure.

\begin{table}[ht]\centering\small
\begin{tabular}{lrrr}\toprule Method & Official EM & Sibling fixed/harmed & Recipient calls\\\midrule
ROWS
\bottomrule\end{tabular}
\caption{Two ideal inspections per context/replica, 288 answers per method. Sibling counts compare final never-inspected answers with their initial states. Inspected answers are replaced directly, and their correctness is not model repair.}\end{table}

The primary adaptive-minus-fixed comparison is PRIMARY, with wins/ties/losses WTL. The practical comparison against risk-only individual inspection is PRACTICAL. Context-paired intervals use 2000 bootstrap resamples after averaging replicas. No noninferiority or equivalence claim follows from a wide interval containing zero. Additional comparisons are secondary.

\begin{figure}[ht]\centering\includegraphics[width=\linewidth]{../../artifacts/adaptive_correction_transfer/figures/quality_cost.pdf}
\caption{Generated answers and ideal annotation feedback on held-out financial contexts. Bands are descriptive context-bootstrap intervals. Machine generations are distinct from human effort. Full policy tables accompany the figure.}\end{figure}

\section{Transfer, adaptation and alternatives}
Adaptive and fixed acquisition chose different inspection sequences in DISAGREEMENT episodes. The source-rule versus reattempt contrast is RETRY. This comparison keeps inspected questions, feedback format, recipient sets and sampling settings matched. It tests correction information beyond the value of an extra generation. Actual identical requests also varied in VARIATION request groups, so action differences and generation variability must be distinguished.

\begin{figure}[ht]\centering\includegraphics[width=\linewidth]{../../artifacts/adaptive_correction_transfer/figures/transfer_and_harm.pdf}
\caption{Helpful and harmful generated changes are retained. Final never-inspected output counts and repeated regeneration-event counts are different quantities. Private labels are used only for this offline analysis.}\end{figure}

The final adaptive outputs contain FINALHELP newly correct and FINALHARM newly wrong never-inspected answers. Sparse development relations and limited generated evidence localization constrain recipient selection. Fixed acquisition corrected 80 currently wrong inspected answers, versus 72 for adaptive acquisition. Regeneration had net effects of -10 and -8, respectively, accounting for the final six-answer difference. Disabling parameter updates changed no inspections, recipient membership or correctness in twelve diagnostic episodes; one recipient execution order changed. At three inspections, adaptive minus fixed EM was -8.33 percentage points, with a descriptive paired interval [-14.58, -2.08] across eight contexts. The same source can support a monetary amount and a scale-invariant ratio, so copying a scale or inferred explanation may be inappropriate. A verified answer alone need not reveal an error's root cause.

\begin{figure}[ht]\centering\includegraphics[width=\linewidth]{../../artifacts/adaptive_correction_transfer/figures/paired_sources.pdf}
\caption{Each bar is a source-context mean across two generated replicas. Positive values favor the first policy. Neither agent roles nor repeated policy runs increase the number of source units.}\end{figure}

Eight synthetic mechanisms use 32 fixed seeds each and scripted response processes. They retain independent errors, correlated errors, misleading similarity, partial applicability, scale exceptions and ineffective repairs. Helpful and unfavorable regimes are both present. These fixtures establish protocol boundaries, not natural prevalence or a rescue for the empirical comparison.

\section{Practical system and conclusion}
The local Decision desk shows the next inspection, shared evidence, the question-specific disclosure, inferred recipients and their actual before/after outputs. Future feedback and uninspected correctness remain hidden. Replay reconstructs all 364 completed traces using only recorded disclosures. Sixteen focused tests, 51 historical checks and nine browser checks validate the implementation boundary. Scripted interaction logs are not participant observations.

CONCLUSION PRACTICALCONCLUSION The supported contribution is an executable acquisition-and-transfer protocol and a controlled measurement of helpful and harmful reuse under selectively observed feedback. It is not evidence that shared memory, adaptive selection or multiple agents are intrinsically superior. Individual QA competence and recipient applicability must improve before additional acquisition complexity can be justified. Human correction effort, fallible human review, independently identified reports and single-agent architectural comparisons remain unmeasured.

The stage used CALLS scheduled calls and ATTEMPTS generation attempts on an existing Qwen2.5-7B BF16 GPU service, with no CPU model offload. All failures and earlier development versions are retained. Reproduction, full diagnostics, source attribution and resource records are in \texttt{research/adaptive\_correction\_transfer/}. The historical submission remains unchanged.
\bibliographystyle{plainurl}\bibliography{references}
\end{document}
'''
 replacements={'PRIMARY':tex(comparison(primary).split(', wins/')[0]),'PRACTICALCONCLUSION':tex(practical_conclusion),'PRACTICAL':tex(comparison(practical).split(', wins/')[0]),'CONCLUSION':tex(conclusion),'HELP':str(int(z['help'].sum())),'HARM':str(int(z.harm.sum())),'ROWS':rows,'WTL':f"{primary['wins']}/{primary['ties']}/{primary['losses']}",'DISAGREEMENT':f'{int(changes.different.sum())}/{len(changes)}','RETRY':tex(comparison(transfer).split(', wins/')[0]),'VARIATION':str(mech['varying_answer_scale_groups']),'FINALHELP':str(a['sibling_fixed']),'FINALHARM':str(a['sibling_damaged']),'CALLS':str(ledger['scheduled_calls']),'ATTEMPTS':str(ledger['attempts']),'CONTRACTCOUNT':str(contract_audit['initial_schema_invalid_credited'])}
 for k in sorted(replacements,key=len,reverse=True):note=note.replace(k,replacements[k])
 (ROOT/'paper/adaptive_correction_transfer/main.tex').write_text(note)
 print('Wrote report and illustrated note from complete results')
if __name__=='__main__':generate()
