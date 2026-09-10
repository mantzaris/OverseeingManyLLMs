#!/usr/bin/env python3
"""Audit all pinned retail splits without consulting model outputs."""
import ast
from collections import Counter, defaultdict
import copy
import json
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.domain import digest
from overseeing.io import utc_now,write_json
from overseeing.retail.upstream import RETAIL,MUTATIONS,account_database,load_database,invoke,state_hash

ROOT=Path('artifacts/stage6_robustness')
FAMILIES=('modify','cancel','return_exchange')


def candidate(split,index,node,data):
    values={v.arg:v.value for v in node.keywords}
    actions=[{v.arg:ast.literal_eval(v.value) for v in a.keywords} for a in values['actions'].elts]
    mutations=[a for a in actions if a['name'].startswith(('cancel_','modify_','return_','exchange_'))]
    uid=ast.literal_eval(values['user_id']);text=ast.literal_eval(values['instruction'])
    if len(mutations)!=1 or mutations[0]['name'] not in MUTATIONS or values['outputs'].elts:
        raise ValueError('Outside historical single-transaction supported subset or additional output requirement')
    action=mutations[0];name=action['name'];args=action['kwargs'];order=data['orders'][args['order_id']]
    if order['user_id']!=uid:raise ValueError('Target account/order mismatch')
    if name.startswith(('modify','exchange')):
        pairs=re.findall(r'(\{[^{}]*\}) to (\{[^{}]*\})',text)
        if len(pairs)!=len(args['item_ids']):raise ValueError('Outside historical explicit item-preference template')
        match=re.search(r'For (#[A-Z]\d+),',text)
        if not match or match.group(1)!=args['order_id']:raise ValueError('Source order mismatch')
        for old,new,(a,b) in zip(args['item_ids'],args['new_item_ids'],pairs):
            before,after=ast.literal_eval(a),ast.literal_eval(b)
            item=next(i for i in order['items'] if i['item_id']==old)
            variants=data['products'][item['product_id']]['variants']
            wanted=dict(before,**after)
            matches=[k for k,v in variants.items() if v['available'] and v['options']==wanted]
            if not after or variants[old]['options']!=before or variants[new]['options']!=wanted or matches!=[new]:
                raise ValueError('Ambiguous/no-op preference or inconsistent annotated item mapping')
    elif name.startswith('cancel'):
        match=re.search(r'Cancel order (#[A-Z]\d+) because (no longer needed|ordered by mistake)',text)
        if not match:raise ValueError('Outside historical explicit cancellation template')
        if match.group(1)!=args['order_id'] or match.group(2)!=args['reason']:raise ValueError('Cancel intent mismatch')
    elif name.startswith('return'):
        match=re.search(r'Return (#[A-Z]\d+) via [a-z_]+\d+: (.*)',text)
        if not match:raise ValueError('Outside historical explicit return template')
        if match.group(1)!=args['order_id']:raise ValueError('Return order mismatch')
        names=[s.strip() for s in match.group(2).split(';') if s.strip()]
        selected=[i['name'] for i in order['items'] if i['item_id'] in args['item_ids']]
        if Counter(names)!=Counter(selected) or any(sum(i['name']==n for i in order['items'])!=names.count(n) for n in names):
            raise ValueError('Return names or multiplicity do not uniquely identify annotation')
    if 'payment_method_id' in args:
        match=re.search(r'via ([a-z_]+\d+)',text)
        if not match or match.group(1)!=args['payment_method_id']:raise ValueError('Payment destination mismatch')
    initial=account_database(data,uid);target=copy.deepcopy(initial);proposal=dict(tool=name,arguments=args)
    response=invoke(target,proposal)
    if response.startswith('Error:') or state_hash(initial)==state_hash(target):raise ValueError('Annotated mutation rejected or no-op')
    family='cancel' if name.startswith('cancel') else 'modify' if name.startswith('modify') else 'return_exchange'
    public=re.sub(r'You are [^.]*\.\s*','',text).replace('Your name is','My name is').strip()
    return dict(case_id=split+':{:03d}'.format(index),source_split=split,source_index=index,source_instruction=text,
        source_actions=actions,user_id=uid,order_id=args['order_id'],family=family,customer_message=public,
        target_action=proposal,initial_state_hash=state_hash(initial),target_state_hash=state_hash(target),
        source_case_group=uid,source_instruction_hash=digest(text),partition='evaluation')


def main():
    if (ROOT/'cases.json').exists():raise FileExistsError('Source audit already frozen')
    historical=Path('artifacts/stage5_practical');excluded=set();exclusion_provenance=[]
    for path in sorted(historical.glob('cases*.json')):
        record=json.loads(path.read_text());groups={c['source_case_group'] for c in record.get('cases',[])}
        excluded.update(groups);exclusion_provenance.append(dict(path=str(path),groups=sorted(groups),record_hash=digest(record)))
    data=load_database();candidates=[];audit=[];account_records=defaultdict(list)
    for split in ('train','dev','test'):
        tree=ast.parse((RETAIL/('tasks_'+split+'.py')).read_text())
        tasks=next(n.value.elts for n in tree.body if isinstance(n,ast.Assign))
        for index,node in enumerate(tasks):
            values={v.arg:v.value for v in node.keywords};uid=ast.literal_eval(values['user_id'])
            key=split+':{:03d}'.format(index);account_records[uid].append(key)
            try:
                case=candidate(split,index,node,data);reason=None
                if uid in excluded:reason='Stage 5 account exclusion (all variants and source splits)'
                else:candidates.append(case)
            except (ValueError,KeyError,StopIteration,TypeError) as exc:reason=str(exc) or type(exc).__name__
            audit.append(dict(case_id=key,user_id=uid,eligible=reason is None,reason=reason))
    def select(n):
        used=set(excluded);chosen=[]
        for family in FAMILIES:
            group=[]
            for c in candidates:
                if c['family']==family and c['source_case_group'] not in used:
                    used.add(c['source_case_group']);group.append(c)
                    if len(group)==n:break
            if len(group)<n:return None
            chosen+=group
        return chosen
    chosen=select(16);n=16
    if chosen is None:chosen=select(8);n=8
    if chosen is None:chosen=[];n=0
    counts={f:len({c['source_case_group'] for c in candidates if c['family']==f}) for f in FAMILIES}
    duplicates={u:ids for u,ids in account_records.items() if len({x.split(':')[0] for x in ids})>1}
    record=dict(created_utc=utc_now(),upstream_revision='59a200c6d575d595120f1cb70fea53cef0632f6b',
        selection_rule='Source order train, dev, test; ascending index within family; reserve modification first, cancellation second, return/exchange third; globally distinct customer accounts. Choose 16 bundles if feasible, otherwise 8, otherwise saved-data sensitivity only.',
        eligibility='Historical explicit-template, single-supported-mutation/no-output subset, plus all Stage 5 source-intent consistency checks. No model outcomes used.',
        cases=chosen,bundle_count=n,distinct_source_cases=len(chosen),excluded_stage5_accounts=sorted(excluded),
        exclusion_provenance=exclusion_provenance,eligible_unused_accounts_by_family=counts,
        duplicate_accounts_across_splits=duplicates,all_account_occurrences=dict(account_records),eligibility_audit=audit,
        limitations='Public benchmark records may have been in training. Source cases/accounts are disjoint, broad workflow templates are shared. Source-split labels do not imply unseen model training data.')
    record['case_manifest_hash']=digest(record);write_json(ROOT/'cases.json',record)
    print(json.dumps(dict(bundles=n,cases=len(chosen),excluded_accounts=len(excluded),eligible_unused_accounts_by_family=counts,
        selected_splits=dict(Counter(c['source_split'] for c in chosen)),duplicate_accounts_across_splits=len(duplicates),manifest_hash=record['case_manifest_hash']),indent=2))

if __name__=='__main__':main()
