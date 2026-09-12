// Pilot-only presentation additions; all decisions still use the original Desk.
const bar=document.querySelector('.toolbar');
// Keep optional source-session controls discoverable above the long financial source.
document.querySelector('#active').before(document.querySelector('#group'));

const calculator=document.createElement('details');calculator.id='calculator';calculator.innerHTML='<summary>Calculator</summary><label>Expression <input id="calc-expression" placeholder="(114 - 108) / 108 * 100" aria-label="Calculator expression"></label><button id="calculate">Calculate</button><output id="calc-result" aria-live="polite"></output><small> Numbers and + − * / parentheses. Results round to two decimals. This does not check source interpretation.</small>';bar.append(calculator);
const timer=document.createElement('strong');timer.id='session-timer';timer.setAttribute('aria-live','off');bar.prepend(timer);
document.getElementById('calculate').onclick=async()=>{try{const r=await post('/pilot/calculate',{expression:document.getElementById('calc-expression').value});document.getElementById('calc-result').textContent=' = '+r.result}catch(e){document.getElementById('calc-result').textContent=e.message}};
const baseActive=renderActive;
renderActive=function(){baseActive();const a=state?.active;if(!a)return;
 const only=state.pilot?.condition==='S',empty=!(a.output.answer||[]).length;
 const sourceDetails=document.querySelector('#active .review-body section:last-child details');
 const raw=state.pilot?.raw_proposals?.[a.request_id];
 if(sourceDetails){
  if(only)sourceDetails.hidden=true;
  else if(raw){sourceDetails.id='original-model-response';sourceDetails.querySelector('summary').textContent='Inspect original model response (version 1)';sourceDetails.querySelector('pre').textContent=JSON.stringify(raw.raw_response,null,2);sourceDetails.ontoggle=()=>{if(sourceDetails.open)logView('original_response_open')};}
 }

 const section=document.querySelector('#active .review-body section');
 if(empty){document.getElementById('approve').disabled=true;document.getElementById('approve').title='No usable answer: write an answer, reject or defer.';const p=document.createElement('p');p.className='notice';p.id='empty-answer';p.textContent=only?'Source-only task. Write an answer from the evidence, or reject or defer.':'The agent supplied no usable answer. You may write your own answer, reject or defer. Any explanation below is generated and may also be wrong.';section.prepend(p);}
 if(only){const badge=section.querySelector('.badge');if(badge)badge.textContent='Your answer · no model proposal';section.querySelector('.answer').textContent='Not answered yet';
 const ps=[...section.children].filter(x=>x.tagName==='P');ps.forEach(p=>{if(p.classList.contains('section-label')||p.textContent.startsWith('Generated citations:')||p.textContent.includes('Source-only task. No model'))p.hidden=true});
 document.getElementById('approve').hidden=true;document.getElementById('reject').textContent='Cannot answer (block)';document.getElementById('correction').open=true;document.querySelector('#correction summary').textContent='Write your answer';document.getElementById('correct').textContent='Record and approve my answer';
 document.querySelector('#correction p').textContent='Record your answer as a new version. A separate release action completes it.';
 }
 // A correction draft remains a draft. Deferring stores it with the note, without approval.
 const defer=document.getElementById('defer');defer.onclick=()=>{const draft={answer:document.getElementById('correct-answer').value,scale:document.getElementById('correct-scale').value,note:document.getElementById('note').value};action('decide',{id:a.request_id,version:a.version,decision:'defer',note:JSON.stringify({pilot_draft:draft}),until:state.elapsed+30})};
 try{const saved=JSON.parse(a.notes||'');if(saved.pilot_draft){document.getElementById('note').value=saved.pilot_draft.note;document.getElementById('correct-answer').value=saved.pilot_draft.answer;document.getElementById('correct-scale').value=saved.pilot_draft.scale;document.getElementById('correction').open=true}}catch(e){}
 const authorField=document.getElementById('correct-answer'),authorButton=document.getElementById('correct');
 const checkDraft=()=>authorButton.disabled=!!state.session_closed||!authorField.value.trim();authorField.addEventListener('input',checkDraft);checkDraft();
};
const baseRender=render;
render=function(s){baseRender(s);const seconds=Math.max(0,Math.ceil((s.study?.duration_seconds||0)-s.elapsed));timer.textContent=s.session_closed?'Block ended':`${Math.floor(seconds/60)}:${String(seconds%60).padStart(2,'0')} remaining`;timer.style.marginRight='20px';
 // Base rendering hides setup labels/details. The calculator is common to both conditions.
 calculator.style.display='block';calculator.querySelectorAll('label').forEach(x=>x.style.display='inline-block');
 document.querySelectorAll('.toolbar #start,.toolbar #restore,.toolbar a,.toolbar > label').forEach(x=>x.hidden=true);
 if(s.pilot)document.getElementById('banner').textContent=s.session_closed?'Block ended. Work is saved; no further approval or release is permitted.':s.banner;
 document.querySelector('header h1').textContent='Review desk';
};
if(state){activeKey='';render(state)}

window.addEventListener('blur',()=>logView('window_blur'));window.addEventListener('focus',()=>logView('window_focus'));
