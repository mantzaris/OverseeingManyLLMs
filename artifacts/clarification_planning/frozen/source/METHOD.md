# Budgeted clarification planning over shared decisions

## State, decisions and objective

There is one user, a finite set of distinct deliverables T, and a set of decision
records D. A record is (value, scope, exceptions, source, version, status).
`inferred` records reflect fallible interpretation; `confirmed` records reflect
an actual received response. A value is never itself general permission to act.
A task registers its required decision set R_j and any applicability conditions.
Some tasks have alternative bindings: use a shared value if its scope applies,
or obtain a local value. Exceptions and allowed task IDs constrain these bindings.
The main dialogue adapter uses fixed domain scopes and does not fabricate hidden
scope labels from coincidentally equal values.

A public state contains task requirements, the current record hypotheses and
categorical beliefs, already received answers, attempted questions, represented
scope conditions, versions, and remaining budget. Hidden theta is actual user
intent, including applicability. Source answers, future revisions and evaluation
correctness do not enter next-question selection.

For a terminal action vector a, let

    L(a,theta) = sum_j [ e_j I(j released incorrectly) + d_j I(j unfinished) ].

Correct release costs zero. Every original deliverable remains in the denominator.
Releasing three copies of the same artifact does not create three task rewards.
Main dialogue tasks are one database shortlist per requested domain, checked by
normalized required constraints and execution against the pinned database. An
empty correctly constrained shortlist is a completed query artifact, not a booked
trip. Synthetic deliverables and their distinct utility are authored assumptions.

The objective is

    min_pi E[ L(a_final,theta) + lambda sum_t c(q_t) ],
    subject to sum_t c(q_t) <= B on every path.

A question resolves one substantive value, applicability, exception or revision
issue. Each costs one response unit in this study. Asking a value and asking
where it applies costs two, even when displayed on one card. Lambda = 0.05 loss
units per response. e=4 and d=1 are primary dimensionless research weights;
e=2 and 8 are empirical sensitivities. Neither units nor weights measure human
cognitive load, money, time or physical harm. Simulated accurate extra answers do
not establish observed user performance. Budget unlimited means enough units to
ask every represented unresolved factor once, plus registered revisions.

## Beliefs, response model and terminal choices

`Factor` stores a finite categorical distribution. Separate value and Boolean
applicability factors represent uncertainty about content and scope. The model
assumes independent distinct factors; shared record references use the SAME
factor. Task correctness is a conjunction over unique factors, so a shared error
is not counted as independent evidence at several agents. The joint sampled
factor also governs every affected task in the evaluator.

For each public binding option, V0 chooses the highest-probability available value
for each needed factor and includes required scope literals. It compares expected
wrong-release loss e_j(1-p_j) with deferral loss d_j. A tie defers. It chooses the
best valid binding or leaves the task unfinished. All controlled policies use this
same rule; terminal decisions cannot read evaluator answers. Products are exact
under the stated factorization, not a claim that natural-language errors really
are independent.

Empirical value reliability is fitted on development only. For supplied values,
use Beta(1,1) smoothing by interpretation backend and domain, falling back to the
backend's pooled estimate with fewer than ten supplied examples. The remaining
mass is OTHER, an unspecified wrong value. A missing value has all mass on OTHER.
This is not a correct-answer lookup or an LLM confidence score. It deliberately
keeps out-of-support possibilities. Missing values are not guessed from labels.
An unobserved OTHER cannot be released as an answer.

A value question predicts categorical responses by its belief and a declared
channel. The primary channel returns the actual value exactly. Synthetic noisy
conditions have symmetric categorical error 0.2; an independent unresolved channel
has probability 0.3 in its own condition. Bayes' rule updates beliefs using the
same declared likelihood, rather than asserting all noisy responses are correct.
With a singleton alphabet, the categorical channel has only one category; unseen
actual strings are represented by OTHER until received. Synthetic noise tests use
binary alphabets. The noisy and unresolved mechanisms are separately varied.

An actual out-of-support answer replaces OTHER with the received string, ONLY
when the question is answered. An unresolved response costs a unit, reveals
nothing and is not retried during the current version. Transport retries during
preparation are separate and never counted as user decisions. The evaluator
samples responses using scenario/question identifiers, shared across matched
policies. It receives true targets; the planner receives only the returned answer
when it has actually asked. Ideal interpretation is a separately marked diagnostic
that intentionally receives annotations, never the primary condition.

## Finite-horizon recursion and bounded candidate construction

    V_0(s,b) = min_a E[L(a,theta) | s]
    V_h(s,b) = min( V_0(s,b),
        min_q:c(q)<=b { lambda c(q)
          + sum_y P(y|s,q) V_(h-1)(Update(s,q,y), b-c(q)) } ).

Already attempted questions are unavailable until their record is revised. The
controller executes only the first question, receives its actual response, then
replans. It can stop with some deliverables released and others deferred. Work
may be displayed as currently feasible while clarification continues; evaluation
scores the final release set. No deadlines or human response durations are added
to this application. Unsolicited registered revisions are public update events,
not secretly planned future observations.

The practical algorithm prioritizes **completion blocks**: up to three unresolved
factors from a single task binding that could reduce its terminal risk together.
For each block it computes an optimistic loss reduction per response cost by
setting its factors' correctness to one, leaving other factors at their current
beliefs. Each factor receives its best block score or its immediate VoI, whichever
is greater. Only the top eight factors are considered at each recursive node.
This preserves zero-immediate-value complementary candidates in a limited search.
Contingent response branches then evaluate their actual expected value, so the
optimistic bound is a ranking device, not promised utility or an extra user answer.
All affordable single questions remain available when the queue has at most eight
factors. The generic-search ablation uses the same width, depth and beliefs but
ranks by single-question VoI. Deterministic ties use factor ID.

Depths one and two are core, depth three a sensitivity. The node limit is 25,000
counted evaluated states per selection; reaching it substitutes V0 at unexplored
nodes and records a cap. Terminal evaluations at the boundary and dictionary
lookups still occur. This is an approximate algorithm with no general optimality
guarantee. Caches include the complete public belief state, asked/revealed masks,
budget and depth. A changed public alphabet or revision discards affected caches.
No cache key or cached value contains hidden labels.

An independent exhaustive contingent recursion (`exact.py`) evaluates all
questions for at most six factors and budget six. It uses the same estimated
model and terminal action set. It does not know sampled answers. Small-instance
checks compare equal horizons; full-budget gaps additionally measure truncation.
Pruning is tested separately by shrinking the width on those same small instances.

## Controlled alternatives

* Semantic memory: the GPU answers from ALL current source-checked memories,
  including updates. Ask missing fields in task order and share explicit answers;
  then use the common risk-sensitive release rule. This is a competent small-store
  adaptation, not a reproduction of Mem0's embedding/graph stack.
* Full history: answer from the complete released dialogue and use the same
  missing-field clarification and terminal rule, with its own development-fitted
  reliability. Bare and wrapped answer dictionaries are both accepted after the
  development parser audit. It receives no deliberately shortened history.
* One-step VoI / depth one: exactly the same candidate construction, response
  model, scope controls, beliefs and task loss as the planner, horizon one.
* Completion heuristic: select a task with the fewest still-queryable factors,
  breaking ties by current task loss per total question cost and task ID; ask its
  least certain factor. It may keep asking when a myopic method would stop.
* Uncertainty-first and no review are additional synthetic comparators.
* Request-specific ablation clones a decision for each consuming task, preserving
  the hidden value and response realization while requiring another atomic answer.
  No-scope disables scope questions, preserving local value alternatives and all
  guards. Ideal interpretation is an explicit upper bound, not new generated data.

## Formal properties and their limits

**Pathwise budget.** Initially spent=0. `propose` admits only questions with positive
integer cost at most B-spent. `answer` checks this again and adds exactly that
cost, including unresolved responses. By induction spent<=B after every event.
No response branch borrows expected budget from another. Revisions do not reset
spent. Tests enumerate stochastic response paths and reject invalid API actions.

**Represented scope and version consistency.** A valid terminal binding cannot use
a record on an excepted or non-allowed task. Received answers are attached to the
specific registered decision. A released artifact records versions for every
value and scope factor it consumed. Incrementing a dependency version marks its
releases for revalidation; the release guard rejects mismatched versions.
Unrelated records retain their versions. Induction over publish/revise/release
establishes consistency with represented records, given complete dependencies and
use of the guard. This is NOT proof that a scope interpretation is semantically
correct or that an unregistered dependency will be discovered.

**No diminishing returns guarantee.** Let q1 and q2 have independent uniform
binary values and jointly determine three distinct deliverables; q3 determines a
fourth. Use e=4,d=1. Before questions, even one unknown binary factor makes wrong
release cost at least 2, so a task defers. Clarifying q1 alone saves zero, but q1
saves three after q2 is known. Thus marginal benefit increases from 0 to 3.
Ordinary and adaptive diminishing returns fail. With two responses, immediate
VoI asks q3 and then stops; depth two asks q1,q2. A fewest-answers heuristic also
starts with q3. This constructed witness proves a mechanism, not its prevalence.
No submodular approximation ratio is claimed.

**Depth-one equivalence.** Substituting h=1 in the recursion compares stopping
with lambda*c(q)+E[V0 after q]. Subtracting V0 gives the implemented net one-step
VoI criterion. With identical candidates and ties, the two methods are the same.

**Complexity.** With n candidate factors, at most k response categories plus an
unresolved branch, depth h, width w, and terminal cost C, a loose un-memoized
bound is O((w(k+1))^h C). Completion-block construction costs
O(sum_options sum_(r=1)^3 binom(m_option,r) * m_option) per uncached node, plus
single-question scores. Exact unpruned search replaces w by n and h by affordable
remaining questions. Bounds on depth, width and expanded states trade computation
for approximation. Cache gains and actual latency are measured, not assumed.
