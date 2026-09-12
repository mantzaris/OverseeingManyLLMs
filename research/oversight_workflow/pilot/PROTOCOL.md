# Formative pilot v1

Status: prepared, no participant observations. This compact protocol specializes
[the existing prospective study](../HUMAN_STUDY.md); it does not replace the
historical systems evaluation or its position-paper framing. No recruitment,
contact, consent or institutional authorization is asserted.

## Question and design

Can investigators run understandable financial answer-review tasks, collect
interpretable B/C interaction records, and identify whether drafts assist review
or require substantial reconstruction? The pilot diagnoses usability and
measurement variability. It is not a powered test of interface superiority.

Each run has separate-source training (up to four minutes), two nine-minute review
blocks, and one four-minute source-only diagnostic. Forms and short breaks follow
the blocks. Allow roughly 35–45 minutes including instructions, forms and discussion;
this is an investigator planning allowance, not measured participant capacity.
The code does not impose a break length; record major deviations in the facilitator
log. Do not coach scored answers or change features during collection.

| Common to B and C | Additional in C |
|---|---|
| Original source, fixed replica-0 answers, scale and explanations | Optional source session of at most three requests |
| Calculator, notes, manual selection and conventional chronological next request | Session members prioritized by Next when pending |
| Stable active artifact; individual approval, correction, rejection and deferral | Shared-source cards with distinct answers and decisions |
| Separate exact-version release, complete offered-work counts | Pause/resume new task starts; in-flight work continues |
| Same clock, arrival schedule, source access and questionnaires | No automatic answer/correction propagation |

This is a **workflow-bundle B/C comparison**. A difference cannot be uniquely
attributed to grouping or admission control. Both controls are logged to diagnose
what was used. Waiting-age labels and all pending work remain visible in B too.
There is one arrival pattern, not an interface-by-load factorial. No new priority,
business deadline, synthetic answer corruption or adaptive scheduler is added.

## Frozen public packet selection

`materials.py` reads only the existing public source manifest. Among the 24 original
contexts, retain those with six questions, at most 60 table cells, at most seven
columns, and at least one question containing the declared arithmetic wording.
Sort by public source-character count with source-index ties and start at the
central-six lower index. Scan forward for six sources, skipping any later source
with the same public basic/diluted earnings-per-share definition question. Among
the 15 possible pairings, minimize the range of arithmetic-wording counts, then
the range of source-character lengths, then source-index ties. This gives three packets, each with two sources
and 12 original questions. Six questions for each source-only variant are selected
by taking the first non-arithmetic, first arithmetic and first remaining question
per source. Model accuracy and gold answers are not inputs to selection.

`manifest.json` records exact IDs, all exclusions implied by this rule, source
complexity and all 18 assignments. The table-size threshold was settled during
software preparation, before packet scoring or any participant outcomes. The first preparation packets were audited. A later public-text check found two
distinct sources asking the same basic EPS definition. The duplicated source was
excluded and packets rematched on public complexity, before any participant
outcomes. Both earlier software dry runs and their declarations are retained.
The final selection did not use draft correctness; its separate audit follows selection. Public lengths are 3,344,
3,144 and 3,240 characters; cell counts are 57, 69 and 57 per two-source packet;
arithmetic-wording counts are 7, 6 and 6. These are coarse matching proxies, not
established equal difficulty. All source contexts are reused benchmark material
already inspected in this repository, not new held-out sources. Previous use is
allowed for this prospective human pilot but must be disclosed.

Training uses the existing two-question development packet, disjoint from all six
scored contexts. Each person encounters each scored source in only one condition.
The 18 assignments cross all six permutations of B/C/S order with three packet
rotations. Across the complete schedule, interface, position and packet balance.
With fewer runs balance is necessarily incomplete. Use a pre-recorded subset of
assignment IDs covering both B-first and C-first orders and varying S position.
For an initial six-run schedule, IDs 0, 3, 7, 11, 13, 17 cover each order once and balance each condition-by-packet
and position-by-packet count at two. This does not establish equal task difficulty. Do not select
assignments in response to outcomes. Reuse a fresh assignment list for a subsequent
development version.

All 12 B/C tasks are **offered at start**. Replay starts are at 0,4,8,12,16,20,
180,184,188,192,196,200 seconds, alternating sources; three simulated task workers
share saved outputs. A 0.25-second driver delay separates start and arrival.
Source-only starts are 0,4,8,12,16,20. Pausing may delay starts but cannot remove
them from the denominator. These times are constructed workload parameters,
unrelated to observed inference latency or human reading time. No inference runs.

## Instructions, scoring and feasibility

Use the exact original questions and full source. Keep missing/wrong model answers
visible. Allow writing, rejecting and deferring. Do not provide gold answers,
scores, audit notes or hints during scored blocks. The source-only block uses the
same decision protocol, but starts with no proposal. Writing an answer creates
and approves a user version; explicit release is still needed. A rejection is a
blocked request, not a completed correct answer.

Primary formative descriptions: correct current-version releases (joint criterion: official answer EM equals one and the scale matches), incorrect releases and all unfinished deliverables in each
B/C block. Report official answer EM and token F1 alongside joint correctness,
separately from additional adjudication. Approval without release is recorded
separately, including incorrect approvals. Retain unstarted tasks, unresolved
requests, rejected work, partial runs, failed commands and incomplete forms.

Secondary descriptions: correction attempts and successful/harmful released
corrections, select-to-action elapsed intervals, resumed intervals, source-focus
revisits, deferrals, grouping, pause/resume, calculator use and visibility/focus
events. An elapsed interval is **not continuous reading time**. A focus event is
not evidence the source was comprehended. Background browser disconnection does
not stop the clock. The server enforces cutoff before handling an action; a late
approval or release is refused and logged. In-flight deliveries may still be
retained after cutoff, without authorizing release.

The source-only diagnostic examines feasibility and manual completion on disjoint
but publicly matched sources. It has fewer questions and less time, so absolute
throughput is not an assistance-effect contrast. Describe correctness, attempted
questions, elapsed interactions and qualitative reconstruction reports by block
position. Balancing order limits systematic order confounding; a tiny, incomplete
schedule cannot eliminate it. Do not interpret a null difference as equivalence.

## Analysis and decision rules

The participant is the B/C paired unit. No clicks, questions, model outputs or
policy replays become independent participants. Use all offered tasks for completion
proportions, and show incorrect releases both as counts and among released answers.
The command exports participant-level counts and paired C-minus-B descriptions,
individual trajectories and missing-block flags. It gives no interval for fewer
than six complete, nonwithdrawn pairs. Above that threshold, a 2,000-resample
participant bootstrap with seed 92741 is descriptive and conditional on these
reused packets. It does not estimate generalization across independent financial
reports. Show order/packet imbalance and individual results; do not fit an elaborate
mixed model or make superiority/noninferiority claims from this formative sample.

The six threshold is a reporting convention, **not a power calculation**. Choose a
small initial formative tranche through the institutionally authorized plan and
resource constraints; the six-run assignment example is logistical, not a claim of
adequate precision. Review task comprehension, empty-draft burden, correction
accuracy, resumption failures and measurement variation after the tranche. If users
mainly reconstruct answers, prioritize better task/draft feasibility before an
effectiveness study. If controls are unused or confusing, revise the workflow as a
new version and repeat development. A later powered design needs an explicit
worthwhile effect and variance estimates, allowing for both participant and source
dependence. No automatic enlargement based on a favorable pilot is authorized.

## Questionnaires and human boundary

Reuse six Raw NASA-TLX ratings, 0–100, with performance anchored perfect to failure.
The unweighted mean is computed only if all six items are present. Missing items
stay missing. The three 1–7 perceived-control items remain separate custom items,
not a validated combined control/workload scale. NASA's instrument and supporting
materials were checked at the [official TLX page](https://www.nasa.gov/human-systems-integration-division/nasa-task-load-index-tlx/)
on 2026-09-12. This implementation is a numeric web presentation of the existing
Raw TLX materials, not a claim that its form has been independently validated.

No participant data exists in this package. `test_data` contains explicitly marked
software fixtures, with blank questionnaire responses; practice is separately
marked. A future participant launch requires a documented investigator authorization
record and consent procedure. That local record is an operator attestation, not
institutional review performed or certified by this software.
