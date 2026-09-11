# Human evaluation protocol for review sessions

Status: protocol only. No recruitment, participants, consent collection or human
measurements have occurred. Browser logs in this package are scripted development
demonstrations. The current simulator does not establish mental workload,
frustration, reading time, human review accuracy or perceived control.

## Research question and conditions

Does an editable bounded review session with a visible opportunity-preservation
explanation help a user maintain decision quality while handling competing agent
requests? Compare **sticky EDF singleton review** with **guarded sessions**,
using identical evidence cards, expandable details, deferral controls and answer
options. The primary contrast concerns the session mechanism, not a more polished
interface versus an intentionally poor queue. Use low and high request loads,
yielding a 2 by 2 within-participant design. Fix context grouping and display
content. Retain source provenance and individual answer responsibility. Do not
propagate answers based on similarity.

A separate later presentation ablation can hide the certificate while preserving
the same schedule, but it is not part of this first study. Without that ablation,
a benefit cannot be uniquely attributed to explanatory text rather than the
session interaction. Likewise, these interfaces do not reproduce AgentLens's
mobile visual modalities or HiLSVA's complete workflow system.

## Tasks and expertise

Recruit people qualified to interpret HVAC controls and sensor summaries, such
as building-controls technicians, commissioning engineers, or relevant graduate
researchers with documented training. Record expertise before assignment. A
mixed novice/expert study would require a larger sample and a separate question;
do not dilute this focused study by claiming novices are interchangeable with
experts. An independent domain review must first verify that the selected windows
contain enough diagnostic evidence. A day-level imposed fault need not be
observable in every chosen hour. If reviewers cannot distinguish the taxonomy
from the available evidence, improve and freeze the task before recruiting the
main study, rather than interpreting failure as an interface effect.

Each participant supervises three simulated assistants presenting retrospective
sensor-window diagnoses. They retain or change each proposal, abstain, defer it,
or override a suggested session. They also maintain a simple ongoing planning
task, such as checking a short maintenance checklist, to make interruptions
observable. The secondary task must be identical across interfaces and scored
separately. No actual equipment or customer state changes. Training uses separate
source days and includes the interface, units, category definitions and a
practice deferral. Evaluation tasks and answers are not disclosed in training.

## Timing and counterbalancing

The current prototype advances an abstract clock on actions. Before participant
use, add a real-time workload driver based on calibrated reading/decision times.
Wall response time already has its own log channel; it must not be equated to a
fixed modeled service duration. Measure context-opening, decision and task-resumption
times in a blinded feasibility pilot. Freeze conservative duration predictions,
arrival rates, cutoff windows and attention budget before the main study. Do not
set timing to favor grouping. Include a low-load condition where both interfaces
can normally finish, and a higher-load condition where allocation matters.

Use four Williams-balanced condition sequences so interface and load order are
balanced. Assign disjoint source packets to the four conditions within a
participant, and rotate packet-to-condition assignments across participants.
Never present the same underlying day in both interfaces to the same person.
Analyze source-packet effects rather than treating all individual windows as
independent. Six current constructed bundles provide limited material, so a
larger study needs further independently audited recordings. Reused packets
across participants must remain identified in the analysis.

## Outcomes and logging

Predeclare **decision quality** as the primary outcome: proportion of incorrect
or unresolved diagnoses at cutoff, with abstentions and preparation failures
retained. Weighted loss is secondary because consequence weights are constructed.
Report correct decisions, harms to initially correct proposals, missed deadlines
and blocked/unresolved items separately. A reduction in review offers is not a
quality improvement.

Interaction outcomes include time to first response, active card decision time,
source-detail expansion, context revisits, deferrals, overrides, original-task
resumption and completion of the secondary checklist. Log DOM rendering and
viewport exposure separately. Neither proves that text was read. Estimate active
time with declared focus/idle rules and sensitivity thresholds; do not count a
hidden browser tab as sustained reading. Record unanswered requests and technical
interruptions instead of replacing the packet.

After each condition administer the six NASA-TLX dimensions: mental demand,
physical demand, temporal demand, performance, effort and frustration. Use the
unweighted Raw TLX mean as declared in advance, retaining all six responses and
orienting performance so higher values consistently indicate worse workload.
Do not mix weighted and unweighted scoring or treat the NASA instrument as an
objective sensor. Use the official instructions and obtain the relevant local
ethics review before deployment.
[NASA instrument and instructions](https://www.nasa.gov/human-systems-integration-division/nasa-task-load-index-tlx/).

Ask three separate exploratory perceived-control items, with consistent seven-point
anchors: "I could change the system's suggested review plan", "I knew which
requests remained unresolved", and "I retained authority over each decision".
These are custom items, not a validated combined scale. Follow with a short
interview about deferral, certificate interpretation and inappropriate groups.
This draws on interaction questions raised by AgentLens and HiLSVA, without
claiming their measures validate ours.

## Sample size and inference

No human pilot variance exists. The CPU replay's six bundle differences cannot
justify a human sample size. Determine the final size from **blinded human pilot
variance**, a meaningful quality margin and the repeated-measures design.

A feasibility pilot of 16 participants is a design-based starting point, not a
powered effectiveness study: it fills four counterbalancing sequences equally,
and under a normal variance approximation gives an approximate relative standard
error of the paired standard-deviation estimate of `1/sqrt(2*(16-1)) = 18.3%`.
Use a conservative upper confidence bound on variance because that estimate is
uncertain. Keep these feasibility participants outside the confirmatory sample
if task/interface/timing revisions occur. Otherwise any internal-pilot inclusion
requires a preregistered blinded re-estimation rule and no outcome-dependent
method changes.

Preliminarily consider noninferiority of quality with a maximum five-percentage-point
increase in unresolved diagnoses, subject to domain review of whether one extra
error per twenty decisions is acceptable. This is a proposed tolerance, not a
validated operational standard. Set the final margin before outcomes. A design
that only reduces effort while exceeding that margin is unsuccessful. Superiority
of active time can be tested only after the quality criterion, using a declared
hierarchical analysis; report the full quality/effort tradeoff regardless.

For a simple paired planning approximation,
`N = ceil((z_.975 + z_.80)^2 * SD_difference^2 / margin^2)`.
At a margin of .05, assumed paired SD values .10, .15 and .20 yield approximately
32, 71 and 126 participants before counterbalance rounding and attrition.
These are sensitivity calculations, not estimates from observed people. The
executable `sample_size.py` produces the planning table. The final calculation
should simulate the planned participant-by-source-packet mixed model using the
blinded pilot's variance components and binomial decision outcomes. Round up to
complete counterbalancing blocks; declare an attrition allowance without
replacing difficult participants or excluding slow responses.

Analyze quality with participant and source-packet effects and fixed terms for
interface, load, their interaction, order and prespecified expertise. Present
marginal paired effects and intervals. Participant-level paired bootstrap is a
sensitivity analysis; additionally examine source-cluster uncertainty if packets
are reused. Model response times on an appropriate skewed scale and report
absolute differences too. Treat perceived-control items and mechanism-specific
interaction measures as secondary, correcting or clearly labeling multiplicity.
Do not count policy runs, repeated windows or generated responses as independent
participants. A wide interval including zero is inconclusive, not equivalence.

## Governance and stopping criteria

Before recruitment: domain audit, ethics approval/consent, accessible UI review,
real-time driver, tested recording/export, predefined exclusions, task/condition
freeze and analysis registration. Participants must be able to pause or stop.
Use local pseudonymous IDs and avoid logging unrelated browser contents or
personal information. Explain that the system's certificate uses estimated
timing and is not an assurance that a diagnosis is correct.

Stop the feasibility phase for interface faults, noninterpretable tasks or
unreliable logging; preserve those outcomes. Complete the declared main sample
without extending it because an effect looks promising. No human efficacy claim
is warranted from the prototype or the current replay results.
