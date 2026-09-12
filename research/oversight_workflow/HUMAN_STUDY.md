# Prospective human evaluation: protocol and materials

**Status: prepared, not conducted.** No participants have been recruited, contacted
or simulated. Browser scripts are software tests. Before recruitment, an
appropriate human-subjects review, consent, compensation, data management and
institutional responsibility must be established by the investigators.

## Question and contrast

Does optional source-based review with admission control help people release more
correct financial answers in a fixed session than the strong central queue?
Primary contrast: C versus B. Both preserve active review, source access,
version-specific approvals, individual decisions, deferral and complete offered-work
accounting. C adds bounded source sessions and visible admission controls. This is
a workflow-bundle comparison. A (separate conversations) is retained as a contextual
prototype, not added to the primary factorial study.

## Participants, task and expertise

Recruit adults able to read English tables and perform basic percentage and
difference calculations. Record accounting/finance experience, quantitative
training, familiarity with LLM tools and corrected vision needs. A financial
license is not required for these benchmark questions. A short practice check
establishes whether instructions, units and the interface are understood; do not
exclude after observing condition outcomes. Prospective exclusions are inability
to complete consent or practice after standardized assistance, not low financial
accuracy. Accessibility accommodations must be recorded.

The user supervises three labeled task workers answering original TAT-QA questions.
Each output is a generated answer, optional explanation and full source table/text.
They may approve and release it, enter their own correction then release it,
reject, or defer. They may use a standard calculator in every condition. Source
annotations and offline scores are unavailable during a scored session. A rejected
answer is blocked, not a correct completion. A deferral or unstarted task remains
unfinished. The task asks for answer quality, not investment advice.

## Within-participant design

Four 12-minute sessions cross interface B/C with lower/higher arrival concentration.
All contain the same number of offered original questions for their assigned
packet; distinct question counts are included in the outcome denominators. Lower
load releases model outputs progressively across the session. Higher load presents
the same packet in three short bursts. Exact intervals are selected in a formative
pilot and frozen before an effectiveness study. The offered task list is visible
at time zero in both conditions. Pause delays starts, never removes tasks.

`study/packets.json` partitions the 24 source contexts into four disjoint six-context
packets using public source length and question count, before any participant data.
Each participant sees each packet once. The assignment file records the complete
counterbalance. Conditions 0..3 = B/lower, C/lower, B/higher, C/higher. Four balanced
Williams orders are 0-1-3-2, 1-2-0-3, 2-3-1-0 and 3-0-2-1. Four packet rotations
cross these orders, producing 16 assignment cells. Disjoint source contexts avoid
answer-memory carryover. Across participants, every packet appears in every
condition and period. No packet is selected because C performs well on it.

All conditions share replica-zero answers. Replica-one may replace the entire
answer set in a separately balanced block if the formative pilot finds it useful;
that decision precedes confirmatory data. The main protocol has no artificial
answer errors. Predetermined real model revisions can be a separately declared
secondary task, rather than surprising participants with unknown injected errors.

## Session procedure and training

1. Consent and background questionnaire, with recording scope stated explicitly.
2. Standard explanation of generated answers, source units, separate decisions and
   explicit release. Demonstrate approve, correction, rejection and deferral.
3. Practice on the old development context in `study/training.json`, not any scored
   packet. Demonstrate an arrival while a note is being typed and a version change.
4. Two comprehension checks: approval does not release a future revision; rejecting
   an answer does not count as completing it correctly. Explain mistakes once.
5. Four counterbalanced 12-minute scored sessions, separated by at least two-minute
   breaks. Give the same task instruction before each: “Review the evidence and
   release as many correct answers as you can. Keep uncertain work visible rather
   than approving it merely to clear the queue.” No think-aloud during timed tasks.
6. After each session, raw NASA-TLX items and perceived-control questions. Optional
   retrospective interview after all conditions, using evidence-linked events.

The facilitator must not reveal answers, suggest an ordering policy, or tell users
that grouping should help. Use the same equipment and browser viewport. Report
training duration, technical failures, interruptions and accommodations.

## Outcomes and analysis

Primary: proportion of all offered questions ending with a current-version correct
released answer, with exact match and scale evaluated consistently. Also report
absolute correct releases. Prespecify a human adjudication procedure for semantically
correct spans missed by automatic exact match; adjudicators should be blind to
interface and retain the original official scores. A blocked or unfinished answer
is not a correct release.

Co-primary safety description: incorrect approvals and incorrect releases separately,
including stale-release attempts blocked by the common guard. Secondary: unresolved
questions, unstarted work, corrections, source revisits, deferrals, resume-to-decision
time and interface action latency. Active review time is an interaction measure
from select-to-action with visibility interruptions reported separately. It is not
assumed to be continuous reading. Source focus/scroll events are evidence visits,
not eye tracking. Report session totals as well as per-completed-item measures to
avoid rewarding omission of difficult work.

NASA's [Task Load Index](https://www.nasa.gov/human-systems-integration-division/nasa-task-load-index-tlx/)
measures reported mental demand, physical demand, temporal demand, performance,
effort and frustration. Use the unweighted raw six-item mean and retain each item;
label it Raw TLX, not the original pairwise-weighted score. Performance is anchored
from perfect to failure so higher values consistently indicate burden. Three
custom 1-7 agreement items assess knowing what remains, control of release, and
ability to return to deferred work. Analyze them separately; do not claim a
validated combined control scale. Wording and anchors are in `study/questionnaires.json`.

A prospective mixed-effects model includes interface, load and their interaction,
period and packet, with participant and source-context intercepts. Check whether
these random effects are estimable for the eventual sample. A transparent fallback
is paired participant-level differences stratified by load with source-packet
sensitivity. Questions, clicks and repeated arrivals are not independent people.
Report intervals and individual trajectories, not only p-values. Confirmatory
comparison and failure/exclusion rules must be registered before data collection.

## Sample size and pilot decision

There is no human pilot variance yet. Therefore no powered sample size is asserted.
A formative pilot should fill enough counterbalance cells to diagnose the interface,
fatigue and packet difficulty; 8-16 consenting participants is a feasibility range,
not an efficacy calculation. It may establish timing, missingness and an uncertainty
range for within-participant differences. Its data must remain development evidence
if the interface or timing is subsequently changed.

Before a confirmatory study, choose a substantively meaningful difference in correct
release proportion, not a margin tuned to favorable pilot effects. Estimate the
paired variance and source clustering with uncertainty. Simulate the planned mixed
model over the 16 assignment cells. As a check, a paired-normal approximation is
n ≈ ((1.96 + .84) SD_difference / target_difference)^2. For SD=.15 and a declared
.05 difference it gives about 71 completers before clustering/attrition and
counterbalance rounding. This is an illustrative calculation, not a power claim.
A noninferiority design would additionally require a justified error margin and
one-sided inference; a nonsignificant accuracy difference is not equivalence.

## Review and data management checklist

Obtain ethics determination and authorized consent text, decide compensation and
withdrawal handling, test accessibility, and minimize recorded personal data. Use
pseudonymous participant codes. Logs contain task/source IDs, versions, displayed
state, actions and timestamps; typed notes may contain personal text and need review
before sharing. Do not collect unrelated browser content. Store identifiable consent
separately. Define retention, de-identification and access controls before recruitment.
No such approval, consent or actual observation is claimed by this repository stage.

## Ready-to-run preview links

With the local desk server running, a facilitator can open, for example:

```
http://127.0.0.1:9041/?study_packet=0&condition=queue&load=lower
http://127.0.0.1:9041/?study_packet=1&condition=sessions&load=higher
```

These are explicitly previews, not participant sessions. Setup controls are hidden
from the timed view. Provisional lower-load offsets span 94% of a 720-second
session. Higher-load offsets use three bursts beginning at 0, 240 and 480 seconds,
with one second between eligible starts inside each burst. No artificial answer
errors are added. These exact preview values must be accepted or revised using
formative evidence before confirmatory collection. The timer closes approval and
release at the session cutoff and preserves all outstanding tasks; in-flight
results may still arrive. The metadata file records the packet, load, duration and
start offsets. The query parameter `seconds` permits a short software test of the
timer, not a human workload manipulation inferred from model speed.

Practice is executable at `http://127.0.0.1:9041/?training=1`. It uses the two
old-source questions specified in the training file and actual pilot answers.
An explicitly labeled same-answer/new-version fixture demonstrates why a prior
approval cannot release a revised artifact. The first question is explanatory;
the second is a direct table lookup. Use the same facilitator script in B and C.
