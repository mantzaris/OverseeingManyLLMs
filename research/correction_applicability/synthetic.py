"""Authored mechanism boundaries; no generated errors or empirical prevalence claims."""
import copy,random
from .tests import C,Q1,Q2,Q3,answer,setup,q
from .patches import propose,infer,apply_to_state
from .representation import parse,version
from .common import ART,write
from .analyze import csvout

def run_all():
 cases=[]
 for seed in range(32):
  old,correct,f,p=setup();r=answer(['T1C2','T1C3'],'x1-x0',periods=['2018','2017'])
  # Same public structure, varied controlled output perturbation. Reference numeric values stay source-defined.
  r['answer']=[str(-273+random.Random(951000+seed).choice([0,1,-1]))]
  scenarios=[('shared_operand_order',C,Q2,r,p,273.,True)]
  x=answer(['T1C2','T1C3'],'x0-x1',periods=['2018','2017']);x['answer']=['273'];scenarios.append(('already_correct_operation',C,Q2,x,p,273.,False))
  f_old=answer(['T1C2'],'x0','lookup',['2018']);f_new=answer(['T1C1'],'x0','lookup',['2019']);fp=infer(C,q('q1','What are research expenses in 2019?'),f_old,f_new,dict(answer='6577',scale='million'));scenarios.append(('local_fact_wrong_period',C,Q2,x,fp,273.,False))
  y=answer(['T2C3'],'x0','lookup',['2017'],metric='sales');y['answer']=['9184'];scenarios.append(('unrelated_metric',C,Q3,y,p,9184.,False))
  z=copy.deepcopy(r);z['rep']=None;scenarios.append(('missing_dependency',C,Q2,z,p,273.,False))
  cc=copy.deepcopy(C);cc['table'][1][2]='7000';scenarios.append(('source_revised',cc,Q2,r,p,941.,False))
  bad=copy.deepcopy(p);bad['to_expression']='x0/0';scenarios.append(('failed_computation',C,Q2,r,bad,273.,False))
  ratioq=q('q2','What is the percentage change in research expenses between 2017 and 2018?');ratio=answer(['T1C2','T1C3'],'x0/x1','ratio',['2018','2017'],scale='percent',unit='dimensionless');ratio['answer']=['1.05'];scenarios.append(('different_percentage_operation',C,ratioq,ratio,p,4.51,False))
  s_old=answer(['T1C1'],'x0','lookup',['2019'],scale='');s_new=answer(['T1C1'],'x0','lookup',['2019'],scale='million');sp=infer(C,q('q1','What are research expenses in 2019?'),s_old,s_new,dict(answer='6577',scale='million'));recipient=answer(['T1C2'],'x0','lookup',['2018'],scale='');recipient['answer']=['6332'];scenarios.append(('shared_amount_scale',C,q('q2','What are research expenses in 2018?'),recipient,sp,6332.,True))
  wrong=copy.deepcopy(p);wrong['to_expression']='x0+x1';wrong['to_op']='sum';scenarios.append(('incorrect_proposed_diagnosis',C,Q2,r,wrong,273.,False))
  # A supported example can underdetermine a general formula. Passing the checks
  # cannot certify that a denominator omitted at value one is semantically valid.
  cc=dict(id='coincidental_formula',table=[['Metric','2021','2020','2019','2018'],['Research expenses','6','3','2','1']],paragraphs=[])
  dq=q('q1','What is the percentage change in research expenses from 2018 to 2019?');rq=q('q2','What is the percentage change in research expenses from 2020 to 2021?')
  def pct(refs,expr,years,value):
   return parse(dict(answer=[str(value)],scale='percent',rep=dict(entity='company',metric='research expenses',op='percentage_change',refs=refs,periods=years,unit='dimensionless',scale='percent',expression=expr)),cc)
  da=pct(['T1C3','T1C4'],'x0/x1*100',['2019','2018'],200);db=pct(['T1C3','T1C4'],'(x0-x1)*100',['2019','2018'],100)
  cp=infer(cc,dq,da,db,dict(answer='100',scale='percent'));ra=pct(['T1C1','T1C2'],'x0/x1*100',['2021','2020'],100)
  scenarios.append(('coincidental_formula_harm',cc,rq,ra,cp,100.,True))
  for name,c,question,before,patch,target,expected in scenarios:
   for checks in [True,False]:
    e=propose(c,question,before,patch,checks);a=e['after'];target_scale='percent' if name in ['different_percentage_operation','coincidental_formula_harm'] else 'million';correct=len(a['answer'])==1 and abs(float(a['answer'][0])-target)<.011 and a['scale']==target_scale
    if checks:assert e['accepted']==expected,(name,e['reasons']);assert e['accepted'] or e['after']==before
    cases.append(dict(case=name,seed=seed,method='patch' if checks else 'no_applicability',accepted=e['accepted'],correct=correct,reasons=';'.join(e['reasons'])))
    if seed==0:write(ART/'synthetic'/name/('patch.json' if checks else 'no_applicability.json'),dict(source=c,question=question,before=before,patch=patch,event=e,target=target,kind='Authored source, dependencies, errors and expected intervention boundary; not TAT-QA observations.'))
 csvout(ART/'synthetic/results.csv',cases);write(ART/'synthetic/audit.json',dict(passed=True,seeds=list(range(32)),cases=11,rows=len(cases),generations=0,source_independent_empirical_units=0,semantic_counterexample='A missing denominator can fit a donor whose denominator is one and harm a recipient despite all structural checks. Added as a boundary diagnostic, without revising the algorithm.'));print('Synthetic boundary rows',len(cases))
if __name__=='__main__':run_all()
