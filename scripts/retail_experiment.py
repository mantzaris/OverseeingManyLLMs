#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.retail.execution import declare,run

parser=argparse.ArgumentParser(description='Declare or execute bounded Stage 5 GPU retail preparation')
parser.add_argument('operation',choices=['declare','run'])
parser.add_argument('name');parser.add_argument('--root',default='artifacts/stage5_practical')
parser.add_argument('--partition',choices=['development','evaluation'],default='development')
parser.add_argument('--bundles',type=int,default=8);parser.add_argument('--replicates',type=int,nargs='+',default=[0,1,2])
parser.add_argument('--estimator');args=parser.parse_args()
if args.operation=='declare':
    r=declare(args.root,args.name,args.partition,args.bundles,args.replicates,args.estimator)
    print(json.dumps({k:r[k] for k in ('name','workflow_count','max_scheduled_calls','declaration_hash')}))
else:run(args.root,args.name)
