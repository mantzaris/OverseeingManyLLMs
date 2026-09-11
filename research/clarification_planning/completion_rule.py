"""Public-only minimum sufficient completion rule; no evaluator imports."""
import itertools
from .planner import Planner

class MinimumCompletion(Planner):
    def heuristic(self,state,budget,method,scope_enabled=True):
        if method!='minimum_completion':return super().heuristic(state,budget,method,scope_enabled)
        available=set(self.available(state,budget,scope_enabled));current={o['task']:o for o in self.terminal(state)[1]};options=[]
        def after(block):
            branches=[(1.,state)]
            for i in block:
                branches=[(p*prob,n) for p,s in branches for _,prob,n in self.response_branches(s,i)]
            return branches
        for task in self.tasks:
            if current[task.id]['status']=='release':continue
            deps=sorted(available & set().union(*(self.deps(o) for o in task.options)))
            for size in range(1,min(6,len(deps),budget)+1):
                blocks=[]
                for block in itertools.combinations(deps,size):
                    cost=sum(self.factors[i].cost for i in block)
                    if cost>budget:continue
                    branches=after(block);outcomes=[(prob,next(o for o in self.terminal(s)[1] if o['task']==task.id)) for prob,s in branches]
                    if not all(o['status']=='release' for _,o in outcomes):continue
                    gain=current[task.id]['predicted_loss']-sum(prob*o['predicted_loss'] for prob,o in outcomes)
                    blocks.append((cost,-gain/cost,task.id,tuple(self.factors[i].id for i in block),block))
                if blocks:options.extend(blocks);break
        return min(options)[-1][0] if options else None

