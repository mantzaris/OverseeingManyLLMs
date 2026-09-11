# Stage 7 measured-data protocol

Authorization begins 2026-09-11 02:44:20 UTC. The original 36-hour deadline,
03:38:57 UTC, remains binding. Inference stops by 03:23:57 UTC. At most 600
attempts across development and evaluation, one retry, 60-second timeouts.
No new server or paid resources. Reuse the verified pinned BF16 Qwen server.

The primary question is whether current-queue planning reduces weighted diagnosis
error when review can both help and harm. The primary comparison is search minus
greedy with a model reviewer, one reviewer, two-tick service, heterogeneous costs.

Use only SZCAV and SZVAV physical FLEXLAB experiments from Figshare version 3,
article 11752740. The source inventory provides day-level imposed-fault labels.
All 26 available experimental days are included. The first date per mode and
component class is development (8 days); the remaining 18 days are evaluation.
No model performance affects inclusion. Whole-day splits prevent adjacent-window
leakage. The same equipment is reused across days, so this is conditional
experimental-day evidence, not independent-building inference.

Each day supplies three retrospective tickets, windows 10:00--10:59,
12:00--12:59 and 14:00--14:59. All are available after the last window closes.
These are correlated requests to classify observed component condition, not
three concurrent physical machines. Dates, filenames, fault flags, imposed-fault
descriptions and subsequent sensor observations are withheld. Public evidence
includes control mode, hour, physical units, mean, min, max and end-minus-start
of ten measured/control channels. A four-class taxonomy distinguishes normal,
outdoor damper, heating valve and cooling valve conditions. Abstention is allowed
and remains unresolved. No repairs or counterfactual energy savings are scored.

One proposal and one independently prompted review generation per ticket use
temperature 0.3, top-p 1, maximum 128 output tokens, fixed role/task seeds and
the existing 2048-token GPU context. Save every attempt. Invalid preparation
remains unresolved; invalid review preserves the proposal. Abstaining review
leaves the task unresolved. Labels are consulted only for scoring and completed
ideal review. Saved review responses become effective only at review completion.

Development fits a conventional standardized nearest-centroid classifier using
the same evidence statistics. Development alone also fits error probability and
signed reviewer gain (corrections minus harms). Bin by proposed diagnosis, use
pooled fallback for fewer than six development examples. Risk is (errors+1)/(n+2)
and gain is (corrections-harms)/(n+2), a zero-centered shrinkage rule. Ideal benefit
is weight times risk; fallible benefit is weight times signed gain. All policies
share positive-benefit eligibility. Negative predicted gain does not force review.

The initial 48-call pilot returned 23 abstentions and no correct proposals. Its
responses also misread array end-minus-start values as current control states.
One development revision, declared before evaluation, names all statistics and
requests the most likely of the four supported conditions, reserving abstention
for unusable observations. It includes general physical reasoning guidance, not
any experiment-specific answers. Preserve initial outputs and estimator; fit
the final estimator only on the revised 48-call development collection.

Freeze estimator, complete source IDs and code hashes after this revision,
before evaluation's 108 scheduled calls. One generation replicate suffices under
the remaining cap; variability between sampling seeds is not separately estimated.

All six policies reuse identical saved proposals/reviews. Release all three tickets
at simulated tick zero, with independently shuffled cutoffs 2/4/6 and weights
4/8/12 using a run-ID seed. Correct diagnosis has loss zero; unresolved/incorrect
diagnosis at cutoff incurs its declared dimensionless weight. Completed review
at equality is timely; late consequences cannot be erased. Ticks do not represent
measured human or GPU time. These operational assumptions are our extension.

Prespecified sensitivity covers 1 or 2 reviewer slots, service durations 1/2/3,
ideal or saved model review, and heterogeneous or uniform weight 8. The 144
policy conditions per day are paired replays, not independent observations.
Search exactly enumerates current-queue ordered subsets and schedules onto the
earliest available reviewer, without future arrivals or hidden labels.

The revised development pilot has six correct proposals, one correction and one
harmful review. Pooled signed gain is zero; the populated heating-proposal bin
has negative gain. Therefore the primary signed-gain condition mechanically
declines every review. Preserve this result. Before evaluation, add one explicitly
secondary mechanism ablation: model review with error-risk-only benefit. This
tests the consequence of ignoring measured reviewer limitations, and is not a
claim that its benefit model is calibrated. It reuses responses without inference.
The final matrix has 216 conditions per day, 3,888 policy replays in total.

Analyze paired experimental-day differences with 2,000 bootstrap resamples,
seed 20260917, stratified by control mode. Keep all conditions/windows of a day
together. Report intervals as small-sample, single-equipment conditional summaries.
Report correctness, harm, corrections, failures, abstention, reviews, time, waiting,
missed useful reviews, calibrated risk and planning effort. Select examples by
first numerical run with positive, zero or negative primary differences.

Figures cover measured signals and withheld annotation, policy outcomes, paired
differences, capacity/duration sensitivity, scheduling timelines and reviewer
transitions. Every caption distinguishes measured, annotated, generated and
simulated quantities. Preserve all historical results and redaction provenance.

SQL is secondary. Critic reference assets require prohibited contact. Accessible
BIRD-SQL would require a separate source/database audit and execution protocol;
omit it if this cannot finish within the original deadline. No shallow SQL or
synthetic fraud study substitutes for the measured primary application.
