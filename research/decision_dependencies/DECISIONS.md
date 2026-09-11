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
