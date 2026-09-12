// Actual Chromium software tests; no participant observations.
import fs from 'node:fs';import {spawn} from 'node:child_process';
const out=process.argv[2]||'artifacts/oversight_workflow/walkthrough';fs.mkdirSync(out,{recursive:true});const port=9241;
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

 await js("busy=true;render(await post('/api/start',{condition:'sessions',bundle:0,mode:'replay',interval:.15,revision:true,revision_at:6}));busy=false");await until('!!state.next_request');await js('await select(state.next_request)');
 await js("window.walkId=state.active.request_id;window.before=JSON.stringify(state.active.output);document.querySelector('#note').value='Check source units and the question period before release.';document.querySelector('#save-note').click()");
 await until("Object.values(state.requests).filter(r=>state.tasks[r.id].source.id===state.tasks[state.active.request_id].source.id).length>=3");
 await js("document.querySelector('#make-group').click()");await until('state.session.length===3');
 await send('Emulation.setDeviceMetricsOverride',{width:1350,height:1600,deviceScaleFactor:1,mobile:false});await screenshot('financial_source_session');
 async function component(selector,name){const rect=await js(`(()=>{const r=document.querySelector('${selector}').getBoundingClientRect();return {x:r.x+scrollX,y:r.y+scrollY,width:r.width,height:r.height,scale:1}})()`);const r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:rect});fs.writeFileSync(out+'/'+name+'.png',Buffer.from(r.data,'base64'))}
 await component('#group','source_session_component');await component('#source-evidence','source_evidence_component');
 await until('state.requests[walkId].current_version===2');assert(await js('state.active.version===1 && JSON.stringify(state.active.output)===before'),'Actual saved model revision leaves pinned version unchanged');
 await screenshot('actual_model_revision');await component('#version-warning','version_warning_component');
 await js("document.querySelector('#approve').click()");await wait(180);assert(await js('!!state.active'),'Actual stale approval refused');
 await js("document.querySelector('#refresh').click()");await wait(150);await js("document.querySelector('#defer').click()");await wait(150);assert(await js("state.requests[walkId].status==='deferred'"),'New actual version can be deferred without losing history');
 // First source fourth question is an unedited model mistake; the controller receives no gold.
 const chosen=await js("Object.values(state.tasks).filter(t=>t.source.id===state.tasks[walkId].source.id)[3].id");await js(`await select('${chosen}')`);await wait(150);await screenshot('first_source_fourth_question');
 const exported=await(await fetch('http://127.0.0.1:9041/api/export')).json();fs.writeFileSync(out+'/events.json',JSON.stringify(exported,null,2)+'\n');
 fs.writeFileSync(out+'/verification.json',JSON.stringify({checks,selection:'First selected source, first question for active/revision; first three same-source questions for grouping; fourth for a fixed ordinary-case display. No source selected by model outcome.',kind:'Scripted replay of actual TAT-QA answers and an actual saved model recheck. No participant data or annotation disclosure.'},null,2));
 await send('Browser.close');console.log('Actual-source walkthrough captured');
}catch(e){fs.writeFileSync(out+'/failed_check.json',JSON.stringify({error:String(e),checks},null,2));throw e}finally{if(ws)ws.close();child.kill()}
