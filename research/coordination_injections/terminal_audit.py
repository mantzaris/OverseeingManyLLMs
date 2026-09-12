"""Post hoc leaf-artifact audit, not a replacement trajectory or policy score."""
from .common import ART,read,write,digest
from .normalize import normalize
from .contracts import contract
from .controller import build_artifact,upstream_state,public_check
from .evaluate import artifact_correct

def audit(output=None):
 projects={p['id']:p for p in read(ART/'frozen/manifest.json')['evaluation']};rows=[]
 for p in sorted((ART/'evaluation/frozen').glob('*.json')):
  if p.name.endswith(('summary.json','initial.json')):continue
  r=read(p)
  if r['method']=='pipeline':continue
  a=r['artifacts'].get('report',{})
  if a.get('accepted'):continue
  project=projects[r['project_id']];proposal=a.get('proposal');normalized=normalize(proposal,'report');changed=normalized!=proposal
  hypothetical=build_artifact('report',normalized,contract(project,'report',1),upstream_state('report',r['artifacts']),a);issues=public_check('report',hypothetical,contract(project,'report',1),r['artifacts'],[])
  rows.append(dict(project_id=r['project_id'],rep=r['rep'],method=r['method'],original_path=str(p.relative_to(ART)),explicit_envelope_recognized=changed,public_checks_pass=not issues,reference_matches=artifact_correct(project,1,'report',hypothetical),normalized_proposal=normalized,remaining_issues=issues))
 result=dict(kind='Post hoc static reinterpretation of final leaf reports. No new LLM calls and no replay of downstream counterfactual prompts. Original policy scores are unchanged.',unfinished_reports=len(rows),recognized=sum(r['explicit_envelope_recognized'] for r in rows),locally_valid_after_normalization=sum(r['public_checks_pass'] and r['reference_matches'] for r in rows),rows=rows)
 write(output or ART/'analysis/terminal_envelope_audit.json',result);return result
if __name__=='__main__':
 d=audit();print({k:v for k,v in d.items() if k!='rows'})
