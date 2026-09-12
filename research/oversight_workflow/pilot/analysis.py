"""Offline participant-level descriptions. Never imported by the task server."""
import argparse,csv,json,random,statistics
from pathlib import Path
from collections import Counter,defaultdict
from research.oversight_workflow.common import read,write,digest,ART
from research.oversight_workflow.protocol import replay
from research.oversight_workflow.offline import labels
from research.adaptive_correction_transfer.scoring import score
from .materials import PILOT,VERSION

def csv_write(path,rows):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('w',newline='') as f:
  if rows:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def expected(m,run,s):
 if s['block_index']==0:
  c=read(PILOT.parent/'study/training.json');return 'training',None,{q['id'] for q in c['questions']}
 b=m['assignments'][run['assignment']]['blocks'][s['block_index']-1];p=m['packets'][b['packet']]
 return b['condition'],b['packet'],set(p['source_only_question_ids'] if b['condition']=='S' else p['question_ids'])

def load_runs(paths,kind):
 m=read(PILOT/'manifest.json');unique={};duplicates=0
 for p in paths:
  r=read(p)
  if r.get('record_kind')!=kind:raise ValueError('Refusing record-kind mixing: '+str(p))
  if r.get('schema')!='oversight-pilot-export-v1' or r.get('pilot_version')!=VERSION or r.get('manifest_sha256')!=m['manifest_sha256']:raise ValueError('Unknown pilot version or manifest')
  if not isinstance(r['assignment'],int) or not 0<=r['assignment']<len(m['assignments']):raise ValueError('Incorrect assignment')
  rid=r['run_id']
  if rid in unique:
   if digest(unique[rid])!=digest(r):raise ValueError('Conflicting exports of one run; select the final export explicitly')
   duplicates+=1;continue
  if any(x['participant_code']==r['participant_code'] for x in unique.values()):raise ValueError('Multiple runs for one participant code; resolve repeat-run provenance explicitly')
  sessions=r['sessions']+([r['active_session']] if r.get('active_session') else [])
  blocks=set()
  for s in sessions:
   if s['record_kind']!=kind or s['block_index'] in blocks:raise ValueError('Duplicate block or mixed session provenance')
   blocks.add(s['block_index']);cond,packet,qids=expected(m,r,s)
   if s['condition']!=cond or s['packet']!=packet or set(s['question_ids'])!=qids:raise ValueError('Incorrect packet assignment')
   if len(s['question_ids'])!=len(qids):raise ValueError('Duplicate questions')
   if s['desk_condition']!=('sessions' if cond in ('C','training') else 'queue'):raise ValueError('Incorrect interface configuration')
   d=replay(s['events'],s['desk_condition'])
   if d.logical()!=s['state']:raise ValueError('Saved-state replay mismatch')
   if {t['question_id'] for t in s['state']['tasks'].values()}!=qids:raise ValueError('Offered workload differs from assigned workload')
   if cond!='training':
    manifest_contexts={c['id']:c for c in read(ART/'frozen/manifest.json')['contexts']}
    for t in s['state']['tasks'].values():
     c=manifest_contexts[t['source']['id']]
     if t['source']['table']!=c['table'] or t['source']['paragraphs']!=c['paragraphs'] or not any(q['id']==t['question_id'] and q['question']==t['question'] for q in c['questions']):raise ValueError('Source or question provenance mismatch')
   if kind=='participant':
    a=r.get('authorization') or {}
    if a.get('collection_authorized') is not True or not all(a.get(k) for k in ('institutional_determination','consent_version','investigator','collection_authorized','record_reference')):raise ValueError('Missing authorization provenance')
    limit=m['training_seconds'] if cond=='training' else m['source_only_seconds'] if cond=='S' else m['review_seconds']
    if s['duration_seconds']!=limit:raise ValueError('Unapproved timing override in participant data')
  unique[rid]=r
 return list(unique.values()),duplicates

def intervals(values):
 if len(values)<6:return None
 rng=random.Random(92741);means=sorted(statistics.mean(rng.choices(values,k=len(values))) for _ in range(2000))
 return [means[49],means[1949]]

def analyze(paths,out,kind='participant'):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);runs,duplicates=load_runs(paths,kind);gold=labels();rows=[];answers=[];timing=[];blind=[];private=[];missing=[]
 for run in runs:
  missing.append(dict(code=run['participant_code'],run_id=run['run_id'],withdrawn=run['withdrawn'],missing_completed_blocks=sorted(set(range(4))-{s['block_index'] for s in run['sessions']}),active_export=bool(run.get('active_session')),planned_scored_questions=30,offered_scored_questions=sum(len(s['state']['tasks']) for s in run['sessions']+([run['active_session']] if run.get('active_session') else []) if s['condition']!='training')))
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
    original=score(r['versions']['1']['output'],g) if r and s['condition']!='S' else None
    row=dict(record_kind=kind,participant_code=run['participant_code'],run_id=run['run_id'],session_id=s['session_id'],condition=s['condition'],packet=s['packet'],request_id=rid,question_id=t['question_id'],source_id=t['source']['id'],version=v,offered=1,started=int(t['started_at'] is not None),received=int(bool(r)),approved=int(approved),released=int(released),official_em=sc['em'] if released else None,official_f1=sc['f1'] if released else None,joint_correct=int(released and sc['joint']),incorrect_released=int(released and not sc['joint']),answer_em_correct=int(released and sc['em']),approved_joint_correct=int(approved and sc['joint']),incorrect_approved=int(approved and not sc['joint']),blocked=int(bool(ds and ds[-1]['decision']=='reject')),corrected=int(any(d['request_id']==rid and d['decision']=='correct' for d in st['decisions']) and s['condition']!='S'),initial_joint=original['joint'] if original else None,unresolved=int(not r or r['status'] in ('queued','active','deferred')),unfinished=int(not released),answer=output['answer'] if output else [],scale=output.get('scale','') if output else '')
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
   for i in range(3):row['control_'+str(i+1)]=q['control'][i] if q else None
   rows.append(row)
 paired=[]
 for run in runs:
  rs={r['condition']:r for r in rows if r['run_id']==run['run_id'] and r['status']!='interrupted_active_export'}
  if 'B' not in rs or 'C' not in rs:continue
  p=dict(record_kind=kind,participant_code=run['participant_code'],run_id=run['run_id'],withdrawn=run['withdrawn'])
  for k in ('joint_correct','incorrect_released','unfinished','corrected','released','select_to_action_seconds','resumed_select_to_action_seconds','source_revisits','tlx_raw_mean','control_1','control_2','control_3'):
   p[k+'_C_minus_B']=rs['C'][k]-rs['B'][k] if rs['C'][k] is not None and rs['B'][k] is not None else None
  paired.append(p)
 summary=dict(record_kind=kind,interpretation='Synthetic software fixtures; NOT human findings' if kind=='software_fixture' else 'Investigator practice; NOT independent participant evidence' if kind=='investigator_practice' else 'Small formative observations, not powered superiority evidence',runs=len(runs),duplicate_exports_ignored=duplicates,paired_runs=len(paired),missing=missing,unit='Participant for genuine observations; fixture runs are not participants. Reused source contexts also induce dependence. No question-level inference.',timing_limit='Select-to-action elapsed time includes thinking, interruptions and idle time; it is not continuous reading time. Source focus counts are interaction proxies.',participant_results_populated=kind=='participant' and bool(runs),paired={})
 for k in ['joint_correct_C_minus_B','incorrect_released_C_minus_B','unfinished_C_minus_B','tlx_raw_mean_C_minus_B']:
  xs=[p[k] for p in paired if not p['withdrawn'] and p[k] is not None];summary['paired'][k]=dict(n=len(xs),mean=statistics.mean(xs) if xs else None,median=statistics.median(xs) if xs else None,positive=sum(x>0 for x in xs),zero=sum(x==0 for x in xs),negative=sum(x<0 for x in xs),descriptive_participant_bootstrap95=intervals(xs) if kind=='participant' else None,interval_limit='Only when at least six complete nonwithdrawn pairs. Conditional on these reused packets, not a population-of-financial-sources interval.')
 csv_write(out/'sessions.csv',rows);csv_write(out/'answers_official.csv',answers);csv_write(out/'review_intervals.csv',timing);csv_write(out/'paired_descriptions.csv',paired)
 write(out/'summary.json',summary);write(out/'adjudication_blinded.json',dict(kind='Investigator-only; never serve to task browser',cases=sorted(blind,key=lambda x:x['case_id'])));write(out/'adjudication_key_PRIVATE.json',private)
 csv_write(out/'adjudication_blank.csv',[dict(case_id=b['case_id'],verdict='',reason='',rater_code='') for b in sorted(blind,key=lambda x:x['case_id'])])
 # A compact individual trajectory, never a population-effect chart from fixtures.
 if rows:
  import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
  fig,axes=plt.subplots(1,2,figsize=(8,3.7),gridspec_kw={'width_ratios':[2,1]})
  colors=['#087f8c','#ba641c','#5a609b','#6b7f39','#93596c','#34668a','#736445','#454545']
  for i,code in enumerate(sorted({r['participant_code'] for r in rows})):
   rr={r['condition']:r for r in rows if r['participant_code']==code};color=colors[i%len(colors)]
   axes[0].plot([j for j,k in enumerate(['B','C']) if k in rr],[rr[k]['joint_correct'] for k in ['B','C'] if k in rr],marker='o',color=color,label=code)
   if 'S' in rr:axes[1].plot([0],[rr['S']['joint_correct']],marker='o',color=color)
  axes[0].set(xticks=[0,1],xticklabels=['B · central queue','C · source sessions'],ylim=(-.15,12.5),yticks=[0,3,6,9,12],ylabel='Correct current-version releases',title='12 offered questions · 9 minutes')
  axes[1].set(xticks=[0],xticklabels=['Source-only'],ylim=(-.1,6.3),yticks=[0,2,4,6],title='6 offered · 4 minutes')
  for ax in axes:
   for k in ('top','right'):ax.spines[k].set_visible(False)
  fig.suptitle(summary['interpretation'],fontsize=11)
  fig.text(.5,.025,'Declared block designs shown. Fixture runs compress time. Source-only is a separate diagnostic.',ha='center',fontsize=8)
  if len(runs)<=8:axes[0].legend(fontsize=8)
  fig.tight_layout(rect=[0,.08,1,.94])
  for ext in ('svg','pdf','png'):fig.savefig(out/('individual_trajectories.'+ext),dpi=180)
  plt.close(fig)
 return summary

def apply_adjudication(analysis_dir,completed_csv):
 d=Path(analysis_dir);keys={x['case_id']:x for x in read(d/'adjudication_key_PRIVATE.json')};rows=[];seen=set()
 with open(completed_csv) as f:
  for r in csv.DictReader(f):
   if r['case_id'] not in keys or r['case_id'] in seen:raise ValueError('Unknown or duplicate adjudication case')
   seen.add(r['case_id'])
   if r['verdict'] not in ('acceptable','unacceptable','uncertain') or not r['reason'].strip() or not r['rater_code'].strip():raise ValueError('Every adjudication needs a verdict, reason and rater')
   rows.append({**keys[r['case_id']],**r})
 csv_write(d/'adjudicated_ADDITIONAL.csv',rows)
 grouped=defaultdict(Counter)
 for r in rows:grouped[r['session_id']][r['verdict']]+=1
 extra=[]
 with (d/'sessions.csv').open() as f:
  for session in csv.DictReader(f):
   counts=grouped[session['session_id']]
   extra.append({**session,'adjudicated_acceptable':counts['acceptable'],'adjudicated_unacceptable':counts['unacceptable'],'adjudicated_uncertain':counts['uncertain'],'released_not_adjudicated':int(session['released'])-sum(counts.values())})
 csv_write(d/'adjudicated_sessions_ADDITIONAL.csv',extra)
 return dict(n=len(rows),remaining=len(keys)-len(rows),official_scores='Unchanged in answers_official.csv; adjudication is an additional result')

def main():
 p=argparse.ArgumentParser();p.add_argument('exports',nargs='*');p.add_argument('--out',required=True);p.add_argument('--kind',choices=['participant','investigator_practice','software_fixture'],default='participant');p.add_argument('--adjudications');a=p.parse_args()
 if a.adjudications:print(apply_adjudication(a.out,a.adjudications));return
 paths=[]
 for s in a.exports:
  path=Path(s);paths.extend(sorted(path.glob('*.pilot.json')) if path.is_dir() else [path])
 if not paths:raise SystemExit('No exports supplied. No participant results will be invented.')
 print(json.dumps(analyze(paths,a.out,a.kind),indent=2))
if __name__=='__main__':main()
