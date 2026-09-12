"""One separately authorized stage ledger, with historical totals preserved."""
import collections,datetime
from .common import ART,ROOT,read,write
from .client import parsed

def account(final=False):
 auth=read(ART/'authorization.json');previous=read(ROOT/auth['prior_ledger']);now=datetime.datetime.now(datetime.timezone.utc);raw=[read(p) for p in sorted((ART/'raw').glob('*.json'))];attempts=[a for r in raw for a in r['attempts']];intents=[readline for readline in (ART/'attempts.jsonl').read_text().splitlines() if readline];status=collections.Counter(r['status'] for r in raw);groups=collections.defaultdict(list)
 for r in raw:
  cid=r['call_id'];k='evaluation' if cid.startswith('evaluation_') else 'development_protocol' if cid.startswith('development_protocol_') else '_'.join(cid.split('_')[:2]);groups[k].append(r)
 totals=dict(scheduled_calls=len(raw),attempts=len(intents),returned_attempts=sum(a['status']=='ok' for a in attempts),failed_attempts=sum(a['status']!='ok' for a in attempts),retries=sum(max(0,len(r['attempts'])-1) for r in raw),prompt_tokens=sum(a.get('response',{}).get('usage',{}).get('prompt_tokens',0) for a in attempts),completion_tokens=sum(a.get('response',{}).get('usage',{}).get('completion_tokens',0) for a in attempts))
 cumulative={k:previous.get('cumulative',{}).get(k,0)+v for k,v in totals.items() if k!='returned_attempts'}
 runs=[read(p) for p in (ART/'evaluation/runs').glob('*.json')]
 out=dict(evaluation_policy_traces=len(runs),simulated_inspections_across_declared_runs=sum(r['inspections'] for r in runs),simulated_inspection_note='Sum across alternative policy runs and diagnostics, including replayed budget prefixes; not actual human decisions or independent annotation labor.',stage='adaptive_correction_transfer',checkpoint_utc=now.isoformat(),started_utc=auth['started_utc'],deadline_utc=auth['deadline_utc'],inference_cutoff_utc=auth['inference_cutoff_utc'],**totals,call_statuses=dict(status),unparseable_ok=sum(r['status']=='ok' and parsed(r) is None for r in raw),unresolved_attempt_intents=len(intents)-len(attempts),generation_seconds=sum(a['elapsed_seconds'] for a in attempts),stage_elapsed_seconds=(now-datetime.datetime.fromisoformat(auth['started_utc'])).total_seconds(),cumulative_wall_seconds=(now-datetime.datetime.fromisoformat(auth['original_start_utc'])).total_seconds(),original_36h_overrun_seconds=max(0,(now-datetime.datetime.fromisoformat(auth['original_deadline_utc'])).total_seconds()),cumulative=cumulative,prior_ledger=auth['prior_ledger'],human_participants=0,supervision='Ideal question-specific annotation disclosure, not human or fallible-model review',gpu='Existing RTX6000Ada BF16 Qwen2.5-7B, no CPU model offload',historical_accounting='This stage is separately authorized; cumulative wall includes inter-session gaps and is outside the original 36h target.',final=final,batches=[dict(batch=k,scheduled=len(rs),attempts=sum(len(r['attempts']) for r in rs),statuses=dict(collections.Counter(r['status'] for r in rs))) for k,rs in groups.items()])
 assert out['scheduled_calls']<=auth['scheduled_call_ceiling'];assert out['attempts']<=auth['attempt_ceiling'];assert all(len(r['attempts'])<=2 for r in raw)
 write(ART/'resource_ledger.json',out);print({k:out[k] for k in ['scheduled_calls','attempts','prompt_tokens','completion_tokens','stage_elapsed_seconds','call_statuses']});return out
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');a=p.parse_args();account(a.final)
