#!/usr/bin/env python3
"""Verify compiled ICAART files and retain inspectable formatting evidence."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.io import write_json,utc_now
root=Path('artifacts/stage6_robustness');provenance=json.loads((root/'sources/template_provenance.json').read_text())
for name,h in provenance['files'].items():assert hashlib.sha256((Path('paper/template')/name).read_bytes()).hexdigest()==h,name
files={}
for stem in ('main','supplement'):
    pdf=Path('paper')/(stem+'.pdf');tex=pdf.with_suffix('.tex').read_text();log=pdf.with_suffix('.log').read_text(encoding='latin-1')
    info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
    pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
    assert 'A4' in info and re.search(r'^Author:\s*$',info,re.M)
    text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
    (root/(stem+'_rendered_text.txt')).write_text(text)
    characters=sum(not c.isspace() for c in text)
    if stem=='main':assert 10000<=characters<=50000 and pages<=12,(characters,pages)
    abstract=re.search(r'\\abstract\{(.*?)\}\n',tex,re.S).group(1)
    words=len(re.sub(r'\\[A-Za-z]+','',abstract).split())
    assert 70<=words<=200,(stem,words)
    assert 'Overfull' not in log and 'undefined' not in log.lower() and 'multiply defined' not in log.lower()
    fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True)
    assert all(row.split()[-5]=='yes' for row in fonts.splitlines()[2:] if row.strip())
    assert './template/article.cls' in log and './template/SCITEPRESS.sty' in log
    assert '\\draftcredit' in tex and 'AI ASSISTANCE' in tex
    assert tex.count('\\draftcredit')==len(re.findall(r'\\section\{',tex))
    assert not any(s in text.lower() for s in ['placeholder','todo:','resort','/home/'])
    (root/(stem+'_fonts.txt')).write_text(fonts)
    files[stem]=dict(path=str(pdf),pages=pages,non_whitespace_extracted_characters=characters,abstract_space_delimited_words=words,
        sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),all_fonts_embedded=True,overfull_boxes=0,undefined_citations_or_references=0,anonymous_pdf_author_metadata=True,official_class_and_style_loaded=True)
result=dict(status='verified',verified_utc=utc_now(),edition='ICAART 2027',files=files,unchanged_template_files=len(provenance['files']),
    character_count_method='pdftotext -layout, counting all non-whitespace characters including extracted figure labels and references; mathematical glyph extraction can differ slightly from venue tooling.',
    limits='Regular review 10000-50000 non-whitespace characters. Ordinary accepted full paper 12 pages; these are distinct rules. No official regular-supplement page/upload allowance is inferred.',
    build_command='bash paper/build.sh',figure_method='Vector PDF plots of saved measurements; no AI-generated raster illustrations.',
    human_submission_decisions=['Authorship and responsibility','Funding/conflicts and submission declarations','Anonymous AI-disclosure placement','Regular-paper supplementary upload permission'])
write_json(root/'manuscript_audit.json',result);print(json.dumps(result,indent=2))
