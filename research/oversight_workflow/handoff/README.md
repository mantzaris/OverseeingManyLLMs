# Author handoff: the review workflow and formative pilot

The active manuscript is [the position-paper draft](../../../paper/oversight_workflow/main.pdf)
([source](../../../paper/oversight_workflow/main.tex)). This handoff consolidates
the paper and investigator instructions. It does not change the desk, packets,
model outputs, questionnaires or analysis algorithm. There are **no participant
results**. Zero inference is used.

Start with [WALKTHROUGH.md](WALKTHROUGH.md) for a 10–15 minute investigator practice,
then [FEEDBACK.md](FEEDBACK.md). [REVIEWER_MEMO.md](REVIEWER_MEMO.md) gives the three
strongest objections. [CLAIMS.md](CLAIMS.md) separates evidence from hypotheses.
[REPORT.md](REPORT.md) records the completed handoff and remaining decisions.

## Preview and exports

From the repository root:

```bash
python3 -m research.oversight_workflow.pilot.server --port 9042
```

Open **http://127.0.0.1:9042** on this Ubuntu workstation. The handoff leaves this
loopback-only preview running; do not launch a second copy on the same port.
Its process, command, log and stop instruction are in
`artifacts/oversight_workflow/author_handoff/preview.json`. No forwarding is needed
on this workstation. The preview is not publicly deployed. A browser on another
computer must not use its own localhost address to reach this process.

The default is **investigator_practice**, with local autosaved exports under
`/tmp/oversight-pilot-practice`. Download the identified `.pilot.json` package using
the setup shell's **Download identified session package** button after a block.
Preserve practice files privately outside `/tmp` if they are to survive cleanup;
do not commit personal notes. End a block before exporting its final state.
Incomplete runs remain incomplete. No reference answers are shown.

Analyze only actual saved practice after someone has tried it:

```bash
python3 -m research.oversight_workflow.pilot.analysis /tmp/oversight-pilot-practice \
  --kind investigator_practice --out /tmp/oversight-practice-analysis
```

Later, after the investigator has the required authorization, analyze genuine
exports separately:

```bash
python3 -m research.oversight_workflow.pilot.analysis /private/path/pilot-records \
  --out /private/path/pilot-analysis
```

The default refuses practice and software fixtures. These are verified commands,
not authorization to collect. Official scores, extra blinded adjudication and
missing work remain separate; see [the existing analysis instructions](../pilot/ANALYSIS.md).
Do not interpret practice figures as participant findings.

## Frozen version and light verification

Runtime and study design remain **formative-v1**, code commit
`370c366ad57605b687ab932e72895b251535819c` (implementation `b8a4af45`). The manifest digest is
`a834086c089d53d5903db6f4e5394ff53f089eccf4a0edf06ff68b73e8d8eaba`.
The separate handoff freeze records exact file hashes, including the original
preparation freeze; it does not replace that declaration.

```bash
python3 -m research.oversight_workflow.handoff.verify
bash paper/oversight_workflow/build.sh
```

The first command checks frozen code and pilot material without inference or a
scenario sweep. The second compiles the active manuscript from saved numerical
inputs. The original full software-reproduction commands remain available in the
parent package but are not required for this handoff. No new score table is created
by rebuilding the paper.

The next evidence should come from real interaction: first investigator practice,
then an authorized formative collection. The historical scripts establish
protocol behavior, not review efficiency or workload reduction.
