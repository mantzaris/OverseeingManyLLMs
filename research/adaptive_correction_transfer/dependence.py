"""Public source-material overlap audit, without inferring missing report identities."""
import collections,re
from .common import ART,read,write,digest

def normalize(s):return ' '.join(re.findall(r'\w+',str(s).lower()))
def audit():
 m=read(ART/'frozen/manifest.json');cs=m['contexts'];paras=collections.defaultdict(list);tables=collections.defaultdict(list)
 for c in cs:
  tables[digest([[normalize(x) for x in row] for row in c['table']])].append(c['id'])
  for p in c['paragraphs']:
   n=normalize(p['text'])
   if len(n)>=160:paras[digest(n)].append(c['id'])
 duplicates=[dict(hash=k,contexts=sorted(set(v))) for k,v in paras.items() if len(set(v))>1];parent={c['id']:c['id'] for c in cs}
 def find(x):
  while parent[x]!=x:x=parent[x]
  return x
 for x in duplicates:
  for cid in x['contexts'][1:]:parent[find(cid)]=find(x['contexts'][0])
 groups=collections.defaultdict(list)
 for cid in parent:groups[find(cid)].append(cid)
 result=dict(contexts=len(cs),exact_duplicate_tables=[v for v in tables.values() if len(v)>1],shared_long_paragraphs=duplicates,public_text_components=list(groups.values()),interpretation='Exact public text overlap is audited independently of model outcomes. Components are not reliable report identifiers. Absence of exact overlap does not establish report-level independence. Primary inference remains the frozen context-level descriptive bootstrap.')
 write(ART/'analysis/source_dependence.json',result);print('Contexts',len(cs),'duplicate tables',len(result['exact_duplicate_tables']),'shared long paragraphs',len(duplicates),'text components',len(groups))
if __name__=='__main__':audit()
