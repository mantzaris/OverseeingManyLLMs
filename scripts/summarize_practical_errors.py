#!/usr/bin/env python3
"""Descriptive policy-check and intent-error audit of saved application outputs.

Added after freeze to make the distinction explicit; it changes no primary metric.
"""
from collections import Counter,defaultdict
import csv
import gzip
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.io import write_json,read_events
from overseeing.retail.analysis import csv_file,semantic_classes
from overseeing.retail.upstream import MUTATIONS

root=Path('artifacts/stage5_practical');batch=root/'batches/evaluation';out=batch/'analysis'
cases={c['case_id']:c for c in json.loads((root/'cases.json').read_text())['cases']}
prepared=[r for p in sorted((batch/'prepared').glob('*/workflows.json')) for r in json.loads(p.read_text())]
blocked=[];classes=Counter();families=[]
for r in prepared:
    for event in r['events']:
        if event['response'].startswith('Error:'):
            blocked.append(dict(bundle_id=r['bundle_id'],replicate=r['replicate'],case_id=r['case_id'],
                step=event['step'],tool=event['call']['tool'],mutation_attempt=event['call']['tool'] in MUTATIONS,
                check='adapter_policy_guard' if event['response'].startswith('Error: automatic safeguard:') else 'upstream_backend',
                reason=event['response']))
    if r['initial_error']:
        classes.update(semantic_classes(r['proposal'],cases[r['case_id']]['target_action']))
for family in ('cancel','modify','return_exchange'):
    group=[r for r in prepared if r['family']==family]
    families.append(dict(family=family,workflows=len(group),source_cases=len({r['case_id'] for r in group}),
        staged=sum(r['proposal'] is not None for r in group),initial_correct=sum(r['initial_task_success'] for r in group),
        initial_wrong_valid=sum(r['initial_error'] for r in group),unstaged_failures=sum(r['proposal'] is None for r in group),
        mean_tool_turns=sum(r['tool_steps'] for r in group)/len(group)))
tools=[]
for tool in sorted({c['target_action']['tool'] for c in cases.values()}):
    group=[r for r in prepared if cases[r['case_id']]['target_action']['tool']==tool]
    tools.append(dict(intended_tool=tool,workflows=len(group),source_cases=len({r['case_id'] for r in group}),
        staged=sum(r['proposal'] is not None for r in group),initial_correct=sum(r['initial_task_success'] for r in group),
        initial_wrong_valid=sum(r['initial_error'] for r in group),unstaged_failures=sum(r['proposal'] is None for r in group),
        mean_tool_turns=sum(r['tool_steps'] for r in group)/len(group)))
csv_file(out/'blocked_tool_attempts.csv',blocked);csv_file(out/'workflow_family_outcomes.csv',families)
csv_file(out/'workflow_tool_outcomes.csv',tools)
generation_failures=[]
for path in sorted((batch/'prepared').glob('*/*_raw.jsonl.gz')):
    for r in read_events(path):
        if r['phase']=='attempt_finished' and 'error' in r:
            generation_failures.append(dict(**r['metadata'],call_id=r['session_call_id'],retry=r['retry'],
                http_status=r.get('http_status'),error=r['error'],input_tokens=r.get('input_tokens'),
                output_tokens=(r.get('usage') or {}).get('completion_tokens'),raw_path=str(path.relative_to(root))))
csv_file(out/'generation_failures.csv',generation_failures)
failure_modes=[]
for r in prepared:
    if r['proposal'] is not None:continue
    if r['failure']=='Maximum agent tool-call steps reached':mode='step_limit'
    elif r['failure'] is None:
        assert r['events'][-1]['call']['tool']=='finish'
        mode='explicit_finish_without_staging'
    else:mode='generation_retry_exhausted' if 'Truncated generation' in r['failure'] else 'other_recorded_failure'
    failure_modes.append(dict(bundle_id=r['bundle_id'],replicate=r['replicate'],case_id=r['case_id'],mode=mode,recorded_failure=r['failure']))
csv_file(out/'workflow_failure_modes.csv',failure_modes)
initial_labels={(r['bundle_id'],r['replicate'],r['case_id']):r['initial_error'] for r in prepared}
queue_rows=[]
for path in sorted((out/'traces').glob('*/*.json.gz')):
    trace=json.loads(gzip.decompress(path.read_bytes()))
    for event in trace['events']:
        if event['event']!='dispatch':continue
        useful=sum(initial_labels[(trace['bundle_id'],trace['replicate'],cid)] for cid in event['eligible'])
        queue_rows.append(dict(bundle_id=trace['bundle_id'],replicate=trace['replicate'],policy=trace['policy'],
            review_duration=trace['review_duration'],tick=event['tick'],eligible=len(event['eligible']),
            initially_wrong_eligible=useful,greedy_search_heads_differ=event['greedy_choice']!=event['search_choice']))
csv_file(out/'retrospective_queue_diagnostics.csv',queue_rows)
queue_summary=[]
for duration in (1,2):
    for policy in ('no_review','fcfs','edf','uncertainty','greedy','search'):
        group=[r for r in queue_rows if r['policy']==policy and r['review_duration']==duration]
        queue_summary.append(dict(policy=policy,review_duration=duration,dispatches=len(group),
            multiple_eligible=sum(r['eligible']>=2 for r in group),
            multiple_initially_wrong_eligible=sum(r['initially_wrong_eligible']>=2 for r in group)))
result=dict(label='Post-freeze descriptive audit; no method or primary analysis changes',
    blocked_tool_calls=len(blocked),blocked_mutation_calls=sum(r['mutation_attempt'] for r in blocked),
    checks=dict(Counter(r['check'] for r in blocked)),reasons=dict(Counter(r['reason'] for r in blocked)),
    initial_wrong_valid_error_classes=dict(classes),error_classes_can_overlap=True,
    automatic_rejections_feature=sum(r['automatic_rejections'] for r in prepared),
    distinction='Blocked invalid calls never commit. Wrong valid transactions violate the annotated task intent while passing active automatic checks. These counts are not a complete natural-language policy-compliance classifier.',
    families=families,intended_tool_outcomes=tools,generation_failed_attempts=len(generation_failures),
    workflow_failure_modes=dict(Counter(r['mode'] for r in failure_modes)),retrospective_queue_summary=queue_summary,
    retrospective_boundary='Initial error labels are used only for this offline descriptive audit, never scheduler or agent inputs.')
write_json(out/'policy_and_intent_audit.json',result)
print(json.dumps(result,indent=2))
