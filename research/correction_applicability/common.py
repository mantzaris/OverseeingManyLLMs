from pathlib import Path
from research.adaptive_correction_transfer.common import read,write,digest,canonical,stable
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifacts/correction_applicability'
OLD=ROOT/'artifacts/adaptive_correction_transfer'
