# Decision desk and adapter API

The external Python boundary is `api.adapt(project, rep, method, initial, **kwargs)`. It validates registered scope exceptions and authority provenance before calling the frozen experimental core `controller.run`. A project registers four role contracts and their fixed dependency graph. `initial=None` prepares original work. Passing a saved artifact dictionary installs the authorized `after` contract and runs bounded adaptation. The return object contains every displayed packet route, generated request ID, tool result, check, snapshot, unresolved artifact and cost record. `generate_fn` can be the bounded GPU transport or a controlled test responder. Do not put evaluator references into this function's inputs.

`contracts.contract(project, role, epoch)` resolves the explicitly registered scope. `build_artifact` invokes only the constrained aggregate, chart or summary tools. `public_check` verifies the selected contract and consumed dependencies. `pipeline.pipeline` is the zero-inference comparator for these supported contracts. Unsupported task graphs and cycles are rejected. This is a fixed four-role adapter, not a general arbitrary-code orchestration framework.

Start the local UI with:

```bash
python3 -m research.coordination_injections.prototype.server --port 9033
```

Open http://127.0.0.1:9033. The normal view replays saved GPU continuations. It does not regenerate another policy's counterfactual response. The optional custom-change panel executes the deterministic pipeline against the pinned transaction snapshot and labels this separately. The UI keeps the existing historical Decision desk implementation intact.

Local endpoints:

| Endpoint | Purpose |
|---|---|
| GET `/api/cases` | List saved project cases |
| POST `/api/load` with `{id, method, study}` | Load paired original/revised traces |
| POST `/api/event` with `{action, payload}` | Log what was shown or selected |
| POST `/api/custom` with `{id, fields}` | Apply a supported main-scope change through the deterministic pipeline |
| GET `/api/log` | Inspect this server's demonstration events |

Custom fields are country (`ALL`, France, Germany, United Kingdom), metric (`units`, `value_micro`), inclusion (`positive`, `signed`) and customer (`all`, `known`). The protected appendix cannot be broadened through that endpoint. This is a local research interface, not a deployment authorization service.

Logs identify software demonstrations, include UTC and monotonic intervals, shown-state hashes, case/method selections, installed changes and revealed events. These intervals are script or local interaction timings, not participant response measurements. The scripted browser walkthrough captures the original, pending, revised and custom states plus a mobile view:

```bash
node research/coordination_injections/prototype/browser_smoke.mjs /tmp/coordination-browser
```

Close the server with Ctrl-C. The browser script closes the browser it starts. Neither action stops the existing GPU service.

The input validator was added as post-freeze interface hardening. Every frozen project already satisfies it. It rejects malformed scope registrations at the external API; it does not change a collected continuation, prompt or experimental method. Do not expose this local application as an authenticated multi-user service without a real authorization layer.

The external API now recognizes the explicit `tool`/`params` envelopes declared in the parser follow-up. It does not fill missing task arguments from reference answers or the current contract. Conflicting envelopes and malformed argument shapes become blocked proposals with their raw content retained. This interface repair is separate from the frozen strict-parser experiment. `study` selects `primary` or `parser_followup` in the saved-replay endpoint.
