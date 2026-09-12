# Analysis contract and data dictionary

Run the commands in README against one record kind at a time. Only genuine,
provenance-validated `participant` exports populate participant figures/results.
Formative-v1, practice and fixture files cannot silently become matched observations.
The code uses no new inference. Reference annotations are imported only by offline
analysis, never by the task server.

## Inputs and validation

An `oversight-matched-export-v1` export retains the existing `.pilot.json` extension.
It records `matched-qgm-v1`, manifest and runtime hashes, kind, run/code/assignment,
authorization metadata when applicable, every ended block and any active snapshot.
Each block includes condition/packet, source/question IDs, raw proposals (all null
in M), declared and actual clock, arrivals, logical state, events, versions,
questionnaire and end reason. The event history contains displayed-state events,
selections, notes, decisions, releases, refusals and cutoff. Logical replay checks
every command response and state digest. The participant server verifies the freeze
before use. The exact code and analysis version must remain unchanged during a
collection tranche; do not recompute a freeze after observations to hide a change.

## Outputs

| File | Interpretation |
|---|---|
| `answers_official.csv` | One offered question per block, current-version joint/EM/F1 release scores, approvals, initial draft score, blocked/unfinished states |
| `sessions.csv` | One person/block, all offered counts, Y, absolute components, packet/order, timing proxies, grouping, Raw TLX and separate control items |
| `paired_descriptions.csv` | G-Q primary; Q-M and G-M secondary, one difference per available person/contrast |
| `summary.json` | Pair means/medians/sign counts, qualified intervals, missingness and provenance |
| `packet_order_coverage.csv` | Counts for each condition/packet/position, exposing imbalance |
| `review_intervals.csv` | Select-to-decision or censored interval with resumed flag; not continuous reading time |
| `request_waits.csv` | Receipt-to-first-selection/cutoff, overlap with another source's grouped active review |
| `version_history_official.json` | Every decision/release scored for its exact version, including superseded versions |
| `qualitative_links_blank.csv` | Empty template linking retrospective accounts and negative cases to events |
| `adjudication_blinded.json` / `adjudication_blank.csv` | All released candidates, references and sources for independent offline review |
| `adjudication_key_PRIVATE.json` | Link to condition/run/official scores, withheld from raters |
| `participant_outcomes.svg/pdf/png` | Produced only from validated genuine observations; one line/person, counts alongside quality |

Current-version `incorrect_approved` and `incorrect_released` are endpoint counts,
not all historical acts. Use `version_history_official.json` to report obsolete
approvals/releases separately. A revised answer cannot inherit an old release.
`unresolved` counts queue/active/deferred status; `unfinished` means no current
release and includes rejection and approval awaiting release. Report both. An
incorrect release is completed but wrong, and must not disappear into unresolved
work. All denominators include offered tasks that never started.

`successful_corrections` counts a released current answer changed from an initially
wrong draft to a joint-correct answer. `harmful_corrections` counts the reverse.
They are final distinct-question counts, not repair event totals. M has no initial
model answer and does not contribute to these assisted-draft metrics.

`source_focus_events` are browser focus/click observations. The legacy
`source_revisits` counts repeat focus events, which may reflect repeated clicks
without a task switch. Use `source_selection_returns` separately for a return to a
previous source after selecting a different source. `grouped_selections` counts
selections of group members; grouping is self-selected use, not randomized exposure.
`resumed_to_decision` and `resumed_to_release` are interval counts with a later
recorded act/release on that request, not proof of comprehension or a correct
answer. Check actual final scores and version events. Other-source wait overlap
shows coincidence with grouped review, not that grouping caused a delay.

## Pairing, uncertainty and incomplete records

The predeclared primary mean is the participant mean of G-Q joint-correct release
proportions, each with denominator 12. Report absolute G and Q counts and incorrect
releases alongside it. Use pairwise available ended blocks, not unrelated people
in each condition. Missing sessions and withdrawn cases remain explicit; withdrawn
pairs are excluded from summaries. Active interrupted blocks are descriptive only.
A voluntary early finish is retained with the full offered denominator, and its
shorter observed duration is reported. No answers or missing ratings are imputed.

Raw TLX retains all six 0-100 items. Its unweighted raw mean is available only when
all six are present. Custom perceived-control items remain separate 1-7 responses;
there is no combined validated workload/control scale. Paired rating comparisons
use only available pairs and give their own n. Incomplete forms remain incomplete.

The 2,000-resample fixed-seed participant bootstrap is descriptive and reported only
with at least six available pairs. It conditions on these reused packets. Show
individual values even when intervals are available. Participants, not clicks or
questions, are the paired unit. With a small sample describe packet/order patterns
without fitting a complex model. A sensitivity table stratified by packet or order
is exploratory and may be sparse. Do not interpret an interval containing zero as
equivalence, or suppress unfavorable error counts when quality improves.

## Additional blinded adjudication

Give a rater `adjudication_blinded.json` and its blank CSV, **not** the private key,
session export, packet assignment or official score table. Cases are shuffled by
opaque hash and include exact-match controls. Candidate and reference wording,
question and original source remain visible because source-based evaluation is the
rater's task. Actual benchmark wording can still create source familiarity; record
that limitation. The rater records `acceptable`, `unacceptable` or `uncertain`, a
source-specific reason and rater code. An uncertainty is not counted as accepted.
Arrange raters and disagreement handling before collection. The import accepts one
resolved judgment per case, so retain independent initial rater files and any
resolution notes privately rather than overwriting them.

```bash
python3 -m research.oversight_workflow.matched.analysis \
  --out /private/matched-analysis \
  --adjudications /private/resolved-blind-adjudications.csv
```

This creates `adjudicated_ADDITIONAL.csv` and
`adjudicated_sessions_ADDITIONAL.csv`. Official files stay unchanged, and cases
not adjudicated remain labeled. No automated semantic or LLM judgment substitutes
for this process. Do not expose any of these annotation-bearing files through the
study server.

## Mechanism analysis

After timed sessions, use INTERVIEW.md. Inspect all valid participants' traces,
including G nonusers, source-only successes and unfavorable group episodes. Code
concrete actions and accounts, distinguish observation from interpretation, link
timestamps/request IDs, and record alternative explanations. Compare claims about
source reuse with returns, deferrals and unrelated waits; inspect claimed carryover
errors against released answers and source evidence. Do not prefill themes or
quotes. This can explain a pattern but cannot alone establish causal mediation.
