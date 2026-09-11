"""Checks for the paired evidence and the local interaction boundary."""
import csv,gzip,json,tempfile,unittest
from pathlib import Path
import numpy as np
from .data import ROOT
from .scope_fixture import examples
from .prototype.server import Session

class PackageChecks(unittest.TestCase):
    def test_distinct_answers_and_shared_harm(self):
        r=examples()
        self.assertEqual(len(set(r['separate_decisions']['final'].values())),2)
        self.assertTrue(r['separate_decisions']['similarity_propagation_rejected'])
        self.assertEqual(r['explicit_dependency']['harmed_recipients'],2)

    def test_interface_targets_are_hidden_and_actions_are_scoped(self):
        with tempfile.TemporaryDirectory() as d:
            s=Session(Path(d)/'demonstration.jsonl');state=s.state()
            self.assertEqual(len(state['requests']),3)
            self.assertNotIn('truth',json.dumps(state))
            self.assertNotIn('source_label',json.dumps(state))
            self.assertNotIn('review_response',json.dumps(state))
            s.action({'action':'start'})
            before=s.controller.final.copy()
            with self.assertRaises(ValueError):
                s.action({'action':'decision','request_id':'not-active','diagnosis':'normal'})
            self.assertEqual(s.controller.final,before)
            current=s.controller.session[0]
            s.action({'action':'decision','request_id':current,'diagnosis':'abstain'})
            self.assertEqual(s.controller.final[current],'abstain')
            log=[json.loads(x) for x in s.log.read_text().splitlines()]
            self.assertTrue(all(x['record_type']=='development_demonstration_not_participant_data' for x in log))

    def test_joint_bundle_resampling_and_failure_accounting(self):
        with gzip.open(ROOT/'evaluation/traces.jsonl.gz','rt') as f:rows=[json.loads(x) for x in f]
        self.assertEqual(len(rows),4500)
        for r in rows:
            self.assertEqual(len(r['jobs']),9)
            self.assertEqual(r['metrics']['correct']+r['metrics']['unresolved'],9)
            self.assertEqual(r['metrics']['loss'],sum(x['weight'] for x in r['jobs'] if x['unresolved']))
            completions=[e for e in r['events'] if e['event']=='review_completed']
            self.assertEqual(len(completions),r['metrics']['reviews'])
        paired={}
        for r in rows:paired.setdefault((r['condition_id'],r['bundle']),set()).add(r['input_hash'])
        self.assertTrue(all(len(v)==1 for v in paired.values()))
        primary=[r for r in rows if r['condition_id']=='core_high_1_12_ideal']
        lookup={(r['bundle'],r['policy']):r['metrics']['loss'] for r in primary}
        values=np.array([lookup[b,'guarded']-lookup[b,'sticky_edf'] for b in range(6)])
        # Independent bundle differences reconstruct the saved interval without
        # treating 10 policies or 75 variants as new observations.
        rng=np.random.default_rng(20260911);indices=rng.integers(0,6,size=(2000,6))
        ci=np.quantile(values[indices].mean(axis=1),[.025,.975])
        with (ROOT/'analysis/paired.csv').open() as f:
            saved=next(x for x in csv.DictReader(f) if x['condition_id']=='core_high_1_12_ideal' and x['comparison']=='guarded-sticky_edf')
        self.assertEqual(float(saved['loss']),values.mean())
        self.assertEqual(float(saved['loss_low']),ci[0]);self.assertEqual(float(saved['loss_high']),ci[1])

if __name__=='__main__':unittest.main()
