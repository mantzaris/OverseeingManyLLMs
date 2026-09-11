# Agent and interface API

Start the local desk with `python3 research/clarification_planning/prototype/server.py`.
It binds to 127.0.0.1:9031. It uses an authored project, not evaluation labels.
The planner selector offers one, two and three steps, a completion rule, memory,
generic bounded search, and the secondary minimum-sufficient-completion audit. The current online controller is `SafeProtocol`.

```python
from research.clarification_planning.adapter import ClarificationDesk
api = ClarificationDesk()
question = api.next_question()
print(question['text'], question['scope'], question['enables'])
api.answer('screen_reader')
print(api.next_question()['text'])
api.answer('web')
print(api.act('finish')['work'])
```

These example responses are scripted, not participant observations. To answer
narrowly, use `api.answer(value, only_task='Website implementation')`. That creates
a distinct scoped record and consumes two units: one for the value and one for changing its proposed scope. The operation is rejected if both units are unavailable. Answering within the already stated scope costs one unit. Other deliverables do not
silently inherit it. `api.defer()` also consumes one answer because an actual
question was posed and the user reported that it could not be resolved. It leaves
work visible. `api.act('ask', id='meeting')` overrides selection while retaining
budget checks. `api.revise('format', value='pdf')` shows prior work needing
revalidation. Explicit unsolicited revisions are separate logged user events and
do not reset the remaining solicited-question budget.

For other applications, construct public records and task dependencies directly:

```python
from research.clarification_planning.planner import Factor, Task, Option, Planner
from research.clarification_planning.safe_protocol import SafeProtocol
factors = [Factor('project.format', ('web','pdf'), (.5,.5),
                  scope='Project A / output format', source='Unresolved project brief')]
tasks = [Task('implementation', (Option((('format','project.format'),)),))]
controller = SafeProtocol(Planner(factors, tasks), budget=2)
question = controller.propose('depth2')
# An actual answer enters here, after the question is shown.
controller.answer('web')
outputs = controller.finish()
```

Each task's options explicitly register value and scope-factor dependencies. Use
`allowed_tasks` and `exceptions` on a Factor to restrict represented applicability.
Use a Boolean factor of kind `scope` and a gate such as `(('scope_id','yes'),)`
for uncertain applicability. Alternative local bindings must be registered
explicitly. Keep any evaluator/simulated responder outside this controller.

REST endpoints: `GET /api/state`, `POST /api/action`, `GET /api/log`. Actions are
reset, next, ask, answer, defer, revise, finish and inspect. Errors return HTTP 400
and roll back the attempted state mutation. Unknown methods and negative budgets
are rejected. All actual display text, action payloads, state hashes, monotonic
response intervals, inspection events and changes are logged. Those timing fields
measure the scripted/development interaction that produced them, not human effort.

The package does not execute deployments, bookings or purchases. An integrator
must register genuine deliverables and their dependencies, define application
checks, and enforce the release guard. Scope metadata is not a semantic proof or
an authorization system for external side effects.
