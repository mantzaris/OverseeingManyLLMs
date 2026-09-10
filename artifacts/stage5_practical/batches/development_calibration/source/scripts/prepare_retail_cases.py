#!/usr/bin/env python3
"""Declare source-case-disjoint retail cases before model inference."""
import ast
import copy
import json
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.domain import digest
from overseeing.io import write_json, utc_now
from overseeing.retail.upstream import RETAIL, MUTATIONS, account_database, load_database, invoke, state_hash


def prepare():
    root=Path('artifacts/stage5_practical');path=root/'cases.json'
    if path.exists(): raise FileExistsError('Source selection is already declared')
    data=load_database();tree=ast.parse((RETAIL/'tasks_train.py').read_text())
    tasks=next(n.value.elts for n in tree.body if isinstance(n,ast.Assign))
    candidates=[];audit=[]
    for index,node in enumerate(tasks):
        values={v.arg:v.value for v in node.keywords}
        actions=[{v.arg:ast.literal_eval(v.value) for v in action.keywords} for action in values['actions'].elts]
        mutations=[a for a in actions if a['name'].startswith(('cancel_','modify_','return_','exchange_'))]
        reason=None
        if len(mutations)!=1 or mutations[0]['name'] not in MUTATIONS or values['outputs'].elts:
            reason='Outside single-transaction supported subset or additional output requirement'
        else:
            action=mutations[0];kwargs=action['kwargs'];instruction=ast.literal_eval(values['instruction'])
            uid=ast.literal_eval(values['user_id']);name=action['name'];order=data['orders'][kwargs['order_id']]
            if name.startswith(('modify','exchange')):
                pairs=re.findall(r'(\{[^{}]*\}) to (\{[^{}]*\})',instruction)
                if len(pairs)!=len(kwargs['item_ids']):reason='Not the supported explicit item-preference template'
                else:
                    for old,new,(a,b) in zip(kwargs['item_ids'],kwargs['new_item_ids'],pairs):
                        old_options,new_options=ast.literal_eval(a),ast.literal_eval(b)
                        item=next(i for i in order['items'] if i['item_id']==old)
                        variant=data['products'][item['product_id']]['variants'][new]
                        wanted=dict(old_options,**new_options)
                        matches=[k for k,v in data['products'][item['product_id']]['variants'].items()
                                 if v['available'] and v['options']==wanted]
                        if not new_options or variant['options']!=wanted or matches!=[new]:
                            reason='Ambiguous/no-op preferences or target inconsistent with available requested options'
            elif name.startswith('cancel') and not re.search(r'Cancel order #[A-Z]\d+ because (no longer needed|ordered by mistake)',instruction):
                reason='Not the supported explicit cancellation template'
            elif name.startswith('return') and not re.search(r'Return #[A-Z]\d+ via [a-z_]+\d+:',instruction):
                reason='Not the supported explicit return template'
            if not reason:
                initial=account_database(data,uid);target=copy.deepcopy(initial)
                proposal=dict(tool=name,arguments=kwargs)
                result=invoke(target,proposal)
                if result.startswith('Error:') or state_hash(initial)==state_hash(target):reason='Annotated transaction fails upstream validation or is a no-op'
            if not reason:
                family='cancel' if name.startswith('cancel') else 'modify' if name.startswith('modify') else 'return_exchange'
                # Remove personality instructions, not operational information. No target IDs are added.
                public=re.sub(r'You are [^.]*\.\s*','',instruction).replace('Your name is','My name is').strip()
                candidates.append(dict(case_id='train:{:03d}'.format(index),source_split='train',source_index=index,
                    source_instruction=instruction,source_actions=actions,user_id=uid,order_id=kwargs['order_id'],
                    family=family,customer_message=public,target_action=proposal,
                    initial_state_hash=state_hash(initial),target_state_hash=state_hash(target),
                    source_case_group=uid,source_instruction_hash=digest(instruction)))
        audit.append(dict(source_index=index,eligible=reason is None,reason=reason))
    selected=[];used=set()
    # Priority to the scarcest family; selection never consults LLM outputs or policy outcomes.
    for split,count in [('development',8),('evaluation',32)]:
        for family in ('modify','cancel','return_exchange'):
            available=[];seen=set(used)
            for candidate in candidates:
                if candidate['family']==family and candidate['source_case_group'] not in seen:
                    available.append(candidate);seen.add(candidate['source_case_group'])
            if len(available)<count:raise ValueError('Insufficient distinct source accounts')
            for case in available[:count]:
                used.add(case['source_case_group']);selected.append(dict(case,partition=split))
    declaration=dict(created_utc=utc_now(),upstream_revision='59a200c6d575d595120f1cb70fea53cef0632f6b',
        selection_rule='Ascending train index within supported family; development first 8/family then evaluation next 32/family; unique source customer across ALL selected cases; priority modify, cancel, return/exchange',
        split_unit='Underlying customer/account case; all variants/orders for selected user excluded from other cases. Workflow families and broad linguistic templates are shared; no unseen-template generalization claim.',
        cases=selected,eligibility_audit=audit,distinct_source_cases=len(selected),
        adaptations=['Single state-changing transaction and no additional output targets',
            'Scripted customer exposes only original task instruction, with personality sentence removed',
            'For partial option changes, unchanged options must retain their original values; annotated target checked for unique compatibility',
            'User confirms proposed details without independently auditing backend IDs; identical confirmation mechanism for every policy',
            'Account-isolated database retains all customer orders and full product catalog'])
    declaration['case_manifest_hash']=digest(declaration);write_json(path,declaration)
    print(json.dumps(dict(selected=len(selected),development=24,evaluation=96,manifest_hash=declaration['case_manifest_hash'])))

if __name__=='__main__':prepare()
