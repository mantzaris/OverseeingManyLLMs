"""Finite Stage 4 matrices: development first, evaluation frozen separately."""
from .domain import STAGE3_POLICIES
from .research_workload import scenario_for

RISK_NAMES=('frozen','pooled','analytical')
LARGER_POLICIES=('fcfs','edf','greedy','delay')


def run_entry(phase,workload,seed,agents,policy,duration,risk='frozen',penalty=0):
    entry=dict(phase=phase,workload=workload,seed=seed,agents=agents,policy=policy,
               review_ticks=duration,risk=risk,closure_penalty=penalty)
    scenario=scenario_for(entry)
    entry.update(scenario_hash=scenario.hash,jobs=len(scenario.jobs),horizon=scenario.horizon,
                 planned_calls=2*len(scenario.jobs),loss_upper_bound=sum(j.public.cost_per_tick*(j.public.deadline-j.public.release)+j.public.terminal_cost for j in scenario.jobs))
    entry['run_id']='{}/{}/{}/a{}/s{}/{}/{}/lambda{}'.format(phase,workload,seed,agents,duration,risk,policy,penalty)
    return entry


def rotated(items,shift):
    shift%=len(items)
    return list(items[shift:])+list(items[:shift])


def ordered_conditions(seed,index,phase,workload,agents,policies,risks,penalties=(0,)):
    entries=[]
    durations=(1,2) if index%2==0 else (2,1)
    for position,duration in enumerate(durations):
        for risk in rotated(risks,index+position):
            for penalty in rotated(penalties,index):
                for policy in rotated(policies,2*index+position):
                    entries.append(run_entry(phase,workload,seed,agents,policy,duration,risk,penalty))
    return entries


def development_plan():
    entries=[]
    for index,seed in enumerate(range(400,408)):
        for workload in rotated(('original','competition'),index):
            entries+=ordered_conditions(seed,index,'risk_pilot',workload,3,('greedy','delay'),RISK_NAMES)
    for index,seed in enumerate(range(408,412)):
        for agents in rotated((3,6),index):
            entries+=ordered_conditions(seed,index,'larger_pilot','larger',agents,LARGER_POLICIES,('frozen',))
    return finish_plan(entries)


def evaluation_plan(original_n=64,competition_n=64,ablation_n=32,larger_n=32):
    # Prefix decisions must be frozen before any evaluation outcome is inspected.
    if original_n not in (16,32,64) or competition_n not in (16,32,64) or larger_n not in (8,16,32):
        raise ValueError('Undeclared evaluation prefix')
    if ablation_n not in (8,16,32) or ablation_n>min(original_n,competition_n):raise ValueError('Invalid paired ablation prefix')
    entries=[]
    for workload,base,n in (('original',10000,original_n),('competition',11000,competition_n)):
        for index,seed in enumerate(range(base,base+n)):
            entries+=ordered_conditions(seed,index,'replication',workload,3,STAGE3_POLICIES,('frozen',))
            if index<ablation_n:
                entries+=ordered_conditions(seed,index,'risk_ablation',workload,3,('greedy','delay'),('pooled','analytical'))
    for index,seed in enumerate(range(12000,12000+larger_n)):
        for agents in rotated((3,6),index):
            entries+=ordered_conditions(seed,index,'capacity','larger',agents,LARGER_POLICIES,('frozen',))
    return finish_plan(entries)


def finish_plan(entries):
    for index,entry in enumerate(entries):entry['execution_index']=index
    if len({e['run_id'] for e in entries})!=len(entries):raise ValueError('Duplicate episode')
    return entries
