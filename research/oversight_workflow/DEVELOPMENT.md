# Development and repair record

- Start: clean main at 8ee8f5a2, no newer working-tree changes. No applicable
  AGENTS.md was found in the repository or checked ancestors. Existing study
  materials and desks were read before implementation.
- Six original questions from the first previously used development context were
  generated with the short readable interface. All returned parseable, nonempty
  answers; mean generation time was about 1.2 seconds. This was a feasibility
  check, not an accuracy-driven tuning loop.
- The fresh selection was fixed to the first 24 eligible unused source contexts,
  excluding historical and selected normalized-source duplicates. There are 145
  original questions. The frozen plan at dec24be3 records 290 initial generations
  and four predetermined revisions. No source or question was replaced.
- The first protocol version passed ten focused tests before fresh generation.
  The live demonstration used the first two source contexts and the initial
  generations already counted in that collection. A six-second pinned review
  overlapped actual model arrivals. A new generation produced a revision; an old
  approval attempt was refused. No reference annotation entered this live desk.
- After freezing, implementation review added locking around counts and atomic
  replay admission/start, and recorded an exact cutoff event sequence. These are
  concurrency/accounting repairs, not changes to sources, prompts, conditions,
  timings or outcomes. The original frozen code hashes remain preserved.
- The first browser harness failed because CDP evaluated an unwrapped top-level
  await. Its second attempt selected before the first asynchronous arrival had
  been polled. Both failures are retained in browser/ and browser_v2/. Waiting
  for the actual ready state fixed the test; browser_v3 passed 44 checks. These
  are harness failures, not model or participant outcomes. The version warning
  was moved above the active card, and a stale toast is cleared on session change.
- The first software-evaluation attempt stopped before its first completed
  scenario: the existing annotation loader returns context -> question -> label,
  while the script initially indexed it as question -> label. The traceback is
  retained in software_attempts/. No scored outcome had been produced. The
  private scripted-inspection lookup was flattened; future incomplete scenario
  failures save events before stopping. No agent request or frozen case changed.
- The UI server imports only the public item adapter, not the evaluator. Source
  annotations are loaded only by offline scoring and explicit ideal scripts.

These records preserve implementation failures without recasting them as a
successful empirical run. Later software results use the repaired implementation;
model outputs and their original requests are unchanged.

## Interface completion after the primary matrix

- Stale poll responses could arrive after a newer command response. The client now
  rejects older event sequences and prior-session states. Active DOM identity,
  focus and typed notes are tested during fresh arrivals in all three views.
- Optional source-session controls initially captured the first rendered related
  list. They now use the latest received requests when explicitly invoked, while
  a session already being inspected stays stable. The failed grouping harness is
  preserved in `browser_verified/`.
- Replaying a journal now preserves original UTC timestamps, and restoring it
  accounts for elapsed time since the last event. A browser recovery test exposed
  duplicate `condition` metadata during re-journaling. A focused restoration test
  and `browser_delivery_v2/` verify the repaired path. The failed preceding run
  remains in `browser_delivery/`.
- The final extended harness passes 57 checks. It includes a dropped browser
  connection, unsuccessful offline approval, idempotent HTTP retry, restored
  deferral, and a one-second prospective-study preview that retains unstarted work.
  These are new software checks, not a replacement of the 144 frozen scenarios.
- The prospective human preview uses four disjoint six-context packets, a server
  cutoff, visible remaining time and all-offered accounting. No human observations
  were collected. Timing is provisional until an authorized formative pilot.
- The actual-source walkthrough uses the first selected source and its first
  questions. Its version event is one of the four saved model rechecks. The browser
  regression harness instead uses explicitly authored metadata revisions. These
  evidence types are kept separate.
- The legacy answer formatter flags optional citation strings in 157 initial
  outputs. Every model body is parseable JSON; 38 answers are empty. Readable
  answers and the complete source remain available. No parser rescue, new model
  prompt, sample replacement or additional inference was introduced after results.
- Final visual inspection found that a persistent newer-version warning was being
  rebuilt on each poll. Its controls now retain DOM identity and focus until the
  request/version changes. Decision history is similarly retained until its actual
  content changes. These are focus-stability fixes, with browser regression checks.
- An executable practice route loads the old development training questions and
  saved pilot answers. It does not consume new inference or scored source cases.
  A same-answer version change is labeled as an authored training fixture.
- The completed final browser harness passes 62 assertions, including persistent
  version-warning focus and the disjoint practice route. Its six journals and the
  actual-source walkthrough are replayed separately from the primary matrix.
  Earlier timing measurements are retained. Published browser latency summaries
  use the final harness rather than selecting the fastest run.
- Final API review put journal restoration and session-ID validation under the
  same application lock as session changes. A delayed command cannot pass an old
  session check and then act on a newly started desk. These atomicity repairs do
  not alter the frozen task/decision semantics or saved logical outcomes.
- Closing the stage seals new inference in its transport when the final ledger is
  present. Exact cached requests remain readable and no longer overwrite prepared
  timing records. A new namespace/authorization is required for later collection.
  The focused closure test confirms refusal before a network call. Historical
  authorization files and the running model server are unchanged.
