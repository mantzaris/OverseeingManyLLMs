# Bounded sessions with public opportunity preservation

## Public state and objective

Request i is `(id, context, suggested_context, arrival a_i, cutoff d_i,
weight w_i, proposed decision, public evidence, estimated risk p_i, signed
review gain g_i)`. Context identity denotes a source record, not a diagnosis.
The public schema excludes annotated faults, label-bearing dates/filenames and
saved future review responses. The controller receives only released requests.
The scheduler observes completed outcomes but the frozen estimates are not
updated. Unreleased requests never enter its continuation calculation.

The objective is to reduce unresolved weighted error at cutoffs subject to
an active attention budget B. For a timely review, expected preventable loss is
`v_i = w_i g_i`, where `g_i = P(initial wrong, review correct) -
P(initial correct, review unresolved)`. Thus harmful reviews subtract value.
We reuse the development-fitted Stage 7 gain only under unchanged individual
review information. Its nonpositive estimates cause a mechanical no-review
condition, preserved as a result. The ideal reference uses `g_i=p_i`; the
risk-only model ablation uses the same assumption with a fallible response and
is explicitly misspecified. Neither estimates human error.

A completed response replaces only its own diagnosis. Invalid review output
preserves the proposal. Abstention remains unresolved. A correct proposal can
be harmed. A review finishing exactly at cutoff is timely. After a cutoff the
recorded consequence cannot be erased. Correctness is externally labeled;
weights, releases, cutoffs and the review mechanism are constructed assumptions.
No repair, energy savings or downstream sensor response is inferred.

## Cost decomposition

One user processes decisions serially. Opening a different context costs setup
`s`; changing from a previous context also costs switching `x`. Setup is reading
the new context; switching is disengagement from the old one. The first context
has no switching charge. Each decision costs `p>0`. Each additional decision
inside the same offered session costs coordination `h>=0`. Thus a contiguous
same-context session of k decisions costs `setup + switching + k*p + (k-1)*h`.
These terms are distinct and reported separately. Context stays available across
consecutive singleton reviews too. An idle gap does not impose invented memory
decay. A no-reuse sensitivity charges setup for every decision, equally for all
policies. No policy receives free decisions or assumed accuracy improvement.

At most three decisions are offered together. Decisions finish individually,
not at batch end. A session uses only already released requests. The method
never waits deliberately to collect more members. Fixed-window batching does
wait, making its latency cost visible. All time units are abstract, not measured
reading times. Session offers, context openings and repeated setups are demand
proxies; they are not experienced interruptions or evidence inspections.

## Selection and its local certificate

At a free decision boundary, filter for positive value and individual
feasibility under remaining budget and cutoff. Compute a deterministic EDF
continuation over that visible eligible queue, skipping jobs that cannot finish.
Call its feasible set P. Enumerate same-context subsets of size one to three,
ordered by cutoff. Suggested grouping must also match; a mistaken suggestion
can split useful groups but cannot fuse different verified record contexts.

For each candidate session S, calculate its per-decision completion times.
Append the requests in `P \ S` in the EDF order, using the same context and
remaining-budget rules. A certificate is valid only when S and every appended
protected request remain feasible. Show protected IDs and their remaining
slack. Choose among valid sessions by greatest expected benefit per active
time, then benefit, duration and stable IDs. If none qualifies, take the first
feasible EDF request. This is an interpretable heuristic, not an optimality
claim or a new family-scheduling algorithm.

The certificate proves only a local feasibility statement: if the current
requests and assumed processing times are unchanged, the displayed continuation
can still finish P after S. It does not guarantee realized correctness, optimal
weighted loss, unknown future arrivals or actual user speed. At each completed
decision, the default controller checks the remaining session against the newly
released queue and can end it. Decisions themselves are nonpreemptive. The
no-reconsideration ablation keeps the original session commitment. Complexity
costs of remaining cards are included in this check.

The strongest simple baseline is **sticky EDF**: retain the current context
for one decision only when that decision preserves the same feasible EDF
continuation; otherwise take EDF. It receives the same context reuse and never
commits to a multi-card session. This distinguishes the session commitment from
ordinary setup-aware sequencing. EDF, FIFO, weighted-benefit greedy and
value/time greedy expose other simpler explanations. Fixed-window and unguarded
sessions remove deadline protection. The capacity-allocation baseline chooses
a maximum-value subset under independent setup-plus-decision costs and then
dispatches EDF. It is a conservative, single-reviewer reduction of DeCCaF's
allocation mechanism, without its training, heterogeneous experts or equality
quotas. It is not a reproduction of the published system.

## User control and unresolved state

The local interface offers a recommendation, its context rationale and the
certificate. Users may inspect source statistics, remove cards, select an
alternative group, defer an item to an explicit time before cutoff, change a
diagnosis, keep a proposal, or end a session. An override may waive preservation
of other opportunities, but cannot silently cross the selected tasks' own
cutoffs or the declared active budget. Deferred and expired unresolved items
stay visible. Each decision and override is individually logged.

Context sharing is **not answer sharing**. The prototype has no answer-all
button. `validate_shared_answer` requires an explicit versioned decision scope
and exact recipient set. All measured requests have empty decision scopes, so
propagation is rejected. A separate stipulated mechanics fixture exercises an
explicit common dependency and the possibility of one wrong answer harming all
recipients. That fixture establishes a boundary check, not empirical value for
shared clarification. Apparent semantic similarity never authorizes propagation.

## Replay interpretation

Replays reuse each saved individual response while varying scheduling only.
The response sees the same window summary and its own proposal. The interface
can present several cards, but this study does not simulate how combined views
change a reviewer response. The CPU results are conditional on response
invariance. A human study must randomize presentation and observe decisions,
reading/response behavior and reported workload rather than borrow these cached
answers. All source cases are historically inspected; none is relabeled fresh.
