"""Optional independent check against the pinned upstream archive (not inference)."""
import argparse,hashlib,json,urllib.request,zipfile
from pathlib import Path
from .common import ART,read,canonical,write_json
from .data import state

def verify_source(archive,download=False):
    archive=Path(archive);provenance=read(ART/'data/upstream_provenance.json');source=next(x for x in provenance['downloads'] if x['path'].endswith('.zip'))
    if not archive.exists():
        if not download:raise FileNotFoundError('Pass --download or provide the pinned archive')
        archive.parent.mkdir(parents=True,exist_ok=True);urllib.request.urlretrieve(source['url'],str(archive))
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==source['sha256']
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();prefix=next(n[:-9] for n in names if n.endswith('/data.json'))
        raw=json.loads(z.read(prefix+'data.json'))
        splits={s:set(z.read(prefix+s+'ListFile.json').decode().split()) for s in ['val','test']}
        gold={r['id']:r for r in read(ART/'data/evaluation_only.json')}
        current=read(ART/'data/public.json')
        for c in current:
            assert c['id'] in splits['val' if c['split']=='development' else 'test']
            log=raw[c['id']]['log'];messages=[dict(turn=i,role='user' if i%2==0 else 'assistant',text=t['text']) for i,t in enumerate(log)]
            assert messages==c['messages']
            target,proof=state(log,len(log)-1);assert target==gold[c['id']]['target']
            assert proof==gold[c['id']]['lexical_support_turns']
            assert hashlib.sha256(canonical(log).encode()).hexdigest()==gold[c['id']]['dialogue_sha256']
        for domain in ['hotel','restaurant','attraction']:
            assert json.loads(z.read(prefix+domain+'_db.json'))==read(ART/'data'/(domain+'_db.json'))
    result=dict(status='passed',selected_dialogues=len(current),evaluation_dialogues=sum(c['split']=='evaluation' for c in current),database_files=3,archive_sha256=source['sha256'],new_generations=0)
    print(json.dumps(result,indent=2));return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive',default='/tmp/clarification-source/MULTIWOZ2.4.zip');p.add_argument('--download',action='store_true');a=p.parse_args();verify_source(a.archive,a.download)
