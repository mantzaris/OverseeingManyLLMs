# Overseeing many LLMs through a user-controlled review queue

## Finding

The new desk makes concurrent answers inspectable and individually releasable.
It retains active evidence during arrivals, keeps paused/deferred work in the
accounting, and requires approval for the exact current output version. It is a
working asynchronous system with a frozen real-data software evaluation. **It does
not yet demonstrate a human performance or workload advantage.**

Three configurations share one protocol: worker conversations, a central stable
queue, and optional user-controlled source sessions. No new optimizer, adaptive
acquisition policy or automatic correction reuse is introduced. The closest systems
already provide agent dashboards, steering, history and queues; the contribution
is a specific review/release workflow and its testable behavior under concurrency.

## Evidence at a glance

- 24 fresh TAT-QA source contexts, 145 original questions, two model replicas.
- 290 initial model answers; 61 exact matches and 38 empty outputs retained.
- 300 GPU attempts including development and four real rechecks; no failed attempts or retries.
- 144 matched wall-clock scenarios; 13,236 replayed events and
  41,722 successful active-snapshot checks.
- All configurations finish the ideal scripted workload. B/C completion differences
  are zero. C's pause increases lower-load queue pressure and waiting; no automatic
  efficiency advantage is supported.
- A live twelve-task demonstration, actual source displays, version examples,
  final browser checks and a prospective human protocol are included.

See [EVALUATION.md](EVALUATION.md) for exact denominators, timings, failures and tables.

## Claim-evidence map

| Claim | Evidence | Limit |
|---|---|---|
| Arrivals preserve active review and typed notes | Protocol interleaving tests, live/events.json, browser_final_verified journals | Local single-user implementation, not arbitrary external agent tools. |
| Approval is version-specific and individually scoped | Refused stale approvals, immutable version history, replay tests | Does not establish correctness of an approved answer. |
| Pausing cannot conceal offered work | Conservation invariants, pause checkpoint and accounting figure | Pausing may delay progress; it is not automatically beneficial. |
| Actual financial questions can enter one review protocol | Fresh source manifest and 290 raw model answers | Low answer accuracy and incomplete citations remain visible. |
| C improves human review over B | No evidence yet; HUMAN_STUDY.md is prospective | No participants, cognition measurements or powered efficacy claim. |
| The interface is the first oversight dashboard | Not claimed; AgentGUI/AGDebugger and earlier interruption research precede it | The novelty is limited to a specified system/evaluation package. |

## Paper framing and recommendation

The separate ICAART-format draft is `paper/oversight_workflow/main.pdf`. It centers
on inspectable concurrent work and explicit release authority. The historical
maintenance, retail, attention-session and correction-transfer manuscripts remain
unchanged. Their negative findings motivate using simple ordering, direct source
access and separate decisions, rather than being recast as support for this desk.

**Recommend a position-paper framing now.** The real-data systems evaluation is
complete, but the central user-benefit comparison has not been conducted and the
building blocks have strong predecessors. A regular-paper argument would be much
stronger after a formative pilot fixes interaction/packet issues and a prospectively
specified human comparison measures correct releases, unresolved work, resumption
behavior and perceived control. A mechanical script tie cannot substitute for that.

The smallest next step is an authorized formative B/C pilot with the supplied
source-disjoint packets and training materials. It should diagnose usability and
variance, not claim powered efficacy. No further automatic correction-transfer
algorithm is justified by the present result.

## Reproduction and accounting

`bash research/oversight_workflow/reproduce.sh` checks saved outputs/events and
regenerates tables/figures without inference. `python3 -m
research.oversight_workflow.prototype.server` runs the local desk. The exact live,
replay and manuscript commands are in README.md. Historical clocks and publication
redaction provenance are preserved. This stage adds no redaction; private evaluation
annotations are separated by code path from online sources.

The resource ledger records stage and cumulative wall time and explicitly retains
the overrun beyond the original 36-hour target. The existing GPU service is retained;
only local test servers and browser workers started for this stage are stopped.
