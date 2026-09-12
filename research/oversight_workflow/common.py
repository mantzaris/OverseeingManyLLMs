from pathlib import Path
from research.adaptive_correction_transfer.common import canonical, digest, read as _read, write

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'artifacts/oversight_workflow'


def read(path):
    """Read compact stage evidence, retaining ordinary historical JSON support."""
    import gzip,json
    p=Path(path)
    if not p.exists() and Path(str(p)+'.gz').exists():p=Path(str(p)+'.gz')
    if p.suffix=='.gz':
        with gzip.open(p,'rt',encoding='utf-8') as f:return json.load(f)
    return _read(p)
