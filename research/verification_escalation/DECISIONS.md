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
