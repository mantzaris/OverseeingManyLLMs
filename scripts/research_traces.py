#!/usr/bin/env python3
"""Readable paired queue traces selected by the declared numerical-seed rule."""
import argparse
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from overseeing.research_analysis import numeric_records,read_csv
from overseeing.io import read_events,write_json,write_csv


def render_pair(root,batch,left,right,path,reason):
    lines=['# Paired queue example','',reason,'','Offline scoring view: hidden faults and initial correctness below were not supplied to schedulers.']
    for row in (left,right):
        events=read_events(root/'batches'/batch/'episodes'/row['run_id']/'events.jsonl');jobs={j['public']['job_id']:j for j in events[0]['scenario']['jobs']}
        lines+=['','## '+row['run_id'],'','Loss {}; incorrect closures {}; corrections {}.'.format(row['total_loss'],row['incorrect_jobs'],row['corrections']),'','| Tick | Event | Details |','| ---: | --- | --- |']
        for e in events:
            kind=e['event'];details=None
            if kind=='proposal':
                j=jobs[e['job_id']];p=j['public'];correct={'filter':'replace_filter','sensor':'reset_sensor'}[j['fault']]
                details='{}: clues {}; first {}; second {}; initial {} (offline label); p={:.4f}; deadline {}; c={}; K={}'.format(e['job_id'],'/'.join(p['clues']),e['primary'],e['secondary'],'correct' if e['primary']==correct else 'wrong',e['p_error'],p['deadline'],p['cost_per_tick'],p['terminal_cost'])
            elif kind=='planning_decision':
                details='eligible '+', '.join('{}(d={},p={:.3f},G_now={:.3f})'.format(r['job_id'],r['deadline'],r['p_error'],r['cost_per_tick']*(r['deadline']-e['tick']-r['review_ticks'])+r['terminal_cost']) for r in e['eligible'])+'; choose '+str(e['selected'])
            elif kind=='queue_snapshot':details='waiting '+', '.join(e['pending'])+'; active '+str(e['busy'])
            elif kind=='review_completed':details='{}: {}, applied={}, corrected={}'.format(e['job_id'],e['instructed_action'],e['applied'],e['changed'])
            elif kind=='request_expired':details='{}: {}'.format(e['job_id'],e['category'])
            elif kind=='job_closed':details='{}: correct={}, job loss={}'.format(e['job_id'],e['correct'],e['job_loss'])
            if details is not None:lines.append('| {} | {} | {} |'.format(e['tick'],kind,details.replace('|','/')))
    path.write_text('\n'.join(lines)+'\n')


def main(root,batch,label):
    root=Path(root);out=root/'summaries'/label/'traces';out.mkdir(parents=True,exist_ok=True)
    episodes=numeric_records(root/'batches'/batch/'analysis/episodes.csv')
    rows={r['run_id']:r for r in episodes};selected=[]
    pairs=read_csv(root/'summaries'/label/'paired_scenarios.csv')
    for workload,agents in (('original',3),('competition',3),('larger',6)):
        candidates=[r for r in pairs if r['kind']=='policy' and r['left']=='{}|a{}|s2|frozen|delay|lambda0'.format(workload,agents) and r['right'].endswith('|greedy|lambda0') and r['loss_difference']!='']
        candidates.sort(key=lambda r:int(r['seed']))
        for direction in ('positive','negative'):
            qualifying=[r for r in candidates if float(r['loss_difference'])*(1 if direction=='positive' else -1)<0]
            fallback=not qualifying
            if not qualifying:qualifying=[r for r in candidates if float(r['loss_difference'])==0]
            if not qualifying:
                selected.append(dict(workload=workload,direction=direction,status='no qualifying example or tie'));continue
            p=qualifying[0];seed=int(p['seed'])
            a=next(r for r in episodes if r['workload']==workload and r['agents']==agents and r['seed']==seed and r['review_ticks']==2 and r['risk']=='frozen' and r['closure_penalty']==0 and r['policy']=='delay')
            b=next(r for r in episodes if r['workload']==workload and r['agents']==agents and r['seed']==seed and r['review_ticks']==2 and r['risk']=='frozen' and r['closure_penalty']==0 and r['policy']=='greedy')
            reason='First numerical seed with search {} loss than greedy at two ticks.'.format('lower' if direction=='positive' else 'higher')
            if fallback:reason='No {} search-versus-greedy example; first numerical tie shown under the declared fallback.'.format(direction)
            filename='{}_{}.md'.format(workload,direction);render_pair(root,batch,a,b,out/filename,reason)
            selected.append(dict(workload=workload,direction=direction,seed=seed,fallback_tie=fallback,loss_difference=float(p['loss_difference']),file=filename,first_action_differences=int(p['primary_action_differences']),different_observations=int(p['different_observations']),identical_request_first_action_differences=int(p['identical_request_primary_differences'])))
    for workload in ('competition','larger'):
        for duration in (1,2):
            candidates=[r for r in pairs if r['kind']=='objective' and r['workload']==workload and r['left'].endswith('|lambda8') and int(r['review_ticks'])==duration and r['loss_difference']!='' and float(r['loss_difference'])>0 and float(r['incorrect_difference'])<0]
            candidates.sort(key=lambda r:int(r['seed']))
            if not candidates:
                selected.append(dict(workload=workload,direction='objective_tradeoff',review_ticks=duration,status='no lambda8 lower-count/higher-cost example'));continue
            p=candidates[0];seed=int(p['seed'])
            a=next(r for r in episodes if r['phase']=='objective_evaluation' and r['workload']==workload and r['seed']==seed and r['review_ticks']==duration and r['closure_penalty']==8)
            b=next(r for r in episodes if r['phase']=='objective_evaluation' and r['workload']==workload and r['seed']==seed and r['review_ticks']==duration and r['closure_penalty']==0)
            filename='{}_s{}_objective.md'.format(workload,duration)
            render_pair(root,batch,a,b,out/filename,'First numerical seed where λ=8 reduces incorrect closures while increasing original maintenance loss relative to λ=0.')
            selected.append(dict(workload=workload,direction='objective_tradeoff',review_ticks=duration,seed=seed,file=filename,loss_difference=float(p['loss_difference']),incorrect_difference=int(p['incorrect_difference'])))
    write_json(out/'selection.json',selected)
    return selected

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',default='artifacts/stage4_research');parser.add_argument('--batch',default='evaluation');parser.add_argument('--label',default='evaluation');args=parser.parse_args();print(main(args.root,args.batch,args.label))
