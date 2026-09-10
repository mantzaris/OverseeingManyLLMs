#!/usr/bin/env python3
"""Consolidate recorded stages without resetting any historical timestamp."""
from datetime import datetime,timezone
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.io import write_json
root=Path('artifacts/stage6_robustness');rows=[]
for folder,name in [('artifacts/stage1_gpu_live','stage1_l40s'),('artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z','stage1_ada')]:
    r=json.loads((Path(folder)/'result_verification.json').read_text());p=r['placement']
    rows.append(dict(stage=name,scheduled_calls=r['experimental_scheduled_calls']+p['scheduled_calls'],attempts=r['experimental_attempts']+p['attempts'],retries=r['retries'],failed_attempts=0,prompt_tokens=r['experimental_prompt_tokens']+p['prompt_tokens'],completion_tokens=r['experimental_completion_tokens']+p['completion_tokens']))
for name in ('stage2_development','stage3_competition'):
    r=json.loads((Path('artifacts')/name/'run/manifest.json').read_text());p=r['placement']
    rows.append(dict(stage=name,scheduled_calls=r['experimental_scheduled_calls']+p['scheduled_calls'],attempts=r['experimental_attempts']+p['attempts'],retries=0,failed_attempts=0,prompt_tokens=r['experimental_prompt_tokens']+p['prompt_tokens'],completion_tokens=r['experimental_completion_tokens']+p['completion_tokens']))
for name in ('stage4_research','stage5_practical','stage6_robustness'):
    r=json.loads((Path('artifacts')/name/('verification.json' if name=='stage6_robustness' else 'session_accounting.json')).read_text())
    rows.append(dict(stage=name,scheduled_calls=r.get('scheduled_calls',r.get('reserved_scheduled_calls')),attempts=r.get('generation_attempts',r.get('reserved_attempts')),retries=r['retries'],failed_attempts=r['failed_attempts'],prompt_tokens=r['prompt_tokens'],completion_tokens=r['completion_tokens']))
auth=json.loads((root/'authorization.json').read_text());clock=json.loads(Path('reports/implementation_clock.json').read_text())
now=datetime.now(timezone.utc);start=datetime.fromisoformat(auth['started_utc']);original=datetime.fromisoformat(clock['overall_started_utc']);target=datetime.fromisoformat(clock['overall_deadline_utc'])
result=dict(report_checkpoint_utc=now.isoformat(),stage6_started_utc=start.isoformat(),stage6_deadline_utc=auth['deadline_utc'],stage6_inference_cutoff_utc=auth['inference_cutoff_utc'],
    stage6_elapsed_seconds=(now-start).total_seconds(),original_started_utc=original.isoformat(),original_target_utc=target.isoformat(),original_elapsed_seconds=(now-original).total_seconds(),original_target_overrun_seconds=max(0,(now-target).total_seconds()),
    stages=rows,total={k:sum(r[k] for r in rows) for k in ('scheduled_calls','attempts','retries','failed_attempts','prompt_tokens','completion_tokens')},
    accounting_scope='Both Stage 1 GPU demonstrations and Stages 2 through 6. Earlier blocked stages made no inference. Elapsed wall time includes gaps between stages; stage authorizations are separately recorded.',
    provider_allocation_seconds=None,provider_hourly_price=None,provider_charge=None,
    finish_marker='Final Stage 6 Git commit committer timestamp; this report checkpoint precedes final verification and commit.')
write_json(root/'cumulative_accounting.json',result);print(json.dumps(result,indent=2))
