import copy,unittest
from .representation import parse,contract,evaluate,version
from .patches import infer,propose,apply_to_state
from .experiment import run
from .common import stable
from research.adaptive_correction_transfer.feedback import Inspector
C={'id':'constructed','table':[['Metric','2019','2018','2017'],['Research expenses','6577','6332','6059'],['Sales','9571','9242','9184']],'paragraphs':[{'order':1,'text':'All expenses and sales in millions of dollars.'}]}
def q(id,text):return {'id':id,'question':text,'order':int(id[-1])}
Q1=q('q1','What is the change in research expenses between 2018 and 2019?')
Q2=q('q2','What is the change in research expenses between 2017 and 2018?')
Q3=q('q3','What are sales in 2017?')
C['questions']=[Q1,Q2,Q3]
def answer(refs,expr,op='difference',periods=None,scale='million',unit='currency',metric='research expenses'):
 return parse({'answer':['0'],'scale':scale,'evidence':refs,'operation':op,'rep':{'entity':'company','metric':metric,'op':op,'refs':refs,'periods':periods or ['2019','2018'],'unit':unit,'scale':scale,'expression':expr}},C)
def setup():
 old=answer(['T1C1','T1C2'],'x1-x0');correct=answer(['T1C1','T1C2'],'x0-x1');f={'id':'q1','question':Q1['question'],'answer':'245','scale':'million','derivation':'6577-6332','answer_type':'arithmetic'}
 return old,correct,f,infer(C,Q1,old,correct,f)
class Boundaries(unittest.TestCase):
 def test_operation_can_generalize_across_periods(self):
  _,_,_,p=setup();r=answer(['T1C2','T1C3'],'x1-x0',periods=['2018','2017']);e=propose(C,Q2,r,p);self.assertTrue(e['accepted']);self.assertEqual(e['after']['answer'],['273.0']);self.assertEqual(e['after']['rep']['refs'],r['rep']['refs'])
 def test_different_period_fact_rejected(self):
  old=answer(['T1C2'],'x0','lookup',['2018']);new=answer(['T1C1'],'x0','lookup',['2019']);question=q('q1','What are research expenses in 2019?');f={'answer':'6577','scale':'million'};p=infer(C,question,old,new,f)
  r=answer(['T1C2','T1C3'],'x0-x1',periods=['2018','2017']);e=propose(C,Q2,r,p);self.assertFalse(e['accepted']);self.assertIn('period_binding',e['reasons']);self.assertEqual(e['after'],r)
 def test_ratio_scale_not_currency(self):
  r=answer(['T1C1','T1C2'],'x0/x1','ratio',scale='million',unit='currency');self.assertIn('dimensionless_unit',contract(C,q('q1','What is the ratio of research expenses in 2019 to 2018?'),r['rep']))
 def test_unrelated_outputs_and_source_unchanged(self):
  old,_,_,p=setup();other=answer(['T2C3'],'x0','lookup',['2017'],metric='sales');state={'q1':old,'q2':answer(['T1C2','T1C3'],'x1-x0',periods=['2018','2017']),'q3':other};before=copy.deepcopy(C);out,events=apply_to_state(C,C['questions'],state,p,['q1']);self.assertEqual(out['q3'],other);self.assertEqual(out['q1'],old);self.assertEqual(C,before)
 def test_source_revision_invalidates_patch(self):
  _,_,_,p=setup();c=copy.deepcopy(C);c['table'][1][1]='9999';r=answer(['T1C2','T1C3'],'x1-x0',periods=['2018','2017']);e=propose(c,Q2,r,p);self.assertFalse(e['accepted']);self.assertIn('source_version',e['reasons'])
 def test_execution_failure_rolls_back(self):
  _,_,_,p=setup();p['to_expression']='x0/0';r=answer(['T1C2','T1C3'],'x1-x0',periods=['2018','2017']);e=propose(C,Q2,r,p);self.assertFalse(e['accepted']);self.assertEqual(e['after'],r)
 def test_missing_representation_retained(self):
  _,_,_,p=setup();a={'answer':['7'],'scale':'million','rep':None};e=propose(C,Q2,a,p);self.assertEqual(e['after'],a);self.assertFalse(e['accepted'])
 def test_inspection_budget_and_hidden_label_isolation(self):
  old,correct,f,_=setup();initial={j['id']:copy.deepcopy(old) for j in C['questions']};gold={j['id']:dict(f,answer='245') for j in C['questions']}
  def gen(*args):return correct,{'call_id':'controlled','tokens':0,'seconds':0,'attempts':0}
  a=run(C,initial,['q1','q2'],Inspector(gold,2),gen,'patch');g=copy.deepcopy(gold);g['q3']['answer']='99999';b=run(C,initial,['q1','q2'],Inspector(g,2),gen,'patch');self.assertEqual(stable(a),stable(b))
  with self.assertRaises(RuntimeError):run(C,initial,['q1','q2'],Inspector(gold,1),gen,'patch')
 def test_unexplained_annotation_no_rule(self):
  old,c,f,_=setup();f['answer']='888';p=infer(C,Q1,old,c,f);self.assertFalse(p['supported'])
 def test_no_label_overrides_numeric_source(self):
  r=answer(['T1C1'],'888','lookup',['2019']);self.assertFalse(r['representation_valid'])
if __name__=='__main__':unittest.main()
