# Change a connected report once

Start the desk from the repository root:

```bash
python3 -m research.coordination_injections.prototype.server --port 9033
```

Open http://127.0.0.1:9033. Select **2011-09 - period**, **original frozen study**, and **targeted**. Load the original, apply the change once, and step through each recorded response. The displayed selection labels may include additional words; the case ID is `eval_09_0`.

This is the first replica-0 case in frozen ID order where targeted completes and broadcast does not. It was not selected by effect magnitude. The inputs are recorded transaction lines; the reporting brief, scope and change are authored. Responses are saved GPU continuations, not participant observations.

## The instruction and work

```json
{
  "exceptions": [
    "appendix"
  ],
  "scope": "main",
  "source": "authorized_user",
  "text": "Use the second half of the month for the main outputs. Keep the appendix on the full original month.",
  "version": 2
}
```

The analysis produces a table, the chart consumes that table, and the report consumes the chart. The appendix keeps the original full-month contract. The original and revised executable analysis are:

### Before

```sql
SELECT stock_code, SUM(quantity) AS value FROM transactions WHERE invoice_date >= '2011-09-01' AND invoice_date < '2011-10-01' AND unit_price_micro > 0 AND quantity > 0 AND is_cancel = 0 GROUP BY stock_code ORDER BY value DESC, stock_code ASC LIMIT 5
```

| Stock code | Recorded quantity (items) |
|---|---:|
| 85099B | 4401 |
| 22197 | 4196 |
| 22952 | 3711 |
| 84077 | 3515 |
| 21212 | 3426 |

The chart receives exactly these saved rows. The report tool returns:

```json
{
  "displayed_products": 5,
  "displayed_total": 19249,
  "top_stock": "85099B",
  "top_value": 4401
}
```

### After

```sql
SELECT stock_code, SUM(quantity) AS value FROM transactions WHERE invoice_date >= '2011-09-16' AND invoice_date < '2011-10-01' AND unit_price_micro > 0 AND quantity > 0 AND is_cancel = 0 GROUP BY stock_code ORDER BY value DESC, stock_code ASC LIMIT 5
```

| Stock code | Recorded quantity (items) |
|---|---:|
| 85099B | 2936 |
| 22197 | 2492 |
| 23285 | 2023 |
| 21787 | 2020 |
| 23288 | 2002 |

The chart receives exactly these saved rows. The report tool returns:

```json
{
  "displayed_products": 5,
  "displayed_total": 11473,
  "top_stock": "85099B",
  "top_value": 2936
}
```

The appendix artifact hash is unchanged: `8c0e66183a1933f15156532ba2f0551a8727701e4af5b7711b24d95230358502`. Targeted needs 4 model calls, including the retained unsuccessful report attempt before repair. Passing the public guard and matching the independent numerical reference are separate recorded checks. A generated narrative can still use the wrong entity name; structured acceptance is not unrestricted prose certification.

## Inspect a tie and a failure

- **Tie:** `eval_02_0`, replica 0, targeted and broadcast both complete. The standalone `timeline_tie` figure retains it.
- **Format failure:** the same case under original shared-state presentation leaves its report unresolved because an explicit `tool`/`params` response is rejected by the frozen strict parser. Select the separately labeled interface-repair follow-up to inspect the fresh successful continuation. It is not a replacement for the historical trace.
- **Retained follow-up failure:** `eval_07_1` with shared state still uses an unsupported `parameters` envelope. It remains unfinished; the parser was not tuned again.
- **Narrative failure:** `eval_06_0` has a report calling stock codes customers despite correct numerical values. Its raw prose is expandable and the normal card uses checked contract labels.

The custom-change panel is a separate deterministic mode. Select a supported country, metric, inclusion or customer rule and apply it to the main scope. This runs on the pinned real snapshot without GPU calls and preserves the appendix. Unsupported actions are rejected, and unresolved artifacts remain visible.

## Reproduce the evidence

```bash
python3 -m research.coordination_injections.reproduce --download --output /tmp/coordination-replay
node research/coordination_injections/prototype/browser_smoke.mjs /tmp/coordination-browser
```

The browser command requires the local server above. It generates scripted demonstration events and screenshots, not participant data. Stop the desk with Ctrl-C.
