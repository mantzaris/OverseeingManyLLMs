# Evaluation of the oversight workflow

The frozen source selection and protocol were committed at `dec24be3` before fresh
collection. All 24 selected source contexts and all 145 original questions were
retained. Two generation replicas yield 290 initial answers. The six old-source
pilot calls and four predetermined rechecks bring the stage to **300 GPU calls and
300 attempts**, without retries, failed attempts or context-preflight rejection.
The unchanged server is Qwen2.5-7B-Instruct at pinned revision
`a09a35458c702b33eeacc393d103063234e8bc28`, BF16 on one RTX 6000 Ada, zero CPU offload.

## Actual answers, before simulated review

Official exact match is **61/290 (21.0%)**. Mean token F1 is
**22.61%**. Joint answer/scale correctness is **59/290**;
scale agreement alone is 212/290. There are 38 empty answers,
including unsupported outputs and parser failures, and 252 nonempty
answers. All 290 returned bodies are parseable JSON. These categories must not be
confused with the legacy formatter's stricter `valid` flag (106/290).
Optional evidence supplied as a string rather than a list accounts for
157 formatting flags; it does not erase the readable answer
or the full source. Other retained issues are {'evidence_shape': 157, 'scale': 6, 'answer_shape': 7, 'calculation_failed': 1}. No complex executable
representation is required or used to select the evaluation sample.

The context-average joint accuracy is 20.49%, with a
source-context bootstrap interval [13.89,
27.09]%. This is model/task evidence, not a user
study. Exact-match scoring can penalize a descriptive span that differs from the
annotation. The original source/question/response remains inspectable.

## Matched wall-clock software scenarios

There are 144 completed scenarios: twelve two-source bundles, two answer replicas,
three interface configurations and two constructed arrival concentrations. The
same saved outputs are used throughout. All tasks are offered at time zero; task
starts become eligible every .15 seconds (lower) or .015 seconds (higher), followed
by a .04-second delivery delay. These are compressed software test timings,
separate from measured GPU generation. The observation cutoff is 2.2 seconds, not
a financial deadline.

A scripted ideal inspection approves or corrects one question after .095 seconds,
then explicitly releases that version. The first request is deferred once for
.35 seconds. C pauses new starts from .25 to .65 seconds and can retain up to three
source-related requests. This script is common in correctness and per-question
service semantics. Its C-only pause/group controls are declared workflow actions,
not assumed human time savings. Actual recheck outputs are inserted at .8 seconds
for the predeclared replica-zero examples. A changed version requires renewed review.

| Interface | Arrivals | Offered | Correct released | Unfinished reviews | Sampled peak queue (mean) | Arrival-to-selection (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| threads | lower | 290 | 290 | 0 | 1.04 | 57.2 |
| threads | higher | 290 | 290 | 0 | 10.08 | 573.6 |
| queue | lower | 290 | 290 | 0 | 1.00 | 57.4 |
| queue | higher | 290 | 290 | 0 | 10.08 | 572.8 |
| sessions | lower | 290 | 290 | 0 | 2.08 | 116.4 |
| sessions | higher | 290 | 290 | 0 | 10.08 | 583.5 |

Every condition/load releases all 290 answers correctly only because the ideal
script supplies annotations and the cutoff is generous for its artificial service
time. **B versus C is a mechanical completion tie in all 12 paired bundles at both
loads**, with difference 0 and a degenerate script-bootstrap interval [0,0]. This
is not evidence of human equivalence. C has no measured throughput advantage.
Its pause increases the lower-load sampled queue peak by 1.083 requests on average
and approximately doubles arrival-to-selection time. At higher concentration,
all three peak queues average 10.083 requests. Queue peaks are sampled every .02
seconds. Arrival-to-selection includes resumed selections and is not pure reading
time or model latency.

No offered work disappears during pauses. `tables/pause_checkpoint.csv` audits
recorded event prefixes at .45 seconds, the midpoint of the declared pause, as a
descriptive accounting check. It is not a new favorable timing experiment. Some
work is unstarted then, while all is accounted for at the eventual cutoff. The
primary final-cutoff experiment does not test a persistently overloaded human
reviewer. Protocol fixtures separately exercise outstanding work at shutdown,
withdrawal, duplicate delivery and stale decisions.

## Measured software behavior

All **13,236 scenario events** replay to their recorded state hashes;
all 144 cutoff states and released-answer scores are independently
reconstructed. There are zero missed, duplicate or misassociated received request
IDs in the completed matrix and zero unexpected protocol/driver command failures.
All **41,722 active-snapshot comparisons** preserve the pinned output.
These repeated checks are not independent sources or human observations.

| Timing boundary | Observations | Median ms | 95th percentile ms |
|---|---:|---:|---:|
| Atomic handler | 13236 | 0.74 | 1.25 |
| Scheduled delivery lateness | 1740 | 1.15 | 2.17 |
| Browser HTTP round trip | 144 | 5.75 | 15.64 |
| State receipt to DOM update | 50 | 1.60 | 6.12 |

Handler timing includes validation and hashing. HTTP timing includes serialization
and local transport. DOM timing ends after JavaScript updates, not compositor
paint. GPU generation is separate: **459.3 summed seconds**,
211,738 prompt and 20,240 completion tokens.
Hardware, host contention and the local browser limit generality of these timings.

The live integration uses twelve initial answers from two fresh contexts, not extra
unaccounted calls. A six-second active review overlaps observed arrivals while
admission is paused for two seconds. A real recheck creates a new version; the old
approval is rejected. The demonstration leaves its 12 questions visible and
unreleased, rather than claiming a participant completed them. Of four actual
model rechecks, 1 change answer or
scale; 4 change the full prepared response.
A version change need not imply an incorrect earlier answer.

Chromium checks exercise all three real interfaces. The final release checks pass
62 assertions, including focus/typed-note stability, deferral,
resumption, separate source-session questions, stale HTTP-state rejection,
version-specific approval, explicit release, connection recovery, idempotent retries, restored journals, a timed
prospective-study cutoff, disjoint practice material and a narrow viewport. 6 browser journals replay exactly. Their metadata revisions are authored stress events,
separate from actual model revisions. Failed earlier harness runs and the resolved
software annotation-indexing error remain in the artifact namespace.

## What the comparisons do and do not establish

The software study establishes executable accounting and release boundaries on
real source material and actual model outputs. It does not establish better human
review quality, less mental demand, faster source reading, or superior ordering.
Source grouping gives an explicit navigation option, not shared correctness.
The appropriate next comparison is the prepared within-participant B/C study,
with disjoint matched packets and real quality/effort measurements. No new inference
or deeper-search study is needed to run a formative interface pilot.
