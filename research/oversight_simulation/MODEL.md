# Computational oversight model, frozen before comparative runs

This is a computational simulation on real-source inputs. It is not a participant
study, investigator practice, a calibrated model of financial analysts, or a new
LLM experiment. Human-study code, records, declarations and manuscripts remain
unchanged. No questionnaire, consent record, human identifier or quotation is
created. All new records carry `record_kind: computational_simulation` and scenario
and simulation-run identifiers, with a schema distinct from human exports.

## Questions, inputs and comparisons

When does arranging review around a common source improve correct releases within
a time budget? Does that remain true against an equally source-aware conventional
queue? Do these particular saved drafts help relative to manual construction?

Inputs are the matched study's 36 original TAT-QA questions, six real financial
report table/text contexts, three packets and genuine replica-0 drafts. Seven
initial drafts are joint-correct and five have empty/unsupported displayed fields.
The same uniform pilot projection is retained; no questions, errors or references
are rewritten. Sources and benchmark questions are real material; the assignment
of independently prompted task workers, arrivals and reviewer behavior are
constructed. Rotations are not independent sources, people or organizations.

Each question is a distinct goal, offered once per simulation. Lower load uses a
public prefix of three questions per source. Higher load unions existing packets,
without duplicating questions or inventing additional utility. Original conditions
run each of the three twelve-question packets under every policy and common seed.
This balances the original packet rotation without pretending to simulate people
or sequential within-person learning. Stress rotations order the same packet pool;
they are correlated configurations, not new source cases.

Policies receive only already arrived request IDs, actual source IDs, arrival
order and pending/deferred status. No future arrival, outcome draw, annotation or
correctness flag is passed to a selector. There is no explicit financial deadline.
Every policy has the same exact-version correction, approval, release and deferral
authority. Requests arriving during review cannot preempt the active output.

| Policy | Public next-request rule |
|---|---|
| Q | FIFO by receipt time, then stable question ID; ordinary central queue |
| G | FIFO starts a bounded source session of up to three currently available requests; finish that set, then return to FIFO; charge card/session overhead when at least two join |
| Q-source-aware | Exactly G's bounded selection rule and information, without source cards or their overhead |
| Q-sticky | Stay with the last source while any eligible request from it exists; otherwise FIFO |
| M | Q's FIFO navigation and manual answer construction, no model draft |

No policy deliberately waits to assemble a group. G's modeled reviewer uses the
optional grouping feature whenever an eligible group exists. This is an assumed
strategy, not observed feature uptake or an optimal use of optional controls.
Q-sticky tests a simpler unbounded source run. Q-source-aware is the critical
interface control: grouping receives no exclusive familiarity or accuracy benefit.
M's interaction/release overhead is the same as assisted policies.

## Shared timing model

A review consists of sequential phases, in simulated seconds:

`grouping (G only, if used) + source orientation + question interpretation
 + verification (nonempty assisted draft) + construction (when needed)
 + decision interaction + release interaction (if approved)`.

There is no separate switching charge that would count orientation twice. A
previously unseen source costs `S * source_size_factor` to orient. For a seen
source, orientation costs

`S * source_size_factor * [r + (1-r)*(1-exp(-gap/tau - intervening/kappa))]`.

Here `r=0.1` is the recent-source residual fraction. `gap` is seconds since the last
completed review decision on the source, and `intervening` is the number of other
completed review decisions since then. A completed failed construction can still
refresh familiarity. Consecutive reviews, including singleton Q reviews, get the
same reuse. Idle time can erode it. `tau` and `kappa` are persistence assumptions,
not inferred cognitive measurements. Source size is public character count divided
by 3,200 and clipped to [0.75,1.25].

Question/verification/construction phases have a public wording factor
`1 + min(40, word_count)/80` and mean-one lognormal time jitter, sigma 0.2.
Jitter and outcome uniforms are keyed by seed, original question ID, attempt and
component, independently of policy and execution order. The same draws are reused
across all conditions as far as different trajectories permit. There is no model
confidence, benchmark answer type or gold derivation in this timing factor.

These analyst-selected values span possible operating regions. No seconds or
probabilities below are measured reviewer parameters:

| Component | Reference setting | Declared sensitivities |
|---|---:|---|
| Unfamiliar orientation S | 25 s | 0, 5, 25, 75 s |
| Persistence tau / kappa | 600 s / 8 decisions | 45 s / 2; 600 s / 8; effectively persistent 10^12 / 10^12 |
| Question interpretation | 8 s times wording/jitter | Held common |
| Draft verification | 18 s times wording/jitter | 8, 18, 40 s |
| Detected-error construction | 45 s times wording/jitter | Held common |
| Manual/empty-draft construction | 45 s times wording/jitter | 20, 45, 90 s |
| Individual decision + release | 2 + 2 s | Held common |
| G group interaction | 4 s per opened group | 0 and 12 s |
| Deferred retry | Eligible after 45 s | Maximum two attempts per question |

Failed/unfinished review consumes the phases actually reached. A review crossing
cutoff charges only its elapsed phases and remains unfinished. An approval before
cutoff followed by release after cutoff is not a release. Completion exactly at
cutoff is accepted. Arrivals and starts at the same time are processed before the
next selection; all offered tasks remain accounted for, including never-started
ones. Release time is separate from approval time.

## Fallibility and authority

The simulated response environment has evaluator annotations. Scheduling does not.
Reference information defines **simulated** correct constructions at completion;
it is not a fallible model generation or a human response. An unsuccessful
construction uses an explicit simulation sentinel, never an invented financial
record. Unchanged wrong drafts remain the actual saved draft.

| Reviewer setting | Detect wrong draft d | Correct detected error c | Damage correct draft h | Correct manual answer m |
|---|---:|---:|---:|---:|
| Ideal | 1 | 1 | 0 | 1 |
| Higher effectiveness | .85 | .85 | .02 | .75 |
| Limited effectiveness | .55 | .60 | .08 | .50 |

A nonempty correct draft is approved unless the harm draw triggers a wrong
correction. A nonempty wrong draft is approved when undetected. Detection adds
construction time; success supplies that question's reference answer/scale only.
Empty drafts and M use the manual construction pathway. On an unsuccessful
construction, half the cases recognize inability and defer, then reject if the
second attempt fails similarly. The other half approve an incorrect simulated
answer. Recognized failure is an explicit additional assumption; the model does
not assume all errors can be detected. Deferral retains the original version.

In stress conditions, a review directly following a different question from the
same source can spoil an otherwise correct output with probability 0, .08 or .20.
This carryover hazard applies equally to Q, G, both source-aware queues and M.
It is not inferred from similarity or measured from people. The same-source event
can occur in every policy. A source session never authorizes one answer for all
questions. Error probabilities are analyst choices independent of the actual
LLM's low benchmark accuracy. Outcome draws are conditionally independent by
question/attempt; no population-level skill distribution is inferred.

## Matrix, selection and accounting

`design.json` declares 66 cells, three packet rotations, 32 Monte Carlo seeds
10000-10031 and five policies: **31,680 runs**. Seeds 0-3 are development throughput
checks, not comparison evidence. The preliminary 64-seed design was reduced before
comparative outcomes because its conservative CPU forecast was 40 minutes for
collection alone. The chosen 32-seed matrix preserves every parameter cell and
allows replay, analysis and reporting within 90 minutes. Both forecasts/declarations
are retained. No setting is selected for favorable generated answers or results.

- Original workload: 24 cells crossing orientation 0/5/25/75, three effectiveness
  levels and short/long persistence, each with 12 questions, 540 s and the exact
  matched schedule `[0,4,8,12,16,20,180,184,188,192,196,200] + 0.25 s` delivery.
- Demand stress: 6/12/24/36 offered questions crossed with 270/540/900 s capacity,
  using two waves and interleaved sources.
- Arrival stress: 24 questions, 540 s; two waves, simultaneous burst, or spread
  over 0-480 s, crossed with interleaved or source-blocked source order.
- Group cost: 5/25/75 s orientation crossed with 0/12 s group overhead.
- Task cost: 8/18/40 s verification crossed with 20/45/90 s manual construction.
- Carryover: short/long/persistent memory crossed with 0/.08/.20 carryover.

All stress cells otherwise use the higher-effectiveness reference. Stress
combinations are specified subsets, not an exhaustive factorial or a distribution
of real workloads. Repeated reference settings in different families are retained
for transparent panel comparison, not counted as independent evidence. The batch
checks the final 20-minute analysis reserve between complete parameter cells; any
unrun declaration would be reported rather than replaced by another seed.

## Outcomes, uncertainty and break-even reasoning

Report correct current-version releases, incorrect releases and unfinished goals
separately. Also report phases of time, source switches/returns, deferrals/retries,
initial errors repaired, previously correct answers damaged, and waiting for other
sources. Unrelated-wait time is summed across tasks and can exceed session duration;
it is a task-wait measure, not the user's time. A low-load all-complete tie is lack
of capacity competition, not statistical equivalence.

Within a cell, average the three paired rotation differences for each random seed.
Across the 32 independent seed blocks report mean, Monte Carlo standard error and
mean +/- 1.96 SE, plus seed-block signs/ties and raw rotation outcomes. This normal
MC interval approximates numerical uncertainty conditional on fixed sources/model,
not uncertainty about a human population. Some cells are deterministic or have
boundary-heavy distributions; retain exact signs/raw outcomes. Model uncertainty
is represented by the parameter grid, and does not shrink with more seeds. Do not
pool all cells into a global effectiveness estimate.

For a fixed set and order-dependent orientation, an explanatory time balance is
`net saved time = orientation_Q - orientation_G - groups_G * group_cost` when the
other work/outcome phases are equal. Saved time helps correct completion only if
it crosses an additional task's full decision-and-release time, without introducing
harm or delaying a valuable unrelated answer past cutoff. Different repair paths
add construction/deferral costs, so report their decomposition too. This is a
model-based accounting identity under its conditions, not a cognitive law.

At zero group cost, G and Q-source-aware have identical selection, familiarity,
random inputs, phase durations and outcomes by induction over event times. This
structural identity is a model check, not an empirical discovery. At positive group
cost and a fixed common sequence/outcome path, G adds overhead and cannot finish
that sequence sooner. In the general arrival-dependent case, delays can change
eligible groups, retention or the completed subset, so no blanket dominance theorem
is asserted. No simulation establishes that real grouping cards lack a benefit;
any comprehension or behavioral benefit beyond navigation is unmodeled and requires
observations. Q-sticky tests the separate ordering explanation.

## Implementation and preservation

Discrete events reuse the existing Desk `_apply` transitions and invariants. A
simulation-specific origin marks corrections and every decision's actor is
`simulated_reviewer`. Bulk runs omit per-event deepcopy/hash profiling; full-engine
Desk.command replay validates selected traces. Every run saves compact command and
phase traces plus a final-state digest and summary. Sources/drafts are referenced
by original IDs to avoid duplicating entire tables in every event. No human export
schema is generated. Saved simulation traces are rejected by the human pipeline.

Selectors use O(n log n) sorting per choice. There are at most two review attempts
per question and O(n) exogenous starts/arrivals. The existing invariant checks may
cost O(n^2) per transition; n is at most 36. Deterministic replay retains version,
cutoff, failure, unfinished-work and information-boundary checks. Neither protocol
invariants nor a successful simulation establish answer comprehension.
