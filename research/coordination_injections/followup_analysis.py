"""Exploratory parser sensitivity summaries and route-equivalence audit."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from .common import ART,read,write,digest,stable
from .analyze import summarize,csv_write
from .plot import COLORS,NAMES,SHORT,save

def analyze(output=None,figure_output=None):
 root=ART/'parser_followup';out=Path(output) if output else root/'analysis';out.mkdir(parents=True,exist_ok=True);rows=read(root/'rows.json');summary=summarize(rows);write(out/'summary.json',summary);csv_write(out/'episodes.csv',rows);csv_write(out/'policy_summary.csv',summary)
 projects=read(root/'manifest.json')['projects'];audit=[]
 for pid in projects:
  a=read(root/'runs'/(pid+'_r0_targeted.json'));b=read(root/'runs'/(pid+'_r0_global_packet.json'))
  ah=[c['request_sha256'] for c in a['calls']];bh=[c['request_sha256'] for c in b['calls']]
  audit.append(dict(project_id=pid,same_call_request_sequence=ah==bh,same_recipient_sequence=[r['role'] for r in a['routes']]==[r['role'] for r in b['routes']],same_artifact_payloads=digest(stable(a['artifacts']))==digest(stable(b['artifacts'])),targeted_checks=len(a['checks']),global_checks=len(b['checks'])))
 write(out/'routing_audit.json',dict(projects=len(audit),identical_request_sequences=sum(r['same_call_request_sequence'] for r in audit),identical_recipient_sequences=sum(r['same_recipient_sequence'] for r in audit),rows=audit,interpretation='For this valid-start, scope-complete graph, global invalidity and changed-contract routing select the same roles. An extra repeated inspect call in the implementation is not a new algorithmic advantage.'))
 fig,axs=plt.subplots(1,3,figsize=(8.4,3.9));methods=['shared_state','broadcast','targeted','sparse','global_packet'];primary=read(ART/'analysis/primary_rows.json')
 for i,m in enumerate(methods):
  rr=[r for r in rows if r['method']==m];strict=[r for r in primary if r['method']==m and r['rep']==0]
  if m=='global_packet':strict=[r for r in read(ART/'analysis/secondary_rows.json') if r['method']==m]
  axs[0].bar(i-.17,100*np.mean([r['project_correct'] for r in strict]),width=.32,color=COLORS[m],alpha=.35);axs[0].bar(i+.17,100*np.mean([r['project_correct'] for r in rr]),width=.32,color=COLORS[m]);axs[1].bar(i,np.mean([r['calls'] for r in rr]),color=COLORS[m]);axs[2].bar(i,np.mean([r['unnecessary_modifications'] for r in rr]),color=COLORS[m])
 for ax in axs:ax.set_xticks(range(5));ax.set_xticklabels([SHORT[m] for m in methods],rotation=30,ha='right')
 axs[0].set(ylabel='Structured projects correct (%)',ylim=(0,108),title='Strict / compatible parser');axs[1].set(ylabel='LLM calls per project',title='Calls after normalization');axs[2].set(ylabel='Unchanged-scope artifact rewrites',title='Unaffected rewrites')
 figout=Path(figure_output) if figure_output else ART/'figures';figout.mkdir(parents=True,exist_ok=True)
 save(fig,figout,'parser_followup','Separately declared post hoc sensitivity on the same sixteen already inspected projects, replica 0, in eight monthly blocks. Solid bars use 250 fresh GPU calls, with the same tools, instructions, scopes and guards plus explicit equivalent-envelope normalization. Faint bars are the matched replica-0 strict-parser originals. This is not new held-out evidence. Targeted and the same-packet global check have identical request sequences on all sixteen runs; no independent routing advantage can be inferred. No method has an accepted numerical error; the remaining shared-state failure uses an unsupported parameters alias. The zero-inference pipeline remains perfect on these contracts.')
 return summary
if __name__=='__main__':
 for r in analyze():print(r['method'],r['project_correct_total'],r['runs'],r['calls_total'])
