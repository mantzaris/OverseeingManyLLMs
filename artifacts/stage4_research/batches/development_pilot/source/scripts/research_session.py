#!/usr/bin/env python3
"""Explicit Stage 4 declarations/execution; historical commands retain their limits."""
import argparse,json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('command',choices=['prepare-diagnostics','diagnostics','prepare-pilot','run-batch'])
parser.add_argument('--batch',default='development_pilot')
parser.add_argument('--root',default='artifacts/stage4_research')
parser.add_argument('--server-pid',type=int,default=7338)
parser.add_argument('--server-log',default='artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/server.log')
args=parser.parse_args()
from overseeing.research_diagnostics import prepare_diagnostics,run_diagnostics
if args.command=='prepare-diagnostics':result=prepare_diagnostics(args.root)
elif args.command=='diagnostics':result=run_diagnostics(args.root,args.server_pid,args.server_log)
else:
    from overseeing.research_execution import prepare_batch,run_batch
    from overseeing.research_plan import development_plan
    result=(prepare_batch(args.root,args.batch,development_plan(),'Declared initial risk and capacity pilots, no evaluation outcomes available')
            if args.command=='prepare-pilot' else run_batch(args.root,args.batch,args.server_pid,args.server_log))
print(json.dumps(result,indent=2,sort_keys=True))
raise SystemExit(0 if result.get('status') in ('declared','completed') else 2)
