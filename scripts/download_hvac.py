#!/usr/bin/env python3
"""Download only the pinned measured CSVs, outside Git, and verify checksums."""
import argparse,hashlib,json,urllib.request
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();dest=Path(a.out);dest.mkdir(parents=True,exist_ok=True)
root=Path(__file__).resolve().parents[1]/'artifacts/stage7_empirical';meta=json.loads((root/'sources/figshare_metadata.json').read_text());expected={r['file']:r for r in json.loads((root/'source_checksums.json').read_text())}
for entry in meta['files']:
    if entry['name'] not in expected:continue
    target=dest/entry['name']
    if not target.exists():
        with urllib.request.urlopen(entry['download_url'],timeout=60) as response:target.write_bytes(response.read())
    assert hashlib.sha256(target.read_bytes()).hexdigest()==expected[entry['name']]['sha256']
    print(target,'verified')
