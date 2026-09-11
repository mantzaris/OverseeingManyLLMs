# Source-linked decisions and consistent release of work

## Application and contribution being tested

A user is preparing a trip, rather than diagnosing specialized equipment. Their
hotel and restaurant preferences are information they can supply. Local agent
roles prepare lodging and dining shortlists, a categorical budget brief, an area
brief, an itinerary specification and accommodation requirements. These are
distinct derived artifacts of **one project**, not independent user goals.
There is no booking, purchase, real travel-price calculation or external action.

The prototype exposes a familiar mechanism in a useful place: before an agent
releases work based on a user's earlier instruction. Its research claim is an
evaluated interaction contract, not a new memory, cache or scheduling algorithm.

## Public information and decision records

At source epoch e, the system sees only the released conversation prefix, the
project identifier and natural-language requests. Qwen extracts candidate
`(domain, attribute, value, source turn, quote)` records and separately interprets
paraphrased requests. The same extraction and request interpretations are shared
across structured methods. No evaluator state, future utterance, hidden target or
correct scope label is sent to these calls.

A record stores the project, decision type, value, source, inferred/confirmed
status, version and explicit exceptions. The public project ID is trusted routing
context. Domain and attribute applicability are model predictions, not supplied
correct labels. The source guard checks supported fields, a real user turn and a
matching quotation. Explicit conditional phrases in that turn cause abstention
until scope is confirmed. This conservative rule can miss paraphrased conditions
and reject valid instructions. A real quote does not prove that the assigned value
or domain follows from it.

Conflicting records are unresolved. An inferred preference is visibly different
from an explicit user answer. A user can answer only the current request or
confirm a named project/domain/attribute scope. Exceptions are preserved. An
action-specific approval can apply only to that action's request identifier and
cannot be widened into a reusable preference or general authority.

## Work dependency and release semantics

Each prepared artifact records the decision versions it consumed. A user change
publishes a new source epoch. Changing or revoking a value, authority scope or
exception increments its version. A source quotation change alone does not change
an otherwise identical value. New source snapshots invalidate temporary answers
obtained from the simulated user in the previous epoch. This is conservative and
can add clarification; it does not assume how an unobserved conversation would
have continued after our inserted questions.

For artifact a with consumed version v(a,k), the selective release check requires
v(a,k) = v_current(k) for every dependency k, and requires each record still to
exist. Explicit temporary answers must also have the current epoch. On failure,
the artifact stays visible as needing revalidation. Already released local drafts
are marked affected; their old release events remain in the audit trail.

This guarantees consistency with the **stored** state under complete dependency
registration. It cannot guarantee the state was interpreted correctly. It also
cannot discover dependencies that an external agent failed to register.

The global version baseline rereads every required value following any new source
epoch. The selective method rereads only stale dependencies. Under identical
record values and deterministic artifact functions, their final answers should
be equal. Any observed equality is expected, not a new empirical discovery.
Selectivity can reduce machine rereads, which are not human inspections.

## Comparators and ablations

| Method | Behavior |
|---|---|
| Independent requests | Each role asks separately when preparing and releasing work. Explicitly an upper-demand reference with a scripted accurate responder. |
| Full history | Qwen answers directly from the complete released conversation at each epoch; available user confirmations are shared. |
| Semantic memory | Qwen selects from all reconstructed current memories at each epoch, including updates. No top-k retrieval handicap. |
| Records at read | Source-checked structured records, but already prepared work has no release consistency check. |
| Global version barrier | Source-checked records; refresh all artifact inputs after an epoch change. |
| Selective dependency barrier | Same records and request parsing; refresh only invalidated dependencies. |
| No source guard | Selective method with schema checks but without user-source, quotation or conditional-scope checks. |
| No domain scope | Selective method resolves matching attribute names across domains, a deliberately weakened scope ablation. |
| Confirm every new record | Selective method requiring a simulated user confirmation before each inferred value is reused in an epoch. An idealized quality reference whose extra decisions are counted. |

Question requests, answered questions, distinct underlying decisions, incorrect
uses, unresolved artifacts and correct project completion are reported separately.
A record may unblock several roles, but one project remains one statistical unit.
Potential source-card inspections are counted as opportunities, not observed
reading. A sensitivity display may add 0, 0.25 or 1 assumed inspection equivalents
per distinct reused source. It is explicitly not a cognitive-load measurement.

## Two evaluation layers

Controlled tests establish source isolation, exceptions, revocation, conflicting
values, approval scope, stale release rejection and deterministic replay. The
source-grounded pilot adds fallible GPU extraction, request interpretation and
baseline answering to an executable local database/brief adapter. Agent request
wordings and artifact functions are authored, not autonomously generated plans.

Development uses eight official validation dialogues. The final comparison uses
24 different official test dialogues, twelve with and twelve without a retained
preference change, selected in source-ID order within each stratum. Two generation
seeds per project are paired across methods. Caps of two, four and six roles model
request demand. Roles with no supported final input fields are inactive and never
credited as completed artifacts. Three test role instances are inactive at the
six-role cap. A source dialogue, with all its conditions and replicates, is the
analysis unit. This is a stress-balanced exploratory sample, not a population
estimate of how frequently users change their minds. Dialogue IDs and text are
disjoint; shared task templates, database records and possible model training
contamination remain limitations.

At each of two source epochs, only already stated, annotation-supported fields
are requested by the constructed workload. After the update, all applicable final
fields must be reflected in released artifacts. Benchmark state and local query
results define correctness. Unstated, no-preference and unsupported fields are
excluded by the frozen source rule, not by model outcomes.

An accurate scripted responder answers only explicit clarification requests and
only within a declared total response budget of 0, 2, 6 or unlimited. Failed calls
and malformed outputs cause abstention or more questions; they are not dropped.
Without an answer, dependent work remains unresolved. Historical user utterances
are common source evidence, not newly measured user effort. We add no synthetic
deadlines or user response times to this application.

Primary comparison: selective dependency barrier minus semantic memory in project
correctness and additional clarification responses, six roles and unlimited
responses. Report both quantities without combining them into a weighted score.
Full history and the global barrier remain prominent comparators. Other demand,
budget and ablation contrasts are secondary. Average generation replicates within
each dialogue, then use 2,000 paired bootstrap resamples with analysis seed 91831,
resampling the changed/unchanged strata separately. Keep all matched conditions
together. Intervals describe this small selected dialogue sample.
