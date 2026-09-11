# Closest methods and the limits of the proposed distinction

Checked 11 September 2026. The earlier [decision-reuse review](../decision_dependencies/LITERATURE.md)
and [attention comparison](../attention_sessions/LITERATURE.md) remain part of the
research record. The exact final ACL/IWSDS papers and the methods below were
inspected. This is a source review, not independent expert validation.

| Work and inspected section | Established mechanism | Difference tested here and competing explanation |
|---|---|---|
| [Dong et al., Value of Information, ACL 2026, Sections 3, 4.1-4.2, Algorithm 1 and evaluation](https://aclanthology.org/2026.acl-long.1987/) | A clarify-or-commit objective, LLM-estimated latent intentions and response likelihoods, one-step expected utility improvement minus question cost, and a clarification cap. | Our depth-one condition uses that decision rule with an explicitly shared backend. Depth two considers questions whose value depends on another answer. Shared task utility is a permissible VoI objective already. This is an extension of an instantiation, not the invention of VoI. |
| [Acikgoz et al., MAC, IWSDS 2026, Section 4.1 and Algorithm 1, Section 5 and Appendix prompts](https://aclanthology.org/2026.iwsds-1.1/) | A supervisor handles global ambiguity, domain agents handle specialized ambiguity, and routing connects clarification to tools. Algorithm 1 issues one question per turn. Model-simulated MultiWOZ evaluation measures task success and turns. | Coordinating questions across agents and asking shared information early are established. Our distinguishing comparison is budgeted complementary question selection under a fixed downstream loss. We do not reproduce MAC's entire dialogue architecture or present a hand-written baseline as MAC. |
| [Zavattari, Tommasi and Prencipe, One Human, N Agents, arXiv v1, Sections 2-5](https://arxiv.org/abs/2607.28317) | Budgeted noisy audits under miscalibrated confidence and correlated errors, with model traces and simulated allocation. | We inherit scarce oversight and fallible beliefs. This study changes the action from auditing an isolated result to eliciting a value/scope decision shared by registered deliverables. A high error probability need not make a clarification useful. No participant performance is measured. |
| [Boutilier, AAAI 2002, Sections 2-4](https://cdn.aaai.org/AAAI/2002/AAAI02-037.pdf) | Preference elicitation as a POMDP, response models, noisy answers, terminal decisions and Bellman values, motivated explicitly by failures of myopic elicitation. Exploits structure in continuous utility beliefs. | This is the strongest conceptual predecessor. Our finite factor representation, registered agent task dependencies and bounded completion-block candidates are a practical protocol/application specialization. The recursion and rationale for lookahead are not novel. |
| [Krause and Guestrin, IJCAI 2005, Sections 2-5 and 7](https://www.ijcai.org/Proceedings/05/Papers/1154.pdf) | Budgeted observation subset selection and conditional observation plans, dynamic programming exploiting graphical structure, exact chain algorithms and complexity limits. Evaluation includes sensor traces and classification. | Structural decomposition and conditional information plans predate LLM agents. Our task hyperedges are a candidate-ranking heuristic, not an exact chain decomposition or a new complexity result. Pruning can lose the best question. |
| [Golovin and Krause, JAIR 2011; arXiv v5, Definition 3 and Theorem 5](https://arxiv.org/abs/1003.3967) | Adaptive diminishing returns permits guarantees for greedy information gathering. Latest v5 (6 December 2017) corrects a coverage theorem under stronger assumptions. | Conjunctive deliverable completion violates adaptive diminishing returns. We supply a counterexample, not a new submodular guarantee. Do not transplant a greedy approximation ratio. |

The latest inspected publication of Dong et al. is ACL 2026, pp. 42879-42896,
DOI 10.18653/v1/2026.acl-long.1987. MAC is IWSDS 2026, pp. 1-17. One Human,
N Agents remains the 30 July 2026 arXiv v1 in the inspected record, with no further
venue verified. Adaptive Submodularity appeared in JAIR 42:427-486 (2011); the
corrected v5 is used for the methodological reading. Boutilier is AAAI 2002,
pp. 239-246. Krause and Guestrin is IJCAI 2005, pp. 1339-1345.

Dong et al.'s Section 4.2 uses LLM-estimated response distributions and
hypothetical one-step updates, not calibrated probability guarantees. Its four
domains evaluate simulated communication utility. The released
[VOI_communication code](https://github.com/dong-river/VOI_communication) and pinned
inspection are recorded in the prior attention review. Our numeric finite-state
VoI comparator is an explicit adaptation of its decision rule, not its complete
LLM simulation pipeline. MAC's final paper and record did not expose an
implementation link in the previous check. We do not infer absence of a mechanism
from absence of code. Author-provided artifacts for the audit paper were not
verified in the prior review. These limitations remain explicit.

Mem0 and full-history answering remain strong practical alternatives. They may
recover source answers without asking any new questions. Our memory baseline gets
all current source-checked memories, avoiding an artificial top-k retrieval loss.
The additional cost of asking already-stated preferences is reported, rather than
credited as free calibration. Ordinary version invalidation remains shared
infrastructure, consistent with the earlier global-barrier result.

New downloaded full-text checksums are in
`artifacts/clarification_planning/literature_sources.json`. Previously downloaded
final papers and pinned code evidence remain under the historical literature
manifests. No author was contacted. This package does not claim that shared
memory, multi-agent clarification, bounded attention, Bellman recursion or
hypergraphs are new.
