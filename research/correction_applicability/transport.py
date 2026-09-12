"""Reuse the historical bounded transport in an isolated stage-local module instance."""
import importlib.util
from .common import ROOT,ART
path=ROOT/'research/adaptive_correction_transfer/client.py'
spec=importlib.util.spec_from_file_location('research.adaptive_correction_transfer._applicability_client',path)
client=importlib.util.module_from_spec(spec);spec.loader.exec_module(client);client.ART=ART
parsed=client.parsed
http=client.http
MODEL=client.MODEL
REVISION=client.REVISION

def request(call_id,messages,seed,max_tokens=440):
 raw=client.generate(call_id,messages,seed,max_tokens)
 usage=dict(call_id=call_id,request_sha256=raw['request_sha256'],status=raw['status'],attempts=len(raw['attempts']),tokens=sum(a.get('response',{}).get('usage',{}).get('total_tokens',0) for a in raw['attempts']),seconds=sum(a['elapsed_seconds'] for a in raw['attempts']))
 return parsed(raw),usage
