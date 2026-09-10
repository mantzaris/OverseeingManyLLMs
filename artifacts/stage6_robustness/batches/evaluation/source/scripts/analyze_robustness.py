#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.retail.robustness_analysis import analyze
p=argparse.ArgumentParser();p.add_argument('cohort',choices=['fresh','post_hoc_stage5']);args=p.parse_args()
print(json.dumps(analyze(args.cohort),indent=2))
