#!/usr/bin/env python3
"""Audit/replay saved batches, then compute fixed scenario-paired summaries."""
import argparse,json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from overseeing.research_analysis import audit_batch,summarize_batches
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root',default='artifacts/stage4_research')
parser.add_argument('--batches',nargs='+',required=True)
parser.add_argument('--label',required=True)
parser.add_argument('--summary-only',action='store_true')
args=parser.parse_args()
if not args.summary_only:
    for name in args.batches:print(json.dumps(audit_batch(args.root,name),sort_keys=True),flush=True)
result=summarize_batches(args.root,args.batches,args.label)
print(json.dumps({k:v for k,v in result.items() if k!='policy_outcomes'},indent=2,sort_keys=True))
