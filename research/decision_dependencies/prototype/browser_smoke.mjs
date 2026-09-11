// Actual-browser walkthrough. These are scripted demonstrations, not participant data.
import fs from 'node:fs';
import {spawn} from 'node:child_process';
const out='artifacts/decision_dependencies/interface';fs.mkdirSync(out,{recursive:true});
const chrome=process.env.CHROME||'/opt/google/chrome/google-chrome';
const child=spawn(chrome,['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-background-networking','--no-first-run','--user-data-dir=/tmp/decision-browser-'+process.pid,'--remote-debugging-port=9227','about:blank'],{stdio:'ignore'});
const wait=ms=>new Promise(r=>setTimeout(r,ms));let ws;
try{
 let pages;for(let i=0;i<50;i++){try{pages=await(await fetch('http://127.0.0.1:9227/json/list')).json();if(pages.length)break}catch{}await wait(100)}
 if(!pages?.length)throw Error('Browser did not start');ws=new WebSocket(pages.find(x=>x.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
 let next=0,pending=new Map(),errors=[];ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result)}if(m.method==='Runtime.exceptionThrown')errors.push(m.params)};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++next;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
 async function js(expression){const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value}
 const assert=(x,m)=>{if(!x)throw Error(m)};
 async function screenshot(name){await wait(100);const r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(out+'/'+name+'.png',Buffer.from(r.data,'base64'))}
 await send('Runtime.enable');await send('Page.enable');await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:'http://127.0.0.1:9027/'});await wait(400);await js("action({action:'reset'})");
 assert(await js("document.querySelectorAll('.card').length===4"),'Four actual agent cards');
 assert(await js("!document.body.innerText.includes('annotation_states')"),'No evaluator state exposed');
 await screenshot('initial_questions');
 // Use the visible form to answer once for an explicit project scope.
 await js("(()=>{const f=document.querySelector('[data-answer=dining_shortlist]');f.closest('details').open=true;f.elements.value.value='christmas';f.elements.key.value='restaurant.food';f.elements.scope.value='project';f.requestSubmit()})()");await wait(200);
 assert(await js("state.requests.filter(r=>r.answer.value==='christmas').length===2"),'One scoped answer resolves both paraphrases');
 await js("document.querySelector('#prepare').click()");await wait(150);await screenshot('shared_answer_and_work');
 await js("document.querySelector('#update').click()");await wait(150);
 assert(await js("state.requests.find(r=>r.id==='dining_shortlist').work_status==='needs_revalidation'"),'Changed source invalidates prepared work');
 await js("action({action:'release',id:'dining_shortlist'})");
 assert(await js("state.tasks.dining_shortlist.status==='needs_revalidation'"),'Stale release blocked');
 await screenshot('instruction_change');
 await js("action({action:'prepare'})");await js("action({action:'release',id:'dining_shortlist'})");
 assert(await js("state.tasks.dining_shortlist.answers['restaurant.food'].value==='indian'"),'Revalidated artifact uses updated source');
 // A distinct conference dinner is an explicitly named exception, not an inferred shared answer.
 await js("action({action:'revise',key:'restaurant.food',value:'indian',exceptions:['conference-night']})");
 await js("action({action:'submit',request:{id:'conference_dinner',project:state.project,agent:'Conference dinner',text:'What cuisine should the separate conference dinner use?',key:'restaurant.food',entity:'conference-night',kind:'preference'}})");
 assert(await js("state.requests.find(r=>r.id==='conference_dinner').answer.reason==='explicit_exception'"),'Named exception prevents automatic reuse');
 const rejected=await js("fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'answer',id:'conference_dinner',key:'restaurant.food',value:'italian',scope:'project'})}).then(r=>r.status)");
 assert(rejected===400,'Exception cannot silently widen scope');
 await js("action({action:'answer',id:'conference_dinner',key:'restaurant.food',value:'italian',scope:'request'})");
 assert(await js("state.requests.find(r=>r.id==='dining_shortlist').answer.value==='indian' && state.requests.find(r=>r.id==='conference_dinner').answer.value==='italian'"),'Different scoped answers remain distinct');
 assert(await js("document.querySelector('[data-id=conference_dinner] .sharing').textContent==='This answer applies only to this request.'"),'Exception display does not imply propagation to ordinary requests');
 await js("action({action:'defer',id:'accommodation_brief'})");
 assert(await js("state.requests.find(r=>r.id==='accommodation_brief').deferred"),'Unresolved deferred work remains visible');
 await send('Runtime.evaluate',{expression:"document.querySelector('[data-id=conference_dinner]').scrollIntoView({block:'center'})"});await screenshot('explicit_exception');
 await send('Emulation.setDeviceMetricsOverride',{width:430,height:1000,deviceScaleFactor:1,mobile:true});await js('window.scrollTo(0,0)');await screenshot('mobile_overview');
 assert(await js('document.documentElement.scrollWidth<=window.innerWidth+2'),'No horizontal overflow on mobile');
 assert(errors.length===0,'No browser exceptions');
 const final=await js("({project:state.project,epoch:state.epoch,questions:state.requests.length,answers:state.confirmations})");
 fs.writeFileSync(out+'/browser_verification.json',JSON.stringify({status:'passed',data_type:'scripted demonstration, not participant observations',checks:['actual form submission','shared answer','source update','stale release rejection','updated output','explicit exception','scope widening rejection','request-only answer','deferral','mobile overflow','no browser exceptions'],final,errors},null,2)+'\n');
 const log=await(await fetch('http://127.0.0.1:9027/api/log')).text();fs.writeFileSync(out+'/walkthrough_interactions.jsonl',log);
 console.log('Browser walkthrough and five screenshots passed');await send('Browser.close');
}finally{if(ws)ws.close();child.kill()}
