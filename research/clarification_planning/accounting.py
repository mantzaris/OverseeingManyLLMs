"""Separate authorization, request accounting and cumulative historical clocks."""
import argparse
import json
import platform
from datetime import datetime,timezone,timedelta
from .common import ART,ROOT,read,write_json
from .client import parsed

def account(final=False):
    path=ART/'resource_ledger.json'
    if path.exists() and read(path).get('status')=='final':return read(path)
    auth=read(ART/'authorization.json');raw=[read(p) for p in sorted((ART/'raw').glob('*.json'))];attempts=[a for r in raw for a in r['attempts']]
    usage=[a.get('response',{}).get('usage',{}) for a in attempts]
    prompt=sum(u.get('prompt_tokens',0) for u in usage);completion=sum(u.get('completion_tokens',0) for u in usage)
    now=datetime.now(timezone.utc);start=datetime.fromisoformat(auth['started_utc']);old=read(ROOT/'artifacts/decision_dependencies/resource_ledger.json')
    first=datetime.fromisoformat(old['original_start_utc']);previous=old['cumulative'];fail=sum(a['status']!='ok' for a in attempts);retries=sum(max(0,len(r['attempts'])-1) for r in raw)
    assert len(raw)<=auth['scheduled_call_ceiling'] and len(attempts)<=auth['attempt_ceiling']
    assert all(len(r['attempts'])<=2 for r in raw)
    result=dict(status='final' if final else 'checkpoint',started_utc=start.isoformat(),checkpoint_utc=now.isoformat(),deadline_utc=auth['deadline_utc'],inference_cutoff_utc=auth['inference_cutoff_utc'],
        session_elapsed_seconds=(now-start).total_seconds(),original_start_utc=first.isoformat(),original_deadline_utc=old['original_deadline_utc'],
        wall_elapsed_since_original_start_seconds=(now-first).total_seconds(),wall_time_after_original_target_seconds=max(0,(now-first).total_seconds()-36*3600),
        inter_session_gap_since_prior_final_seconds=(start-datetime.fromisoformat(old['checkpoint_utc'])).total_seconds(),
        interpretation='Separately authorized continuation. Cumulative wall time includes idle gaps; this work is outside the historical 36-hour window. No historical clock or attempt total was reset.',
        scheduled_calls=len(raw),actual_attempts=len(attempts),retries=retries,transport_failed_attempts=fail,
        context_limit_calls=sum(r['status']=='context_limit' for r in raw),unparseable_calls=sum(parsed(r) is None for r in raw),
        prompt_tokens=prompt,completion_tokens=completion,total_tokens=prompt+completion,
        summed_generation_attempt_seconds=sum(a['elapsed_seconds'] for a in attempts),
        generation_finished_utc=max((datetime.fromisoformat(a['started_utc'])+timedelta(seconds=a['elapsed_seconds'])).isoformat() for a in attempts),
        human_participants=0,paid_resources_provisioned=0,python=platform.python_version(),
        provider_accounting='Reused existing authorized pod. Provider price, billing duration, remaining allocation and accrued charge are unavailable. Summed request latency is not billing time.',
        cumulative={k:previous[k]+v for k,v in dict(scheduled_calls=len(raw),attempts=len(attempts),retries=retries,failed_attempts=fail,prompt_tokens=prompt,completion_tokens=completion).items()})
    write_json(path,result);print(json.dumps(result,indent=2));return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');account(p.parse_args().final)
