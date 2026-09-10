#!/usr/bin/env python3
"""Read-only pod status: existing server, GPU allocation, and remaining workers."""
from datetime import datetime, timezone
import importlib.metadata as metadata
import json, shutil, subprocess, urllib.request


def run(args):
    result=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=20)
    return dict(exit_code=result.returncode,output=result.stdout.strip())


def main():
    processes=run(['ps','-eo','pid,args'])
    workers=[]
    for line in processes['output'].splitlines()[1:]:
        parts=line.split()
        # Match script argv entries, not arbitrary occurrences inside other commands.
        if len(parts)>2 and 'python' in parts[1] and any(p.endswith(('research_session.py','run_bounded.py')) for p in parts[2:]):
            workers.append(dict(pid=int(parts[0]),command=' '.join(parts[1:])))
    urls={}
    for endpoint in ('health','metrics','v1/models'):
        try:
            with urllib.request.urlopen('http://127.0.0.1:8000/'+endpoint,timeout=15) as response:
                text=response.read().decode();urls[endpoint]=dict(status=response.status,body=text if endpoint!='metrics' else '\n'.join(l for l in text.splitlines() if l.startswith(('vllm:request_success_total{','vllm:prompt_tokens_total{','vllm:generation_tokens_total{','vllm:num_requests_running{','vllm:num_requests_waiting{'))))
        except Exception as error:urls[endpoint]=dict(error=type(error).__name__+': '+str(error))
    result=dict(captured_utc=datetime.now(timezone.utc).isoformat(),remaining_experimental_workers=workers,
        server_processes=run(['ps','-p','7338,8449','-o','pid,etimes,pcpu,pmem,args']),
        gpu=run(['nvidia-smi','--query-gpu=name,uuid,driver_version,memory.total,memory.used,utilization.gpu','--format=csv']),
        compute_processes=run(['nvidia-smi','--query-compute-apps=pid,process_name,used_memory','--format=csv']),
        disk=run(['df','-h','/workspace']),nvcc_on_path=shutil.which('nvcc'),
        packages={p:metadata.version(p) for p in ('torch','vllm','transformers')},endpoints=urls,
        new_generations=0,services_changed=False,billing_information='Not available from this runtime inspection; no monetary allocation estimate inferred.')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
