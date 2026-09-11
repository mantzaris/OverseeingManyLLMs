# Novelty assessment and competing explanations

The useful question is not whether agents can share memory. They can. It is
whether a person can see the scope of an earlier answer, reuse it appropriately,
and identify work that no longer agrees with a changed instruction.

| Candidate | User problem and mechanism | Closest explanation | Distinguishing test and falsification |
|---|---|---|---|
| A. Reusable decisions with change handling | Agents ask repeatedly or release work based on old preferences. Source-linked records and a release check make the consumed instruction explicit. | MAC coordinates clarification. Mem0/Zep update memory. Truth maintenance and incremental builds invalidate dependencies. A shared state tracker with a version barrier may suffice. | Use actual dialogue utterances and fallible extraction, then compare final artifacts and additional questions against full history, semantic memory and simple records. No benefit over simple records falsifies the need for the richer graph. More clarification without a quality improvement argues for simplification. |
| B. Control human-dependent work admission | Agents create a queue of blockers before the user is available. Start independent preparation when possible. | Admission control, yielding blocked workers and ordinary concurrency limits. | Count every original goal, including unstarted work. Our controlled probe found a simple yielding baseline strong and an urgent case where human-aware admission did worse. The result does not justify a new controller under these assumptions. |
| C. Evidence-linked resumption | A returning user cannot locate new decisions or changed assumptions. Show a delta from the last inspection. | HiLSVA already provides provenance, reusable feedback and concurrent session awareness; generic summaries are strong alternatives. | Would require decision-identification and evidence-retention comparisons plus actual interaction observations for comprehension claims. Use change receipts as an interface view supporting A, not a separately claimed summarization contribution. |

Selected mechanism A is a **testable application of established consistency
techniques**, not a new scheduling or memory algorithm. The live interface makes
the scope explicit and lets the user supply exceptions, revise or revoke answers.
The evaluation asks whether that contract is useful when natural-language inputs
are imperfect. A perfectly structured fixture establishes an invariant only.

The strongest simple baseline is a global version barrier. If a new conversation
epoch causes it to reread all current inputs, it should have the same final values
as selective dependency checking. Selectivity can save machine reads. Without
measured user interaction, it cannot establish less reading, fewer context
switches or lower mental workload. The prototype should not retain complexity
merely because its dependency diagram looks sophisticated.

There are two further alternative explanations. First, source rejection may
improve correctness by asking an assumed accurate user more often. That is a
quality-demand tradeoff, not free improvement. Second, the all-memory baseline
may already recover the answer cheaply. It receives updated memories, not a
deliberately stale or unscoped bag of strings. Full history is included separately
because these source conversations fit in a small context much of the time.

The currently defensible contribution is an auditable prototype and an empirical
test of these alternatives on source-grounded dialogue projects, including
incorrect transfers and changes of instruction. Whether this becomes a paper
contribution depends on the final evidence and later interaction evaluation.
No priority claim is made for shared decisions, scope checking, interruption
management, provenance or dependency invalidation.

## Assessment after the frozen comparison

The broad benefit hypothesis did not survive the comparison. Selective checking
and semantic memory tied on whole-project correctness in every one of 24 final
dialogues, while selective checking requested 1.875 more answers per project
([1.041, 2.854] paired 95% interval). The global version baseline matched selective
quality and question counts in every condition. Its additional machine reads are
too cheap here to support a user-attention argument. On the authored challenges,
the simpler full-history method understood a paraphrased exception and revocation
that the structured extractor failed to represent.

The one-artifact primary accuracy advantage over memory came from an adapter
normalization difference, not superior handling of an instruction change. A
separately labeled post hoc normalization makes both methods' artifact quality
equal while preserving the additional questions. The frozen result remains intact.

Recommend **simplification**. Keep explicit user scope, source receipts and change
impact in the local interface, backed by competent shared context and an ordinary
global release check. Do not claim a new automatic memory algorithm, a reliable
scope recognizer or reduced cognitive load. The testable follow-up concerns
whether people can supply and revise intended scope more accurately with those
controls than with the same backend and a conventional conversation view. The
current work belongs in follow-up research, with the completed submission intact.
