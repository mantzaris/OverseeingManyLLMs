# Review sessions for a user supervising agent requests

## Scope and verification

This comparison examines mechanisms, not title similarity. Full methods,
evaluation and limitations were read for the five requested papers. The final
ACL version of Value of Information and the author-hosted TMLR version of DeCCaF
were checked in addition to arXiv. Source hashes, versions, code revisions and
inspected paths are in `sources/`. Full third-party papers and code were read
outside Git. No authors were contacted and no participant data were collected.

### Foundation

**One Human, N Agents.** Zavattari, Tommasi and Prencipe, arXiv
2607.28317v1, 30 July 2026. No later version, publication venue or author-linked
code/data release was located in the checked records and title searches.
Section 3 allocates B noisy audits per round across persistent agents. The
Gaussian copula separates fleet-wide and family factors; an audit updates
beliefs about related agents. Residual risk counts undetected errors, and
vacuity means no considered deployable policy achieves a declared fractional
risk reduction. Sections 4-6 test synthetic conditions and six models on aligned
GSM8K/HotpotQA items. Shared difficulty explains co-failure better than lineage;
transfer needs persistent errors and a sufficiently reliable verifier. Our
historical work already shares scarce oversight, imperfect confidence, noisy
review, saved-output allocation and ineffective-oversight analysis. Its audit
model does not replace proposals; our correction-before-cutoff semantics differ.
[Sections 3-6](https://arxiv.org/html/2607.28317v1#S3).

**Value of Information.** Dong, Hu, Hui, Zhang, Vulic, Bobu and Collier,
ACL 2026, pp. 42879-42896; arXiv remains v1. Section 4 asks when expected
posterior decision value exceeds current value plus question cost. Closed
answers and model-estimated replies make the lookahead tractable. Sections 5-6
use mixed-stakes guessing/diagnosis, flight preferences and ambiguous WebShop.
The limitation section explicitly uses linear per-question cost, not measured
mental demand. Table 1 includes high-cost settings where the method loses to
the best baseline. Released flight code computes posterior action value minus
current value and cost; it includes saved outputs and data. The repository has
no detected license. The paper does not restrict the general VoI principle to
linear costs, so adding setup costs alone would not be a conceptual novelty.
[Final paper, Sections 3-6 and Limitations](https://aclanthology.org/2026.acl-long.1987.pdf).

**AgentLens.** Kim, Joung, Lee, Lee, Min and Lee, arXiv 2604.20279v3,
7 September 2026, identifies UIST 2026 and DOI 10.1145/3830398.3830619.
The conference is forthcoming in November; the publisher endpoint was
inaccessible in this check. Sections 4-5 implement full, cropped and generated
visual overlays. The 21-person controlled study uses replica apps, scripted
action paths and predetermined modalities, isolating interaction design from
execution failures. Eighteen preferred AgentLens. Separate modality studies
use 43 tasks. This supports selective visual interaction, not fleet scheduling
or deadline guarantees. Android/backend code is released under Apache 2.0;
raw participant-level study data were not located. The abstract reports lower
PSSUQ as better while Section 5.2.4 describes a reversed scale; we do not import
its numerical PSSUQ score into our evaluation.
[Sections 4, 5.1, 5.2.1-5.2.6](https://arxiv.org/html/2604.20279v3#S4).

**HiLSVA.** Ai, Do and Wang, arXiv 2606.26614v2, 16 July 2026;
the author record identifies TVCG/IEEE VIS 2026, without independently verified
volume, pages or DOI here. Sections 2.1-2.4 include editable plans, approvals,
rollback, provenance, concurrent task sessions and reusable feedback. Section
2.3 has an interaction budget with unit query costs and assigns human-derived
knowledge confidence one. The 12-person study balances three autonomy modes
but confounds human involvement with retrieval-based adaptation. Mean times
increase from 9.83 to 13.50 minutes; the Friedman test is not significant
(p=.078). Expertise comparisons are descriptive. This already addresses
handoffs, concurrent-session awareness and feedback reuse. We extend its
interaction questions toward explicit competition between expiring requests,
not claim to invent session management. Code and demonstrations are released;
no repository license or raw participant dataset was located.
[Sections 2-4](https://arxiv.org/html/2606.26614v2#S2).

**DeCCaF.** Alves, Leitao, Jesus, Sampaio, Liebana, Saleiro, Figueiredo
and Bizarro, TMLR July 2024; arXiv v3, 19 August 2024. Section 3 learns
classifier and expert correctness, then globally assigns cases under capacity
constraints. The released CP-SAT implementation uses equality quotas; the
paper also discusses maximum-capacity inequalities. Sections 4-5 use synthetic
bank applications and nine synthetic analysts, with instance-dependent errors,
cost ratios and capacity variations. These are not observed analyst behavior.
Thus error risk alone is not intervention value: the assigned expert can also
err. Code, data and models are released; the license file contains Apache 2.0
text and a commercial-use contact notice. We inspect rather than copy this
code. Our capacity-allocation baseline is a declared single-reviewer reduction,
not a reproduction of its learned multi-expert system.
[Sections 3-5](https://research.feedzai.com/oshuzuxa/2024/08/Alves_Cost_Sensitive_Learning_TMLR_2024.pdf).

## Compact mechanism matrix

"Not modeled" below means absent from the inspected formal mechanism and
experimental design, not absent from every sentence or imaginable extension.
The cited sections delimit each inference. "Shared" distinguishes shared
information from one binding answer applied to several decisions.

| Work | Decision maker / supervised units | Shared attention competition | Duration / deadline | Context setup / switch | Grouped decisions / shared answer | Error or harm | Evidence / assets |
|---|---|---|---|---|---|---|---|
| One Human, N Agents, Sec. 3-6 | Noisy auditor / persistent LLM fleet | Explicit B audits/round | Round counts; no per-item service/cutoff | Not modeled | Belief transfer, not answer propagation | Noisy detection; no harmful replacement | Simulation + LLM traces; no release found |
| VoI, Sec. 3-6 | User answers / one clarify-or-commit dialogue | Question budget, not competing queue | Question cost; no request cutoff | General cost framework; linear experiment | Belief update within dialogue | Imperfect beliefs/replies; not corrective review transitions | Model/benchmark evaluation; code/data/results |
| AgentLens, Sec. 4-5 | User manipulates / mobile agent | Multitasking, not fleet allocation | Interaction latency; no cutoff scheduler | Presentation studied; no explicit switching price | UI options for current task; no scoped fleet answer | Controlled study removes execution failures | Human studies; Android/backend code |
| HiLSVA, Sec. 2-3 | User and orchestrator / specialized agents | Concurrent sessions + query budget | Unit query costs; no item deadline allocation | Provenance/knowledge reuse; no explicit time decomposition | Editable plans and feedback reuse; no typed decision-scope guarantee | Feedback dependence; no calibrated harm transition model | Cases + 12 humans; code/demo |
| DeCCaF, Sec. 3-5 | Assigner / classifier and expert team | Explicit batch capacity | Case quotas, not individual service deadlines | Not modeled | Allocation batches, not shared-context review sessions | Learned expert correctness | Synthetic cases/analysts; code/data/models |
| Historical project, Stages 5-7 | Simulated reviewer / prepared transactions or diagnoses | Explicit shared queue | Service duration and cutoff | Not modeled | Independent review outcomes | Ideal, restricted authority and harmful model review | Executable/model/measured substrate; full replay |

## Closest established mechanisms

**Family scheduling is the strongest competing explanation.** Potts and
Kovalyov's review distinguishes common setups, serial decision processing and
item availability from simultaneous batch completion. It explicitly discusses
the tradeoff between fewer setups and delaying important other families.
Schutten, van de Velde and Zijm also combine release dates, due dates and
family setups. Our saved-output scheduling problem is a small online instance
of this established family. Neither exact enumeration nor the observation that
context grouping can save setup is a new result.
[Potts and Kovalyov, Sections 2 and 4](https://doi.org/10.1016/S0377-2217(99)00153-8),
[Schutten et al., institutional record](https://research.utwente.nl/en/publications/single-machine-scheduling-with-release-dates-due-dates-and-family/).
The review's publisher introduction/model material was accessible; the full
Schutten algorithm was not read, so we make no algorithm-by-algorithm distinction.

**Interruption deferral and notification batching have human evidence.**
Horvitz, Apacible and Subramani investigate bounded notification deferral;
Iqbal and Bailey's Oasis work places notifications at task breakpoints. These
are stronger alternatives than immediate FIFO alerts for interruption timing.
Fitz et al. randomize notification delivery in a field study with 237 analyzed
participants; conditions include three daily batches, hourly batches and none.
Its methods report attrition and self-reported outcomes. These interventions
concern notification delivery, not correctness of expiring agent decisions.
We implement a fixed-window batching baseline, not a learned breakpoint detector,
because the saved traces have no observed user-task breakpoints.
[Bounded deferral](https://www.microsoft.com/en-us/research/publication/balancing-awareness-interruption-investigation-notification-deferral-policies/),
[Oasis study](https://doi.org/10.1145/1357054.1357070),
[Fitz et al., Sections 3-4](https://static1.squarespace.com/static/57a40c19414fb54f51f8095f/t/614a55faa7b89e25f4e48ad1/1632261627146/2019%2BFitz%2BBatching.pdf).
Only the publisher summary was obtained for Oasis and bounded deferral; the
Fitz full text and methods were read. No exact reproduction is claimed.

**Mixed initiative and resumption support are established.** Horvitz's
principles include attention-aware timing, uncertainty-sensitive action,
interaction refinement and memory of recent interactions. Iqbal and Horvitz
observe disruption and recovery in desktop work. A persistent unresolved list
and user override implement these principles; queue length is not a measure
of frustration or mental demand.
[Horvitz, principles and LookOut testbed](https://erichorvitz.com/chi99horvitz.pdf),
[Iqbal and Horvitz, methods and recovery analysis](https://www.erichorvitz.com/CHI_2007_Iqbal_Horvitz.pdf).

**Shared clarification is also occupied ground.** MAC assigns global ambiguity
to a supervisor and domain ambiguity to experts. Algorithm 1 issues at most
one clarification per turn, then routes the clarified request. Its MultiWOZ
experiments use a simulated user, not a human fleet study. HiLSVA also reuses
human feedback across steps/sessions. Consequently, "ask once for several
agents" is insufficient novelty without a distinct, tested scope mechanism.
[MAC, Sections 3-5 and Algorithm 1](https://aclanthology.org/2026.iwsds-1.1.pdf).
The newer AgentAsk work concerns clarification at inter-agent message edges;
it is not evidence about a shared human's attention. Its publisher abstract was
checked, not its complete method, and it is not an implemented comparator.
[Publisher record](https://aclanthology.org/2026.acl-long.1294/).

## Three candidates and selection

| Candidate | User problem and mechanism | Closest alternative / assumptions | Distinguishing test / falsifier |
|---|---|---|---|
| A. Bounded context sessions | Inspect common evidence once while retaining separate decisions. Refine into a session with a public deadline-preservation certificate and persistent deferred items. | Family scheduling, bounded deferral, HiLSVA. Requires explicit context identity and estimated time. | Same cards, same responses, setup-aware EDF and unguarded sessions. Falsified as a scheduling advance if EDF/sticky EDF dominates or gains are only assumed setup savings. |
| B. Scoped shared clarification | One explicitly scoped answer resolves a declared common dependency, with revocation and downstream accounting. | MAC, VoI and HiLSVA knowledge reuse. Requires genuine shared intent and typed dependency records. | Compare repeated questions with scoped reuse and wrong shared answers. Falsified if validated scopes are rare or correlated harm outweighs saved effort. Existing HVAC windows are not such a dependency. |
| C. Adaptive glance and handoff | Choose a compact card versus source view while leaving a decision trail. | AgentLens and mixed-initiative UI. Requires measured comprehension and presentation-specific responses. | Same decisions, randomized presentation, quality and interaction measures. Saved responses cannot distinguish this; no new human evidence is authorized. |

Bare candidate A fails a novelty claim. B and C were investigated next, but MAC,
HiLSVA and AgentLens substantially occupy their generic formulations, and the
available traces cannot test their essential response changes. We select the
**narrowed A as an interaction research hypothesis**, not a new scheduling
algorithm: expose a bounded, editable context session together with the pending
opportunities that its proposed commitment preserves under the public timing
model. Study whether this explicit contract helps people override batching
without losing postponed decisions. The present CPU study can falsify its
modeled allocation premise; only a later interaction study can test control
and workload benefits.

The strongest competing explanation remains ordinary setup-aware ordering.
A useful result must survive equal context reuse for all methods, negligible
setup costs, deadline-aware simple alternatives and ineffective review. A
certificate is local to released requests and assumed durations, not a promise
about unknown arrivals or human speed. No priority claim over all HCI or
scheduling literature is established by this focused search.
