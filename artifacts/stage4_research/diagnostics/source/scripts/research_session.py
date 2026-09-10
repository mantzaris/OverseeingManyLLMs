#!/usr/bin/env python3
"""Explicit Stage 4 declarations/execution; historical commands retain their limits."""
import argparse,json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('command',choices=['prepare-diagnostics','diagnostics'])
parser.add_argument('--root',default='artifacts/stage4_research')
parser.add_argument('--server-pid',type=int,default=7338)
parser.add_argument('--server-log',default='artifacts/stage1_gpu_live/rtx6000_ada_20260910T002404Z/setup/server.log')
args=parser.parse_args()
from overseeing.research_diagnostics import prepare_diagnostics,run_diagnostics
result=prepare_diagnostics(args.root) if args.command=='prepare-diagnostics' else run_diagnostics(args.root,args.server_pid,args.server_log)
print(json.dumps(result,indent=2,sort_keys=True))
raise SystemExit(0 if result.get('status') in ('declared','completed') else 2)
