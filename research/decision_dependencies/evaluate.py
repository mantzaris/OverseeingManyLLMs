"""Paired saved-output evaluation. This is the only module given private labels."""
import argparse
import csv
import gzip
import hashlib
import io
import json
import time
from pathlib import Path
from .client import ART, canonical, write_json
from .data import ROLES, role_keys
from .application import artifact
from .records import DecisionController, extracted_records, parsed_queries, model_answers, normalize

METHODS=['independent','full_history','semantic_memory','records_read',
         'global_barrier','dependency_barrier','no_source_guard','no_scope','confirm_records']
DEMANDS=[2,4,6]
BUDGETS=[0,2,6,None]


def simulate(case,gold,prepared,method,demand,budget,databases):
    started=time.perf_counter();outputs=prepared['outputs'];controller=DecisionController(case['project'])
    maps=[parsed_queries(outputs.get('parse%d'%v)) for v in range(2)]
    source_guard=method!='no_source_guard'
    records=[];rejections=[]
    for stage in range(2):
        accepted,rejected=extracted_records(outputs.get('extract%d'%stage),case['stages'][stage],source_guard)
        records.append(accepted);rejections.append(rejected)
    stats=dict(questions=0,distinct_questions=0,unanswered_questions=0,incorrect_reuse=0,
               reused_answers=0,scope_confirmations=0,candidate_sources=0,
               version_checks=0,revalidation_reads=0,changed_instruction_recoveries=0,
               changed_instruction_failures=0,initial_wrong_fields=0)
    stats['stale_or_wrong_retained_uses']=0
    asked=set();distinct_decisions=set();inspected=set();wrong_sources={};question_records=[];task_values={};task_answers={}
    after_gold=gold['annotation_states'][1];before_gold=gold['annotation_states'][0]
    keys=case['keys'];query_ids=[{k:case['queries'][v][i]['id'] for i,k in enumerate(keys)} for v in range(2)]
    def request_for(role,key,stage):
        v=ROLES.index(role)%2;qid=query_ids[v][key];q=next(q for q in case['queries'][v] if q['id']==qid)
        return dict(id='%s:%s:%s'%(role,key,stage),project=case['project'],text=q['text'],
                    key=maps[v].get(qid),kind='preference',agent=role),v,qid
    def resolve(role,key,stage):
        request,v,qid=request_for(role,key,stage);target=request.get('key')
        controller.requests[request['id']]=request
        cached=controller.answer_cache.get(('scope',target))
        if method=='independent':answer=dict(status='needs_user',reason='Independent request')
        elif cached:answer=cached
        elif method in ('full_history','semantic_memory'):
            prefix='history' if method=='full_history' else 'memory'
            value=model_answers(outputs.get('%s%d_%d'%(prefix,stage,v))).get(qid)
            answer=dict(status='available',value=value,key=target,
                        basis=dict(key=target,epoch=controller.epoch,origin='snapshot'),
                        source=dict(authority='model_answer',scope_status='inferred')) if value is not None else dict(status='needs_user',reason='Model abstained or failed')
        else:answer=controller.lookup(request,ignore_scope=method=='no_scope')
        if method=='confirm_records' and not cached and answer['status']=='available':
            answer=dict(status='needs_user',reason='Explicitly confirm the inferred answer and its scope')
            stats['scope_confirmations']+=1
        if answer['status']=='needs_user':
            signature=(stage,key)
            stats['questions']+=1;asked.add(signature)
            distinct_decisions.add((key,gold['annotation_states'][stage][key]))
            available=budget is None or controller.confirmations<budget
            question_records.append(dict(stage=stage,role=role,key=key,reason=answer.get('reason'),answered=available))
            controller.event('question_shown',request=request,reason=answer.get('reason'),answered=available)
            if not available:
                stats['unanswered_questions']+=1
                return dict(status='unresolved',value=None,key=target)
            # Labels enter only as an explicitly requested simulated user response.
            truth=gold['annotation_states'][stage][key]
            answer=controller.answer(request,truth,scope='request' if method=='independent' else 'project',key=key)
        else:
            stats['reused_answers']+=1
            inspected.add((stage,answer.get('key')))
            if answer['value']!=gold['annotation_states'][stage][key]:
                stats['incorrect_reuse']+=1
                source_id=(stage,answer.get('key'),answer.get('value'))
                wrong_sources.setdefault(source_id,set()).add(role)
        return answer

    controller.publish(records[0],reason='Initial released dialogue prefix')
    # Never count an empty derived artifact as an additional completed goal.
    roles=[role for role in ROLES[:demand] if role_keys(role,sorted(after_gold))]
    for role in roles:
        fields=role_keys(role,sorted(before_gold))
        answers={key:resolve(role,key,0) for key in fields}
        task_answers[role]=answers
        stats['initial_wrong_fields']+=sum(a['status']=='available' and a['value']!=before_gold[k] for k,a in answers.items())
        controller.prepare(role,{k:a for k,a in answers.items() if a['status']=='available'})
    controller.publish(records[1],reason='Remaining source dialogue released; no earlier access to future turns')
    final_artifacts=[]
    for role in roles:
        fields=role_keys(role,sorted(after_gold));previous=task_answers[role];answers={}
        for key in fields:
            old=previous.get(key);reuse=False
            if old and old['status']=='available':
                if method=='records_read':reuse=True
                elif method in ('dependency_barrier','no_source_guard','no_scope','confirm_records'):
                    stats['version_checks']+=1;reuse=controller.current(old['basis'])
                elif method=='global_barrier':stats['version_checks']+=1
            if reuse:
                answers[key]=old;stats['reused_answers']+=1
                if old['value']!=after_gold[key]:
                    stats['incorrect_reuse']+=1;stats['stale_or_wrong_retained_uses']+=1
                    source_id=(0,old.get('key'),old.get('value'))
                    wrong_sources.setdefault(source_id,set()).add(role)
            else:
                if old:stats['revalidation_reads']+=1
                answers[key]=resolve(role,key,1)
            if key in gold['changed_fields']:
                if answers[key]['status']=='available' and answers[key]['value']==after_gold[key]:stats['changed_instruction_recoveries']+=1
                else:stats['changed_instruction_failures']+=1
        available={k:a for k,a in answers.items() if a['status']=='available'}
        controller.prepare(role,available)
        missing=sorted(set(fields)-set(available));values={k:a['value'] for k,a in available.items()}
        expected={k:after_gold[k] for k in fields}
        output=artifact(role,values,databases) if not missing else None
        correct=not missing and values==expected and output==artifact(role,expected,databases)
        released=False if missing else controller.release(role,barrier=method!='records_read')
        if missing:
            controller.tasks[role]['status']='unresolved';controller.event('work_unresolved',task_id=role,missing=missing)
        final_artifacts.append(dict(role=role,status='unresolved' if missing or not released else 'correct' if correct else 'incorrect',
                                    values=values,expected=expected,missing=missing,output=output,
                                    expected_output=artifact(role,expected,databases)))
    stats['distinct_questions']=len(asked);stats['candidate_sources']=len(inspected)
    stats['distinct_decisions_requested']=len(distinct_decisions)
    stats['repeated_decision_questions']=stats['questions']-len(distinct_decisions)
    stats['repeated_question_requests']=stats['questions']-len(asked)
    stats['answered_questions']=controller.confirmations
    stats['maximum_error_fanout']=max([len(v) for v in wrong_sources.values()] or [0])
    stats['correct_artifacts']=sum(x['status']=='correct' for x in final_artifacts)
    stats['incorrect_artifacts']=sum(x['status']=='incorrect' for x in final_artifacts)
    stats['final_wrong_fields']=sum(sum(v!=after_gold[k] for k,v in x['values'].items()) for x in final_artifacts)
    stats['unresolved_artifacts']=sum(x['status']=='unresolved' for x in final_artifacts)
    stats['project_correct']=int(stats['correct_artifacts']==len(roles))
    stats['artifact_accuracy']=stats['correct_artifacts']/len(roles)
    stats['failed_generation_calls']=sum(c['status']!='ok' or c['parsed'] is None for c in prepared['calls'])
    row=dict(id=case['id'],replicate=prepared['replicate'],method=method,demand=demand,
             budget='unlimited' if budget is None else budget,changed=int(bool(gold['changed_fields'])),
             original_project_goals=1,artifact_goals=len(roles),**stats)
    row['inactive_empty_roles']=demand-len(roles)
    trace=dict(row=row,events=controller.events,artifacts=final_artifacts,questions=question_records,
               source_rejections=rejections,controller_final=controller.snapshot())
    # Runtime is measured separately; excluded from deterministic replay hashes.
    latency=time.perf_counter()-started
    return row,trace,latency

def evaluate(split,output_dir=None):
    output=Path(output_dir) if output_dir else ART/split
    output.mkdir(parents=True,exist_ok=True)
    cases=[c for c in json.loads((ART/'data/public_projects.json').read_text()) if c['split']==split]
    labels={c['id']:c for c in json.loads((ART/'data/evaluation_only.json').read_text())}
    databases={k:json.loads((ART/('data/%s_db.json'%k)).read_text()) for k in ('hotel','restaurant')}
    rows=[];latencies=[];digest=hashlib.sha256();count=0
    with (output/'traces.jsonl.gz').open('wb') as raw:
        with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0,filename='') as archive:
            for case in cases:
                paths=sorted((ART/'prepared').glob(split+'_'+case['project']+'_*.json'))
                for path in paths:
                    prepared=json.loads(path.read_text())
                    for demand in DEMANDS:
                        for budget in BUDGETS:
                            for method in METHODS:
                                row,trace,latency=simulate(case,labels[case['id']],prepared,method,demand,budget,databases)
                                payload=(canonical(trace)+'\n').encode();archive.write(payload);digest.update(payload)
                                rows.append(row);latencies.append(latency);count+=1
    if not rows:raise RuntimeError('No prepared cases to evaluate')
    with (output/'episodes.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    write_json(output/'replay.json',dict(rows=count,trace_sha256=digest.hexdigest(),
               csv_sha256=hashlib.sha256((output/'episodes.csv').read_bytes()).hexdigest(),
               projects=len(set(r['id'] for r in rows))))
    ordered=sorted(latencies)
    write_json(output/'controller_timing.json',dict(runs=len(ordered),total_seconds=sum(ordered),
               median_ms=1000*ordered[len(ordered)//2],p95_ms=1000*ordered[int(.95*(len(ordered)-1))]))
    print('Evaluated',count,'paired rows from',len(set(r['id'] for r in rows)),'projects')
    return rows

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--split',choices=['development','evaluation'],required=True)
    p.add_argument('--output-dir');a=p.parse_args();evaluate(a.split,a.output_dir)
