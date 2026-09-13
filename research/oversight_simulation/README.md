# Computational oversight study

**This package contains simulations, not participant observations.** It reuses six
real TAT-QA financial table/text contexts, 36 original questions and their actual
saved drafts. Reviewer times, decisions, repairs and arrivals are modeled. No new
inference was performed. The frozen matched-qgm-v1 study and its manuscript remain
unchanged.

The study completed 31,680 runs from a committed 66-setting design. Grouping helps
over FIFO in some modeled operating regions, but never has a greater cell-mean
correct-release count than a queue using the same bounded source-aware navigation.
See [REPORT.md](REPORT.md) for the unfavorable findings, error tradeoffs and limits.

## Reproduce from a clean checkout

From the repository root, using Python 3 with NumPy, pandas and matplotlib, plus
`pdflatex` for the illustrated note:

```bash
bash research/oversight_simulation/reproduce.sh
```

This verifies the original frozen code/input hashes and regenerates numerical
analyses, nine vector/PNG figures, the report and separate illustrated PDF from
saved simulation outputs. It does not run a model, read human records, reset a
clock or rewrite the declaration. Existing repository Python dependencies suffice;
the recorded environment used Python 3.8. LaTeX needs standard `article`,
`geometry`, `graphicx`, `amsmath`, `booktabs` and `hyperref` packages.

For complete command replay, official re-scoring and historical-file preservation:

```bash
bash research/oversight_simulation/reproduce.sh --verify-all
python3 -m unittest discover -s research/oversight_simulation/tests -v
```

Full verification took about five minutes on the recorded host. Twelve focused
tests cover information isolation, common familiarity, paired draws, manual draft
isolation, cutoff, failure and release semantics. Simulation results use a separate
record schema and must never be passed off as practice or participant exports.

## Inspect the evidence

- [MODEL.md](MODEL.md): frozen model, parameters, policies, uncertainty and limits.
- [LITERATURE.md](LITERATURE.md): primary-source rationale without borrowed timing constants.
- [DATA.md](DATA.md): exact provenance, selected IDs and data layers.
- [EXAMPLES.md](EXAMPLES.md): first qualifying positive, tied and adverse runs,
  with original questions/drafts and simulated outcomes. The first favorable
  example has zero orientation cost and does **not** establish a context-reuse gain.
- `artifacts/oversight_simulation/design.json`, `inputs.json`, `freeze.json`:
  committed declaration and public inputs. `inputs.json` retains original call IDs.
- `results.jsonl.gz`: all planned outcome rows, including unfinished work.
- `traces.jsonl.gz`: complete compact command streams, phase times, simulated
  decisions and final logical-state hashes. Source payloads expand from `inputs.json`.
- `analysis/cell_means.csv`, `paired_differences.csv`, `paired_seed_blocks.csv.gz`:
  reproducible numerical evidence, without pooling parameter cells into a claim
  about a human population.
- `figures/`: PDF, SVG and PNG; `captions.json` identifies simulated quantities.
- `paper/oversight_simulation/main.pdf`: separate illustrated computational note.

Each parameter setting uses 32 paired random seeds and three reused packet
rotations. These are not 96 people or 96 independent reports. Reported intervals
measure numerical Monte Carlo uncertainty conditional on the fixed assumptions.

## Regenerate the CPU simulation, separately

The historical `run.py` retains its original stage cutoff and refusal to overwrite
results. A reproduction adapter reuses the **same frozen model and design** while
writing to a new directory with its own CPU deadline:

```bash
python3 -m research.oversight_simulation.regenerate \
  --out /tmp/oversight-simulation-reproduction --max-minutes 30
```

The destination must not exist. A smaller integrity check can use
`--config 000_o0_ideal_short --seed 10000 --rotation 0`; this is a reproduction
subset, not an additional evaluation. Neither path modifies historical accounting.
Compare decoded result/trace objects, since gzip headers and runtime measurements
may differ. No model inference, GPU service or participant collection is involved.

The existing human interface is intentionally unchanged. The next evidence needed
to validate this computational claim concerns actual source familiarity, navigation,
verification and construction performance; these were not measured here.
