"""Single-writer session ledger: reserve every call/attempt before GPU HTTP dispatch."""
from datetime import datetime, timedelta, timezone
import fcntl
import json
from pathlib import Path

from .io import append_jsonl, utc_now, write_json


class ResearchBudgetExceeded(RuntimeError):
    pass


def authorized_window(record, now=None):
    now = now or datetime.now(timezone.utc)
    start = datetime.fromisoformat(record['started_utc'])
    finish = datetime.fromisoformat(record['deadline_utc'])
    cutoff = datetime.fromisoformat(record['inference_cutoff_utc'])
    if (record.get('name') != 'stage4_research' or record.get('authorization') != 'explicit_user_request'
            or record.get('limit_hours') != 9 or start.tzinfo is None or finish.tzinfo is None
            or cutoff.tzinfo is None or finish != start + timedelta(hours=9)
            or cutoff != finish - timedelta(minutes=90) or not start <= now < cutoff
            or record.get('scheduled_call_limit') != 50000 or record.get('attempt_limit') != 60000):
        raise ResearchBudgetExceeded('Invalid or expired Stage 4 inference authorization/reserve')
    return cutoff


class SessionLedger:
    def __init__(self, root, context):
        self.root, self.context = Path(root), context
        self.authorization = json.loads((self.root / 'authorization.json').read_text())
        self.deadline = authorized_window(self.authorization)
        self.lock = (self.root / 'worker.lock').open('a')
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.lock.close()
            raise ResearchBudgetExceeded('Another session worker owns the ledger')
        self.path = self.root / 'ledger.jsonl'
        records = [json.loads(line) for line in self.path.read_text().splitlines()] if self.path.exists() else []
        self.calls = sum(r['kind'] == 'call_reserved' for r in records)
        self.attempts = sum(r['kind'] == 'attempt_reserved' for r in records)
        self.per_call = {}
        for r in records:
            if r['kind'] == 'attempt_reserved':
                self.per_call[r['call_id']] = self.per_call.get(r['call_id'], 0) + 1
        self.checkpoint()

    def check_time(self):
        if datetime.now(timezone.utc) >= self.deadline:
            raise ResearchBudgetExceeded('Inference cutoff reached; reporting reserve begins')

    def reserve_call(self, metadata, sample):
        self.check_time()
        if self.calls >= self.authorization['scheduled_call_limit']:
            raise ResearchBudgetExceeded('Session scheduled-call ceiling reached')
        self.calls += 1
        append_jsonl(self.path, dict(kind='call_reserved', call_id=self.calls, context=self.context,
                                    metadata=metadata, sample=sample, wall_utc=utc_now()))
        return self.calls

    def reserve_attempt(self, call_id, retry):
        self.check_time()
        if self.attempts >= self.authorization['attempt_limit']:
            raise ResearchBudgetExceeded('Session generation-attempt ceiling reached')
        if retry not in (0, 1) or self.per_call.get(call_id, 0) >= 2 or not 1 <= call_id <= self.calls:
            raise ResearchBudgetExceeded('Invalid call/retry reservation')
        self.attempts += 1
        self.per_call[call_id] = self.per_call.get(call_id, 0) + 1
        append_jsonl(self.path, dict(kind='attempt_reserved', call_id=call_id, attempt_id=self.attempts,
                                    retry=retry, context=self.context, wall_utc=utc_now()))

    def checkpoint(self):
        write_json(self.root / 'ledger_state.json', dict(captured_utc=utc_now(), scheduled_calls=self.calls,
            generation_attempts=self.attempts, scheduled_limit=50000, attempt_limit=60000,
            inference_cutoff_utc=self.deadline.isoformat(), note='Reservations include interrupted/unknown attempts; raw logs reconcile completed responses.'))

    def close(self):
        self.checkpoint()
        fcntl.flock(self.lock, fcntl.LOCK_UN)
        self.lock.close()
