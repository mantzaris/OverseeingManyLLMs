"""Evaluator-only annotations. Never imported by the live desk or task workers."""
from .common import ART,read,write,digest

def labels():
    data=read(ART/'offline_annotations.json')
    if digest(data['annotations'])!=data['annotations_sha256']:raise ValueError('Offline annotation projection hash mismatch')
    return data['annotations']

def export():
    from research.adaptive_correction_transfer.data import annotations
    m=read(ART/'frozen/manifest.json');all_labels=annotations('test_gold')
    selected={c['id']:{q['id']:all_labels[c['id']][q['id']] for q in c['questions']} for c in m['contexts']}
    write(ART/'offline_annotations.json',dict(kind='Evaluator-only compact projection, created after frozen generation. Not an agent or UI input.',
        split='test_gold',source_file_sha256='c4d08418359c1d76468dec420ee748a37f48c06b63cb8ec2766f19d5d314b597',
        annotations_sha256=digest(selected),annotations=selected))

if __name__=='__main__':export()
