# Local adapter and end-to-end walkthrough

Start the desk from the repository root:

```bash
python3 research/decision_dependencies/prototype/server.py --port 9027
```

Open `http://127.0.0.1:9027`. This uses saved development model outputs and local
benchmark databases. It does not call a model, book anything or contact a user.
Press Ctrl-C to stop it. Interaction logs default to
`/tmp/decision-desk-demonstration.jsonl`.

## Walkthrough

1. Inspect the first dining question and the released conversation evidence.
   The source user asked for Christmas food. The saved model failed to recover
   that preference in its initial record set, so the desk asks for clarification.
2. Open **Answer or change the scope**. Enter `christmas`, choose **Cuisine** and
   **All requests for this trip and decision type**. One explicit answer now
   resolves the dining and itinerary questions. Answering **Only this request**
   instead deliberately leaves the other question unresolved.
3. Click **Prepare available work**. The dining query executes against the local
   restaurant database. No matching Christmas-food restaurant is an honest empty
   shortlist, not a successful booking.
4. Click **Show the user's next update**. The source user changes the cuisine to
   Indian. The two drafts become affected. **Release checked draft** blocks the
   stale draft. Re-prepare, inspect the new shortlist and release it.
5. In the shared cuisine decision, add `conference-night` to its exceptions.
   A request carrying that entity cannot reuse the general answer. A request-only
   answer can resolve the exception without changing the ordinary dining plan.
6. Postpone an unanswered question. It remains visible and can be brought back.

This demonstration includes an extraction failure rather than substituting a
benchmark answer for the model's interpretation. It is scripted development
evidence, not participant data.

## API contract

`GET /api/state` returns the public current state. `POST /api/action` accepts JSON.
The smallest agent integration is:

```python
from research.decision_dependencies.adapter import DecisionDesk

desk = DecisionDesk('http://127.0.0.1:9027')
desk.submit('conference_dinner', 'Conference dinner',
            'What cuisine should the separate conference dinner use?',
            candidate_scope='restaurant.food', entity='conference-night')
print(desk.status('conference_dinner'))
# The user may answer in the local interface.
desk.prepare_available()
print(desk.release('conference_dinner'))
```

An external agent's `candidate_scope` is a hypothesis, not an authoritative label.
The demo's predefined questions use saved Qwen interpretations. A new request
without a candidate scope stays unresolved until a user supplies one. This
endpoint does not silently run a new model for arbitrary incoming text.

Supported actions are `submit`, `answer`, `prepare`, `release`, `source_update`,
`revise`, `defer`, `resume`, `inspect`, `shown` and `reset`. `answer` requires a
request ID, value, explicit domain/attribute key and either `request` or `project`
scope. `revise` accepts a decision key, a new value, named exceptions or
`revoke: true`. `prepare` produces local demonstration artifacts for available
requests. A caller must check release status and must not treat an available
answer as permission for an unrelated external action.

The Python `DecisionController` API supports multi-input work through
`prepare(task_id, answers)` and validates consumed versions in `release(task_id)`.
Integrators must register every dependency. A bypassed release check offers no
guarantee. The local HTTP adapter demonstrates this contract; it is not an
authentication service or production transaction coordinator.

## Interaction provenance

Logs identify the source epoch, server/session identity, state hash, cards entering
the viewport, expanded evidence, answers, scope choices, deferrals, overrides and
rejected operations. Response timing is time since the card was first shown in
the relevant epoch, not measured reading time. Logs are explicitly marked as
development demonstrations. No participant inference is made from scripted
timings, and fresh user-entered logs should not be committed without consent.
