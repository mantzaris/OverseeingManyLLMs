# Formative review pilot

A runnable preparation package for comparing B (central queue) with C (optional
source sessions and admission controls). It reuses the existing desk and review
protocol. **No participant observations or workload benefits are reported.**
The real TAT-QA tasks and saved Qwen drafts are suitable for testing task feasibility;
their low draft accuracy makes that check necessary before an effectiveness study.
See [AUDIT.md](AUDIT.md), [PROTOCOL.md](PROTOCOL.md) and [INVESTIGATOR.md](INVESTIGATOR.md).

## Alex's preview

From the repository root, in the existing Python environment (or install the parent
`research/oversight_workflow/requirements.txt` into a local virtual environment):

```bash
python3 -m research.oversight_workflow.pilot.server --port 9042 \
  --log-dir /tmp/oversight-pilot-practice
```

Open **http://127.0.0.1:9042**. Choose a code and assignment, start separate-source
training, then follow B/C/source-only blocks and forms. Assignment 0 demonstrates
B, C, then source-only; all 18 rotations are available. The normal block lengths
are 4 minutes training, 9 minutes each B/C and 4 minutes source-only. These durations
are design choices. You may end practice blocks early. Export has the code, run,
assignment and provenance; practice cannot silently enter participant analysis.
Ctrl-C stops only this local pilot server. No model service is used or changed.

Preview uses the same source and decision controls as collection. A calculator,
visible clock, saved deferred draft and post-block forms are included. The source
session controls appear above long sources so they can be found. Every question
keeps its own answer and approval. Empty proposals remain visible and editable.

The investigator must complete institutional/consent requirements before enabling
participant mode. [PARTICIPANT.md](PARTICIPANT.md) is task instruction, not consent.
[INVESTIGATOR.md](INVESTIGATOR.md) contains the neutral facilitator script and the
remaining collection checklist.

## Saved-output verification and analysis

```bash
bash research/oversight_workflow/pilot/reproduce.sh
```

This reproduces the raw-answer audit, verifies meaningful pilot and historical
protocol boundaries, and analyzes the saved **software fixture**. No inference or
participants are involved. [ANALYSIS.md](ANALYSIS.md) describes all output fields,
official and additional adjudicated scoring, partial runs and duplicate handling.

Later, analyze genuinely authorized observations with:

```bash
python3 -m research.oversight_workflow.pilot.analysis /private/path/pilot-records \
  --out /private/path/pilot-analysis
```

Default participant mode refuses fixtures and practice. For Alex's own practice:

```bash
python3 -m research.oversight_workflow.pilot.analysis /tmp/oversight-pilot-practice \
  --kind investigator_practice --out /tmp/oversight-practice-analysis
```

To exercise the complete browser collection path, use two terminals with Node 22+
and Chromium at `/opt/google/chrome/google-chrome` (edit the documented executable
path only for another installation):

```bash
python3 -m research.oversight_workflow.pilot.server --port 9042 \
  --kind software_fixture --log-dir /tmp/oversight-pilot-software-test
node research/oversight_workflow/pilot/browser_dry_run.mjs /tmp/pilot-browser-test
python3 -m research.oversight_workflow.pilot.analysis \
  /tmp/pilot-browser-test/complete_fixture.pilot.json \
  --kind software_fixture --out /tmp/pilot-browser-test/analysis
```

The browser script closes its temporary browser. Stop the temporary pilot server
with Ctrl-C. It runs one compressed assignment, not a large scripted policy study,
and leaves questionnaire answers blank.

## Files and evidence

- `manifest.json`: public selection, exact question/source IDs, 18 assignments,
  identical B/C arrival settings and source-only subset.
- `adapter.py`: uniform pilot-only display projection. Historical scores stay fixed.
- `server.py`, `setup.html`, `desk.js`: thin study wrapper around the existing desk.
- `analysis.py`: offline scoring, replay, paired descriptions and blinded adjudication.
- `AUDIT.md`: all 38 empty answers and a declared 22-case nonempty audit.
- `PROTOCOL.md`, `PARTICIPANT.md`, `INVESTIGATOR.md`: study-ready instructions.
- `REPORT.md`: completed preparation, tests, evidence limits and investigator decisions.
- `../../../artifacts/oversight_workflow/pilot_preparation/`: exact audit rows,
  separate dry-run records, screenshots, manifest freeze and resource ledger.

The existing ICAART position-paper draft remains intact. No interface effectiveness
or human cognitive-load claim is added by this preparation stage.
