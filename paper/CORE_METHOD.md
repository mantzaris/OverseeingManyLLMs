# Core method: allocating simulated supervision

## Research question

How should one simulated human supervisor allocate a limited amount of review time across three LLM agents when incorrect actions incur continuing cost and the opportunity to correct them expires? The implemented comparison asks whether planning the order of reviews using their completion times changes loss relative to FCFS, uncertainty-first, and myopic benefit. This backbone and its single-scenario demonstration establish integration; they do not establish policy superiority or novelty.

## Implemented mechanism

Each agent receives two independent synthetic campus ventilation maintenance jobs during a 12-tick episode. A hidden `filter` or `sensor` fault determines the correct repair. Agents see their current public job, a shared manual, two noisy clues with declared accuracies 0.8 and 0.6, costs, deadline, and their own action/review history. Hidden faults and unreleased jobs are excluded from these observations.

The pinned Qwen2.5-7B-Instruct model makes two independently seeded GPU generation requests for the same observation. The first action executes immediately; the second is retained only to measure agreement. Every proposal joins the review queue. Valid wrong actions remain valid model outputs. The current error probability is the **provisional, uncalibrated constant `p=0.5`**, regardless of agreement; no calibration or online learning occurs.

Schedulers receive only immutable public review records for released, pending jobs: proposal, estimated error probability, request time, costs, deadline, and review duration. They cannot inspect hidden faults, future jobs, scorer loss, or another agent's feedback. The supervisor performs one nonpreemptive review at a time, taking exactly two ticks. Only when the review completes does it obtain definitive diagnostic information and command the correct action. The controller obeys immediately for an open job. Review cannot erase accumulated loss or reopen a closed job.

At each tick the simulator applies completed reviews, closes due jobs, releases new jobs and resolves their model calls, dispatches a review, then charges interval costs. Completion exactly at the deadline can prevent terminal loss. Inference wall time pauses the simulated clock, so hardware latency does not determine queue order. Full truth in saved scorer traces is offline diagnostic data, never a scheduler input.

## Loss and scheduling

For job `i`, release `r_i`, deadline `d_i`, downtime rate `c_i`, terminal cost `K_i`, action `a_i(t)`, and correct action `a_i*`, the episode loss sums

`loss_i = c_i Σ[t=r_i,...,d_i−1] 1[a_i(t) ≠ a_i*] + K_i 1[a_i(d_i) ≠ a_i*]`.

The preventable consequence of completing a review at `T` is

`G_i(T) = 1[T ≤ d_i] [c_i(d_i−T) + K_i]`.

All four policies skip requests with no positive estimated benefit at earliest completion `t+s_i`.

| Policy | Dispatch rule for feasible requests |
| --- | --- |
| FCFS | Earliest request, with agent ID as tie-break. |
| Uncertainty-first | Highest `p_i`; shared FCFS tie-break. Constant probabilities can make it identical to FCFS. |
| Myopic benefit | Highest `p_i G_i(t)`, ignoring service time in the ranking. |
| Queue-order search (`delay`) | Enumerate ordered subsets of the current queue and maximize `Σ_k p_i G_i(t+Σ_{j≤k}s_j)`; dispatch the first review and recompute when free. |

Queue-order search optimizes the current queue estimate, without anticipating arrivals. Tied plans prefer fewer reviews, then lexicographic request/agent order. Correct jobs at closure are reported alongside loss: a wrong job with both costs zero contributes zero loss.

## Assumptions and evidence

Supervision is **simulated**, with perfect diagnosis, fixed duration, and mandatory compliance. There are no human participants or measurements of workload, trust, or usability. Automatic review admission, two repair actions, independent synthetic jobs, public deterministic deadlines/costs, and uncalibrated probabilities are simplifying assumptions. Two samples can agree on an incorrect action; agreement is not a correctness guarantee.

The five [mechanics fixtures](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/mechanics/episodes.csv) stipulate actions to demonstrate arithmetic, correction, competition, expiry, and a baseline win. They are not model-quality observations. Measured live outcomes, raw requests, GPU placement, and independently replayed scores are linked in the [Ada report](../reports/STAGE1_GPU_LIVE.md), [episode CSV](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/episodes.csv), and [queue timeline](../artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/run/queue_timeline.md). One seed cannot support a general effectiveness claim or a meaningful scenario-level confidence interval. Calibration and larger paired experiments remain later work.
