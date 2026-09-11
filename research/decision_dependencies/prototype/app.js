let state;
let actionSerial=0;
let visibilityObserver;
const scopeNames={'hotel.area':'Accommodation location','hotel.pricerange':'Accommodation price range','hotel.stars':'Hotel star rating','hotel.type':'Accommodation type','restaurant.area':'Dining location','restaurant.food':'Cuisine','restaurant.pricerange':'Dining price range'};
const escapeHtml=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const nice=s=>String(s??'unknown').replaceAll('_',' ').replace('.',' / ');
async function action(args){actionSerial++;let r=await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(args)});let data=await r.json();if(!r.ok){document.querySelector('#error').textContent=data.error;return null}state=data;document.querySelector('#error').textContent='';render();return data}
function render(){
 document.querySelector('#project').textContent='Shared travel plan';
 const waiting=state.requests.filter(r=>r.answer.status==='needs_user').length,stale=state.requests.filter(r=>r.work_status==='needs_revalidation').length;
 document.querySelector('#overview').textContent=`${waiting} clarification ${waiting===1?'request needs':'requests need'} an answer. ${stale} prepared ${stale===1?'draft needs':'drafts need'} revalidation. ${state.confirmations} ${state.confirmations===1?'answer':'answers'} supplied in this demonstration.`;
 document.querySelector('#update').disabled=state.source_stage===1;
 document.querySelector('#requests').innerHTML=state.requests.map(r=>{
  let a=r.answer,available=a.status==='available',stale=r.work_status==='needs_revalidation',source=a.source||{};
  const exceptions=state.records[r.key]?.exceptions||[];
  const requestOnly=source.scope==='request'||exceptions.includes(r.entity)||(r.kind||'preference')!=='preference';
  const audience=r.key&&!requestOnly?state.requests.filter(q=>q.key===r.key&&(q.kind||'preference')==='preference'&&!exceptions.includes(q.entity)&&q.answer.source?.scope!=='request').map(q=>q.agent).join(', '):r.agent;
  const sharing=requestOnly?'This answer applies only to this request.':!r.key?'Choose what this question decides before sharing an answer.':`Requests with this candidate scope: ${audience||r.agent}.`;
  return `<article class="card ${stale?'stale':!available?'attention':''} ${r.deferred?'deferred':''}" data-id="${escapeHtml(r.id)}"><div class="card-head"><h3>${escapeHtml(r.agent)}</h3><span class="badge ${stale?'stale':!available?'warn':''}">${r.deferred?'Postponed':stale?'Instruction changed':available?'Earlier answer found':'Needs clarification'}</span></div>
   <p>${escapeHtml(r.text)}</p>${available?`<div class="answer"><strong>${escapeHtml(a.value)}</strong><div class="scope">${source.scope==='request'?'Only this request':'This trip · '+escapeHtml(scopeNames[a.key]||nice(a.key))} · ${source.scope_status==='confirmed'?'User-confirmed scope':'Inferred scope - inspect before relying on it'}</div></div>`:`<p class="muted">${escapeHtml(nice(a.reason))}. An uncertain answer will not silently complete this work.</p>`}
   <p class="scope sharing">${escapeHtml(sharing)}</p>
   ${stale?`<p class="scope">Affected input: ${escapeHtml((r.affected||[]).map(k=>scopeNames[k]||nice(k)).join(', '))}. Re-prepare before releasing this draft.</p>`:''}
   ${source.quote?`<details data-inspect="${escapeHtml(r.id)}"><summary>Why this answer is suggested</summary><blockquote>${escapeHtml(source.quote)}</blockquote><span class="muted">${source.turn==null?'Your answer in this session.':'User turn '+escapeHtml(source.turn)+'.'} The quote and its inferred meaning can still be wrong.</span></details>`:''}
   <details><summary>Answer or change the scope</summary><form data-answer="${escapeHtml(r.id)}"><div class="form-row"><label>Your answer<input name="value" value="${escapeHtml(available?a.value:'')}" required></label><label>What this decides<select name="key" required><option value="">Choose the scope</option>${Object.entries(scopeNames).map(([k,v])=>`<option value="${k}" ${k===r.key?'selected':''}>${v}</option>`).join('')}</select></label></div><label>Where this answer applies<select name="scope"><option value="request">Only this request</option><option value="project">All requests for this trip and decision type</option></select></label><button class="primary" type="submit">Use my answer</button></form></details>
   <div class="buttons" style="margin-top:12px"><button data-release="${escapeHtml(r.id)}" ${r.work_status==='not_prepared'?'disabled':''}>Release checked draft</button><button data-defer="${escapeHtml(r.id)}">${r.deferred?'Bring back':'Postpone'}</button></div>
   <p class="scope">Work: ${escapeHtml(nice(r.work_status))}</p>${r.output?`<details data-inspect="${escapeHtml(r.id)}"><summary>Inspect prepared output</summary><pre>${escapeHtml(JSON.stringify(r.output.preview,null,2))}</pre></details>`:''}</article>`
 }).join('');
 document.querySelector('#decisions').innerHTML=Object.entries(state.records).map(([k,r])=>`<div class="decision"><div class="decision-title"><b>${escapeHtml(scopeNames[k]||nice(k))}</b><span>${escapeHtml(r.value??'Conflict')}</span></div><div class="scope">${r.scope_status==='confirmed'?'Confirmed by you':'Inferred from dialogue'} · version ${state.versions[k]}</div>${r.quote?`<blockquote>${escapeHtml(r.quote)}</blockquote>`:''}<details><summary>Revise, narrow or revoke</summary><form data-revise="${escapeHtml(k)}"><label>New value<input name="value" value="${escapeHtml(r.value??'')}"></label><label>Exception entities, separated by commas<input name="exceptions" value="${escapeHtml((r.exceptions||[]).join(', '))}" placeholder="e.g. conference-night"></label><button type="submit">Update and show affected work</button><button type="button" data-revoke="${escapeHtml(k)}">Revoke</button></form></details></div>`).join('')||'<p class="muted">No supported shared preference is available yet.</p>';
 const changes=state.events.filter(e=>['source_update','release_blocked','work_released','user_answer'].includes(e.kind)).slice(-7).reverse();
 document.querySelector('#changes').innerHTML=changes.map(e=>`<div class="change"><b>${escapeHtml(nice(e.kind))}</b><div>${escapeHtml(e.reason||nice(e.task_id||e.request_id||''))}</div>${e.affected_tasks?.length?`<div class="scope">Check: ${escapeHtml(e.affected_tasks.map(nice).join(', '))}</div>`:''}</div>`).join('');
 document.querySelector('#transcript').innerHTML=state.source_messages.map(t=>`<div class="turn"><b>Turn ${t.turn} · ${t.role}</b>${escapeHtml(t.text)}</div>`).join('');
 document.querySelectorAll('[data-answer]').forEach(f=>f.onsubmit=e=>{e.preventDefault();let x=Object.fromEntries(new FormData(f));action({action:'answer',id:f.dataset.answer,...x})});
 document.querySelectorAll('[data-revise]').forEach(f=>f.onsubmit=e=>{e.preventDefault();let x=Object.fromEntries(new FormData(f));action({action:'revise',key:f.dataset.revise,value:x.value,exceptions:x.exceptions.split(',').map(x=>x.trim()).filter(Boolean)})});
 document.querySelectorAll('[data-release]').forEach(b=>b.onclick=()=>action({action:'release',id:b.dataset.release}));
 document.querySelectorAll('[data-defer]').forEach(b=>b.onclick=()=>action({action:state.requests.find(r=>r.id===b.dataset.defer).deferred?'resume':'defer',id:b.dataset.defer}));
 document.querySelectorAll('[data-revoke]').forEach(b=>b.onclick=()=>action({action:'revise',key:b.dataset.revoke,revoke:true}));
 document.querySelectorAll('[data-inspect]').forEach(d=>d.ontoggle=()=>{if(d.open)fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'inspect',id:d.dataset.inspect,view:d.querySelector('summary').textContent})})});
 if(visibilityObserver)visibilityObserver.disconnect();
 visibilityObserver=new IntersectionObserver(entries=>{const ids=entries.filter(e=>e.isIntersecting).map(e=>e.target.dataset.id);if(ids.length)fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'shown',ids,visibility:'at least half the card in the viewport'})})},{threshold:.5});
 document.querySelectorAll('.card').forEach(c=>visibilityObserver.observe(c));
}
document.querySelector('#prepare').onclick=()=>action({action:'prepare'});document.querySelector('#update').onclick=()=>action({action:'source_update'});document.querySelector('#reset').onclick=()=>action({action:'reset'});
fetch('/api/state').then(r=>r.json()).then(s=>{state=s;render()});
setInterval(async()=>{if(!state||document.activeElement?.matches('input,select,textarea'))return;const serial=actionSerial;try{const fresh=await(await fetch('/api/state')).json();if(serial===actionSerial&&JSON.stringify(fresh)!==JSON.stringify(state)){state=fresh;render()}}catch{}},1500);
