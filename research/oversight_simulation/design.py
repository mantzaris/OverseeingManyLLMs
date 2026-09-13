"""Predeclared compact parameter coverage, with no comparative-result selection."""
from copy import deepcopy
from .inputs import OUT,POLICIES
from research.oversight_workflow.common import write


def build_design():
    base=dict(offered=12,horizon=540,arrival='two_wave',source_order='interleaved',orientation=25.,memory_seconds=600.,memory_intervening=8.,recent_fraction=.1,
              question_seconds=8.,verify_seconds=18.,construction_seconds=45.,manual_seconds=45.,interaction_seconds=4.,group_seconds=4.,
              detect=.85,correct=.85,damage=.02,manual_accuracy=.75,recognized_failure=.5,carryover=0.,jitter_sigma=.2,defer_seconds=45.,max_attempts=2)
    effectiveness={'ideal':dict(detect=1.,correct=1.,damage=0.,manual_accuracy=1.),'high':dict(detect=.85,correct=.85,damage=.02,manual_accuracy=.75),'limited':dict(detect=.55,correct=.60,damage=.08,manual_accuracy=.50)}
    memories={'short':dict(memory_seconds=45.,memory_intervening=2.),'long':dict(memory_seconds=600.,memory_intervening=8.),'persistent':dict(memory_seconds=1e12,memory_intervening=1e12)}
    configs=[]
    def add(family,label,changes):
        c={**base,**changes};configs.append(dict(id='%03d_%s'%(len(configs),label),family=family,**c))
    for orientation in (0,5,25,75):
        for e,ep in effectiveness.items():
            for mem in ('short','long'):
                add('original','o%s_%s_%s'%(orientation,e,mem),dict(orientation=orientation,effectiveness=e,memory=mem,**ep,**memories[mem]))
    for n in (6,12,24,36):
        for h in (270,540,900):add('demand','n%d_h%d'%(n,h),dict(offered=n,horizon=h))
    for arrival in ('two_wave','burst','spread'):
        for order in ('interleaved','source_blocked'):add('arrival','%s_%s'%(arrival,order),dict(offered=24,arrival=arrival,source_order=order))
    for o in (5,25,75):
        for g in (0,12):add('group_cost','o%d_g%d'%(o,g),dict(orientation=o,group_seconds=g))
    for v in (8,18,40):
        for m in (20,45,90):add('task_cost','v%d_m%d'%(v,m),dict(verify_seconds=v,manual_seconds=m))
    for mem in memories:
        for carry in (0.,.08,.20):add('carryover','%s_c%d'%(mem,round(carry*100)),dict(memory=mem,carryover=carry,**memories[mem]))
    assert len(configs)==66
    return dict(schema='oversight-simulation-design-v1',record_kind='computational_simulation',policies=POLICIES,seeds=list(range(10000,10032)),rotations=[0,1,2],development_seeds=[0,1,2,3],configs=configs,
        primary='Original workload: G minus Q and G minus Q-source-aware correct current-version releases; error and unfinished counts alongside. Every parameter cell retained.',
        statistical_unit='Independent Monte Carlo seed block, averaged across all three reused packet rotations. Not human population or independent reports.',
        analysis='Cell means, seed-block paired mean +/-1.96 Monte Carlo standard error, sign/tie counts; conditional on fixed inputs and assumptions. Model uncertainty represented by full declared sensitivity grid, not the Monte Carlo interval.',
        examples='First configuration in declaration order, then rotation, then seed with positive and negative G-Q correct-release differences. Same paired tasks/outcomes; no effect-magnitude selection.',
        execution_limit='90 minutes including analysis; final 20 minutes reserved. Pilot runtime forecast uses development seeds and no outcome inspection. Fixed complete matrix; no outcome-driven early stopping.',
        provenance='Reviewer probabilities, times, familiarity, carryover, arrivals and goals are analyst-selected simulation assumptions, not calibrated human measurements. Model outcomes can use annotations; selectors cannot.')


if __name__=='__main__':write(OUT/'design.json',build_design());print('Declared 66 configurations x 3 rotations x 32 seeds x 5 policies = 31680 simulations')
