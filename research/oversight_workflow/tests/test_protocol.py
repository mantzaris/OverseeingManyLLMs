import threading
import unittest
from copy import deepcopy
from research.oversight_workflow.protocol import Desk,replay
from research.oversight_workflow.common import digest

OUT=dict(answer=['12'],scale='million',derivation='Generated explanation')
def offer(i='a',source_id='source'):
    src=dict(id=source_id,table=[['Year','Value'],['2024','12']],paragraphs=[])
    return dict(id=i,agent='Worker '+i,question_id='q'+i,question='What is the value?',source={**src,'sha256':digest(src),'provenance':{'dataset':'synthetic fixture'}},dependencies=[])

class ProtocolTests(unittest.TestCase):
    def setUp(self):self.d=Desk();self.n=0
    def cmd(self,action,p=None,ok=True):
        self.n+=1;r=self.d.command(str(self.n),action,p,at=self.n/10)
        self.assertEqual(r['ok'],ok,r);return r
    def receive(self,i='a',source_id='source'):
        self.cmd('offer',offer(i,source_id));self.cmd('admit',{'id':i});self.cmd('start',{'id':i});self.cmd('receive',{'id':i,'output':OUT})
    def test_concurrent_arrivals_preserve_active(self):
        self.receive();self.cmd('select',{'id':'a'});before=deepcopy(self.d.state['active'])
        def incoming(i):
            for action,p in [('offer',offer(i)),('admit',{'id':i}),('start',{'id':i}),('receive',{'id':i,'output':OUT})]:
                self.assertTrue(self.d.command(i+action,action,p)['ok'])
        threads=[threading.Thread(target=incoming,args=(str(i),)) for i in range(8)]
        for t in threads:t.start()
        for t in threads:t.join()
        self.assertEqual(before,self.d.state['active']);self.assertEqual(self.d.counts()['received'],9)
    def test_revision_cannot_inherit_approval(self):
        self.receive();self.cmd('select',{'id':'a'});self.cmd('decide',{'id':'a','version':1,'decision':'approve'});self.cmd('release',{'id':'a','version':1})
        self.cmd('revise',{'id':'a','output':{**OUT,'answer':['13']}})
        self.assertFalse(self.d.current_released('a'));self.assertEqual(len(self.d.state['releases']),1)
        self.cmd('release',{'id':'a','version':2},False);self.cmd('release',{'id':'a','version':1},False)
    def test_revision_during_review_and_rollback(self):
        self.receive();self.cmd('select',{'id':'a'});before=deepcopy(self.d.state['active'])
        self.cmd('revise',{'id':'a','output':{**OUT,'answer':['13']}});self.assertEqual(before,self.d.state['active'])
        self.cmd('decide',{'id':'a','version':1,'decision':'approve'},False);self.assertEqual(before,self.d.state['active'])
        self.cmd('refresh');self.cmd('decide',{'id':'a','version':2,'decision':'approve'});self.cmd('release',{'id':'a','version':2})
    def test_deferral_restores_notes_and_source(self):
        self.receive();self.cmd('select',{'id':'a'});src=self.d.state['active']['source']
        self.cmd('decide',{'id':'a','version':1,'decision':'defer','until':99,'note':'Check heading'})
        self.assertEqual(self.d.counts()['remaining'],1);self.assertIsNone(self.d.next_request(10))
        self.cmd('select',{'id':'a'});self.assertEqual(self.d.state['active']['notes'],'Check heading');self.assertEqual(self.d.state['active']['source'],src)
    def test_pause_counts_unstarted_and_preserves_inflight(self):
        for i in ['a','b']:self.cmd('offer',offer(i))
        self.cmd('admit',{'id':'a'});self.cmd('start',{'id':'a'});self.cmd('pause')
        self.cmd('admit',{'id':'b'},False);self.cmd('receive',{'id':'a','output':OUT})
        self.assertEqual(self.d.counts()['offered'],2);self.assertEqual(self.d.counts()['unstarted'],1)
        self.cmd('resume');self.cmd('admit',{'id':'b'});self.cmd('start',{'id':'b'})
    def test_grouping_never_merges_authority(self):
        self.receive('a');self.receive('b');self.receive('c','different')
        self.cmd('session',{'ids':['a','c']},False);self.cmd('session',{'ids':['a','b']});self.cmd('select',{'id':'a'})
        self.cmd('decide',{'id':'a','version':1,'decision':'approve'});self.cmd('release',{'id':'b','version':1},False)
        self.assertEqual(self.d.counts()['resolved'],1)
    def test_idempotency(self):
        p=offer();r=self.d.command('once','offer',p);self.assertEqual(self.d.command('once','offer',p),r);self.assertEqual(len(self.d.events),1)
        with self.assertRaises(ValueError):self.d.command('once','offer',offer('b'))
    def test_annotation_isolation_and_provenance(self):
        p=offer();p['source']['answer']='secret';self.cmd('offer',p,False)
        p=offer();p['source']['table'][1][1]='99';self.cmd('offer',p,False)
        self.receive();self.cmd('revise',{'id':'a','output':{**OUT,'reference_answer':'secret'}},False)
        self.assertEqual(self.d.state['requests']['a']['current_version'],1)
    def test_failure_remains_reviewable_not_silently_deleted(self):
        self.cmd('offer',offer());self.cmd('admit',{'id':'a'});self.cmd('start',{'id':'a'})
        self.cmd('receive',{'id':'a','output':dict(answer=[],scale='',issues=['timeout'])});self.assertEqual(self.d.counts()['unresolved'],1)
        self.cmd('select',{'id':'a'});self.cmd('decide',{'id':'a','version':1,'decision':'reject'});self.cmd('release',{'id':'a','version':1},False)
        self.assertEqual(self.d.counts()['resolved'],1);self.assertEqual(self.d.counts()['released'],0)
    def test_replay_interleavings(self):
        self.receive();self.receive('b');self.cmd('select',{'id':'a'});self.cmd('pause');self.cmd('revise',{'id':'a','output':OUT})
        self.cmd('decide',{'id':'a','version':1,'decision':'approve'},False);self.cmd('decide',{'id':'a','version':1,'decision':'defer'})
        self.assertEqual(replay(self.d.events).logical(),self.d.logical())

    def test_replay_resume_clock_never_goes_backwards(self):
        self.receive();self.cmd('select',{'id':'a'})
        r=replay(self.d.events);r.command('after-restore','note',{'text':'resumed'})
        self.assertGreaterEqual(r.events[-1]['at'],self.d.events[-1]['at'])
        self.assertEqual(r.events[0]['utc'],self.d.events[0]['utc'])

    def test_hidden_label_change_leaves_online_inputs_identical(self):
        from research.adaptive_correction_transfer.data import context
        from research.oversight_workflow.inference import messages
        from research.oversight_workflow.data import task
        raw=dict(table=dict(uid='ctx',table=[['year','amount'],['2020','12']]),paragraphs=[],questions=[dict(uid='q',order=1,question='What is the 2020 amount?',answer='12',scale='',derivation='secret')])
        changed=deepcopy(raw);changed['questions'][0].update(answer='999',scale='billion',derivation='different hidden information')
        a=context(raw,'fixture',0);b=context(changed,'fixture',0)
        self.assertEqual(a,b);self.assertEqual(messages(a,a['questions'][0]),messages(b,b['questions'][0]))
        ds=[]
        for c in (a,b):
            d=Desk();p=task(c,c['questions'][0],0)
            d.command('1','offer',p,at=0);d.command('2','admit',{'id':p['id']},at=.1);d.command('3','start',{'id':p['id']},at=.2)
            d.command('4','receive',{'id':p['id'],'output':OUT},at=.3);ds.append(d.logical())
        self.assertEqual(ds[0],ds[1])

    def test_racing_revision_and_approval(self):
        import random
        for seed in range(40):
            d=Desk();p=offer()
            for action,payload in [('offer',p),('admit',{'id':'a'}),('start',{'id':'a'}),('receive',{'id':'a','output':OUT}),('select',{'id':'a'})]:d.command(action,action,payload)
            jobs=[('revise',{'id':'a','output':{**OUT,'answer':['13']}}),('decide',{'id':'a','version':1,'decision':'approve'})]
            random.Random(seed).shuffle(jobs)
            ts=[threading.Thread(target=d.command,args=('race'+action,action,payload)) for action,payload in jobs]
            for t in ts:t.start()
            for t in ts:t.join()
            self.assertFalse(d.command('release','release',{'id':'a','version':2})['ok'])
            self.assertFalse(d.current_released('a'))
            self.assertEqual(replay(d.events).logical(),d.logical())

    def test_timed_close_retains_outstanding_and_refuses_late_release(self):
        self.receive();self.cmd('offer',offer('b'));self.cmd('admit',{'id':'b'});self.cmd('start',{'id':'b'})
        self.cmd('select',{'id':'a'});self.cmd('close_session')
        self.cmd('decide',{'id':'a','version':1,'decision':'approve'},False)
        self.cmd('receive',{'id':'b','output':OUT})
        self.assertEqual(self.d.counts()['offered'],2);self.assertEqual(self.d.counts()['remaining'],2)
        self.assertEqual(replay(self.d.events).logical(),self.d.logical())

if __name__=='__main__':unittest.main()
