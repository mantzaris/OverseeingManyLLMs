# Frozen prospective protocol: matched-qgm-v1

## Question and evidence boundary

Primary hypothesis: optional grouping around an actual source increases the
proportion of correct answers released within nine minutes compared with a
conventional central queue. The proposed explanation is reduced repeated source
reconstruction. Both remain hypotheses. Logs can describe source returns and
elapsed interactions, but cannot measure reading effort or cognitive demand.

Secondary question: do these particular saved LLM drafts help compared with
answering directly from the source under matched allocations? This is a controlled
allocation comparison, unlike formative-v1's shorter six-question diagnostic.
It is not a test of multiple model architectures against a single model.

No participant outcomes informed this freeze. Previously inspected source material,
model outputs and software practice informed implementation. Original scores and
manuscripts, including the weaker formative-v1 design, remain preserved.

## Conditions

| Feature | Q: central queue | G: source grouping | M: manual source-only |
|---|---|---|---|
| Questions, source tables/paragraphs, calculator | Same | Same | Same |
| Actual saved draft, scale, optional explanation/raw response | Present | Same as Q | Absent, including backend raw payload |
| Sequential Next and manual pending-request selection | Yes | Yes | Yes |
| Optional actual-source cards, at most three questions, source-aware Next | No | Yes | No |
| Stable active version; independent correct/approve/reject/defer and release | Same | Same | Same; own answer must first be entered |
| Notes and deferred drafts restored | Same | Same | Same |
| Admission pause/resume | Disabled | Disabled | Disabled |
| Offered questions / time | 12 / 540 seconds | 12 / 540 seconds | 12 / 540 seconds |

Q is the existing conventional queue, with manual selection, visible pending and
deferred work, source access and stable active review. G adds a **grouping
interaction**: same-source cards occupy space above the active review, can contain
up to three separate requests, and guide Next while members remain available.
Grouping never copies an answer or combines approval authority. Manual selection
can override Next in all conditions. G's additional cards and navigation are the
declared treatment; this study cannot isolate their visual and navigation effects
from one another. Admission is excluded both in the UI and command handler.

M necessarily lacks draft display and approving an existing draft. It uses the
same answer/scale entry, calculator, correction-version creation and separate
release. No model answers or explanations are loaded in its initial state. Its
blank placeholder is labeled source-only, not an empty model generation.

## Workload and packets

Reuse the exact three formative-v1 packets, replica 0, without selecting on model
correctness. `manifest.json` lists all six source IDs, 36 original question IDs,
raw call IDs and raw/display hashes. Each packet has two sources and 12 questions.
Public source-size and calculation characteristics motivated the earlier packet
selection; the new study retains every question, including missing/wrong drafts.
These are previously inspected benchmark contexts, not fresh held-out source data.

All tasks are offered at block start. Worker starts, in seconds from block start,
are `[0,4,8,12,16,20,180,184,188,192,196,200]`. A 0.25-second replay preparation delay
and maximum three in-flight workers are common. Questions from the two sources
are interleaved using original question order. These schedules are constructed,
not measured generation latency. All offered tasks, including unstarted tasks,
remain in the denominator. No financial deadline or economic cost is inferred.

Training uses the existing separate real source, two questions, 240 seconds.
Participants practice source/scale checking, calculator, an entered answer,
deferral/resumption, independent approval/release, and optional grouping. The
facilitator then verifies comprehension before starting scored blocks. Record
extra instruction as a deviation. No correctness feedback is supplied during
scored blocks. Forms and breaks occur outside each fixed-period block. No
think-aloud during timed blocks. Use the neutral retrospective interview after
all three blocks.

## Assignment and first tranche

The 18 manifest assignments cross all six Q/G/M orders with three packet rotations.
Each person sees each packet once and therefore six distinct scored sources; none
is the training source. Across all assignments, each condition/position/packet
cell occurs twice. The existing balanced six-run example is IDs
`0,3,7,11,13,17`. Six is a convenient assignment cycle, **not a powered sample size**.

Before collection, investigators register a feasible tranche, pseudonymous
code-to-assignment sequence, recruitment/eligibility arrangements, actual permitted
consent version and storage plan. Register assignment independently of outcomes.
Use no pilot participant twice on these sources. Report incomplete coverage after
withdrawals or failures. Do not silently reassign to favorable packets. The
software records the chosen assignment but cannot attest that external scheduling
was randomized or authorized. Coverage is reported by condition, packet and order.

## Primary endpoint and comparisons

A correct answer requires official TAT-QA exact match **and correct scale** on the
current released version. This joint definition prevents incorrect units from
counting as correct; official answer EM and token F1 are also retained separately.
For person p and condition c,

`Y(p,c) = joint-correct current-version releases / 12 offered questions`.

Primary effect: `Delta(G,Q) = mean_p[Y(p,G) - Y(p,Q)]`.
Secondary comparisons: Q minus M and G minus M, with the same outcome and
allocations. Secondary metrics and mechanism descriptions are not alternative
primary endpoints. A rejection is blocked unfinished work. Approval without release
is not completion. A new version cannot inherit approval. Old release/approval
versions remain in the event history but do not replace current-version scoring.

Also report counts of correct releases, incorrect approvals/releases, unresolved
statuses, unfinished deliverables, unstarted questions, corrections of initially
wrong drafts, damage to initially correct drafts, review/resumption intervals,
source focus/returns, grouping use, waiting while another source is reviewed,
Raw NASA-TLX and three separate control items. Manual answers have no model-draft
correction/damage baseline. Always show the components with the proportion.

## Scoring, missingness and technical exclusions

Use the unchanged official scorer and frozen annotation projection offline. No
annotation is sent to scored task views. All released answers, including EM
controls, enter blinded adjudication packets. A human rater records evidence,
reason and identity code. Adjudication is additional and does not replace official
metrics or become the primary endpoint after results. No LLM judge. Rater and
conflict-resolution arrangements must be registered before collection.

Retain all valid offered questions, difficult drafts and incomplete questionnaires.
A deliberate early finish retains 12 in the denominator and counts as an ended
block. Do not extrapolate its performance to 540 seconds. Withdrawal is retained
as provenance; its outcomes are not included in comparative summaries, subject to
the actual consent/deletion rules. In-progress interrupted exports remain in
absolute tables, not fixed-period paired effects. Missing blocks are not imputed
as zero and do not remove a person's other available comparisons.

Reject corrupt or mismatched exports from analysis with explicit errors: changed
version/manifest/runtime, wrong assignment/source/draft/schedule, failed replay or
mixed record kinds. Preserve originals and document exclusion; do not rescue them
using answers. Identical duplicate exports are deduplicated; conflicting snapshots
require choosing the final export explicitly. Multiple runs with one code are
refused until provenance is resolved. Do not silently merge development versions.
A connection loss with a running server does not pause the clock. Returned users
resume the saved logical state; interruption time is not labeled reading time.

## Analysis and interpretation

Participant is the paired unit. Average differences across complete nonwithdrawn
pairs; show individual values, absolute counts, sign/tie counts and missingness.
Report packet/order coverage and stratified descriptive outcomes where supported.
The few reused contexts are not independent financial reports. Do not treat
questions, events, generations or agent roles as independent participants.

The implementation supplies a descriptive percentile bootstrap only at six or
more complete pairs: 2,000 participant resamples with fixed seed 92741. Resample
all matched values together through each person's paired difference. This threshold
is a reporting convention, not a precision guarantee. Intervals are conditional on
the reused packets and participant sampling assumptions, which must be stated.
Below it show raw pairs and no bootstrap. No complex mixed model or automatic
significance/power/equivalence claim. A later effectiveness study must choose a
meaningful effect and sample size based on measured participant variability,
packet effects and defensible sampling assumptions.

Check whether G actually changes grouping use and source returns, whether deferred
work is later acted on/released, and whether unrelated requests wait during group
review. Compare event traces with neutral retrospective accounts. These are
exploratory behavioral explanations, not causal mediation or mental-state measures.
Use `CLAIM_DECISIONS.md` before promoting any human-effectiveness claim. A revision
after observation creates a new version; preserve and analyze versions separately.
