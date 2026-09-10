#!/usr/bin/env python3
"""Select declared benefit/tie/failure examples and render actual tool consequences."""
import csv,gzip,json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from overseeing.domain import canonical
from overseeing.retail.upstream import load_database

root=Path('artifacts/stage5_practical');folder=root/'batches/evaluation';analysis=folder/'analysis'
cases={c['case_id']:c for c in json.loads((root/'cases.json').read_text())['cases']};data=load_database()
rows=list(csv.DictReader((analysis/'sequence_comparisons.csv').open()))
comparisons=sorted([r for r in rows if r['review_duration']=='2' and r['comparator']=='greedy'],key=lambda r:(r['bundle_id'],int(r['replicate'])))
selections={name:next((r for r in comparisons if pred(float(r['loss_difference']))),None)
    for name,pred in [('benefit',lambda x:x<0),('tie',lambda x:x==0),('unfavorable',lambda x:x>0)]}
prepared_paths=sorted((folder/'prepared').glob('*/workflows.json'))
failed=next(((p,r) for p in prepared_paths for r in json.loads(p.read_text()) if r['proposal'] is None),None)
out=analysis/'examples';out.mkdir(exist_ok=True)
lines=['# Retail transaction examples','',
    'Selection: first ascending bundle/replicate where search beats, ties or loses to greedy at two-tick review. '
    'The first failed workflow is separate. These are saved GPU outputs with deterministic policy replays, not stipulated actions.','']
def describe(action):
    if action is None:return 'No transaction staged.'
    name=action['tool'];args=action['arguments'];order=data['orders'][args['order_id']]
    text='`'+name+'` on `'+args['order_id']+'`'
    if 'reason' in args:text+='; reason '+repr(args['reason'])
    if 'item_ids' in args:
        descriptions=[]
        for i,item_id in enumerate(args['item_ids']):
            item=next(x for x in order['items'] if x['item_id']==item_id)
            description=item['name']+' (`'+item_id+'`)'
            if 'new_item_ids' in args:
                new_id=args['new_item_ids'][i];variant=data['products'][item['product_id']]['variants'][new_id]
                description+=' → `'+new_id+'` '+canonical(variant['options'])
            descriptions.append(description)
        text+='; '+ '; '.join(descriptions)
    if 'payment_method_id' in args:text+='; payment/refund `'+args['payment_method_id']+'`'
    return text
for name,selection in selections.items():
    lines+=['## '+name.title(),'']
    if selection is None:lines+=['No such primary-comparison example occurred; none is substituted.',''];continue
    key=selection['bundle_id']+'_r'+selection['replicate'];prepared=json.loads((folder/'prepared'/key/'workflows.json').read_text())
    lines+=['Bundle `'+key+'`; search minus greedy loss = '+selection['loss_difference']+' points.','']
    for result in prepared:
        case=cases[result['case_id']]
        lines+=['**'+case['case_id']+'** — '+case['customer_message'],'',
            '- Agent proposal: '+describe(result['proposal']),
            '- Annotated intended transaction (offline/completed-review information): '+describe(case['target_action']),
            '- Preparation: '+str(result['tool_steps'])+' model/tool turns; '+str(result['automatic_rejections'])+' blocked attempts; initial error '+str(result['initial_error'])+'.','']
    lines+=['| Policy | Loss | Completed tasks | Corrections | Completed review order |','|---|---:|---:|---:|---|']
    results={}
    for policy in ['no_review','fcfs','edf','uncertainty','greedy','search']:
        result=json.loads(gzip.decompress((analysis/'traces'/key/('s2_'+policy+'.json.gz')).read_bytes()));results[policy]=result
        lines+=['| %s | %s | %s | %s | %s |'%(policy,result['operational_loss'],result['task_completed'],result['corrections'],' → '.join(result['review_sequence']))]
    lines+=['','| Tick | Search queue events | Greedy queue events | EDF queue events |','|---:|---|---|---|']
    for tick in sorted({e['tick'] for r in results.values() for e in r['events']}):
        values=[]
        for policy in ['search','greedy','edf']:
            parts=[]
            for event in results[policy]['events']:
                if event['tick']!=tick:continue
                if event['event']=='review_started':parts.append('start '+event['case_id']+' → '+str(event['completion']))
                elif event['event']=='transaction_committed':parts.append(('reviewed commit ' if event['reviewed'] else 'cutoff commit ')+event['case_id']+(' correct' if event['task_completed'] else 'WRONG'))
            values.append('; '.join(parts) or '—')
        lines+=['| %d | %s | %s | %s |'%(tick,*values)]
    lines+=['','Full preparations: [`'+key+'`](../../prepared/'+key+'/workflows.json). Full policy traces: [`'+key+'`](../traces/'+key+'/).','']
lines+=['## First failed preparation','']
if failed:
    path,result=failed;case=cases[result['case_id']]
    lines+=['`'+path.parent.name+'`, `'+case['case_id']+'`: '+case['customer_message'],'',
        'Failure: '+str(result['failure'])+'. No valid transaction entered the review queue; even the idealized unlimited-review reference cannot rescue this preparation failure.','',
        '| Step | Agent tool | Backend response (excerpt) |','|---:|---|---|']
    for event in result['events']:
        lines+=['| %d | `%s` | %s |'%(event['step'],event['call']['tool'],event['response'][:180].replace('|','/').replace('\n',' '))]
    lines+=['','[Complete failed workflow and raw-call siblings](../../prepared/'+path.parent.name+'/workflows.json).','']
else:lines+=['No failed evaluation preparation occurred.','']
(out/'REPRESENTATIVE_TRACES.md').write_text('\n'.join(lines)+'\n')
(out/'selection.json').write_text(json.dumps(dict(policy_examples=selections,failed_preparation=dict(bundle=failed[0].parent.name,case_id=failed[1]['case_id']) if failed else None),indent=2)+'\n')
print(json.dumps(selections,indent=2))
