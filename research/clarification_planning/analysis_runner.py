"""Serialization-only compatibility wrapper around the unchanged frozen analysis.

NumPy boolean sums produce int64 counters. Original CSV analysis completes, but
its final JSON writer rejects those scalars. Convert scalar types at serialization
only; statistical computations and CSV tables remain byte-for-byte unchanged.
"""
import argparse
import json
from types import SimpleNamespace
from unittest.mock import patch
from . import analyze
from .common import write_json

def safe(value):
    return json.loads(json.dumps(value,default=lambda x:x.item()))

def run(root=None):
    proxy=SimpleNamespace(dumps=lambda value,**kw:json.dumps(safe(value),**kw),loads=json.loads)
    with patch.object(analyze,'write_json',lambda p,v:write_json(p,safe(v))),patch.object(analyze,'json',proxy):
        analyze.analyze(root)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root');run(p.parse_args().root)
