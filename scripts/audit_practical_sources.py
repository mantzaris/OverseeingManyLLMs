#!/usr/bin/env python3
"""Check selected upstream intents against target identifiers, without model outputs."""
import ast
from collections import Counter
import json
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.io import write_json,utc_now
from overseeing.retail.upstream import load_database
root=Path('artifacts/stage5_practical');cases=json.loads((root/'cases.json').read_text())['cases'];data=load_database()
issues=[];checked=[]
for case in cases:
    action=case['target_action'];args=action['arguments'];text=case['source_instruction'];order=data['orders'][args['order_id']]
    checks=[]
    if action['tool'].startswith(('modify','exchange')):
        pairs=re.findall(r'(\{[^{}]*\}) to (\{[^{}]*\})',text)
        assert len(pairs)==len(args['item_ids'])==len(args['new_item_ids'])
        assert re.search(r'For (#[A-Z]\d+),',text).group(1)==args['order_id']
        for old,new,(before,after) in zip(args['item_ids'],args['new_item_ids'],pairs):
            item=next(i for i in order['items'] if i['item_id']==old)
            variants=data['products'][item['product_id']]['variants']
            if variants[old]['options']!=ast.literal_eval(before):issues.append([case['case_id'],'source old options mismatch'])
            wanted=dict(ast.literal_eval(before),**ast.literal_eval(after))
            matches=[k for k,v in variants.items() if v['available'] and v['options']==wanted]
            if matches!=[new]:issues.append([case['case_id'],'source new options ambiguous or inconsistent'])
        checks+=['source old options match actual items','new preferences retain unspecified options and identify unique available target']
    if action['tool'].startswith('cancel'):
        match=re.search(r'Cancel order (#[A-Z]\d+) because (no longer needed|ordered by mistake)',text)
        if match.group(1)!=args['order_id'] or match.group(2)!=args['reason']:issues.append([case['case_id'],'cancel intent mismatch'])
        checks+=['cancellation order and reason match source intent']
    if 'payment_method_id' in args:
        if re.search(r'via ([a-z_]+\d+)',text).group(1)!=args['payment_method_id']:issues.append([case['case_id'],'payment intent mismatch'])
        checks+=['payment/refund destination matches source intent']
    if action['tool'].startswith('return'):
        match=re.search(r'Return (#[A-Z]\d+) via [a-z_]+\d+: (.*)',text)
        if match.group(1)!=args['order_id']:issues.append([case['case_id'],'return order mismatch'])
        names=[s.strip() for s in match.group(2).split(';') if s.strip()]
        selected=[i['name'] for i in order['items'] if i['item_id'] in args['item_ids']]
        if Counter(names)!=Counter(selected):issues.append([case['case_id'],'return named items mismatch'])
        if any(sum(i['name']==name for i in order['items'])!=names.count(name) for name in names):
            issues.append([case['case_id'],'return named items do not uniquely identify intended list'])
        checks+=['return names and multiplicities uniquely identify target items']
    checked.append(dict(case_id=case['case_id'],partition=case['partition'],checks=checks))
result=dict(status='verified' if not issues else 'issues_retained',verified_utc=utc_now(),
    scope='Post-freeze source-intent audit only; no model outputs used, no source case replaced or method changed.',
    cases=len(cases),cases_by_tool=dict(Counter(c['target_action']['tool'] for c in cases)),issues=issues,checked=checked)
write_json(root/'source_intent_audit.json',result)
print(json.dumps({k:v for k,v in result.items() if k!='checked'},indent=2))
if issues:raise SystemExit(1)
