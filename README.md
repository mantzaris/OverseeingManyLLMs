# OverseeingManyLLMs

A reproducible backbone for studying how one simulated human supervisor allocates review time across three LLM agents doing synthetic civilian maintenance tasks. It implements generation, public observations, GPU actions, a frozen agreement estimator, a review queue, six schedulers, corrective interventions, loss scoring, and independent replay.

Start with the [competition report](reports/STAGE3_COMPETITION.md), [Stage 2 report](reports/STAGE2_DEVELOPMENT.md), [core method](paper/CORE_METHOD.md), and [proof-of-concept plan](plan/PROOF_OF_CONCEPT_PLAN.md). The runtime uses an **RTX 6000 Ada**, the pinned **Qwen2.5-7B-Instruct** model, BF16, and zero CPU offloading. Supervision is simulated. Stage 1's [preserved GPU report](reports/STAGE1_GPU_LIVE.md) records its four-policy zero-loss tie with no corrections.

Stage 2 adds an offline agreement-based error estimator and a delay-aware greedy baseline. Calibration uses 16 FCFS episodes with provisional **p=0.5**; the frozen estimator then drives five policies on eight development scenarios. The declared scope is 56 episodes, 672 experimental calls, and at most one placement generation. A bin with fewer than ten calibration examples uses the smoothed pooled estimate. This development batch is not a held-out effectiveness study.

All 56 episodes completed and replayed: **672 experimental generations plus one placement**, with no retries or failures. Calibration had 87 agreeing pairs (12 errors) and nine disagreeing pairs (five errors), so disagreement used pooled fallback. Validation loss totaled 60 for FCFS/uncertainty-first and 62 for myopic/greedy/queue search; each policy corrected two jobs. Queue search and greedy chose identical review orders on all eight scenarios. These ties and negative results are retained.

## Inspect and verify

Host code requires Python 3.8+ and the standard library. These commands perform no model inference:

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

The declared development calibration and fifth baseline are implemented. The separate Stage 3 condition adds deadline-first scheduling and a one-versus-two-tick review comparison. Held-out evaluation seeds, larger experiments, advanced tasks, estimator changes, and a full manuscript remain later work. Weights, environments, and credentials are excluded from Git. Nothing is pushed automatically.

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

The separately recorded Stage 3 authorization lasts at most two hours and remains within the original overall deadline. Earlier command deadlines are unchanged. Stop after this batch; further inference requires a new authorized scope.

## Stage 4 research session

A separately authorized nine-hour research session is underway. The [working report](reports/STAGE4_RESEARCH.md), [register](artifacts/stage4_research/RESEARCH_PLAN.md), and [decisions](artifacts/stage4_research/decisions.jsonl) distinguish development from frozen evaluation. New entry points use a shared 50,000-call / 60,000-attempt ledger and stop inference 90 minutes before the stage deadline. Historical commands retain their previous limits. No claim is made that equal sampling seeds reproduce identical GPU actions.
