#!/usr/bin/env python3
"""Own a Stage 6 experiment process group and terminate it at the inference cutoff."""
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

root=Path('artifacts/stage6_robustness');name='evaluation'
auth=json.loads((root/'authorization.json').read_text())
cutoff=datetime.fromisoformat(auth['inference_cutoff_utc'])
seconds=(cutoff-datetime.now(timezone.utc)).total_seconds()
if seconds<=0:raise SystemExit('Inference cutoff has passed')
folder=root/'launches'/name;folder.mkdir(parents=True,exist_ok=False)
record=dict(started_utc=datetime.now(timezone.utc).isoformat(),cutoff_utc=cutoff.isoformat(),
    command=[sys.executable,'scripts/robustness_experiment.py','run'],wrapper_pid=os.getpid())
with (folder/'worker.log').open('w') as log:
    worker=subprocess.Popen(record['command'],stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    record['worker_pid']=worker.pid
    (folder/'launch.json').write_text(json.dumps(record,indent=2)+'\n')
    try:
        code=worker.wait(timeout=seconds)
    except subprocess.TimeoutExpired:
        os.killpg(worker.pid,signal.SIGTERM)
        try:worker.wait(timeout=10)
        except subprocess.TimeoutExpired:os.killpg(worker.pid,signal.SIGKILL);worker.wait()
        code=124
    record.update(exit_code=code,finished_utc=datetime.now(timezone.utc).isoformat())
    (folder/'launch.json').write_text(json.dumps(record,indent=2)+'\n')
raise SystemExit(code)
