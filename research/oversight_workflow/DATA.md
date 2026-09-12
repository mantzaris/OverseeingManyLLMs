# Data, provenance and construction

## Source and reuse audit

The application uses TAT-QA, introduced by Zhu et al. at ACL-IJCNLP 2021:
[paper](https://aclanthology.org/2021.acl-long.254/),
[author repository](https://github.com/NExTplusplus/tat-qa),
[dataset site](https://nextplusplus.github.io/TAT-QA/).
The pinned release is commit `870accc41953dcde885aabeb963d94aabdc0fbc3`.
The official repository supplies financial-report tables/text, human-written
questions, annotations and the scorer. Dataset attribution is CC BY 4.0; repository
code is MIT. `artifacts/oversight_workflow/provenance.json` preserves release-file
SHA-256 values and the existing scorer's relative-import-only modification.
No external financial records are invented or edited here.

The prior correction-applicability audit covered all 2,201 train, 278 development
and 277 public test-gold contexts. Historical TAT-QA use consists of 12 development
and 24 evaluation contexts; the later correction-applicability stage reused those
and did not run fresh evaluation. This stage excludes all 36 IDs, their normalized
tables, matching normalized paragraphs at least 160 characters long, and source
exact duplicates detected across the upstream splits. The audit had identified
223 unused technically eligible test contexts.

We selected the first 24 in original source order, also excluding duplicate tables
or long paragraphs among the selected contexts. Eligibility retains all original
questions, requires four to eight questions per source and source rendering no
longer than 3,600 characters for the existing 2,048-token server. The selection is
frozen in `selection.json` and `frozen/manifest.json` before held-out generation.
There are 145 original questions, because one selected context has seven questions.
Two generation replicas give 290 initial answers. The source length/count filter
limits generality to this compatible subset, but was not selected using outcomes.

Source tables and paragraph wording are preserved in the public manifest. Prompt
formatting adds cell/paragraph identifiers, renders rows as text, and replaces a
literal pipe inside a cell with a slash only in that text rendering. The browser
uses original cell strings. The short answer interface requests a readable answer,
scale and optional explanation/evidence. It does not require a computation graph.
The existing bounded calculator can evaluate an expression chosen by the model;
it does not choose operands or insert a reference answer.

TAT-QA's public test-gold release contains labels, so this is a fresh partition
relative to our development, not a hidden benchmark test or evidence of absence
from model pretraining. Public source projections omit reference answers,
annotated derivations and gold evidence fields. Labels are loaded only for offline
scoring or the explicitly labeled scripted question-specific inspection.

## Evidence hierarchy

| Component | Provenance and interpretation |
|---|---|
| Financial values and source paragraphs | Real financial-report material represented in the benchmark, not live transactions or measured analyst behavior. |
| Original questions and answers | Human-written benchmark questions and reference annotations; all original questions retained. |
| Initial answers | 290 actual independently prompted Qwen GPU outputs, with raw request/response records. |
| Revisions | Four actual source-rechecking model continuations selected before collection; their timing in replay is constructed. |
| Workers and source bundles | Three labeled task workers and twelve two-context workload bundles are constructed assignments. Shared source identity does not imply answer sharing or a causal dependency. |
| Live arrivals | Observed generation/delivery wall times from the first two contexts. GPU work is serialized; task worker/queue activity is asynchronous. |
| Comparative arrivals | Declared wall-clock eligible-start schedules, lower versus higher concentration, with saved identical answers. Admission pause may delay actual arrivals. |
| Scripted reviewer | Ideal benchmark-based question-specific approval/correction after an assumed 95 ms action interval. This is a software stress input, not human reading time. |
| Browser actions and stress revisions | Automated Chromium actions; metadata-only revisions are authored protocol fixtures and are kept separate from the financial-answer collection. |
| Human effectiveness | Unmeasured. The study protocol and packets are prospective materials. |

## Dependence and units

There are 24 fresh source contexts, grouped into 12 paired two-context software
workloads. We cannot reliably recover complete report identities from this release.
Exact duplicate screening does not establish independent companies or reports.
Questions within a source, generation replicas, conditions and replay events are
not independent source samples. Bundle-level resampling averages the two replicas
first and keeps compared conditions matched. Its intervals describe the constructed
software scenarios, not a population of people or operational financial deadlines.

## Scoring and retained outcomes

We reuse the official normalized exact match and token F1 implementation. Joint
correctness additionally requires the annotated scale. Structural parse validity
and empty/unfinished outputs are reported separately. Textual exact match may miss
semantically adequate spans; no outcome is manually rescued for the principal
software evaluation. The ideal script corrects only at a recorded review action.
A correction is recorded as a user-authored version rather than attributed to the
model. All offered questions, failed outputs and unfinished reviews remain counted.

## Getting the source

Raw full-release files remain outside Git under the historical source-cache path.
To restore the pinned source for fresh collection or private rescoring:

```bash
git clone https://github.com/NExTplusplus/tat-qa /tmp/adaptive-transfer-sources/tat-qa
git -C /tmp/adaptive-transfer-sources/tat-qa checkout 870accc41953dcde885aabeb963d94aabdc0fbc3
```

The compact selected public contexts, generated answers and disclosed-script traces
are tracked with provenance. Saved-output reproduction uses the compact stage-local
evaluation annotation projection produced after collection; it is never imported
by the online desk. Its provenance hashes are checked against the pinned release.
