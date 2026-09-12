"""Bounded source-linked expressions. Executability is not semantic correctness."""
import ast,copy,math,re
from research.adaptive_correction_transfer.answers import prepare,calculate,SCALES,source_text
from research.adaptive_correction_transfer.features import kind,words
from .common import digest
OPS={'lookup','sum','difference','percentage_change','ratio','average','count','other'}
SYSTEM='''Return JSON for the financial question: answer (list), scale ("", thousand, million, billion, percent), evidence (IDs), derivation (under 25 words), and rep. For a supported numerical computation, rep is {"entity":"subject", "metric":"row metric", "op":"lookup|sum|difference|percentage_change|ratio|average|count", "refs":["T2C1","T2C2"], "periods":["2019","2018"], "unit":"currency|shares|count|dimensionless|other", "scale":"million", "expression":"x0-x1"}. xi means the numeric value of refs[i], read directly from the immutable source. Order operands deliberately. Constants allowed: 0,1,100,1000,1000000,1000000000 and divisor counts. Percentage change is (later-earlier)/earlier*100; ratio is numerator/denominator. Match the question's requested periods, row, and scale. Do not use a displayed variance for different periods. For text answers or unsupported computations set rep:null and still answer the question. No external facts or text outside JSON.'''

def version(c):return digest({'id':c['id'],'table':c['table'],'paragraphs':c['paragraphs']})
def messages(c,q,old=None,mode='initial',feedback=None):
 text=source_text(c)+'\nQUESTION: '+q['question']
 if old is not None:text+='\nDRAFT: '+str({k:old.get(k) for k in ['answer','scale','derivation','rep']})
 if mode=='extract':text+='\nExtract the draft\'s numerical interpretation. Preserve its answer even if execution differs. Bind operands to the actual cells; rep:null if the draft has no supported numerical interpretation.'
 elif mode=='verify':text+='\nIndependently verify the question against the source. Check row, period, scale, operand order and arithmetic. Produce the best source-supported representation and answer. No inspected sibling information is available.'
 elif mode=='reattempt':text+='\nMake an ordinary fresh attempt at this question using the same source. No new verified information is available.'
 elif mode=='corrected':text+='\nOnly THIS question was inspected. Reconstruct a source-supported computation consistent with the acquired annotation. Do not change source values. If the annotation cannot be explained by the source, use rep:null. ANNOTATION: '+str({k:feedback.get(k) for k in ['question','answer','scale','derivation']})
 elif mode=='coarse':text+='\nACQUIRED SAME-CONTEXT CORRECTIONS, verified only for their own questions: '+str([{k:f.get(k) for k in ['question','answer','scale','derivation']} for f in feedback])+'\nReconsider your distinct answer; preserve its own periods, entity and units.'
 return [{'role':'system','content':SYSTEM},{'role':'user','content':text}]

def number(s):
 s=str(s).strip().replace(',','').replace('$','').replace('€','').replace('£','').replace('%','').strip()
 if s in ['—','–','-']:raise ValueError('dash is not a verified zero')
 if s.startswith('(') and s.endswith(')'):s='-'+s[1:-1].strip()
 if not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)',s):raise ValueError('nonnumeric cell')
 return float(s)

def cell(c,ref):
 m=re.fullmatch(r'T(\d+)C(\d+)',str(ref))
 if not m:raise ValueError('unsupported reference')
 r,k=map(int,m.groups());return c['table'][r][k]

def period_evidence(c,ref):
 m=re.fullmatch(r'T(\d+)C(\d+)',ref);r,k=map(int,m.groups());found=[]
 # Closest same-column explicit year or preceding year section. No future rows.
 for i in range(r,-1,-1):
  row=c['table'][i];value=row[k] if k<len(row) else '';ys=re.findall(r'\b(?:19|20)\d{2}\b',str(value))
  if ys:return ys
  if i<r and row and re.search(r'\b(?:19|20)\d{2}\b',str(row[0])) and sum(bool(str(x).strip()) for x in row)<=1:return re.findall(r'\b(?:19|20)\d{2}\b',str(row[0]))
 return found

def evaluate(rep,c):
 if not isinstance(rep,dict):raise ValueError('unsupported representation')
 refs=rep.get('refs');expr=rep.get('expression','')
 if not isinstance(refs,list) or not 1<=len(refs)<=8 or len(expr)>160:raise ValueError('representation bounds')
 vals=[number(cell(c,x)) for x in refs];tree=ast.parse(expr,mode='eval')
 if len(list(ast.walk(tree)))>45:raise ValueError('expression bounds')
 constants=[n.n for n in ast.walk(tree) if isinstance(n,ast.Num)]
 if any(v not in {0,1,2,3,4,5,6,7,8,100,1000,1000000,1000000000} for v in constants):raise ValueError('unsupported constant')
 names={n.id for n in ast.walk(tree) if isinstance(n,ast.Name)}
 if not names or not names<={'x'+str(i) for i in range(len(refs))}:raise ValueError('operand names')
 if names!={'x'+str(i) for i in range(len(refs))}:raise ValueError('unused operands')
 class Bind(ast.NodeTransformer):
  def visit_Name(self,n):return ast.copy_location(ast.Num(n=vals[int(n.id[1:])]),n)
 # The historical calculator admits only bounded arithmetic, not calls or attributes.
 replaced=re.sub(r'\bx(\d+)\b',lambda m:'('+str(vals[int(m[1])])+')',expr)
 return float(calculate(replaced))

def parse(payload,c):
 a=prepare(payload,c);rep=copy.deepcopy(payload.get('rep')) if isinstance(payload,dict) else None
 a['rep']=rep;a['representation_errors']=[];a['representation_valid']=False
 if not isinstance(rep,dict):a['representation_errors']=['unsupported'];return a
 rep['source_id']=c['id'];rep['source_version']=version(c)
 try:
  if rep.get('op') not in OPS or rep.get('scale') not in SCALES:raise ValueError('operation or scale')
  if not all(isinstance(rep.get(k),str) for k in ['entity','metric','unit','expression']):raise ValueError('binding fields')
  if not isinstance(rep.get('periods'),list):raise ValueError('periods')
  a['executed']=evaluate(rep,c);a['representation_valid']=True
 except (ValueError,TypeError,IndexError,SyntaxError,KeyError,OverflowError,ZeroDivisionError) as e:a['representation_errors']=[str(e)]
 return a

def contract(c,q,rep):
 reasons=[]
 if not isinstance(rep,dict):return ['unsupported_representation']
 if rep.get('source_id')!=c['id'] or rep.get('source_version')!=version(c):reasons.append('source_version')
 try:evaluate(rep,c)
 except Exception as e:return reasons+['execution:'+str(e)]
 wanted=set(re.findall(r'\b(?:19|20)\d{2}\b',q['question']));declared=set(map(str,rep.get('periods',[])));actual=set(y for ref in rep['refs'] for y in period_evidence(c,ref))
 if wanted and (not wanted<=declared or not wanted<=actual or actual-wanted):reasons.append('period_binding')
 if declared and not declared<=actual:reasons.append('unsupported_period')
 k=kind(q['question']);op=rep['op'];text=q['question'].lower()
 if 'percentage' in text or 'percent' in text:
  if rep['scale']!='percent':reasons.append('percentage_scale')
  if k=='ratio' and any(x in text for x in ['change','increase','decrease','growth']) and op!='percentage_change':reasons.append('operation_contract')
 elif k=='difference' and op!='difference':reasons.append('operation_contract')
 elif k=='average' and op!='average':reasons.append('operation_contract')
 if op in ['ratio','percentage_change'] and rep['unit']!='dimensionless':reasons.append('dimensionless_unit')
 if op=='percentage_change' and ('100' not in rep['expression'] or '-' not in rep['expression']):reasons.append('percentage_expression')
 if op=='difference' and '-' not in rep['expression']:reasons.append('difference_expression')
 # Lexical support is deliberately a necessary weak check, not a gold metric map.
 rows=[int(re.fullmatch(r'T(\d+)C(\d+)',ref)[1]) for ref in rep['refs']]
 labels=' '.join(str(c['table'][r][0]) for r in rows)
 if not (words(rep['metric'])&words(labels)&words(q['question'])):reasons.append('metric_support')
 return sorted(set(reasons))

def executed_answer(a,c):
 b=copy.deepcopy(a);value=evaluate(a['rep'],c);b.update(answer=[str(value)],scale=a['rep']['scale'],valid=True,issues=[],operation=a['rep']['op'],derivation='Executed '+a['rep']['expression']);return b
