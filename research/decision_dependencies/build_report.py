"""Build a standalone research report while leaving the submission untouched."""
import re
import subprocess
from pathlib import Path

def build():
    here=Path(__file__).resolve().parent
    source=(here/'REPORT.md').read_text()
    # Keep the explanatory caption with the figure rather than as a separate
    # paragraph that LaTeX can leave on another page.
    def caption(match):
        text=re.sub(r'\s+',' ',match.group(2)).strip()
        return '!['+text+']('+match.group(1)+')\n'
    source=re.sub(r'!\[[^\]]*\]\(([^)]+)\)\n\n\*Figure \d+\.\s+(.*?)\*\n',caption,source,flags=re.S)
    source=re.sub(r'!\[[^\]]*\]\(([^)]+)\)\n\n\*Interface screenshot\.\s+(.*?)\*\n',caption,source,flags=re.S)
    source=source.replace('# Results\n','\\clearpage\n\n# Results\n')
    # Use vector plots in the PDF. Browser screenshots remain raster evidence.
    source=re.sub(r'(../../artifacts/decision_dependencies/publication/[^)]+)\.png',r'\1.pdf',source)
    result=subprocess.run(['pandoc','-f','markdown','--standalone','--pdf-engine=pdflatex',
        '-V','geometry:margin=0.8in','-V','fontsize=10pt','-V','colorlinks=true',
        '-V','linkcolor=teal','-V','urlcolor=teal','-V','papersize=a4',
        '--include-in-header=report_header.tex',
        '-o','REPORT.pdf'],input=source,text=True,cwd=str(here),capture_output=True)
    if result.stdout:print(result.stdout)
    if result.stderr:print(result.stderr)
    result.check_returncode()
    print('Built',here/'REPORT.pdf')

if __name__=='__main__':build()
