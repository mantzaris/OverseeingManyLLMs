"""Observable relations; no benchmark mappings or gold operations."""
import re
STOP=set('what is the in of a an and for to was were how much many does did are from between at on as by total years year'.split())
def words(q):return set(re.findall('[a-z]+',q.lower()))-STOP
def kind(q):
 q=q.lower()
 if any(s in q for s in ['percent','percentage','proportion','ratio','growth rate']):return 'ratio'
 if any(s in q for s in ['average','mean']):return 'average'
 if any(s in q for s in ['difference','change','increase','decrease']):return 'difference'
 if any(s in q for s in ['total','sum','combined']):return 'sum'
 if any(s in q for s in ['how many','number of']):return 'count'
 return 'lookup'
def risk_key(q,a):return 'invalid' if not a.get('valid') else kind(q['question'])
def relation(qi,ai,qj,aj):
 ei=set(ai.get('evidence',[]));ej=set(aj.get('evidence',[]));rows=lambda es:{re.sub('C[0-9]+$','',e) for e in es if e.startswith('T')}
 w1,w2=words(qi['question']),words(qj['question']);similarity=len(w1&w2)/max(1,len(w1|w2));shared=bool(ei&ej) or bool(rows(ei)&rows(ej));same_operation=kind(qi['question'])==kind(qj['question']);scale_same=ai.get('scale')==aj.get('scale')
 bin='evidence' if shared else 'lexical' if similarity>=.2 else 'context'
 return dict(bin=bin,evidence_overlap=shared,lexical_similarity=similarity,same_operation=same_operation,same_scale=scale_same,period_overlap=bool(set(re.findall(r'20\d\d|19\d\d',qi['question']))&set(re.findall(r'20\d\d|19\d\d',qj['question']))))
def fixed_eligible(rel):return rel['evidence_overlap'] or (rel['lexical_similarity']>=.2 and rel['same_operation'])
def initial_rank(c,answers):
 risk={'invalid':1.,'ratio':.8,'average':.65,'difference':.65,'sum':.55,'count':.45,'lookup':.3}
 def key(q):
  linked=sum(fixed_eligible(relation(q,answers[q['id']],j,answers[j['id']])) for j in c['questions'] if j['id']!=q['id'])
  return -(risk[risk_key(q,answers[q['id']])]+.08*linked),q['order'],q['id']
 return [q['id'] for q in sorted(c['questions'],key=key)]
