"""Paths and deterministic serialization for this experiment only."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'artifacts/verification_escalation'

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))

def write_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n')

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def read(path):
    return json.loads(Path(path).read_text())
