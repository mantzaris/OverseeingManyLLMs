"""Publication plots from saved measurements, never manually entered outcomes."""
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from .common import ART,read,write

COLORS=dict(threads='#687c89',queue='#3267a2',sessions='#087f7a')
NAMES=dict(threads='A · Threads',queue='B · Queue',sessions='C · Sessions')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.titlesize':10,'axes.labelsize':9,'legend.fontsize':8,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','savefig.dpi':220})

def save(fig,name,caption):
    out=ART/'figures';out.mkdir(exist_ok=True)
    fig.tight_layout()
    for ext in ('pdf','svg','png'):fig.savefig(out/f'{name}.{ext}',bbox_inches='tight',metadata={'Creator':'OverseeingManyLLMs saved-output plotting'} if ext=='pdf' else None)
    plt.close(fig)
    (out/f'{name}.caption.txt').write_text(caption+'\n')


def main():
    runs=read(ART/'software_summary.json');conditions=list(csv.DictReader((ART/'tables/conditions.csv').open()));latency=read(ART/'tables/latency.json')
    # A live clock, not a rescaled animation.
    events=read(ART/'live/events.json');offers=[e for e in events if e['action']=='offer'];ids=[e['payload']['id'] for e in offers]
    fig,(ax,focus)=plt.subplots(2,1,figsize=(7.0,4.7),sharex=True,gridspec_kw={'height_ratios':[3,1]})
    for i,rid in enumerate(ids):
        start=next(e['at'] for e in events if e['action']=='start' and e['payload']['id']==rid)
        end=next(e['at'] for e in events if e['action']=='receive' and e['payload']['id']==rid)
        worker=offers[i]['payload']['agent'];color={'Worker 1':'#3267a2','Worker 2':'#087f7a','Worker 3':'#b77a28'}[worker]
        ax.plot([start,end],[i,i],color=color,lw=5,alpha=.5);ax.scatter([end],[i],color=color,s=17,zorder=5)
    ax.set_yticks(range(len(ids)));ax.set_yticklabels([f'Q{i+1}' for i in range(len(ids))]);ax.invert_yaxis();ax.set_ylabel('Distinct financial questions');ax.set_title('Observed live task lifetime and answer arrival (12 questions, 2 sources)')
    selections=[e for e in events if e['action']=='select' and e['response']['ok']]
    for i,e in enumerate(selections):
        end=next((x['at'] for x in events if x['at']>e['at'] and x['action']=='decide' and x['response']['ok'] and x['payload']['id']==e['payload']['id']),events[-1]['at'])
        focus.barh(i,end-e['at'],left=e['at'],color='#087f7a',height=.35)
        focus.text((e['at']+.15) if i==0 else (end-.10),i,f"Pinned Q{ids.index(e['payload']['id'])+1}",ha='left' if i==0 else 'right',va='center',fontsize=8,color='white')
    pause=next(e['at'] for e in events if e['action']=='pause');resume=next(e['at'] for e in events if e['action']=='resume')
    for a in (ax,focus):a.axvspan(pause,resume,color='#d7a747',alpha=.15)
    for e in events:
        if e['action']=='revise':focus.axvline(e['at'],color='#bd5b31',ls='--');focus.text(e['at'],1.4,'New draft',ha='right',fontsize=8,color='#99472a')
    focus.set_yticks([]);focus.set_ylim(-.5,1.8);focus.set_xlabel('Elapsed wall time (seconds)');focus.set_ylabel('Scripted review');focus.set_title('Shading: new starts paused; in-flight answers still arrive',loc='left',fontsize=8)
    save(fig,'live_timeline','Actual GPU task-worker start/arrival times and scripted review actions. Bars include waiting for the shared serial GPU. Source data and questions are real benchmark material. Shading marks an admission pause. No human review time is measured.')
    # Queue and all outstanding work on the same observation clock.
    fig,axs=plt.subplots(2,2,figsize=(7.0,4.7),sharex=True)
    grid=np.linspace(0,2.2,111)
    for col,load in enumerate(('lower','higher')):
        for cond in COLORS:
            files=[ART/'scenarios'/f"b{s['bundle']:02d}_r{s['replica']}_{cond}_{load}.json" for s in runs if s['condition']==cond and s['load']==load]
            for row,metric in enumerate(('queued','remaining')):
                ys=[]
                for p in files:
                    samples=read(p)['samples'];times=[x['at'] for x in samples];values=[x[metric] for x in samples]
                    ys.append(np.interp(grid,times,values,left=values[0],right=values[-1]))
                axs[row,col].plot(grid,np.mean(ys,axis=0),color=COLORS[cond],label=NAMES[cond],ls='--' if cond=='threads' else '-',lw=1.6)
            axs[0,col].set_title(('Lower' if load=='lower' else 'Higher')+' arrival concentration')
        axs[1,col].set_xlabel('Measured scenario time (seconds)')
        axs[0,col].axvspan(.25,.65,color=COLORS['sessions'],alpha=.08)
        axs[1,col].axvspan(.25,.65,color=COLORS['sessions'],alpha=.08)
    axs[0,0].set_ylabel('Queued requests');axs[1,0].set_ylabel('All unfinished reviews');axs[0,1].legend(loc='upper right');
    save(fig,'queue_and_outstanding','Mean measured counts over 24 scripted runs per curve (12 paired source bundles, two generated-answer replicas). All tasks are offered at time zero. Arrival concentration and a C-only admission pause (.25-.65 s) are constructed. Unfinished reviews include offered unstarted work. Curves do not measure human burden.')
    checkpoints=list(csv.DictReader((ART/'tables/pause_checkpoint.csv').open()))
    fig,axs=plt.subplots(1,2,figsize=(7.0,3.5),sharey=True)
    layers=[('released','Released','#087f7a'),('queued','Queued','#d6a94a'),('active','Active','#3267a2'),('deferred','Deferred','#b16b9b'),('in_flight','In flight','#9cbdcf'),('unstarted','Not started','#d5dde3')]
    for ax,when in zip(axs,('pause','cutoff')):
        rows=[]
        for cond in ('queue','sessions'):
            for load in ('lower','higher'):
                if when=='cutoff':row=next(s for s in conditions if s['condition']==cond and s['load']==load)
                else:
                    ss=[s for s in checkpoints if s['condition']==cond and s['load']==load]
                    row={k:sum(int(s[k]) for s in ss) for k in ['offered']+[x[0] for x in layers]}
                    row.update(condition=cond,load=load)
                rows.append(row)
        x=np.arange(4);bottom=np.zeros(4)
        for key,label,color in layers:
            vals=np.array([int(s[key]) for s in rows]);ax.bar(x,vals,bottom=bottom,color=color,label=label,width=.68);bottom+=vals
        ax.scatter(x,[int(s['offered']) for s in rows],marker='_',s=150,color='black',zorder=5)
        ax.set_xticks(x);ax.set_xticklabels([('B' if s['condition']=='queue' else 'C')+' / '+('low' if s['load']=='lower' else 'high') for s in rows],rotation=25,ha='right')
        ax.set_title('During C pause (0.45 s)' if when=='pause' else 'Observation cutoff (2.2 s)')
    axs[0].set_ylabel('All 290 offered task instances');axs[0].set_ylim(0,315)
    axs[1].legend(loc='upper center',bbox_to_anchor=(-.15,-.32),ncol=3)
    save(fig,'work_accounting','Recorded event prefixes at the midpoint of the declared admission pause and at the final cutoff. The midpoint is a descriptive accounting audit, not a new evaluation condition. Every B/C load includes all 290 offered tasks from 24 sources and two replicas. Corrected releases use ideal simulated annotation disclosure. Pausing may shift work into the not-started category; it never removes it.')
    # Timing distributions, not participant measurements.
    fig,axs=plt.subplots(1,3,figsize=(7.0,2.9))
    keys=['protocol_handler_ms','browser_http_roundtrip_ms','browser_received_to_render_ms']
    labels=['Atomic command handler','Browser HTTP round trip','State receipt to DOM update']
    for ax,key,label in zip(axs,keys,labels):
        z=latency[key];ax.bar([0,1],[z['median'],z['p95']],color=['#3267a2','#087f7a'],width=.6)
        for i,v in enumerate([z['median'],z['p95']]):ax.text(i,v+max(z['p95']*.06,.02),f'{v:.2f}',ha='center',fontsize=8)
        ax.set_xticks([0,1]);ax.set_xticklabels(['Median','95th pct.']);ax.set_ylim(0,z['p95']*1.35+.1);ax.set_title(label+'\n'+str(z['n'])+' observations',fontsize=9);ax.set_ylabel('Milliseconds')
    save(fig,'software_latency','Measured local software timings. Command handling includes protocol validation and state hashing. HTTP round trip includes local transport and serialization. Receipt-to-DOM-update measures JavaScript rendering after state receipt, not the browser compositor, network one-way delay, human response or model inference. Observation counts are events, not independent sources.')
    fig,axs=plt.subplots(1,2,figsize=(7.0,3.2),sharey=True)
    paired=list(csv.DictReader((ART/'tables/paired_bundles.csv').open()));contrasts=read(ART/'tables/contrasts.json')
    for ax,load in zip(axs,('lower','higher')):
        ds=[float(x['sessions_minus_queue']) for x in paired if x['load']==load and x['metric']=='correct_released'];c=next(x for x in contrasts if x['load']==load and x['metric']=='correct_released')
        ax.axhline(0,color='#abb8c1',lw=1);ax.scatter(range(1,13),ds,color='#087f7a',s=28)
        ax.set_xticks([1,4,8,12]);ax.set_xlabel('Paired source bundle');ax.set_title(load.title()+f" arrivals\nC better / tied / worse: {c['positive']} / {c['ties']} / {c['negative']}")
        ax.text(.03,.95,f"Mean {c['mean']:+.3f}\nBundle interval [{c['ci95'][0]:+.3f}, {c['ci95'][1]:+.3f}]",transform=ax.transAxes,va='top',fontsize=8)
        ax.set_ylim(min(-1.1,min(ds)-.5),max(1.1,max(ds)+.5))
    axs[0].set_ylabel('Correct releases: C minus B\n(positive favors sessions)')
    save(fig,'paired_script_outcomes','Twelve paired constructed bundles, averaging two generated-answer replicas before a fixed-seed 2,000-resample paired bootstrap. Ideal scripted review determines correctness after disclosure. These contrasts describe fixed software scripts and cannot establish human effectiveness or equivalence.')
    # Explicit protocol diagram with authority kept per output.
    fig,ax=plt.subplots(figsize=(7,3));ax.set_xlim(0,10);ax.set_ylim(0,4);ax.axis('off')
    boxes=[(.1,2.2,1.65,.8,'Offered tasks\npaused work\nstays visible'),(2.1,2.2,1.65,.8,'Task workers\nsame model\nshared GPU'),(4.1,2.2,1.65,.8,'Requests\nversion + source'),(6.1,2.2,1.65,.8,'Pinned review\none output/version'),(8.1,2.2,1.75,.8,'Decide on\nthis version\nthen release')]
    for x0,y,w,h,label in boxes:ax.add_patch(Rectangle((x0,y),w,h,facecolor='#eef5f7',edgecolor='#5e8194'));ax.text(x0+w/2,y+h/2,label,ha='center',va='center',fontsize=8)
    for i in range(4):ax.annotate('',xy=(boxes[i+1][0],2.6),xytext=(boxes[i][0]+boxes[i][2],2.6),arrowprops=dict(arrowstyle='->',color='#416477'))
    ax.text(6.9,1.15,'Defer: keep draft, source and history\nReject: block, do not claim completion',ha='center',fontsize=9)
    ax.annotate('',xy=(6.9,1.5),xytext=(6.9,2.2),arrowprops=dict(arrowstyle='->',color='#a57328'))
    ax.text(5,.45,'New arrivals update pending work. A revision never inherits an approval.',ha='center',fontsize=9,color='#087f7a')
    save(fig,'protocol','Specified software workflow, not an empirical human result. Each request has its own approval authority. A source session changes navigation, never merges answers or decisions.')
    write(ART/'figures/manifest.json',dict(source_tables=['tables/conditions.csv','tables/paired_bundles.csv','tables/latency.json','software_summary.json','live/events.json'],figures=[p.stem for p in sorted((ART/'figures').glob('*.pdf'))],style='Accessible teal/blue/ochre; physical units specified; vector PDF/SVG and 220 dpi PNG.'))
    print('Six figures regenerated')

if __name__=='__main__':main()
