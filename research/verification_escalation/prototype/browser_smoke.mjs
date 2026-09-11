// Real browser interactions, explicitly scripted rather than participant evidence.
import fs from 'node:fs';import {spawn} from 'node:child_process';
const out=process.argv[2]||'/tmp/verification-browser-demo';fs.mkdirSync(out,{recursive:true});
let occupied=false;try{await fetch('http://127.0.0.1:9232/json/version');occupied=true}catch{}
if(occupied)throw Error('Debug port 9232 is in use; refusing to attach to an unrelated browser');
const child=spawn('/opt/google/chrome/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--no-first-run','--user-data-dir=/tmp/verification-browser-'+process.pid,'--remote-debugging-port=9232','about:blank'],{stdio:'ignore'});
const wait=ms=>new Promise(r=>setTimeout(r,ms));let ws;
try{
 let pages;for(let i=0;i<50;i++){try{pages=await(await fetch('http://127.0.0.1:9232/json/list')).json();if(pages.length)break}catch{}await wait(100)}
 if(!pages?.length)throw Error('Browser unavailable');ws=new WebSocket(pages.find(x=>x.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
 let next=0,pending=new Map(),errors=[];ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result)}if(m.method==='Runtime.exceptionThrown')errors.push(m.params)};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++next;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
 async function js(expression){const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value}
 let checks=0;const assert=(x,m)=>{checks++;if(!x)throw Error(m)};
 async function screenshot(name){await wait(120);const r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(out+'/'+name+'.png',Buffer.from(r.data,'base64'))}
 await send('Runtime.enable');await send('Page.enable');await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:'http://127.0.0.1:9032/'});await wait(350);
 await js("action({action:'reset',method:'verification',budget:3})");
 assert(await js("state.work.filter(w=>w.status==='released').length===2"),'Two distinct results proceed without a user answer');await screenshot('ready_and_unresolved');
 await js("action({action:'inspect'})");assert(await js("state.question.task==='export'"),'Consequential export question shown');
 assert(await js("state.question.remaining_work.length===2"),'Unaffected work visible');await screenshot('consequence_question');
 await js("answer('spending')");assert(await js("state.work.find(w=>w.id==='export').status==='released'"),'Export follows received answer');assert(await js("state.work.find(w=>w.id==='partner').status==='unfinished'"),'Partner exception preserved');await screenshot('shared_answer_exception');
 await js("action({action:'snapshot'})");assert(await js("state.work.every(w=>w.status==='needs_revalidation')"),'Snapshot invalidates all dependent artifacts');await screenshot('revalidation');
 await js("action({action:'inspect'})");assert(await js("state.question && state.question.task==='count'"),'Changed data makes the count consequential');
 await js("action({action:'reset',method:'verification',budget:3})");await js("action({action:'inspect'})");await js("document.querySelector('#narrow').checked=true");await js("answer('orders')");assert(await js("state.answers_remaining===1"),'Value plus narrow scope costs two decisions');await screenshot('narrow_scope');
 await js("action({action:'reset',method:'recovery_completion',budget:1})");await js("action({action:'inspect'})");await js("action({action:'defer'})");assert(await js("state.answers_remaining===0 && state.work.some(w=>w.status==='unfinished')"),'Unresolved answer counted');
 await js("action({action:'reset',method:'verification',budget:3})");await js("action({action:'inspect'})");
 await send('Emulation.setDeviceMetricsOverride',{width:430,height:1000,deviceScaleFactor:1,mobile:true});await js('window.scrollTo(0,0)');await screenshot('mobile');
 assert(await js('document.documentElement.scrollWidth<=window.innerWidth+2'),'No mobile horizontal overflow');assert(errors.length===0,'No browser exceptions');
 fs.writeFileSync(out+'/verification.json',JSON.stringify({status:'passed',type:'Scripted software demonstration, not participant observations',checks,errors},null,2)+'\n');
 fs.writeFileSync(out+'/interactions.jsonl',await(await fetch('http://127.0.0.1:9032/api/log')).text());
 console.log(checks+' browser checks, six screenshots and actual interaction log saved');await send('Browser.close');
}finally{if(ws)ws.close();child.kill()}
