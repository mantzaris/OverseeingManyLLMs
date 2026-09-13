# Computational oversight study: results and interpretation

**Completed:** 31,680 declared CPU simulations on 36 original TAT-QA questions,
six reused real financial-report contexts and genuine saved model drafts. There
are **zero human observations and zero new inference calls**. Every result below
is conditional on the declared simulated reviewer and workload. The prospective
matched human study and its position paper are preserved.

## Main result

Grouping's mean correct-release count never exceeds the central queue with the
same bounded source-aware navigation in any of the 66 declared settings. It is
lower in 62 and tied in 4. Three ties are the zero-group-cost settings,
where equality follows from the model by construction; the fourth is the low-load,
long-budget condition with nearly all work completed. This is not evidence that
real grouping cards cannot help people. Their possible comprehension or strategy
benefit was deliberately not granted to the simulation without data.

Against FIFO, grouping has positive cell-mean differences in 24 settings,
negative differences in 40, and ties in 2. These counts describe a designed
sensitivity grid, not the prevalence of beneficial conditions in real work.
Source-aware ordering, rather than the presence of cards, is the stronger
computational explanation. Q-sticky is a further useful simple control and usually
matches or exceeds G, but can suffer when consecutive-source carryover is harmful.

## Reference setting, not a fitted human model

Twelve questions, 540 seconds, original arrivals, orientation coefficient S=25 s
(actual unfamiliar orientation 18.75 s), long familiarity, 4-second group overhead, detection .85, correction
.85, initial-correct damage .02 and manual correctness .75. Means average three
packets and 32 paired Monte Carlo seeds.

| Policy | Correct | Incorrect | Unfinished | Orientation seconds | Group seconds |
|---|---:|---:|---:|---:|---:|
| FIFO Q | 5.448 | 1.062 | 5.490 | 69.862 | 0.000 |
| Grouped G | 5.292 | 1.042 | 5.667 | 61.061 | 10.724 |
| Source-aware Q | 5.406 | 1.062 | 5.531 | 61.859 | 0.000 |
| Sticky Q | 5.615 | 1.031 | 5.354 | 48.317 | 0.000 |
| Manual M | 5.177 | 0.792 | 6.031 | 69.591 | 0.000 |


Primary G-Q difference: **-0.156 [-0.270, -0.043] correct releases per twelve offered**.
G minus source-aware Q: **-0.115 [-0.170, -0.059]**. G minus sticky Q: **-0.323 [-0.477, -0.169]**.
Intervals are mean +/- 1.96 Monte Carlo SE on seed blocks, after averaging the
three rotations. They quantify numerical uncertainty under these assumptions,
not uncertainty about people or financial reports. Reference G-Q seed-block
wins/ties/losses are **3/16/13**. No noninferiority or equivalence
claim is made.

Q-M is +0.271 [-0.007, 0.548]; G-M is +0.115 [-0.152, 0.381]. The reference assistance differences are therefore
small and numerically uncertain under this particular model. Q-M holds FIFO
navigation fixed and isolates draft availability within the model. G-M also changes
source ordering, so it is a whole-workflow comparison, not a pure assistance effect.
All components stay
visible: a larger released count can include more wrong releases. Empty original
drafts use the same construction pathway as manual questions, rather than being
removed or credited as correct.

| Policy | Source switches | Source returns | Mean first wait (s) | Unrelated task-wait sum (s) | Never selected |
|---|---:|---:|---:|---:|---:|
| FIFO Q | 6.71 | 5.71 | 260.21 | 1686.66 | 4.33 |
| Grouped G | 2.48 | 1.48 | 261.13 | 1722.69 | 4.47 |
| Source-aware Q | 2.52 | 1.52 | 258.22 | 1710.00 | 4.32 |
| Sticky Q | 0.96 | 0.03 | 246.36 | 1913.31 | 4.24 |
| Manual M | 6.48 | 5.48 | 268.01 | 1722.72 | 4.79 |


Waiting includes received but never-selected requests censored at cutoff. Source
returns count a previously encountered source after another source. Unrelated
task-wait is summed across tasks and can exceed 540 seconds; it is not a reviewer's
elapsed time or an observed attention measure. In this original schedule all 12
tasks arrive and start before cutoff. All declared stress schedules also finish
delivery before cutoff, so unstarted count is zero throughout this matrix.
Never-selected review work is nevertheless substantial and remains in the totals.

## Where the outcome changes

- **Familiarity matters.** At orientation coefficient S=25 s and higher effectiveness,
  changing long to short persistence moves G-Q from -0.156 [-0.270, -0.043] to +0.198 [0.081, 0.315]. At S=75 s
  with short persistence, G-Q is +0.865 [0.727, 1.002]. That condition also raises
  mean incorrect releases from 0.688 in Q to 0.833 in G.
  More correct releases are not an unqualified improvement in oversight.
- **Preexisting source order matters.** With 24 questions in two waves, interleaved
  arrivals yield G-Q +0.583 [0.462, 0.704]; source-blocked arrivals yield -0.042 [-0.090, 0.007].
  When FIFO already stays within a source, there is little orientation saving
  for grouping to obtain. Burst/spread and capacity panels are retained separately.
- **Capacity changes the opportunity.** With six questions and fifteen minutes,
  all four assisted policies average 5.031 correct, 0.938 incorrect and
  0.031 unfinished. Their tie reflects ample capacity and shared potential
  outcomes, not proof of human equivalence. With 36 questions and fifteen minutes,
  G-Q is +1.333 [1.068, 1.599], while source-aware Q still exceeds G by 0.208 answers.
- **Carryover can reverse an apparent benefit.** With long memory and a .20
  same-source carryover hazard, G-Q becomes -0.740 [-0.925, -0.555]. G's wrong releases rise from
  1.042 to 1.688; FIFO's rise from 1.062 to 1.125.
  The same hazard applies in every condition. More frequent same-source
  transitions expose G and sticky Q more often. This relationship is modeled,
  not an observed psychological effect.
- **Draft usefulness is conditional.** When manual construction is 20 seconds and
  verification 40 seconds, G-M is -4.198 [-4.528, -3.868]. With 90-second construction and
  8-second verification it is +2.229 [2.040, 2.418]. These are declared extremes, not tuned
  estimates. Actual initial drafts are low quality (7/36 joint-correct, five
  empty/unsupported), while the effectiveness of checking/repair remains assumed.

## Mechanism and counterexamples

For the same completed task-attempt set, a useful time balance is orientation
saved minus group interaction overhead. This can predict capacity benefit only
when other work phases and success paths are comparable. Across different task
subsets, subtracting aggregate orientation totals alone does not prove time saving.
A saved minute matters only if enough remains to finish an additional decision and
release. Waiting for unrelated work and harmful carryover can offset that benefit.

The bounded source-aware Q control removes group cards but uses exactly G's
selection mechanism. The zero-cost identity is a structural check, not a discovery.
Positive overhead can change eligible groups and the completed subset, so no general
dominance theorem for every possible arrival/outcome stream is asserted. In this
finite declared grid, however, no G cell mean exceeds that control.

Examples use the first qualifying configuration, rotation and seed rather than
maximum effect. The first favorable individual trace is **002_o0_high_short,
rotation 1, seed 10014**: G releases one more correct answer even though orientation
cost is zero and the cell mean favors FIFO. This gain comes from which outcomes
reach cutoff, not recovered context time. The first unfavorable trace is
**000_o0_ideal_short, rotation 0, seed 10000**, where G completes one fewer correct
answer. A favorable single trace therefore cannot establish an operating-region
advantage. See `EXAMPLES.md` and the paired timelines for actual questions and
saved drafts behind these simulated outcomes.

The simulated FIFO policy is a navigation strategy, not a limitation imposed by
the real central-queue interface. People can manually select related requests in
that interface. Both source-aware queue controls represent that stronger competing
explanation. This study does not show that multiple model architectures outperform
a single model or that users experience reduced cognitive load.

## Reproducibility, validation and failures

The model, original inputs, fixed matrix and analysis were committed at
`8b74d58b` before comparative runs. A 64-seed preliminary forecast was reduced to
32 before outcomes, preserving all 66 parameter settings. No seeds were added,
replaced or removed based on results. The batch finished in 265.2
seconds of measured host wall time. Raw result rows and compact command/phase
traces are saved, with scenario/simulation identifiers and no human-export schema.

Eight pre-run tests cover original arrivals, unique goals, equal selector information,
shared familiarity, zero-cost identity, cutoff accounting, versioned releases,
recognized failure and ordinary-engine replay. Four additional read-only checks
probe actual hidden-label mutation before first dispatch, manual draft isolation,
paired randomness and approval without release. Initial development tests exposed
an integer-versus-float timestamp digest mismatch and a test incorrectly expecting
a familiarity saving with zero orientation cost; both were fixed before freezing,
and the failing log is preserved. Figure review identified an overlapping colorbar
and a plotting compatibility warning; plotting-only fixes leave outcomes unchanged.

`verification.json` records replay of every trace, official re-scoring of every
released output and ordinary atomic-engine checks. `preservation.json` and the
human-study freeze protect historical materials. No practice or participant records
were used. Reference-based simulated correct responses and explicit unsuccessful
response sentinels are not claimed as actual reviewer generations. No inference,
paid resource or unrelated service was started or changed.

## Claim-evidence boundary and next observation

| Claim | Evidence | Limit |
|---|---|---|
| The source-aware queue is the simpler supported computational alternative | All 66 cells, zero-cost identity and paired release counts | This model contains no measured visual/comprehension advantage for cards |
| Source grouping can help over FIFO when repeated orientation is expensive | Original orientation/persistence map and load/interleaving stress | Conditional operating region, not measured human task prevalence |
| Grouping can trade additional correct releases for additional errors | Fallibility and carryover panels with wrong releases retained | Reviewer rates and carryover mechanism are unvalidated |
| Saved drafts are not automatically beneficial | Matched manual construction and cost sensitivity | Relative construction/verification costs and human accuracy remain unknown |
| Simulation matches the review protocol | Event replay and exact-version scoring | Software semantics do not establish understanding or human performance |

The strongest supported contribution is a reproducible **conditional comparison
that separates source-aware navigation from grouping-card overhead**, grounded in
real tasks and actual imperfect drafts. It does not validate grouping as a human
interface improvement. Measure source orientation after consecutive/intervening
work, group-control interaction costs, detection/repair performance on these drafts,
manual construction, and unit/assumption carryover. Observe whether queue users
already adopt source-aware ordering. These observations can calibrate or falsify
the model. The existing frozen prospective study remains intact; any later design
adding a source-aware automatic-queue condition needs a separately declared version.

All six selected source-size factors clip to 0.75 (1,120-1,750 source characters),
so first-visit orientation is 0.75 times the declared S coefficient. This model
does not distinguish source-size difficulty within these approximately matched
packets. Plot labels identify S rather than mislabeling it as an actual first-visit
duration. This reporting clarification changes no frozen function or result.

Additional model limits: familiarity is evaluated when a review is selected and
held fixed for that attempt, rather than continuously during its phases. The
post-selection group overhead therefore does not trigger a second memory update.
Question-level random effectiveness is shared across policies but does not model
a common latent skill level or correlated source-level errors. Apart from declared
carryover, those sources of behavioral dependence remain unmodeled.

## Recorded verification

All 31680 simulation traces replayed, 200286 released answers were independently re-scored, and 120 selected traces matched ordinary atomic-engine replay. All 52 protected historical files remain unchanged. No human records were read.

## Stage resource accounting

The separately authorized CPU stage reached its packaging checkpoint after 43.2 minutes, within the 90-minute limit. The declared batch used 265.2 seconds of host wall time and full verification 281.0 seconds. There were zero scheduled model calls, attempts or new tokens. Five additional CPU runs checked the isolated reproduction adapter against saved objects; they are verification, not an expanded evaluation. No services were started or modified.

Calendar elapsed from the preserved original start is 82.72 hours, or 46.72 hours beyond the original 36-hour target, including previous stages and idle gaps. This is not active-compute time and the new stage is not represented as work inside that original window. Historical cumulative inference remains unchanged at 61729 actual attempts. The ledger identifies the packaging checkpoint immediately before the final commit.
