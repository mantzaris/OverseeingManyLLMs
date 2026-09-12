"""Manuscript table generated directly from saved corrected results."""
from .common import ART,ROOT,read

def run():
 data=read(ART/'repair/analysis/summary.json');names=[('recovery_completion','Recovery + completion'),('recovery_depth2','Recovery + depth two'),('verification','Verification'),('full_context','Full-context proposal'),('matched_checking','Matched checking'),('no_coverage_guard','No coverage guard')]
 lines=[r'\begin{tabular}{lrrrrr}',r'\toprule',r'Method & Answers & Match & Mismatch & Unfinished & Loss \\',r'\midrule']
 for m,label in names:
  r=next(x for x in data if x['method']==m and x['budget']==1 and x['condition']=='generated');lines.append(label+' & '+' & '.join(str(int(r[k])) for k in ['questions','correct','wrong','unfinished','loss'])+r' \\')
 lines += [r'\bottomrule',r'\end{tabular}']
 (ROOT/'paper/verification_escalation/results_table.tex').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':run()
