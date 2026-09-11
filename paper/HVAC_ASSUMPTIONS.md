# Measured HVAC evidence and constructed oversight

This is a source-based methodological assessment, not independent human expert
validation. The source inventory and article are linked in the provenance manifest.

| Assumption | Implementation and evidence | Interpretation limit |
|---|---|---|
| Measured inputs | Physical FLEXLAB SZCAV/SZVAV records, 1-minute sampling | Controlled lab apparatus with manually imposed faults, not occupied-building incident data |
| Correct diagnosis | Four component categories mapped from inventory date labels and cross-checked against binary fault flags | Coarse category scoring; a day-level imposed fault may not be observably excited within every selected window. Not severity estimation, unique causal identification or proof of repair success |
| Public evidence | Ten sensor/control channels summarized within fixed windows, with units and time of day | Summaries lose temporal structure; command signals need not equal physical positions; the 7B model sometimes misinterprets numbers |
| Conventional baseline | Development-only standardized nearest-centroid classifier on the same evidence | Simple, untuned comparator; both methods miss all evaluation cooling cases |
| Source split | Whole experimental days, first per mode/category for development | Same equipment and season/control confounding persist; 18 day blocks are not independent buildings |
| Ticket interpretation | Three retrospective diagnostic judgments from one day's windows, all available after 14:59 | Constructed concurrent backlog, not three separate machines or observed arrival rates |
| Review | Same pinned model, separate prompt, proposal plus permitted evidence | Correlated model errors; not measured human inspection; one saved response per proposal |
| Review authority | Completed review can replace a diagnostic label or abstain; failed response preserves proposal | It changes a diagnosis record only, not actual equipment or the recorded trace |
| Ideal reference | Correct label returned at completed review only | Upper bound on reviewer effectiveness, not a realistic technician measurement or clairvoyant scheduler |
| Benefit estimation | Development signed corrections-minus-harms with sparse-bin pooled fallback | Small calibration set and coarse bins; nonpositive learned gains mechanically decline review |
| Service and capacity | One/two slots, service one/two/three abstract ticks | Assumed workflow conditions; no conversion from GPU latency to human service time |
| Cutoff and loss | Independently shuffled 2/4/6 cutoffs and 4/8/12 error weights, uniform-eight sensitivity | Dimensionless scenario costs, not observed energy cost, damage risk or business deadlines |
| Pairing | All policies and timing/weight conditions share saved proposal/review pairs | Isolates scheduling on fixed judgments; does not measure feedback-dependent adaptation |

The existing synthetic ventilation clues are not measured HVAC data. Adapted
tau-bench records are simulated despite executable workflows and genuine model
outputs. The measured study supplies external observations and experiment labels,
while the scheduling dynamics remain an explicitly constructed application.

SQL was not evaluated. Critic's required reference/test fields need an email
request, and a valid BIRD-SQL fallback could not fit the remaining original budget.
The practical extension therefore claims one completed measured application only.
