# Coordinated changes in the Decision desk

A user changes a reporting requirement once. The controller identifies applicable roles, sends scoped instructions, runs their tool choices and checks actual uptake. The analysis table feeds a chart, which feeds numerical report claims. A protected appendix keeps its original contract.

The package uses recorded **UCI Online Retail** transactions. Briefs, roles, changes and stress cases are constructed; model continuations are genuine GPU outputs. It is not a study of real users. See [REPORT.md](REPORT.md), [METHOD.md](METHOD.md), [DATA.md](DATA.md), [LITERATURE.md](LITERATURE.md) and [API.md](API.md). Historical research and submission files remain unchanged.

The strict-parser primary comparison and the separately declared parser-repair follow-up are both preserved. Targeted and same-packet global checking make identical requests on these registered contracts. In the follow-up each completes 16/16 projects in 46 calls, versus 64 calls for broadcast. The zero-inference parameterized pipeline is sufficient for the supported application. See [PARSER_FOLLOWUP.md](PARSER_FOLLOWUP.md) and the [worked example](WALKTHROUGH.md).

## Reproduce saved results

Tested environment: Python 3.8.10, SQLite 3.31.1, NumPy 1.22.1, Matplotlib 3.1.2 and openpyxl 3.1.5. Install the listed dependencies in an isolated environment if needed. For a different Python version, compatible NumPy/Matplotlib versions can reproduce numeric tables, but figure bytes and fonts may differ.

```bash
python3 -m pip install -r research/coordination_injections/requirements.txt
python3 -m research.coordination_injections.reproduce --download --output /tmp/coordination-replay
```

The second command retrieves the pinned official source if absent, verifies all 541,909 transformed rows, reconstructs 328 study traces and their 1,053 requests, including the exploratory parser follow-up, checks the published tables and regenerates figures. **No inference is performed.** The source ZIP is about 24 MB and remains outside Git in `/tmp/coordination-sources/`. Existing source-audit records are checked, not overwritten.

For figures alone, using the committed numeric evidence and no download:

```bash
python3 -m research.coordination_injections.plot
```

## Run the demonstration

```bash
python3 -m research.coordination_injections.prototype.server --port 9033
```

Open http://127.0.0.1:9033. Choose a saved project and method, apply its change once, and inspect individual responses or the final outcome. Expand evidence to inspect actual SQL, tool parameters and dependency fingerprints. The optional custom-change panel runs the deterministic parameterized pipeline on the real snapshot. It is explicitly distinguished from saved GPU replay.

```bash
node research/coordination_injections/prototype/browser_smoke.mjs /tmp/coordination-browser
```

The scripted browser checks produce screenshots and an interaction log, not participant observations. Ctrl-C stops the local desk. It does not stop the existing GPU server.

## Focused verification and collection provenance

```bash
python3 -m research.coordination_injections.tests
python3 -m research.coordination_injections.test_normalize
python3 -m research.coordination_injections.freeze verify
python3 -m research.coordination_injections.replay
bash paper/coordination_injections/build.sh
```

The frozen collection command was:

```bash
python3 -m research.coordination_injections.collect evaluation --revision frozen
```

It uses the existing Qwen2.5-7B-Instruct service through local port 8021. The original authorized tunnel was `ssh -F /tmp/overseeing_stage2_ssh_config -N -L 8021:127.0.0.1:8000 overseeing-development`, using the previously authenticated pod at `root@38.80.152.248:33513`. The pod checkout/environment and server were reused. The exact serving command and hardware/model identity are saved in `gpu_initial.json`; the pinned revision is `a09a35458c702b33eeacc393d103063234e8bc28`, BF16, one GPU, zero CPU offload. Final-generation settings are temperature 0.3, top-p 1, 384 output tokens and a 2,048-token context limit, with serial calls.

The historical authorization and cutoff remain enforced. Running this command on its existing cache does not create a fresh replication. A future GPU replication requires new explicit authorization, a separate resource ledger and artifact namespace. Do not reset the saved stage clock or call saved outputs new inference.

## Evidence locations

- `artifacts/coordination_injections/frozen/`: committed declaration and source archive.
- `raw/`, `attempts.jsonl`: every request, attempt and retained development interruption.
- `development/`: failed interfaces and the final competence pilot.
- `evaluation/frozen/`: paired originals, actual method-specific continuations and deterministic comparator.
- `analysis/`: per-project CSV, artifact/event tables, paired intervals, format/stress controls and request-variation diagnostics.
- `synthetic/`: authored mechanism cases, zero inference.
- `figures/`: PDF/SVG/PNG exports and source-specific captions.
- `parser_followup/`: committed separate declaration, 80 new continuations, 250 requests and matched analysis on already inspected cases.
- `interface/` and `interface_final/`: preserved original and final scripted browser screenshots, 13 final checks and interaction evidence.
- `paper/coordination_injections/main.pdf`: separate illustrated research draft, preserving the historical submission.
- `resource_ledger.json`: separate stage and cumulative accounting.

The work measures structured task completion, communication and machine costs. It does not equate fewer calls with lower experienced cognitive load. A parameterized pipeline or global check matching the method is a meaningful finding.
