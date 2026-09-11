#!/usr/bin/env python3
"""Read-only final state of the reused server and this stage's serial workers."""
import json,subprocess,urllib.request
from pathlib import Path
from datetime import datetime,timezone
root=Path('artifacts/stage7_empirical');workers=[]
for p in Path('/proc').iterdir():
    if not p.name.isdigit():continue
    try:args=(p/'cmdline').read_bytes().decode().strip('\0').split('\0')
    except (OSError,UnicodeError):continue
    if 'scripts/hvac_infer.py' in args:workers.append(int(p.name))
result=dict(captured_utc=datetime.now(timezone.utc).isoformat(),experimental_workers=workers,health=urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=10).status,
    metrics=urllib.request.urlopen('http://127.0.0.1:8000/metrics',timeout=10).read().decode(),gpu_processes=subprocess.check_output(['nvidia-smi','--query-compute-apps=pid,process_name,used_gpu_memory','--format=csv'],text=True),services_changed=False,server_started_for_stage7=False)
assert not workers and result['health']==200
(root/'runtime_at_completion.json').write_text(json.dumps(result,indent=2)+'\n');print(result['captured_utc'],'healthy; no Stage 7 inference workers')
