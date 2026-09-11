# Budgeted clarification planning: completed research evaluation

Two-step planning avoids a measurable failure of one-step clarification, but this application does **not** establish an overall practical advantage for the more elaborate planner. A stronger completion heuristic matches its loss with fewer additional user answers. Full-history interpretation also removes much of the need to ask again. The appropriate contribution is a tested decision protocol, a bounded algorithm, and a carefully limited mechanism result.

## What was implemented

A public task/decision graph connects distinct deliverables to required values and applicability conditions. Decisions retain source, represented scope, exceptions, status and version. The planner considers stopping, releasing sufficiently reliable work, and deferring unfinished work. It ranks small complementary dependency blocks, evaluates contingent sequences at depths one to three, executes the first atomic question, and replans from the received answer. An independent exact recursion checks small instances. Caching, width eight and a 25,000-state expansion limit bound the practical search. No general optimality guarantee is claimed.

The local Decision desk makes the method selectable. It shows the next question, potentially enabled work, scope, a possible need for another answer, remaining response budget and deferred items. Users can answer narrowly, override selection, leave a question unresolved, revise an instruction or revoke it. Actual displayed questions and interactions are logged and replayable. The demonstration has several distinct publishing roles and an exceptional partner export; it does not perform consequential external actions.

The frozen mathematical specification is [METHOD.md](METHOD.md). Its online version invariant is qualified by the isolated fix in [SEMANTIC_AUDIT.md](SEMANTIC_AUDIT.md). [API.md](API.md) describes direct integration. The separate draft is [main.pdf](../../paper/clarification_planning/main.pdf); historical submission files are unchanged.

## Design and evidence

The freeze at commit `397c7a32` preceded held-out generations. `artifacts/clarification_planning/frozen/` contains method/source snapshots, prompts, hashes, estimator, case selection, policies, budgets, seeds and statistical definitions. Primary comparisons are depth two minus one-step VoI and minus semantic memory at response budget two, with error weight four and unfinished weight one. Question penalty is 0.05 loss units per answer. Loss, correctness and questions are reported separately.

The empirical data are task-elicited human MultiWOZ 2.4 dialogues, with benchmark annotations and databases. Our two-agent domain-shortlist tasks, budgets and additional user responses are constructed adaptations. Source values are evaluator-only. The complete conversation and task field names are public. Evaluation uses 48 fresh repository-unused test dialogues and two GPU interpretation replicates. Each dialogue supplies two genuinely distinct domain shortlists. Twelve development dialogues fit the estimator; all 18 exposed development cases and all 33 historical source exclusions are disclosed. Cases were selected in fixed source order without inspecting model outcomes. There were no replacements.

The unit of paired analysis is a dialogue, averaging its two replicates before 2,000 bootstrap resamples with analysis seed 82164. Database/template dependence and unknown source participant overlap limit independence claims. Fresh source IDs do not establish absence from model pretraining. [DATA.md](DATA.md) describes inclusion, provenance, transformations, exclusions and the evidence hierarchy.

Actual GPU generations use pinned Qwen2.5-7B-Instruct revision `a09a35458c702b33eeacc393d103063234e8bc28`, BF16, one RTX 6000 Ada, temperature 0.3, top-p 1, serial calls and zero CPU offloading. We reuse the healthy existing server. Three calls prepare each replicate: source-linked extraction, answering from all current accepted memories, and full-history answering. Output limits are 640/256/256 tokens within the existing 2,048-token context. All controlled planning policies reuse the same saved memory answers. Full history is a separate interpretation comparison, not a pure planning ablation. Every simulated user response costs one atomic decision; combining display cards does not reduce that accounting.

## Primary empirical results

Totals below cover **96 preparations, 192 task preparations, and 48 statistical units**. Whole projects require both domain tasks correct. These counts must not be interpreted as independent policy samples.

| Method | Terminal loss | Correct tasks | Wrong releases | Unfinished | Whole projects | Extra answers |
|---|---:|---:|---:|---:|---:|---:|
| Semantic memory |72|129|3|60|41|160|
| Full history |82|140|10|42|45|3|
| One-step VoI |86|112|2|78|37|132|
| Declared fewest-answers completion |77|118|1|73|22|192|
| Two-step planner |63|135|2|55|39|177|
| Minimum sufficient completion, secondary audit |62|139|3|50|44|135|
| Ideal interpretation diagnostic |0|192|0|0|96|0|

Planner-minus-baseline mean paired terminal loss, with marginal 95% bootstrap intervals:

| Comparison | Difference per dialogue | Interval | Planner wins / ties / losses |
|---|---:|---|---|
| One-step VoI, primary |−0.2396|[−0.3646, −0.1146]|17 / 29 / 2|
| Semantic memory, primary |−0.0938|[−0.2188, +0.0104]|6 / 40 / 2|
| Declared completion, secondary |−0.1458|[−0.2708, −0.0104]|9 / 38 / 1|
| Full history, secondary |−0.1979|[−0.5625, +0.1354]|11 / 26 / 11|
| Minimum sufficient completion, post-freeze audit |+0.0104|[−0.1146, +0.1042]|1 / 44 / 3|

Depth two completes 23 more tasks than one-step with the same two wrong releases, but needs 45 more answers. Against semantic memory, six extra correct tasks and one fewer wrong release come with 17 extra answers and two fewer complete projects. These are objective tradeoffs, not general superiority.

### The stronger simple comparator

The frozen completion rule counts every still-queryable factor, including uncertain supplied values that may not need confirmation. [ANALYSIS_ADDENDUM.md](ANALYSIS_ADDENDUM.md) records a secondary audit of this limitation before the completed summary tables were inspected. Minimum sufficient completion finds the cheapest affordable dependency subset that makes a deferred task releasable under every modeled response path, then breaks ties by expected task loss saved per cost. It ignores already releasable tasks, executes one question, and reconsiders. It receives no evaluation targets, additional generations or special release rule.

Its loss of 62 versus 63 for the planner is accompanied by 42 fewer answers. Planner-minus-audit questions are +0.4375 per dialogue, interval [+0.3021,+0.5729]. The audit completes four more tasks and five more projects, with one additional wrong release. A wide loss interval is not proof of equivalence. Nevertheless, this result is strong evidence against attributing practical value to the additional contingent search in these tasks. This audit reuses inspected preparations and is not a new confirmatory result.

### Which mechanism occurs in the source adaptation?

Seventy-three of 96 source tasks require multiple fields. Across generated replicates, 70 of 192 task preparations lack at least two memory values. Depth one and two choose different initial actions in 47/96 preparations, spanning 25/48 dialogues. Depth one stops while depth two asks in 21 preparations across 13 dialogues. This is direct evidence for myopic stopping on conjunctive completion under the chosen beliefs.

However, **every required value was already stated in the source dialogue**. The apparent information gap is caused by interpretation and the source guard. Extraction supplies 148/382 field preparations, memory 160/382, and full history 379/382. Conditional correctness is 147/148, 152/160 and 363/379 respectively. The guard rejects 143 extracted records. Before any answer, the mean predicted two-step net benefit is 0.9965 versus realized 0.9703; the mean absolute difference is 0.1234 across preparations. Four of 96 preparations have negative realized net benefit. These descriptive values include the 0.05 question penalty and do not establish individual calibration. Conditional Brier scores are 0.01551, 0.04945 and 0.04373. Coverage must accompany those scores; missing values are not successful predictions.

The final development set has no attraction examples. That domain uses the preregistered pooled fallback. The evaluation contains 12 hotel/attraction, 2 hotel/restaurant, and 34 restaurant/attraction dialogues. This shift weakens confidence in the small risk model.

There are **zero annotated cross-task shared decisions** in the main adapter. We did not invent authority from equal values. Scope-disabled and request-specific ablations therefore tie mechanically. Generic depth-two search also ties because all source-derived candidate sets fit in width eight. Depth three cannot improve on depth two at budget two. These conditions do not substantiate the distinctive candidate ranking or the practical frequency of legitimate shared scope.

### Generation variation

With the two independently seeded generation replicates, accepted extraction values differ on 19 fields across 13 dialogues. Memory answers differ on 21 fields across 14 dialogues; full-history answers differ on four fields across four dialogues. These are different-seed preparations, not repeated identical requests. Memory prompts can also differ because their extracted records differ. Under depth two, replicate losses differ in three dialogues (replicate-one minus replicate-zero range −3 to +3); under one-step they differ in eleven (−4 to +3). `generation_variation.csv` and `replicate_variation.csv` retain all cases. Replicates remain inside their source dialogue for inference.

### Objective sensitivity and negative findings

At error weight two, full history outperforms the planner: planner minus full-history loss is +0.2604 per dialogue, interval [+0.0417,+0.4688]. At error weight eight the difference reverses to −0.8333 [−1.1250,−0.5417]. Full history's three questions versus 177 for the planner are important regardless of the selected loss weight. Perfect annotation interpretation completes all tasks without questions. Better interpretation is therefore a strong competing solution.

`analysis/paired.csv` reports all declared budgets, weights and contrasts. The study does not choose a favorable weight after seeing evaluation data. There is no multiplicity correction; the two primary marginal intervals and all secondary results should be interpreted accordingly.

## Synthetic evidence and semantic repairs

The frozen synthetic batch has 14 families × 20 seeds and 9 overlap/arity configurations × 12 seeds, totaling 388 configuration/seed instances and 23,280 replay rows. Seeds repeat across configurations; these are not 388 independent real projects. Families include independent requirements, legitimate sharing, complements, mixed tasks, scope exceptions, wrong sharing, revisions, revocation, noisy and unresolved answers, sufficient memory, zero value, candidate distractors, and misspecified beliefs.

The transparent budget-two fixture has three distinct deliverables needing q1 and q2, plus one independent deliverable needing q3. One-step and the declared completion rule ask q3 and retain loss three. Depth two asks q1 and q2 and retains loss one. Marginal task benefit increases from zero to three, disproving diminishing returns for this objective. This authored witness establishes possibility only.

Independent and already-sufficient-memory families tie at budget two. Several noisy, unresolved and scope comparisons also tie. A local value answer can substitute for a scope question. The full-overlap/arity-two map favors depth two, whereas insufficient budget for three required answers restores a tie. At budget four in the full-overlap, three-required-answer grid cell, depth two is worse than the simple completion heuristic by three loss points. The heuristic follows through on a three-answer requirement that the two-step horizon cannot value. This negative case remains visible in the right heatmap; increasing the total response budget alone does not fix a short planning horizon. The twelve-factor distractor fixture favors dependency ranking over an equally bounded generic search, but no equivalent empirical candidate pressure occurs here.

The original two scope-family responders could return a fallback value inconsistent with the task's effective preference. Thirteen of 40 instances had an inconsistent potential local answer. We retain those original traces, label their outcome evidence invalid, and separately replay the same seeds with consistent local answers. `scope_consistency_repair/` holds 2,400 corrected rows. Valid summary tables use 348 original instances plus these 40 post-freeze repaired sensitivities. The empirical data and all other synthetic families are unaffected. The repaired scope variables are correlated, so the factorized planner remains an approximation there.

Two-step planning matches the independent exact same-depth reference in 220 small comparisons at each tested width, with no positive gap beyond floating-point tolerance. This is a finite check. A separate authored six-factor width-two witness has an approximation gap of 1.2 when pruning removes a useful complementary pair. No optimality or submodular guarantee is claimed. No reported run reaches the 25,000-state limit.

## Cost, failure and reproducibility accounting

The inference ledger contains **396 calls, 396 attempts, zero retries, zero transport failures and zero unparseable calls**. Development accounts for 108 calls over 18 exposed cases; held-out preparation accounts for 288 calls over 48 dialogues. Token usage is 174,262 prompt plus 25,545 completion, totaling 199,807. Summed request latency is 604.67 seconds. The saved server counter increments match these totals. No placement generation, paid instance, credential change or model search was used.

Full-history and memory interpretation errors, guard rejections, unfinished tasks, wrong releases and unresolved synthetic responses remain in the principal accounting. They are not transport failures. The initial source-screen revision, a JSON scalar serialization failure, plotting compatibility failures, a browser assertion correction and the isolated semantic repairs remain in logs. No historical outcome was replaced.

Mean measured empirical episode CPU time is 1.335 ms for depth two, 0.645 ms for one-step and 0.553 ms for declared completion. Synthetic depth two averages 6.706 ms and depth three 27.893 ms. `costs.csv` retains original measured timings; deterministic replay does not pretend to reproduce latency.

`resource_ledger.json` records this separately authorized session beginning 2026-09-11 13:05:24 UTC, its 16:05:24 deadline, final elapsed time, cumulative calls and elapsed time since the original 36-hour clock. Fresh inference finished at 13:37:45 UTC. No historical authorization was altered. Cumulative wall time includes inter-session idle gaps and explicitly exceeds the old target under later authorization. Provider billing rate, accrued charge and remaining purchased allocation are unavailable; request latency is not used to invent billing costs.

The full replay verifies 17,280 empirical rows, 23,280 original synthetic rows, 1,728 stronger-completion audit rows and 2,400 scope-repair rows: **44,688 rows**, with no new inference. It reconstructs all 396 exact model requests and 132 preparation files, checks frozen hashes and estimator integrity, reproduces paired statistics, and replays displayed UI interactions. A separate upstream-archive check verifies the selected messages, target derivation and database copies. Focused tests cover budget paths, information isolation, scope/exception handling, revisions, the complementary fixture and exact references. Forty-one historical tests passed once without new inference or expensive unrelated audits.

## Visual evidence and recommendation

The figures directory contains PDF, SVG and high-resolution PNG exports for ten plots: dependency example, correctness/budget, wrong/unfinished components, paired differences, overlap/arity map, ablations, risk/benefit diagnostics, computation/gaps, matched question sequences, and quality versus answers including the stronger audit. Favorable, tied and unfavorable examples use the first lexicographic qualifying dialogue by replicate-averaged loss. The frozen display initially specified replicate zero; the final plot expands it to both replicates without changing which dialogues qualify. Both replicates are shown, so an effect cannot be hidden by showing only the more convenient replicate. Six interface screenshots and their scripted interactions are preserved.

The supported paper claims are a scope-aware budget protocol, a formal and observed myopic-stopping failure, explicit bounds and approximation limits, and evidence that a simple completion rule can remove the practical case for deeper search. The study does **not** establish reduced human cognitive load, broad empirical benefit from scope acquisition, or a generally superior new planning algorithm. Classical nonmyopic elicitation is the closest theoretical explanation; minimum sufficient completion and full-history interpretation are the strongest practical explanations.

Develop this as follow-up work rather than replacing the completed submission. Use minimum sufficient completion as the practical default and retain the planner as an experimental option. The single next useful step is to evaluate both on a small collection of real multi-deliverable projects with independently justified shared decisions and exceptions, while measuring source interpretation coverage before asking the user again. That would test the currently missing application premise instead of adding another favorable synthetic configuration.

## Final verification and closure

The separately authorized session ran from 2026-09-11T13:05:24+00:00 through the accounting checkpoint 2026-09-11T14:46:57.582360+00:00: **1h 41m 34s**, within its three-hour limit. Cumulative wall time since the original start is **47h 8m 1s**, including idle gaps, or **11h 8m 1s beyond the historical 36-hour target**. This continuation is not backdated into that window. Cumulative inference accounting is 56,766 scheduled calls, 56,768 attempts, 31,333,955 prompt tokens and 787,378 completion tokens. The session itself used 396 calls/attempts and 199,807 tokens, with no retries or transport failures.

Final verification passed 27 focused tests, 41 historical checks, 15 browser checks, 19 displayed interaction replay events, all 44,688 policy/audit rows and all 24 numerical analysis tables. A clean detached checkout of the research milestone reproduced the frozen package; final online-accounting and descriptive-analysis additions were verified separately. The detached checkout was removed. All 16 manuscript pages were rendered and visually inspected, with no overflowing boxes or undefined references. Ten figure sets have PDF, SVG and PNG exports.

The temporary local desk and SSH tunnel are stopped. The existing GPU server was healthy (HTTP 200, pinned model identity) before tunnel closure and remains running. No paid resources were provisioned. The repository changes are confined to the new research, artifact and standalone-paper namespaces. Milestones are the pre-evaluation freeze `397c7a32` and completed research `e4f2793a`, followed by the final verification/accounting commit on main. Nothing was pushed.
