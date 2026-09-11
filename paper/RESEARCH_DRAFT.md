# Planning shared review for language model workflows

The submission sources are [main.tex](main.tex) and [main.pdf](main.pdf), with
[supplement.tex](supplement.tex) and [supplement.pdf](supplement.pdf). This outline
follows the scientific argument. Development chronology and complete historical
results remain in the stage reports and supplement.

## Research question and formulation

When a finite reviewer serves multiple language model proposals, useful
intervention can expire before service completes. Which proposals should be
reviewed, in what order, and under which assumptions does planning outperform
greedy allocation or earliest-deadline-first?

A public request specifies arrival, cutoff, service duration, consequence weights
and a development-fitted benefit estimate. Schedulers see only released requests.
Hidden correctness and saved review outputs remain evaluator state until review
completes. FCFS, EDF, uncertainty-first, greedy and exhaustive current-queue search
share eligibility, deterministic ties and information. No review is a control.
Enumeration is established scheduling machinery, not a novelty claim.

With effective review, expected benefit is error risk times preventable consequence.
With fallible review, benefit must account for unresolved errors and harm to correct
proposals. The measured study uses the signed probability of correction minus error
introduction. This can rationally decline review and differs from ranking error risk.

## Principal measured application

Berkeley Lab's FLEXLAB SZCAV/SZVAV records provide actual minute-level temperature
and control observations under experimentally imposed faults. Only physical files
are selected, with provenance, CC0 licensing and checksums from the pinned version.
Four component categories are scored against inventory labels. This supplies
external diagnosis correctness, not observed repair outcomes or operational loss.

Eight complete experimental days supply development. Eighteen remaining day blocks
on one air handler supply 54 evaluation windows. Three windows remain one paired
unit. Control mode, physical units and recording hours are public; source dates,
filenames, fault indicators and answer-bearing descriptions are withheld. A
standardized nearest-centroid classifier uses the same evidence and development-only
fitting. No adjacent windows cross the split.

One saved proposal and one separately prompted same-model review are reused across
policies, capacities and consequence conditions. These are correlated judgments.
The retrospective backlog opens after every window has been observed. Arrivals,
review duration, cutoffs and dimensionless loss weights are constructed. Eighteen
day blocks do not constitute eighteen independent buildings.

The proposer labels 19/54 windows correctly, versus 27/54 for the conventional
baseline. It proposes heating valve on 51 windows. Both methods miss all cooling
cases. Review corrects one wrong proposal, changes five correct proposals to wrong
categories and makes one correct proposal abstain. Reviewing everything reduces
correctness to 14/54. Frozen risk AUROC is 0.5023 with sparse, nearly tied predictions.

Development-fitted signed gains are nonpositive, so the primary condition admits
no reviews. Search minus greedy is mechanically 0 [0,0] across 18 day blocks. This
is not evidence of scheduling-policy equivalence. A predeclared secondary risk-only
ablation ignores reviewer harm and produces search loss 2.667 points above no review
[0.217,5.778]. Under ideal review, search beats greedy by 3.333 points [1.778,4.889],
but EDF matches search. Deadline order fits all two-tick reviews, giving a structural
explanation. All 204 GPU attempts and 3,888 paired scheduling replays are retained.

Figures connect measured signals, generated diagnoses, annotated correctness and
simulated allocation. Claims concern limited reviewer effectiveness and conditional
ordering value, not successful HVAC deployment.

## Synthetic mechanism evidence

The original ventilation observations are invented noisy clues. They remain a
controlled mechanism study with fresh feedback-dependent trajectories. The 2,752
frozen evaluation episodes are analyzed by distinct workload distribution. Search
minus greedy at two ticks is -0.094 [-0.563,0.344] on the original workload and
-1.313 [-2.250,-0.438] on constructed competition. EDF matches search's zero
competition loss at one tick. Larger-workload planning gains are strong at one tick
and small at two. Better analytical risk scores do not consistently improve
allocation. A correctness-penalty objective reduces wrong closures while increasing
original cost. The supplement preserves full matrices and positive, null and
unfavorable outcomes.

## Retail transfer and limits

Adapted tau-bench retail uses simulated customer and transaction records with
genuine GPU-generated retrieval, policy interpretation and state-changing tools.
Existing tool guards remain enabled. Added staging permits simulated review before
a constructed posting cutoff. Policies share identical prepared transactions,
without later feedback-dependent model generations.

The original 96-case, 32-bundle study retains 288 workflow attempts and 1,152 replays.
Search minus greedy is +0.250 [-0.333,1.000], with one bundle win, 29 ties and two
losses. At one tick all review policies correct all staged errors; 55 unstaged
failures remain. The 24-case, eight-bundle restricted-authority follow-up gives
+1.667 [0.000,4.667], with zero wins, six ties and two losses. Blocking avoids a wrong
posting without completing the task. Neither unfavorable result is hidden or pooled
with measured HVAC or synthetic maintenance.

## Contribution and remaining limits

The framework makes intervention benefit, finite service and expiry explicit across
proposal types. Its paired protocols distinguish feedback-dependent trajectories
from fixed-proposal allocation. The analysis shows how competition, risk ranking,
objective choice and corrective effectiveness determine whether ordering matters.
The contribution is this formulation, reproducible integration and conditional
evidence, not the invention of shared oversight, deferral or exhaustive scheduling.

Measured HVAC evidence covers one apparatus and a weak diagnostic model. Retail
records, deadlines and consequence weights are constructed. Supervision is simulated;
no human performance or real savings are measured. Public-benchmark pretraining
exposure is not ruled out. Independent domain review and a separately frozen
multi-equipment study are the next useful scientific steps. SQL was not evaluated
under the remaining original deadline.

The official-template manuscript is complete for human review. Authors must take
responsibility for interpretation, finalize submission declarations and confirm
anonymous AI-disclosure and supplementary-upload handling. Reproduction commands,
claim-evidence mapping and source-based assumption assessments accompany it.
