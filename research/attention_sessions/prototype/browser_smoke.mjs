// Exercise the actual browser UI. All resulting interactions are scripted demos.
import fs from 'node:fs';import {spawn} from 'node:child_process';
const out='artifacts/attention_sessions';fs.mkdirSync(out+'/figures',{recursive:true});
const chrome=process.env.CHROME||'/opt/google/chrome/google-chrome';
const port=9224,profile='/tmp/attention-browser-smoke-'+process.pid;
const child=spawn(chrome,['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--no-first-run','--user-data-dir='+profile,'--remote-debugging-port='+port,'about:blank'],{stdio:'ignore'});
let ws;const wait=ms=>new Promise(r=>setTimeout(r,ms));
try{
 let pages;for(let i=0;i<40;i++){try{pages=await(await fetch('http://127.0.0.1:'+port+'/json/list')).json();if(pages.length)break}catch{}await wait(100)}
 if(!pages?.length)throw Error('Browser did not start');ws=new WebSocket(pages.find(x=>x.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
 let serial=0,pending=new Map(),errors=[];ws.onmessage=e=>{let m=JSON.parse(e.data);if(m.id){let p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result)}if(m.method==='Runtime.exceptionThrown')errors.push(m.params)};
 function send(method,params={}){return new Promise((resolve,reject)=>{let id=++serial;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))})}
 async function js(expression){let r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value}
 await send('Runtime.enable');await send('Page.enable');await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:'http://127.0.0.1:9017/'});await wait(500);await js("action({action:'reset'})");
 const assert=(v,m)=>{if(!v)throw Error(m)};
 assert(await js("document.querySelectorAll('.card').length===3"),'Initial public cards');
 assert(await js("!document.body.innerText.includes('source_label')"),'No evaluator label field');
 async function screenshot(name){await wait(100);let m=await send('Page.getLayoutMetrics');let c=m.cssContentSize;let r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:Math.ceil(c.width),height:Math.ceil(c.height),scale:1}});fs.writeFileSync(out+'/figures/'+name+'.png',Buffer.from(r.data,'base64'))}
 await screenshot('interface_initial');
 await js("document.getElementById('start').click()");await wait(100);
 assert(await js("document.getElementById('submit-decision')!==null"),'Active decision controls');
 await js("document.querySelector('details').open=true");await wait(100);await screenshot('interface_active');
 await js("document.getElementById('submit-decision').click()");await wait(100);
 assert(await js("state.used>0&&state.requests.some(r=>r.status==='reviewed')"),'Manual decision completes');
 await js("document.getElementById('end').click()");await wait(100);
 const deferred=await js("state.requests.find(r=>r.status==='pending'&&r.deadline>state.tick+2)?.request_id");
 if(deferred){await js(`action({action:'defer',request_id:${JSON.stringify(deferred)},until:state.tick+1})`);assert(await js(`state.requests.find(r=>r.request_id===${JSON.stringify(deferred)}).status==='deferred'`),'Deferral persists')}
 await screenshot('interface_deferred');
 await js("document.getElementById('policy').value='sticky_edf';document.getElementById('policy').dispatchEvent(new Event('change'))");await wait(100);
 assert(await js("state.policy==='sticky_edf'"),'Policy override');
 const reject=await js("fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'decision',request_id:'not-the-active-card',diagnosis:'normal'})}).then(r=>r.status)");assert(reject===400,'Wrong-scope action rejected');
 await js("action({action:'reset',policy:'guarded'})");let grouped=false;for(let k=0;k<12;k++){if(await js('state.recommendation.length>1')){await js("document.getElementById('start').click()");await wait(100);await screenshot('interface_grouped');grouped=true;break}await js("action({action:'replay'})")}
 assert(grouped,'Actual multi-card session demonstrated');
 const final=await js("({tick:state.tick,used:state.used,policy:state.policy,visible:state.requests.length})");
 assert(errors.length===0,'No browser exceptions');
 fs.writeFileSync(out+'/browser_verification.json',JSON.stringify({status:'passed',type:'scripted development demonstration, not participant data',checks:['public cards','individual decision','source expansion','deferral','policy override','wrong-scope rejection','no browser exceptions','multi-card session'],final,errors,screenshots:['interface_initial','interface_active','interface_deferred','interface_grouped']},null,2)+'\n');
 console.log('Browser interaction and screenshots verified');await send('Browser.close');
}finally{if(ws)ws.close();child.kill();}
