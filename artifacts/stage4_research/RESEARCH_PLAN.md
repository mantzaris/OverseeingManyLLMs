# Stage 4 research register (initial plan)

Authorized start 2026-09-10 03:48:53 UTC; hard finish 12:48:53; all inference stops by 11:18:53, reserving 90 minutes. Caps: 50,000 scheduled calls, 60,000 generation attempts, one retry per ordinary call. Historical clocks/limits are unchanged.

| ID | Hypothesis / question | Development data / initial budget | Status |
| --- | --- | --- | --- |
| D0 | Identical seeded requests sometimes vary; assess frequency without stability-seeking reruns | 128 fixed diagnostic requests from saved Stage 3 prompts | Selection to be frozen before requests |
| D1 | Public Bayesian risk may rank requests differently from coarse agreement bins | Saved Stage 2/3 trajectories; no generations | Offline analysis |
| D2 | Better predictions may change greedy/search allocation | Seeds 400–407; original + competition; 3 estimators; greedy/search; durations 1/2; 2,304 calls | Pilot declaration pending checks |
| D3 | Staggered, larger queues expose capacity/planning tradeoffs | Seeds 408–411; 3/6 agents; 4 policies; durations 1/2; 1,728 calls | Pilot declaration pending checks |
| D4 | At most one unresolved extension chosen from D0–D3 | Unused development seeds 412–463; at most 6,000 calls, two iterations | No branch selected |
| E | Frozen evaluation A/B/C and optional one branch | Target core 38,400 calls; prefixes set from measured forecast before outcomes | Not started |

D2+D3 = 4,032 calls (approximately 4,000). Diagnostic calls count toward the session ceiling. No calibration refit. Evaluation definitions and optional branch will be frozen after development; no evaluation-driven redesign. Main comparison: search minus greedy at two ticks, separately original and constructed workloads; EDF prominent. Scenario-level paired bootstrap: 2,000 draws, fixed analysis seed 20260910. Exact enumeration, no queue truncation, at most six pending.

All primary policy runs use fresh GPU generations. Fixed scenario streams and sample seeds do not promise identical GPU outputs. Saved traces must replay deterministically.
