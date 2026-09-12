# Use the matched desk, then register collection

Operational handoff checked 2026-09-12. **This is not a study registration.**
The frozen `matched-qgm-v1` manifest and runtime verify at main commit `1c2a2c72`.
No study code, packets, scores, manuscript or frozen hashes were changed.
Inspection was limited to repository study records and the configured pilot/practice
locations. It found software fixtures and one older formative-v1 investigator
practice export, with no genuine matched participant exports, registered schedule
or documented participant authorization. Off-system arrangements remain unknown.
No participant analysis, adjudication, task responses or new inference occurred.

## Alex's practice, available now

- URL: <http://127.0.0.1:9043>
- Mode: `investigator_practice`; no run or timed block was started for you.
- Process: PID `1411715`, `python3 -m research.oversight_workflow.matched.server --port 9043`
- Codex process session: `20523`
- Local exports/journals: `/tmp/oversight-matched-practice/`
- Stop exactly this server: `kill -INT 1411715`

This process identity is valid for this launch. If it has exited, do not kill a
reused PID. Relaunch with the command above. The server binds only to loopback;
existing investigator/model services were preserved. Export practice work before
temporary storage is cleared.

1. Open the URL, enter a new practice code such as `alex-matched-practice`, and
   choose **assignment 0**. This is your practice, not a participant allocation.
2. Complete separate-source training (four minutes). Try source inspection,
   calculator, entering an answer/scale, deferral/resumption, optional grouping,
   and the distinction between approval and release.
3. Complete **Q, then G, then M**, each twelve questions/nine minutes. Use the actual
   sources and controls. Drafts can be wrong or missing. No answers are supplied
   by this handoff. Leave difficult work unresolved rather than hiding it.
4. Save each block's questionnaires with your own responses or explicit missing
   items. Break between blocks as needed. Any retrospective comments are your
   investigator-practice observations, not independent participant evidence.
5. Select **Download identified session package** after the last form. Alternatively:

```bash
curl --fail http://127.0.0.1:9043/pilot/export -o /tmp/alex-matched-practice.pilot.json
```

Record concrete task or interface problems. Practice does not estimate G-Q or an
assistance effect. Do not restart a timed block and silently pool its rerun. A
material defect should be documented before any separately versioned change.

## One remaining collection checklist

Use the existing [investigator instructions](../INVESTIGATOR.md), without treating
an authorization JSON as approval. Before actual participant use, resolve:

- **Institutional determination and consent:** actual coverage of matched-qgm-v1,
  three nine-minute blocks, logging, ratings, interview and withdrawal. References
  are unresolved here; reuse valid existing coverage if it is supplied.
- **Population:** eligible participants, required source/numeracy familiarity and
  prior exposure exclusions. No population or participant commitments are invented.
- **Tranche and schedule:** decide whether this is standalone feasibility or part
  of a larger predetermined collection. Fix size, assignment order and stopping/
  missingness arrangements before outcomes. Do not extend or stop for effect direction.
- **Adjudication:** name actual source-qualified raters and disagreement handling,
  with blinding and official scores preserved. No additional judgments exist here.
- **Storage and withdrawal:** choose actual private export/identity/consent locations,
  access/retention and withdrawal handling. The `/private/...` examples in prior
  instructions are placeholders, not configured or verified records.

## Concrete scheduling option, not yet registered

The existing balanced six-assignment cycle is a feasible **scheduling option**.
It is not a powered sample, agreed tranche, recruitment commitment or registration.
It may be selected for standalone feasibility; if collection belongs to a larger
study, the total design and sample/stopping rules must be predetermined first.
Study purpose, actual tranche size, investigator, authorization/consent references,
private code mapping and registration date remain **unresolved**.

| Proposed slot | Assignment ID | First block | Second block | Third block |
|---|---:|---|---|---|
| 1 | 0 | Q / packet 0 | G / packet 1 | M / packet 2 |
| 2 | 3 | Q / packet 0 | M / packet 1 | G / packet 2 |
| 3 | 7 | G / packet 1 | Q / packet 2 | M / packet 0 |
| 4 | 11 | G / packet 2 | M / packet 0 | Q / packet 1 |
| 5 | 13 | M / packet 1 | Q / packet 2 | G / packet 0 |
| 6 | 17 | M / packet 2 | G / packet 0 | Q / packet 1 |

These are exact manifest entries. Every person sees disjoint sources in Q/G/M.
Slot numbers are not participant identities. Assign private codes before outcomes;
keep the schedule registration outside this public repository. Investigators must
state how nonattendance/withdrawal affects the predetermined tranche, rather than
replenishing based on observed results. Do not count someone who practiced on these
sources as a naive matched participant on the same sources.

**Next action:** try the running practice desk; then supply or complete the actual
collection arrangements and register the selected tranche before participant mode.
The supported paper remains a systems position. Human grouping and draft-assistance
benefits remain unmeasured; there are no new participant figures or manuscript claims.
