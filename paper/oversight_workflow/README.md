# Active ICAART workflow position paper

`main.tex` and `main.pdf` are the **one active workflow manuscript**, using the
unchanged official SCITEPRESS template. Other papers in this repository preserve
historical research. The current draft is eight pages and separates completed
software evaluation, completed formative-pilot preparation and an unperformed
human study. See [SUBMISSION.md](SUBMISSION.md) for current format verification
and remaining author/disclosure decisions.

Build from saved inputs, without inference or repeating the software matrix:

```bash
bash paper/oversight_workflow/build.sh
```

Numerical macros and the scripted result table remain the historical saved-output
products. Existing vector diagrams and an actual Chromium component capture are
reused. The live timeline and full figure set remain in the parent evidence
package; the main paper uses a compact subset. No paper figure depicts participant
results. The seven recovered answer displays leave exact match at 61/290.

The prepared study is [formative-v1](../../research/oversight_workflow/pilot/PROTOCOL.md):
two nine-minute B/C blocks, a separate four-minute source-only diagnostic, disjoint
packets and counterbalanced assignments. It is distinct from the earlier proposed
interface-by-load effectiveness study. No participant observations exist.

Use the [author handoff](../../research/oversight_workflow/handoff/README.md),
[claim-evidence table](../../research/oversight_workflow/handoff/CLAIMS.md) and
[internal reviewer memo](../../research/oversight_workflow/handoff/REVIEWER_MEMO.md)
for review, then the short investigator walkthrough. The complete original
software reproduction remains `bash research/oversight_workflow/reproduce.sh`;
it need not be rerun to build this manuscript or try the frozen pilot.
