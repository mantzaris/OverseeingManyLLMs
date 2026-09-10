from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess
import sys
import urllib.request,urllib.error
root=Path('artifacts/stage5_practical')
status=json.loads(subprocess.check_output([sys.executable,'scripts/capture_research_status.py'],text=True))
assert status['endpoints']['health']['status']==200
initial=json.loads((root/'runtime_initial.json').read_text())
def counters(value):
 result={}
 for line in value.splitlines():
  if line.startswith(('vllm:prompt_tokens_total{','vllm:generation_tokens_total{','vllm:request_success_total{')):
   key=line.split('{')[0];result[key]=result.get(key,0)+float(line.rsplit(' ',1)[1])
 return result
assert counters(initial['endpoints']['metrics']['body'])==counters(status['endpoints']['metrics']['body'])
rows=subprocess.check_output(['ps','-eo','pid,pgid,stat,comm'],text=True).splitlines()[1:]
assert not [r for r in rows if int(r.split()[1])==242538 and not r.split()[2].startswith('Z')]
assert '243285,' not in status['compute_processes']['output']
try:
 urllib.request.urlopen('http://127.0.0.1:8015/health',timeout=3)
 raise AssertionError('Retail server remains available')
except urllib.error.URLError:pass
for path in (root/'launches').glob('*/launch.json'):
 r=json.loads(path.read_text());assert r['exit_code']==0 and 'finished_utc' in r
 for key in ('worker_pid','wrapper_pid'):
  process=Path('/proc')/str(r[key])/'cmdline'
  if process.exists():assert not any(x.endswith((b'retail_experiment.py',b'run_retail_bounded.py')) for x in process.read_bytes().split(b'\0'))
now=datetime.now(timezone.utc).isoformat()
status.update(stage5_experimental_workers_remaining=[],stage5_separate_server_stopped=True,original_server_generation_counters_unchanged=True)
record=dict(stop_verified_utc=now,stopped_process_group=242538,signal='SIGTERM',preserved_server_pid=7338,persistent_files_removed=False,
 gpu_evidence_captured_utc=json.loads((root/'gpu_after.json').read_text())['captured_utc'],
 timing_note='The first cleanup command stopped the Stage 5 group after final GPU evidence, then failed only on its missing read-only status helper. This recovery verifies the completed stop without restarting or sending another stop signal.',
 cleanup_status_repair='Transferred scripts/capture_research_status.py; no additional inference or service configuration change.')
(root/'runtime_final.json').write_text(json.dumps(status,indent=2)+'\n')
(root/'server_stop.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
