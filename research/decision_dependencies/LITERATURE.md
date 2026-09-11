# Decision reuse, clarification and changing instructions

Checked on 11 September 2026. This extends, rather than replaces, the
[previous methods comparison](../attention_sessions/LITERATURE.md). Full methods
and evaluations were read. Paper/download checksums are in `sources.json`; pinned
code revisions and inspected paths are in `code_sources.json` and
`code_review.json`. No authors were contacted. No unavailable repository is
treated as evidence that an idea was absent from a paper.

## Closest methods

| Work and inspected sections | Established mechanism | Relevant distinction and assets |
|---|---|---|
| [MAC, Sections 3-5 and Appendix prompts](https://aclanthology.org/2026.iwsds-1.1.pdf) | A supervisor routes work and handles general ambiguity. Domain agents clarify specialized information. Shared dialogue information coordinates questions. | Already addresses clarification across agents. The evaluated object is dialogue success, rather than whether a prepared artifact still satisfies a revised instruction at release. Final IWSDS 2026 paper, pp. 1-17. No author-linked implementation was located in the checked final paper, Anthology record or exact-title search. |
| [AgentAsk, Sections 3-5](https://aclanthology.org/2026.acl-long.1294.pdf) | An edge clarification module detects information gaps and asks another agent targeted questions. Training trades task utility against clarification costs. | Inter-agent repair is different from asking the user to decide a preference. Its taxonomy includes data gaps, corrupted signals, referential drift and capability gaps. ACL 2026, pp. 28055-28077. The final paper/author publication records were checked; a usable author-linked code release was not located. |
| [Mem0, Sections 2-3](https://arxiv.org/pdf/2504.19413) | Extract memories, retrieve similar records, and decide ADD, UPDATE, DELETE or NOOP. The graph variant represents entities and contradictory relations. | Ordinary memory is not an append-only strawman. Our small-memory selector receives all current records, avoiding top-k retrieval losses. It is a Mem0-inspired adaptation, not a reproduction. Latest arXiv record v1, 28 April 2025; no journal venue verified. [Released code](https://github.com/mem0ai/mem0) is Apache 2.0. |
| [Value of Information, Sections 3-6](https://aclanthology.org/2026.acl-long.1987.pdf) | Ask when the expected value of the response exceeds communication cost. User responses are modeled as uncertainty-reducing information. | The benefit of one answer affecting several tasks fits this principle already. We do not introduce a new VoI objective. Final ACL 2026 version, pp. 42879-42896. Author code/data and their limits are recorded in the earlier review. |
| [HiLSVA, Sections 2-4](https://arxiv.org/html/2606.26614v2) | Editable plans, approvals, feedback retrieval, concurrent sessions, explicit handoffs and stepwise provenance. | Reusable feedback and session awareness are established. Its twelve-person study does not isolate our change-consistency mechanism. Latest arXiv v2, 16 July 2026. The author publication page lists TVCG/IEEE VIS 2026; volume/pages/DOI are not independently verified. [Official implementation](https://github.com/KuangshiAi/HiLSVA). |
| [Zep, Sections 2-4](https://arxiv.org/pdf/2501.13956) | Episodic provenance, temporal facts, hybrid retrieval, and invalidation of contradictory earlier edges. | Time-aware memory and conflict handling cannot support a novelty claim here. The public Graphiti implementation explicitly checks validity intervals before expiring an edge. [Code](https://github.com/getzep/graphiti), Apache 2.0, pinned in our source manifest. |
| [LongMemEval, Sections 2-4](https://arxiv.org/pdf/2410.10813) | Tests extraction, cross-session reasoning, temporal reasoning, knowledge updates and abstention. | A strong precedent for evaluating stale-answer retrieval. Its human-curated questions and model-generated, edited histories are distinct from observed participant use. ICLR 2025, arXiv v2. Our added outcome concerns downstream local artifacts, not only answers to memory queries. |

MAC uses 1,000 MultiWOZ 2.4 test tasks with model-simulated users and five runs.
Its main mean success result is 58.40 +/- 2.10 versus 53.72 +/- 0.92. The
62.3 versus 54.5 numbers highlighted in the abstract are the maximum-over-five
results. Neither is measured human attention savings. AgentAsk evaluates five
reasoning/code benchmarks with a trained Qwen3-4B clarifier and GPT-4o-mini
executors. These are useful clarification mechanisms, but we neither train nor
reproduce their full systems in this bounded study.

Mem0 evaluates long-conversation question answering on LOCOMO. Its published
pipeline handles updates and graph conflicts already. The currently pinned
`mem0/memory/main.py` differs from the paper's presentation: the inspected path
uses additive extraction, retrieves ten related memories, and maintains entity
filters and expiry handling. We record that difference rather than describing
the latest code as an exact copy of the 2025 algorithm. Our scalar record
reconstruction and all-memory semantic selection are explicit simplifications.

## Established foundations and strongest competing explanation

Dependency invalidation is older than agent memory. [Doyle's truth-maintenance
system](https://groups.csail.mit.edu/medg/people/doyle/publications/) maintains
beliefs with their supporting assumptions. [Gray and Cheriton's leases](https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15712-s12/www/papers/gray89.pdf)
bound cached rights in time. [Build Systems a la Carte](https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-5ab0f42d0f937.pdf)
separates dependency discovery, change detection and rebuilding. These are direct
conceptual ancestors of tracking which artifact consumed which decision version.
[NIST SP 800-162](https://csrc.nist.gov/pubs/sp/800/162/upd2/final) explains
attribute-based authorization using subject, object, operation and environment
attributes. A preference record cannot grant general action authority.

The strongest alternative explanation is therefore straightforward: a shared
state tracker plus an ordinary version check solves the consistency problem.
Our evaluation includes that exact simple alternative. A graph, a new name or a
polished interface would not establish a new algorithm. The defensible extension
to test is the *end-to-end tradeoff*: imperfect interpretation of actual user
utterances, additional clarification, and correctness of work released after
those instructions change.

The previous review's comparisons remain relevant. One Human, N Agents allocates
scarce audits under correlated, miscalibrated confidence. AgentLens evaluates
adaptive visual presentation, including a controlled human study. DeCCaF models
expert correctness as well as capacity; its fraud analysts are synthetic.
Established interruption and batching studies already motivate attention-aware
interfaces. This prototype adds no evidence about experienced mental demand,
frustration or human reviewer accuracy.

## What is and is not implemented

Implemented: source-backed record extraction with Qwen; public request parsing;
full-history answering; all-current-memory semantic selection; scoped records;
global and selective version checks; explicit user correction and revocation;
local dependency receipts and executable planning artifacts.

Conceptual comparisons: MAC's hierarchical dialogue manager, AgentAsk's trained
edge policy, Mem0's complete embedding/graph stack, Zep's temporal graph,
HiLSVA's visualization agents and VoI's response lookahead. We do not label a
small adapted baseline as any of these complete published systems.

MultiWOZ 2.4's [Sections 2-3](https://aclanthology.org/2022.sigdial-1.34.pdf)
describe author correction of validation/test annotations, including unmentioned
values and assistant-only information. Training labels remain unchanged. Our
annotation-based screen requires lexical support in user turns, but this is not
independent expert adjudication of entailment. The source data are task-elicited
dialogues and benchmark database records. The multi-agent workload is constructed.
