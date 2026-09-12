// One end-to-end SOFTWARE FIXTURE. No participant or questionnaire responses.
import fs from 'node:fs';import {spawn} from 'node:child_process';
const out=process.argv[2]||'artifacts/oversight_workflow/pilot_preparation/test_data';fs.mkdirSync(out,{recursive:true});const base='http://127.0.0.1:9042',port=9242;
const child=spawn('/opt/google/chrome/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--no-first-run',`--user-data-dir=/tmp/pilot-browser-${process.pid}`,`--remote-debugging-port=${port}`,'about:blank'],{stdio:'ignore'});
const wait=ms=>new Promise(r=>setTimeout(r,ms));let ws;const checks=[];let next=0,pending=new Map(),errors=[];
try{
 let pages;for(let i=0;i<60;i++){try{pages=await(await fetch(`http://127.0.0.1:${port}/json/list`)).json();if(pages.length)break}catch{}await wait(100)}
 ws=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result)}if(m.method==='Runtime.exceptionThrown')errors.push(m.params)};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++next;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
 async function js(expression){const r=await send('Runtime.evaluate',{expression:expression.includes('await ')?'(async()=>{'+expression+'})()':expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value}
 const frame=expr=>js(`document.querySelector('#desk').contentWindow.eval(${JSON.stringify(expr)})`);
 async function until(f,label){for(let i=0;i<80;i++){if(await f())return;await wait(80)}throw Error('Timeout: '+label)}
 function check(x,label){checks.push({label,passed:!!x});if(!x)throw Error(label)}
 async function screenshot(name){const r=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(out+'/'+name+'.png',Buffer.from(r.data,'base64'))}
 const api=async(path,p)=>{const r=await fetch(base+path,p?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)}:{});const d=await r.json();if(!r.ok)throw Error(d.error||JSON.stringify(d));return d};
 check((await api('/pilot/status')).kind==='software_fixture','Server explicitly marks software fixture records');
 await send('Page.enable');await send('Runtime.enable');await send('Network.enable');await send('Emulation.setDeviceMetricsOverride',{width:1600,height:1300,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:base});await until(()=>js("document.querySelector('#assignment').options.length===18"),'assignment setup');
 await js("document.querySelector('#code').value='software-dry-run';document.querySelector('#assignment').value='0';document.querySelector('#create').click()");await until(()=>js('!!data?.run'),'run creation');await screenshot('setup_training_instructions');
 for(const [step,condition] of ['training','B','C','S'].entries()){
  // Only fixture servers accept compressed time. Scored sessions keep frozen durations.
  await api('/pilot/begin',{seconds:condition==='S'?8:24});await until(()=>js("!document.querySelector('#task').hidden && document.querySelector('#desk').contentWindow.eval('typeof state !== typeof undefined && !!state && !!state.next_request')"),'task ready');
  check(await frame("!!document.querySelector('#session-timer')"),condition+': timer visible');
  check(await frame("document.querySelector('#start').hidden"),condition+': setup controls absent');
  await frame('select(state.next_request)');await until(()=>frame("!!document.querySelector('#note')"),'active question');
  check(await frame(condition==='S'?"!document.querySelector('#original-model-response')":"!!document.querySelector('#original-model-response pre')"),condition+': original response available only when a model proposal exists');
  await frame("window.noteNode=document.querySelector('#note');noteNode.value='Check the source units when returning';window.sourceNode=document.querySelector('#source-evidence');window.oldId=state.active.request_id;window.pinned=JSON.stringify(state.active);document.querySelector('#calc-expression').value='(114 - 108) / 108 * 100';document.querySelector('#calculate').click()");
  await until(()=>frame("document.querySelector('#calc-result').textContent.includes('5.56')"),'calculator');
  const before=await frame('state.counts.received');await wait(1100);
  check(await frame("noteNode===document.querySelector('#note') && sourceNode===document.querySelector('#source-evidence') && noteNode.value.includes('source units')"),condition+': arrivals preserve active DOM and typed notes');
  if(condition==='B')check(await frame('state.counts.received')>before,'Concurrent arrivals during active B review');
  if(condition==='C'){
   await until(()=>frame("Object.values(state.requests).filter(r=>state.tasks[r.id].source.id===state.active.source.id).length>1"),'related request');
   await frame("document.querySelector('#make-group').click()");await until(()=>frame('state.session.length>=2'),'source group');
   check(await frame("document.querySelectorAll('.groupcard').length>=2"),'C: distinct source-group cards');
   await frame("document.querySelector('#pause').click()");await until(()=>frame('state.paused'),'pause');check(await frame('state.counts.unstarted>0'),'Paused work stays in offered denominator');await screenshot('source_session_practice');
   await frame("document.querySelector('#pause').click()");await until(()=>frame('!state.paused'),'resume');
  }else if(condition!=='training')check(await frame("document.querySelector('#pause').style.display==='none'"),condition+': source-session admission control absent');
  if(condition==='S'){
   check(await frame("document.querySelector('#approve').hidden && document.querySelector('#correction').open"),'S: source-only authoring replaces model approval');
   const s=await api('/api/state');check(Object.values(s.requests).every(r=>r.versions['1'].output.answer.length===0),'S: no cached proposal leaked');await screenshot('source_only_practice');
  }
  await frame("document.querySelector('#correct-answer').value='0';document.querySelector('#correct-scale').value='thousand';document.querySelector('#defer').click()");await until(()=>frame('!state.active'),'defer');
  await frame('select(oldId)');await until(()=>frame("!!document.querySelector('#note')"),'resume deferred');
  check(await frame("document.querySelector('#note').value==='Check the source units when returning' && document.querySelector('#correct-answer').value==='0' && document.querySelector('#correct-scale').value==='thousand'"),condition+': deferral preserves note, uncommitted answer and scale');
  if(condition==='B'){
   await send('Network.emulateNetworkConditions',{offline:true,latency:0,downloadThroughput:0,uploadThroughput:0});await wait(900);
   check(await frame("document.querySelector('#note')===noteNode" )===false,'Resumed review has its own stable DOM'); // Prior active node was intentionally replaced at resumption.
   check(await frame("document.querySelector('#note').value==='Check the source units when returning'"),'Connection interruption retains resumed note');
   await send('Network.emulateNetworkConditions',{offline:false,latency:0,downloadThroughput:-1,uploadThroughput:-1});await until(()=>frame("document.querySelector('#connection').textContent==='Connected'"),'reconnect');await until(()=>js("!document.querySelector('#status').textContent.includes('interrupted')"),'shell reconnect');await screenshot('central_queue_practice');
  }
  // A scripted answer of zero is a test input, not an ideal reviewer or a participant.
  await frame("document.querySelector('#correct').click()");await until(()=>frame('!state.active'),'correct');check(await frame('state.counts.released===0'),condition+': approval does not release');
  await frame("document.querySelector('[data-release]').click()");await until(()=>frame('state.counts.released===1'),'release');
  if(condition==='S'){
   await until(()=>js("!document.querySelector('#questionnaire').hidden"),'automatic cutoff');
   const ended=await api('/api/state');const raw=await fetch(base+'/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:ended.session_id,event_id:'fixture-late-approval',action:'decide',payload:{id:Object.keys(ended.requests)[0],version:1,decision:'approve'}})});check(raw.status===409,'Action at/after cutoff refused');
  }else{await js("document.querySelector('#end').onclick=null");await api('/pilot/finish',{})}await until(()=>js("!document.querySelector('#questionnaire').hidden"),'questionnaire');
  check(await js("[...document.querySelectorAll('#items input')].every(x=>x.value==='')"),condition+': questionnaires never prepopulated');
  await js("document.querySelector('#comment').value='Software fixture: no experienced workload or control response is supplied.';document.querySelector('#submit-form').click()");await until(()=>js("document.querySelector('#questionnaire').hidden"),'form saved');
 }
 await until(()=>js("!document.querySelector('#done').hidden"),'run completion');await screenshot('completed_practice');
 const exported=await api('/pilot/export');check(exported.sessions.length===4,'Training and all three assigned blocks retained');check(exported.sessions.every(s=>s.questionnaire?.tlx.every(x=>x===null)),'No simulated questionnaire responses');check(exported.sessions.every(s=>Object.keys(s.state.tasks).length===(s.condition==='training'?2:s.condition==='S'?6:12)),'Entire offered workload remains in export');
 fs.writeFileSync(out+'/complete_fixture.pilot.json',JSON.stringify(exported,null,2)+'\n');await js("document.querySelector('#new-run').click()");await wait(900);check(await js("!document.querySelector('#setup').hidden && document.querySelector('#code').value===''"),'Next investigator assignment can be set up without editing files or restarting');check(errors.length===0,'No uncaught browser exceptions');
 fs.writeFileSync(out+'/browser_checks.json',JSON.stringify({record_kind:'software_fixture',checks,errors,not_human_evidence:true},null,2)+'\n');console.log(JSON.stringify({passed:checks.length,out}));
}catch(e){fs.writeFileSync(out+'/browser_failure.json',JSON.stringify({record_kind:'software_fixture',checks,error:String(e),errors},null,2));console.error(e);process.exitCode=1}
finally{if(ws)ws.close();child.kill('SIGTERM')}
