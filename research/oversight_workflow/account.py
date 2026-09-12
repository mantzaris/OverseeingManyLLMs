from datetime import datetime,timezone
from collections import Counter
from .common import ROOT,ART,read,write

def main(final=False):
    auth=read(ART/'authorization.json');old=read(ROOT/auth['prior_ledger']);raw=[read(p) for p in (ART/'raw').glob('*.json')]
    attempts=[a for r in raw for a in r['attempts']];now=datetime.now(timezone.utc)
    counts=dict(scheduled_calls=len(raw),attempts=len(attempts),failed_attempts=sum(a['status']!='ok' for a in attempts),retries=sum(max(0,len(r['attempts'])-1) for r in raw),
        prompt_tokens=sum(a.get('response',{}).get('usage',{}).get('prompt_tokens',0) for a in attempts),completion_tokens=sum(a.get('response',{}).get('usage',{}).get('completion_tokens',0) for a in attempts))
    cumulative={k:old['cumulative'].get(k,0)+v for k,v in counts.items()}
    wall=(now-datetime.fromisoformat('2026-09-09T15:38:57+00:00')).total_seconds()
    ledger=dict(stage='oversight_workflow',started_utc=auth['started_utc'],deadline_utc=auth['deadline_utc'],inference_cutoff_utc=auth['inference_cutoff_utc'],
        checkpoint_utc=now.isoformat(),stage_elapsed_seconds=(now-datetime.fromisoformat(auth['started_utc'])).total_seconds(),
        **counts,statuses=dict(Counter(r['status'] for r in raw)),generation_seconds=sum(a['elapsed_seconds'] for a in attempts),
        batches=dict(Counter(r['call_id'].split('_')[0] for r in raw)),cumulative=cumulative,cumulative_wall_seconds=wall,original_36h_overrun_seconds=max(0,wall-36*3600),
        prior_ledger=auth['prior_ledger'],original_start_utc='2026-09-09T15:38:57+00:00',final=final,
        infrastructure='Existing server and tunnel retained. No paid resource provision. Same pinned Qwen model, BF16 GPU, zero offload.',
        human_observations=0,scripted_inspections='Software scenario inputs only; not human or model review efficacy.')
    write(ART/'resource_ledger.json',ledger);print(counts)

if __name__=='__main__':
    import sys
    main('--final' in sys.argv)
