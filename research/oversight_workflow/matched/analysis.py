"""Matched Q/G/M analysis. Offline only; never imported by the server.

Answer/event extraction is versioned from formative-v1; scorer, CSV utilities,
bootstrap and additional adjudication remain shared. Old exports are refused.
"""
import argparse
import csv
from copy import deepcopy
from collections import Counter
from pathlib import Path
import statistics

from research.oversight_workflow.common import read, write, digest, ART
from research.oversight_workflow.offline import labels
from research.adaptive_correction_transfer.scoring import score
from research.oversight_workflow.pilot.analysis import csv_write, intervals, apply_adjudication
from research.oversight_workflow.pilot.adapter import saved_output
from research.oversight_workflow.pilot.materials import PILOT
from .materials import HERE, VERSION, SCHEMA
from .protocol import replay
from .freeze import runtime_fingerprint, verify


def expected(manifest, run, session):
    if session['block_index'] == 0:
        training = read(PILOT.parent / 'study/training.json')
        return 'training', None, {q['id'] for q in training['questions']}
    b = manifest['assignments'][run['assignment']]['blocks'][session['block_index']-1]
    return b['condition'], b['packet'], set(manifest['packets'][b['packet']]['question_ids'])


def load_runs(paths, kind):
    manifest = read(HERE / 'manifest.json'); unique = {}; duplicates = 0
    if kind=='participant': verify()
    runtime=runtime_fingerprint()
    public = {c['id']: c for c in read(ART / 'frozen/manifest.json')['contexts']}
    training = read(PILOT.parent / 'study/training.json'); public[training['context']['id']] = training['context']
    for path in paths:
        r = read(path)
        if r.get('record_kind') != kind:
            raise ValueError('Refusing record-kind mixing: ' + str(path))
        if r.get('runtime_sha256') != runtime:
            raise ValueError('Runtime version differs; do not pool development versions')
        if r.get('schema') != SCHEMA or r.get('pilot_version') != VERSION or r.get('manifest_sha256') != manifest['manifest_sha256']:
            raise ValueError('Unknown matched version; formative-v1 and old practice are not this comparison')
        if type(r['assignment']) is not int or not 0 <= r['assignment'] < len(manifest['assignments']):
            raise ValueError('Incorrect assignment')
        if kind == 'participant':
            a = r.get('authorization') or {}
            if a.get('collection_authorized') is not True or not all(a.get(k) for k in ('institutional_determination','consent_version','investigator','record_reference','assignment_schedule_reference')) or a.get('study_version') != VERSION or a.get('manifest_sha256') != manifest['manifest_sha256']:
                raise ValueError('Missing matched-study authorization or assignment provenance')
        rid = r['run_id']
        if rid in unique:
            if digest(unique[rid]) != digest(r):
                raise ValueError('Conflicting snapshots of one run; select the final export explicitly')
            duplicates += 1; continue
        if any(x['participant_code'] == r['participant_code'] for x in unique.values()):
            raise ValueError('Repeated participant code; resolve repeat-run provenance explicitly')
        blocks = set(); scored_durations = set()
        for s in r['sessions'] + ([r['active_session']] if r.get('active_session') else []):
            if s['record_kind'] != kind or type(s['block_index']) is not int or s['block_index'] not in range(4) or s['block_index'] in blocks:
                raise ValueError('Duplicate/invalid block or mixed provenance')
            blocks.add(s['block_index']); cond, packet, qids = expected(manifest, r, s)
            if s['condition'] != cond or s['packet'] != packet or set(s['question_ids']) != qids or len(s['question_ids']) != len(qids):
                raise ValueError('Incorrect packet assignment')
            if s['desk_condition'] != ('sessions' if cond in ('G','training') else 'queue') or s['admission_controls'] is not False:
                raise ValueError('Incorrect treatment configuration')
            declared = manifest['training_seconds'] if cond == 'training' else manifest['review_seconds']
            if s['declared_duration_seconds'] != declared or (kind != 'software_fixture' and s['duration_seconds'] != declared):
                raise ValueError('Unapproved timing difference')
            if cond != 'training': scored_durations.add(s['duration_seconds'])
            offsets = manifest['training_start_offsets'] if cond == 'training' else manifest['review_start_offsets']
            if s['start_offsets'] != [v*s['duration_seconds']/declared for v in offsets] or s['generation_delay'] != .25:
                raise ValueError('Unequal or altered arrival schedule')
            desk = replay(s['events'], s['desk_condition'])
            if desk.logical() != s['state']:
                raise ValueError('Saved-state replay mismatch')
            state = s['state']
            if {t['question_id'] for t in state['tasks'].values()} != qids or len(state['tasks']) != len(qids):
                raise ValueError('Offered workload differs from assigned workload')
            expected_sources = {training['context']['id']} if cond == 'training' else set(manifest['packets'][packet]['context_ids'])
            if set(s['source_ids']) != expected_sources or {t['source']['id'] for t in state['tasks'].values()} != expected_sources:
                raise ValueError('Source assignment mismatch')
            for tid,t in state['tasks'].items():
                c = public[t['source']['id']]
                q = next((q for q in c['questions'] if q['id'] == t['question_id']), None)
                if not q or q['question'] != t['question'] or t['source']['table'] != c['table'] or t['source']['paragraphs'] != c['paragraphs']:
                    raise ValueError('Source/question provenance mismatch')
                request = state['requests'].get(tid)
                raw = s['raw_proposals'].get(tid)
                if cond == 'M':
                    if raw is not None:
                        raise ValueError('Manual condition contains a model proposal')
                    placeholder=dict(answer=[], scale='', evidence=[], derivation='Manual source-only task. No model proposal is shown.', issues=[])
                    if request and (request['versions']['1']['output'] != placeholder or request['versions']['1']['origin'] != 'source_only_placeholder'):
                        raise ValueError('Manual initial state is not source-only')
                else:
                    output, original = saved_output(c, q, 'pilot' if cond == 'training' else 'primary')
                    if raw != original or (request and request['versions']['1']['output'] != output):
                        raise ValueError('Saved draft/display differs from frozen input')
        if len(scored_durations) > 1:
            raise ValueError('Fixture compression differs across matched conditions')
        unique[rid] = r
    return list(unique.values()), duplicates


def analyze(paths,out,kind='participant'):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);runs,duplicates=load_runs(paths,kind);gold=labels();rows=[];answers=[];timing=[];blind=[];private=[];missing=[]
 for run in runs:
  missing.append(dict(code=run['participant_code'],run_id=run['run_id'],withdrawn=run['withdrawn'],missing_completed_blocks=sorted(set(range(4))-{s['block_index'] for s in run['sessions']}),active_export=bool(run.get('active_session')),planned_scored_questions=36,offered_scored_questions=sum(len(s['state']['tasks']) for s in run['sessions']+([run['active_session']] if run.get('active_session') else []) if s['condition']!='training')))
  for s in run['sessions']+([run['active_session']] if run.get('active_session') else []):
   if s['condition']=='training':continue
   st=s['state'];ok=[e for e in s['events'] if e['response']['ok']];counts=Counter();end=st.get('closed_at',max([e['at'] for e in s['events']] or [0]));select_start={};was_deferred=set();source_visits=[]
   for e in ok:
    a=e['action'];p=e['payload'];rid=p.get('id')
    if a=='select':select_start[rid]=(e['at'],rid in was_deferred)
    if a=='decide':
     if rid in select_start:
      begin,resumed=select_start.pop(rid);timing.append(dict(record_kind=kind,participant_code=run['participant_code'],session_id=s['session_id'],condition=s['condition'],request_id=rid,start=begin,end=e['at'],elapsed_seconds=e['at']-begin,resumed=int(resumed),censored=0,action=p['decision']))
     if p['decision']=='defer':was_deferred.add(rid);counts['deferrals']+=1
    if a=='display' and p.get('action')=='source_focus':source_visits.append(st['tasks'].get(p.get('request_id'),{}).get('source',{}).get('id'))
    if a=='session':counts['group_actions']+=1
    if a=='pause':counts['pause_actions']+=1
    if a=='resume':counts['resume_actions']+=1
    if a=='display' and p.get('action')=='visibility_change' and not p.get('focus'):counts['visibility_interruptions']+=1
    if a=='display' and p.get('action')=='calculator':counts['calculator_uses']+=1
   for rid,(begin,resumed) in select_start.items():timing.append(dict(record_kind=kind,participant_code=run['participant_code'],session_id=s['session_id'],condition=s['condition'],request_id=rid,start=begin,end=end,elapsed_seconds=max(0,end-begin),resumed=int(resumed),censored=1,action='unfinished_at_cutoff'))
   for rid,t in st['tasks'].items():
    r=st['requests'].get(rid);v=r['current_version'] if r else None;output=r['versions'][str(v)]['output'] if r else None
    released=bool(r and r['status']!='withdrawn' and any(x['request_id']==rid and x['version']==v for x in st['releases']));ds=[d for d in st['decisions'] if d['request_id']==rid and d['version']==v];approved=bool(ds and ds[-1]['decision'] in ('approve','correct'))
    g=gold[t['source']['id']][t['question_id']];sc=score(output,g) if output else dict(em=0,f1=0,joint=0,scale=0,unfinished=1)
    original=score(r['versions']['1']['output'],g) if r and s['condition']!='M' else None
    row=dict(record_kind=kind,participant_code=run['participant_code'],run_id=run['run_id'],session_id=s['session_id'],condition=s['condition'],packet=s['packet'],request_id=rid,question_id=t['question_id'],source_id=t['source']['id'],version=v,offered=1,started=int(t['started_at'] is not None),received=int(bool(r)),approved=int(approved),released=int(released),official_em=sc['em'] if released else None,official_f1=sc['f1'] if released else None,joint_correct=int(released and sc['joint']),incorrect_released=int(released and not sc['joint']),answer_em_correct=int(released and sc['em']),approved_joint_correct=int(approved and sc['joint']),incorrect_approved=int(approved and not sc['joint']),blocked=int(bool(ds and ds[-1]['decision']=='reject')),corrected=int(any(d['request_id']==rid and d['decision']=='correct' for d in st['decisions']) and s['condition']!='M'),initial_joint=original['joint'] if original else None,unresolved=int(not r or r['status'] in ('queued','active','deferred')),unfinished=int(not released),answer=output['answer'] if output else [],scale=output.get('scale','') if output else '')
    row['corrected_released']=int(row['corrected'] and released)
    row['successful_corrections']=int(row['corrected'] and released and sc['joint'] and original is not None and not original['joint'])
    row['harmful_corrections']=int(row['corrected'] and released and not sc['joint'] and original is not None and original['joint'])
    answers.append(row)
    if released:
     ident=digest([run['run_id'],s['session_id'],rid,v])[:20]
     blind.append(dict(case_id=ident,question=t['question'],source=t['source'],candidate=dict(answer=output['answer'],scale=output.get('scale','')),reference=dict(answer=g['answer'],scale=g['scale'],derivation=g.get('derivation','')),instruction='Blind review of every released answer, including exact-match controls. Judge acceptability from source, question and declared scale conventions. Do not infer interface or participant.'))
     private.append(dict(case_id=ident,run_id=run['run_id'],session_id=s['session_id'],request_id=rid,official_em=sc['em'],official_joint=sc['joint']))
   aa=[a for a in answers if a['session_id']==s['session_id']];tt=[t for t in timing if t['session_id']==s['session_id']];q=s.get('questionnaire');tlx=q.get('tlx',[]) if q else []
   row=dict(record_kind=kind,participant_code=run['participant_code'],run_id=run['run_id'],assignment=run['assignment'],condition=s['condition'],packet=s['packet'],session_id=s['session_id'],status=s.get('end_reason','interrupted_active_export'),seconds_observed=end,withdrawn=int(run['withdrawn']))
   for k in ('offered','started','received','approved','released','joint_correct','answer_em_correct','approved_joint_correct','incorrect_approved','incorrect_released','blocked','corrected','corrected_released','successful_corrections','harmful_corrections','unresolved','unfinished'):row[k]=sum(a[k] for a in aa)
   row.update(unstarted=row['offered']-row['started'],select_to_action_seconds=sum(t['elapsed_seconds'] for t in tt if not t['censored']),resumed_select_to_action_seconds=sum(t['elapsed_seconds'] for t in tt if t['resumed'] and not t['censored']),censored_active_seconds=sum(t['elapsed_seconds'] for t in tt if t['censored']),source_focus_events=len(source_visits),source_revisits=sum(x in source_visits[:i] for i,x in enumerate(source_visits)),technical_events=sum(t.get('session_id')==s['session_id'] for t in run['technical_events']),refused_commands=sum(not e['response']['ok'] for e in s['events']),questionnaire_present=int(q is not None),tlx_raw_mean=statistics.mean(tlx) if len(tlx)==6 and all(x is not None for x in tlx) else None)
   for k in ('deferrals','group_actions','pause_actions','resume_actions','visibility_interruptions','calculator_uses'):row[k]=counts[k]
   for i in range(6):row['tlx_'+str(i+1)]=tlx[i] if len(tlx)==6 else None
   for i in range(3):row['control_'+str(i+1)]=q['control'][i] if q else None
   rows.append(row)
 # Matched allocations and behavioral proxies. No automatic mechanism attribution.
 for row in rows:
  row['correct_release_proportion']=row['joint_correct']/row['offered']
  row['declared_seconds']=540
  run=next(r for r in runs if r['run_id']==row['run_id'])
  row['block_position']=next(s['block_index'] for s in run['sessions']+([run['active_session']] if run.get('active_session') else []) if s['session_id']==row['session_id'])
  row.update(behavior_counts(next(s for s in run['sessions']+([run['active_session']] if run.get('active_session') else []) if s['session_id']==row['session_id']),timing))
 paired=[]
 metrics=['correct_release_proportion','joint_correct','incorrect_approved','incorrect_released','unfinished','unstarted','successful_corrections','harmful_corrections','released','select_to_action_seconds','resumed_select_to_action_seconds','source_revisits','source_selection_returns','group_actions','tlx_raw_mean','control_1','control_2','control_3']
 for run in runs:
  rs={r['condition']:r for r in rows if r['run_id']==run['run_id'] and r['status']!='interrupted_active_export'}
  for a,b in [('G','Q'),('Q','M'),('G','M')]:
   if a not in rs or b not in rs:continue
   p=dict(record_kind=kind,participant_code=run['participant_code'],run_id=run['run_id'],withdrawn=run['withdrawn'],contrast=a+'_minus_'+b,assignment=run['assignment'],packet_a=rs[a]['packet'],packet_b=rs[b]['packet'],position_a=rs[a]['block_position'],position_b=rs[b]['block_position'])
   for k in metrics:p[k]=rs[a][k]-rs[b][k] if rs[a][k] is not None and rs[b][k] is not None else None
   paired.append(p)
 interpretation={'software_fixture':'SYNTHETIC SOFTWARE FIXTURE; NOT participant findings','investigator_practice':'Investigator practice; NOT independent participant evidence','participant':'Formative matched observations; not automatically powered effectiveness evidence'}[kind]
 summary=dict(version=VERSION,record_kind=kind,interpretation=interpretation,runs=len(runs),duplicate_exports_ignored=duplicates,participant_results_populated=kind=='participant' and bool(runs),missing=missing,primary_comparison='G_minus_Q',unit='Participant; six reused source contexts, not independent financial reports',contrasts={},technical_limits='Interrupted active blocks remain in tables but not fixed-period paired estimates. Early finish retained. Withdrawn pairs shown but excluded from summaries.',mechanism_limit='Source focus and select-to-action intervals are proxies, not reading or cognitive effort. Group use is self-selected, not randomized mediation.')
 for contrast in ('G_minus_Q','Q_minus_M','G_minus_M'):
  result={}
  for metric in metrics:
   xs=[p[metric] for p in paired if p['contrast']==contrast and not p['withdrawn'] and p[metric] is not None]
   result[metric]=dict(n=len(xs),mean=statistics.mean(xs) if xs else None,median=statistics.median(xs) if xs else None,positive=sum(x>0 for x in xs),ties=sum(x==0 for x in xs),negative=sum(x<0 for x in xs),descriptive_bootstrap95=intervals(xs) if kind=='participant' else None)
  summary['contrasts'][contrast]=result
 summary['interval_limit']='2000 participant resamples, seed 92741, only at least six complete nonwithdrawn pairs; conditional on reused packets. Six is a reporting threshold, not power. No equivalence or noninferiority conclusion.'
 balance=[]
 for (condition,packet,position),n in Counter((r['condition'],r['packet'],r['block_position']) for r in rows).items():balance.append(dict(record_kind=kind,condition=condition,packet=packet,position=position,sessions=n))
 csv_write(out/'sessions.csv',rows);csv_write(out/'answers_official.csv',answers);csv_write(out/'review_intervals.csv',timing);csv_write(out/'paired_descriptions.csv',paired);csv_write(out/'packet_order_coverage.csv',balance)
 write(out/'summary.json',summary)
 write(out/'adjudication_blinded.json',dict(kind='Investigator-only; never serve to task browser',cases=sorted(blind,key=lambda x:x['case_id'])))
 write(out/'adjudication_key_PRIVATE.json',private)
 csv_write(out/'adjudication_blank.csv',[dict(case_id=b['case_id'],verdict='',reason='',rater_code='') for b in sorted(blind,key=lambda x:x['case_id'])])
 write_behavior_exports(runs,timing,out,kind)
 write_version_history(runs,out,kind)
 if kind=='participant' and rows: participant_figures(rows,paired,out)
 return summary


def behavior_counts(session, timing):
    tasks=session['state']['tasks'];sequence=[];groups=[];active_group=[];grouped=0;returns=0
    for e in session['events']:
        if not e['response']['ok']:continue
        if e['action']=='session':active_group=e['payload']['ids'];groups.append(e['at'])
        if e['action']=='select':
            rid=e['payload']['id'];source=tasks[rid]['source']['id']
            if not sequence or sequence[-1]!=source:
                returns+=int(source in sequence);sequence.append(source)
            grouped+=int(rid in active_group)
    tt=[t for t in timing if t['session_id']==session['session_id']]
    return dict(source_selection_episodes=len(sequence),source_selection_returns=returns,
                grouped_selections=grouped,group_actions_count=len(groups),
                resumed_to_decision=sum(t['resumed'] and not t['censored'] for t in tt),
                resumed_to_release=sum(t['resumed'] and not t['censored'] and any(x['request_id']==t['request_id'] for x in session['state']['releases']) for t in tt))


def write_behavior_exports(runs,timing,out,kind):
    waits=[];links=[]
    for run in runs:
        for s in run['sessions']+([run['active_session']] if run.get('active_session') else []):
            if s['condition']=='training':continue
            state=s['state'];events=[e for e in s['events'] if e['response']['ok']];group=[];group_at_select={}
            for e in events:
                if e['action']=='session':group=e['payload']['ids']
                if e['action']=='select':group_at_select[(e['payload']['id'],e['at'])]=e['payload']['id'] in group
            end=state.get('closed_at',max([e['at'] for e in events] or [0]))
            tt=[t for t in timing if t['session_id']==s['session_id']]
            for rid,request in state['requests'].items():
                source=state['tasks'][rid]['source']['id'];first=next((e['at'] for e in events if e['action']=='select' and e['payload']['id']==rid),None);stop=first if first is not None else end;overlap=0
                for t in tt:
                    if state['tasks'][t['request_id']]['source']['id']!=source and group_at_select.get((t['request_id'],t['start']),False):
                        overlap+=max(0,min(stop,t['end'])-max(request['received_at'],t['start']))
                waits.append(dict(record_kind=kind,run_id=run['run_id'],session_id=s['session_id'],condition=s['condition'],packet=s['packet'],request_id=rid,source_id=source,received_at=request['received_at'],first_selected_at=first,wait_or_censored_seconds=max(0,stop-request['received_at']),censored=int(first is None),other_source_group_review_overlap_seconds=overlap))
            links.append(dict(record_kind=kind,run_id=run['run_id'],session_id=s['session_id'],condition=s['condition'],packet=s['packet'],interview_evidence='',event_sequences='',source_ids='',observed_strategy_or_failure='',alternative_explanation='',analyst='',negative_case=''))
    csv_write(out/'request_waits.csv',waits);csv_write(out/'qualitative_links_blank.csv',links)


def write_version_history(runs, out, kind):
    gold=labels();history=[]
    for run in runs:
        for s in run['sessions']+([run['active_session']] if run.get('active_session') else []):
            if s['condition']=='training':continue
            state=s['state']
            for category,entries in [('decision',state['decisions']),('release',state['releases'])]:
                for entry in entries:
                    rid=entry['request_id'];t=state['tasks'][rid];version=entry['version']
                    output=state['requests'][rid]['versions'][str(version)]['output']
                    sc=score(output,gold[t['source']['id']][t['question_id']])
                    history.append(dict(record_kind=kind,run_id=run['run_id'],session_id=s['session_id'],condition=s['condition'],request_id=rid,version=version,event_kind=category,action=entry.get('decision','release'),official_em=sc['em'],official_f1=sc['f1'],joint_correct=sc['joint'],is_current=version==state['requests'][rid]['current_version'],event=entry))
    write(out/'version_history_official.json',history)


def participant_figures(rows, paired, out):
    """Only validated participant exports reach here; no fixture performance figures."""
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(10,3.6))
    codes=sorted({r['participant_code'] for r in rows})
    for code in codes:
        rs={r['condition']:r for r in rows if r['participant_code']==code}
        xs=[i for i,c in enumerate(('Q','G','M')) if c in rs]
        for ax,key in zip(axes,('correct_release_proportion','incorrect_released','unfinished')):
            ax.plot(xs,[rs[c][key] for c in ('Q','G','M') if c in rs],marker='o',alpha=.65)
    for ax,title in zip(axes,('Correct releases / offered','Incorrect releases','Unfinished answers')):
        ax.set(xticks=[0,1,2],xticklabels=['Q','G','M'],title=title)
        for spine in ('top','right'):ax.spines[spine].set_visible(False)
    axes[0].set_ylim(-.02,1.02)
    fig.suptitle('Recorded participant outcomes; each line is one person')
    fig.text(.5,.015,'12 offered questions and 9 minutes in each condition. Incomplete records remain visible.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,.05,1,.94])
    for ext in ('svg','pdf','png'):fig.savefig(Path(out)/('participant_outcomes.'+ext),dpi=200)
    plt.close(fig)


def main():
    p=argparse.ArgumentParser();p.add_argument('exports',nargs='*');p.add_argument('--out',required=True)
    p.add_argument('--kind',choices=['participant','investigator_practice','software_fixture'],default='participant');p.add_argument('--adjudications');args=p.parse_args()
    if args.adjudications:print(apply_adjudication(args.out,args.adjudications));return
    paths=[]
    for name in args.exports:
        path=Path(name);paths.extend(sorted(path.glob('*.pilot.json')) if path.is_dir() else [path])
    if not paths:raise SystemExit('No exports supplied. Participant results remain unpopulated.')
    import json
    print(json.dumps(analyze(paths,Path(args.out),args.kind),indent=2))


if __name__=='__main__':main()
