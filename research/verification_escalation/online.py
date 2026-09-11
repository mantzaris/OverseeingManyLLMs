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
        history=self.events
        visible=[e for e in history if e['event']!='answer' or e.get('dependency_versions')==self.signature(e['decision'])]
        self.events=list(visible);n=len(visible)
        try:return super().next_question()
        finally:
            new=self.events[n:];self.events=history+new
    def revise(self,task_id,**updates):
        super().revise(task_id,**updates);self.pending=[]
