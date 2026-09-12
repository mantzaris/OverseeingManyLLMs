"""Download source from its author host and reconstruct excluded source inputs."""
import base64,hashlib,json,urllib.request,zipfile,tempfile
from pathlib import Path
from .common import ART,read

def source():
    from . import data
    manifest=read(ART/'provenance.json');archive=Path('/tmp/verification-sources/ambrosia.zip')
    if not archive.exists():
        archive.parent.mkdir(parents=True,exist_ok=True)
        # This is the public password printed on the author's dataset website,
        # not a personal credential or a bypass of their access requirements.
        public_auth=base64.b64encode(b'pOk0Kfrn1oq96UR:AM8R0S1A').decode()
        request=urllib.request.Request('https://datasync.ed.ac.uk/public.php/webdav/',headers={'Authorization':'Basic '+public_auth})
        with urllib.request.urlopen(request,timeout=90) as response:archive.write_bytes(response.read())
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=manifest['dataset']['archive_sha256']:raise ValueError('Changed source archive')
    dest=archive.parent/'ambrosia'
    if not data.SOURCE.exists():
        with zipfile.ZipFile(archive) as z:
            for name in z.namelist():
                if not str((dest/name).resolve()).startswith(str(dest.resolve())+'/'):raise ValueError('Invalid archive path')
            z.extractall(dest)
    if hashlib.sha256(data.SOURCE.read_bytes()).hexdigest()!=manifest['dataset']['csv_sha256']:raise ValueError('Changed source CSV')
    # Rebuild into a temporary root before checking against the frozen selection.
    old=data.ART
    with tempfile.TemporaryDirectory(prefix='verification-source-') as tmp:
        data.ART=Path(tmp)
        try:data.select()
        finally:data.ART=old
        b=(Path(tmp)/'private/cases.json').read_bytes()
        if hashlib.sha256(b).hexdigest()!=read(ART/'frozen.json')['cases_hash']:raise ValueError('Source reconstruction differs')
        if (Path(tmp)/'split_manifest.json').read_bytes()!=(ART/'split_manifest.json').read_bytes():raise ValueError('Split reconstruction differs')
        target=ART/'private/cases.json'
        if target.exists() and target.read_bytes()!=b:raise ValueError('Existing source cases differ')
        if not target.exists():target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
    return {'source':'verified','databases':57,'evaluation':48,'development':9,'raw_prompts':'Kept locally, excluded from Git at author request'}

def repaired_source():
    """Reconstruct the disjoint, ordering-correct follow-up without generation."""
    source()
    from . import repair_data
    old=repair_data.ART
    with tempfile.TemporaryDirectory(prefix='verification-repaired-source-') as tmp:
        repair_data.ART=Path(tmp)
        try:repair_data.select()
        finally:repair_data.ART=old
        b=(Path(tmp)/'private/cases.json').read_bytes()
        if hashlib.sha256(b).hexdigest()!=read(old/'frozen.json')['cases_hash']:raise ValueError('Repaired source reconstruction differs')
        if (Path(tmp)/'split_manifest.json').read_bytes()!=(old/'split_manifest.json').read_bytes():raise ValueError('Repaired split differs')
        target=old/'private/cases.json'
        if target.exists() and target.read_bytes()!=b:raise ValueError('Existing repaired cases differ')
        if not target.exists():target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
    return {'source':'verified','fresh_databases':24,'excluded_prior_databases':57}
if __name__=='__main__':print(json.dumps(source(),indent=2))
