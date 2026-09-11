"""Authored generative mechanism benchmark, never described as human evidence."""
import random
from dataclasses import asdict
from .planner import Factor, Option, Task, OTHER

FAMILIES=['independent','shared','complementary','mixed','scope_exception',
          'wrong_sharing','revision','revocation','noisy_response','unresolved_response',
          'memory_suffices','zero_value','large_generic_trap','misspecified']

def generate(family,seed):
    r=random.Random(seed);factors=[];tasks=[];truth={};actual={};updates=[]
    def add(key,p=.5,known=False,scope='project',kind='value',actual_p=None):
        choices=('yes','no') if kind=='scope' else ('A','B')
        factors.append(Factor(key,choices,(p,1-p),kind=kind,scope=scope,status='confirmed' if known else 'inferred'))
        truth[key]=choices[0] if r.random()<(p if actual_p is None else actual_p) else choices[1]
    def task(name,keys,weight=4.,defer=1.):
        bindings=tuple((k,k) for k in keys);tasks.append(Task(name,(Option(bindings),),weight,defer))
        actual[name]={k:truth[k] for k in keys}
    if family.startswith('grid_'):
        _,overlap,_,arity=family.split('_');arity=int(arity);shared_n={'none':0,'one':1,'full':arity}[overlap]
        common=['shared%d'%i for i in range(shared_n)]
        for key in common:add(key,.5)
        for j in range(3):
            private=['task%d.value%d'%(j,i) for i in range(arity-shared_n)]
            for key in private:add(key,.5)
            task(['implementation','test_plan','user_guide'][j],common+private)
        add('independent',.5);task('separate_report',['independent'])
    elif family in ['independent','noisy_response','unresolved_response','memory_suffices','zero_value','misspecified']:
        for i in range(4):
            p=1. if family=='memory_suffices' else .94 if family=='misspecified' else r.choice([.5,.7,.9])
            add('d%d'%i,p,actual_p=.55 if family=='misspecified' else None)
            task('deliverable%d'%i,['d%d'%i],defer=0. if family=='zero_value' else 1.)
    elif family=='shared':
        add('shared',r.choice([.5,.7,.9]))
        for name in ['implementation','test_plan','user_guide']:task(name,['shared'])
        add('independent',.5);task('separate_report',['independent'])
    elif family in ['complementary','mixed','large_generic_trap']:
        add('q1',.5);add('q2',.5)
        for name in ['implementation','test_plan','user_guide']:task(name,['q1','q2'])
        add('q3',.5);task('separate_report',['q3'])
        if family=='mixed':
            add('q4',.7);task('integration',['q2','q4'])
        if family=='large_generic_trap':
            # Many weak independent distractors can displace a zero-immediate-gain
            # dependency from a generic singleton-ranked candidate shortlist.
            for i in range(9):
                add('a%d'%i,.5);task('small_task%d'%i,['a%d'%i],defer=.2)
    elif family in ['scope_exception','wrong_sharing']:
        add('project.preference',.85);add('exception.preference',.5)
        add('scope.applies',.6 if family=='scope_exception' else .98,kind='scope',actual_p=.25 if family=='wrong_sharing' else None)
        task('main_project',['project.preference'])
        for name in ['exception_implementation','exception_tests']:
            tasks.append(Task(name,(Option((('value','project.preference'),),(('scope.applies','yes'),)),
                                         Option((('value','exception.preference'),))),4.,1.))
            actual[name]={'value':truth['project.preference'] if truth['scope.applies']=='yes' else truth['exception.preference']}
    elif family in ['revision','revocation']:
        add('project.preference',1.,True)
        for name in ['implementation','test_plan','user_guide']:task(name,['project.preference'])
        add('independent',.5);task('separate_report',['independent'])
        changed='B' if truth['project.preference']=='A' else 'A'
        updates=[dict(key='project.preference',value=None if family=='revocation' else changed,revoke=family=='revocation')]
        truth['project.preference']=changed
        for name in ['implementation','test_plan','user_guide']:actual[name]['project.preference']=changed
    error=.2 if family=='noisy_response' else 0.
    unresolved=.3 if family=='unresolved_response' else 0.
    return dict(id=family+'_'+str(seed),family=family,seed=seed,
        factors=[asdict(f) for f in factors],tasks=[asdict(t) for t in tasks],
        response_error=error,unresolved_probability=unresolved,updates=updates),dict(truth=truth,targets=actual)

def decode(case):
    factors=[Factor(**dict(f,choices=tuple(f['choices']),probabilities=tuple(f['probabilities']),exceptions=tuple(f.get('exceptions',[])))) for f in case['factors']]
    tasks=[Task(t['id'],tuple(Option(tuple(tuple(b) for b in o['bindings']),tuple(tuple(g) for g in o.get('gates',[]))) for o in t['options']),t['error_weight'],t['defer_weight']) for t in case['tasks']]
    return factors,tasks
