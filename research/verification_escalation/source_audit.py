"""Post-freeze evaluator-reference audit, never used to select cases."""
from .common import ART,read,write_json
from .engine import MachineBudget,execute,equivalent

def run():
 cases=read(ART/'private/cases.json');records=[]
 for split,cc in cases.items():
  for c in cc:
   rs=[execute(c['snapshot'],q,MachineBudget(1)) for q in c['refs']]
   records.append(dict(id=c['id'],split=split,kind=c['kind'],db=c['db'],references=len(rs),reference_status=[r['status'] for r in rs],errors=[r.get('error') for r in rs],reference_hashes=[r.get('table_hash') for r in rs],all_reference_outputs_equal=equivalent(rs),foreign_key_violations=len(c['foreign_key_violations']),intent_indices=c.get('intent_indices',[0,1])))
 write_json(ART/'reference_audit.json',records)
 print('reference failures',sum(any(s!='ok' for s in r['reference_status']) for r in records),'equal',sum(r['all_reference_outputs_equal'] for r in records))
if __name__=='__main__':run()
