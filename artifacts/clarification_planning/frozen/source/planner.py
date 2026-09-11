"""Public-only finite-horizon clarification planning with bounded candidate search.

A factor is a categorical belief about a value or applicability. Shared factors
are reused once in each joint task event, never multiplied as independent copies.
No evaluator or source annotation module is imported here.
"""
import copy
import itertools
import math
import time
from dataclasses import dataclass
from functools import lru_cache

OTHER='__OTHER__'
UNRESOLVED='__UNRESOLVED__'

@dataclass(frozen=True)
class Factor:
    id: str
    choices: tuple
    probabilities: tuple
    kind: str = 'value'
    scope: str = 'project'
    source: str = 'inferred public evidence'
    version: int = 1
    status: str = 'inferred'
    cost: int = 1
    exceptions: tuple = ()
    allowed_tasks: tuple = ()

    def __post_init__(self):
        if len(self.choices)!=len(self.probabilities) or not self.choices:raise ValueError('Belief shape')
        if len(set(self.choices))!=len(self.choices):raise ValueError('Duplicate value')
        if any(p<0 for p in self.probabilities) or abs(sum(self.probabilities)-1)>1e-8:raise ValueError('Belief probabilities')
        if self.cost<=0 or not isinstance(self.cost,int):raise ValueError('Positive integer question cost required')

@dataclass(frozen=True)
class Option:
    # Public output field -> factor ID. Fixed literals represent applicability.
    bindings: tuple
    gates: tuple = ()

@dataclass(frozen=True)
class Task:
    id: str
    options: tuple
    error_weight: float = 4.
    defer_weight: float = 1.

@dataclass(frozen=True)
class State:
    beliefs: tuple
    asked: int = 0
    revealed: int = 0

class Planner:
    def __init__(self,factors,tasks,response_error=0.,unresolved_probability=0.,
                 question_penalty=.05,width=8,node_limit=25000):
        self.factors=tuple(factors);self.tasks=tuple(tasks)
        self.index={f.id:i for i,f in enumerate(factors)}
        if len(self.index)!=len(factors):raise ValueError('Duplicate factor')
        if not 0<=response_error<1 or not 0<=unresolved_probability<=1:raise ValueError('Response model')
        self.response_error=response_error;self.unresolved_probability=unresolved_probability
        self.question_penalty=question_penalty;self.width=width;self.node_limit=node_limit
        self.initial=State(tuple(f.probabilities for f in factors));self.nodes=0;self.capped=False
        self.cache_hits=0;self.last_stats={}
        for task in tasks:
            if task.error_weight<0 or task.defer_weight<0:raise ValueError('Nonnegative loss weights')
            for opt in task.options:
                for _,key in opt.bindings:
                    if key not in self.index:raise ValueError('Unregistered dependency')
                for key,value in opt.gates:
                    if key not in self.index or value not in self.factors[self.index[key]].choices:raise ValueError('Unregistered scope')
        self._terminal_cache={};self._response_cache={};self._candidate_cache={}

    def deps(self,opt):
        return {self.index[k] for _,k in opt.bindings}|{self.index[k] for k,_ in opt.gates}

    def terminal(self,state):
        if state in self._terminal_cache:return self._terminal_cache[state]
        outcomes=[];total=0.
        for task in self.tasks:
            best=None
            for oi,opt in enumerate(task.options):
                assignments={};values={};possible=True
                for field,key in opt.bindings:
                    i=self.index[key];factor=self.factors[i]
                    allowed=[k for k,v in enumerate(factor.choices)
                             if v!=OTHER or state.revealed&(1<<i) or factor.status=='confirmed']
                    if not allowed:possible=False;break
                    k=min(allowed,key=lambda k:(-state.beliefs[i][k],str(factor.choices[k])))
                    if i in assignments and assignments[i]!=k:possible=False;break
                    assignments[i]=k;values[field]=factor.choices[k]
                    if task.id in factor.exceptions or (factor.allowed_tasks and task.id not in factor.allowed_tasks):possible=False;break
                for key,value in opt.gates:
                    i=self.index[key];k=self.factors[i].choices.index(value)
                    if i in assignments and assignments[i]!=k:possible=False;break
                    assignments[i]=k
                if not possible:continue
                p=math.prod(state.beliefs[i][k] for i,k in assignments.items())
                candidate=dict(task=task.id,probability_correct=p,values=values,option=oi,
                               dependencies=sorted(self.factors[i].id for i in assignments),
                               versions={self.factors[i].id:self.factors[i].version for i in assignments})
                if best is None or p>best['probability_correct']+1e-12:best=candidate
            release_loss=task.error_weight*(1-best['probability_correct']) if best else float('inf')
            # Ties defer, protecting against zero expected gain; uniform across methods.
            if best and release_loss<task.defer_weight-1e-12:
                out=dict(best,status='release',predicted_loss=release_loss)
            else:out=dict(task=task.id,status='defer',values={},probability_correct=0.,predicted_loss=task.defer_weight,
                          dependencies=[],versions={})
            total+=out['predicted_loss'];outcomes.append(out)
        result=(total,tuple(outcomes));self._terminal_cache[state]=result;return result

    def response_branches(self,state,i):
        key=(state,i)
        if key in self._response_cache:return self._response_cache[key]
        prior=state.beliefs[i];k=len(prior);branches=[]
        # An unresolved answer uses budget and prevents repeating this same atomic
        # question until a new registered revision. It conveys no evidence.
        if self.unresolved_probability:
            branches.append((UNRESOLVED,self.unresolved_probability,State(state.beliefs,state.asked|(1<<i),state.revealed)))
        for y in range(k):
            likelihood=[1. if k==1 else 1-self.response_error if t==y else self.response_error/(k-1) for t in range(k)]
            prob=sum(p*l for p,l in zip(prior,likelihood))
            if prob<1e-14:continue
            posterior=tuple(p*l/prob for p,l in zip(prior,likelihood))
            beliefs=list(state.beliefs);beliefs[i]=posterior
            branches.append((self.factors[i].choices[y],(1-self.unresolved_probability)*prob,
                             State(tuple(beliefs),state.asked|(1<<i),state.revealed|(1<<i))))
        self._response_cache[key]=tuple(branches);return tuple(branches)

    def available(self,state,budget,scope_enabled=True):
        used=set().union(*(self.deps(o) for t in self.tasks for o in t.options)) if self.tasks else set()
        return [i for i in sorted(used) if not state.asked&(1<<i) and self.factors[i].cost<=budget
                and (scope_enabled or self.factors[i].kind!='scope') and
                (max(state.beliefs[i])<1-1e-12 or self.factors[i].choices[state.beliefs[i].index(max(state.beliefs[i]))]==OTHER)]

    def candidates(self,state,budget,construction='dependency',scope_enabled=True):
        key=(state,budget,construction,scope_enabled)
        if key in self._candidate_cache:return self._candidate_cache[key]
        available=self.available(state,budget,scope_enabled)
        if construction=='exact' or len(available)<=self.width:return available
        current=self.terminal(state)[0]
        singles={i:current-sum(p*self.terminal(s)[0] for _,p,s in self.response_branches(state,i)) for i in available}
        if construction=='generic':scores=singles
        else:
            # Optimistic completion-block bound. Enumerate up to three unresolved
            # dependencies of each task. A block's score is not assumed realizable;
            # only the subsequent contingent recursion evaluates its actual value.
            scores=dict(singles)
            for task in self.tasks:
                for option in task.options:
                    deps=sorted(set(available)&self.deps(option))
                    for size in range(1,min(3,len(deps))+1):
                        for block in itertools.combinations(deps,size):
                            cost=sum(self.factors[i].cost for i in block)
                            if cost>budget:continue
                            p=1.
                            for i in self.deps(option):
                                if i in block:continue
                                fixed=next((v for key,v in option.gates if self.index[key]==i),None)
                                p*=state.beliefs[i][self.factors[i].choices.index(fixed)] if fixed is not None else max(state.beliefs[i])
                            old=next(o['predicted_loss'] for o in self.terminal(state)[1] if o['task']==task.id)
                            gain=max(0.,old-min(task.defer_weight,task.error_weight*(1-p)))/cost
                            for i in block:scores[i]=max(scores[i],gain)
        result=sorted(available,key=lambda i:(-scores[i],self.factors[i].id))[:self.width]
        self._candidate_cache[key]=result;return result

    def select(self,state,budget,depth=2,construction='dependency',scope_enabled=True):
        start=time.perf_counter();self.nodes=0;self.capped=False
        @lru_cache(None)
        def value(s,b,h):
            best=self.terminal(s)[0];action=None
            if self.nodes>=self.node_limit:
                self.capped=True;return best,action
            self.nodes+=1
            if not h or b<=0:return best,action
            for i in self.candidates(s,b,construction,scope_enabled):
                cost=self.factors[i].cost
                expected=self.question_penalty*cost+sum(p*value(n,b-cost,h-1)[0]
                              for _,p,n in self.response_branches(s,i))
                if expected<best-1e-10 or (abs(expected-best)<=1e-10 and action is not None and self.factors[i].id<self.factors[action].id):
                    best=expected;action=i
            return best,action
        predicted,chosen=value(state,budget,min(depth,budget))
        self.last_stats=dict(nodes=self.nodes,cache_hits=value.cache_info().hits,capped=self.capped,
                            seconds=time.perf_counter()-start,depth=depth,width=self.width,
                            expected_terminal_now=self.terminal(state)[0],expected_plan_loss=predicted)
        return chosen

    def heuristic(self,state,budget,method,scope_enabled=True):
        available=self.available(state,budget,scope_enabled)
        if not available:return None
        if method=='uncertainty':return min(available,key=lambda i:(max(state.beliefs[i]),self.factors[i].id))
        if method=='memory':
            # Competent retrieval is upstream. Ask missing/unusable memories in
            # task order, sharing confirmed responses. Do not ask just because a
            # calibrated confidence is below the loss-sensitive release threshold.
            for task in self.tasks:
                for opt in task.options[:1]:
                    for i in sorted(self.deps(opt)):
                        choices=self.factors[i].choices;probs=state.beliefs[i]
                        if i in available and all(v==OTHER or p==0 for v,p in zip(choices,probs)):return i
            return None
        # Fewest answers to resolve a single task, then optimistic utility/cost.
        groups=[]
        terminal={o['task']:o for o in self.terminal(state)[1]}
        for task in self.tasks:
            for opt in task.options:
                deps=sorted(set(available)&self.deps(opt))
                if not deps or terminal[task.id]['predicted_loss']<1e-10:continue
                cost=sum(self.factors[i].cost for i in deps)
                groups.append((len(deps),-terminal[task.id]['predicted_loss']/cost,task.id,deps))
        if not groups:return None
        deps=min(groups)[-1]
        return min(deps,key=lambda i:(max(state.beliefs[i]),self.factors[i].id))

    def observe(self,state,i,answer):
        if state.asked&(1<<i):raise ValueError('Atomic question already attempted')
        if answer==UNRESOLVED:return State(state.beliefs,state.asked|(1<<i),state.revealed)
        # Public observed out-of-support answers expand the response alphabet.
        # Their actual string is received only here, after a paid question.
        factor=self.factors[i]
        if answer not in factor.choices:
            if OTHER not in factor.choices:raise ValueError('Unexpected scope answer')
            choices=list(factor.choices);choices[choices.index(OTHER)]=answer
            factors=list(self.factors);factors[i]=Factor(**dict(factor.__dict__,choices=tuple(choices)))
            self.factors=tuple(factors);self._terminal_cache={};self._response_cache={};self._candidate_cache={}
        for y,_,s in self.response_branches(state,i):
            if y==answer:return s
        # Zero probability observations are retained, not silently dropped. Use a
        # confirmed point belief only when the declared channel is perfectly exact.
        if self.response_error==0:
            p=tuple(float(v==answer) for v in self.factors[i].choices);b=list(state.beliefs);b[i]=p
            return State(tuple(b),state.asked|(1<<i),state.revealed|(1<<i))
        raise ValueError('Out-of-support noisy observation')

    def question(self,i):
        f=self.factors[i]
        return dict(id=f.id,kind=f.kind,cost=f.cost,scope=f.scope,exceptions=list(f.exceptions),
                    source=f.source,version=f.version,allowed_tasks=list(f.allowed_tasks),
                    text=('Does this earlier answer apply to '+f.scope+'?' if f.kind=='scope' else
                          'What is the current '+f.id.replace('.',' ')+' for '+f.scope+'?'),
                    enables=[t.id for t in self.tasks if any(i in self.deps(o) for o in t.options)])

class Protocol:
    """Event-driven budget and revision barrier; no private answer simulator."""
    def __init__(self,planner,budget):
        if not isinstance(budget,int) or budget<0:raise ValueError('Nonnegative integer budget')
        self.planner=planner;self.state=planner.initial;self.budget=budget;self.spent=0
        self.events=[];self.pending=None;self.releases={}

    def propose(self,method='depth2'):
        if self.pending is not None:raise ValueError('Answer or defer the displayed question first')
        p=self.planner;b=self.budget-self.spent
        if method in ('depth1','depth2','depth3','generic2','no_scope','exact'):
            depth={'depth1':1,'depth2':2,'depth3':3,'generic2':2,'no_scope':2,'exact':min(b,6)}[method]
            if method=='exact' and (len(p.factors)>6 or b>6):raise ValueError('Exact reference limit')
            i=p.select(self.state,b,depth,'exact' if method=='exact' else 'generic' if method=='generic2' else 'dependency',method!='no_scope')
        elif method=='no_review':i=None
        else:i=p.heuristic(self.state,b,method)
        if i is None:return None
        q=p.question(i);self.pending=i;self.events.append(dict(kind='question_shown',remaining_budget=b,question=q))
        return q

    def answer(self,value):
        if self.pending is None:raise ValueError('No displayed question')
        i=self.pending;cost=self.planner.factors[i].cost
        if self.spent+cost>self.budget:raise ValueError('Path budget would be exceeded')
        self.state=self.planner.observe(self.state,i,value);self.spent+=cost;self.pending=None
        self.events.append(dict(kind='answer_received',id=self.planner.factors[i].id,value=value,cost=cost,spent=self.spent))

    def revise(self,key,value=None,revoke=False,exceptions=None):
        if self.pending is not None:raise ValueError('Resolve displayed question before revision')
        p=self.planner;i=p.index[key];old=p.factors[i];choices=old.choices
        if value is not None and value not in choices:choices=choices+(value,)
        probs=tuple(float(v==value) for v in choices) if not revoke else tuple(float(v==OTHER) for v in choices)
        if revoke and OTHER not in choices:choices=choices+(OTHER,);probs=tuple(float(v==OTHER) for v in choices)
        factors=list(p.factors);factors[i]=Factor(**dict(old.__dict__,choices=choices,probabilities=probs,version=old.version+1,
            status='revoked' if revoke else 'confirmed',exceptions=old.exceptions if exceptions is None else tuple(exceptions)))
        beliefs=list(self.state.beliefs);beliefs[i]=probs
        self.planner=Planner(factors,p.tasks,p.response_error,p.unresolved_probability,p.question_penalty,p.width,p.node_limit)
        self.state=State(tuple(beliefs),self.state.asked&~(1<<i),self.state.revealed&~(1<<i))
        affected=[k for k,r in self.releases.items() if key in r['dependencies']]
        for k in affected:self.releases[k]['status']='needs_revalidation'
        self.events.append(dict(kind='revision',id=key,version=old.version+1,affected=affected,revoke=revoke))

    def finish(self):
        if self.pending is not None:raise ValueError('Outstanding displayed question')
        outcomes=copy.deepcopy(list(self.planner.terminal(self.state)[1]))
        self.releases={o['task']:o for o in outcomes};self.events.append(dict(kind='terminal',outcomes=outcomes,spent=self.spent))
        return outcomes

    def release_current(self,task):
        r=self.releases[task]
        return r['status']=='release' and all(self.planner.factors[self.planner.index[k]].version==v for k,v in r['versions'].items())
