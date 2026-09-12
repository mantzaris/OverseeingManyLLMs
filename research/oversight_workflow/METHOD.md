# A review and release protocol for concurrent task workers

The user reviews outputs from multiple LLM task workers answering questions about
real financial-report tables. A worker is an independently prompted task using
one shared model and GPU service. It is not a different model architecture. There
are no inferred cross-question dependencies and no automatic correction transfer.

## Request and state

An offered task identifies its worker, original question, public source ID/hash,
source provenance and any explicitly registered dependencies. A received request
adds an immutable artifact version, receipt time, requested decision and status.
No financial deadlines are assigned. Optional priority/deadline fields require an
explicit origin, such as a user's instruction. The observation cutoff is not a
business deadline.

Task lifecycle: offered -> admitted -> started -> received. Requests remain
queued, active, deferred, resolved or withdrawn. A revision supersedes the current
artifact version, retains historical versions and decisions, and queues the new
version unless the user is still inspecting the pinned older version.

The desk maintains one active review snapshot. Receiving another request changes
pending work, never that snapshot. Updating the active artifact leaves the old
snapshot visible and marks a newer version as requiring inspection. Refresh is
explicit. A stale decision is refused without destroying the active review.

| User action | Authority and accounting |
|---|---|
| Approve | Approves only the active, current request/version; does not itself release it. |
| Correct and approve | Records the user's answer as a new version and approves that exact correction. Other questions are unaffected. |
| Release | Publishes only the current version with an explicit approval or user correction. Historical releases remain recorded after revision. |
| Reject | Resolves the review by blocking the answer. This is not a completed correct answer. |
| Defer | Keeps the question unresolved, saves notes/source/draft/history and an optional return time. |
| Pause new tasks | Blocks admission and new task starts. In-flight generation and delivery continue. All offered tasks remain counted. |
| Withdraw | Explicitly closes a request with a reason, retaining its versions and history. |

A decision key is (request ID, artifact version). A newer artifact cannot inherit
approval. Source grouping includes at most three visible requests with the same
actual source ID; every question retains its own answer and authority. The group
does not claim a common correct answer. The user can select another request,
change the group, defer, or choose the next pending item.

## Atomic event processing

```
receive command(event_id, action, payload):
    lock desk
    if event_id was processed:
        require identical action and payload; return earlier receipt
    save previous state
    validate transition and exact artifact identity
    apply transition; check structural invariants
    on refusal: restore previous state
    append command, receipt, sequence, timestamps and logical-state hash
    notify waiting clients
```

Commands serialize under a conventional lock. Duplicate transport IDs are
idempotent; a conflicting reuse is rejected. Backend processing is linear in the
number of outstanding tasks for invariant checks and state serialization, plus
source/output byte size. Next-request selection scans pending requests. No search
optimizer is used. Stable FIFO applies without deadlines; explicit user deadlines
use EDF within priority. An active review is nonpreemptive until a user action.

Live and replay drivers use identical offer/admit/start/receive/revise commands.
The live driver has three independently prompted task workers. GPU transport is
serialized under the existing server configuration; interface delivery is not.
The replay driver uses real wall-clock timers and stops at an observation cutoff,
leaving unstarted and unresolved work in state. Neither advances a simulated clock
when a user clicks. Recorded logical events can be replayed deterministically;
fresh model generations and measured latency are not promised deterministic.

## Interface conditions

A provides navigable worker threads, unread counts and the same source/decision
controls. B puts actionable requests in a conventional central queue. C adds
explicit optional source sessions, admission controls and a prominent account of
pending and unstarted work. All three have stable active review, visible outstanding
counts, exact-version decisions, deferral/resumption, full source access and logs.
A is contextual; B versus C is the primary prospective human comparison. C is a
workflow bundle, not an isolated claim about batching. Scripted pause effects are
reported as mechanical throughput/backlog changes, not benefits to people.

## Properties and limits

By induction over accepted commands, every offered task is unstarted, in flight,
or associated with one request. Every received request has exactly one status.
No transition deletes a request. Immutable version records and copied active
snapshots imply arrival stability. A release requires the current version and its
own approving decision. Revision therefore cannot inherit an approval. Grouping
only changes a list of request IDs and cannot authorize sibling answers. Deferral
retains the same source and version history. These statements assume all releases
pass through this single-process controller; they do not cover external side
effects bypassing it, distributed consensus or durable crash-atomic transactions.

The prototype journals logical events and can recover a saved session. It is a
local research application, not a multi-user authenticated deployment. Structural
properties do not imply answer correctness, comprehension or lower workload.
Generated explanations/citations are labeled and never replace the full source.
Annotations are absent from agent requests and the live interface. An ideal
scripted inspection discloses only the question it explicitly corrects. Offline
scoring has a separate private annotation lookup.
