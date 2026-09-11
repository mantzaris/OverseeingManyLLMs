"""Online safeguards, isolated from the frozen terminal-only experiment."""
from dataclasses import replace
from .planner import Protocol,Planner,UNRESOLVED
from .completion_rule import MinimumCompletion

class SafePlanner(MinimumCompletion):
    """Apply represented allow/exception guards to applicability records as well."""
    def terminal(self,state):
        if state in self._terminal_cache:return self._terminal_cache[state]
        def allowed(task,key):
            f=self.factors[self.index[key]]
            return task.id not in f.exceptions and (not f.allowed_tasks or task.id in f.allowed_tasks)
        tasks=tuple(replace(t,options=tuple(o for o in t.options if all(allowed(t,k) for k,_ in o.gates))) for t in self.tasks)
        if tasks==self.tasks:return super().terminal(state)
        # Keep the original dependency graph for future updates. The restricted
        # terminal view is rebuilt when the record/version configuration changes.
        view=Planner(self.factors,tasks,self.response_error,self.unresolved_probability,self.question_penalty,self.width,self.node_limit)
        result=view.terminal(state);self._terminal_cache[state]=result;return result


def safe(planner):
    if isinstance(planner,SafePlanner):return planner
    return SafePlanner(planner.factors,planner.tasks,planner.response_error,planner.unresolved_probability,planner.question_penalty,planner.width,planner.node_limit)

class SafeProtocol(Protocol):
    def __init__(self,planner,budget):super().__init__(safe(planner),budget)

    def answer(self,value):
        if self.pending is None:return super().answer(value)
        key=self.planner.factors[self.pending].id
        super().answer(value)
        if value==UNRESOLVED:return
        p=self.planner;i=p.index[key];old=p.factors[i];factors=list(p.factors)
        factors[i]=replace(old,version=old.version+1,status='confirmed',
            source='Received answer to '+key+'. Earlier evidence: '+old.source)
        self.planner=SafePlanner(factors,p.tasks,p.response_error,p.unresolved_probability,p.question_penalty,p.width,p.node_limit)
        affected=[]
        for task,r in self.releases.items():
            if key in r['dependencies']:r['status']='needs_revalidation';affected.append(task)
        self.events.append(dict(kind='answer_version_updated',id=key,version=old.version+1,affected=affected))

    def revise(self,key,value=None,revoke=False,exceptions=None):
        super().revise(key,value,revoke,exceptions)
        p=self.planner;i=p.index[key];factors=list(p.factors)
        factors[i]=replace(factors[i],source='User '+('revocation' if revoke else 'revision')+' of '+key+'. Earlier evidence: '+factors[i].source)
        self.planner=SafePlanner(factors,p.tasks,p.response_error,p.unresolved_probability,p.question_penalty,p.width,p.node_limit)
