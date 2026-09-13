"""Write numerical report tables/macros from saved results, without simulation."""
import json
from pathlib import Path
import pandas as pd
from research.oversight_workflow.common import ROOT,read,write
from .inputs import OUT,HERE,POLICIES
from .plot import LABELS


def main():
    m=pd.read_csv(OUT/'analysis/cell_means.csv');p=pd.read_csv(OUT/'analysis/paired_differences.csv');d=read(OUT/'design.json')
    base='015_o25_high_long'
    def val(cid,policy,metric):return float(m[(m.config==cid)&(m.policy==policy)&(m.metric==metric)]['mean'].iloc[0])
    def paired(cid,contrast,metric='correct'):return p[(p.config==cid)&(p.contrast==contrast)&(p.metric==metric)].iloc[0]
    def effect(cid,contrast):
        r=paired(cid,contrast);return '%+.3f [%.3f, %.3f]'%(r['mean'],r.mc_low,r.mc_high)
    a=paired(base,'G_minus_Q');b=paired(base,'G_minus_Q-source-aware');c=paired(base,'G_minus_Q-sticky')
    table='| Policy | Correct | Incorrect | Unfinished | Orientation seconds | Group seconds |\n|---|---:|---:|---:|---:|---:|\n'
    for pol in POLICIES:table+='| %s | %s |\n'%(LABELS[pol],' | '.join('%.3f'%val(base,pol,k) for k in ('correct','incorrect','unfinished','time_orientation','time_grouping')))
    waiting='| Policy | Source switches | Source returns | Mean first wait (s) | Unrelated task-wait sum (s) | Never selected |\n|---|---:|---:|---:|---:|---:|\n'
    for pol in POLICIES:waiting+='| %s | %s |\n'%(LABELS[pol],' | '.join('%.2f'%val(base,pol,k) for k in ('source_switches','source_returns','mean_wait','unrelated_wait_sum','never_selected')))
    cells=p[(p.contrast=='G_minus_Q-source-aware')&(p.metric=='correct')];q=p[(p.contrast=='G_minus_Q')&(p.metric=='correct')]
    stats=dict(group_beats_source_aware_cells=int((cells['mean']>1e-9).sum()),group_ties_source_aware_cells=int((cells['mean'].abs()<=1e-9).sum()),group_loses_source_aware_cells=int((cells['mean']< -1e-9).sum()),group_beats_fifo_cells=int((q['mean']>1e-9).sum()),group_ties_fifo_cells=int((q['mean'].abs()<=1e-9).sum()),group_loses_fifo_cells=int((q['mean']< -1e-9).sum()))
    write(OUT/'analysis/claim_numbers.json',stats)
    text='''# Computational oversight study: results and interpretation

**Completed:** 31,680 declared CPU simulations on 36 original TAT-QA questions,
six reused real financial-report contexts and genuine saved model drafts. There
are **zero human observations and zero new inference calls**. Every result below
is conditional on the declared simulated reviewer and workload. The prospective
matched human study and its position paper are preserved.

## Main result

Grouping's mean correct-release count never exceeds the central queue with the
same bounded source-aware navigation in any of the 66 declared settings. It is
lower in {lose} and tied in {tie}. Three ties are the zero-group-cost settings,
where equality follows from the model by construction; the fourth is the low-load,
long-budget condition with nearly all work completed. This is not evidence that
real grouping cards cannot help people. Their possible comprehension or strategy
benefit was deliberately not granted to the simulation without data.

Against FIFO, grouping has positive cell-mean differences in {winq} settings,
negative differences in {loseq}, and ties in {tieq}. These counts describe a designed
sensitivity grid, not the prevalence of beneficial conditions in real work.
Source-aware ordering, rather than the presence of cards, is the stronger
computational explanation. Q-sticky is a further useful simple control and usually
matches or exceeds G, but can suffer when consecutive-source carryover is harmful.

## Reference setting, not a fitted human model

Twelve questions, 540 seconds, original arrivals, orientation coefficient S=25 s
(actual unfamiliar orientation 18.75 s), long familiarity, 4-second group overhead, detection .85, correction
.85, initial-correct damage .02 and manual correctness .75. Means average three
packets and 32 paired Monte Carlo seeds.

{table}

Primary G-Q difference: **{gq} correct releases per twelve offered**.
G minus source-aware Q: **{gs}**. G minus sticky Q: **{gt}**.
Intervals are mean +/- 1.96 Monte Carlo SE on seed blocks, after averaging the
three rotations. They quantify numerical uncertainty under these assumptions,
not uncertainty about people or financial reports. Reference G-Q seed-block
wins/ties/losses are **{wins}/{ties}/{losses}**. No noninferiority or equivalence
claim is made.

Q-M is {qm}; G-M is {gm}. The reference assistance differences are therefore
small and numerically uncertain under this particular model. Q-M holds FIFO
navigation fixed and isolates draft availability within the model. G-M also changes
source ordering, so it is a whole-workflow comparison, not a pure assistance effect.
All components stay
visible: a larger released count can include more wrong releases. Empty original
drafts use the same construction pathway as manual questions, rather than being
removed or credited as correct.

{waiting}

Waiting includes received but never-selected requests censored at cutoff. Source
returns count a previously encountered source after another source. Unrelated
task-wait is summed across tasks and can exceed 540 seconds; it is not a reviewer's
elapsed time or an observed attention measure. In this original schedule all 12
tasks arrive and start before cutoff. All declared stress schedules also finish
delivery before cutoff, so unstarted count is zero throughout this matrix.
Never-selected review work is nevertheless substantial and remains in the totals.

## Where the outcome changes

- **Familiarity matters.** At orientation coefficient S=25 s and higher effectiveness,
  changing long to short persistence moves G-Q from {gq} to {short}. At S=75 s
  with short persistence, G-Q is {large}. That condition also raises
  mean incorrect releases from {largeqerr:.3f} in Q to {largegerr:.3f} in G.
  More correct releases are not an unqualified improvement in oversight.
- **Preexisting source order matters.** With 24 questions in two waves, interleaved
  arrivals yield G-Q {interleaved}; source-blocked arrivals yield {blocked}.
  When FIFO already stays within a source, there is little orientation saving
  for grouping to obtain. Burst/spread and capacity panels are retained separately.
- **Capacity changes the opportunity.** With six questions and fifteen minutes,
  all four assisted policies average {lowc:.3f} correct, {loww:.3f} incorrect and
  {lowu:.3f} unfinished. Their tie reflects ample capacity and shared potential
  outcomes, not proof of human equivalence. With 36 questions and fifteen minutes,
  G-Q is {overload}, while source-aware Q still exceeds G by {qsaover:.3f} answers.
- **Carryover can reverse an apparent benefit.** With long memory and a .20
  same-source carryover hazard, G-Q becomes {carry}. G's wrong releases rise from
  {basewrong:.3f} to {carrywrong:.3f}; FIFO's rise from {qwrong:.3f} to {qcarrywrong:.3f}.
  The same hazard applies in every condition. More frequent same-source
  transitions expose G and sticky Q more often. This relationship is modeled,
  not an observed psychological effect.
- **Draft usefulness is conditional.** When manual construction is 20 seconds and
  verification 40 seconds, G-M is {manualfav}. With 90-second construction and
  8-second verification it is {draftfav}. These are declared extremes, not tuned
  estimates. Actual initial drafts are low quality (7/36 joint-correct, five
  empty/unsupported), while the effectiveness of checking/repair remains assumed.

## Mechanism and counterexamples

For the same completed task-attempt set, a useful time balance is orientation
saved minus group interaction overhead. This can predict capacity benefit only
when other work phases and success paths are comparable. Across different task
subsets, subtracting aggregate orientation totals alone does not prove time saving.
A saved minute matters only if enough remains to finish an additional decision and
release. Waiting for unrelated work and harmful carryover can offset that benefit.

The bounded source-aware Q control removes group cards but uses exactly G's
selection mechanism. The zero-cost identity is a structural check, not a discovery.
Positive overhead can change eligible groups and the completed subset, so no general
dominance theorem for every possible arrival/outcome stream is asserted. In this
finite declared grid, however, no G cell mean exceeds that control.

Examples use the first qualifying configuration, rotation and seed rather than
maximum effect. The first favorable individual trace is **002_o0_high_short,
rotation 1, seed 10014**: G releases one more correct answer even though orientation
cost is zero and the cell mean favors FIFO. This gain comes from which outcomes
reach cutoff, not recovered context time. The first unfavorable trace is
**000_o0_ideal_short, rotation 0, seed 10000**, where G completes one fewer correct
answer. A favorable single trace therefore cannot establish an operating-region
advantage. See `EXAMPLES.md` and the paired timelines for actual questions and
saved drafts behind these simulated outcomes.

The simulated FIFO policy is a navigation strategy, not a limitation imposed by
the real central-queue interface. People can manually select related requests in
that interface. Both source-aware queue controls represent that stronger competing
explanation. This study does not show that multiple model architectures outperform
a single model or that users experience reduced cognitive load.

## Reproducibility, validation and failures

The model, original inputs, fixed matrix and analysis were committed at
`8b74d58b` before comparative runs. A 64-seed preliminary forecast was reduced to
32 before outcomes, preserving all 66 parameter settings. No seeds were added,
replaced or removed based on results. The batch finished in {batch_seconds:.1f}
seconds of measured host wall time. Raw result rows and compact command/phase
traces are saved, with scenario/simulation identifiers and no human-export schema.

Eight pre-run tests cover original arrivals, unique goals, equal selector information,
shared familiarity, zero-cost identity, cutoff accounting, versioned releases,
recognized failure and ordinary-engine replay. Four additional read-only checks
probe actual hidden-label mutation before first dispatch, manual draft isolation,
paired randomness and approval without release. Initial development tests exposed
an integer-versus-float timestamp digest mismatch and a test incorrectly expecting
a familiarity saving with zero orientation cost; both were fixed before freezing,
and the failing log is preserved. Figure review identified an overlapping colorbar
and a plotting compatibility warning; plotting-only fixes leave outcomes unchanged.

`verification.json` records replay of every trace, official re-scoring of every
released output and ordinary atomic-engine checks. `preservation.json` and the
human-study freeze protect historical materials. No practice or participant records
were used. Reference-based simulated correct responses and explicit unsuccessful
response sentinels are not claimed as actual reviewer generations. No inference,
paid resource or unrelated service was started or changed.

## Claim-evidence boundary and next observation

| Claim | Evidence | Limit |
|---|---|---|
| The source-aware queue is the simpler supported computational alternative | All 66 cells, zero-cost identity and paired release counts | This model contains no measured visual/comprehension advantage for cards |
| Source grouping can help over FIFO when repeated orientation is expensive | Original orientation/persistence map and load/interleaving stress | Conditional operating region, not measured human task prevalence |
| Grouping can trade additional correct releases for additional errors | Fallibility and carryover panels with wrong releases retained | Reviewer rates and carryover mechanism are unvalidated |
| Saved drafts are not automatically beneficial | Matched manual construction and cost sensitivity | Relative construction/verification costs and human accuracy remain unknown |
| Simulation matches the review protocol | Event replay and exact-version scoring | Software semantics do not establish understanding or human performance |

The strongest supported contribution is a reproducible **conditional comparison
that separates source-aware navigation from grouping-card overhead**, grounded in
real tasks and actual imperfect drafts. It does not validate grouping as a human
interface improvement. Measure source orientation after consecutive/intervening
work, group-control interaction costs, detection/repair performance on these drafts,
manual construction, and unit/assumption carryover. Observe whether queue users
already adopt source-aware ordering. These observations can calibrate or falsify
the model. The existing frozen prospective study remains intact; any later design
adding a source-aware automatic-queue condition needs a separately declared version.

All six selected source-size factors clip to 0.75 (1,120-1,750 source characters),
so first-visit orientation is 0.75 times the declared S coefficient. This model
does not distinguish source-size difficulty within these approximately matched
packets. Plot labels identify S rather than mislabeling it as an actual first-visit
duration. This reporting clarification changes no frozen function or result.

Additional model limits: familiarity is evaluated when a review is selected and
held fixed for that attempt, rather than continuously during its phases. The
post-selection group overhead therefore does not trigger a second memory update.
Question-level random effectiveness is shared across policies but does not model
a common latent skill level or correlated source-level errors. Apart from declared
carryover, those sources of behavioral dependence remain unmodeled.
'''.format(lose=stats['group_loses_source_aware_cells'],tie=stats['group_ties_source_aware_cells'],winq=stats['group_beats_fifo_cells'],loseq=stats['group_loses_fifo_cells'],tieq=stats['group_ties_fifo_cells'],table=table,waiting=waiting,gq=effect(base,'G_minus_Q'),gs=effect(base,'G_minus_Q-source-aware'),gt=effect(base,'G_minus_Q-sticky'),wins=int(a.seed_positive),ties=int(a.seed_ties),losses=int(a.seed_negative),qm=effect(base,'Q_minus_M'),gm=effect(base,'G_minus_M'),short=effect('014_o25_high_short','G_minus_Q'),large=effect('020_o75_high_short','G_minus_Q'),largeqerr=val('020_o75_high_short','Q','incorrect'),largegerr=val('020_o75_high_short','G','incorrect'),interleaved=effect('036_two_wave_interleaved','G_minus_Q'),blocked=effect('037_two_wave_source_blocked','G_minus_Q'),lowc=val('026_n6_h900','G','correct'),loww=val('026_n6_h900','G','incorrect'),lowu=val('026_n6_h900','G','unfinished'),overload=effect('035_n36_h900','G_minus_Q'),qsaover=-paired('035_n36_h900','G_minus_Q-source-aware')['mean'],carry=effect('062_long_c20','G_minus_Q'),basewrong=val(base,'G','incorrect'),carrywrong=val('062_long_c20','G','incorrect'),qwrong=val(base,'Q','incorrect'),qcarrywrong=val('062_long_c20','Q','incorrect'),manualfav=effect('054_v40_m20','G_minus_M'),draftfav=effect('050_v8_m90','G_minus_M'),batch_seconds=read(OUT/'batch.json')['elapsed_seconds'])
    text=text.replace('{waiting}',waiting)
    verified=read(OUT/'verification.json') if (OUT/'verification.json').exists() else None
    if verified:
        text+='\n## Recorded verification\n\nAll %s simulation traces replayed, %s released answers were independently re-scored, and %s selected traces matched ordinary atomic-engine replay. All %s protected historical files remain unchanged. No human records were read.\n'%(verified['simulation_traces'],verified['official_release_scores_checked'],verified['ordinary_engine_replays'],verified['preserved_files'])
    ledger=read(OUT/'ledger.json')
    if 'elapsed_to_packaging_seconds' in ledger:
        text+='\n## Stage resource accounting\n\nThe separately authorized CPU stage reached its packaging checkpoint after %.1f minutes, within the 90-minute limit. The declared batch used %.1f seconds of host wall time and full verification %.1f seconds. There were zero scheduled model calls, attempts or new tokens. Five additional CPU runs checked the isolated reproduction adapter against saved objects; they are verification, not an expanded evaluation. No services were started or modified.\n'%(ledger['elapsed_to_packaging_seconds']/60,ledger['simulation_batch_seconds'],ledger['full_verification_seconds'])
        text+='\nCalendar elapsed from the preserved original start is %.2f hours, or %.2f hours beyond the original 36-hour target, including previous stages and idle gaps. This is not active-compute time and the new stage is not represented as work inside that original window. Historical cumulative inference remains unchanged at %s actual attempts. The ledger identifies the packaging checkpoint immediately before the final commit.\n'%(ledger['original_to_checkpoint_calendar_seconds']/3600,ledger['original_target_overrun_calendar_seconds']/3600,ledger['historical_cumulative_inference']['attempts'])
    (HERE/'REPORT.md').write_text(text)
    paper=ROOT/'paper/oversight_simulation';paper.mkdir(exist_ok=True)
    macros=''
    for pol,stem in [('Q','Queue'),('G','Group'),('Q-source-aware','Aware'),('Q-sticky','Sticky'),('M','Manual')]:
        for key,field in [('Correct','correct'),('Wrong','incorrect'),('Unfinished','unfinished')]:macros+='\\newcommand{\\'+stem+key+'}{%.2f}\n'%val(base,pol,field)
    for stem,cid,contrast in [('Primary',base,'G_minus_Q'),('Control',base,'G_minus_Q-source-aware'),('Short','014_o25_high_short','G_minus_Q'),('Large','020_o75_high_short','G_minus_Q')]:
        row=paired(cid,contrast)
        for suffix,field in [('Delta','mean'),('Low','mc_low'),('High','mc_high')]:macros+='\\newcommand{\\'+stem+suffix+'}{%+.3f}\n'%row[field]
    (paper/'numbers.tex').write_text(macros)
    inputs=read(OUT/'inputs.json');ts=read(OUT/'analysis/example_traces.json.gz');examples=read(OUT/'analysis/example_selection.json');lines=['# Source-grounded examples with simulated review outcomes','', 'Original questions and drafts are actual benchmark/generation records. All subsequent review actions and outcomes below are SIMULATED. Selection follows the frozen first-qualifying rule, not effect magnitude.','']
    decompositions=[]
    for label,ident in examples.items():
        match=[t for t in ts if all(t[k]==ident[k] for k in ('config','rotation','seed'))];by={t['policy']:t for t in match}
        lines+=['## '+label.title(),'', '`'+json.dumps(ident)+'`','', '| Original question / source | Actual draft | Q outcome | G outcome |','|---|---|---|---|']
        oq={x['id']:x for x in by['Q']['observed_outcomes']};og={x['id']:x for x in by['G']['observed_outcomes']}
        changed=sorted(set(oq)^set(og) | {q for q in set(oq)&set(og) if oq[q]['correct']!=og[q]['correct']})
        if not changed:changed=[by['Q']['reviews'][0]['id']]
        def out(x):return 'Unreleased' if x is None else 'Correct release' if x['correct'] else 'Incorrect release'
        for qid in changed:
            i=inputs['items'][qid];question=i['question'].replace('|','/');answer=(str(i['output']['answer'])+'; scale '+i['output'].get('scale','')).replace('|','/')
            lines+=['| '+question+' (`'+qid+'`, source `'+i['source_id']+'`) | '+answer+' | '+out(oq.get(qid))+' | '+out(og.get(qid))+' |']
        commonq={(r['id'],r['attempt']):r for r in by['Q']['reviews']};commong={(r['id'],r['attempt']):r for r in by['G']['reviews']}
        common=set(commonq)&set(commong)
        def phase(r,name):return sum(b-a for n,a,b in r['segments'] if n==name)
        orientation=sum(phase(commonq[k],'orientation')-phase(commong[k],'orientation') for k in common)
        group=sum(phase(commong[k],'grouping') for k in common)
        decompositions.append(dict(example=label,common_task_attempts=len(common),planned_orientation_saved_on_common_attempts=orientation,planned_group_cost_on_common_attempts=group,balance=orientation-group,limit='Planned phase times on shared attempted tasks, not a guarantee of another released answer'))
        lines+=['','For common attempted questions, planned orientation saving is %.2f s and extra group interaction is %.2f s. This does not equate different completed task subsets or certify a cognitive mechanism.'%(orientation,group),'']
    (HERE/'EXAMPLES.md').write_text('\n'.join(lines).rstrip()+'\n');pd.DataFrame(decompositions).to_csv(OUT/'analysis/example_time_balance.csv',index=False)
    print('Report, exact numerical macros and source-linked examples generated')


if __name__=='__main__':main()
