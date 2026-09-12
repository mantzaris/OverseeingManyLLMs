"""Real-time scripted software scenarios, then private saved-output scoring."""
import time
from copy import deepcopy
from itertools import zip_longest
from research.adaptive_correction_transfer.scoring import score
from research.adaptive_correction_transfer.data import annotations
from .common import ART,read,write,digest
from .protocol import Desk,replay,CONDITIONS
from .driver import ReplayDriver,items_for


def ordered_items(contexts,replica):
    groups=[items_for([c],replica) for c in contexts]
    return [x for row in zip_longest(*groups) for x in row if x]

def run(contexts,replica,condition,load,bundle):
    config=read(ART/'frozen/manifest.json')['software_scenarios']
    items=ordered_items(contexts,replica);desk=Desk(condition);gold=annotations('test_gold')
    interval=config['start_interval_seconds'][load];cutoff=config['observation_seconds'];service=config['script_action_seconds']
    revision=None
    c=contexts[0];q=c['questions'][0];revfile=ART/'prepared'/f"revision_r0_{q['id']}.json"
    if replica==0 and revfile.exists():revision=dict(id=items[0]['task']['id'],at=.8,output=read(revfile)['output'])
    driver=ReplayDriver(desk,items,interval=interval,revision=revision).start()
    samples=[];last_sample=-1;first_deferred=False;paused=False;resumed=False;counter=0;errors=[];active_checks=0;stable_checks=0;pinned=None
    def command(action,p=None):
        nonlocal counter
        counter+=1;r=desk.command('reviewer:'+str(counter),action,p)
        if not r['ok']:errors.append(dict(action=action,error=r['error']))
        return r
    while time.monotonic()-desk.started<cutoff:
        now=time.monotonic()-desk.started
        if condition=='sessions' and not paused and now>=.25:command('pause');paused=True
        if condition=='sessions' and not resumed and now>=.65:command('resume');resumed=True
        state=desk.logical()
        if now-last_sample>=.02:samples.append(dict(at=now,**desk.counts()));last_sample=now
        a=state['active']
        if a:
            if pinned and (a['request_id'],a['version'],a['opened_at'])==pinned[0]:
                active_checks+=1;stable_checks+=int(digest(a['output'])==pinned[1])
            r=state['requests'][a['request_id']]
            if now-a['opened_at']>=service:
                rid=a['request_id'];qid=state['tasks'][rid]['question_id']
                if a['version']!=r['current_version']:
                    command('refresh');pinned=None;continue
                if not first_deferred and rid==items[0]['task']['id']:
                    command('decide',dict(id=rid,version=a['version'],decision='defer',until=now+.35,note='Scripted deferral: resume with this source and draft.'))
                    first_deferred=True
                else:
                    # This explicit scripted inspection is the only point where an
                    # annotation enters the public event stream. It is not a participant.
                    g=gold[qid];sc=score(a['output'],g)
                    if sc['joint']:
                        result=command('decide',dict(id=rid,version=a['version'],decision='approve',by='scripted_ideal_inspection'))
                    else:
                        answer=g['answer'] if isinstance(g['answer'],list) else [str(g['answer'])]
                        result=command('decide',dict(id=rid,version=a['version'],decision='correct',by='scripted_ideal_annotation_disclosure',
                            output=dict(answer=answer,scale=g['scale'],derivation='Scripted question-specific annotation disclosure; not a model or human response.',evidence=[])))
                    if result['ok']:command('release',dict(id=rid,version=result['result']['version']))
                pinned=None
        else:
            rid=desk.next_request()
            if rid:
                if condition=='sessions':
                    src=state['tasks'][rid]['source']['id']
                    group=[rid]+[r['id'] for r in state['requests'].values() if r['id']!=rid and r['status']=='queued' and state['tasks'][r['id']]['source']['id']==src][:2]
                    command('session',{'ids':group})
                command('select',{'id':rid});a=desk.logical()['active'];pinned=((a['request_id'],a['version'],a['opened_at']),digest(a['output']))
        time.sleep(.003)
    cutoff_state=desk.logical();cutoff_counts=desk.counts();driver.stop()
    # Worker stop does not remove pending or unstarted tasks.
    events=deepcopy(desk.events);rep=replay(events,condition)
    assert rep.logical()==desk.logical()
    released=[]
    for rid,r in cutoff_state['requests'].items():
        if any(x['request_id']==rid and x['version']==r['current_version'] for x in cutoff_state['releases']):
            released.append(score(r['versions'][str(r['current_version'])]['output'],gold[cutoff_state['tasks'][rid]['question_id']]))
    waits=[e['at']-next(x['at'] for x in events if x['action']=='receive' and x['payload']['id']==e['payload']['id']) for e in events if e['action']=='select' and e['response']['ok']]
    summary=dict(bundle=bundle,source_context_ids=[c['id'] for c in contexts],replica=replica,condition=condition,load=load,counts=cutoff_counts,
        correct_released=sum(x['joint'] for x in released),wrong_released=sum(1-x['joint'] for x in released),
        observations=len(samples),peak_queued=max([s['queued'] for s in samples] or [0]),
        mean_wait_seconds=sum(waits)/len(waits) if waits else None,wait_seconds=waits,
        active_stability_checks=active_checks,active_stability_passed=stable_checks,
        handler_ms=[e['handler_ms'] for e in events],delivery_lateness_ms=[x['delivery_lateness_ms'] for x in driver.timings],
        events=len(events),command_errors=errors,driver_errors=driver.errors,replay=True,
        final_sha256=digest(desk.logical()),kind='Measured wall-clock software behavior with constructed arrivals and ideal scripted reviewer actions')
    path=ART/'scenarios'/f'b{bundle:02d}_r{replica}_{condition}_{load}.json'
    write(path,dict(summary=summary,samples=samples,events=events,cutoff_state_sha256=digest(cutoff_state)))
    return summary

def main():
    contexts=read(ART/'frozen/manifest.json')['contexts'];summaries=[]
    for bundle in range(12):
        pair=contexts[bundle*2:bundle*2+2]
        for replica in range(2):
            for load in ('lower','higher'):
                # Rotate execution order to distribute host warmup/drift.
                k=(bundle+replica)%3;order=CONDITIONS[k:]+CONDITIONS[:k]
                for condition in order:summaries.append(run(pair,replica,condition,load,bundle))
        print('Completed bundle',bundle,flush=True)
    write(ART/'software_summary.json',summaries)

if __name__=='__main__':main()
