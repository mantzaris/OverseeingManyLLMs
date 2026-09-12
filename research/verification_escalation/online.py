"""Online revision handling, isolated from frozen terminal-only policy replays."""
from .controller import Controller
class OnlineController(Controller):
    def signature(self,decision):
        return sorted((t['id'],t['version'],t['scope']) for t in self.tasks if t.get('decision_id',t['id'])==decision)
    def answer(self,q,response):
        task=next(t for t in self.tasks if t['id']==q['task'])
        # The desk validates the displayed state before preparing a received answer.
        before=len(self.events);super().answer(q,response)
        for e in self.events[before:]:
            if e['event']=='answer':e['dependency_versions']=self.signature(e['decision'])
    def next_question(self):
        if self.method=='no_sharing':
            pending=self.inspect()
            answered={e['task'] for e in self.events if e['event']=='answer' and e.get('dependency_versions')==self.signature(e['decision'])}
            pending=[q for q in pending if q['task'] not in answered]
            if not pending or self.spent>=self.budget:return None
            q=min(pending,key=lambda x:x['task'])
            self.log('show_question',task=q['task'],decision=q['decision'],scope=q['scope'],text=q['issue'])
            return q
        history=self.events
        visible=[e for e in history if e['event']!='answer' or e.get('dependency_versions')==self.signature(e['decision'])]
        self.events=list(visible);n=len(visible)
        try:return super().next_question()
        finally:
            new=self.events[n:];self.events=history+new
    def release_answer(self,t,sql,key,reason):
        old=self.records.get(t['id'])
        if old and old.get('key')==key and old.get('sql')==sql and old.get('reason')=='answer_execution_failed':
            self.log('failed_answer_cache',task=t['id'],key=key)
            return
        return super().release_answer(t,sql,key,reason)
    def revise(self,task_id,**updates):
        super().revise(task_id,**updates);self.pending=[]
