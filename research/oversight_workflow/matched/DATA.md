# Reused real-data tasks and display projection

The source is the existing pinned TAT-QA release and its original financial-report
tables, paragraphs and human-written questions. See `../DATA.md`, `../pilot/AUDIT.md`
and the source provenance linked there. No new download, question rewriting,
model call, artificial error or outcome-based exclusion occurs in this stage.

| Layer | Provenance and role |
|---|---|
| Financial values and text | Real report material represented in benchmark tables and paragraphs |
| Questions and reference annotations | Original human-written benchmark tasks/labels; labels offline only |
| Drafts | Actual saved Qwen outputs, replica 0, with exact original call identities |
| Display | The pilot's uniform parsing projection, including restored array answer displays |
| Worker roles, arrivals, nine-minute period | Constructed supervision application and study allocation |
| Software dry-run actions | Authored fixture inputs, never human observations |
| Participant answers, actions, ratings | Not yet collected for this comparison |

`manifest.json` names all sources/questions and hashes original raw responses and
displayed projections. The three twelve-question packets have 3,144-3,344 source
characters, 57-69 table cells and 6-7 arithmetic questions each under the existing
public-characteristic matching rule. They are approximately matched, not identical.
Each packet rotates across every condition and position. Residual task differences
must remain visible in analysis.

The selected replica contains 7/36 initially joint-correct drafts and five
empty/unsupported display fields. These known audit findings do **not** justify
excluding questions or selecting a different replica. Draft usefulness is an open
question directly tested by M. A person may need to reconstruct rather than edit
many answers. All 36 offered questions remain in each person's three-block plan.

Historical full collection: 24 source contexts, 145 questions, 290 generated
answers, **61/290 exact matches and 38 historical empty parsed outputs**. Pilot
projection restored seven answer displays and has **31 empty or unsupported
fields**; exact match remains **61/290**. Restoring display is not improving model
accuracy. The new manual block omits drafts by design; its 12 empty entry fields
are not additional model failures.

The six selected contexts were already inspected for prior pilot preparation.
Report identifiers do not establish six independent organizations or reports.
The study's paired units are people, with disjoint packets within person and
reused source contexts across people. The study does not test a multi-agent
architecture against a single model. Here agents are independently prompted task
workers whose saved outputs require individual review decisions.
