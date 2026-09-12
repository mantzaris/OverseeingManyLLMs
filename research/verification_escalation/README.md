# Verification-guided escalation

A runnable local controller, frozen SQL experiment and separate research note.
It recovers scoped instructions, compares executable interpretations, shows why a
question matters and keeps unaffected goals moving. **The experiment does not
support automatic question suppression from generated-candidate agreement.**

Read [REPORT.md](REPORT.md) for the completed findings, [VERIFICATION_BOUNDARY.md](VERIFICATION_BOUNDARY.md)
for the exact guarantees and limits, [LITERATURE.md](LITERATURE.md) and
[NOVELTY.md](NOVELTY.md) for the research comparison, and [DATA.md](DATA.md) for
provenance. [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) maps claims to exact outputs.
The current principal study is the ordering-correct disjoint follow-up
under `artifacts/verification_escalation/repair/`. The initial 48-database run is
preserved as a flawed-adapter diagnostic. Neither is pooled with historical studies.

## One-command saved-output reproduction

From the repository root, with Python 3.8+ and the existing analysis dependencies:

```bash
python3 -m pip install -r requirements-analysis.txt
python3 -m research.verification_escalation.reproduce --output /tmp/verification-replay
```

Use a new empty output directory. The command checks both committed freezes,
downloads/checks the original public AMBROSIA archive if absent, reconstructs the
excluded source records, replays all 17,880 final/initial/synthetic rows and 144 post hoc direct-reader rows, plus the uniform-integrity-quarantine sensitivity and their
events, verifies primary and secondary tables, and regenerates eight principal
PDF/SVG/PNG figures. It makes **zero model calls**. It checks semantic outcomes and
logs rather than claiming byte-identical timing or plot metadata. Original measured
CPU latency is retained in the reproduced analysis instead of replacing it with a
new benchmark. The author's public download password is published on their website;
no personal account or newly provisioned service is needed.

Source archive SHA-256:
`a77f9cdb1f60bea69445fccc1f9f8f61146efe2ac2627f1b9e725855fac1242e`.
Full source inputs and raw envelopes are intentionally excluded from Git at the
authors' no-dataset-upload request. Generated SQL, source hashes, raw-attempt
accounting and deterministic replay inputs are committed. See DATA.md for this
publication-redaction provenance. Do not mistake the committed prepared JSON for
unredacted raw model envelopes; those remain in the original local `raw/` directory.

To regenerate only the principal figures from already saved tables:

```bash
python3 -c "from research.verification_escalation.common import ART; from research.verification_escalation.plot import run; run(ART/'repair')"
python3 -m research.verification_escalation.example_analysis
bash paper/verification_escalation/build.sh
```

The separate 14-page methods/results draft is `paper/verification_escalation/main.pdf`.
Its exact page count and build checks are recorded alongside it. Existing submission
sources remain intact.

## Demonstration

```bash
python3 -m research.verification_escalation.prototype.server --port 9032
# Open http://127.0.0.1:9032
```

1. The eligible-customer count and inventory are ready. The two registered eligibility
   rules happen to give the same count, but different customer IDs. No answer has
   been spent. These are authored demonstration data and stipulated interpretations.
2. Choose **Check what needs me**. Inspect the ID difference and Atlas scope.
3. Answer using spending or order count. Atlas work follows that answer. The partner
   request remains unresolved because its scope is different.
4. **Reconsider this definition** identifies the Atlas results needing revalidation,
   leaving unrelated inventory and partner work untouched. Spent budget is retained.
5. **Simulate new data** invalidates the prior snapshot results. The count can now
   depend on the unresolved interpretation. An unchanged certificate is not reused.
6. Restart and select **Apply only to this request**. A value plus a new scope
   restriction costs two units. Leaving a question unresolved consumes one response
   unit and does not count as completion.

Use Ctrl-C to stop this local server. The demo starts no GPU service or external
application action. [API.md](API.md) documents a Python client and controller input
boundary. `ValidatedController` adds source-integrity checks to the version-aware `OnlineController` wrapper; the frozen
`Controller` remains available for historical experimental replay.

Recorded screenshots, 14 browser checks and 18 displayed interactions are under
`artifacts/verification_escalation/interface/final/`. Replay them with:

```bash
python3 -m research.verification_escalation.replay_interface
```

The browser script requires Node 22 and Chrome, used only for optional UI testing:

```bash
node research/verification_escalation/prototype/browser_smoke.mjs /tmp/verification-ui-check
```

These logs and response times are scripted development evidence, not participant data.

## Focused verification

```bash
python3 -m unittest research.verification_escalation.test_protocol research.verification_escalation.test_ordering research.verification_escalation.test_online research.verification_escalation.test_boundaries research.verification_escalation.test_integrity -v
python3 -m research.verification_escalation.validate_results
```

The 34 focused tests cover information isolation, pathwise budgets, source provenance,
revocation, scope exceptions, shared-answer accounting, omission counterexamples,
query comparison and stale results. The 27 relevant historical clarification tests
were also run without fresh inference. All old experimental code and artifacts
remain unchanged.

## Fresh GPU regeneration is different

Historical commands and deadlines remain enforced. The completed authorization is
`artifacts/verification_escalation/authorization.json`, with 592 of 600 scheduled
calls used and an inference cutoff of 2026-09-12 01:23:26 UTC. The collection commands
were:

```bash
python3 -m research.verification_escalation.collect evaluation
python3 -m research.verification_escalation.repair_collect evaluation
python3 -m research.verification_escalation.direct_reader collect  # separately declared post hoc audit
```

They used an already authenticated SSH tunnel to the existing Qwen BF16 server and
recorded all attempt intents before requests. Cached calls do not create new model
outputs. A genuinely fresh replication needs its own authorized ledger, cutoff,
artifact namespace and verified GPU endpoint; do not edit the completed clock or
present a cache replay as fresh generation. No credentials or SSH private keys are
included in this package.
