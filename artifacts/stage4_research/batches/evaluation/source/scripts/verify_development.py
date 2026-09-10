#!/usr/bin/env python3
"""Replay and summarize the fixed saved development batch without inference."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from overseeing.development_analysis import analyze_development

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("folder")
args = parser.parse_args()
print(json.dumps(analyze_development(args.folder), indent=2, sort_keys=True))
