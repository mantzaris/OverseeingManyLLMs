#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.retail.robustness_execution import declare,run
p=argparse.ArgumentParser();p.add_argument('operation',choices=['declare','run']);args=p.parse_args()
if args.operation=='declare':
    d=declare();print(json.dumps({k:d[k] for k in ['declaration_hash','workflow_count','max_scheduled_calls','max_attempts','planned_policy_episodes']},indent=2))
else:run()
