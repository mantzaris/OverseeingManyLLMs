# Local adapter API

Run `python3 -m research.oversight_workflow.prototype.server --port 9041`.
The server binds to loopback. The UI and both workload adapters use the same
`Desk.command(event_id, action, payload)` protocol. Every external command supplies
its current `session_id` and a stable unique `event_id`. Retrying identical content
with that ID returns the previous receipt. Reusing it for different content fails.

- `GET /api/catalog`: twelve source-packet descriptions, without annotations.
- `POST /api/start`: `{condition:"threads"|"queue"|"sessions", mode:"replay"|"live"|"manual", bundle:0, replica:0, interval:1.5}`. Replay starts wall-clock deliveries of saved actual answers. Live uses the bounded existing GPU transport. A `study_packet` from 0 to 3 loads the six-context prospective packet instead of a two-context demo bundle.
- `GET /api/state`: current public logical state, counts and recommended next ID.
- `POST /api/command`: `{session_id, event_id, action, payload}`. Supported actions are offer, admit, start, receive, select, session, note, decide, release, revise, refresh, pause, resume, withdraw and display.
- `GET /api/export`: atomic event/state snapshot suitable for logical replay.
- `GET /api/journals`: saved local journal names.
- `POST /api/restore`: `{name:"<journal>.jsonl"}` restores a recorded state without starting any workers. The path must remain inside the configured journal directory.

Example task submission in Python:

```python
from research.oversight_workflow.protocol import Desk
from research.oversight_workflow.data import task

desk = Desk('sessions')
offer = task(public_context, original_question, replica=0)
desk.command('offer-1', 'offer', offer)
desk.command('admit-1', 'admit', {'id': offer['id']})
desk.command('start-1', 'start', {'id': offer['id']})
# A background task independently obtains a model answer.
desk.command('arrival-1', 'receive', {'id': offer['id'], 'output': generated_answer})
# No answer is released until a user selects, decides and explicitly releases it.
```

The output object contains `answer` (list, including empty for failure), `scale`,
optional `evidence` and `derivation`. Full source remains available when these are
incomplete. A readable response is sufficient. No schema-generated computation is
required. Revision creates a new immutable version; an active older snapshot is
not changed. The UI has no reference-answer endpoint.

This is a local single-user research server. It is not an authenticated public
service or a crash-atomic distributed queue. Bound requests, escape source strings,
refuse cross-origin commands, and do not expose the loopback port to untrusted users.
The interaction journal is written before command acknowledgement but does not
claim fsync-backed durability. New network latency measurements require running
the browser harness; saved traces only reproduce their numerical analysis.

`mode: "training"` loads two old development questions with their saved pilot
answers. `?training=1` opens that practice view. Its optional 18-second same-answer
revision is an authored version fixture, explicitly distinguished from real model
rechecks. `close_session` is the server timer's command for a prospective study
cutoff. It refuses subsequent decisions/releases while accepting in-flight answers.
