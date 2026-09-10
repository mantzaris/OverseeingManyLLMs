"""Small durable artifacts; no inference or simulation here."""

import csv
import gzip
from datetime import datetime, timezone
import json
from pathlib import Path


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n")


def append_jsonl(path, data):
    with Path(path).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(data, sort_keys=True, allow_nan=False) + "\n")
        handle.flush()


def read_events(path):
    path = Path(path)
    if not path.exists() and Path(str(path) + ".gz").exists():
        path = Path(str(path) + ".gz")
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_csv(path, rows):
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with Path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def render_trace(events_path, output_path):
    events = read_events(events_path)
    lines = ["# Episode trace", "", "Scoring/diagnostic artifact; not an agent observation.", "",
             "| Tick | Event | Details |", "| --- | --- | --- |"]
    for event in events:
        kind = event["event"]
        if kind == "episode_started":
            lines.insert(2, "Evidence: **{}**, policy **{}**, scenario seed {}.\n".format(
                event["evidence"], event["policy"], event["scenario"]["seed"]))
            continue
        if kind == "observation":
            continue
        detail = {k: v for k, v in event.items() if k not in ("event", "tick", "wall_utc", "seq")}
        lines.append("| {} | {} | `{}` |".format(event.get("tick", "—"), kind,
                     json.dumps(detail, sort_keys=True).replace("|", "\\|")))
    Path(output_path).write_text("\n".join(lines) + "\n")
