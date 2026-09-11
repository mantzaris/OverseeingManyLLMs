"""Separate wall-clock and inference accounting, preserving historical totals."""
import argparse
import json
import platform
from datetime import datetime,timedelta,timezone
from pathlib import Path
from .client import ART,ROOT,parsed,write_json

def account(status='checkpoint'):
    now=datetime.now(timezone.utc);auth=json.loads((ART/'authorization.json').read_text())
    start=datetime.fromisoformat(auth['started_utc']);original=datetime.fromisoformat('2026-09-09T15:38:57+00:00')
    records=[json.loads(p.read_text()) for p in sorted((ART/'raw').glob('*.json'))]
    attempts=[a for r in records for a in r['attempts']]
    usage=[a.get('response',{}).get('usage',{}) for a in attempts]
    prompt=sum(x.get('prompt_tokens',0) for x in usage);completion=sum(x.get('completion_tokens',0) for x in usage)
    history=json.loads((ROOT/'artifacts/attention_sessions/resource_ledger.json').read_text())['cumulative_generations_unchanged']
    failures=sum(a['status']!='ok' for a in attempts);retries=sum(max(0,len(r['attempts'])-1) for r in records)
    result=dict(status=status,started_utc=start.isoformat(),checkpoint_utc=now.isoformat(),
        deadline_utc=auth['deadline_utc'],inference_cutoff_utc=auth['inference_cutoff_utc'],
        session_elapsed_seconds=(now-start).total_seconds(),
        original_start_utc=original.isoformat(),original_deadline_utc=(original+timedelta(hours=36)).isoformat(),
        wall_elapsed_since_original_start_seconds=(now-original).total_seconds(),
        wall_time_after_original_target_seconds=max(0,(now-original-timedelta(hours=36)).total_seconds()),
        clock_interpretation='Separately authorized continuation outside the completed original 36-hour window. Cumulative wall time includes inter-session idle gaps, not only active work or GPU allocation.',
        scheduled_calls=len(records),actual_attempts=len(attempts),transport_failed_attempts=failures,retries=retries,
        successful_but_unparseable_calls=sum(r['status']=='ok' and parsed(r) is None for r in records),
        context_limit_calls=sum(r['status']=='context_limit' for r in records),
        prompt_tokens=prompt,completion_tokens=completion,available_total_tokens=prompt+completion,
        summed_generation_attempt_seconds=sum(a['elapsed_seconds'] for a in attempts),
        generation_finished_utc=max([(datetime.fromisoformat(a['started_utc'])+timedelta(seconds=a['elapsed_seconds'])).isoformat() for a in attempts] or [None]),
        human_participants=0,paid_resources_provisioned=0,python=platform.python_version(),
        provider_accounting='Existing authorized pod reused. No provider billing rate, allocation balance or accrued charge was available; request runtime is not a billed-allocation measurement.',
        cumulative=dict(scheduled_calls=history['scheduled_calls']+len(records),attempts=history['attempts']+len(attempts),
                        retries=history['retries']+retries,failed_attempts=history['failed_attempts']+failures,
                        prompt_tokens=history['prompt_tokens']+prompt,completion_tokens=history['completion_tokens']+completion))
    write_json(ART/'resource_ledger.json',result);return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--status',default='checkpoint');a=p.parse_args();print(json.dumps(account(a.status),indent=2))
