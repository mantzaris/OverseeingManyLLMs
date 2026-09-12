// Actual Chromium software tests; no participant observations.
import fs from 'node:fs';import {spawn} from 'node:child_process';
const out=process.argv[2]||'artifacts/oversight_workflow/browser';fs.mkdirSync(out,{recursive:true});const port=9241;
const child=spawn('/opt/google/chrome/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--no-first-run',`--user-data-dir=/tmp/oversight-browser-${process.pid}`,`--remote-debugging-port=${port}`,'about:blank'],{stdio:'ignore'});
let ws;const wait=ms=>new Promise(r=>setTimeout(r,ms));let checks=[];
try{
 let pages;for(let i=0;i<60;i++){try{pages=await(await fetch(`http://127.0.0.1:${port}/json/list`)).json();if(pages.length)break}catch{}await wait(100)}
 if(!pages?.length)throw Error('Browser unavailable');ws=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});let next=0,pending=new Map(),errors=[];ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result)}if(m.method==='Runtime.exceptionThrown')errors.push(m.params)};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++next;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
 async function js(expression){const r=await send('Runtime.evaluate',{expression:expression.includes('await ')?'(async()=>{'+expression+'})()':expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value}
 async function until(expression){for(let i=0;i<50;i++){if(await js(expression))return;await wait(100)}throw Error('Timed out: '+expression)}
 function assert(x,label){checks.push({label,passed:!!x});if(!x)throw Error(label)}
 async function screenshot(name){const r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(out+'/'+name+'.png',Buffer.from(r.data,'base64'))}
 await send('Page.enable');await send('Runtime.enable');await send('Emulation.setDeviceMetricsOverride',{width:1600,height:1300,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:'http://127.0.0.1:9041/'});await wait(500);
 assert(await js('!!state'),'Loaded real application');
 for(const condition of ['threads','queue','sessions']){
  await js(`busy=true;render(await post('/api/start',{condition:'${condition}',bundle:0,mode:'replay',interval:.3,revision:false}));busy=false`);await until('!!state.next_request');
  await js('await select(state.next_request)');await until("!!document.querySelector('#note')");
  await js("window.savedNode=document.querySelector('#note');window.savedSource=document.querySelector('#source-evidence');window.pinned=JSON.stringify(state.active);savedNode.value='Check the units when I return';savedNode.focus()");
  const before=await js('state.counts.received');await wait(650);
  assert(await js('state.counts.received')>before,condition+': asynchronous arrivals observed');
  assert(await js("document.querySelector('#note')===savedNode && document.querySelector('#source-evidence')===savedSource"),condition+': active DOM preserved');
  assert(await js("savedNode.value==='Check the units when I return' && document.activeElement===savedNode"),condition+': typed draft and focus preserved');
  assert(await js('JSON.stringify(state.active)===pinned'),condition+': active logical snapshot preserved');await js('render({...state,sequence:state.sequence-1,active:null})');assert(await js('JSON.stringify(state.active)===pinned'),condition+': stale HTTP state refused');
  if(condition==='sessions'){
   await until("Object.values(state.requests).filter(r=>state.tasks[r.id].source.id===state.tasks[state.active.request_id].source.id).length>=2");await js("document.querySelector('#make-group').click()");await until('state.session.length>=2');
   assert(await js('state.session.length>=2'),'Optional source session has distinct questions');
   assert(await js("document.querySelectorAll('.groupcard').length>=2"),'Separate answer cards in source session');
   await send('Emulation.setDeviceMetricsOverride',{width:1600,height:1750,deviceScaleFactor:1,mobile:false});await screenshot('source_session');await send('Emulation.setDeviceMetricsOverride',{width:1600,height:1300,deviceScaleFactor:1,mobile:false});
   await js("document.querySelector('#pause').click()");await wait(150);assert(await js('state.paused'),'Admission pause visible');
   const unstarted=await js('state.counts.unstarted');await wait(400);assert(await js('state.counts.unstarted')===unstarted,'Pause does not start waiting tasks');
   assert(await js('state.counts.offered')>await js('state.counts.started'),'Offered unstarted work remains accounted');
   await screenshot('paused_backlog');await js("document.querySelector('#pause').click()");await wait(100);
  }else await screenshot(condition);
  await js("window.oldId=state.active.request_id;document.querySelector('#defer').click()");await wait(180);
  assert(await js("state.requests[oldId].status==='deferred'"),condition+': deferral remains visible');
  await js('await select(oldId)');await wait(120);assert(await js("document.querySelector('#note').value==='Check the units when I return'"),condition+': resumption restores note');
  // Authored metadata revision, separate from the four actual model rechecks.
  await js("window.oldVersion=state.active.version;await action('revise',{id:state.active.request_id,output:{...state.active.output,derivation:state.active.output.derivation+' [Scripted metadata revision for protocol test]'},origin:'authored_browser_stress'})");
  await wait(150);assert(await js('state.active.version===oldVersion'),'Revision preserves pinned old version');
  assert(await js("document.querySelector('#version-warning').style.display==='block'"),'New-version warning displayed');
  await js("window.warningNode=document.querySelector('#refresh');warningNode.focus()");await wait(350);assert(await js("document.querySelector('#refresh')===warningNode && document.activeElement===warningNode"),condition+': version warning control stays stable during polling');
  if(condition==='sessions'){await send('Emulation.setDeviceMetricsOverride',{width:1600,height:1550,deviceScaleFactor:1,mobile:false});await screenshot('revision_requires_review');await send('Emulation.setDeviceMetricsOverride',{width:1600,height:1300,deviceScaleFactor:1,mobile:false});}
  await js("document.querySelector('#approve').click()");await wait(150);assert(await js('!!state.active'),'Stale approval refused');
  await js("document.querySelector('#refresh').click()");await wait(100);
  await js("document.querySelector('#approve').click()");await wait(150);assert(await js('state.active===null'),'Current approval resolves review');
  assert(await js('state.counts.released===0'),'Approval alone does not release');
  await js("document.querySelector('[data-release]').click()");await wait(120);assert(await js('state.counts.released===1'),'Explicit version release works');
  const exported=await(await fetch('http://127.0.0.1:9041/api/export')).json();fs.writeFileSync(out+'/'+condition+'_events.json',JSON.stringify(exported,null,2)+'\n');
 }
 // Recovery and timing checks use a new saved-output session, not new inference.
 await js("busy=true;render(await post('/api/start',{condition:'sessions',bundle:0,mode:'replay',interval:.1,revision:false}));busy=false");await until('!!state.next_request');await js('await select(state.next_request)');
 await js("window.recoveryId=state.active.request_id;window.recoveryNode=document.querySelector('#note');recoveryNode.value='Resume this financial question';window.beforeOffline=state.counts.received");
 await send('Network.enable');await send('Network.emulateNetworkConditions',{offline:true,latency:0,downloadThroughput:0,uploadThroughput:0});await wait(500);
 assert(await js("document.querySelector('#note')===recoveryNode"),'Offline connection preserves active DOM');
 await js("document.querySelector('#approve').click()");await wait(200);assert(await js('!!state.active'),'Offline failed action does not invent approval');
 await send('Network.emulateNetworkConditions',{offline:false,latency:0,downloadThroughput:-1,uploadThroughput:-1});await until("document.querySelector('#connection').textContent==='Connected'");
 assert(await js('state.counts.received>=beforeOffline'),'Reconnect retains background arrivals');
 await js("window.sameCommand={session_id:state.session_id,event_id:crypto.randomUUID(),action:'note',payload:{text:'Resume this financial question'}};await post('/api/command',sameCommand);await post('/api/command',sameCommand)");
 assert(await js("fetch('/api/export').then(r=>r.json()).then(d=>d.events.filter(e=>e.event_id===sameCommand.event_id).length===1)"),'HTTP retry idempotent');
 await js("await action('decide',{id:state.active.request_id,version:state.active.version,decision:'defer',note:'Resume this financial question',until:state.elapsed+30});window.oldJournal=state.session_id+'.jsonl';busy=true;render(await post('/api/restore',{name:oldJournal}));busy=false");
 assert(await js('state.counts.offered===12'),'Restore retains complete offered workload');
 await js('await select(recoveryId)');assert(await js("document.querySelector('#note').value==='Resume this financial question'"),'Restored session preserves deferred note');
 const recovery=await(await fetch('http://127.0.0.1:9041/api/export')).json();fs.writeFileSync(out+'/recovery_events.json',JSON.stringify(recovery,null,2)+'\n');
 await js("busy=true;render(await post('/api/start',{condition:'sessions',study_packet:0,mode:'replay',load:'higher',study_seconds:1,revision:false}));busy=false");await until('!!state.session_closed');
 assert(await js('state.counts.offered===36'),'Prospective packet contains six real sources and 36 original questions');
 assert(await js('state.counts.unstarted>0 && state.counts.remaining===36'),'Timed cutoff retains unstarted and unresolved work');
 assert(await js("getComputedStyle(document.querySelector('#start')).display==='none'"),'Timed preview hides setup controls');
 assert(await js("fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:state.session_id,event_id:crypto.randomUUID(),action:'select',payload:{id:state.next_request}})}).then(r=>r.status===409)"),'Timed cutoff refuses further decisions');
 await screenshot('timed_cutoff');const timed=await(await fetch('http://127.0.0.1:9041/api/export')).json();fs.writeFileSync(out+'/timed_events.json',JSON.stringify(timed,null,2)+'\n');
 await js("busy=true;render(await post('/api/start',{condition:'sessions',mode:'training',revision:false}));busy=false");await until('state.counts.received===2');
 assert(await js('state.counts.offered===2'),'Practice uses two old development questions');
 assert(await js("Object.values(state.tasks).every(t=>t.source.id==='e78f8b29-6085-43de-b32f-be1a68641be3')"),'Practice source is disjoint from scored packets');
 await js('await select(state.next_request)');await screenshot('training');
 const training=await(await fetch('http://127.0.0.1:9041/api/export')).json();fs.writeFileSync(out+'/training_events.json',JSON.stringify(training,null,2)+'\n');
 await send('Emulation.setDeviceMetricsOverride',{width:430,height:1100,deviceScaleFactor:1,mobile:true});await wait(120);await screenshot('mobile');assert(await js('document.documentElement.scrollWidth<=window.innerWidth+2'),'Mobile page fits viewport');
 assert(errors.length===0,'No browser runtime errors');
 const timings=await js('latency');fs.writeFileSync(out+'/verification.json',JSON.stringify({passed:true,checks,errors,http_roundtrip_ms:timings,kind:'Scripted Chromium interaction and rendering checks on actual TAT-QA answers; no participant data. Metadata revisions are authored stress fixtures.'},null,2)+'\n');console.log(checks.length+' checks passed');await send('Browser.close');
}catch(e){fs.writeFileSync(out+'/failed_check.json',JSON.stringify({error:String(e),checks},null,2));throw e}finally{if(ws)ws.close();child.kill()}
