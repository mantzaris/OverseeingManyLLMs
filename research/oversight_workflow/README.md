# Decision desk for concurrent agent work

**New matched comparison:** [Q/G/M with equal twelve-question, nine-minute blocks](matched/README.md).
Grouping is isolated from admission control, and source-only work now has matched
allocations. No participant comparison has been performed.

**Preserved handoff:** [position paper, frozen formative pilot and Alex's walkthrough](handoff/README.md).
The compact pilot replaces no historical results and has no participant observations.
Its source-only diagnostic is separate from the older effectiveness-study proposal.


Review actual model answers beside their original financial source. Keep a request
in focus while others arrive, defer it with a note, optionally inspect related
questions together, pause new task starts, and approve/release a specific version.
A revised answer requires another review. Source grouping never applies one answer
or approval to another question.

This is the active ICAART paper direction. [REPORT.md](REPORT.md) describes the
supported systems contribution and its limits. The [conference draft](../../paper/oversight_workflow/main.pdf)
is separate from every historical manuscript. Human effectiveness is unmeasured.

## Formative B/C pilot preparation

The [pilot package](pilot/README.md) adds investigator setup, compact counterbalanced
packets, a source-only feasibility check, calculator, forms and offline analysis.
Its [answer audit](pilot/AUDIT.md) preserves the low historical scores and diagnoses
why task feasibility needs testing. No participant observations are supplied.
This formative-v1 package remains preserved; the matched comparison above is the
new investigator preview. Institutional determination
and consent preparation remain necessary before collection.

## Quick start: no inference

From the repository root:

```bash
python3 -m venv .venv-workflow
. .venv-workflow/bin/activate
python3 -m pip install -r research/oversight_workflow/requirements.txt
python3 -m research.oversight_workflow.prototype.server --port 9041
```

Open **http://127.0.0.1:9041**. Choose A, B or C and “Saved answers, live arrivals”,
then start a packet. These are actual saved Qwen answers delivered by a real-time
background driver. The arrival spacing is an explicit demonstration setting,
not recorded human or GPU speed. The full source remains available for incomplete
answers. The default first packet has two sources and twelve original questions.

### Short walkthrough

1. Choose **C · Review sessions**, packet 1, and start the saved-answer workload.
2. Select the first arriving financial question. Type a note. As more answers
   arrive, the source, answer and text field remain in place.
3. Choose **Keep up to three related requests together**. Compare their separate
   answers beside the source. Finish or defer each question separately.
4. Pause new tasks. In-flight tasks still deliver results; not-started tasks remain
   counted. Resume to admit the rest.
5. Defer a question, then select it again. Its note, source and prior draft return.
6. The first packet has a predetermined actual model recheck at 18 seconds. If its
   earlier version is active, a warning appears. Approving that old version is
   refused. Refresh to review the new draft. It may retain the same answer.
7. Approve an answer and then explicitly release its version, or enter your own
   correction. Rejecting blocks an answer and is not a correct completion.

The UI contains no annotation-reveal button. Users inspect the source or type their
own corrections. Ideal reference-based actions occur only in separately labeled
software scripts. The first-source example includes both correct lookups and an
incorrect generated average; do not assume all displayed answers are correct.

## Reproduce the saved study

```bash
bash research/oversight_workflow/reproduce.sh
bash paper/oversight_workflow/build.sh
```

The first command verifies requests, prepared outputs, logical events, cutoff
accounting and scores, then regenerates tables and vector/PNG figures. It needs no
GPU or external dataset download. The compact evaluator-only annotation projection
is included for this purpose and is not imported by the online desk. The second
command requires a LaTeX installation with the ordinary packages used by the
unchanged official SCITEPRESS template.

To remeasure software timing rather than replay recorded measurements:

```bash
# This writes a new timing run and never replaces the published scenarios.
python3 -m research.oversight_workflow.evaluate --output-dir /tmp/workflow-timing-rerun
node research/oversight_workflow/prototype/browser_check.mjs /tmp/workflow-browser-check
```

Chrome at `/opt/google/chrome/google-chrome` and Node 22 are used by the supplied
browser harness. The server must already be running on 9041. This is scripted
software testing, not a participant study. Saved logical replay is deterministic;
fresh timings, generated answers and PNG/PDF metadata are not asserted bitwise
identical.

## Live mode and generation

The live adapter uses the existing authorized local forwarding endpoint 8021 and
pinned GPU service. It never starts a replacement model server. The stage-specific
`authorization.json` enforces the inference cutoff and call/attempt ceilings.
Cached completed requests can be read after cutoff. Fresh generation requires a
valid separately authorized configuration; historical authorization is not reset.

Within the recorded stage authorization, “Live GPU workers” sends independently
prompted task jobs through the same protocol. GPU requests are serial; the user
interface and task workers remain asynchronous. The saved twelve-task live
integration is in `artifacts/oversight_workflow/live/`.

Exact collection command (the frozen stage has already completed):

```bash
python3 -m research.oversight_workflow.collect
```

A completed collection refuses to overwrite its live evidence. Fresh collection
should use a new declared artifact namespace and authorization. Do not rerun the
original as though it were a new independent source sample.

## Study and adapter

[API.md](API.md) documents task submission, statuses, exact-version decisions,
local journals and restore. [HUMAN_STUDY.md](HUMAN_STUDY.md) supplies the prospective
B/C comparison, counterbalancing, training, outcomes and analysis. Public-source
packet assignments and questionnaires are under `study/`. A six-context packet
can be previewed with `POST /api/start` and `study_packet: 0` through `3`; this does
not create participant observations. Timing and consent arrangements must be fixed
before any authorized human evaluation.

Sources and construction are documented in [DATA.md](DATA.md), the protocol in
[METHOD.md](METHOD.md), and measurements in [EVALUATION.md](EVALUATION.md). The final
resource ledger counts all 300 GPU calls, without resetting historical clocks.
No human workload or cognitive-load reduction has been measured. The current
recommendation is a position paper and an authorized formative user pilot.

### Prospective study practice

Open `http://127.0.0.1:9041/?training=1` to practice on two previously inspected
development questions and their actual pilot answers. They are disjoint from the
24 scored sources. A same-answer version event after 18 seconds is explicitly
labeled as a training fixture. It illustrates version authority without inserting
a false financial answer. The facilitator instructions and questionnaires remain
prospective materials; this preview does not collect or assert participant data.

After final closure, the stage transport rejects new calls even if its original
cutoff has not yet passed. Exact cached requests remain readable without rewriting
their timing evidence. This keeps later use from silently changing the completed
stage's ledger. A future authorized collection needs its own namespace and clock.
