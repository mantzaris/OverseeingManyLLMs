# OverseeingManyLLMs
how an operator can manage many ongoing llms

See the [proof-of-concept plan](plan/PROOF_OF_CONCEPT_PLAN.md) and [Stage 1 report](reports/STAGE1_GPU_BACKBONE.md). The first bounded backbone is implemented; GPU integration remains blocked by SSH access. Calibration and evaluation are not implemented or authorized in this stage.

The host code needs Python 3.8+ and the standard library. Focused checks and the stipulated mechanics demonstration perform no model inference:

```bash
python3 -m unittest discover -s tests -v
python3 -m overseeing mechanics --out artifacts/local-mechanics
python3 -m overseeing replay artifacts/local-mechanics/competition/delay/events.jsonl
```

Output directories must be new, preserving earlier traces. The report contains the bounded live GPU command and the exact connection blocker. All live inference requires the allocated A100 and the pinned Qwen model; there is no CPU inference path.
