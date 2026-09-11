# Candidate and adaptation log

## Initial source audit, 2026-09-11 07:16-07:37 UTC

The worktree was clean at `3f843bee`. Created the newly requested research branch.
No submission files changed. The initial direct SSH invocation lacked the saved
known-hosts configuration. Reusing the recorded strict configuration authenticated
successfully. The existing RTX 6000 Ada BF16 server was verified without a model
restart or a separate placement generation.

Read MAC and AgentAsk methods and evaluations. Coordinating clarification is
already established. Read Mem0 and Zep update/invalidation methods and inspect
their released code. Versioned knowledge and dependency invalidation cannot be
claimed as a new algorithm. The useful empirical question is whether these simple
mechanisms survive imperfect extraction and stop stale *work* from being released.

## First adaptation checkpoint, 2026-09-11 07:37 UTC (21 minutes)

Probe A made 12 GPU calls on six development snapshots, two sampling seeds each.
Two responses were not valid JSON. Some valid responses contained an old price,
assistant-only evidence, wrong source turn numbers or invalid field names. A
four-call, separately declared format probe enabled JSON object constrained
decoding. All four returned parseable objects, while semantic and citation errors
remained. Adopt this format setting and normalize only declared schema aliases
(`cuisine`, `price_range`, `city centre`, `guest house`). Preserve every original
response. Exact source checks will not be presented as proof of entailment.

Probe B used four declared, authored task sets, two preparation workers and three
user response slots. Letting blocked tasks yield their worker slot matched or
improved the holding-cap baseline. Human-aware admission had fewer timely goals
than simple yielding in the urgent case (2 versus 3), tied in the shared bottleneck
(4 each), and helped in the long-preparation case (3 versus 2). It also completed
fewer total goals in the shared bottleneck (4 versus 5). These results do not
justify another scheduling method without evidence for its workload assumptions.

Select A: source-linked decision reuse with a release consistency check. Keep B
as a small falsifying probe. C supplies a view of changed dependencies in the UI,
not a separately evaluated summarization method. Add a **global version barrier**
as the strongest simple baseline. If it matches selective dependencies, recommend
the simpler implementation unless selective checking has a measurable cost benefit.

The source screen yields 8 development and 24 evaluation dialogues, stratified
equally by a retained preference change versus no retained change. Roles, fanout
and local artifact generation are authored. This is not an observed agent-fleet
or participant dataset. Selection is independent of generated outcomes.

## Second adaptation checkpoint, 2026-09-11 08:05 UTC (49 minutes)

The eight-dialogue development collection completed 96 scheduled calls. Together
with the two probes, this is 112 attempts, mean 2.733 seconds and p95 5.364 seconds,
with no transport failures or retries. Only the original unconstrained-format
probe had two unparseable outputs. No evaluation generations have started.

At the six-role cap and unlimited scripted responses, selective and global
version checking each completed 48/48 artifacts correctly and requested 40 extra
answers across eight projects. Semantic memory also completed 48/48, with 19
questions. Full history completed 47/48 with four questions. Records without a
release check completed 38/48 with 23 questions. Selective checks needed 51 repeat
reads versus 81 globally. This is a machine-read saving, not observed human effort.
The elaborate method is not necessary for development quality and is less frugal
than semantic memory. The final comparison must retain these strong alternatives.

Revision 2 adds conservative confirmation for explicitly conditional source
phrases and checks exception scope before reusing an answer. This is a limited
lexical guard, not a learned scope recognizer. Twelve authored natural-language
challenges will expose its limits separately from the dialogue study. A metric
repair counts stale retained answers as incorrect uses; earlier development CSVs
remain unchanged. Separate final-development outputs use the corrected accounting.
Source audit found three empty derived role instances in the test selection. They
will be inactive, never counted as completed goals. No case was dropped.

The local API initially exposed an honest preparation failure: the saved model
omitted the first dining preference and parsed the lodging-type question as
unknown. The demo therefore requires an explicit user answer before those drafts
can be prepared. Its source update and unknown-request behavior are retained,
rather than silently replacing model output with benchmark labels.

Freeze 24 distinct test dialogues, two generation replicates, role caps 2/4/6,
response budgets 0/2/6/unlimited, nine methods, and twelve authored scope challenges.
Primary outcomes are project correctness and extra questions for selective checks
versus semantic memory at the six-role cap with unlimited responses. No combined
utility or human-time model. The 672 additional calls forecast 30.6 minutes, or
45.9 minutes with a 50 percent margin. Proceed with this fixed comparison, then
finish the interface, inspect failures, plot and package. No tuning on final data.

## Final collection checkpoint, 2026-09-11 08:43 UTC (87 minutes)

The declared 672 new calls completed at 08:33 UTC. The session has 784 calls and
attempts, no retries or transport failures, and three unparseable responses
(including the two original development probe failures). All 5,184 controller
rows replay exactly. The 21 frozen hashes and all 18,759 historical tracked files
remain intact.

The primary whole-project outcome ties semantic memory on every one of 24
dialogues. Selective checking asks 1.875 more questions per project, with a paired
95% interval [1.041, 2.854]. Global checking has identical quality and questions.
The authored challenges reveal wrong transfers for a paraphrased exception and a
revocation under both structured methods, while full history handles all twelve
challenge cases in both replicates. These outcomes reject a broad claim that the
more elaborate record controller is a better automatic applicability method.

Inspecting the failed final artifacts found an adapter normalization issue:
`center of town` is semantically compatible with `centre`, but is not among the
frozen aliases and yields an empty local database result. Another source project
really retains an outdated expensive-hotel preference after a cheap-guesthouse
request. Keep both failures in primary results. Add a **post hoc, saved-output
sensitivity** that maps only this area alias in all methods, recomputes local
artifacts, and leaves every controller choice and user question unchanged. This
is a hypothetical adapter repair, not a replacement final evaluation.

The remaining analysis will classify errors, inspect the first cost-unfavorable
quality-tied case in source-ID order, and quantify the declared 0/0.25/1 source
inspection-equivalent sensitivity. No more model generations or method changes.
Online interface fixes for explicit manual overrides are separate from the frozen
simulation: they invalidate prepared work and roll back rejected scope changes.
They do not retroactively repair the natural-language challenge failures.

## Completion checkpoint, 2026-09-11 09:15 UTC

The complete prototype, evaluation and ten-page report are committed in
`8061aaf5`, following the pre-evaluation freeze `70299a02`. The final package
passes 24 new focused tests and 17 historical tests. All 5,184 controller runs,
120 challenge rows, 768 reconstructed prompt/seed/setting payloads, frozen and
post hoc numerical tables reproduce without network access or inference. The
source download helper verifies the exact selected bytes and all 33 development/
evaluation goal signatures, including the extra initial-probe dialogue.

The final area-alias sensitivity gives semantic memory and both version methods
274/282 correct artifacts and 46/48 correct project runs. Questions remain 58 for
memory and 148 for either version method. The frozen scores remain 267 versus
268 artifacts and 44/48 projects for both. No new generation or method tuning
followed the result. Five publication figures and the actual-browser screenshots
were inspected; the standalone report keeps figure captions attached and leaves
the submission untouched.

Temporary local server, browser and SSH tunnel are stopped. The existing remote
GPU model server was checked again and preserved. Stop with the simple-backend
recommendation rather than spending unused budget on another method variant.
Exact elapsed time and cumulative totals are finalized in the resource ledger.
