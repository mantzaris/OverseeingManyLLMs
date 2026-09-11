# Decision dependencies: exploratory session plan

Authorized start: 2026-09-11 07:16:21 UTC. Hard stop: 10:16:21 UTC.
New inference stops by 09:46:21 UTC. This session is additional to all historical
clocks. No paid provisioning, model changes, training or historical reanalysis.
Work stays on `research/decision-dependencies`; the submitted paper is unchanged.

## User problem and candidate mechanisms

1. **Decision reuse and change handling.** A travel-planning user has already
   stated a preference. Several distinct deliverables need it, but a later change
   can invalidate prepared work. Test natural-language extraction, applicability,
   and release of work against current instructions. Compare with shared history,
   semantic retrieval, explicit records, and a simple version barrier. Memory
   updates, access scopes and dependency invalidation are established mechanisms.
2. **Admission of human-dependent work.** Regulate tasks before clarification
   requests arrive. A controlled probe must count all original goals, including
   work left unstarted. Reject a supposed benefit explained by a concurrency cap
   or perfect knowledge of future blockers.
3. **Resumption support.** Evidence-linked changes may help the interface but are
   not a second complete system. Generic summaries and existing provenance tools
   are strong alternatives. Do not claim improved human comprehension.

The first two probes examine natural-language decision reuse and a small
admission-control counterexample. The selection checkpoint will use their actual
findings. At most one main mechanism will proceed.

## Evidence and initial hypotheses

Use pinned MultiWOZ 2.4 human-authored, task-elicited travel dialogues. Development
comes from the official validation split; final cases from the official test
split. State annotations are evaluator-only and require a source consistency
audit. Agent roles, repeated requests, release events and attention costs are
constructed. The prototype has no booking authority and performs no transactions.

H1: Reuse can reduce repeated questions without increasing incorrect deliverables.
H2: Checking consumed decision versions at release reduces stale work after a
changed instruction. H3: selective dependency tracking reduces unnecessary
revalidation relative to a global version barrier. An equal-quality simpler
baseline falsifies a claim that a richer mechanism is necessary. Poor extraction,
scope transfer or confirmation costs may erase savings.

The independent unit is a source dialogue/project, never an agent request.
Hold all demand conditions and extraction replicates together in analysis.
Report project and artifact correctness, questions, incorrect reuse, revalidation,
propagated errors and model/controller cost separately. No human workload claims.

## Resource and adaptation rules

At most 1,500 actual generation attempts including diagnostics and retries, serial
requests on the existing pinned Qwen2.5-7B BF16 GPU server. Each ordinary call has
at most one retry and a 60-second attempt timeout. Raw attempts are retained. The
ceiling is not a target. Measure a small pilot before freezing the final matrix.
No replacement of failed cases. Preserve both development revisions and failures.
Freeze source IDs, prompts, methods, metrics, seeds and analysis before final
generations. Any later repair gets a separate, explicit audit trail.

Reserve the last 30 minutes for verification, plots, documentation and commits.
The local interface will expose answers, their source and scope, dependent work,
uncertainty, request-only answers and explicit changes. Interaction logs are
development demonstrations, not participant observations.
