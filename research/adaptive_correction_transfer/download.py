"""Restore the exact official source release used for collection, with hash checks."""
import subprocess,hashlib
from .data import SOURCE,REVISION
from .common import ART,read
if __name__=='__main__':
 if not SOURCE.exists():
  SOURCE.parent.mkdir(parents=True,exist_ok=True);subprocess.run(['git','clone','https://github.com/NExTplusplus/tat-qa',str(SOURCE)],check=True);subprocess.run(['git','checkout',REVISION],cwd=SOURCE,check=True)
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=SOURCE,text=True).strip()
 if head!=REVISION:raise RuntimeError('Existing source checkout has a different revision; preserve it and use the documented path separately.')
 for f in read(ART/'provenance.json')['files']:
  p=SOURCE/f['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],f['path']
 print('Pinned official source and all declared file hashes verified:',SOURCE)
