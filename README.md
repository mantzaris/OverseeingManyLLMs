# OverseeingManyLLMs
how an operator can manage many ongoing llms

See the [proof-of-concept plan](plan/PROOF_OF_CONCEPT_PLAN.md) and [first live GPU report](reports/STAGE1_GPU_LIVE.md). The seed-100 demonstration completed on an L40S: one placement request, 48 experimental requests, and four verified replays. All four policies tied at loss 0 with 5/6 jobs correct. Calibration and evaluation remain outside this stage. Earlier blocked attempts are preserved in the [original Stage 1 report](reports/STAGE1_GPU_BACKBONE.md) and [recovery report](reports/STAGE1_GPU_RECOVERY.md).

The host code needs Python 3.8+ and the standard library. Focused checks and the stipulated mechanics demonstration perform no model inference:

```bash
python3 -m unittest discover -s tests -v
python3 -m overseeing mechanics --out artifacts/local-mechanics
python3 -m overseeing replay artifacts/local-mechanics/competition/delay/events.jsonl
```

Audit the saved GPU results without new inference:

```bash
python3 scripts/verify_live_results.py artifacts/stage1_gpu_live/run
```

Output directories must be new, preserving earlier traces. The live report records exact commands, runtime, raw responses, and limitations. Inference requires the verified L40S, pinned Qwen model, BF16 CUDA placement, and zero CPU offloading. The CLI accepts a named, explicitly recorded continuation while enforcing its two-hour limit and the unchanged overall deadline.
