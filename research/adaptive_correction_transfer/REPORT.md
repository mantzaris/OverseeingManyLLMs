# Adaptive acquisition and reuse of verified corrections

This study does not establish a correctness advantage for adaptive acquisition over fixed acquisition with the same transfer mechanism. A practical improvement over risk-only individual correction is not established. The highest observed two-inspection EM is Risk-only individual at 59.0%. These observations do not establish equivalence between methods.

## What was implemented

A bounded controller chooses an answer to inspect, obtains only its answer/scale/derivation annotation, and selectively regenerates related answers. It estimates initial error, beneficial repair and harmful repair separately. A later inspection may reveal a previous recipient's before/after correctness and update those transition estimates. Uninspected private labels never become rewards. This is a harm-aware Bayesian heuristic with a five-percent randomized acquisition component, not a new bandit algorithm or an optimal policy.

The Decision desk replays current answers, source evidence, the proposed inspection, purchased feedback, uncertain recipient eligibility, actual generated repairs and the remaining budget. It withholds future disclosures and uninspected correctness. Users can demonstrate an inspection and see its consequences; arbitrary new human corrections were not evaluated. All interaction logs are scripted software demonstrations.

## Data, feasibility and freeze

TAT-QA supplies real financial-report tables/prose and human-written benchmark questions. Agent assignments, source-context episodes and unit-cost inspections are constructed. The experiment uses ideal annotation supervision and fallible Qwen-generated repairs, not measured human review. The public source revision is `870accc41953dcde885aabeb963d94aabdc0fbc3`, dataset CC BY 4.0 and code MIT.

Twelve source-order train contexts were development-only. All four answer-interface versions are retained. The final pilot obtained 20/72 initial EM. Among 60 transfer trials, nine helped and six harmed accepted sibling answers; matched reattempts helped seven and harmed three. Four additional reused development contexts exercised sequential acquisition. No further method revision followed that smoke pilot.

The protocol was committed at `18dbae40` before held-out inference. Evaluation contains **24 new source contexts, 144 distinct questions, two generation replicas and 288 common initial answers**. Seven core policies produce 336 paired runs at two inspections, with budget-zero/one prefixes. Twelve contexts at replica zero add the frozen-parameter diagnostic; eight add third-inspection adaptive/fixed comparisons, for **364 completed traces**. No case was replaced. Selection followed released test_gold order, exact duplicate exclusions, source size and a 1200-token public-prompt cap. No selection used model outcomes.

The released data lack reliable report identifiers. Contexts are the paired units, but different contexts may originate from one report. Consequently 24 contexts do not imply 24 independent companies or reports. One long paragraph is shared by two evaluation contexts, producing 23 exact-text components. A separately labeled post hoc component-bootstrap sensitivity is saved in `analysis/overlap_sensitivity.csv`; these components still do not identify all shared reports. Repeated generations and policy runs are not independent observations. Public benchmark exposure during model training cannot be excluded.

## Primary outcomes at two inspections

| Policy | Official EM | F1 | Answer + exact scale | Whole contexts correct / 48 | Never-inspected fixed / harmed | Recipient calls | Unfinished |
|---|---:|---:|---:|---:|---:|---:|---:|
| Individual | 167/288 (58.0%) | 63.3% | 165/288 | 1 | 0/0 | 0 | 17 |
| Context memory | 165/288 (57.3%) | 63.9% | 160/288 | 1 | 24/26 | 432 | 2 |
| Source rule | 158/288 (54.9%) | 60.7% | 154/288 | 0 | 4/13 | 95 | 16 |
| Fixed acquisition | 162/288 (56.2%) | 62.7% | 159/288 | 1 | 15/20 | 186 | 13 |
| Adaptive | 156/288 (54.2%) | 60.5% | 153/288 | 0 | 14/21 | 189 | 7 |
| Reattempt | 164/288 (56.9%) | 63.1% | 162/288 | 0 | 1/4 | 95 | 17 |
| Risk-only individual | 170/288 (59.0%) | 65.0% | 167/288 | 2 | 0/0 | 0 | 3 |


Each method uses 96 ideal inspections across 48 context/replica episodes. Inspected outputs are replaced directly, so their correctness is not evidence of model repair. The table's sibling counts compare final **never-directly-inspected** answers with their original states. They differ from event counts, which may count a repeatedly regenerated answer more than once. Official EM/F1 and separate exact-scale/joint scores follow the released evaluator.

- **Primary, adaptive minus fixed acquisition:** -2.08 percentage points, 95% paired interval [-4.86, 0.35], wins/ties/losses 4/12/8 across 24 contexts.
- **Practical, adaptive minus risk-only individual:** -4.86 percentage points, 95% paired interval [-9.72, 0.00], wins/ties/losses 4/9/11 across 24 contexts.
- **Correction versus extra generation, source rule minus reattempt:** -2.08 percentage points, 95% paired interval [-5.90, 1.74], wins/ties/losses 2/16/6 across 24 contexts.

Intervals use 2000 paired context bootstrap resamples with seed 91844 after averaging replicas within context. They are descriptive for this small sample and are not multiplicity-adjusted. No noninferiority margin was declared, so an interval crossing zero cannot establish preserved quality or equivalence. All prespecified comparisons are in `analysis/comparisons.csv`.

## What explains the outcomes

Initial answers achieved 92/288 official EM and 89/288 joint answer/scale correctness. There were 36 unfinished initial answers. Only 115 had usable generated evidence IDs, and 103 supplied all requested output fields. The format guard validates answer shape, scale and explicit arithmetic; it does not require complete evidence or certify that a citation supports the answer. Individual financial QA competence and evidence localization remain substantial bottlenecks; these are not coordination failures.

Adaptive transfer produced **16 helpful and 24 harmful regeneration events** in 189 attempts at the primary budget. Its final never-inspected answers included **14 additional correct answers and 21 newly wrong answers**, or 0.146 additional sibling fixes per inspection before subtracting harm. 72 of its inspections found a currently incorrect answer; 56 of those actual corrections were reused. Confirmations of already correct answers are counted separately in `analysis/feedback.csv`.

Adaptive and fixed acquisition selected different inspection sequences in 39/48 matched episodes. Thus this is not an experiment where the policies are identical by construction. However a different action is not itself a benefit. By the second inspection, 8/48 adaptive episodes had acquired at least one label for an earlier transfer. Such feedback can affect second-step recipients; only the third-inspection diagnostic can let it influence a subsequent acquisition.

A telescoping score accounting clarifies the primary gap. Adaptive corrected 72 currently wrong inspected answers, versus 80 for fixed acquisition. Their regeneration events contributed net -8 and -10 correct answers, respectively. Starting from the same 92 correct answers, this gives 156 versus 162. Thus the observed gap reflects weaker local inspection gains despite slightly less net regeneration damage; fresh-generation variation remains part of the comparison.

The frozen-parameter diagnostic gave +0.00 percentage points, 95% paired interval [0.00, 0.00], wins/ties/losses 0/12/0 across 12 contexts. The three-inspection adaptive-minus-fixed diagnostic gave -8.33 percentage points, 95% paired interval [-14.58, -2.08], wins/ties/losses 0/4/4 across 8 contexts. These use the smaller prespecified subsets and are secondary. Disabling parameter updates changed no inspection or recipient membership in the twelve diagnostic episodes. One recipient execution order changed, without changing official correctness. The action changes in the main comparison therefore should not be credited to demonstrated parameter-learning benefits. The third-inspection result is unfavorable rather than a rescue for the primary finding.

There were 218 groups of genuinely identical full model requests, of which 23 returned different answer/scale pairs. Of those identical-request groups, 2 also varied in official correctness. Seeds did not provide bitwise reproducibility. Changed feedback/history prompts are excluded from this count. Each primary policy received actual continuations, and all variation was retained. Sampling variability can contribute to differences even when a policy's decisions coincide.

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

**Recommendation:** This study does not establish a correctness advantage for adaptive acquisition over fixed acquisition with the same transfer mechanism. A practical improvement over risk-only individual correction is not established. Retain the protocol as a reproducible audit-and-transfer baseline. Do not make adaptive correction transfer the central methodological claim without a supported gain over the strongest simple comparator. The next useful experiment is to establish reliable recipient applicability and individual answer competence, with matched correction-versus-reattempt trials, before adding more acquisition complexity. A single orchestrator could run the same protocol; this experiment does not establish that splitting answer generation into agent roles adds value.

## Failures, verification and resources

Every declared trace completed. Failed and malformed generations remain in the main accounting, and malformed repairs retain the previous answer. The reporting implementation initially requested `scale_exact` from a wrapper that exposes `scale`; it raised before writing tables. `results.py` fixes only that reporting lookup. The frozen original and `analysis_implementation_note.json` preserve the defect. No controller, estimator or source selection changed after freeze. A separate reporting audit found 4 initial answers with invalid auxiliary/scale-schema fields that still received official answer credit. The frozen statement that malformed outputs score zero was too broad: the implemented metric scores the extracted answer even when another field is invalid. Primary recorded scores and online updates are preserved. `analysis/contract_sensitivity.csv` and `contract_comparisons.csv` additionally zero schema-invalid outputs; this post hoc rescore does not claim those stricter labels drove the saved trajectories.

Replay verified 364 complete evaluation traces and 1334 unique actual prompts without loading private sibling annotations. Integrity checks verified 48 complete matched context/replica blocks. Sixteen focused protocol/UI tests, 51 relevant historical tests, and nine browser workflow checks passed. Replay median was 4.99 ms per trace and p95 7.43 ms, including saved-request reads, parsing and scoring of purchased feedback; this is not pure planner latency.

At this ledger checkpoint the stage used 2083 scheduled calls, 2058 attempt intents, 2058 returned GPU generations, 0 failed transport attempts and 0 retries. Statuses: `{'context_limit': 25, 'ok': 2058}`. Eight returned responses were unparseable JSON; these are separate from transport failures. Tokens: 2103772 input and 172836 output. Development, failed preflight checks, primary evaluation and diagnostics are all included. Final resource closure is recorded in `resource_ledger.json`.

Stage elapsed: 2h 0m 1s. Cumulative wall since the original start, including gaps: 62h 28m 54s; overrun beyond the original 36-hour target: 26h 28m 54s. This stage has separate explicit authorization and is not backdated into the original budget. Existing Qwen2.5-7B BF16 RTX6000Ada service was reused without CPU offloading. No paid resources, human participants or outbound messages were added.

## Reproduce and demonstrate

```bash
bash research/adaptive_correction_transfer/reproduce.sh
bash paper/adaptive_correction_transfer/build.sh
python3 -m research.adaptive_correction_transfer.prototype.server --port 9034
```

The first command reconstructs saved evidence without inference. The last starts the local replay desk at http://127.0.0.1:9034/. See README.md for the collection provenance, official data download, API and exact GPU configuration. Scientific figures are generated from CSV tables as PDF, SVG and PNG. The separate illustrated note is `paper/adaptive_correction_transfer/main.pdf`; historical manuscript sources remain unchanged.
