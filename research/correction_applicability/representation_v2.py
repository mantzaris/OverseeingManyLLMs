"""Development refinement: source-derived binding descriptors, fewer generated fields."""
import copy,re
from . import representation as base
from .common import digest
from research.adaptive_correction_transfer.answers import prepare,source_text,SCALES
from research.adaptive_correction_transfer.features import kind,words
SYSTEM='''Answer the financial question using only the source. Return JSON: {"answer":["value or text"],"scale":"million","evidence":["T2C1"],"derivation":"brief explanation","rep":{"op":"difference","refs":["T2C1","T2C2"],"expression":"x0-x1","scale":"million"}}. rep is null for text answers or unsupported arithmetic. refs must identify actual numeric table cells, xi reads refs[i] exactly. Operation: lookup, sum, difference, average, percentage_change, ratio, count. Average: (x0+x1)/2. Percentage change: (later-earlier)/earlier*100. Ratios are dimensionless. Scale: "", thousand, million, billion, percent. Use the source's amount scale. A rate already displayed with % has percent scale. Match requested rows and periods. Do not use a displayed variance for other periods. Do not put numeric operands into expression: use xi. Return concise JSON only.'''

def messages(c,q,old=None,mode='initial',feedback=None):
 text=source_text(c)+'\nQUESTION: '+q['question']
 if old is not None:
  r=old.get('rep');small={k:r.get(k) for k in ['op','refs','expression','scale']} if isinstance(r,dict) else None
  text+='\nDRAFT: '+str(dict(answer=old.get('answer'),scale=old.get('scale'),rep=small))
 if mode=='extract':text+='\nRepresent the draft using source-cell operands. Preserve its stated answer. If its computation cannot be supported, rep:null. Do not force execution to match a wrong draft.'
 elif mode=='verify':text+='\nIndependently reread the source and verify this question. Check rows, periods, units and arithmetic. No sibling correction is available.'
 elif mode=='reattempt':text+='\nMake another ordinary attempt with this source. No verified correction is available.'
 elif mode=='corrected':text+='\nOnly THIS question has been inspected. Explain its annotation with a source-bound computation; rep:null if unexplained. Do not alter source values. Annotation: '+str({k:feedback.get(k) for k in ['answer','scale','derivation']})
 elif mode=='coarse':
  text+='\nVerified only for these sibling questions: '+str([{k:f.get(k) for k in ['question','answer','scale','derivation']} for f in feedback])+'\nReconsider your own answer without copying incompatible periods, rows or operations.'
 return [{'role':'system','content':SYSTEM},{'role':'user','content':text}]

def binding(c,ref):
 m=re.fullmatch(r'T(\d+)C(\d+)',ref)
 if not m:raise ValueError('unsupported reference')
 r,k=map(int,m.groups());raw=c['table'][r][k];label=str(c['table'][r][0]);section='';period=[];headers=[]
 for i in range(r,-1,-1):
  row=c['table'][i];first=str(row[0]) if row else '';v=str(row[k]) if k<len(row) else ''
  if i<r and i<3:headers.append(v)
  if not section and i<r and first.strip() and all(not str(v).strip() for v in row[1:]):section=first
  if not period:
   # Explicit year columns in the table header, or dated row/section labels.
   if i<r and i<3 and re.search(r'\b(?:19|20)\d{2}\b',v):period=re.findall(r'\b(?:19|20)\d{2}\b',v)
   elif re.search(r'\b(?:19|20)\d{2}\b',first) and re.search(r'\b(at|as|january|february|march|april|may|june|july|august|september|october|november|december)\b',first.lower()):period=re.findall(r'\b(?:19|20)\d{2}\b',first)
 return dict(ref=ref,row=r,column=k,row_label=label,section=section,column_header=' '.join(reversed(headers)),periods=period,raw=raw,value=base.number(raw))

def parse(payload,c):
 a=prepare(payload,c);rawrep=payload.get('rep') if isinstance(payload,dict) else None;a['rep']=None;a['representation_valid']=False;a['representation_errors']=[]
 if not isinstance(rawrep,dict):a['representation_errors']=['unsupported'];return a
 try:
  r=copy.deepcopy(rawrep)
  if r.get('op') not in base.OPS or r.get('scale') not in SCALES:raise ValueError('operation or scale')
  bs=[binding(c,x) for x in r.get('refs',[])];r.update(source_id=c['id'],source_version=base.version(c),entity=c['id'],metric=' '.join(sorted(set(b['row_label']+' '+b['section'] for b in bs))),periods=sorted(set(y for b in bs for y in b['periods'])),unit='dimensionless' if r['op'] in ['ratio','percentage_change'] or r['scale']=='percent' else 'source_amount',bindings=bs)
  a['rep']=r;a['executed']=base.evaluate(r,c);a['representation_valid']=True
 except (ValueError,TypeError,IndexError,KeyError,SyntaxError,ZeroDivisionError,OverflowError) as e:a['representation_errors']=[str(e)];a['rep']=dict(rawrep,source_id=c['id'],source_version=base.version(c))
 return a

def contract(c,q,r):
 if not isinstance(r,dict):return ['unsupported_representation']
 reasons=[]
 if r.get('source_id')!=c['id'] or r.get('source_version')!=base.version(c):reasons.append('source_version')
 try:
  bs=[binding(c,x) for x in r['refs']];base.evaluate(r,c)
 except Exception as e:return reasons+['execution:'+str(e)]
 wanted=set(re.findall(r'\b(?:19|20)\d{2}\b',q['question']));actual=set(y for b in bs for y in b['periods'])
 if wanted and (not wanted<=actual or actual-wanted):reasons.append('period_binding')
 if sorted(actual)!=r.get('periods'):reasons.append('changed_period_record')
 text=q['question'].lower();op=r.get('op');k=kind(text)
 if 'percentage' in text or 'percent' in text:
  if r.get('scale')!='percent':reasons.append('percentage_scale')
  if any(w in text for w in ['change','increase','decrease','growth']) and op!='percentage_change':reasons.append('operation_contract')
 elif k=='difference' and op!='difference':reasons.append('operation_contract')
 elif k=='average' and op!='average':reasons.append('operation_contract')
 if op=='percentage_change' and ('-' not in r['expression'] or '100' not in r['expression']):reasons.append('percentage_expression')
 if op=='difference' and '-' not in r['expression']:reasons.append('difference_expression')
 if op in ['ratio','percentage_change'] and r.get('unit')!='dimensionless':reasons.append('dimensionless_unit')
 if any('%' in str(b['raw']) for b in bs) and op not in ['ratio','percentage_change'] and r.get('scale')!='percent':reasons.append('source_percent_scale')
 anchors=' '.join(b['row_label']+' '+b['section'] for b in bs)
 if not words(anchors)&words(text):reasons.append('metric_support')
 # An amount cannot acquire percentage scale without a percentage source or ratio operation.
 if r.get('scale')=='percent' and op not in ['ratio','percentage_change'] and not (any('%' in str(b['raw']) or '%' in b['column_header'] for b in bs) or '%' in ' '.join(str(x) for row in c['table'][:2] for x in row)):reasons.append('unsupported_percent_scale')
 return sorted(set(reasons))

executed_answer=base.executed_answer


def rebind(c,r):
 r=copy.deepcopy(r);bs=[binding(c,x) for x in r['refs']];r.update(bindings=bs,periods=sorted(set(y for b in bs for y in b['periods'])),metric=' '.join(sorted(set(b['row_label']+' '+b['section'] for b in bs))))
 return r


def supported_spans(c,a):
 """Literal source support for nonnumeric generated spans, not semantic correctness."""
 if not a.get('valid') or not a.get('evidence') or not a.get('answer'):return False
 evidence=[]
 for ref in a['evidence']:
  if ref.startswith('P'):
   evidence.extend(p['text'] for p in c['paragraphs'] if 'P'+str(p['order'])==ref)
  else:
   try:evidence.append(str(base.cell(c,ref)))
   except Exception:pass
 normalize=lambda s:' '.join(re.findall(r'\w+',str(s).lower()))
 return all(re.search('[a-zA-Z]',s) and any(normalize(s) in normalize(e) for e in evidence) for s in a['answer'])
