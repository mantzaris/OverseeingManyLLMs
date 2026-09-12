# Alex's 10–15 minute investigator walkthrough

**Investigator practice only.** This is a route through the existing application,
not a comparison, participant session or test of Alex. Use your own judgments;
there is no answer key in this walkthrough. Do not try to finish every question.
The example deliberately includes missing drafts and difficult unit/percentage
checks. It must reveal task difficulty, not conceal it.

## 0–1 minute: open the preview

Open http://127.0.0.1:9042 on the Ubuntu workstation. If it is not running, use:

```bash
python3 -m research.oversight_workflow.pilot.server --port 9042
```

Confirm **INVESTIGATOR PRACTICE**, choose a fresh pseudonymous practice code and
**assignment 7**. It offers C / packet 1, then B / packet 2, then source-only /
packet 0, after separate-source training. Click **Create run** and **Start block**.
A full study run is longer; this short walkthrough stops after training and the
first C block. Later blocks stay explicitly unperformed. No timing configuration
is changed.

## 1–4 minutes: learn review and exact-version release

Training uses the original actuarial-assumptions table, with 2019/2018/2017 columns.
Open a question from the pending list. Inspect the actual model draft and **Original
source evidence**. Read the period and units. Open **Inspect original model response
(version 1)** if useful, remembering that its explanation is generated.

Keep this first review open while the second request arrives after 1.5 seconds.
The pending display should change; your source, draft and controls should stay put.
If both training questions arrived before you opened one, observe this during the
C block instead; do not restart merely to produce the expected scene.
Use **Calculator** for a check if needed. It performs arithmetic, not source
interpretation.

Select the question **“How much is the 2019 rate of inflation?”** when ready.
Locate its evidence yourself. If the draft is acceptable, use **Approve this
version**; otherwise enter a checked answer/scale in **Supply your own correction** and
use **Correct and approve**. Observe that approval alone does not release it.
In the approved-work area, use **Release this version** for that exact request/version.
A correction produces a new user version; sibling questions receive no approval.
If you cannot justify an answer, defer it rather than release for demonstration.

End training early if ready, or let its four-minute timer end. Leave optional form
items blank or answer from your actual practice experience. Click **Save form,
including any unanswered items**, then start the C block.

## 4–6 minutes: inspect a missing draft and preserve partial work

The first C request is **“How are Provisions for post-employment benefits plans
recognised?”** from source `832f8af1730c8f79e9d70fc20c3e9ed5` (question ID
`7cb0ad318722820690b52bfdac79a1c0`). Its saved answer field is empty. The full
source and original response remain available. This is a retained actual output,
not an inserted error. Decide whether the draft offers any help or whether you
must reconstruct the answer from the paragraphs.

Open **Supply your own correction**, enter a partial draft or note in your own words,
and select a scale if appropriate. Do not approve an unfinished correction.
Use **Defer and keep my place** (the reminder is 30 seconds). Open another request; then select the deferred request
from the pending list, directly or after its return time. Check that the source,
note, partial answer and scale return. Deferral is retained unfinished work.

Incoming questions alternate this source with a Bell capital-expenditure table.
Keep a review open across an arrival. Compare what changed in the pending display
with what stayed fixed in the active pane.

## 6–10 minutes: related questions and admission control

With a post-employment question active, use **Keep up to three related requests
together**. The other questions ask about the basis and types of those benefits.
They share a source, not an answer. Finish or defer the current review, then use
**Next** or the pending list to inspect another. The “Review separately next” card
keeps that question in the session; it does not approve it or replace the current
review. Check that every answer retains its own decision.

Before the C block reaches **3:00 elapsed** (6:00 remaining), select **Pause new
tasks**. If already past that point, note that fewer tasks may remain to pause;
do not restart the run to manufacture a backlog. Inspect **Offered tasks**, **Not
started**, **Requests received** and unfinished/deferred work. Pause holds new
starts, not in-flight work. At the scheduled second wave, some work should remain
not started. Resume after a short inspection and observe the new requests arrive.
The timer continues during a pause.

If time permits, inspect the original question about Bell Media's 2018 and 2019
capital expenditures. Its actual proposal lists two yearly values. Check the
wording and evidence; do not assume that a plausible-looking number or the model's
scale settles what the question asks. Keep uncertainty visible by noting or
deferring it. No hidden scoring judgment is supplied here.

## 10–15 minutes: release, preserve unfinished work and export

If you have a checked answer, approve/correct and then release its displayed
version separately. Verify that this does not release other source-session items.
If a newer version warning ever appears, explicitly refresh and review before
approval; the frozen pilot does not inject agent revisions, so a natural warning
is not required for this practice. The user's correction already exercises a new
version. Existing software fixtures cover stale-approval races.

Use **End block early** after roughly six to eight minutes in C, or let its
nine-minute timer expire. All offered questions remain recorded, even if not
started or released. Save the form with missing items preserved. Use **Download
identified session package**. To leave this abbreviated practice cleanly closed,
choose **Withdraw and preserve work** rather than starting B/S, and download the
final package again. Keep the final export; earlier snapshots are partial exports,
not additional observations. This practice is intentionally incomplete and is not
eligible for a B/C effectiveness comparison.

Fill [FEEDBACK.md](FEEDBACK.md) from what you actually observed. Optionally analyze
the practice export using the command in [README.md](README.md). Alex can later
try a complete practice run, but should not be counted as a new independent
participant or reuse these learned answers in a purported fresh scored comparison.
