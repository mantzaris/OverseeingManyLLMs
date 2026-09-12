"""Check the handoff's frozen pilot bytes. No generation or scenario sweep."""
import hashlib
import json
from pathlib import Path

from research.oversight_workflow.common import ROOT, digest, read

ART = ROOT / 'artifacts/oversight_workflow/author_handoff'


def verify():
    frozen = read(ART / 'pilot_handoff_freeze.json')
    prior_path = ROOT / frozen['prior_freeze']
    if hashlib.sha256(prior_path.read_bytes()).hexdigest() != frozen['prior_freeze_sha256']:
        raise ValueError('Historical preparation freeze changed')
    prior_files = read(prior_path)['files']
    for relative in prior_files.keys() & frozen['files'].keys():
        if prior_files[relative] != frozen['files'][relative]:
            raise ValueError('Handoff conflicts with historical freeze: ' + relative)
    all_files = {**prior_files, **frozen['files']}
    for relative, expected in all_files.items():
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
            raise ValueError('Pilot handoff differs: ' + relative)
    manifest = read(ROOT / 'research/oversight_workflow/pilot/manifest.json')
    declared = manifest.pop('manifest_sha256')
    if declared != frozen['manifest_sha256'] or digest(manifest) != declared:
        raise ValueError('Pilot manifest digest mismatch')
    return dict(status='verified', version=frozen['handoff_version'],
                code_commit=frozen['pilot_code_commit'], manifest_sha256=declared,
                frozen_files=len(all_files), inference_calls=0, scenario_replays=0,
                limit='Byte/version check, not human-study authorization or evidence')


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
