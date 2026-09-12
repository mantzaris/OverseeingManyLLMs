# Export and offline analysis

The server has no scoring or annotation imports. Export uses
`oversight-pilot-export-v1`, a pilot version and manifest hash, run ID, pseudonymous
code, assignment and explicit `record_kind`. It includes block IDs, interface,
packet, original question/source IDs, complete offered tasks, source hashes,
proposals (B/C only), all artifact versions, events, final state, cutoff/end reason,
questionnaires and technical notes. Raw proposal responses contain model content,
not benchmark annotations. Source-only exports contain no cached model proposals.

Each event includes a server monotonic offset, UTC timestamp, event ID, action,
payload, response and resulting logical-state hash. The application records arrival,
selection, note, decision, release, pause, grouping, display/focus and refusal events.
A late action is retained even if refused. Exports also preserve an active unfinished
block if the process is stopped or exported mid-block. Journals are appended before
HTTP acknowledgement; these files do not constitute a crash-atomic database.
The wrapper writes its current package by atomic file replacement.

## Run analysis

```bash
# Future genuine observations only; default rejects practice and fixtures.
python3 -m research.oversight_workflow.pilot.analysis /private/path/pilot-records \
  --out /private/path/pilot-analysis

# Alex's practice remains a different evidence class.
python3 -m research.oversight_workflow.pilot.analysis /tmp/oversight-pilot-practice \
  --kind investigator_practice --out /tmp/oversight-practice-analysis
```

A directory supplies its immediate `*.pilot.json` files. Do not mix downloaded and
server exports from different moments: identical duplicates are deduplicated, but
conflicting snapshots of one run are refused until the investigator selects the
final export explicitly. Multiple runs for one code are refused to avoid inflating
independent observations. Unknown versions, altered assignments, source mismatches
and replay mismatches also fail validation. The tool does not discard hard tasks,
missing sessions, withdrawals or incomplete questionnaires silently.

Outputs:

- `sessions.csv`: offered, started, received, approved, released, official answer-EM
  and joint-correct releases, incorrect approvals/releases, blocked, unresolved,
  unstarted and unfinished work. Correction attempts, successful and harmful released
  corrections are separate. Source-only writing is not counted as correcting an LLM.
- `answers_official.csv`: every offered question, current version, completion status,
  and official scoring when released. An unreleased answer is not awarded completion
  credit. F1/EM/scale are not replaced by subjective interpretations.
- `review_intervals.csv`: complete and cutoff-censored select-to-action intervals,
  with resumption flags. These include idle time and interruptions, not just reading.
- `paired_descriptions.csv`: one C-minus-B row per completed B/C pair, with withdrawal
  flags. Different tasks within a person are matched at packet-design level, not as
  identical questions. Missing B/C blocks cannot form a complete pair.
- `summary.json`: missing blocks, duplicate handling, explicit evidence type and
  descriptive paired summaries. At least six complete nonwithdrawn pairs are needed
  for the optional descriptive participant bootstrap. This is not a power threshold.
- `individual_trajectories.{svg,pdf,png}`: individual raw counts, clearly labeled by
  evidence type. Source-only has six offered tasks and four minutes; its separate panel is
  not a direct assistance-effect comparison with the 12-question nine-minute blocks.

Raw TLX mean requires all six values; custom control items stay separate. The app
also saves individual TLX items in exports. Missing items are not imputed. Withdrawn
and partial records remain in descriptive tables, subject to the investigator's
actual authorized data-retention requirements; the tool cannot decide consent.
Do not infer preserved quality from a nonsignificant difference, or count question
rows as independent participants. These repeated packets do not constitute a random
sample of independent financial reports.

## Additional blinded adjudication

The analysis generates `adjudication_blinded.json` for **every released answer**,
including exact-match controls. It contains question, source, candidate and reference
without participant, condition, official score or outcome labels. It is an
offline investigator resource, never a file served by the desk. Its private key
maps case IDs back to results. Assign raters under the declared plan. They assess
source-grounded acceptability, units and meaningful precision, retaining uncertainty.
A reference annotation is evidence for adjudication, not an infallible verdict.

Copy `adjudication_blank.csv` outside the analysis output directory, enter
`acceptable`, `unacceptable` or `uncertain`, a substantive reason, and rater code.
Do not replace raw candidate wording or reference values. Record disagreement
resolution separately; one rater's decision is not inter-rater reliability.

```bash
python3 -m research.oversight_workflow.pilot.analysis \
  --out /private/path/pilot-analysis \
  --adjudications /private/path/completed_adjudications.csv
```

The command validates IDs, duplicates, verdicts and reasons and creates
`adjudicated_ADDITIONAL.csv` and additional per-session counts in
`adjudicated_sessions_ADDITIONAL.csv`. Missing/uncertain judgments remain explicit. Original `answers_official.csv` remains unchanged.
Do not report additional adjudicated acceptability as official benchmark accuracy.
The audit's three potentially defensible nonmatches have **not** been adjudicated.

## Failure handling

Missing completed sessions and active interrupted exports are flagged; no synthetic
replacement is generated. Early finish keeps all offered tasks; an early withdrawal
retains its provenance and is excluded from paired interval calculation. The
investigator decides whether its retention is permitted. A technical dropout is
not ordinary rejection. Clock cutoff is checked before handling new decisions, so
queued network actions cannot backdate an approval. Already in-flight arrivals can
remain in the final state without becoming releases. Duplicate action IDs return
one receipt, and duplicate exports do not increase the sample size.

The compressed browser dry run is stored only under `test_data`. It supplies a
literal zero as an intentionally scripted answer to exercise authoring/release,
and submits **no numeric questionnaire responses**. It is not a participant,
simulated human efficacy test or ideal-review comparison. Every analysis table and
plot marks its provenance. The analysis refuses it in default participant mode.
