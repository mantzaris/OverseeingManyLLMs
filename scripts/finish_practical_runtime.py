#!/usr/bin/env python3
"""Capture final GPU evidence, then stop only this stage's separate serving group.

Run on the recorded pod after every preparation worker has exited. The original
port-8000 server and persistent files remain intact. No generation is requested.
"""
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import urllib.request
import urllib.error

root=Path('artifacts/stage5_practical')
assert Path('scripts/capture_research_status.py').is_file(),'Transfer the read-only status helper before cleanup'
assert (root/'runtime_initial.json').is_file(),'Transfer the captured baseline status before cleanup'
launch=json.loads((root/'setup/launch.json').read_text());server=launch['server_pid']
assert launch['port']==8015 and launch['preserved_server_pid']==7338
for path in sorted((root/'launches').glob('*/launch.json')):
    record=json.loads(path.read_text())
    assert 'exit_code' in record and 'finished_utc' in record,path
    for key in ('worker_pid','wrapper_pid'):
        process=Path('/proc')/str(record[key])
        if process.exists():
            command=(process/'cmdline').read_bytes().split(b'\0')
            assert not any(part.endswith((b'retail_experiment.py',b'run_retail_bounded.py')) for part in command),record[key]
command=(Path('/proc')/str(server)/'cmdline').read_bytes().split(b'\0')
assert b'--port' in command and command[command.index(b'--port')+1]==b'8015'
assert b'Qwen/Qwen2.5-7B-Instruct' in command
assert os.getpgid(server)==server and os.getpgid(7338)!=server
subprocess.run([sys.executable,'scripts/capture_retail_status.py','after'],check=True,timeout=60)
record=dict(captured_before_stop_utc=datetime.now(timezone.utc).isoformat(),stopped_process_group=server,
    reason='Declared Stage 5 preparation matrix finished; release only the separate retail server allocation.',
    preserved_server_pid=7338,signal='SIGTERM',persistent_files_removed=False)
(root/'server_stop_started.json').write_text(json.dumps(record,indent=2)+'\n')
os.killpg(server,signal.SIGTERM)
def group_members():
    rows=subprocess.check_output(['ps','-eo','pid,pgid,stat,comm'],text=True).splitlines()[1:]
    return [line.strip() for line in rows if int(line.split()[1])==server and not line.split()[2].startswith('Z')]
for _ in range(40):
    if not group_members():break
    time.sleep(.5)
remaining=group_members()
if remaining:
    os.killpg(server,signal.SIGKILL);record['forced_kill_after_grace']=remaining
    for _ in range(20):
        if not group_members():break
        time.sleep(.5)
assert not group_members()
status=json.loads(subprocess.check_output([sys.executable,'scripts/capture_research_status.py'],text=True,timeout=60))
assert status['endpoints']['health']['status']==200
initial=json.loads((root/'runtime_initial.json').read_text())
def counters(value):
    result={}
    for line in value.splitlines():
        if line.startswith(('vllm:prompt_tokens_total{','vllm:generation_tokens_total{','vllm:request_success_total{')):
            key=line.split('{')[0];result[key]=result.get(key,0)+float(line.rsplit(' ',1)[1])
    return result
assert counters(initial['endpoints']['metrics']['body'])==counters(status['endpoints']['metrics']['body'])
try:
    urllib.request.urlopen('http://127.0.0.1:8015/health',timeout=3)
    raise AssertionError('Stage 5 server is still accepting requests')
except urllib.error.URLError:pass
status.update(stage5_experimental_workers_remaining=[],stage5_separate_server_stopped=True,
    original_server_generation_counters_unchanged=True)
record['finished_utc']=datetime.now(timezone.utc).isoformat()
(root/'runtime_final.json').write_text(json.dumps(status,indent=2)+'\n')
(root/'server_stop.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
