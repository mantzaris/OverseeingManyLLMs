"""Session-wide accounting from scheduled raw records and attempt intents."""
import hashlib,json,platform,sqlite3
from datetime import datetime,timezone
from .common import ART,ROOT,read,write_json
from .client import parsed

def run(final=False):
    auth=read(ART/'authorization.json');previous=read(ROOT/auth['prior_ledger']);raws=[read(p) for p in sorted((ART/'raw').glob('*.json'))]
    attempts=[a for r in raws for a in r.get('attempts',[])];intents=[json.loads(l) for l in (ART/'attempts.jsonl').read_text().splitlines()]
    assert len(attempts)==len(intents),'Attempt still in flight or missing response record'
    assert len(raws)<=auth['scheduled_call_ceiling'] and len(attempts)<=auth['attempt_ceiling']
    assert all(len(r.get('attempts',[]))<=2 for r in raws)
    pt=sum(a.get('response',{}).get('usage',{}).get('prompt_tokens',0) for a in attempts);ct=sum(a.get('response',{}).get('usage',{}).get('completion_tokens',0) for a in attempts)
    now=datetime.now(timezone.utc);elapsed=(now-datetime.fromisoformat(auth['started_utc'])).total_seconds();wall=(now-datetime.fromisoformat(auth['original_start_utc'])).total_seconds()
    counts=dict(scheduled_calls=len(raws),attempts=len(attempts),prompt_tokens=pt,completion_tokens=ct,retries=sum(max(0,len(r['attempts'])-1) for r in raws),failed_attempts=sum(a['status']!='ok' for a in attempts))
    ledger=dict(status='final' if final else 'checkpoint',started_utc=auth['started_utc'],checkpoint_utc=now.isoformat(),deadline_utc=auth['deadline_utc'],inference_cutoff_utc=auth['inference_cutoff_utc'],session_elapsed_seconds=elapsed,original_start_utc=auth['original_start_utc'],original_deadline_utc=auth['original_deadline_utc'],cumulative_wall_seconds=wall,over_original_36h_seconds=max(0,wall-36*3600),inter_session_gap_seconds=(datetime.fromisoformat(auth['started_utc'])-datetime.fromisoformat(previous['checkpoint_utc'])).total_seconds(),**counts,
      total_tokens=pt+ct,context_limit_calls=sum(r['status']=='context_limit' for r in raws),tokenize_failures=sum(r['status']=='tokenize_failed' for r in raws),unparseable_success_calls=sum(r['status']=='ok' and parsed(r) is None for r in raws),summed_attempt_latency_seconds=sum(a['elapsed_seconds'] for a in attempts),cumulative={k:previous['cumulative'][k]+v for k,v in counts.items()},human_participants=0,paid_resources_provisioned=0,provider_accounting='Existing authorized pod only. Price, billed allocation and accrued cost unavailable. Summed request latency is not provider billing time.',historical_accounting='Original 36-hour window exceeded before this session; new work explicitly separately authorized. Cumulative wall includes inter-session gaps.',python=platform.python_version(),sqlite=sqlite3.sqlite_version)
    write_json(ART/'resource_ledger.json',ledger)
    manifests=[]
    for r in raws:
        manifests.append(dict(call_id=r['call_id'],status=r['status'],request_sha256=r['request_sha256'],input_tokens=r.get('input_tokens'),max_tokens=r['request']['max_tokens'],seed=r['request']['seed'],parsed=parsed(r) is not None,attempts=[dict(status=a['status'],started_utc=a['started_utc'],elapsed_seconds=a['elapsed_seconds'],usage=a.get('response',{}).get('usage'),response_sha256=hashlib.sha256(json.dumps(a.get('response'),sort_keys=True).encode()).hexdigest(),error=a.get('error')) for a in r['attempts']]))
    write_json(ART/'generation_manifest.json',manifests)
    print(json.dumps({k:ledger[k] for k in ['scheduled_calls','attempts','context_limit_calls','unparseable_success_calls','total_tokens','session_elapsed_seconds']},indent=2));return ledger
if __name__=='__main__':
 import sys;run('--final' in sys.argv)
