# Source provenance and partition boundary

This stage reuses the official TAT-QA release pinned at `870accc41953dcde885aabeb963d94aabdc0fbc3`, from https://github.com/NExTplusplus/tat-qa. `provenance.json` retains the exact raw-file and evaluator hashes from the preceding official-source audit; `data.py` rechecks them. Dataset attribution is CC BY 4.0; upstream evaluator code is MIT. Zhu et al., ACL-IJCNLP 2021, DOI https://doi.org/10.18653/v1/2021.acl-long.254.

Real source material: financial-report tables and paragraphs. Benchmark material: original human-written questions and answer/scale/derivation annotations. Constructed material: assignment of questions to agents, fixed inspection episodes, two-unit inspection budget and the correction protocol. Generated material: interpretations, source bindings and repairs. Supervision: ideal question-specific annotation disclosure. No human oversight observations are collected.

The twelve training contexts already used by adaptive-correction-transfer are development-only, including their saved v4 initial answers. The reproducible historical error audit reuses prior evaluation outputs and is also development evidence. It does not create a fresh held-out sample.

`source_pool_audit.json` records used-context IDs, source-manifest hashes, table duplicate exclusions and exact repeated paragraphs of at least 160 normalized characters. All released train/dev/test_gold records are checked for exact table duplication in split order. Candidate eligibility is four to eight original questions and at most 3600 rendered source characters. Availability does not imply commitment to an evaluation: the development gate must pass first.

Raw release records supply context/table and paragraph identifiers, but not reliable report identifiers. Context-level pairing is therefore weaker than independent-report inference; related material from the same report may remain after exact duplicate checks. Public test-gold labels are legitimately released, but public-benchmark pretraining contamination cannot be excluded.

The public projection retains original table values and question wording. Rendering assigns T-row/C-column identifiers and replaces a literal vertical bar with a slash only for Markdown layout, as in the historical adapter. Source hashes use the original content. The patch mechanism never modifies source cells. An executable expression is a generated interpretation, not a gold program. Unsupported text/complex arithmetic remains in full-sample accounting.

Official answer EM/F1, exact scale and joint correctness are separate. The established scorer can credit a readable answer even when auxiliary representation fields are invalid. Representation validity and contract coverage are reported independently, avoiding the preceding stage's overbroad malformed-output wording.
