#!/usr/bin/env python3
"""Audit all saved Stage 3 evidence and replay completed traces without inference."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from overseeing.competition_analysis import analyze_competition
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('folder')
args = parser.parse_args()
print(json.dumps(analyze_competition(args.folder), indent=2, sort_keys=True))
