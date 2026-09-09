# Stage 1 GPU recovery: connection blocked before authentication

**GPU inference did not succeed.** The registered RSA private key at `~/.ssh/id_rsa` is readable with mode `0600`. The new direct SSH endpoint still cannot be reached from this execution environment: socket creation is prohibited. This recovery adds a separate connection record and explicitly incomplete outcomes; it does not represent another implementation completion or new mechanics evidence.

One bounded direct attempt used the exact requested command:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 \
  -i ~/.ssh/id_rsa -p 19211 root@209.170.80.132 \
  'hostname; nvidia-smi'
```

It exited **255**, with this output:

```text
socket: Operation not permitted
ssh: connect to host 209.170.80.132 port 19211: failure
```

The SSH-agent probe also returned `Error connecting to agent: Operation not permitted`. The direct connection failed before authentication, so server acceptance of the registered key remains unverified. No gateway retry or restriction bypass was attempted. Key contents were not displayed or copied; no keys were generated or replaced. See [connection.json](../artifacts/stage1_gpu_recovery/connection.json).

No remote command ran. Actual GPU model, VRAM, driver, CUDA/BF16 capability, available disk/RAM, Python, installed packages, processes, and services are **unknown**. The user may have changed hardware; this report does not assume an A100. No installation, model download, compatibility repair, inference, or service change occurred. **Final inference-server status: unknown; the pod and its persistent files were untouched.**

The unexecuted target remains **Qwen/Qwen2.5-7B-Instruct**, revision **`a09a35458c702b33eeacc393d103063234e8bc28`**, **BF16**, with planned **vLLM 0.10.2 / PyTorch 2.8.0 / Transformers 4.55.2 / Python 3.11**. These are requested pins, not observed pod versions. [The launch script](../scripts/serve_gpu.sh) and [placement validator](../overseeing/gpu.py) were inspected and remain unchanged. They require the original A100 configuration, GPU-resident serving processes, CUDA logs, and zero CPU offloading. Adapting validation to replacement hardware requires actual hardware evidence first. No GPU placement evidence or measured throughput exists from this attempt.

The recovery started **2026-09-09 17:58:37 UTC**, with its own authorized deadline **2026-09-09 19:58:37 UTC**. At the report checkpoint **2026-09-09T18:04:11+00:00**, recovery elapsed time was **334 seconds** and overall elapsed time was **8714 seconds**. The recovery commit's committer timestamp marks completion of the final Git step. The original implementation start **2026-09-09 15:38:57 UTC**, Stage 1 deadline **2026-09-09 19:38:57 UTC**, and overall deadline **2026-09-11 03:38:57 UTC** are preserved in [implementation_clock.json](implementation_clock.json). Time between stages counts toward the overall window. Existing CLI deadline enforcement was not removed or extended; it still rejects a live deadline beyond the original Stage 1 cap. No live command was attempted against either deadline.

| Policy | Outcome | Loss / correct jobs | Planned calls | Scheduled calls | Attempts | Tokens |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| FCFS | Blocked before start | Unknown / unknown | 12 | 0 | 0 | 0 |
| Uncertainty-first | Blocked before start | Unknown / unknown | 12 | 0 | 0 | 0 |
| Myopic benefit | Blocked before start | Unknown / unknown | 12 | 0 | 0 | 0 |
| Queue-order search | Blocked before start | Unknown / unknown | 12 | 0 | 0 | 0 |

**Experimental calls:** 48 planned, **0 scheduled, 0 attempts, 0 prompt/output tokens, 0 seconds request time**. **Separate placement request:** one planned, **0 scheduled, 0 attempts, 0 tokens**. No simulated ticks ran, and no task loss was measured. Reviews and corrections were never exercised in live runs. All unstarted outcome scores remain null/blank, never zero-loss successes. No completed live traces exist to replay; replay verification is **not applicable**, rather than passed.

The saved [manifest](../artifacts/stage1_gpu_recovery/manifest.json) retains seed 100, three agents, two jobs each, 12 ticks, review duration two, all four policies, provisional uncalibrated `p=0.5`, and the existing call/retry limits. The [CSV](../artifacts/stage1_gpu_recovery/episodes.csv) contains all four blocked rows. Each policy directory has one `run_blocked` JSONL event, an empty raw-request file, and a readable status trace. The placement raw-request file is also empty. The [combined trace](../artifacts/stage1_gpu_recovery/trace.md) and timeline explicitly show that no episode ran. There are no fabricated responses, proposals, corrections, or GPU timelines.

The blocked-record command took **0.005131 seconds** inside the CLI; that is local artifact-writing time. Allocation start/end, billed intervals, GPU rental rate, allocation duration, and charges for the new pod are **unknown**, independently of zero request time. The former A100's quoted rate is not applied to unverified replacement hardware.

Original [Stage 1 artifacts](../artifacts/stage1/) and [report](STAGE1_GPU_BACKBONE.md) are preserved. Their stipulated mechanics checks were not rerun or counted as new GPU evidence. [Artifact checks](../artifacts/stage1_gpu_recovery/artifact_checks.json) verify only truthful blocked records, preservation of prior files, and unchanged source/configuration. No implementation, calibration, extra seed, baseline, development matrix, or evaluation was added.

To reproduce the local blocked-record package with the captured connection evidence, use a new output directory:

```bash
python3 -m overseeing record-blocked --config configs/stage1.json \
  --connection artifacts/stage1_gpu_recovery/connection.json \
  --out artifacts/local-recovery-record
```

Exit code 2 is intentional. This command writes status artifacts; it does not retry SSH or perform inference. No new live reproduction command has been validated.

The smallest useful next step is to establish ordinary SSH access to the new endpoint from an execution environment that permits it, inspect the actual GPU, and complete the same placement request plus four seed-100 runs. If the original Stage 1 deadline has expired, the live CLI needs explicit support for a still-authorized recovery deadline while retaining the overall cap; later work needs new authorization once this recovery window ends. Real runtime compatibility, GPU placement, live scoring/replay, and policy outcomes remain unverified. This stage stops at the concrete connection blocker. Nothing was pushed.
