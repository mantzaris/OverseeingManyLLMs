# Answer quality and task feasibility

This is an offline developer audit, not independent human adjudication. All original
290 answers, raw responses, annotations and frozen scores remain unchanged. The
pilot uses the same saved model generation, with a separate uniform display
projection. No new inference was needed or used.

## Raw response to display to score

`audit.py` compares every initial raw JSON response with the historical `prepare`
output, pilot projection and official scorer. Original evidence is under
`artifacts/oversight_workflow/{raw,prepared}/`; audit rows, exact affected call IDs
and full inspected cases are under `artifacts/oversight_workflow/pilot_preparation/`.
The pilot server imports neither the offline scorer nor these audit files.

| Cause of the 38 historically empty answers | Count | Pilot treatment |
|---|---:|---|
| Model omitted the answer field (`{}`) | 6 | Retain missing answer |
| Model explicitly supplied `answer: []` | 24 | Retain empty answer and any generated explanation |
| Model supplied nested answer arrays rejected by the flat-list parser | 7 | Flatten primitive leaves without joining words, changing numbers or inventing spans |
| Cell-reference calculator expression unsupported by the declared numeric-only interface | 1 | Retain unsupported answer; original source remains available |

All raw responses were parseable JSON. The four rows above exhaust the 38 old empty cases; the seven parser cases are
already included in that total. Of the 24 explicit
empty arrays, some explanations contain potentially useful answer material, while
others assert unavailable information or contain wrong numbers. For example, an
empty loan answer's explanation uses 267 where the inspected reference uses 88.
We do not automatically promote explanatory text to an answer. An explanation is
fallible model content, not a verified repair.

A complete content pass over the 24 explicit-empty cases found eight with
answer-bearing text outside the answer field, four with partial/qualified answer
text, one with only a source pointer, four with no substantive answer text, two
with a wrong number in the explanation, and five claiming unavailable details that
the supplied source actually provides. These are developer/source assessments,
not adjudicated scores or measured draft usefulness. `empty_content_audit.json`
records each case. One raw response puts its quoted answer in an evidence string;
the new expandable **original model response (version 1)** view preserves that
text, even when the normalized citation list cannot. It is identical in B/C and
absent in source-only. The main answer field stays empty. Thus an empty scored
answer does not always mean that the model supplied no potentially useful help.

The seven nested-array cases contain readable components that the historical
interface lost. `adapter.py` fixes this **only in the new pilot path** and preserves
the original answer lists and scores in the audit. Flattening does not infer how
word tokens should be joined into spans. A separate optional citation repair
extracts literal `T#C#` and `P#` identifiers from evidence strings before the existing
validator checks them. It neither certifies relevance nor changes the answer.

| Measure | Frozen original | Separate pilot display projection |
|---|---:|---:|
| Exact-match answer correctness | 61/290 (21.0%) | 61/290 (21.0%) |
| Joint answer and scale correctness | 59/290 (20.3%) | 59/290 (20.3%) |
| Empty/unsupported answer lists | 38/290 (13.1%) | 31/290 (10.7%) |
| Mean token F1 | 22.6% | 23.6% |

157 answers had the optional evidence-shape flag. **32 of these were jointly
correct.** Citation formatting is not an answer-correctness label. The pilot
uniformly separates answer availability, generated explanation, citations and
scale. Full source inspection never depends on citation compliance.

## Bounded nonempty inspection

The reproducible rule is replica 0, separately within each benchmark answer type
and joint-correct/error stratum, taking the first three distinct contexts ordered
by SHA-256 of the question ID. This yields 22 nonempty cases: 10 correct controls
and 12 scored errors. It is a stratified diagnostic sample, not a representative
estimate of the composition of all errors. Full question/source/raw/annotation
records are in `bounded_nonempty_audit.json`; `qualitative_audit.json` records the
case-specific assessment, including unresolved interpretations.

Among these 12 errors, five have clear answer/content problems (three counts,
one magnitude calculation and one wrong answer type), and four have clear unit
problems (units applied to years, an unsupported ARPU scale, and million changed
to billion). Three require caution about interpretation or scoring:

- Bell Media's 2018/2019 capital expenditures: the model lists 114 and 108 million;
  the annotation sums them to 222. The original wording can invite separate yearly
  values. Do not adjudicate the list as correct automatically.
- Off-net ARPU change: the model gives -6.8%, which the source table itself prints;
  the annotation gives -6.78%. This is a credible precision disagreement.
- Net earnings of 157,133: the model adds `thousand`, whereas the reference scale is
  blank. Financial table context makes the unit interpretation worth independent
  review. Exact answer/scale records are retained.

The ten controls show that the material also includes correctly answered lookups,
counts and calculations. We did not turn the three disputed cases into successes.
Their presence motivates **additional blinded adjudication**, not replacement of
the official score. No automated semantic judge was used.

## Are these useful drafts?

The parser correction does not explain the low exact-match accuracy. Most scored
errors cannot be attributed to the optional citation flag. The sample contains
substantive numerical and unit errors as well as some potentially acceptable
wording/precision disagreements. It cannot quantify those proportions over all
229 non-matches. Model explanations can aid a review, but also require checking.
Participants are likely to reconstruct a substantial fraction of answers rather
than make a quick approve/reject judgment. That is a task-feasibility concern, not
a demonstrated human effect.

The publicly selected pilot packets retain these limitations:

| Packet | Original questions | Pilot exact/joint correct drafts | Missing drafts |
|---|---:|---:|---:|
| 0 | 12 | 1 | 0 |
| 1 | 12 | 2 | 3 |
| 2 | 12 | 4 | 2 |

These counts were calculated **after** the final public-characteristic selection.
An earlier preparation selection was revised because it repeated an EPS definition
across distinct sources, then rematched on public complexity. The old packet scores
and dry runs are retained. No packet was changed in response to model correctness
or participant outcomes. One source-only question refers to pension obligation information
while its supplied table emphasizes asset allocation. Such wording/source
mismatches may make a task ambiguous. Retain the original question and allow
rejection/deferral; record it for blinded source-based adjudication. The task
packets are suitable for a small **feasibility and usability pilot**, not yet a
validated instrument for proving interface effectiveness. The source-only block
will help establish whether available drafts offer useful assistance or mainly
add reconstruction work. It uses different contexts and balanced block order,
so it does not rely on remembered answers, but remains a small diagnostic.
