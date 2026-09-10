#!/usr/bin/env python3
"""Same-pod retail serving identity, placement and counters; no model generation."""
import json
from pathlib import Path
import sys
import urllib.request
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.gpu import collect_evidence
from overseeing.io import utc_now,write_json

root=Path('artifacts/stage5_practical');label=sys.argv[1]
launch=json.loads((root/'setup/launch.json').read_text())
result=collect_evidence(launch['server_pid'],str(root/'setup/server_port8015.log'),str(root/('gpu_'+label+'.json')),
    expected_port=8015,serving_limits={'--max-model-len':'16384','--gpu-memory-utilization':'0.4'})
models=json.load(urllib.request.urlopen('http://127.0.0.1:8015/v1/models'))
assert models['data'][0]['id']=='Qwen/Qwen2.5-7B-Instruct' and models['data'][0]['max_model_len']==16384
health=urllib.request.urlopen('http://127.0.0.1:8015/health').status
(root/('metrics_'+label+'.txt')).write_bytes(urllib.request.urlopen('http://127.0.0.1:8015/metrics').read())
write_json(root/('serving_'+label+'.json'),dict(captured_utc=utc_now(),health=health,models=models,
    server_pid=launch['server_pid'],placement_status=result['status']))
print(json.dumps(dict(status=result['status'],health=health,server_pid=launch['server_pid'])))
