# Provenance, split and task audit

The empirical source is [MultiWOZ 2.4](https://github.com/smartyfh/MultiWOZ2.4), revision `6807c1d85f547fcaae10494d26991d2d37c90a63`. Its utterances are task-elicited human conversations. The hotel, restaurant and attraction databases are benchmark records. The repository distributes this pinned release under MIT; attribution and the license are retained under `artifacts/clarification_planning/data/`. This is neither observed fleet supervision nor an official MultiWOZ state-tracking score.

The source archive SHA-256 is `d4c66523614af016c1d2dafa35b4a548c96cb9ffadb71338937b60ac51272fe5`. `upstream_provenance.json` records exact download URLs and checksums. `verify_source.py` independently checks selected messages, annotated targets, lexical support, official split membership and the three databases against the archive. Full datasets remain outside Git. Saved selected data suffice for policy reproduction.

The complete current dialogue is public. Supported field names from the final annotation define the task interface, but annotated values are evaluator-only. A lexical-support check requires a supporting user utterance. Normalization reuses the earlier adapter and adds center/centre-of-town and guest-house forms during development. It is a fallible lexical filter, not a validated semantic entailment model. All agents receive the same public text and schema. No future user turn is held back and then passed to the planner.

A deliverable is one executable database shortlist for each supported domain. Its required fields are conjunctive constraints. Success requires both normalized constraint agreement with the source annotation and execution yielding the corresponding database matches. We deliberately do not treat a accidentally identical result from incorrect constraints as full success. Empty but correctly constrained results are valid completed query artifacts. This is not a reservation or a claim that a customer obtained a suitable trip. Constraints and task completion are a constructed adaptation of the dialogues.

Selection takes the first lexicographically eligible official validation/test IDs, with at least two supported domains and at most 4,500 source text characters. These rules precede held-out generation. It excludes 33 previously used or inspected source IDs, exact dialogue duplicates of those IDs and duplicate selected goal signatures. The initial development pilot used a broader screen; all 18 newly exposed development IDs remain excluded. Twelve final validation dialogues fit the estimator. Forty-eight fresh test dialogues, each with two generation replicates, form the evaluation. `audit.json` and `development_exposure_audit.json` disclose all IDs, exclusions and the initial revision. No held-out case was replaced after generation.

There are 152 eligible test candidates before final selection. The selected 48 contain 96 distinct domain shortlists and 191 constraints. Seventy-three shortlists require at least two fields. Across 96 generated preparations, 70 of 192 task preparations lack at least two memory values. This is an interpretation/guard limitation: the required preferences were already stated in the source. The condition does not measure naturally missing user information.

The final development set happens to contain hotel and restaurant cases only. The attraction reliability therefore uses the declared sparse-bin pooled fallback. Test combinations are hotel/attraction (12), hotel/restaurant (2), and restaurant/attraction (34). This distribution shift and the shared database/template structure limit calibration and generalization.

No source annotation establishes cross-domain decision authority. Consequently the primary adapter contains **zero shared factors across different deliverables**. Equal values are not merged. Multi-field completion can be studied, but the prevalence of legitimate shared decisions, exceptions and revisions cannot be inferred from this evaluation. Those mechanisms appear only in the separately labeled synthetic benchmark and local authored demonstration.

Each source dialogue is a statistical unit. Replicates are averaged before paired resampling. Source participant identities and template correlations are not fully available, so 48 dialogues must not be described as 48 independent human participants. Public benchmark contamination in model pretraining is unknown. Fresh here means unused in this repository's prior experiments, not proven absent from model training.

## Evidence hierarchy

| Quantity | Origin |
|---|---|
| Dialogue utterances | Task-elicited human source text |
| Current constraints and database records | Benchmark annotations and records |
| Domain-agent roles, deliverables and execution checks | Constructed adapter |
| Memory extraction and proposed answers | Actual GPU model outputs |
| Additional user answers | Simulated accurate responses from evaluator-only source labels |
| Response budget, error/defer weights and question penalty | Declared dimensionless research assumptions |
| Synthetic scopes, revisions, noise and dependencies | Authored generative conditions |
| Interface actions/screenshots | Scripted software demonstration, no participant data |
