#!/usr/bin/env python3
import argparse,json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.retail.analysis import audit_preparation,fit,score
parser=argparse.ArgumentParser(description='Audit, calibrate and score Stage 5 without inference')
parser.add_argument('operation',choices=['audit','fit','score']);parser.add_argument('batches',nargs='+')
parser.add_argument('--root',default='artifacts/stage5_practical');args=parser.parse_args()
if args.operation=='fit':result=fit(args.root,args.batches)
elif args.operation=='audit':result=[audit_preparation(args.root,b) for b in args.batches]
else:result=[score(args.root,b) for b in args.batches]
print(json.dumps(result,indent=2,sort_keys=True))
