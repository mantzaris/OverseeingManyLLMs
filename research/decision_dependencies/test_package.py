"""Concrete saved-evidence and execution-boundary regression checks."""
import copy
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from . import client
from .client import ART
from .evaluate import simulate
from .freeze import verify_frozen
from .reproduce import verify_raw


class PackageChecks(unittest.TestCase):
    def test_final_call_accounting_and_freeze(self):
        self.assertEqual(verify_raw(),dict(calls=784,attempts=784))
        declaration=verify_frozen()
        self.assertEqual(len(declaration['evaluation_ids']),24)

    def test_gold_values_cannot_change_unanswered_controller_actions(self):
        case=next(x for x in json.loads((ART/'data/public_projects.json').read_text())
                  if x['split']=='evaluation')
        gold=next(x for x in json.loads((ART/'data/evaluation_only.json').read_text()) if x['id']==case['id'])
        prepared=json.loads((ART/('prepared/evaluation_'+case['project']+'_0.json')).read_text())
        altered=copy.deepcopy(gold)
        for state in altered['annotation_states']:
            for key in state:state[key]='private-canary-value'
        db={d:json.loads((ART/('data/'+d+'_db.json')).read_text()) for d in ['hotel','restaurant']}
        for method in ['dependency_barrier','semantic_memory','full_history','global_barrier']:
            _,a,_=simulate(case,gold,prepared,method,6,0,db)
            _,b,_=simulate(case,altered,prepared,method,6,0,db)
            self.assertEqual(a['events'],b['events'])
            self.assertEqual([x['values'] for x in a['artifacts']],[x['values'] for x in b['artifacts']])

    def test_all_global_and_selective_outputs_match(self):
        grouped={}
        with gzip.open(ART/'evaluation/traces.jsonl.gz','rt') as f:
            for line in f:
                t=json.loads(line);r=t['row']
                if r['method'] not in ['global_barrier','dependency_barrier']:continue
                key=(r['id'],r['replicate'],r['demand'],r['budget'])
                signature=(t['artifacts'],r['questions'],r['answered_questions'])
                if key in grouped:self.assertEqual(grouped.pop(key),signature)
                else:grouped[key]=signature
        self.assertEqual(grouped,{})

    def test_expired_authorization_stops_before_network(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'authorization.json').write_text(json.dumps(dict(inference_cutoff_utc='2000-01-01T00:00:00+00:00',attempt_ceiling=1)))
            with patch.object(client,'ART',root),patch.object(client,'http') as network:
                with self.assertRaisesRegex(RuntimeError,'cutoff'):
                    client.generate('unmade',[dict(role='user',content='Hello')],1)
                network.assert_not_called()

    def test_attempt_ceiling_cannot_generate(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'authorization.json').write_text(json.dumps(dict(inference_cutoff_utc='2100-01-01T00:00:00+00:00',attempt_ceiling=1)))
            (root/'attempts.jsonl').write_text('{}\n')
            with patch.object(client,'ART',root),patch.object(client,'http',return_value={'count':1}) as network:
                with self.assertRaisesRegex(RuntimeError,'ceiling'):
                    client.generate('unmade',[dict(role='user',content='Hello')],1)
                self.assertEqual(network.call_count,1)
                self.assertEqual(network.call_args[0][0],'/tokenize')

if __name__=='__main__':unittest.main()
