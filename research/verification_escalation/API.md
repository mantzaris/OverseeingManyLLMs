# Local Decision desk and agent adapter

```bash
python3 -m research.verification_escalation.prototype.server --port 9032
# Open http://127.0.0.1:9032
```

The default authored analytics workload has four roles and four distinct goals.
Two results can be produced before the user answers. The customer export needs
an eligibility definition. The partner export has its own scope and remains
unresolved after an Atlas answer. Selecting a new data snapshot marks old results
for revalidation. A narrow answer costs one value decision plus one scope decision.
Deferring a displayed question consumes one answer unit and keeps unfinished work.
These are transparent accounting conventions, not measured attention costs.

The server exposes `GET /api/state`, `GET /api/log`, and `POST /api/action`.
For example:

```python
from research.verification_escalation.adapter import Client
client = Client('http://127.0.0.1:9032')
client.act(action='inspect')
client.act(action='answer', value='spending', only_this_request=False)
print(client.state()['work'])
client.act(action='reconsider', task='export') # revise the shared definition
client.act(action='snapshot')   # authored demo change, not an external database
```

For another local application, construct `Controller(tasks, preparations, B, M)`
from `controller.py`. Each public task provides `id`, `request`, `snapshot`,
`contract`, `scope`, `version`, `sources`, `exceptions` and an optional explicitly
registered `decision_id`. Each preparation contains `candidates` and `audit`
objects with up to three `{meaning, sql}` alternatives and the unsupported-option
flag. `inspect()` runs bounded checks. `next_question()` returns an escalation
record. Only after that call should an adapter request the real user's answer and
call `answer(question, response)`. A response maps independently implemented SQL
for each registered affected task. Unknown or unresolved responses are `None`.
Do not import benchmark evaluator files into an agent process.

Use `ValidatedController` from `integrity.py` for an interactive application. It
checks public SQLite integrity before delegating to `OnlineController`, which
handles revised instructions.
It retains all answer events but makes a changed dependency version eligible for
reconsideration, without resetting spent budget. The desk also validates the
currently displayed certificate key before applying an answer. `revise` invalidates
pending questions. These online guards are isolated from frozen terminal-only
experimental replays. A caller must register all relevant dependencies; the API
does not discover semantic sharing from similar wording.

The interface logs what was displayed, action payloads, source/version status,
response time, simulated data changes, deferrals and certificate keys. Logs are
explicitly development observations, not participant data. All database execution
is local and read-only. This research adapter is not a general database gateway.

The **Reconsider this definition** button invalidates the selected registered
scope and makes its question eligible again. It leaves unrelated inventory and
partner work unchanged and never restores consumed answer units. A scope record
must be explicitly replaced or revoked when the user changes its authority.
