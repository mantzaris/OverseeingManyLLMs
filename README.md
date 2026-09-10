# OverseeingManyLLMs

A reproducible backbone for studying how one simulated human supervisor allocates review time across three or six LLM agents doing synthetic civilian maintenance tasks. It implements generation, public observations, GPU actions, a frozen agreement estimator, a review queue, six schedulers, corrective interventions, loss scoring, and independent replay.

Start with the completed [Stage 4 research report](reports/STAGE4_RESEARCH.md), [research draft](paper/RESEARCH_DRAFT.md), [competition report](reports/STAGE3_COMPETITION.md), [Stage 2 report](reports/STAGE2_DEVELOPMENT.md), [core method](paper/CORE_METHOD.md), and [proof-of-concept plan](plan/PROOF_OF_CONCEPT_PLAN.md). The runtime uses an **RTX 6000 Ada**, the pinned **Qwen2.5-7B-Instruct** model, BF16, and zero CPU offloading. Supervision is simulated. Stage 1's [preserved GPU report](reports/STAGE1_GPU_LIVE.md) records its four-policy zero-loss tie with no corrections.

Stage 2 adds an offline agreement-based error estimator and a delay-aware greedy baseline. Calibration uses 16 FCFS episodes with provisional **p=0.5**; the frozen estimator then drives five policies on eight development scenarios. The declared scope is 56 episodes, 672 experimental calls, and at most one placement generation. A bin with fewer than ten calibration examples uses the smoothed pooled estimate. This development batch is not a held-out effectiveness study.

All 56 episodes completed and replayed: **672 experimental generations plus one placement**, with no retries or failures. Calibration had 87 agreeing pairs (12 errors) and nine disagreeing pairs (five errors), so disagreement used pooled fallback. Validation loss totaled 60 for FCFS/uncertainty-first and 62 for myopic/greedy/queue search; each policy corrected two jobs. Queue search and greedy chose identical review orders on all eight scenarios. These ties and negative results are retained.

## Inspect and verify

Core host simulation and replay require Python 3.8+ and the standard library. Stage 4 summaries and its integration checks also use NumPy; figure rendering uses Matplotlib (`requirements-analysis.txt`). Exact analysis versions are saved with the research artifacts. These commands perform no model inference:

```bash
python3 -m unittest discover -s tests -v
python3 -m overseeing mechanics --out artifacts/local-mechanics
python3 -m overseeing replay artifacts/local-mechanics/competition/delay/events.jsonl
python3 -m overseeing development-mechanics --out artifacts/local-development-mechanics
python3 scripts/verify_development.py artifacts/stage2_development/run
python3 scripts/verify_competition.py artifacts/stage3_competition/run

task_artifacts=artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z
python3 scripts/verify_live_results.py "$task_artifacts/run"
for policy in fcfs uncertainty myopic delay; do
  python3 -m overseeing replay "$task_artifacts/run/$policy/events.jsonl"
done
```

Use a fresh mechanics output directory on repeat runs. The five examples use **stipulated actions as mechanics fixtures**. Live raw requests/responses, episode CSV, event traces, queue timeline, GPU evidence, exact environment versions, and the executed source snapshot are saved together under [the Ada artifact directory](artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/). The verifier uses that snapshot so later source changes do not invalidate the historical audit.

The [development artifacts](artifacts/stage2_development/run/) contain the pre-inference declaration, frozen estimator, raw attempts, all 56 episode rows, replayable traces, per-policy Brier scores, paired scenario differences, and dispatch-competition diagnostics. The development verifier recomputes diagnostics from saved outputs without generation requests.

## Verified GPU setup

In a dedicated pod checkout, the setup used the available Python 3.11.13 and these commands:

```bash
uv venv --python python3.11 .venv
timeout 5400 uv pip install --python .venv/bin/python -r requirements-gpu.txt
HF_HOME="$PWD/model-cache" bash scripts/serve_gpu.sh
```

The launcher serves the pinned model and tokenizer revision `a09a35458c702b33eeacc393d103063234e8bc28` on `127.0.0.1:8000`. It requires one verified L40S or RTX 6000 Ada with at least 45,000 MiB VRAM and native CUDA BF16. The 0.5 memory reservation, tensor parallelism 1, CPU offload 0, and swap 0 are fixed. Keep Jupyter and other existing services running.

The [report](reports/STAGE1_GPU_LIVE.md) records the exact SSH, isolated directory, detached server launch, and one-shot demonstration command, with server PID, logs, and full resolved dependency versions. The live CLI accepts `--continuation stage1_gpu_live_rtx6000_ada`, using its recorded deadline by default or an earlier explicit `--deadline-utc`. It retains the original overall deadline and rejects unknown, expired, or overlong continuation windows. Saved runs cannot be overwritten; the recorded demonstration wrapper also refuses a repeat execution.

The separate development path predeclares source/configuration hashes and ordered episodes before inference:

```bash
python3 -m overseeing prepare-development --out artifacts/stage2_development/run
.venv/bin/python -m overseeing develop --out artifacts/stage2_development/run \
  --server-pid 7338 \
  --server-log artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/server.log \
  --deadline-utc 2026-09-10T03:07:01+00:00
```

These are historical execution commands. Existing outputs and the one-shot execution marker prevent repetition. The named Stage 2 authorization and original overall deadline remain enforced; subsequent inference requires its own authorization.

## Preserved history and scope

The [original backbone report](reports/STAGE1_GPU_BACKBONE.md), [blocked recovery](reports/STAGE1_GPU_RECOVERY.md), and [first L40S live report](reports/STAGE1_GPU_L40S.md) remain available with their original artifacts. All clocks are retained in [implementation_clock.json](reports/implementation_clock.json).

The declared development calibration and fifth baseline are implemented. The separate Stage 3 condition adds deadline-first scheduling and a one-versus-two-tick review comparison. Stage 4 extends this history with frozen evaluation seeds, a larger workload, public risk references, and a research draft. Advanced tasks and real-human validation remain outside the implemented scope. Weights, environments, and credentials are excluded from Git. Nothing is pushed automatically.

## Stage 3 competition diagnostic

Motivated by Stage 2's limited competition, a separate generator releases three jobs together at ticks 0 and 6, independently permutes deadline windows 2/4/5 and penalties 4/8/12, and sets downtime costs to zero. The frozen Stage 2 estimator is reused without fitting. Six policies, two review durations, and seeds 300–315 give **192 episodes / 2,304 experimental calls**, with one separate placement request. The 192 repeated conditions represent 16 paired scenarios, not 192 independent observations. Historical policy lists and commands retain their original scope.

All 192 episodes completed and replayed with **2,305 total GPU generations, zero retries/failures**. At one tick, search and EDF tied at loss 0 versus greedy's 12. At two ticks, search totaled 44 versus greedy's 52 and EDF's 84, while losing on individual scenarios. Search/greedy orders differed in 15/16 and 14/16 scenarios. These deliberately constructed development results are separate from Stage 2; exact regenerated actions are not assured, and every saved result remains replayable.

[Declaration and raw evidence](artifacts/stage3_competition/run/), [paired-loss figure](artifacts/stage3_competition/run/paired_loss.png), and [first differing queue example](artifacts/stage3_competition/run/queue_example.md) accompany the [report](reports/STAGE3_COMPETITION.md). Verify saved results with the command above. Recreate the figure with `python3 scripts/plot_competition.py artifacts/stage3_competition/run` (requires Matplotlib; the audit itself uses only the standard library).

Historical execution commands, guarded against overwriting or rerunning the saved batch:

```bash
python3 -m overseeing prepare-competition --out artifacts/stage3_competition/run
.venv/bin/python -m overseeing competition --out artifacts/stage3_competition/run \
  --server-pid 7338 \
  --server-log artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/server.log \
  --deadline-utc 2026-09-10T04:47:37+00:00
```

The separately recorded Stage 3 authorization lasts at most two hours and remains within the original overall deadline. Earlier command deadlines are unchanged. That historical authorization ends with its batch; Stage 4 uses its own separately recorded scope.

## Stage 4 research session

The bounded research session completed **2,752 frozen evaluation episodes plus 304 development episodes**, all replayed, with **48,320 successful GPU generations, zero retries and zero failures**. The [completed report](reports/STAGE4_RESEARCH.md), [register](artifacts/stage4_research/RESEARCH_PLAN.md), and [decisions](artifacts/stage4_research/decisions.jsonl) distinguish development from frozen evaluation. The execution used a shared 50,000-call / 60,000-attempt ledger and reserved the final 90 minutes before the stage deadline for reporting. All experimental workers have stopped; the existing GPU server and pod files remain intact. Historical commands retain their previous limits. No claim is made that equal sampling seeds reproduce identical GPU actions.


The main findings are conditional. Search minus greedy mean loss at two ticks is **−0.094** on the original workload (95% paired interval includes zero), and **−1.313** on the constructed competition workload ([−2.250, −0.438]). EDF matches search's zero loss at one-tick competition. Larger-workload planning gains are strong at one tick but small at two. Analytical public risk improves prediction scores without consistently improving allocation. Adding an incorrect-closure penalty reduces wrong closures at one tick while increasing original cost; null and negative results are retained. See the report for all policies, per-agent outcomes and scenario-paired comparisons.

The [saved-output reproduction guide](artifacts/stage4_research/REPRODUCE.md) gives exact audit and rendering commands. The new larger workload supports three or six agents, three jobs per agent, a 24-tick horizon, and at most six outstanding requests. Search enumerates every ordered subset of the eligible public queue; no queue truncation or future-arrival access is used. Frozen agreement, pooled calibration, and analytical public-clue risk rules are compared without refitting. The selected extension adds a declared incorrect-closure penalty while retaining original maintenance loss as a separate metric.

```bash
python3 scripts/analyze_research.py --batches evaluation --label evaluation
python3 scripts/audit_numerical_ties.py --batches evaluation --label evaluation
python3 scripts/audit_objective_null.py
python3 scripts/plot_research.py
python3 scripts/research_traces.py
python3 scripts/research_tables.py
python3 scripts/audit_research_session.py
```

The [research draft](paper/RESEARCH_DRAFT.md), [claim–evidence map](paper/CLAIM_EVIDENCE.md), and [verified related-work note](paper/RELATED_WORK.md) distinguish the framework and measured analysis from established scheduling and uncertainty-guided help-seeking methods. Supervision remains simulated; exhaustive scheduling itself is not claimed as novel.
