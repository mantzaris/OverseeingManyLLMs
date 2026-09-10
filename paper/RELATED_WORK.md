# Verified related work

Verified from primary author/publisher pages on 2026-09-10. This is a focused positioning note, not a systematic literature review. Abstract-level verification supports only the claims below; it does not establish priority over all prior work.

- **Ren et al. (2023), _Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners_ (KnowNo), CoRL.** KnowNo uses conformal prediction to decide when an LLM planner should request help, with statistical task-completion assurances under its assumptions, evaluated in simulated and real robot settings. Our experiment instead fixes request admission and studies how one finite-duration simulated supervisor orders pending requests with correction deadlines. We provide no conformal coverage guarantee. [Author manuscript, verified v2](https://arxiv.org/abs/2307.01928).
- **Alves et al. (2024), _Cost-Sensitive Learning to Defer to Multiple Experts with Workload Constraints_ (DeCCaF).** This work models expert error and uses constraint programming for cost-sensitive deferral subject to expert workload limits, with synthetic fraud-analyst experiments. Thus cost-aware allocation under limited expert capacity is established prior work. Our distinction is an online maintenance simulation with accumulating costs, deadlines, fresh LLM actions, and feedback histories. [Author manuscript, verified v3](https://arxiv.org/abs/2403.06906).
- **Hariri, Potts, and Van Wassenhove (1995), _Single Machine Scheduling to Minimize Total Weighted Late Work_, ORSA Journal on Computing 7(2):232–242.** This paper develops scheduling algorithms, including branch and bound, for weighted late work. Its late work is processing performed after a due date; that is different from our erroneous-action downtime before correction plus an incorrect-closure penalty. The connection is time-dependent weighted scheduling loss, not equality of objectives. Exhaustive scheduling is not our novelty claim. [Publisher record and abstract](https://pubsonline.informs.org/doi/10.1287/ijoc.7.2.232).
- **Guo et al. (2022), _Pareto-scheduling with double-weighted jobs to minimize the weighted number of tardy jobs and total weighted late work_, Naval Research Logistics 69(5):816–837.** This studies a scheduling tradeoff between tardy-job counts and weighted late work. It motivates distinguishing count and cost objectives; our incorrect-closure count and maintenance loss are different quantities and our finite grid is not a Pareto-optimality result. [Publisher record and abstract](https://onlinelibrary.wiley.com/doi/abs/10.1002/nav.22050).

The candidate contribution is an auditable experimental framework and analysis of interacting risk estimates, supervision capacity, workload, and objective choice in synthetic LLM oversight. It is not a new exact scheduling algorithm, a human-performance measurement, or evidence of general LLM alignment. Claims about the experiment must be supported by its held-out scenario results and bounded to its single model and synthetic observation process.

## Practical-application positioning (Stage 5)

The following papers and their linked implementations were checked on
2026-09-10. Exact repository revisions and inspected-file hashes are in the
[source verification record](../artifacts/stage5_practical/sources/verified_sources.json);
[BibTeX entries](references.bib) use verified author/title metadata.

| Work | Mechanism and verified code | Relationship to this study |
|---|---|---|
| [τ-bench, Yao et al. (2024)](https://arxiv.org/abs/2406.12045) | Stateful retail/airline tools, policy-following interaction and final-state validation. [Released source](https://github.com/sierra-research/tau-bench/tree/59a200c6d575d595120f1cb70fea53cef0632f6b) inspected directly. | We reuse retail tools, policy, records and validator semantics. Scripted users, transaction staging, shared review and cutoffs are adaptations. No official score. |
| [One Human, N Agents, Zavattari et al. (2026)](https://arxiv.org/abs/2607.28317) | Budgeted noisy auditing of a fleet, confidence miscalibration and correlated errors; synthetic experiments and saved-trace allocation. No author-linked released code was located in the paper or exact-title/author search. | Shared oversight is already explicit prior work. Our retail condition studies finite-duration correction before posting, rather than a per-round detection budget. This is a conceptual comparison, not a reproduced baseline. |
| [Value of Information, Dong et al. (2026)](https://arxiv.org/abs/2601.06407) | Clarification value balances expected decision utility against question cost. [Released code](https://github.com/dong-river/VOI_communication/tree/27466a7832d5aafff82017a659e08942e18b01ae) includes flight and mixed-20Q implementations; the inspected flight function computes expected posterior value minus current value and question cost. | Our intervention benefit likewise expresses value in an explicit objective, but allocates a fixed reviewer among staged requests. We do not implement their belief/clarification mechanism. |
| [KnowNo, Ren et al. (2023)](https://arxiv.org/abs/2307.01928) | [Released notebooks](https://github.com/google-research/google-research/tree/9850ffb9352e34676ed8113a70aa85cb3aee416b/language_model_uncertainty) calibrate a quantile threshold, form option sets and trigger help for nonsingleton sets. | Request admission and conformal coverage differ from queue ordering. Our uncertainty-first baseline ranks empirical application risk; it is not KnowNo and provides no conformal guarantee. |
| [DeCCaF, Alves et al. (2024)](https://arxiv.org/abs/2403.06906) | [Released implementation](https://github.com/feedzai/deccaf/tree/b910b48d7e146d53b5f145224b819bdb0962d40a) combines learned expert correctness with OR-Tools CP-SAT allocation and capacity constraints. | Cost-aware deferral and global allocation are established. We test timed transaction correction with a shared idealized reviewer; DeCCaF's learned heterogeneous experts are not implemented here. |

Our implemented comparisons isolate arrival order (FCFS), urgency (EDF), risk
ranking (uncertainty-first), immediate expected avoidable loss (greedy), and
joint ordering of the currently visible queue (search). No review keeps the
same automatic safeguards. These are mechanism baselines, not claims to
reproduce the full cited systems. The practical contribution sought is the
application adapter and controlled evidence about when queue planning changes
retail consequences; exhaustive scheduling itself is inherited methodology.
