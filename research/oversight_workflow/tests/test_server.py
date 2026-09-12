import json
import tempfile
import unittest
from research.oversight_workflow.prototype.server import Application
from research.oversight_workflow.tests.test_protocol import offer,OUT
from research.oversight_workflow.protocol import replay

class JournalTests(unittest.TestCase):
    def test_restore_retains_metadata_without_duplicate_keyword_and_replays(self):
        with tempfile.TemporaryDirectory() as tmp:
            app=Application(tmp)
            for action,p in [('offer',offer()),('admit',{'id':'a'}),('start',{'id':'a'}),('receive',{'id':'a','output':OUT}),('select',{'id':'a'}),('decide',{'id':'a','version':1,'decision':'defer','note':'Check the year','until':40})]:
                self.assertTrue(app.desk.command(action,action,p)['ok'])
            app.journal();old=app.session+'.jsonl';logical=app.desk.logical()
            app.restore(old)
            self.assertEqual(logical,app.desk.logical())
            self.assertEqual(app.desk.state['requests']['a']['notes'],'Check the year')
            app.desk.command('again','select',{'id':'a'});app.journal()
            rows=[json.loads(s) for s in (app.logdir/(app.session+'.jsonl')).read_text().splitlines()]
            self.assertEqual(replay(rows).logical(),app.desk.logical());app.stop()

    def test_old_session_command_cannot_offer_into_new_desk(self):
        from http.server import ThreadingHTTPServer
        from http.client import HTTPConnection
        import threading
        from research.oversight_workflow.prototype.server import Handler
        with tempfile.TemporaryDirectory() as tmp:
            app=Application(tmp);old=app.session;app.start(dict(mode='manual',condition='queue'))
            handler=type('TestHandler',(Handler,),{'app':app});server=ThreadingHTTPServer(('127.0.0.1',0),handler)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            try:
                conn=HTTPConnection('127.0.0.1',server.server_port,timeout=3)
                conn.request('POST','/api/command',json.dumps(dict(session_id=old,event_id='late',action='offer',payload=offer())),{'Content-Type':'application/json'})
                response=conn.getresponse();self.assertEqual(response.status,400);self.assertIn('Session changed',response.read().decode());conn.close()
                self.assertEqual(app.desk.counts()['offered'],0)
            finally:server.shutdown();server.server_close();thread.join();app.stop()
