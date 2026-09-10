#!/usr/bin/env python3
"""First qualifying primary examples, chosen by numeric order, not effect size."""
import csv,gzip,json
from pathlib import Path
root=Path('artifacts/stage6_robustness')
for cohort in ('fresh','post_hoc_stage5'):
    folder=root/'analysis'/cohort
    if not (folder/'summary.json').exists():continue
    rows=list(csv.DictReader((folder/'episodes.csv').open()))
    source=root if cohort=='fresh' else Path('artifacts/stage5_practical')
    cases={c['case_id']:c for c in json.loads((source/'cases.json').read_text())['cases']}
    pairs={}
    for row in rows:
        if row['variant']=='approve_block' and row['review_duration']=='2' and row['policy'] in ('search','greedy'):
            pairs.setdefault((row['bundle_id'],int(row['replicate'])),{})[row['policy']]=row
    selected={}
    for key,group in sorted(pairs.items()):
        delta=float(group['search']['operational_loss'])-float(group['greedy']['operational_loss'])
        label='benefit' if delta<0 else 'unfavorable' if delta>0 else 'tie'
        if label not in selected:selected[label]=dict(bundle_id=key[0],replicate=key[1],search_minus_greedy=delta)
    texts=['# Representative restricted-authority traces','',
        'First numeric bundle then replicate for each category at base duration two. These are saved model outputs with simulated review, not mechanics fixtures.','']
    for label in ('benefit','tie','unfavorable'):
        if label not in selected:texts+=['## '+label,'','No qualifying example in this cohort.',''];continue
        entry=selected[label];key=entry['bundle_id']+'_r'+str(entry['replicate'])
        texts+=['## '+label+': '+key,'']
        preps=json.loads((source/'batches/evaluation/prepared'/key/'workflows.json').read_text())
        for p in preps:
            c=cases[p['case_id']]
            texts+=['Case '+p['case_id']+' ('+c['family']+'). Initial error: '+str(p['initial_error'])+'. Staged: '+str(p['proposal'] is not None)+'.',
                '', 'Customer intent: '+c['customer_message'],'', 'Proposed transaction:', '```json',json.dumps(p['proposal'],indent=2), '```',
                'Annotated transaction (scoring/completed review only):','```json',json.dumps(c['target_action'],indent=2),'```','']
        for policy in ('search','greedy'):
            trace=json.loads(gzip.decompress((folder/'traces'/key/('approve_block_s2_'+policy+'.json.gz')).read_bytes()))
            texts+=['### '+policy,'','Loss '+str(trace['operational_loss'])+'; correct tasks '+str(trace['task_completed'])+'; blocked unresolved '+str(trace['blocked_unresolved'])+'.','',
                '| Tick | Event | Case | Consequence |','|---:|---|---|---|']
            for e in trace['events']:
                if e['event'] not in ('review_request_arrived','review_started','review_completed','transaction_committed','transaction_blocked','processing_cutoff'):continue
                c=e.get('case_id') or e.get('request',{}).get('request_id','')
                note=''
                if e['event']=='review_started':note='Completion at '+str(e['completion'])
                if e['event']=='transaction_blocked':note='No mutation; service unresolved'
                if e['event']=='transaction_committed':note='Correct' if e['task_completed'] else 'Wrong transaction posts'
                if e['event']=='review_request_arrived':note='Cutoff '+str(e['request']['cutoff'])
                texts+=['| '+str(e['tick'])+' | '+e['event']+' | '+c+' | '+note+' |']
            texts+=['']
    failure=None
    for path in sorted((source/'batches/evaluation/prepared').glob('*/workflows.json')):
        for row in json.loads(path.read_text()):
            if row['proposal'] is None:failure=row;break
        if failure:break
    if failure:
        selected['preparation_failure']={k:failure[k] for k in ('bundle_id','replicate','case_id','failure')}
        texts+=['## First preparation failure','',failure['case_id']+' in '+failure['bundle_id']+'_r'+str(failure['replicate']),
            '',str(failure['failure'])+'; no staged transaction, no reviewer request.','',
            '| Step | Tool | Result |','|---:|---|---|']
        for i,event in enumerate(failure['events']):
            response=str(event.get('response',event.get('result',''))).replace('|','/').replace('\n',' ')[:180]
            texts+=['| '+str(i)+' | '+event['call']['tool']+' | '+response+' |']
    dest=folder/'examples';dest.mkdir(exist_ok=True)
    (dest/'selection.json').write_text(json.dumps(selected,indent=2)+'\n')
    (dest/'TRACES.md').write_text('\n'.join(texts).rstrip()+'\n')
