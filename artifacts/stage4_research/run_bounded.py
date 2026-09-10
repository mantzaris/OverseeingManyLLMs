"""Run one declared batch under the session inference cutoff, with telemetry."""
from datetime import datetime,timezone
import json,os,signal,subprocess,sys
from pathlib import Path

root=Path('artifacts/stage4_research');name=sys.argv[1];command=sys.argv[2:]
auth=json.loads((root/'authorization.json').read_text())
remaining=(datetime.fromisoformat(auth['inference_cutoff_utc'])-datetime.now(timezone.utc)).total_seconds()
assert remaining>0 and command
out=root/'launches'/name;out.mkdir(parents=True,exist_ok=False)
record=dict(started_utc=datetime.now(timezone.utc).isoformat(),command=command,checkout=str(Path.cwd()),inference_cutoff_utc=auth['inference_cutoff_utc'])
with (out/'launch.json').open('x') as f:json.dump(record,f,indent=2)
with (out/'gpu_telemetry.csv').open('x') as telemetry,(out/'stdout.txt').open('x') as stdout:
    monitor=subprocess.Popen(['nvidia-smi','--query-gpu=timestamp,uuid,name,memory.total,memory.used,utilization.gpu,power.draw','--format=csv','--loop-ms=1000'],stdout=telemetry,stderr=subprocess.STDOUT)
    worker=None
    try:
        worker=subprocess.Popen(command,stdout=stdout,stderr=subprocess.STDOUT,start_new_session=True)
        record['exit_code']=worker.wait(timeout=remaining)
    except subprocess.TimeoutExpired:
        os.killpg(worker.pid,signal.SIGTERM)
        try:worker.wait(timeout=5)
        except subprocess.TimeoutExpired:os.killpg(worker.pid,signal.SIGKILL);worker.wait()
        record.update(exit_code=124,error='Inference cutoff; worker group terminated, server retained')
    finally:
        monitor.terminate();monitor.wait(timeout=10)
        record['finished_utc']=datetime.now(timezone.utc).isoformat()
        (out/'launch.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2));print('\n'.join((out/'stdout.txt').read_text().splitlines()[-10:]))
raise SystemExit(record.get('exit_code',2))
