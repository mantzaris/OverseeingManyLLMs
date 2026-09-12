"""Separate stage accounting. Never edits prior authorizations or ledgers."""
import collections,datetime
from .common import ART,ROOT,read,write
from .transport import parsed

def account(final=False):
 auth=read(ART/'authorization.json');old=read(ROOT/auth['prior_ledger']);now=datetime.datetime.now(datetime.timezone.utc);raw=[read(p) for p in (ART/'raw').glob('*.json')];attempts=[a for r in raw for a in r['attempts']];intents=(ART/'attempts.jsonl').read_text().splitlines() if (ART/'attempts.jsonl').exists() else []
 totals=dict(scheduled_calls=len(raw),attempts=len(intents),failed_attempts=sum(a['status']!='ok' for a in attempts),retries=sum(max(0,len(r['attempts'])-1) for r in raw),prompt_tokens=sum(a.get('response',{}).get('usage',{}).get('prompt_tokens',0) for a in attempts),completion_tokens=sum(a.get('response',{}).get('usage',{}).get('completion_tokens',0) for a in attempts))
 stages=collections.defaultdict(list)
 for r in raw:stages['_'.join(r['call_id'].split('_')[:2])].append(r)
 out=dict(stage=auth['stage'],checkpoint_utc=now.isoformat(),started_utc=auth['started_utc'],deadline_utc=auth['deadline_utc'],inference_cutoff_utc=auth['inference_cutoff_utc'],**totals,returned_generations=sum(a['status']=='ok' for a in attempts),unparseable_returns=sum(r['status']=='ok' and parsed(r) is None for r in raw),statuses=dict(collections.Counter(r['status'] for r in raw)),unresolved_attempt_intents=len(intents)-len(attempts),generation_seconds=sum(a['elapsed_seconds'] for a in attempts),stage_elapsed_seconds=(now-datetime.datetime.fromisoformat(auth['started_utc'])).total_seconds(),cumulative_wall_seconds=(now-datetime.datetime.fromisoformat(auth['original_start_utc'])).total_seconds(),original_36h_overrun_seconds=(now-datetime.datetime.fromisoformat(auth['original_deadline_utc'])).total_seconds(),cumulative={k:old['cumulative'].get(k,0)+v for k,v in totals.items()},prior_ledger=auth['prior_ledger'],final=final,supervision='Simulated ideal question-specific annotation disclosure; no participant observations',gpu='Existing Qwen2.5-7B BF16 RTX6000Ada, zero CPU offload; server retained',batches=[dict(batch=k,scheduled=len(rs),attempts=sum(len(r['attempts']) for r in rs),statuses=dict(collections.Counter(r['status'] for r in rs))) for k,rs in sorted(stages.items())])
 assert len(raw)<=auth['scheduled_call_ceiling'];assert len(intents)<=auth['attempt_ceiling'];assert all(len(r['attempts'])<=2 for r in raw)
 write(ART/'resource_ledger.json',out);print({k:out[k] for k in ['scheduled_calls','attempts','statuses','stage_elapsed_seconds']});return out
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');a=p.parse_args();account(a.final)
