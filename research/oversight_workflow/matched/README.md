# Matched Q/G/M comparison: matched-qgm-v1

This is a **new prospective comparison**, separate from `formative-v1`. It tests
whether optional shared-source review increases correct releases within a fixed
period, and whether the saved drafts provide assistance relative to source-only
work. No participant results have been collected or analyzed for this version.
The existing position paper remains unchanged.

All three conditions offer **12 original questions in nine minutes**. Q is the
central queue. G adds optional same-source cards and source-aware Next. M uses
Q's navigation without drafts or generated explanations. Admission controls are
disabled in all conditions. This removes the two allocation/treatment confounds
in the earlier pilot without replacing the review protocol.

## Inspect and practice

From the repository root, using the existing Python environment:

```bash
python3 -m research.oversight_workflow.matched.freeze
python3 -m research.oversight_workflow.matched.server --port 9043
```

Open <http://127.0.0.1:9043>. The default is **investigator practice**. Choose a
pseudonymous code and assignment in the setup screen, complete training, then
follow the three assigned blocks and forms. Export using **Download session
package**, or, on this local machine:

```bash
curl --fail http://127.0.0.1:9043/pilot/export -o /tmp/matched-practice.pilot.json
python3 -m research.oversight_workflow.matched.analysis \
  /tmp/matched-practice.pilot.json --kind investigator_practice \
  --out /tmp/matched-practice-analysis
```

Practice is development evidence, not a participant result. Stop this server
with Ctrl-C. It binds only to loopback, performs no inference, and uses a different
port and export namespace from the preserved formative-v1 preview on 9042.
For remote access use an authorized SSH connection with local forwarding of
`9043:127.0.0.1:9043`; do not publish the service or open firewall ports.

## Investigator handoff

Read [PROTOCOL.md](PROTOCOL.md), [INVESTIGATOR.md](INVESTIGATOR.md), and
[ANALYSIS.md](ANALYSIS.md). [INTERVIEW.md](INTERVIEW.md) is a neutral retrospective
script. [CLAIM_DECISIONS.md](CLAIM_DECISIONS.md) connects possible observations to
permitted claims. [REPORT.md](REPORT.md) records preparation results only.

The responsible investigator must register an authorized first tranche and its
assignment schedule **before collection**. This repository supplies no approval
or participant consent. The existing authorization checklist remains applicable;
the changed matched design must be covered explicitly. Do not import old practice
or formative-v1 observations into this comparison.

## Saved software-check reproduction

```bash
python3 -m unittest research.oversight_workflow.matched.tests.test_matched -v
python3 -m research.oversight_workflow.matched.analysis \
  artifacts/oversight_workflow/matched_preparation/test_data/complete_fixture.pilot.json \
  --kind software_fixture --out /tmp/matched-software-analysis
```

The fixture uses literal scripted answers and blank questionnaires. Its shortened
clock checks the machinery, not human performance. No participant figures are
produced from fixtures or practice. A browser recheck, if needed after a concrete
change, is documented in `EVIDENCE.md`; it is not needed for saved-output analysis.

## Future genuine observations

```bash
python3 -m research.oversight_workflow.matched.analysis \
  /private/authorized-matched-exports --kind participant \
  --out /private/matched-analysis
```

Use the actual private path. Exports carry study, manifest, runtime, assignment
and record-kind identifiers. Analysis refuses incompatible versions, mixed record
kinds, incorrect assignments, changed drafts and non-replayable states. Official
scores and additional blinded adjudications are separate. Do not commit private
observations or identity keys to the public repository by default.
