#!/usr/bin/env python3
"""Explicit Stage 4 declarations/execution; historical commands retain their limits."""
import argparse,json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('command',choices=['prepare-diagnostics','diagnostics','prepare-pilot','prepare-branch','prepare-evaluation','run-batch'])
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
    from overseeing.research_plan import development_plan,objective_branch_plan,selected_evaluation_plan
    plans={'prepare-pilot':(development_plan,'Declared initial risk and capacity pilots, no evaluation outcomes available'),
           'prepare-branch':(objective_branch_plan,'Branch A selected before evaluation: pilot search versus EDF showed lower cost with more incorrect closures; one fixed lambda grid 0/4/8'),
           'prepare-evaluation':(selected_evaluation_plan,'Full user-target core prefixes and one fixed objective grid; development evidence and forecast recorded in evaluation_freeze.json')}
    if args.command in plans:
        plan,reason=plans[args.command];result=prepare_batch(args.root,args.batch,plan(),reason)
    else:result=run_batch(args.root,args.batch,args.server_pid,args.server_log)
print(json.dumps(result,indent=2,sort_keys=True))
raise SystemExit(0 if result.get('status') in ('declared','completed') else 2)
