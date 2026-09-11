# Semantic audit and isolated repairs

The original frozen code, declarations, generated evidence and outcome rows stay
unchanged. These findings were identified by inspecting implementation semantics,
not by searching for a favorable policy result.

## Synthetic scope responder inconsistency

The two scope families sampled a fallback preference independently, then defined
the effective exception target using the shared value whenever scope applied.
But asking directly for the exception's preference returned the independently
sampled fallback even when it differed from that effective target. Thirteen of
40 source instances had an inconsistent potential answer. The simulated accurate
responder therefore was not accurate in those cases. Those original family rows
must not be used as valid task-outcome evidence.

`repair_scope.py` changes only the direct local answer to the effective task
preference, for the same 40 seeds. It preserves planner probabilities, all methods,
question costs, task targets and original traces. All 2,400 matched rows are
replayed into a separate directory. These are post-freeze corrected sensitivities,
not a new held-out study. The main dialogue experiment and other 348 synthetic
instances do not use this conditional fallback and are unaffected. The corrected
scope variables are correlated in the generative state. The planner's independent
factor approximation remains a limitation in these two families.

## Online confirmation after an earlier release

Frozen evaluation releases only once, after clarification stops. The interactive
protocol also allows someone to finish, then ask another question. Its original
`answer` updated beliefs but did not increment the version, so an earlier release
could retain an old value while still passing a version-only check. Explicit
`revise` already handled this correctly. This is a concrete online consistency
bug, not a new research mechanism.

`SafeProtocol` increments the specific record version after a resolved answer,
marks prior dependent releases for revalidation, and leaves unrelated releases
alone. The local desk uses this class. The frozen terminal-only evaluation remains
replayable without altered traces. Additional tests compare question choices and
terminal metrics against the frozen protocol to confirm that the correction has
no effect on the reported terminal-only comparisons. No new inference is needed.

The formal scope/version invariant applies to SafeProtocol, complete registered
dependencies and the release guard. It does not establish semantic interpretation
accuracy. Spontaneous user revisions remain separately logged public events; they
do not reset the budget for solicited clarifications. The UI now labels that
budget as a planned-question budget, rather than all possible user interaction.

## Applicability-record exceptions and the completed online audit

The final API review checked represented exceptions on a factor consumed only as an applicability gate. The frozen terminal guard checks value bindings, but did not apply an explicit allow/exception list on the gate record itself. None of the frozen empirical or synthetic cases has that configuration. The online SafePlanner now applies that guard to the gate as well, preserving the complete dependency graph so a later scope revision can restore an option. A focused test excludes a task through its scope gate and restores it only after an explicit revision. The actual received answer/revision is also named in the current record provenance, while earlier evidence remains visible.

The original frozen algorithm is unchanged. All 96 primary empirical preparations have identical question choices and terminal quality/demand metrics under the online repair. Planning counters can change because confirmation rebuilds caches; those counters are not asserted equal and the original measured costs remain in the research results. The first widened audit assertion incorrectly required equal cache-dependent node counts; its failed log is retained, and the corrected test compares the relevant behavioral invariant. The stronger minimum-completion rule is available as an additional interface selection through a public-only module with no evaluator imports.
