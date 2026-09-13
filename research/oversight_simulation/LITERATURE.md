# Modeling rationale and closest established explanation

No retrieved source calibrates orientation time, retention, correction probability
or carryover for this TAT-QA review task. All numerical reviewer parameters are
analyst-selected. Prior publications motivate components and comparators, not
transportable human-performance constants.

| Source | What supports this model | Limit and closest competing explanation |
|---|---|---|
| [Iqbal and Horvitz, CHI 2007](https://www.erichorvitz.com/CHI_2007_Iqbal_Horvitz.pdf), sections on lifecycle, deployment and recovery analysis | Separates returning to an application from restoring task context; uses activity logs and interviews to examine interruption and resumption. | Desktop-work observations do not supply financial-review times. We model recency and intervening work conditionally, without claiming this retention function was fitted or validated. |
| [Potts and Kovalyov, 2000](https://doi.org/10.1016/S0377-2217(99)00153-8), *Scheduling with batching: A review*, EJOR 120:228-249 | Established setup/batching perspective motivates the tradeoff between reducing repeated context setup and delaying other work. | Setup-aware ordering is the strongest simpler explanation. The preceding repository review inspected publisher model material; this stage's DOI fetch returned an access error. No new full-text or algorithm-reproduction claim is made. |
| [Zhu et al., ACL-IJCNLP 2021](https://aclanthology.org/2021.acl-long.254/), TAT-QA | Original hybrid financial table/text task and released annotations/scorer supply authentic task inputs and a correctness reference. | An annotation-based simulated repair is not observed human expertise. The source does not supply our arrivals, service times or supervision policy. |

The original literature package at `research/attention_sessions/LITERATURE.md`
contains the broader interruption and batching comparison. The current workflow
paper already compares AgentGUI and AGDebugger. This stage does not claim a new
queue, batching algorithm, memory model or user interface. Its contribution is a
reproducible conditional operating map with strong controls, genuine low-quality
LLM drafts and exact workflow accounting. A group-card benefit cannot be inferred
when an identically source-aware queue obtains the same modeled advantage.

The author-hosted Iqbal/Horvitz PDF was reopened in this stage, including methods
and analysis, not just its abstract. No numerical observations from that paper are
used as our timing calibration. No additional participant evidence is implied.
