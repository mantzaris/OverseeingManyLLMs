"""Replay logged local UI actions, including explicit server restarts."""
import argparse,hashlib,json,tempfile
from pathlib import Path
from .prototype.server import Session

def verify(path):
    rows=[json.loads(x) for x in Path(path).read_text().splitlines()]
    assert rows and rows[0]['action']=='server_initialized','Use a lifecycle-aware log; legacy demonstration is retained separately.'
    with tempfile.TemporaryDirectory() as d:
        s=None
        for i,r in enumerate(rows):
            if r['action']=='server_initialized':s=Session(Path(d)/'replayed.jsonl')
            else:
                succeeded=True
                try:s.action(r['payload'])
                except (ValueError,KeyError,TypeError):succeeded=False
                assert succeeded==r['ok'],('action outcome mismatch',i)
            digest=hashlib.sha256(json.dumps(s.state(),sort_keys=True).encode()).hexdigest()
            assert digest==r['public_state_sha256'],('public state mismatch',i)
            assert s.controller.now==r['simulated_tick']
    return dict(status='verified',events=len(rows),human_participants=0,
                basis='Recorded actions reproduce public state exactly. Wall-clock response times are retained observations of a scripted browser, not simulated or participant measurements.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('path');a=p.parse_args();print(json.dumps(verify(a.path),indent=2))
