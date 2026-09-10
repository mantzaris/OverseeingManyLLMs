# Retail source and adaptation record

This is an **adapted τ-bench study**, not an official τ-bench score. The upstream
repository warns that later benchmark versions contain task fixes. We pin the
requested τ-bench source, audit selected target transactions, and make no claim
to reproduce a current leaderboard. MIT attribution and unmodified source are
in [the vendored package](../third_party/tau_bench/UPSTREAM.json).

| Component | Inherited source | Stage 5 use or modification |
|---|---|---|
| Database | `tau_bench/envs/retail/data/{users,orders,products}.json` | Independent account copies retain all that customer's orders and the complete product catalog. All records are simulated. |
| Tool implementations | Nine authentication/retrieval and cancellation/item-modification/return/exchange tools | Invoke upstream functions unchanged. Preserve status, inventory, product compatibility, item multiplicity, payment and gift-card-balance guards. |
| Retail policy | `wiki.md`; `rules.py` retained | Full policy is in the model prompt. Added deterministic authentication, ownership, prior-retrieval, nonempty-transaction and exact-confirmation guards apply to every condition. These guards do not check the hidden target. |
| Task records | `tasks_train.py`, original indices | Fixed feasible single-transaction subset, 24 development and 96 evaluation cases. All 120 customer accounts are distinct. Selection is by source index within family, not model errors or scheduler wins. |
| Task validator | `Env.calculate_reward`, `to_hashable`, `consistent_hash` | Reproduce the upstream final-database hash comparison on account-isolated states. Selected tasks have no separate required textual outputs. Store source and target hashes; test each annotated transaction. |
| Scripted customer | Original instruction text | Remove personality directions; expose only original operational information. Repeat it when asked. Explicitly confirm the displayed proposal without independently resolving backend IDs. No LLM user simulator or extra hidden action IDs are provided. |
| Tool serialization | Upstream parameter schemas | JSON tool envelopes with reported confidence; explicit confirmation and finish interfaces. One tool call per model turn. Longer context and output cap declared separately from maintenance. |
| Review opportunity | Our extension | Guarded proposed mutation is staged without changing the database. Three independently prepared transactions enter a processing batch at public slots 0/0/1. |
| Processing cutoff | Our extension | Public relative windows 2/4/5 represent order-processing, change-lock or reverse-logistics batch cutoffs. A completed review commits its corrected transaction immediately; otherwise the staged proposal posts at the cutoff. Completion exactly at cutoff is timely. No later rollback is allowed. |
| Simulated reviewer | Our idealization | One nonpreemptive reviewer, duration 2 (primary) or 1 (secondary). Only a completed review may use the private annotated target and correct the full transaction. Preparation failures without a valid staged transaction cannot be rescued. |
| Operational objective | Our declared points | Four points for an unresolved service request, plus a public 4/8/12-point processing/rework consequence for a wrong posted transaction. These are synthetic consequence weights, not observed dollars or actual retailer penalties. |
| Paired policy evaluation | Our design | Reuse the same GPU-prepared transactions across all policies/capacities because no model generation follows staging. Three fresh workflow replicates measure generation variability. This does not test feedback-dependent multi-job agent behavior. |

Exact task IDs, original instructions/actions, exclusion reasons and partition
groups are in [cases.json](../artifacts/stage5_practical/cases.json). A first
pre-inference selection bug admitted repeated customers; its failed declaration
is preserved and the unique-account test repaired it before any generation.
Broad workflow templates are shared across partitions, so this is held-out
**source-case** evaluation, not held-out workflow-template generalization.

Automatic validation prevents structurally invalid transactions. Review can
additionally address a valid but unwanted product variant, omitted requested
items, wrong valid refund method, or incorrect cancellation reason. We report
blocked policy attempts separately from committed semantic errors and database
task completion. The scripted customer's confirmation is deliberately not an
independent semantic validator; this limits realism and may overstate the
additional value of a perfect reviewer.

The flat cutoff benefit is derived directly from the declared objective:
`p(error) * (service_failure_cost + wrong_transaction_cost)` if review finishes
by the cutoff, and zero afterward. Failed unstaged workflows have no eligible
request. Search sees only arrived public requests and enumerates all ordered
subsets, at most 16 with three requests. No maintenance downtime formula is used.
