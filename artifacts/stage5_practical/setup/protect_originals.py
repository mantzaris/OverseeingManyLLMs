import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
root=Path('artifacts/stage5_practical');manifest=json.loads((root/'publication_redactions.json').read_text());rows=[]
for r in manifest['files']:
 path=root/r['path'];assert path.resolve().is_relative_to(root.resolve())
 assert hashlib.sha256(path.read_bytes()).hexdigest()==r['original_sha256']
 path.chmod(0o600);rows.append(dict(path=r['path'],original_sha256=r['original_sha256'],mode='0600'))
record=dict(verified_utc=datetime.now(timezone.utc).isoformat(),original_files=len(rows),files=rows,
 purpose='Preserve exact raw originals privately on the pod; public Git copies are separately redacted. No content changed.')
(root/'original_evidence_permissions.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'original_files':len(rows),'contents_unchanged':True,'mode':'0600'}))
