# Decision desk: reusable answers and changed instructions

This research prototype lets a user answer a travel-planning question for one
request or an explicit shared scope, see which agent drafts depend on it, and
identify work needing revalidation after an instruction changes. It uses saved
Qwen outputs and local MultiWOZ data. It performs no bookings or external actions.

The completed ICAART submission and previous experiments are unchanged. This is
work on `research/decision-dependencies`, following baseline `3f843bee`, with a
separately authorized three-hour session. Nothing is pushed.

The pilot found no whole-project quality advantage over semantic memory and more
additional questions. The simple global version check matched selective checking.
Keep the explicit scope/change controls and simplify the automatic backend;
the [report](REPORT.md) retains the failures and explains this recommendation.

## Try it

From the repository root, Python's standard library is enough for the interface:

```bash
python3 research/decision_dependencies/prototype/server.py --port 9027
```

Open `http://127.0.0.1:9027`. Follow [the walkthrough and adapter API](API.md).
Stop the server with Ctrl-C. The demonstration includes a real saved extraction
failure, an answer reused by two roles, an actual source preference change and a
separately authored exception. It is not a participant study.

## Reproduce saved results without inference

Use Python 3.8 or later with NumPy and Matplotlib. The verified host used Python
3.8.10, NumPy 1.22.1 and Matplotlib 3.1.2. This command writes to a separate output
directory and checks exact trace, episode-table and analysis-table replay:

```bash
python3 -m research.decision_dependencies.reproduce --figures
```

The default destination is `/tmp/decision-dependencies-replay`. No model endpoint,
GPU, download, credentials or new generation is needed. Vector PDF/SVG and 300 dpi
PNG figures regenerate from saved results. PDF metadata, SVG internal identifiers
and font rendering need not be byte-identical across installations; the numerical
tables and canonical replay traces are checked separately.
The same command also reconstructs every final/dev preparation from raw calls,
checks exact prompt/seed/settings correspondence, replays the authored challenges,
and regenerates the separately labeled post hoc diagnosis and five report figures.

Focused tests and a browser demonstration are available:

```bash
python3 -m unittest research.decision_dependencies.test_decisions research.decision_dependencies.test_interface research.decision_dependencies.test_package -v
# With the local server running; requires Chrome and Node 22:
node research/decision_dependencies/prototype/browser_smoke.mjs
```

## Research package

- [Report](REPORT.md): measured findings, failures and recommendation.
- [Standalone report PDF](REPORT.pdf), built with
  `python3 -m research.decision_dependencies.build_report` (Pandoc and LaTeX).
- [Literature](LITERATURE.md), [novelty assessment](NOVELTY.md) and
  [decision log](DECISIONS.md): competing mechanisms and adaptation history.
- [Formal method](METHOD.md), [initial plan](PLAN.md), [future interaction study](HUMAN_STUDY.md).
- `artifacts/decision_dependencies/frozen/`: committed protocol, source snapshot,
  source IDs, model settings, challenge cases and hashes.
- `artifacts/decision_dependencies/data/`: public dialogue excerpts, separate
  evaluator states, local databases, source audit and upstream MIT license.
- `artifacts/decision_dependencies/raw/` and `prepared/`: every model request,
  response and attempt, plus shared parsed preparations.
- `artifacts/decision_dependencies/evaluation/`: all paired controller traces,
  episode CSV, diagnostic tables and figures.
- `artifacts/decision_dependencies/interface/`: browser checks, screenshots and
  explicitly scripted interaction logs.
- `artifacts/decision_dependencies/resource_ledger.json`: this session and
  cumulative accounting without resetting historical clocks.

## Source reconstruction and fresh generation

The selected dialogue excerpts and small local databases are included under the
upstream MIT license. Full third-party papers and the full dialogue archive are
outside Git. `data_provenance.json` records exact download URLs and checksums.
To download the pinned archive, verify its checksum, rebuild selection and check
the exact selected source bytes in a separate directory:

```bash
python3 -m research.decision_dependencies.rebuild_source --output /tmp/decision-source-rebuild
```

The archive SHA-256 is
`d4c66523614af016c1d2dafa35b4a548c96cb9ffadb71338937b60ac51272fe5`.
This optional source audit downloads data, but performs no inference and preserves
the original evidence. Ordinary saved-output reproduction needs no downloads.

Fresh generation is a different operation from replay. The historical commands
were `python3 -m research.decision_dependencies.collect --split evaluation
--replicates 2` and `python3 -m research.decision_dependencies.challenges collect`,
using the existing authenticated SSH tunnel to port 8017. The saved authorization
expires at its recorded cutoff; these commands cannot silently reset it. They
return existing cached calls unchanged. New generations require a newly
authorized artifact namespace and deadline, not deleting old failed calls or
changing the existing authorization file.

The fixed model was Qwen/Qwen2.5-7B-Instruct at revision
`a09a35458c702b33eeacc393d103063234e8bc28`, BF16 on the RTX 6000 Ada, zero CPU
offloading, temperature 0.3 and top-p 1.0. JSON object output formatting is a
separately recorded setting for this application. The historical server and all
previous decoding configurations remain intact.
