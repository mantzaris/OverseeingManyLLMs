"""Reuse the bounded GPU transport; serialize only inference, never the review UI."""
import importlib.util
import threading
from .common import ROOT, ART

_spec = importlib.util.spec_from_file_location(
    'research.adaptive_correction_transfer._workflow_client',
    ROOT / 'research/adaptive_correction_transfer/client.py')
client = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(client)
client.ART = ART
_gpu_lock = threading.Lock()

def generate(call_id, messages, seed, max_tokens=230):
    with _gpu_lock:
        raw = client.generate(call_id, messages, seed, max_tokens)
    return client.parsed(raw), raw
