"""Small controlled counterexample, not observed multi-agent workload data."""
from .client import ART, write_json

CASES = {
    'low_demand': [(1, True, 2, 14), (2, False, 2, 14)],
    'shared_user_bottleneck': [(1, True, 2, 14)] * 4 + [(2, False, 2, 7)] * 2,
    'urgent_user_decision': [(1, True, 1, 5)] + [(2, False, 2, 7)] * 3,
    'preparation_long': [(4, True, 1, 9)] * 2 + [(1, False, 1, 4)] * 2,
}

def simulate(tasks, method):
    state=[dict(pre=x[0],ask=x[1],post=x[2],deadline=x[3],status='new',end=None) for x in tasks]
    blocked_ticks=0;questions=0
    for tick in range(16):
        waiting=[i for i,t in enumerate(state) if t['status']=='waiting']
        blocked_ticks += len(waiting)
        if tick in (4,8,12) and waiting:
            k=min(waiting,key=lambda i:(state[i]['deadline'],i))
            state[k]['status']='post';questions+=1
        runnable=[i for i,t in enumerate(state) if t['status'] in ('pre','post')]
        occupied=len(runnable)+(len(waiting) if method=='holding_cap' else 0)
        new=[i for i,t in enumerate(state) if t['status']=='new']
        if method=='human_aware':
            new.sort(key=lambda i:(state[i]['ask'],state[i]['deadline'],i))
        for k in new[:max(0,2-occupied)]:state[k]['status']='pre';runnable.append(k)
        for k in runnable[:2]:
            t=state[k];phase=t['status'];t[phase]-=1
            if t[phase]==0:
                if phase=='post':t.update(status='done',end=tick+1)
                else:t['status']='waiting' if t['ask'] else 'post'
    return dict(completed=sum(t['status']=='done' for t in state),
                on_time=sum(t['end'] is not None and t['end']<=t['deadline'] for t in state),
                original_goals=len(tasks),unfinished=sum(t['end'] is None for t in state),
                questions=questions,blocked_agent_ticks=blocked_ticks,trace=state)

if __name__=='__main__':
    write_json(ART/'development/admission_declaration.json',
               dict(cases=CASES,methods=['holding_cap','yield_blocked','human_aware'],
                    semantics='Two preparation workers; user resolves one decision at ticks 4,8,12. No inferred human mental-state penalty. All goals counted.'))
    rows=[dict(case=c,method=m,**simulate(tasks,m)) for c,tasks in CASES.items()
          for m in ('holding_cap','yield_blocked','human_aware')]
    write_json(ART/'development/admission_results.json',rows)
    for r in rows:print(r['case'],r['method'],r['on_time'],r['completed'],r['original_goals'])
