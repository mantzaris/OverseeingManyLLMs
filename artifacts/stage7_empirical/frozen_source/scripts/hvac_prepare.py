#!/usr/bin/env python3
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.hvac import prepare,save
root=Path('artifacts/stage7_empirical');cases,sources=prepare(sys.argv[1])
save(root/'cases.json',cases);save(root/'source_checksums.json',sources)
for split in ('development','evaluation'):
    selected=[c for c in cases if c['split']==split]
    save(root/(split+'_public.json'),[dict(case_id=c['case_id'],public=c['public']) for c in selected])
    print(split,len(selected),'tasks',len({c['run_id'] for c in selected}),'whole experimental days')
