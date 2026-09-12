"""Public prompts, bounded arithmetic and structural validation. No gold annotations."""
import ast,operator,math,re
from .common import digest
SCALES=['','thousand','million','billion','percent']
SYSTEM='''Answer the financial question from the supplied table and paragraphs. Return JSON with evidence (cell IDs like T2C1 or paragraph IDs P1), operation, brief derivation, answer (list of values/spans), and scale. Reason from relevant row labels and periods before the answer; do not combine unrelated rows. For 'which year' return a year; for 'how' return the requested description.
Scale must be "", "thousand", "million", "billion", or "percent". Read units from source headings and text. Preserve the source scale for amounts. Ratios reported as percentages use percent, regardless of currency units; a source percentage is already in percent. For arithmetic, answer may contain an expression starting with '=', e.g. ["=(12-9)/9*100"]. A calculator evaluates it and rounds to two decimals. Otherwise give the final answer. Do not copy these example numbers. Operation: lookup, sum, difference, average, ratio, count, or other. Derivation under 35 words. If unsupported, answer:[] with an explanation. No text outside JSON.'''
def source_text(c):
 cols=max(len(row) for row in c['table']);lines=['TABLE: C0 contains row labels; cite cells as T<row>C<column>.']
 lines+=['| row | '+' | '.join('C%d'%k for k in range(cols))+' |','|---|'+'---|'*cols]
 for r,row in enumerate(c['table']):lines.append('| T%d | '%r+' | '.join(str(v).replace('|','/') for v in row+['']*(cols-len(row)))+' |')
 lines+=['P%s: %s'%(p['order'],p['text']) for p in c['paragraphs']]
 return '\n'.join(lines)
def messages(c,q,current=None,corrections=None,reattempt=False):
 text=source_text(c)+'\nQUESTION: '+q['question']
 if current is not None:text+='\nThis is a fresh re-solution. Recompute YOUR requested answer from the source; do not assume a prior draft was correct.'
 if corrections:
  text+='\nVERIFIED INSPECTIONS (only these questions were inspected; explanations beyond the annotation are not certified):\n'
  for f in corrections:text+='Previous answer: '+str({k:f.get('previous',{}).get(k) for k in ['answer','scale']})+'\nQuestion: '+f['question']+'\nAnswer: '+str(f['answer'])+'; scale: '+f['scale']+'; annotated derivation: '+str(f['derivation'])+'\n'
  text+='These records apply directly only to their stated questions and context. Recheck relevant evidence for YOUR distinct question; preserve different periods, entities and ratio scales. You may retain your answer when the correction does not apply.'
 elif reattempt:text+='\nRecheck this output using the same source. No new verified correction is available. Revise only when justified.'
 return [dict(role='system',content=SYSTEM),dict(role='user',content=text)]
OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv}
def calculate(s):
 if len(s)>160:raise ValueError('Expression too long')
 tree=ast.parse(s,mode='eval')
 if len(list(ast.walk(tree)))>45:raise ValueError('Expression too large')
 def go(n):
  if isinstance(n,ast.Expression):return go(n.body)
  if isinstance(n,ast.Num) and not isinstance(n.n,bool):return float(n.n)
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):return (-1 if isinstance(n.op,ast.USub) else 1)*go(n.operand)
  if isinstance(n,ast.BinOp) and type(n.op) in OPS:return OPS[type(n.op)](go(n.left),go(n.right))
  raise ValueError('Unsupported calculation')
 v=go(tree)
 if not math.isfinite(v) or abs(v)>1e18:raise ValueError('Nonfinite or excessive result')
 return str(round(v,2))
def prepare(p,c):
 out=dict(answer=[],scale='',evidence=[],operation='other',derivation='',valid=False,issues=[])
 if not isinstance(p,dict):out['issues']=['malformed'];return out
 out.update({k:p[k] for k in out if k in p and k not in ['valid','issues']})
 a=out['answer']
 if isinstance(a,(str,int,float)):a=[str(a)]
 if not isinstance(a,list) or any(not isinstance(x,(str,int,float)) for x in a):out['issues'].append('answer_shape');a=[]
 out['answer']=[str(x) for x in a]
 if out['scale'] not in SCALES:out['issues'].append('scale');out['scale']=''
 if not isinstance(out['evidence'],list):out['evidence']=[];out['issues'].append('evidence_shape')
 allowed={'T%dC%d'%(r,k) for r,row in enumerate(c['table']) for k in range(len(row))}|{'P%s'%x['order'] for x in c['paragraphs']}
 out['invalid_evidence']=[str(x) for x in out['evidence'] if str(x) not in allowed];out['evidence']=[str(x) for x in out['evidence'] if str(x) in allowed]
 if not isinstance(out['operation'],str):out['operation']='other'
 out['derivation']=str(out['derivation'])[:1000]
 out['calculation']=p.get('calculation','')
 if len(out['answer'])==1 and out['answer'][0].startswith('='):
  try:out['answer']=[calculate(out['answer'][0][1:])]
  except Exception as e:out['issues'].append('calculation_failed');out['answer']=[]
 out['valid']=bool(out['answer']) and not out['issues']
 return out
