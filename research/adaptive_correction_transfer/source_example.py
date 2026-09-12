"""Show the actual financial source behind a prespecified transfer example."""
import textwrap,html
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .common import ART,read,write
from .plot import OUT,save,LABEL

def build():
 examples=read(ART/'analysis/examples.json');m=read(ART/'frozen/manifest.json');cs={c['id']:c for c in m['contexts']};pages=[]
 for key in ['transfer_help','transfer_tie','transfer_harm']:
  x=examples.get(key)
  if not x:continue
  c=cs[x['context']];r=read(ART/'evaluation/runs'/('%s_r%d_%s_b2.json'%(c['id'],x['rep'],x['method'])));ev=r['events'][int(x['step'])-1];repair=next(h for h in ev['repairs'] if h['id']==x['recipient']);qs={q['id']:q for q in c['questions']};f=ev['disclosure'];b=repair['before'];a=repair['after']
  lines=[('Inspected question',f['question']),('Question-specific annotation',str(f['answer'])+' '+f['scale']),('Recipient question',qs[x['recipient']]['question']),('Generated before',str(b['answer'])+' '+b['scale']),('Generated after',str(a['answer'])+' '+a['scale']),('Offline official EM',str(x['before'])+' -> '+str(x['after'])),('Generated revised derivation',a['derivation'])]
  pages.append('<section><h2>'+html.escape(key.replace('_',' ').title())+'</h2><p>Source '+html.escape(c['id'])+' | '+html.escape(LABEL[x['method']])+'</p><table>'+''.join('<tr><th>T'+str(i)+'</th>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in row)+'</tr>' for i,row in enumerate(c['table']))+'</table>'+''.join('<p><b>P'+str(p['order'])+'</b> '+html.escape(p['text'])+'</p>' for p in c['paragraphs'])+''.join('<p><b>'+label+':</b> '+html.escape(value)+'</p>' for label,value in lines)+'</section>')
  if key!='transfer_help':continue
  table=c['table'][:12];ncols=max(map(len,table));widths=[.06]+[.44]+[(.5/(ncols-1))]*(ncols-1);data=[];linecounts=[]
  for i,row in enumerate(table):
   wrapped=[str(i)]+[textwrap.fill(str(v),40 if j==0 else max(9,int(60/(ncols-1)))) for j,v in enumerate(row)]+['']*(ncols-len(row));data.append(wrapped);linecounts.append(max(v.count('\n')+1 for v in wrapped))
  fig=plt.figure(figsize=(10,8.5));ax=fig.add_axes([.05,.48,.9,.43]);ax.axis('off');tab=ax.table(cellText=data,colWidths=widths,cellLoc='left',bbox=[0,0,1,1]);tab.auto_set_font_size(False);tab.set_fontsize(8)
  for (i,j),cell in tab.get_celld().items():
   cell.set_height(linecounts[i]/sum(linecounts));cell.set_edgecolor('#c6d3da');cell.set_linewidth(.5)
   if i==0:cell.set_facecolor('#e3eef0')
  fig.text(.05,.96,'A correction reused on actual financial-report evidence',fontsize=14,weight='bold');fig.text(.05,.925,'Source rows are recorded report content; questions and reference feedback are benchmark annotations.',fontsize=9)
  foot='All source rows shown.' if len(c['table'])<=12 else 'First 12 source rows shown; complete source is in worked_sources.html.'
  fig.text(.05,.46,foot+' Left column gives the T row index.',fontsize=8,color='#4e6570');y=.415
  for label,value in lines:
   wrapped=textwrap.fill(label+': '+value,112);fig.text(.05,y,wrapped,fontsize=9,va='top');y-=(wrapped.count('\n')+1)*.023+.01
  fig.text(.05,.025,'First helpful transfer in frozen source order. Generated revisions are fallible. An answer label does not certify a shared root cause.',fontsize=8,color='#4e6570')
  save(fig,'source_example','Real financial-report table, human-written TAT-QA questions and question-specific reference feedback. Answers and revised derivation are generated. The first helpful adaptive transfer is chosen by frozen source order, with memory fallback only if none exists. Reference information and correctness are shown for offline analysis, not disclosed to uninspected agents.')
  captions=read(OUT/'captions.json');from .plot import captions as extra
  captions.update(extra);write(OUT/'captions.json',captions)
 style='<style>body{font:16px system-ui;max-width:1100px;margin:35px auto;line-height:1.5}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border:1px solid #bdcdd3;padding:8px}section{border-top:3px solid #176574;padding:20px 0;margin-top:30px}h1,h2{color:#17495a}</style>'
 (ART/'analysis/worked_sources.html').write_text('<!doctype html><meta charset="utf-8"><title>Source-grounded correction transfers</title>'+style+'<h1>Helpful, score-tied and harmful transfer</h1><p>First-qualifying examples. Real source tables and benchmark questions; generated proposals and repairs; simulated annotation inspection. All correctness labels below are offline evaluation information.</p>'+''.join(pages))
 print('Built full-source examples and source figure')
if __name__=='__main__':build()
