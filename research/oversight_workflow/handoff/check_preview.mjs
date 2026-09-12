// Read-only launch check. Does not create practice or participant records.
import fs from 'node:fs';
import {spawn} from 'node:child_process';
const out=process.argv[2]||'/tmp/oversight-handoff-preview';fs.mkdirSync(out,{recursive:true});
const base='http://127.0.0.1:9042',port=9342;
const child=spawn('/opt/google/chrome/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--no-first-run',`--user-data-dir=/tmp/oversight-handoff-browser-${process.pid}`,`--remote-debugging-port=${port}`,'about:blank'],{stdio:'ignore'});
const wait=ms=>new Promise(r=>setTimeout(r,ms));let ws;let id=0;const pending=new Map();
try {
 let pages;for(let i=0;i<50;i++){try{pages=await(await fetch(`http://127.0.0.1:${port}/json/list`)).json();if(pages.length)break;}catch{}await wait(100);}
 ws=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j;});
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});
 const js=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
 await send('Page.enable');await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1050,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:base});
 let ready=false;for(let i=0;i<50;i++){ready=await js("document.querySelector('#assignment')?.options.length===18");if(ready)break;await wait(100);}
 const status=await(await fetch(base+'/pilot/status')).json();
 const result={record_kind:'read_only_software_check',created_run:false,checks:{assignment_choices_ready:ready,investigator_practice:status.kind==='investigator_practice',no_run_created:status.run===null,practice_label:await js("document.body.innerText.includes('INVESTIGATOR PRACTICE')"),setup_visible:await js("!document.querySelector('#setup').hidden")}};
 fs.writeFileSync(out+'/preview_check.json',JSON.stringify(result,null,2)+'\n');
 const capture=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(out+'/preview_setup.png',Buffer.from(capture.data,'base64'));
 if(Object.values(result.checks).some(v=>!v))throw Error('Preview check failed');
 console.log(JSON.stringify(result));
} finally {if(ws)ws.close();child.kill('SIGTERM');}
