"""Stage-only attempt ledger including interrupted development requests."""
import json,platform,sqlite3,collections
from datetime import datetime,timezone
from .common import ART,ROOT,read,write,digest
from .client import parsed

def run(final=False):
 auth=read(ART/'authorization.json');prior=read(ROOT/auth['prior_ledger']);raws=[read(p) for p in sorted((ART/'raw').glob('*.json'))];intents=[json.loads(x) for x in (ART/'attempts.jsonl').read_text().splitlines()];attempts=[a for r in raws for a in r['attempts']]
 completed_ids={(a['call_id'],a['attempt']) for a in attempts};unreturned=[x for x in intents if (x['call_id'],x['attempt']) not in completed_ids]
 assert len(raws)<=auth['scheduled_call_ceiling'] and len(intents)<=auth['attempt_ceiling']
 assert all(len(r['attempts'])<=2 for r in raws)
 pt=sum(a.get('response',{}).get('usage',{}).get('prompt_tokens',0) for a in attempts);ct=sum(a.get('response',{}).get('usage',{}).get('completion_tokens',0) for a in attempts)
 counts=dict(scheduled_calls=len(raws),attempts=len(intents),prompt_tokens=pt,completion_tokens=ct,retries=sum(a['attempt']>1 for a in intents),failed_attempts=sum(a['status']!='ok' for a in attempts))
 now=datetime.now(timezone.utc);elapsed=(now-datetime.fromisoformat(auth['started_utc'])).total_seconds();wall=(now-datetime.fromisoformat(auth['original_start_utc'])).total_seconds()
 ledger=dict(status='final' if final else 'checkpoint',started_utc=auth['started_utc'],checkpoint_utc=now.isoformat(),deadline_utc=auth['deadline_utc'],inference_cutoff_utc=auth['inference_cutoff_utc'],session_elapsed_seconds=elapsed,original_start_utc=auth['original_start_utc'],original_deadline_utc=auth['original_deadline_utc'],cumulative_wall_seconds=wall,over_original_36h_seconds=max(0,wall-129600),**counts,total_tokens=pt+ct,unreturned_attempts=len(unreturned),unreturned_attempt_details=unreturned,token_accounting='Returned-token lower bound. Interrupted development requests may have generated unobserved tokens; attempt intents are counted conservatively.',call_statuses=dict(collections.Counter(r['status'] for r in raws)),unparseable_success_calls=sum(r['status']=='ok' and parsed(r) is None for r in raws),summed_returned_attempt_latency_seconds=sum(a['elapsed_seconds'] for a in attempts),cumulative={k:prior['cumulative'][k]+v for k,v in counts.items()},historical_accounting='New explicit authorization, not inside original 36h. Cumulative wall includes inter-session gaps.',provider_accounting='Existing GPU only. Price and allocation billing unavailable. Measured request latency is not billing time.',paid_resources_provisioned=0,human_participants=0,python=platform.python_version(),sqlite=sqlite3.sqlite_version)
 batches=[]
 for prefix in ['development_v1','development_v2','development_v3','development_v4','development_v5','evaluation_frozen']:
  rs=[r for r in raws if r['call_id'].startswith(prefix+'_')];ids={r['call_id'] for r in rs}
  batches.append(dict(batch=prefix,scheduled=len(rs),attempts=sum(a['call_id'] in ids for a in intents),returned=sum(len(r['attempts']) for r in rs),statuses=dict(collections.Counter(r['status'] for r in rs)),unparseable=sum(r['status']=='ok' and parsed(r) is None for r in rs)))
 ledger['batches']=batches;write(ART/'resource_ledger.json',ledger)
 write(ART/'generation_manifest.json',[dict(call_id=r['call_id'],status=r['status'],request_sha256=r['request_sha256'],seed=r['request']['seed'],input_tokens=r.get('input_tokens'),max_tokens=r['request']['max_tokens'],attempts=len(r['attempts']),parsed=parsed(r) is not None,response_sha256=digest([a.get('response') for a in r['attempts']])) for r in raws])
 print({k:ledger[k] for k in ['scheduled_calls','attempts','unreturned_attempts','total_tokens','session_elapsed_seconds']});return ledger
if __name__=='__main__':
 import sys;run('--final' in sys.argv)
