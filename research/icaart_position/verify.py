"""Verify the single-file manuscript, preserved evidence, and isolated compilation."""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PAPER=ROOT/'paper/icaart_position'
ART=ROOT/'artifacts/icaart_position'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def command(args,cwd=None):return subprocess.check_output(args,cwd=cwd,stderr=subprocess.STDOUT).decode()


def verify():
    preserved=json.loads((ART/'preservation.json').read_text())
    if 'files' in preserved:preserved=preserved['files']
    for path,expected in preserved.items():
        assert sha(ROOT/path)==expected, 'Historical file changed: '+path
    template=json.loads((ART/'sources/template.json').read_text())
    # Exact official bytes; do not regenerate these hashes to accept a modification.
    expected={'article.cls':'23e48b9a27539b6589503b6b5c5ff1451b58edfb245a0fa4c5847bb94392d32c',
              'SCITEPRESS.sty':'d4a8482e5b2772a279b881012bedd813023f3c614287e02d5c648497ade3bf14',
              'apalike.sty':'183bdccc3608e9db948dbd1cdffec3e2a476650dad223c7a3294325371fc0339'}
    for p,h in expected.items():assert sha(PAPER/p)==h,p
    tex=(PAPER/'main.tex').read_text()
    assert len(list(PAPER.glob('*.tex')))==1
    assert not re.search(r'\\(?:input|include|subfile|import|bibliography|externaldocument)\s*[\[{]',tex)
    assert not re.search(r'\\(?:appendix|includeonly|subimport|IfFileExists)\b',tex)
    assert not re.search(r'supplement|appendix',tex,re.I)
    assert r'\begin{thebibliography}' in tex
    assert not re.search(r'\\(?:geometry|setstretch|fontsize|enlargethispage)\b',tex)
    assert set(re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',tex))=={'workflow.pdf','reference.pdf','orientation.pdf','tradeoffs.pdf'}
    with tempfile.TemporaryDirectory(prefix='icaart-isolated-',dir='/tmp') as tmp:
        dest=Path(tmp);(dest/'figures').mkdir()
        for p in ['main.tex']+list(expected):shutil.copy2(PAPER/p,dest/p)
        for p in (PAPER/'figures').glob('*.pdf'):shutil.copy2(p,dest/'figures'/p.name)
        for _ in range(2):command(['pdflatex','-interaction=nonstopmode','-halt-on-error','-recorder','main.tex'],dest)
        log=(dest/'main.log').read_text()
        assert not re.search(r'Overfull|undefined|Rerun to get|Fatal error',log), 'LaTeX warning requiring resolution'
        info=command(['pdfinfo',str(dest/'main.pdf')]);pages=int(re.search(r'Pages:\s+(\d+)',info)[1]);assert pages==8
        standalone_text=command(['pdftotext','-layout',str(dest/'main.pdf'),'-'])
        actual_text=command(['pdftotext','-layout',str(PAPER/'main.pdf'),'-'])
        assert standalone_text==actual_text,'Isolated build differs from delivered PDF'
        chars=len(''.join(standalone_text.split()));assert 8000<=chars<=40000
        dependencies=(dest/'main.fls').read_text()
        assert str(ROOT) not in dependencies,'Repository dependency in isolated build'
        (ART/'isolated-build.log').write_text('\n'.join(line.rstrip() for line in log.splitlines()).rstrip()+'\n')
        for p in (dest/'figures').glob('*'):assert p.suffix=='.pdf'
        result=dict(record_kind='publication_verification',pages=pages,nonwhitespace_pdf_characters=chars,
            historical_files_unchanged=len(preserved),official_template_hashes=expected,
            isolated_inputs=['main.tex']+list(expected)+['figures/'+x.name for x in sorted((PAPER/'figures').glob('*.pdf'))],
            no_repository_dependencies=True,isolated_pdf_text_identical=True,authored_tex_files=1,embedded_bibliography=True,
            supplementary_document_required=False,overfull_boxes=0,undefined_references=0,
            main_tex_sha256=sha(PAPER/'main.tex'),main_pdf_sha256=sha(PAPER/'main.pdf'))
    (ART/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':verify()
