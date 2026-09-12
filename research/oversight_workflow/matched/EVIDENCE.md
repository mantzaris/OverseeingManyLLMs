# Preparation evidence, not participant findings

The final software run is
`artifacts/oversight_workflow/matched_preparation/test_data/complete_fixture.pilot.json`.
It contains four blocks (training, Q, G, M), 223 events, and 60 passing browser
checks. It uses the real sources and genuine saved drafts for assisted blocks;
its answer `0` and actions are explicitly authored software inputs. Questionnaire
items are all null. No participant quotes, ratings, themes or effect figures are
created from it.

Scored fixture clocks are compressed equally to 18 seconds; training is eight
seconds. This is a test-only override. The manifest and actual practice/participant
configuration remain 540 seconds for each of Q/G/M and 240 seconds for training.
Each scored fixture block offers and receives 12 questions and releases one authored
version 2. It rejects one other answer and retains 11 unfinished deliverables.
The computed fixture G-Q tie is an arithmetic/software check, not human evidence.

The run covers setup/assignment, neutral training, incoming second waves while
active, preserved draft controls, grouping three separate same-source cards,
deferral/resumption, exact-version correction approval, separate release, rejection,
automatic cutoff, refused late release, blank forms and export. M receives no raw
model proposals or generated answer/explanation. Q/M have no grouping controls.
All conditions reject admission-control commands. Every block replays exactly.

Screenshots are actual browser captures and visibly labeled **SYNTHETIC SOFTWARE
FIXTURE**. Q, G, M and final-export images were visually inspected. They show
incomplete/wrong actual drafts, the source and differing navigation, not user
performance. The G cards take additional vertical space, a declared part of the
grouping interaction rather than an unreported layout difference.

Twelve focused new tests verify allocation/assignment balance, source isolation,
manual draft absence, protocol restrictions, stable active versions, separate
approval/release, freeze/version/kind checks, scoring and additional adjudication,
paired denominators, missing/withdrawn handling and cutoff. Three existing pilot
regression checks cover display projection, approval/replay and annotation isolation.
The old handoff's 24-file hash verification passes. The new preservation snapshot
also includes the current manuscript, formative-v1 files and unchanged scoring
code/annotations. No broad historical replay sweep was run.

## Development record

- Reused formative-v1 runtime and packets; added a small versioned adapter. No
  architecture rewrite, correction-transfer study or inference was launched.
- During implementation a generated Python line in the new analysis writer had a
  syntax error, corrected before evaluation. Compilation and subsequent analysis
  pass. No participant exports existed.
- The first focused test run passed but exposed a file-handle warning. It was fixed.
  A later run correctly found that a participant-kind rejection attempted to read
  the not-yet-created freeze and raised FileNotFoundError instead of a clear
  ValueError. The new freeze function now reports that the comparison is not yet
  frozen. Logs of both development runs are retained.
- The final twelve-test run and the **one complete** browser Q/G/M fixture pass.
  There were no failed browser collections or repeated favorable-result searches.
- Existing formative-v1 practice metadata was inspected only for provenance. It
  was not rescored or relabeled. No genuine matched participant records were found.

## Optional exact browser recheck

The saved-output reproduction in README needs no running browser or server. To
recheck the interaction after a concrete code change, use an explicitly separate
software output directory and identify a new development version if collection has
started. The script expects Google Chrome at `/opt/google/chrome/google-chrome`
and Node with native WebSocket support (the checked environment has Node 22).

```bash
python3 -m research.oversight_workflow.matched.server --port 9043 \
  --kind software_fixture --log-dir /tmp/matched-software-recheck
# In another terminal:
node research/oversight_workflow/matched/browser_dry_run.mjs /tmp/matched-browser-recheck
python3 -m research.oversight_workflow.matched.analysis \
  /tmp/matched-browser-recheck/complete_fixture.pilot.json \
  --kind software_fixture --out /tmp/matched-browser-analysis
```

Stop that fixture server after use. The checked script closes its temporary browser.
Do not point participant analysis at these software records. Do not repeatedly run
this as a surrogate for collecting genuine observations.
