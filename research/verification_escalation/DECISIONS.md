# Development decisions

- Start: main 9cea20b9, clean. No applicable AGENTS.md found in repository ancestry.
  Previous clarification results motivate source recovery, not a stronger queue.
- Dataset audit: BIRD-Interact reference SQL/tests still require email; no contact.
  PRACTIQ repository provides generation code but no complete released task table.
  AmbiSQL repository provides the interactive method but not its described 40-case
  table. AmbiQT is public, but its evaluator maps alternatives to original SQL.
  Do not treat that mapping as empirical outcome invariance.
- Followed closest reference AMBROSIA: accessible public-password download,
  generated databases and human-written requests/interpretations. Source license
  CC BY 4.0, authors request no dataset upload to GitHub. Full source and raw prompt
  records therefore remain local and excluded; derived results and generated SQL
  are committed. Reproduction downloads source from its original host.
- Pilot v1: nine development cases, 36 scheduled calls. Model errors, context
  failures and a malformed response retained. Generated verification produced no
  suppression. Source recovery reduced answers but sometimes implemented the
  recovered instruction wrongly. This separates provenance from semantic accuracy.
- Revision v2: serialize database as JSON data instead of an escaped JSON string;
  explain the unsupported-alternative flag rather than putting true in the example.
  Preserve all v1 calls. Same nine cases, 36 further scheduled calls. No cases
  selected by outcome. Balanced final selection across three ambiguity types
  replaces a source-order-only design that would contain attachment cases alone.
- Code checks found two erroneous test expectations: execution latency is not a
  deterministic observation, and a scope-excepted count can independently be
  invariant. Corrected tests compare semantic state and scoped answer effects.
  Original failed test logs retained. A baseline adapter return-type error was
  corrected before evaluation and its traceback retained.
- Decision: retain the no-gain pilot, test the conservative rule on fresh source
  databases, and characterize candidate omission with explicit synthetic failures.
  No new grouping or queue algorithm is claimed. A final null result completes
  this research question without weakening the recovery baseline.

## Source-reading fairness audit (secondary, after freeze)

The recovery condition supplies a structured authoritative instruction. Requiring
an exact model-quoted copy is a narrow backend choice, not the strongest possible
source reader. A secondary saved-output audit therefore uses the cached SQL response
to that identical full instruction, with zero new questions. It verifies that the
available source text equals the instruction received by the cached generation.
This isolates direct reading from candidate enumeration and quote extraction. It
changes prompt style, so it is reported separately from the common-backend frozen
comparison and requires no new inference. It cannot support an algorithmic claim
for verification. The primary ambiguous-input comparison remains unchanged.

## Online-only repairs

Interactive inspection found that a prior attempted question could prevent asking
again after its dependency version changed. OnlineController preserves the full
history while making the changed version eligible, without restoring spent budget.
The desk rejects a stale displayed question and invalidates affected earlier outputs
when a received instruction changes their implementation. Display replay hashes
exclude measured execution latency. The terminal-only frozen empirical runs do not
revise after an answer; their code and results remain unchanged. Earlier failed
browser logs are preserved.

## Ordering defect and disjoint repair

After the first frozen run completed, inspection found that its blanket unordered
contract and generation prompt contradicted explicit ranking requests 2842 and
2863. Preserve all 48-database outcomes as a flawed-adapter diagnostic. Before any
new outcome, freeze a disjoint 24-database follow-up and infer ordering from the
released request/instruction. Commit 58c366d7 records the repair. The same model,
controller, comparisons and statistical definitions remain. Six additional source
availability databases are a paired subset, not independent extra cases. The 156
additional calls bring the declared session total to 540, below 600.

## Additional boundary checks and scope of synthetic evidence

A COUNT query returning zero has one result row. A new adversarial unit test shows
that the frozen nonempty-table safeguard does not prevent equally mistaken zero
aggregates. This is a limitation, not a post-evaluation tuning opportunity.
The synthetic count and export are distinct goals, but count often happens to be
invariant. Consequently, the no-sharing ablation may tie even though the export
needs a decision. Do not attribute that tie to successful shared-answer reuse.
The family named verification_waste is structurally another equality control;
its name alone does not establish wasted computation. Report the executed
arithmetic and measured costs, not the family label's intended interpretation.

Further online checks found that the frozen no-sharing path has a final
decision-level duplicate guard that can prevent a second request-specific answer
when two consequential tasks share an identifier. The frozen empirical tasks each
have one task, and the existing synthetic second count was invariant, so this did
not change their quality results. Treat that ablation's generality as limited.
OnlineController now uses request-level accounting in that mode, with a targeted
two-consequential-task test. It also caches unchanged failed answered SQL. The
frozen replay counts include the original repeated failed executions (five extra
in the primary completion condition). These online repairs do not alter saved
experimental rows or claim a new empirical improvement.
