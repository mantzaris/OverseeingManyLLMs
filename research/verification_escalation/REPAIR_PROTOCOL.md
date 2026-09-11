# Corrected, disjoint follow-up

The first frozen experiment used unordered tables for every request, including
explicit ranking requests. This violates the original request in cases 2842 and
2863 (four replicas). Its global prompt also said ordering was not required.
The initial rows, responses and figures remain in their original locations. They
are a flawed-adapter diagnostic, not the principal valid study. No historical
experiment before this new module is affected.

The repair derives `contract.ordered` from released request/source text, using the
regex in repair_data.py, before generation. All policies receive the same repaired
contract. Generated prompts now require respecting explicit ordering. References
and candidates are compared under that identical contract. The controller and
its conservative agreement rule are otherwise unchanged. Other source-reference
projection ambiguities remain a scoring limitation: exact table mismatch is not
necessarily a semantically incorrect answer. Report reference-table agreement,
wrong releases under that declared contract, and concrete semantic failures.

Freeze a new source-disjoint set of 24 test databases, eight per ambiguity type,
in original source order after excluding all 57 previously used databases. Two
replicas use the original fixed intent-offset rule. Source-recovery diagnostic:
first two of eight cases per type, six databases, two replicas. No generated
outcomes determine inclusion. No calibration or policy tuning is performed.

One hundred fifty-six further calls (24*2*3 + 6*2) bring the session total to
540 scheduled calls, below its existing 600-call ceiling. Reuse the same GPU,
authorization, timeout, attempt ceiling and cutoff. No historical clock resets.

The main contrast, answer budgets 0/1/2, methods, loss weights and paired analysis
remain as previously declared. The source database remains the unit, replicas
averaged first. These new outcomes are the valid principal follow-up. Report the
first run's findings separately, with the affected ordering defect explicit.
Synthetic final results remain valid because their public contracts concern
unordered snapshot tables and do not include ordered requests. Add focused tests
for ordering detection, ordered table comparison and replay before the new freeze.
