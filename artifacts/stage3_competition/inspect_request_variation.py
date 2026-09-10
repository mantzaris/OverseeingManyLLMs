"""Post-run reproducibility check of saved request JSON; zero new generations."""
import json
from pathlib import Path
import sys
from collections import defaultdict
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from overseeing.domain import digest
out = Path(__file__).resolve().parent
by_request = defaultdict(list)
for path in sorted((out / 'run').glob('*/*/*/raw_requests.jsonl')):
    for line in path.read_text().splitlines():
        row = json.loads(line)
        if row['phase'] == 'attempt_finished' and 'parsed_action' in row:
            by_request[digest(row['request'])].append(dict(path=str(path.relative_to(out / 'run')),
                job_id=row['job_id'], sample=row['sample'], action=row['parsed_action']))
differences = [dict(request_hash=h, observations=rows) for h, rows in by_request.items()
               if len({r['action'] for r in rows}) > 1]
record = dict(distinct_request_groups=len(by_request),
              repeated_request_groups=sum(len(rows) > 1 for rows in by_request.values()),
              mixed_action_groups=len(differences), groups=differences,
              note='Post-run reproducibility check, no additional inference. Matching request JSON and seeds did not always yield identical GPU outputs; cause not established.')
(out / 'identical_request_variation.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({k:v for k,v in record.items() if k != 'groups'}, indent=2))
