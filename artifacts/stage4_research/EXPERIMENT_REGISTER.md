# Experiment register

All clocks, initial hypotheses, and original declarations remain in RESEARCH_PLAN.md, authorization.json, and batches/*/declaration.json. Decisions are append-only in decisions.jsonl.

| Study | Question / fixed data | Calls | Development finding / next decision |
| --- | --- | ---: | --- |
| D0 diagnostic | 32 deterministically selected saved prompts × 4 identical repetitions | 128 | No mixed actions in this bounded set; historical and later integrated variation remains. No further diagnostic generations. |
| D1 saved trajectories | Stage 2 validation and Stage 3; three public risk rules | 0 | Analytical Brier improves on competition, worsens slightly on small original sample. Run actual risk-specific trajectories. |
| D2 risk pilot | Seeds 400–407; original/competition; frozen/pooled/analytical; greedy/search; s=1/2 | 2,304 | At s=2 frozen search and greedy tie in both workloads; analytical changes some decisions/losses. Preserve all three risks for declared ablation. |
| D3 capacity pilot | Seeds 408–411; 3/6 agents; FCFS/EDF/greedy/search; s=1/2 | 1,728 | Six outstanding requests, valid short contexts. Search can lower cost while closing more jobs incorrectly than EDF. Select branch A. |
| D4 objective pilot | Seeds 412–415; competition a3/larger a6; search; λ=0/4/8; s=1/2 | 1,152 | Mostly ties; no clear improvement. Keep grid unchanged, no second iteration. |
| E-A replication | Original 10000–10063, competition 11000–11063; six policies; s=1/2; frozen risk | 18,432 | Frozen before evaluation; see evaluation summary when completed. |
| E-B risk ablation | First 32 seeds of each E-A workload; greedy/search; pooled/analytical; s=1/2 | 6,144 | Matching frozen rows reused from E-A; alternative trajectories use fresh calls. |
| E-C capacity | 12000–12031; 3/6 agents; four policies; s=1/2 | 13,824 | Nested public/private scenario streams, no future arrivals visible to planners. |
| E-D objective | 13000–13015; same fixed objective grid as D4 | 4,608 | One selected secondary extension; no universal-superiority claim. |

Total declared calls: **48,320**, of which 38,400 core evaluation and 5,760 total branch calls. The complete evaluation is 2,752 episodes and 43,008 calls. The 304 development episodes and 128 repeated diagnostic requests remain separate from evaluation. No added calibration or placement generation.

Primary comparisons: search minus greedy maintenance loss at s=2, separately original and competition. EDF is a prominent secondary comparator. Scenario-level paired bootstrap: 2,000 resamples, seed 20260910. Distributions remain separate. Full method, settings, execution order, scenario hashes, source hashes, failure handling, trace selection and analysis definitions are frozen in the evaluation declaration.
