// Real browser interactions, explicitly scripted rather than participant evidence.
import fs from 'node:fs';import {spawn} from 'node:child_process';
const out=process.argv[2]||'/tmp/clarification-browser-demo';fs.mkdirSync(out,{recursive:true});
let occupied=false;try{await fetch('http://127.0.0.1:9231/json/version');occupied=true}catch{}
if(occupied)throw Error('Debug port 9231 is in use; refusing to attach to an unrelated browser');
const child=spawn('/opt/google/chrome/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--no-first-run','--user-data-dir=/tmp/clarification-browser-'+process.pid,'--remote-debugging-port=9231','about:blank'],{stdio:'ignore'});
const wait=ms=>new Promise(r=>setTimeout(r,ms));let ws;
try{
 let pages;for(let i=0;i<50;i++){try{pages=await(await fetch('http://127.0.0.1:9231/json/list')).json();if(pages.length)break}catch{}await wait(100)}
 if(!pages?.length)throw Error('Browser unavailable');ws=new WebSocket(pages.find(x=>x.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
 let next=0,pending=new Map(),errors=[];ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result)}if(m.method==='Runtime.exceptionThrown')errors.push(m.params)};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++next;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
 async function js(expression){const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value}
 let checks=0;const assert=(x,m)=>{checks++;if(!x)throw Error(m)};
 async function screenshot(name){await wait(120);const r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(out+'/'+name+'.png',Buffer.from(r.data,'base64'))}
 await send('Runtime.enable');await send('Page.enable');await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:'http://127.0.0.1:9031/'});await wait(350);
 await js("action({action:'reset',method:'depth2',budget:2})");await js("action({action:'next'})");
 assert(await js("state.question.id==='accessibility'"),'First complementary question selected');
 assert(await js("document.querySelector('#question').innerText.includes('second answer')"),'Second answer dependency displayed');
 assert(await js("!document.body.innerText.includes('evaluation_only')"),'No evaluator file in UI');await screenshot('planned_question');
 await js("(()=>{const f=document.querySelector('#answer-form');f.elements.value.value='screen_reader';f.requestSubmit()})()");await wait(150);await js("action({action:'next'})");
 assert(await js("state.question.id==='format'"),'Actual response followed by replanning');
 await js("(()=>{const f=document.querySelector('#answer-form');f.elements.value.value='web';f.requestSubmit()})()");await wait(150);await js("action({action:'finish'})");
 assert(await js("state.work.filter(w=>w.status.startsWith('Ready')).length===3"),'Three distinct deliverables available');
 assert(await js("state.work.find(w=>w.id==='Partner export').status==='Deferred'"),'No automatic propagation to exceptional work');await screenshot('complementary_work_ready');
 await js("action({action:'revise',id:'format',value:'pdf'})");
 assert(await js("state.work.filter(w=>w.registered_release==='needs_revalidation').length===3"),'Changed decision identifies three stale releases');await screenshot('revision_impact');
 await js("action({action:'reset',method:'depth2',budget:2})");await js("action({action:'next'})");
 await js("(()=>{const f=document.querySelector('#answer-form');f.elements.value.value='large_print';f.elements.only_task.value='Website implementation';f.requestSubmit()})()");await wait(150);
 assert(await js("state.records.find(r=>r.id==='Website implementation::accessibility').allowed_tasks.length===1"),'Request-specific scope');
 assert(await js("state.remaining_budget===0"),'Value and changed scope count as two decisions');await screenshot('narrow_answer');
 await js("action({action:'reset',method:'depth2',budget:1})");
 await js("action({action:'next'})");await js("action({action:'defer'})");
 assert(await js("state.remaining_budget===0 && state.work.some(w=>w.status==='Deferred')"),'Unresolved response costs an answer and leaves visible work');
 await js("action({action:'reset',method:'depth1',budget:2})");await js("action({action:'next'})");
 assert(await js("state.question.id==='exception.format'"),'One-step comparison makes a different decision');
 await js("action({action:'answer',value:'spreadsheet'})");await js("action({action:'next'})");
 assert(await js("state.question.id==='meeting'"),'Second independent decision');await js("action({action:'answer',value:'morning'})");await js("action({action:'finish'})");assert(await js("state.work.filter(w=>w.status.startsWith('Ready')).length===2"),'Two independent tasks versus three complementary tasks');await screenshot('one_step_independent');
 await send('Emulation.setDeviceMetricsOverride',{width:430,height:1000,deviceScaleFactor:1,mobile:true});await js('window.scrollTo(0,0)');await screenshot('mobile');
 assert(await js('document.documentElement.scrollWidth<=window.innerWidth+2'),'No mobile horizontal overflow');assert(errors.length===0,'No browser exceptions');
 fs.writeFileSync(out+'/verification.json',JSON.stringify({status:'passed',type:'Scripted software demonstration, not participant observations',checks,errors},null,2)+'\n');
 fs.writeFileSync(out+'/interactions.jsonl',await(await fetch('http://127.0.0.1:9031/api/log')).text());
 console.log(checks+' browser checks, six screenshots and actual interaction log saved');await send('Browser.close');
}finally{if(ws)ws.close();child.kill()}
