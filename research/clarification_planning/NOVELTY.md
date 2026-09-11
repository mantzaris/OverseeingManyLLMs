# Novelty assessment before the held-out comparison

The candidate contribution is a **decision protocol and practical approximate
planner for complementary clarifications across registered deliverables**, with
scope conditions, pathwise response budgets, stop/defer actions and fallible
interpretation. Its distinguishing implementation is the use of completion blocks
to retain useful zero-immediate-value questions in a bounded contingent search.
The first question is executed and the plan is reconsidered after the response.

This is not a new general decision-theoretic objective. Boutilier already poses
nonmyopic preference elicitation as a POMDP. Krause and Guestrin already exploit
structure for budgeted conditional observation plans. Dong et al. already connects
VoI to LLM clarification, and MAC already coordinates clarification among agents.
The closest mathematical explanation is an ordinary small POMDP specialized to a
task graph. The closest practical explanation is a simple task-completion rule
that counts missing answers. Both are essential comparisons.

The empirical test is not whether a favorable authored witness exists. It asks
whether, with the same GPU memory interpretations, candidate questions, response
simulator and release loss, depth two improves over one step at budget two. It
also asks whether any gain survives the fewer-missing-answers heuristic and
competent shared memory. Full history tests whether apparent value is caused by
weak extraction. Source tasks are not selected for missing answers or model errors.

Potential falsifications:

* The completion heuristic matches or improves task quality and demand. Then a
  general practical planning advantage is not supported by this application.
* Depth two only beats a missing-answer memory policy because it asks more
  redundant confirmations, while depth one is equally good. Then complementarity
  is not the observed mechanism.
* Candidate construction ties generic search in small cases and helps only an
  authored distractor trap. Then it has an implementation rationale, not broad
  empirical evidence for an algorithmic advance.
* The source has few unresolved complementary requirements or no annotated
  cross-agent scope relations. Then the data do not establish prevalence of the
  intended shared-decision problem, even if multi-field completion is measurable.
* Misspecified scope or response beliefs reverse a gain. The planner is only as
  trustworthy as those assumptions; consistent stored versions cannot fix it.

A supported result would be a scoped mechanism claim with an identified operating
region, measured approximation/computation, and a source-grounded test. A null or
unfavorable result should lead to a narrower claim or a simpler method. Human
attention savings and decision quality remain interaction-study questions. Counts
of simulated responses are not observations of cognitive load.
