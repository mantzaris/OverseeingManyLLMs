// Scripted software checks; no participant observations.
import fs from 'node:fs';import {spawn} from 'node:child_process';
const out=process.argv[2]||'/tmp/adaptive-browser';fs.mkdirSync(out,{recursive:true});const port=9234;
try{await fetch(`http://127.0.0.1:${port}/json/version`);throw Error('Debug port occupied')}catch(e){if(e.message.includes('occupied'))throw e}
const child=spawn('/opt/google/chrome/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--no-first-run',`--user-data-dir=/tmp/adaptive-browser-${process.pid}`,`--remote-debugging-port=${port}`,'about:blank'],{stdio:'ignore'});let ws;const wait=ms=>new Promise(r=>setTimeout(r,ms));
try{
 let pages;for(let i=0;i<60;i++){try{pages=await(await fetch(`http://127.0.0.1:${port}/json/list`)).json();if(pages.length)break}catch{}await wait(100)}
 if(!pages?.length)throw Error('Browser unavailable');ws=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});let next=0,pending=new Map(),errors=[];ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result)}if(m.method==='Runtime.exceptionThrown')errors.push(m.params)};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++next;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
 async function js(expression){const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value}
 let checks=0;function assert(x,msg){checks++;if(!x)throw Error(msg)}
 async function screenshot(name){const r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(out+'/'+name+'.png',Buffer.from(r.data,'base64'))}
 await send('Page.enable');await send('Runtime.enable');await send('Emulation.setDeviceMetricsOverride',{width:1450,height:1250,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:'http://127.0.0.1:9034/'});await wait(700);
 if(process.argv[3]){await js(`$('case').value=${JSON.stringify(process.argv[3])};$('load').click()`);await wait(300)}
 assert(await js('!!state && state.step===0'),'Initial state');assert(await js('state.last===null'),'Future disclosure withheld');assert(await js('document.querySelectorAll(".card").length===6'),'Six distinct questions');await screenshot('before');
 await js('$("inspect").click()');await wait(300);assert(await js('state.remaining===1 && !!state.last.disclosure'),'Exactly one inspection disclosed');assert(await js('state.last.disclosure.id===state.last.inspected'),'Question-scoped feedback');await screenshot('after_one');
 await js('$("inspect").click()');await wait(300);assert(await js('state.remaining===0 && !$("inspect")'),'Budget exhausted');await screenshot('after_two');
 assert(await js('fetch("/api/inspect",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({session:state.session})}).then(r=>r.status)')===400,'Excess inspection refused');
 await send('Emulation.setDeviceMetricsOverride',{width:430,height:1000,deviceScaleFactor:1,mobile:true});await screenshot('mobile');assert(await js('document.documentElement.scrollWidth<=window.innerWidth+2'),'Mobile overflow absent');assert(errors.length===0,'No runtime exceptions');
 fs.writeFileSync(out+'/verification.json',JSON.stringify({passed:true,checks,errors,kind:'Scripted interface checks, not participant data'},null,2)+'\n');console.log(checks+' checks passed');await send('Browser.close');
}finally{if(ws)ws.close();child.kill()}
