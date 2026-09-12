import copy,unittest
from .answers import prepare,calculate
from .feedback import Inspector
from .controller import run
from .common import stable,digest
from .features import relation,fixed_eligible
C=dict(id='synthetic',table=[['Item','2019','2020'],['A','10','20'],['B','4','4']],paragraphs=[dict(order=1,text='Amounts in millions; ratios are percentages.')],questions=[dict(id='q'+str(i),order=i,question=q) for i,q in enumerate(['What is A in 2020?','What is A in 2019?','What is the percentage change in A?','What is B in 2020?'])])
P=dict(risk={k:[3.,2.] for k in ['pooled','lookup','ratio','invalid']},conditional={k+'_'+str(e):[2.,2.] for k in ['context','lexical','evidence'] for e in [0,1]},transfer={k:dict(fix=[4.,1.],harm=[1.,8.]) for k in ['pooled','context','lexical','evidence']},machine_cost=.01,epsilon=0.,recipient_cap=3)
G={q['id']:dict(answer=str([20,10,100,4][i]),scale=['million','million','percent','million'][i],derivation='',answer_type='arithmetic') for i,q in enumerate(C['questions'])}
def initial():return {q['id']:prepare(dict(answer=['12'],scale='million',evidence=['T1C1'],operation='lookup',derivation='Authored faulty answer'),C) for q in C['questions']}
def responder(q,old,f,step,retry):return prepare(dict(answer=['10'],scale='million',evidence=['T1C1'],operation='lookup'),C),dict(call_id=q['id']+'_'+str(step),attempts=0,tokens=0,seconds=0)
class ProtocolTests(unittest.TestCase):
 def test_budget(self):
  inspector=Inspector(G,2);r=run(C,initial(),P,inspector,responder,5,budget=2)
  self.assertEqual(r['inspections'],2);self.assertLessEqual(len(r['calls']),6)
  with self.assertRaises(RuntimeError):inspector.inspect(C['questions'][-1])
 def test_hidden_sibling_labels_cannot_change_actions(self):
  a=run(C,initial(),P,Inspector(G,2),responder,5,budget=2);seen={e['inspected'] for e in a['events']};g=copy.deepcopy(G)
  for k in g:
   if k not in seen:g[k]['answer']='999999';g[k]['scale']='billion'
  b=run(C,initial(),P,Inspector(g,2),responder,5,budget=2);self.assertEqual(stable(a),stable(b))
 def test_learning_only_observed_recipients(self):
  r=run(C,initial(),P,Inspector(G,2),responder,5,budget=2);seen={e['inspected'] for e in r['events']}
  self.assertTrue(all(u['question'] in seen for u in r['updates']))
 def test_scope_relation_is_not_gold_applicability(self):
  a=initial();rel=relation(C['questions'][0],a['q0'],C['questions'][2],a['q2']);self.assertTrue(rel['evidence_overlap']);self.assertFalse(rel['same_operation'])
  self.assertNotIn('correct',rel)
 def test_arithmetic_and_scale(self):
  self.assertEqual(calculate('(20-10)/10*100'),'100.0')
  a=prepare(dict(answer=['=(20-10)/10*100'],scale='percent',evidence=['T1C1']),C);self.assertEqual(a['answer'],['100.0']);self.assertEqual(a['scale'],'percent')
  for expression in ['__import__("os")','1/0','2**100']:
   with self.assertRaises(Exception):calculate(expression)
 def test_intermediate_calculation_does_not_replace_year(self):
  a=prepare(dict(answer=['2020'],scale='',calculation='20-10',evidence=['T0C2']),C);self.assertEqual(a['answer'],['2020'])
 def test_failure_retained(self):
  def bad(*args):return prepare(None,C),dict(call_id='bad',attempts=1,tokens=0,seconds=0)
  r=run(C,initial(),P,Inspector(G,1),bad,5,method='memory',budget=1)
  self.assertTrue(r['events'][0]['repairs']);self.assertTrue(all(not x['accepted'] for x in r['events'][0]['repairs']));self.assertEqual(r['events'][0]['repairs'][0]['proposal']['issues'],['malformed'])
 def test_repeatable(self):
  a=run(C,initial(),P,Inspector(G,2),responder,5);b=run(C,initial(),P,Inspector(G,2),responder,5);self.assertEqual(stable(a),stable(b))
 def test_fixed_transfer_and_retry_have_same_audits_recipients(self):
  a=run(C,initial(),P,Inspector(G,2),responder,5,method='source_rule');b=run(C,initial(),P,Inspector(G,2),responder,5,method='reattempt')
  self.assertEqual([(e['inspected'],e['recipients']) for e in a['events']],[(e['inspected'],e['recipients']) for e in b['events']])
 def test_harmful_valid_repairs_not_hidden(self):
  def wrong(*args):return prepare(dict(answer=['999'],scale='million',evidence=['T1C1']),C),dict(call_id='wrong',attempts=1,tokens=10,seconds=0)
  a=initial();a['q3']=prepare(dict(answer=['4'],scale='million',evidence=['T2C2']),C)
  r=run(C,a,P,Inspector(G,1),wrong,5,method='memory',budget=1)
  harmed=[x for x in r['events'][0]['repairs'] if x['id']=='q3'];self.assertTrue(harmed);self.assertEqual(harmed[0]['after']['answer'],['999'])
if __name__=='__main__':unittest.main()
