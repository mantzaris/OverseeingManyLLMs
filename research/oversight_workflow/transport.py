"""Reuse the bounded GPU transport; serialize only inference, never the review UI."""
import importlib.util
import threading
from .common import ROOT, ART, read

_spec = importlib.util.spec_from_file_location(
    'research.adaptive_correction_transfer._workflow_client',
    ROOT / 'research/adaptive_correction_transfer/client.py')
client = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(client)
client.ART = ART
_gpu_lock = threading.Lock()

def generate(call_id, messages, seed, max_tokens=230):
    with _gpu_lock:
        ledger=ART/'resource_ledger.json'
        if ledger.exists() and read(ledger).get('final') and not (ART/'raw'/(call_id+'.json')).exists():
            raise RuntimeError('This stage is closed. Fresh inference requires a new authorized namespace.')
        raw = client.generate(call_id, messages, seed, max_tokens)
    return client.parsed(raw), raw
