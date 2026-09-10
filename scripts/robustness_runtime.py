#!/usr/bin/env python3
"""Own only the separately launched Stage 6 retail server; preserve port 8000."""
from datetime import datetime,timezone
import argparse,json,os,signal,socket,subprocess,sys,urllib.request
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.gpu import collect_evidence
from overseeing.io import utc_now,write_json
root=Path('artifacts/stage6_robustness')
p=argparse.ArgumentParser();p.add_argument('operation',choices=['start','capture','stop']);p.add_argument('--label',default='before');a=p.parse_args()
if a.operation=='start':
    auth=json.loads((root/'authorization.json').read_text())
    if datetime.now(timezone.utc)>=datetime.fromisoformat(auth['inference_cutoff_utc']):raise SystemExit('Stage 6 inference reserve has begun')
    setup=root/'setup';setup.mkdir(parents=True,exist_ok=False)
    with socket.socket() as s:
        s.settimeout(3)
        if s.connect_ex(('127.0.0.1',8015))==0:raise SystemExit('Port 8015 already occupied; do not alter existing service')
    env=dict(os.environ,HF_HOME=str(Path.cwd()/'model-cache'))
    with (setup/'server.log').open('w') as log:
        proc=subprocess.Popen(['bash','scripts/serve_retail_gpu.sh'],stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,env=env)
    record=dict(started_utc=utc_now(),server_pid=proc.pid,process_group=proc.pid,command=['bash','scripts/serve_retail_gpu.sh'],HF_HOME=env['HF_HOME'],port=8015)
    write_json(setup/'launch.json',record);print(json.dumps(record))
else:
    launch=json.loads((root/'setup/launch.json').read_text());pid=launch['server_pid']
    if a.operation=='capture':
        result=collect_evidence(pid,str(root/'setup/server.log'),str(root/('gpu_'+a.label+'.json')),expected_port=8015,
            serving_limits={'--max-model-len':'16384','--gpu-memory-utilization':'0.4'})
        models=json.load(urllib.request.urlopen('http://127.0.0.1:8015/v1/models',timeout=15))
        assert models['data'][0]['id']=='Qwen/Qwen2.5-7B-Instruct' and models['data'][0]['max_model_len']==16384
        health=urllib.request.urlopen('http://127.0.0.1:8015/health',timeout=15).status
        (root/('metrics_'+a.label+'.txt')).write_bytes(urllib.request.urlopen('http://127.0.0.1:8015/metrics',timeout=15).read())
        write_json(root/('serving_'+a.label+'.json'),dict(captured_utc=utc_now(),health=health,models=models,server_pid=pid,placement_status=result['status']))
        print(json.dumps(dict(status=result['status'],health=health,server_pid=pid)))
    else:
        cmd=Path('/proc/{}/cmdline'.format(pid)).read_bytes().replace(b'\0',b' ').decode()
        assert 'vllm serve Qwen/Qwen2.5-7B-Instruct' in cmd and '--port 8015' in cmd
        assert os.getpgid(pid)==launch['process_group']
        os.killpg(launch['process_group'],signal.SIGTERM)
        write_json(root/'server_stop_requested.json',dict(requested_utc=utc_now(),pid=pid,process_group=launch['process_group'],signal='SIGTERM'))
        print('Stage 6 server stop requested; original server untouched')
