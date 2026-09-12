"""Frozen fresh collection plus one actual asynchronous integration demonstration."""
import time
from .common import ART,read,write,digest
from .protocol import Desk,replay
from .driver import LiveDriver
from .inference import answer

def main():
    if (ART/'live/events.json').exists() or (ART/'collection_complete.json').exists():
        raise SystemExit('This stage already has live evidence. Use saved-output replay; fresh collection requires a new declared namespace.')
    manifest=read(ART/'frozen/manifest.json');contexts=manifest['contexts']
    live=Desk('sessions');driver=LiveDriver(live,contexts[:2]).start()
    held=False;paused=False;resumed=False;deferred=False;opened=None;selected=None
    while not driver.done():
        now=time.monotonic()-live.started
        if not held and live.next_request():
            selected=live.next_request();live.command('demo-select','select',{'id':selected});held=True;opened=now
        if held and not paused:
            live.command('demo-pause','pause');paused=True
        if held and not resumed and now-opened>=2:
            live.command('demo-resume','resume');resumed=True
        if held and not deferred and now-opened>=6:
            live.command('demo-defer','decide',dict(id=selected,version=1,decision='defer',note='Scripted demonstration: retain this review while other workers finish.'))
            deferred=True
        time.sleep(.02)
    driver.stop()
    if live.state['active']:
        live.command('demo-defer-final','decide',dict(id=selected,version=1,decision='defer',note='Live demonstration retained; no approval asserted.'))
    if live.state['paused']:live.command('demo-resume-final','resume')
    # Actual fresh model continuation, chosen by source order before collection.
    c=contexts[0];q=c['questions'][0];rid=f"r0/{q['id']}"
    if live.state['requests'][rid]['status']=='queued':live.command('demo-select-revision','select',{'id':rid})
    else:live.command('demo-resume-review','select',{'id':rid})
    old=live.state['active']['output'];revision=answer(c,q,0,'revision',old)
    live.command('demo-revise','revise',dict(id=rid,output=revision['output'],origin='live_model_revision'))
    live.command('demo-stale-approve','decide',dict(id=rid,version=1,decision='approve',by='scripted_protocol_probe'))
    live.command('demo-refresh','refresh')
    live.command('demo-retain','decide',dict(id=rid,version=2,decision='defer',note='New version requires a user decision; no annotation was disclosed.'))
    assert replay(live.events,'sessions').logical()==live.logical()
    write(ART/'live/events.json',live.events);write(ART/'live/final.json',live.view())
    write(ART/'live/summary.json',dict(kind='Actual GPU generations and wall-clock delivery; all reviewer actions scripted, no participants or annotation disclosures.',
        requests=len(driver.rows),worker_errors=driver.errors,counts=live.counts(),replay=True,
        stable_review_seconds=6,revision_call=revision['call_id'],actual_source_contexts=2))
    for replica in range(2):
        subset=contexts[2:] if replica==0 else contexts
        desk=Desk();d=LiveDriver(desk,subset,replica).start()
        while not d.done():time.sleep(.1)
        d.stop();write(ART/'collection'/f'events_r{replica}.json',desk.events)
        write(ART/'collection'/f'summary_r{replica}.json',dict(rows=len(d.rows),errors=d.errors,counts=desk.counts()))
        print('Collected replica',replica,len(d.rows),flush=True)
    # Three more predetermined source-order revision requests; no correctness-based selection.
    for c in contexts[1:4]:
        q=c['questions'][0];old=read(ART/'prepared'/f"primary_r0_{q['id']}.json")['output'];answer(c,q,0,'revision',old)
    print('Collection complete',flush=True)

if __name__=='__main__':main()
