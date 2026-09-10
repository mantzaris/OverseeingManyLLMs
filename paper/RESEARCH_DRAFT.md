# Planning a shared review queue for synthetic LLM maintenance agents

Research draft. Stage 4 results are inserted after the complete frozen evaluation; this working draft makes no outcome claims while inference runs.

## Abstract

Pending completed evaluation. The study compares online review-order policies inside a synthetic maintenance simulation using fresh generations from one frozen instruction-tuned language model. Its contribution is an auditable experimental framework and an analysis of interactions between risk estimates, supervisor capacity, workload, and performance objective. It does not propose exhaustive scheduling as a novel algorithm or measure human supervision.

## 1. Research question and motivation

When several LLM agents share one reviewer, a useful intervention may arrive too late. Ranking requests by their individual expected benefit can sacrifice opportunities that a different sequence would preserve. Conversely, planning can provide little benefit when contention is rare, or allocate attention poorly when its estimated error risks are inaccurate. A lower weighted maintenance cost can also coexist with more incorrect job closures. We ask when planning review order matters, how public risk information changes allocation, and how capacity and objective choice qualify the conclusions.

The setting is civilian synthetic campus ventilation maintenance. A binary hidden fault requires one of two repairs. There is one simulated supervisor, finite review duration, perfect diagnosis on completed review, and immediate compliance. These simplifications isolate scheduling mechanisms; they do not represent measured human behavior, real equipment performance, or general LLM alignment.

Stages 1–3 supplied development evidence. Stage 1 established GPU integration and a zero-loss four-policy tie. Stage 2 found identical greedy/search sequences and slightly lower FCFS losses. Its eight original-distribution validation scenarios were too small and rarely competitive. Stage 3 deliberately released simultaneous review waves. Search beat greedy in aggregate weighted loss but tied EDF at one-tick reviews; at two ticks it left more jobs incorrect than greedy. These observations motivated the present predeclared replication, risk comparison, capacity study, and objective extension. Historical results and their source snapshots remain preserved.

## 2. Formulation and information boundary

Job i has release r_i, deadline d_i, downtime cost c_i, and terminal cost K_i. While its executed action differs from the fault-specific correct repair, it incurs c_i per simulated tick; an incorrect closure incurs K_i. Episode loss is

`L = Σ_i { c_i Σ_(t=r_i)^(d_i−1) I[a_i(t) ≠ a_i*] + K_i I[a_i(d_i) ≠ a_i*] }`.

Correct-closure count is a separate outcome. In particular, a job with c_i=K_i=0 may close incorrectly without contributing to L. Completed review at T can prevent `G_i(T)=I[T≤d_i]{c_i(d_i−T)+K_i}` if the initial action is wrong. Completion exactly at the deadline can avoid terminal loss but cannot erase earlier downtime.

The agent sees only its released job's public parameters, two clues, the task manual, and its own action/review history. The first clue matches the fault with probability 0.8 and the second with probability 0.6, independently given the fault; the fault prior is uniform. The model produces two freshly sampled repair actions for the same observation. The first executes; the second supplies an agreement feature. All proposals request review automatically. Wrong valid actions are preserved. Hidden faults are available only for offline analysis, scoring, and diagnosis when supervision completes.

Schedulers receive immutable public pending-request records, including estimated initial-error probability p_i, proposal, arrival, costs, deadline, and review duration. Search sees no unreleased jobs or future arrivals. A single nonpreemptive reviewer serves one request at a time. Tick order is completed reviews, deadline closures, job releases and model calls, dispatch, then interval scoring. Inference latency pauses the simulation clock. Each policy/duration/risk condition has its own model calls and within-episode histories.

## 3. Policies, risks, and extension

All core policies share a positive-benefit eligibility check at earliest completion t+s. FCFS selects the earliest request; uncertainty-first the greatest p_i; myopic benefit the greatest p_i G_i(t); delay-aware greedy the greatest p_i G_i(t+s); EDF the earliest deadline. The shared deterministic tie rule uses request time, agent ID, and job ID. Queue-order search enumerates every ordered subset of the currently eligible queue, maximizes `Σ_k p_(i_k) G_(i_k)(t+k s)`, executes its first review, and replans when free. It is exact for this finite current-queue objective, not an oracle for future arrivals or realized faults. Ties in computed floating-point values prefer fewer reviews, then lexicographic request order. Six eligible requests yield 1,957 ordered subsets including empty; queues are checked, never truncated.

A pre-evaluation validity repair replaces order-dependent sequential floating-point summation with `math.fsum` in the Stage 4 search path. A saved development state had equal mathematical totals but differing rounded values across permutations. Historical implementations remain available for historical replay and audits. This repair preserves the declared objective and tie preference; it is documented in the decision log. On 1,920 saved Stage 3 dispatch states, it changes 42 hypothetical search first choices, all at one-tick reviews, and none at two ticks. This is a same-state audit, not a rerun of historical trajectories. A further exact-rational audit of 4,001 saved Stage 4 development states found no loss of expected value from the selected search head, but four differences from the canonical exact tie preference. Uniform risk rescaling changed ten hypothetical choices among 1,771 uniform-risk states; all were exactly co-optimal. Thus exhaustive enumeration is not a claim of exact rational tie arithmetic, and such changes carry no new risk-ranking information. The frozen execution is retained; the same audit is applied to evaluation.

Three immutable public risk rules are compared. The primary historical estimator is the exact Stage 2 artifact: agreement predicts 13/89; disagreement uses pooled fallback 18/98 because its calibration bin contained only nine observations. Its calibration labels concern initial first actions before correction, irrespective of whether reviewed. The pooled alternative uses 18/98 for every request. Neither is refitted.

The analytical reference knows the synthetic prior and observation likelihoods. It computes the posterior probability that the first proposed repair is wrong given the public clues. Following agreeing clues yields 1/7; following the stronger clue when they disagree yields 3/11. Choosing the opposite repair yields 6/7 or 8/11 respectively. Public costs and IDs add no fault information under the generator. This is an informed synthetic reference, not an automatically available deployment estimator. The second model sample is retained in every condition to keep inference protocol constant.

Development findings selected one optional extension, cost versus correctness. Search adds a declared incorrect-closure penalty λ∈{0,4,8}, replacing K_i by K_i+λ in both eligibility and expected intervention benefit. Original maintenance loss L and incorrect-closure count U remain unchanged in scoring. Comparisons additionally report common objectives L+kU for each fixed k∈{0,4,8} across all λ conditions, rather than comparing unlike own-objective values. The finite grid is a tradeoff study, not a proof of Pareto optimality or universal improvement. No imperfect-supervision or generation-replicate branch was added. With uniform estimated risk and terminal-only costs, adding λ contributes the same `m p λ` to every feasible plan of fixed length m. It therefore cannot change their mathematical ranking. In the three-request competition wave at two-tick duration, at most two reviews can finish usefully and every pair is feasible in an appropriate order. When all three risks coincide, λ has no allocation information to distinguish expected incorrect closures among those pairs. Larger queues with downtime and zero original-cost jobs can behave differently.

## 4. Workloads and frozen design

The original generator and Stage 3 generator are unchanged. Both use three agents, two jobs each, and 12 ticks. The competition condition releases three jobs at ticks 0 and 6, independently permutes deadline windows 2/4/5 and terminal penalties 4/8/12 within each wave, and sets downtime cost to zero. It is intentionally constructed after the Stage 2 competition limitation; replication within it does not turn it into a naturally representative task distribution. With zero downtime, myopic and delay-aware greedy have the same shared-state ranking after eligibility.

The separate larger workload uses three or six agents, three jobs each, and 24 ticks. Release waves have bases 0,8,16 plus independent jitter 0/1. Relative deadline windows are sampled from 2/4/6, downtime rates from 0/1/3, and terminal penalties from 0/4/8/12. Independent public-component and hidden-component streams keep costs and arrivals unrelated to faults. Stable per-agent/job streams make the first three agents' exogenous jobs identical across team sizes. Every job closes before the next wave; at most six outstanding requests are possible. Future releases remain hidden from schedulers.

Development used seeds 400–407 for risk pilots, 408–411 for the larger-workload pilot, and 412–415 for one objective-grid pilot. All 304 episodes completed; no seed was selected by favorable outputs. A separate diagnostic preselected 32 historical prompt hashes and made four identical-request repetitions each. It found no new mixed group in those 128 calls, but integrated development again produced a few mixed-action groups. Seeds are controls on requested sampling, not a promise of bitwise regeneration. Replay deterministically scores saved outputs, which is a different reproducibility claim.

The full evaluation was frozen before its first request:

| Study | Scenario seeds | Conditions | Fresh calls |
| --- | --- | --- | ---: |
| Replication | Original 10000–10063; competition 11000–11063 | Six policies; review durations 1/2; frozen risk | 18,432 |
| Risk ablation | First 32 declared seeds from each replication workload | Greedy/search; pooled/analytical; durations 1/2; reuse matching frozen rows | 6,144 |
| Capacity | Larger workload 12000–12031 | Three/six agents; FCFS/EDF/greedy/search; durations 1/2 | 13,824 |
| Objective extension | 13000–13015, each in competition a3 and larger a6 | Search; λ=0/4/8; durations 1/2 | 4,608 |

The evaluation contains 2,752 episodes. Its 64, 64, 32, and 16-per-extension-workload scenario sets are the statistical units; repeated policy/duration conditions are not independent scenarios. Matching numeric extension seeds across its two distributions do not justify pooling them. Policy order rotates and duration order is balanced. Sampling seeds exclude policy, risk, review duration, objective, and execution order. Each actual rollout nevertheless makes fresh GPU calls; supervision can change later prompts.

The model is Qwen/Qwen2.5-7B-Instruct revision `a09a35458c702b33eeacc393d103063234e8bc28`, BF16 on one RTX 6000 Ada, with zero CPU offloading. Decoding retains temperature 0.3, top-p 1.0, 48 maximum output tokens, and guided two-action JSON. Requests are serial, with at most one retry and the existing 60-second attempt timeout. The session ledger caps scheduled calls at 50,000 and actual generation attempts at 60,000. The nine-hour authorization reserves the final 90 minutes for reporting; a watchdog terminates experimental workers at the inference cutoff while preserving the serving process.

## 5. Analysis

The primary contrast is search minus greedy loss at two-tick reviews, separately for original and competition workloads. EDF is a prominent secondary comparator. We report means, paired scenario differences, wins/ties/losses, correct closures, corrections, review utilization, missed opportunities, and per-agent distributions. Scenario-paired percentile bootstrap intervals use 2,000 resamples and analysis seed 20260910. Each resample carries every condition of a scenario together. Intervals are descriptive, without multiplicity adjustment; extension and additional contrasts are secondary.

Brier scores and reliability summaries are computed from initial first-action labels on saved trajectories, by policy, duration, workload, and risk condition. Alternative probabilities can be scored on the same outputs without new generations. Those prediction diagnostics do not establish counterfactual policy effects, which require the fresh risk-specific rollouts. The ablation uses the matching 32-scenario frozen prefix, not all 64 replication rows.

Dispatch diagnostics compare alternative policies on identical saved public states and count multiple-eligible-request opportunities. Actual review sequences are separately compared across rollouts. We count differing observations, differing sampled actions, and differing actions despite identical full requests. Such diagnostics describe intertwined trajectory changes; they do not isolate a pure causal scheduling effect. Planning latency and ordered-subset counts are recorded independently of simulated time.

The declared trace rule selects the first numerical seed where search beats greedy and the first where it loses, at two ticks for each core workload (six agents for the larger workload); if a direction has no example, the first tie is labeled as a fallback. Extension examples use the first seed where λ=8 reduces incorrect closures but raises original cost. Failures are retained, incomplete pairs bounded, and failed seeds never replaced.

## 6. Measured evaluation results

Pending completion of the fixed matrix. Tables, paired intervals, figures, and trace interpretations will be inserted from audited saved outputs; the design above is frozen.

## 7. Related work and scope of contribution

[KnowNo (Ren et al., 2023)](https://arxiv.org/abs/2307.01928) connects LLM uncertainty with requests for help using conformal prediction. Our admission rule is fixed; the experimental question concerns ordering a shared review queue. [DeCCaF (Alves et al., 2024)](https://arxiv.org/abs/2403.06906) optimizes cost-sensitive deferral under expert capacity constraints, so neither cost-aware allocation nor limited-supervision optimization is new here. [Hariri, Potts, and Van Wassenhove (1995)](https://pubsonline.informs.org/doi/10.1287/ijoc.7.2.232) study weighted late-work scheduling, and [Guo et al. (2022)](https://onlinelibrary.wiley.com/doi/abs/10.1002/nav.22050) study scheduling tradeoffs involving late-work and tardy-job counts. Their objectives differ from our downtime and incorrect-closure loss, but establish the relevant scheduling context. The verified [related-work note](RELATED_WORK.md) records primary-source scope. We do not claim novelty for exhaustive queue enumeration, perfect simulated supervision, or adding a scalar count penalty.

The candidate contribution is an inspectable integration of actual LLM actions and feedback histories with an explicit public/private observation boundary, finite review time, time-dependent correction value, frozen risk estimates, and paired workload controls. Its scientific contribution must be the measured interactions and limitations, including null and negative findings, rather than the existence of a scheduler.

## 8. Limitations and reproducibility

One model/revision, a two-action fault task, a known observation model, automatic review requests, independent jobs, perfect diagnosis, mandatory compliance, and at most six pending requests sharply limit external validity. The analytical reference receives privileged knowledge of generating assumptions without seeing realized hidden labels. Agreement calibration is small and distribution-sensitive. Cost weights are designer choices; a policy's ranking can change under a different objective. Six-request enumeration does not establish large-queue scalability. Arrival-hidden current-queue optimization is not full-horizon optimal control.

Fresh GPU generations sometimes vary for identical requests. A single integrated trajectory per scenario/condition does not separate all generation variance from scenario variance. Scenario bootstrap intervals do not remove that limitation. Multiple secondary analyses and selected development workloads require cautious interpretation even when evaluation seeds were untouched during adaptation. There are no human participants, real maintenance incidents, or claims about measured human cognitive workload.

All source/configuration/scenario/estimator hashes, declarations, raw requests/responses, event streams, episode tables, clocks, and decision records are retained under `artifacts/stage4_research/`. Compressed raw evidence round-trips byte-for-byte. The report supplies exact audit, replay, analysis, and rendering commands. Historical artifacts and commands keep their original limits. New inference requires a fresh explicit authorization after this session; saved-output analysis needs no GPU.
