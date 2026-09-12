// One SOFTWARE FIXTURE through training + Q/G/M. No participants or invented ratings.
import fs from 'node:fs';import {spawn} from 'node:child_process';
const out=process.argv[2]||'artifacts/oversight_workflow/matched_preparation/test_data';fs.mkdirSync(out,{recursive:true});
const base='http://127.0.0.1:9043',port=9343;
const child=spawn('/opt/google/chrome/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--no-first-run',`--user-data-dir=/tmp/matched-browser-${process.pid}`,`--remote-debugging-port=${port}`,'about:blank'],{stdio:'ignore'});
const wait=ms=>new Promise(r=>setTimeout(r,ms));let ws;const checks=[];let id=0;const pending=new Map();let created=false;
try {
 let pages;for(let i=0;i<60;i++){try{pages=await(await fetch(`http://127.0.0.1:${port}/json/list`)).json();if(pages.length)break;}catch{}await wait(100);}
 ws=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j;});
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});
 const js=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
 const frame=expr=>js(`document.querySelector('#desk').contentWindow.eval(${JSON.stringify(expr)})`);
 async function until(f,label,tries=180){for(let i=0;i<tries;i++){if(await f())return;await wait(120);}throw Error('Timeout: '+label);}
 const api=async(path,p)=>{const r=await fetch(base+path,p===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)});const d=await r.json();if(!r.ok)throw Error(d.error||JSON.stringify(d));return d;};
 function check(ok,label){checks.push({label,passed:!!ok});if(!ok)throw Error(label);}
 async function shot(name){const r=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(out+'/'+name+'.png',Buffer.from(r.data,'base64'));}
 check((await api('/pilot/status')).kind==='software_fixture','Server explicitly marks software fixtures');
 await send('Page.enable');await send('Emulation.setDeviceMetricsOverride',{width:1550,height:1200,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:base});
 await until(()=>js("document.querySelector('#assignment')?.options.length===18"),'assignment setup');
 await js("document.querySelector('#code').value='matched-software-fixture';document.querySelector('#assignment').value='0';document.querySelector('#create').click()");
 await until(()=>js('!!data?.run'),'create run');created=true;
 for(const [step,condition] of ['training','Q','G','M'].entries()) {
  await api('/pilot/begin',{seconds:condition==='training'?8:18});
  await until(()=>js("document.querySelector('#desk')?.contentWindow?.document.querySelector('#next') && document.querySelector('#desk').contentWindow.eval('typeof state !== \"undefined\" && !!state?.pilot')"),'loaded task frame');
  await until(()=>frame('!!state.next_request'),'first request');
  check(await frame('document.querySelector("#pause").hidden && document.querySelector("#pause").disabled'),'Admission control absent: '+condition);
  check(await frame('state.counts.offered')===(condition==='training'?2:12),'Complete offered denominator: '+condition);
  check(await frame('state.study.duration_seconds')===(condition==='training'?8:18),'Matched declared compression: '+condition);
  await frame("document.querySelector('#next').click()");await until(()=>frame('!!state.active'),'active review');
  await frame("window.keepId=state.active.request_id;window.keepNode=document.querySelector('#note');keepNode.value='Check period and units before release';window.keepVersion=state.active.version;");
  if(condition!=='training') {
   const before=await frame('state.counts.received');
   await until(()=>frame('state.counts.received===12'),'second wave while active');
   check(await frame("document.querySelector('#note')===keepNode && keepNode.value==='Check period and units before release' && state.active.version===keepVersion"),'Arrivals preserve active controls: '+condition);
   check((await frame('state.counts.received'))>before,'New arrivals observed: '+condition);
  }
  if(condition==='G') {
   await frame("document.querySelector('#make-group').click()");await until(()=>frame('state.session.length===3'),'source group');
   check(await frame('document.querySelectorAll(".groupcard").length===3'),'G has three separate cards');
   check(await frame('new Set(state.session.map(id=>state.tasks[id].source.id)).size===1'),'G groups actual identical source IDs');
   await shot('G_source_group_software_fixture');
  } else if(condition!=='training') check(await frame('document.querySelector("#group").style.display==="none"'),'No grouping in '+condition);
  if(condition==='M') {
   check(await frame('Object.values(state.pilot.raw_proposals).every(x=>x===null)'),'M never receives raw proposals');
   check(await frame('Object.values(state.requests).every(r=>r.versions["1"].output.answer.length===0)'),'M initial answers absent');
   check(await frame('document.querySelector("#approve").hidden'),'M requires own answer');
   await shot('M_source_only_software_fixture');
  }
  await frame("document.querySelector('#correct-answer').value='0';document.querySelector('#correct-scale').value='thousand';document.querySelector('#defer').click()");await until(()=>frame('!state.active'),'defer');
  await frame('select(keepId)');await until(()=>frame('!!state.active'),'resume');
  check(await frame("document.querySelector('#correct-answer').value==='0' && document.querySelector('#correct-scale').value==='thousand' && document.querySelector('#note').value==='Check period and units before release'"),'Draft and notes resume: '+condition);
  await frame("document.querySelector('#correct').click()");await until(()=>frame('!state.active'),'record authored fixture answer');
  check(await frame('state.counts.released===0'),'Approval alone does not release: '+condition);
  await frame('document.querySelector("[data-release]").click()');await until(()=>frame('state.counts.released===1'),'release');
  check(await frame('state.releases[0].version===2'),'Release targets authored v2: '+condition);
  if(condition!=='training') {
   await frame("document.querySelector('#next').click()");await until(()=>frame('!!state.active'),'another request');
   await frame("document.querySelector('#reject').click()");await until(()=>frame('!state.active'),'reject');
   check(await frame('state.counts.released===1'),'Rejection adds no release: '+condition);
   check(await frame('document.querySelector("#metrics .metric:nth-child(4) strong").textContent==="11"'),'Unfinished deliverables retained: '+condition);
   if(condition==='Q')await shot('Q_central_queue_software_fixture');
  }
  await until(()=>js('!data.current'),'automatic common cutoff');
  const status=await api('/pilot/status');const last=status.run.sessions.at(-1);
  check(last.end_reason==='cutoff','Clock ends block: '+condition);
  const late=await fetch(base+'/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:last.session_id,event_id:'late-fixture-'+condition,action:'release',payload:{id:Object.keys(last.state.requests)[0],version:1}})});
  check(late.status===409,'Late release refused: '+condition);
  await until(()=>js('!document.querySelector("#questionnaire").hidden'),'form');
  check(await js('[...document.querySelectorAll("#items input")].every(x=>x.value==="")'),'No questionnaire values fabricated: '+condition);
  await js('document.querySelector("#submit-form").click()');await until(()=>js('data.run.sessions.at(-1).questionnaire!==null'),'save blank form');
 }
 const record=await api('/pilot/export');fs.writeFileSync(out+'/complete_fixture.pilot.json',JSON.stringify(record,null,2)+'\n');
 check(record.pilot_version==='matched-qgm-v1' && record.record_kind==='software_fixture','Export version/kind');
 check(record.sessions.length===4 && record.sessions.slice(1).every(s=>s.duration_seconds===18&&s.question_ids.length===12),'All matched blocks complete');
 check(new Set(record.sessions.slice(1).flatMap(s=>s.source_ids)).size===6,'Scored sources disjoint');
 check(record.sessions.every(s=>s.questionnaire.tlx.every(x=>x===null)&&s.questionnaire.control.every(x=>x===null)),'Blank questionnaires retained');
 await shot('completed_software_fixture');fs.writeFileSync(out+'/browser_checks.json',JSON.stringify({record_kind:'software_fixture',checks,passed:checks.length,participant_observations:0},null,2)+'\n');console.log('Passed '+checks.length+' software checks');
} catch(error) {
 fs.writeFileSync(out+'/failure.json',JSON.stringify({record_kind:'software_fixture',error:String(error),checks},null,2)+'\n');
 if(created){try{const r=await(await fetch(base+'/pilot/export')).json();fs.writeFileSync(out+'/interrupted_fixture.pilot.json',JSON.stringify(r,null,2)+'\n');}catch{}}
 throw error;
} finally {if(ws)ws.close();child.kill('SIGTERM');}
