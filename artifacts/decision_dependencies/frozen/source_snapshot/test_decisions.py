import copy
import json
import unittest
from .client import ART, canonical
from .records import DecisionController, extracted_records
from .evaluate import simulate

def record(value,turn=0,quote=None):
    return dict(domain='hotel',slot='pricerange',key='hotel.pricerange',value=value,
                turn=turn,quote=quote or value,kind='preference',scope_status='inferred')

def request(name='r',project='p',key='hotel.pricerange',**kw):
    return dict(id=name,project=project,key=key,text='What price band for lodging?',**kw)

class DecisionSemantics(unittest.TestCase):
    def test_quote_guard_rejects_assistant_future_and_misattribution(self):
        messages=[dict(turn=0,role='user',text='Cheap lodging please.'),
                  dict(turn=1,role='assistant',text='Try an expensive hotel.')]
        payload={'records':[record('expensive',1,'expensive'),record('cheap',2,'Cheap'),record('cheap',0,'I want cheap')]}
        good,bad=extracted_records(payload,messages)
        self.assertEqual(good,{})
        self.assertEqual(len(bad),3)

    def test_valid_quote_is_not_an_entailment_guarantee(self):
        payload={'records':[record('expensive',0,'Cheap lodging')]}
        good,_=extracted_records(payload,[dict(turn=0,role='user',text='Cheap lodging please.')])
        self.assertEqual(good['hotel.pricerange']['value'],'expensive')

    def test_conditional_source_is_not_promoted_to_global_preference(self):
        text='Use an expensive hotel only for the conference night.'
        good,bad=extracted_records({'records':[record('expensive',0,'expensive hotel')]},
                                  [dict(turn=0,role='user',text=text)])
        self.assertFalse(good)
        self.assertEqual(bad[0]['reason'],'conditional_scope_requires_confirmation')

    def test_project_exception_and_approval_scope(self):
        c=DecisionController('p');r=record('cheap');r['exceptions']=['conference-night'];c.publish({r['key']:r})
        self.assertEqual(c.lookup(request(project='another'))['status'],'needs_user')
        self.assertEqual(c.lookup(request(entity='conference-night'))['status'],'needs_user')
        c.answer(request(),'cheap',scope='project')
        self.assertEqual(c.lookup(request(entity='conference-night'))['status'],'needs_user')
        with self.assertRaises(ValueError):c.answer(request(entity='conference-night'),'expensive',scope='project')
        approval=request(kind='approval')
        self.assertEqual(c.lookup(approval)['reason'],'action_specific_approval')
        with self.assertRaises(ValueError):c.answer(approval,'yes',scope='project')
        c.answer(approval,'yes',scope='request')
        self.assertEqual(c.lookup(approval)['value'],'yes')
        self.assertEqual(c.lookup(request(name='different-action',kind='approval'))['status'],'needs_user')

    def test_scope_narrowing_and_revocation_invalidate_work(self):
        c=DecisionController('p');c.publish({'hotel.pricerange':record('cheap')})
        a=c.lookup(request());c.prepare('draft',{'hotel.pricerange':a});self.assertTrue(c.release('draft'))
        c.revise('hotel.pricerange',exceptions=['conference-night'])
        self.assertFalse(c.release('draft'))
        self.assertEqual(c.tasks['draft']['status'],'needs_revalidation')
        c.revise('hotel.pricerange',revoke=True)
        self.assertEqual(c.lookup(request())['status'],'needs_user')
        self.assertTrue(any(e['kind']=='work_released' for e in c.events))

    def test_unrelated_change_preserves_consumed_version(self):
        c=DecisionController('p');c.publish({'hotel.pricerange':record('cheap')})
        old=c.lookup(request());c.prepare('draft',{'hotel.pricerange':old})
        new=record('centre');new.update(key='restaurant.area',domain='restaurant',slot='area')
        c.publish({'hotel.pricerange':record('cheap'),'restaurant.area':new})
        self.assertTrue(c.release('draft'))
        self.assertTrue(c.current(old['basis']))

    def test_conflicting_records_cannot_be_silently_resolved(self):
        payload={'records':[record('cheap'),record('expensive'),record('cheap')]}
        records,_=extracted_records(payload,[],source_guard=False)
        c=DecisionController('p');c.publish(records)
        self.assertEqual(c.lookup(request())['reason'],'conflicting_answers')

    def test_failed_extraction_clears_old_inferred_snapshot(self):
        c=DecisionController('p');c.publish({'hotel.pricerange':record('cheap')})
        old=c.lookup(request());c.prepare('draft',{'hotel.pricerange':old})
        empty,_=extracted_records(None,[]);c.publish(empty)
        self.assertFalse(c.release('draft'))
        self.assertEqual(c.lookup(request())['status'],'needs_user')

    def test_sources_are_split_and_public_has_no_annotations(self):
        cases=json.loads((ART/'data/public_projects.json').read_text())
        ids=[c['id'] for c in cases];self.assertEqual(len(ids),len(set(ids)))
        user_texts=['\n'.join(t['text'] for t in c['stages'][1] if t['role']=='user') for c in cases]
        self.assertEqual(len(user_texts),len(set(user_texts)))
        forbidden={'goal','metadata','annotation_states','changed_fields','lexical_support_turns'}
        def check(obj):
            if isinstance(obj,dict):
                self.assertFalse(set(obj)&forbidden)
                for v in obj.values():check(v)
            elif isinstance(obj,list):
                for v in obj:check(v)
        check(cases)

    def test_controlled_release_and_failure_accounting(self):
        keys=['hotel.pricerange','restaurant.area']
        before=[dict(turn=0,role='user',text='Cheap hotel and a restaurant in the centre.')]
        after=before+[dict(turn=2,role='user',text='Make the hotel expensive instead.')]
        case=dict(id='fixture',project='p',keys=keys,stages=[before,after],
                  queries=[[dict(id='q%d'%i,text=k) for i,k in enumerate(keys)] for _ in range(2)])
        gold=dict(annotation_states=[dict(zip(keys,['cheap','centre'])),dict(zip(keys,['expensive','centre']))],changed_fields=['hotel.pricerange'])
        dining=dict(domain='restaurant',slot='area',value='centre',turn=0,quote='centre')
        outputs={}
        for stage in range(2):outputs['extract%d'%stage]={'records':[record('cheap' if stage==0 else 'expensive',0 if stage==0 else 2,'Cheap' if stage==0 else 'expensive'),dining]}
        for v in range(2):outputs['parse%d'%v]={'queries':[dict(id='q0',domain='hotel',slot='pricerange'),dict(id='q1',domain='restaurant',slot='area')]}
        prepared=dict(outputs=outputs,replicate=0,calls=[]);db={'hotel':[],'restaurant':[]}
        outcomes={m:simulate(case,gold,prepared,m,2,None,db) for m in ['records_read','global_barrier','dependency_barrier']}
        self.assertEqual(outcomes['records_read'][0]['incorrect_artifacts'],1)
        self.assertEqual(outcomes['global_barrier'][0]['correct_artifacts'],2)
        self.assertEqual(outcomes['dependency_barrier'][0]['correct_artifacts'],2)
        self.assertEqual(outcomes['dependency_barrier'][0]['revalidation_reads'],1)
        self.assertEqual(outcomes['global_barrier'][0]['revalidation_reads'],2)
        replay=simulate(case,gold,prepared,'dependency_barrier',2,None,db)
        self.assertEqual(canonical(replay[1]),canonical(outcomes['dependency_barrier'][1]))
        failed=copy.deepcopy(prepared);failed['outputs']['extract1']=None;failed['calls']=[dict(status='failed',parsed=None)]
        row,_,_=simulate(case,gold,failed,'dependency_barrier',2,0,db)
        self.assertEqual(row['failed_generation_calls'],1)
        self.assertEqual(row['unresolved_artifacts'],2)
        self.assertEqual(row['correct_artifacts'],0)

    def test_paired_resampling_keeps_dialogue_replicates_together(self):
        import numpy as np
        from .analyze import project_means,resamples,METRICS
        rows=[]
        for rep,value in enumerate([0,1]):
            row=dict(id='a',method='x',demand=2,budget='unlimited',replicate=rep)
            row.update({k:value for k in METRICS});rows.append(row)
        means=project_means(rows)
        self.assertEqual(len(means),1)
        self.assertEqual(means[('a','x',2,'unlimited')]['project_correct'],.5)
        samples=resamples(['a','b','c','d'],{'a':0,'b':0,'c':1,'d':1})
        self.assertEqual(samples.shape,(2000,4))
        self.assertTrue(np.all(samples[:,:2]<2));self.assertTrue(np.all(samples[:,2:]>=2))

if __name__=='__main__':unittest.main()
