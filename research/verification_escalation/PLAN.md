# Bounded exploration and frozen comparison

Authorized start 2026-09-11 23:08:26 UTC. End 2026-09-12 02:08:26 UTC;
new inference stops by 01:23:26 UTC. Historical clocks are unchanged. Initial
ceiling 600 scheduled calls and 1,200 attempts, one retry, existing RTX 6000 Ada
only. Reserve the last 45 minutes for reporting and verification.

Primary question: does conditional outcome verification reduce substantive intent
answers relative to source recovery plus minimum sufficient completion, while
retaining correct completed table artifacts? Report each outcome, not a claim of
noninferiority from an insignificant difference. No noninferiority margin is used.

AMBROSIA is selected after the access audit. Human annotators authored requests
and interpretations; databases were model-generated with human filtering. This
is an externally authored benchmark, not observed production data. The study uses
48 distinct test databases, 16 per ambiguity type, in source order after excluding
nine development databases. Two generation replicates also rotate the intended
reference using a fixed hash offset. More than two reference alternatives remain
in coverage analysis but two replicas cannot test every intent per case.

Three conditions: generated candidates primary; privileged reference alternatives;
and a source-recovery diagnostic on the first four cases per type, making the
human-written clarification available as a scoped prior instruction. The last is
our constructed availability condition, not an original dialogue observation.
No source annotations establish shared decisions across tasks. Shared dependencies
and parallel continuation are tested only in the separately authored SQL workloads.

Budgets 0,1,2; ten policies listed in controller.py. Primary comparison is
verification minus recovery_completion at budget 1 for answers, correct artifacts,
wrong releases and unfinished work. Depth two is the secondary algorithm baseline.
Loss 4*wrong+unfinished is descriptive; also report weights 1,2,8 in analysis.
Average replicas within database before paired bootstrap, 2,000 resamples, seed
86421. Report direction, intervals and win/tie/loss counts. No favorable-case
replacement or adaptive stopping. A failure remains one planned case.

Synthetic final seeds 7200..7215 in all 17 declared families. Seeds 7000 and
7100..7115 are development. Preserve the accidental early full development run;
it is not a frozen evaluation. Agent labels have no utility or policy effect.

Models: pinned Qwen2.5-7B BF16, temperature .3, top_p1, 2048 context, serial,
512-token candidates and 256-token answered SQL. Every empirical replica has
2 public generation calls and 1 potential clarified-response call, cached and
shared by all policies. The 12 recovery cases use one additional call per replica.
Expected evaluation generations: 312. They include cached response branches that
some policies never consume. No answer branch is visible before a charged question.

Freeze source IDs, code, prompts and this method before held-out generation.
All outputs and malformed responses retained. No model-based verifier grades its
own semantics. Reference execution occurs exclusively in evaluator code. Public
release checks are structural/execution/provenance checks, not a hidden SQL oracle.

Select first lexicographic favorable/tied/unfavorable source case by average loss,
show both replicas. If a category is absent say so. Synthetic counterexamples are
selected by predeclared family, never presented as empirical prevalence.
