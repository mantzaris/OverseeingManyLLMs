# Investigator handoff for the matched comparison

## What is ready and what is not authorized

The software, matched packets, scoring path and neutral task materials are ready
for investigator inspection. No genuine matched observations or documented
human-study determination/consent approval were found. The existing prospective
checklist at `../pilot/INVESTIGATOR.md` remains the institutional/consent boundary;
its preparation is not authorization. There is one old formative-v1 practice
export, which is not evidence for this comparison. No one was contacted.

**Next investigator action:** register the first authorized matched tranche and its
assignment schedule. Confirm that the institutional determination and consent cover
three nine-minute blocks, the specific logging, questionnaires, retrospective
interview and retention/withdrawal rules. Specify eligible population, practical
tranche size, workstation, rater arrangement and storage using the existing
investigator process. Do not claim power from a convenient assignment cycle.
If authorization is not yet supplied, restrict use to investigator practice.

For assignment coverage, manifest IDs `0,3,7,11,13,17` are a balanced six-run example,
not a required sample size. Predetermine the code/assignment order and persist its
registration reference. A completed 18-assignment cycle gives fuller balance.
Report actual coverage, dropout and deviations. Old practice users who have seen
these tasks are development users, not naive participants on these same packets.

## Launch and fixed flow

```bash
python3 -m research.oversight_workflow.matched.freeze
python3 -m research.oversight_workflow.matched.server --port 9043 \
  --log-dir /tmp/oversight-matched-practice
```

Open <http://127.0.0.1:9043>. Select code/assignment in setup; no per-block file edit
is required. Verify the header says `matched-qgm-v1`. Training uses its separate
source, then the assigned Q/G/M blocks each run for nine minutes. Save each form,
including unanswered items; break between blocks as needed outside the clock.
Conduct the interview after all timed blocks. The timed blocks have no think-aloud.
Use the same workstation, display size and calculator access across conditions.

Read neutrally before training:

> You will answer questions using the tables and text. Some blocks include an
> agent's draft, which may be correct, wrong or missing. Check the source and units.
> You may approve a draft, enter a correction or your own answer, reject, or defer.
> Approval and release are separate. Release only answers you judge correct.
> Each timed block offers twelve questions over nine minutes. Some arrive later.
> You can choose the next request. One interface also offers optional source
> sessions, with separate decisions for each question. Use the controls as you
> find appropriate. We are examining the tasks and interfaces, not testing you.

In training ask them to find a table heading/paragraph, try the calculator, enter
an answer with scale, defer and resume its draft, create a source session, and
approve then separately release an exact version. Do not suggest that grouping or
drafts should help. Check comprehension before starting the first scored block.
If training is insufficient, record the issue and additional support. During scored
blocks resolve only technical questions and record intervention; give no answer
or interpretation advice. Never open annotation/audit files in the scored browser.

## Future participant mode

Only after actual authorization, create a **private** JSON record with the genuine
values for `collection_authorized` (true), `institutional_determination`,
`consent_version`, `investigator`, `record_reference`, plus:

- `study_version`: `matched-qgm-v1`
- `manifest_sha256`: `71352c921464ab4799309e6368437532ae30d9ddebe2ccf957b75ba32017ba10`
- `assignment_schedule_reference`: identifier/path for the pre-recorded schedule.

A JSON record documents the investigator's assertion; the application cannot
supply or independently verify institutional authorization. Do not reuse the old
formative-v1 authorization without covering and identifying this changed protocol.

```bash
python3 -m research.oversight_workflow.matched.server --port 9043 \
  --kind participant --authorization /private/matched-authorization.json \
  --log-dir /private/matched-exports
```

The server verifies frozen files, and exports include its runtime hash. Use the
registered assignment for each code. Setup permits all manifest assignments for
operational use; the investigator must follow the external schedule. Do not change
features, packets, timing, prompts or scoring within a version. A later revision
must have a separate version and declaration, with older observations preserved.

## Export and interruptions

Use **Download session package** after forms, or:

```bash
curl --fail http://127.0.0.1:9043/pilot/export -o /private/code-run.pilot.json
python3 -m research.oversight_workflow.matched.analysis \
  /private/matched-exports --kind participant --out /private/matched-analysis
```

Server exports are atomically saved after actions. Reconnecting to a running server
restores the active logical state and remaining time; the timer does not stop while
disconnected. Record interruptions. If the server dies, retain its partial export,
stop that block and document the failure. Do not reset the clock and pool the rerun.
Use explicit withdrawal if requested and follow the authorized data deletion rule.
Keep consent/identity keys separate. Never commit genuine records by default.

The endpoint is loopback-only. Keep setup and exports investigator-controlled;
this is a local trusted-study application, not a hardened public multiuser service.
Stop the process with Ctrl-C after use. Leave the existing model server unchanged.
