# Stage 7 measured-data application

Stage 7 completes a measured HVAC diagnosis and simulated review study. It starts
from pushed Stage 6 commit `d9b39589ce7b67ae09c1b7055fcf3dceecdb7a00`; the working
tree was clean and no newer work existed. All historical experiment artifacts
and positive, null and unfavorable results remain preserved. The methodological
contribution is allocation using expected preventable loss when review itself
can fail or introduce an error. It is not a new exhaustive scheduling algorithm.

## Scope and original clock

Start: **2026-09-11 02:44:20 UTC**. The original start remains
2026-09-09 15:38:57 UTC and the binding 36-hour deadline remains
**2026-09-11 03:38:57 UTC**. The gap after Stage 6 consumes the budget: only
54m37s remained at authorization. Stage 7 therefore reserves the final 15 minutes,
stops inference by 03:23:57, and caps attempts at 600. No additional paid resources
or model server are started. The final clock and cumulative ledger are in
[accounting.json](../artifacts/stage7_empirical/accounting.json).

The primary measured application takes precedence over SQL. The official
[BIRD-Critic repository](https://github.com/bird-bench/BIRD-CRITIC-1#dataset-uses)
excludes `sol_sql` and `test_cases` from public records and distributes them by
email request. No contact was made. The [BIRD-SQL site](https://bird-bench.github.io/)
offers accessible development references and databases. A separate database audit,
execution evaluator, disjoint split and paired query study could not be completed
alongside the primary study within the remaining original deadline. No SQL results
or synthetic fraud validation are claimed. This is a resource limitation, not a
claim that BIRD-SQL assets are inaccessible.

## Provenance and evidence hierarchy

The [source study](https://doi.org/10.1038/s41597-020-0398-6) and
[Berkeley Lab inventory](https://data.openei.org/files/910/lbnldatasynthesisinventory.pdf)
distinguish physical experiments from simulations. We select only **SZCAV.csv**
and **SZVAV.csv** from
[Figshare article 11752740, version 3](https://figshare.com/articles/dataset/LBNLDataSynthesisInventory_pdf/11752740/3).
The pinned API metadata specifies **CC0**. Complete file checksums, download URLs,
metadata and transformations are saved in [provenance.json](../artifacts/stage7_empirical/provenance.json)
and [source_checksums.json](../artifacts/stage7_empirical/source_checksums.json).

| Evidence layer | What it represents |
|---|---|
| Observed | One-minute temperatures and fractional control commands recorded on the FLEXLAB X3A air handler |
| Ground truth | Component conditions manually imposed for named experimental days, from inventory Tables 3-3/3-4; binary fault indicators cross-checked offline |
| Constructed task | Four-class diagnosis of three retrospective windows per experimental day |
| Generated | Pinned Qwen proposals and separately prompted same-model review responses |
| Assumed oversight | Simultaneous ticket arrivals, review slots and abstract service times, cutoffs, dimensionless error weights and ideal correction |

The physical apparatus is real, but faults are experimentally imposed and the
facility is not observed occupied-building operation. The prior ventilation
observations are synthetic. Retail transaction records are simulated benchmark
records despite genuine generated tool workflows. Those evidence levels remain
distinct. Nothing here measures actual repair success, energy savings, prevented
equipment damage or human performance.

## Cases, preprocessing and development

All 26 source days are included: 15 constant-volume and 11 variable-volume days.
The first chronological day within each of four component categories and each
mode is development. This gives **eight development days and 18 evaluation days**.
Whole-day splits keep adjacent windows together. Evaluation comprises 54 windows
at 10:00--10:59, 12:00--12:59 and 14:00--14:59. Each contains 60 actual samples.
All are available before the retrospective ticket queue opens after 14:59.
They are three correlated diagnosis tickets for one apparatus, not three
independent physical faults or 54 independent source cases.

Public evidence retains control mode, recording hour, physical units and named
mean/min/max/end-minus-start statistics of ten channels. Actual dates, filenames,
fault flags, imposed-fault descriptions and future observations are excluded.
The taxonomy is normal, outdoor damper, heating valve and cooling valve, grouping
stuck/leaking variants. The conventional nearest-centroid classifier fits mean,
standard deviation and class centers on development only, using the same 40
statistics, mode and hour. No evaluation preprocessing parameters are fitted.

The initial 48-call pilot has zero correct proposals and 23 abstentions. Raw
responses expose misinterpretation of a statistics array's final change value as
the current reading. One declared revision names each statistic and asks for the
most likely supported condition, allowing abstention for unusable evidence. It
also provides generic physical reasoning guidance. The revised pilot has six
correct proposals, one correction and one harm. Both changes are documented
together; their individual causal effects are not identified. Every initial
pilot output and initial estimator is preserved.

The final application estimator bins on proposed category, with pooled fallback
for fewer than six examples. Risk is `(errors+1)/(n+2)`. Signed gain is
`(corrections-harms)/(n+2)`. The populated heating bin has n=21, risk 0.695652 and
gain -0.043478. Other bins fall back to pooled risk 0.730769 and gain zero.
This sparse estimator has no positive-benefit request. The frozen primary
condition must decline review. It does not inspect evaluation labels to decide
which reviews would harm. A secondary risk-only benefit ablation, declared before
evaluation, ignores reviewer failure/harm. Ideal review is a separate upper bound.

## Frozen evaluation and semantics

The method freeze is **`5a5ae06a4cf311799214cac148bbbb7c2361f823`**. The
[declaration](../artifacts/stage7_empirical/declaration.json) and frozen source
hashes precede every evaluation call. No source case is selected using model
outcomes. No evaluation label refits the estimator, prompt or baseline.

One generation replicate per source window gives 54 evaluation proposals and
54 saved review responses. Six policies are no review, FCFS, EDF, uncertainty,
delay-aware greedy and queue-order search. All share public requests and positive
expected-benefit eligibility. Review completion, not dispatch, releases the saved
response. An invalid review preserves the proposal; abstention remains unresolved.
All final proposals and reviews are syntactically valid, so those failure rules
are tested but not exercised by evaluation failures.

Each day has three simultaneous tickets with independently shuffled cutoffs 2/4/6
and weights 4/8/12, using seed 7000 plus the opaque run index. Wrong or unresolved
diagnosis incurs the assigned weight at cutoff. These are dimensionless scenario
costs, not empirical business or energy losses. Completion at equality is timely.
Search enumerates all 16 ordered subsets at queue size three, assigning each
candidate review to the earliest available slot. It cannot see hidden correctness,
saved review outcomes, or unreleased observations.

The prespecified matrix uses model signed gain, model risk-only and ideal review;
heterogeneous and uniform weight eight; one/two slots; and durations one/two/three.
This yields **3,888 paired policy replays** on the same 54 preparations. No extra
GPU calls repeat scheduling comparisons. The primary contrast is search minus
greedy, signed-gain model review, one slot, two ticks, heterogeneous weights.
Bootstrap intervals use 2,000 draws with seed 20260917, resampling whole days
within control mode and preserving every matched condition. The single apparatus
and small day sample limit population interpretation. There is no stable equipment-level interval, and exchangeability across day blocks is unverified. Intervals are conditional resampling summaries. Repeated policy replays
and windows do not inflate the independent-unit count.

## Measured results

### Diagnosis and reviewer effectiveness

| Annotated category | Evaluation days | Windows | Proposal correct | Review correct | Conventional baseline correct |
|---|---:|---:|---:|---:|---:|
| Normal | 3 | 9 | 1 | 1 | 6 |
| Outdoor damper | 4 | 12 | 0 | 0 | 7 |
| Heating valve | 6 | 18 | 18 | 12 | 14 |
| Cooling valve | 5 | 15 | 0 | 1 | 0 |
| Total | 18 | 54 | 19 | 14 | 27 |

The proposer selects heating valve on 51/54 windows, showing severe category
collapse. The baseline reaches 50.0% versus the model's 35.2%, but both miss all
cooling-valve cases. A day-level imposed-condition label does not guarantee that every selected window excites an observable symptom. Accuracy therefore measures the whole representation and classification task, rather than isolating model reasoning. This is evidence of a diagnosis bottleneck, not reliable
application operation. The general guidance and small development split are
limitations, not a basis to tune the frozen evaluation after seeing this result.

Saved review corrects **1/35 wrong proposals**, leaves 34 unresolved, preserves
13/19 correct proposals, changes five correct proposals to a wrong label, and
changes one correct proposal to abstention. Five reviews abstain in total, with
four on already wrong proposals. Review-everything accuracy falls to 14/54.
No malformed generation or HTTP failure occurs. Prediction AUROC is 0.50226;
Brier is 0.23049 versus pooled-development 0.23488 and constant-half 0.25000.
Nearly tied risks provide little discrimination.

### Primary and secondary paired allocation

| Condition, one slot / two ticks | Search loss | Greedy loss | EDF loss | Search-minus-greedy, 95% interval | W/T/L |
|---|---:|---:|---:|---|---|
| Model signed gain (primary) | 15.333 | 15.333 | 15.333 | 0.000 [0.000, 0.000] | 0/18/0 |
| Model risk-only (secondary) | 18.000 | 18.000 | 18.000 | 0.000 [0.000, 0.000] | 0/18/0 |
| Ideal review (secondary) | 0.000 | 3.333 | 0.000 | -3.333 [-4.889, -1.778] | 10/8/0 |

The primary zero interval is a **mechanical admission-rule tie**, not proof of
policy equivalence. All policies decline review, retain 19 correct/35 unresolved
diagnoses and miss the one realized useful model review. They avoid six harmful
changes. This follows from frozen development information, not an evaluation oracle.

Risk-only search and EDF review all 54 tickets; greedy reviews 39. Search and
greedy sequences differ on 15/18 days, but both apply the one helpful and six
harmful responses, leaving 14 correct and 40 unresolved. Search minus no-review
loss is **+2.667 [0.217, 5.778]**, with one win, 12 ties and five losses. Reviewing
more proposals is not a benefit by itself.

Ideal search corrects all 35 initial errors, while greedy corrects 25 and misses
ten. EDF matches search exactly at this capacity. Earliest-deadline ordering
fits all three equal-duration reviews into cutoffs 2/4/6, so search's advantage
over greedy does not establish a need for exhaustive planning. All model
search-minus-greedy sensitivities also tie. The complete capacity/duration and
uniform-weight outcomes remain in the saved tables, including no-review controls.

## Figures, examples and manuscript

Nine figures are generated from saved source windows, output pairs and tables as
vector PDFs and 300-dpi PNGs. They cover recorded signals, correctness and loss,
paired differences, zero-centered capacity sensitivity, review transitions and
risk diagnostics, a risk-only ablation, and first-qualifying queue examples.
Selection is numerical source order, never effect magnitude. Primary model review
has only ties; its first is run01. Ideal review's first benefit is run02 (-8),
and its first tie is run01. No unfavorable search-minus-greedy example exists in
these declared primary-capacity conditions. No substitute favorable case is chosen.

The main manuscript now leads with measured HVAC diagnosis and fallible review,
condenses synthetic maintenance into a mechanism study, and preserves both
unfavorable retail primary findings (+0.250 and +1.667). Detailed maintenance
and retail robustness results move to the supplement. Dataset labels validate
diagnoses; they do not validate the imposed scheduling consequences. The compiled
manuscript and supplement, build audit and page inspection record accompany this
package. [Reproduction](../paper/STAGE7_REPRODUCTION.md).

## Verification, failures and accounting

All 204 GPU attempts succeed with zero retries, reconciling to server deltas of
**125,765 prompt tokens and 9,131 completion tokens**. Total request latency is
174.658 seconds, maximum 1.734 seconds; largest actual prompt/output are 745/93
tokens. The last generation finishes **02:58:51.311836 UTC**, before the reserve.
The existing RTX 6000 Ada server remains healthy with the pinned Qwen revision,
BF16 and zero CPU offloading. No server or experimental background worker was
started; serial SSH workers have exited. Provider allocation charges are unavailable.

Eleven focused tests cover label isolation, whole-day splits, signed-benefit
eligibility, EDF/search arithmetic, cutoff equality, reviewer harm, failure
preservation and policy pairing. All 3,888 traces and five result tables replay.
Historical regression checks cover nine retail and nine robustness tests, Stage 1
through Stage 4 traces, 288 Stage 5 preparations and all Stage 6 live/sensitivity
traces. Audit reports are redirected into Stage 7, so historical bytes are preserved.

The local Matplotlib 3.1 lacks `TwoSlopeNorm`; a compatibility wrapper supplies
the mathematically identical symmetric normalization and changes the displayed
harm label to include unresolved abstention. The initial plotting failure log is
retained. No frozen simulation, selection, estimator or numerical analysis changes.
No new publication redaction was needed. Prior Stage 5 redaction provenance,
original hashes and private originals remain intact. Keys, environments, complete
external CSVs and model weights are excluded from Git.

The strongest supported contribution is a reproducible connection between public
expected intervention benefit and finite-duration allocation, with empirical
evidence showing how ineffective review can dominate scheduling. A credible next
step is independent domain review of the diagnosis representation and reviewer
protocol, followed by a newly authorized, separately frozen multi-equipment study.
Human authors must still review scientific claims, authorship/declarations and
venue AI-disclosure and supplementary-upload requirements before submission.

## Final package checkpoint

At **2026-09-11T03:30:35.242085+00:00**, Stage 7 elapsed time is **0h 46m 15s**. Cumulative elapsed
time from the original start is **35h 51m 38s**, including inter-stage gaps,
with **0h 8m 21s** remaining before the binding 36-hour deadline. There is
no overrun at this checkpoint. The final commit's committer timestamp records
subsequent packaging time; it does not reset the clock.

Cumulative accounting is **55,586 scheduled calls, 55,588 attempts, two retries,
three retained historical failed attempts, 30,796,634 prompt tokens and 684,928
completion tokens**. Stage 7 contributes 204 attempts and no failures.
[Ledger](../artifacts/stage7_empirical/accounting.json). The read-only final
server check at 03:26:09 UTC reports HTTP health 200, no experimental workers,
and the original GPU engine still resident. No existing service was changed.

The final saved-output reproduction command passes, rebuilding all tables,
figures and both PDFs. The **8-page main paper** contains 26,529 extracted
non-whitespace characters; the **17-page companion supplement** contains 48,727.
All fonts are embedded, citations resolve, template files are unchanged,
and every rendered page was visually inspected.
[Build audit](../artifacts/stage7_empirical/manuscript_audit.json),
[page inspection](../artifacts/stage7_empirical/visual_inspection.json),
[final reproduction log](../artifacts/stage7_empirical/end_to_end_reproduction_final.log).
Raw LaTeX logs retain intermediate-pass warnings and their original encoding;
the final PDF audit has zero unresolved citations or overfull boxes.

A canonical Git-blob audit confirms **18,033 historical artifact and
configuration files** are unchanged from the pushed Stage 6 baseline.
[Preservation audit](../artifacts/stage7_empirical/historical_preservation.json).
The experiment was frozen in `5a5ae06a4cf311799214cac148bbbb7c2361f823`; completed
evaluation evidence was committed as `7635383211d920ea2ccdf4784c22e559a0c9c8e0`.
The final manuscript package is a separate milestone. No push or submission
is performed.
