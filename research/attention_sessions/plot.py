"""Publication figures from saved tables and traces; no new simulations."""
from pathlib import Path
import csv,json,gzip
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .data import ROOT,load as load_source,workload,bundles,save_json
from .analyze import PRIMARY

OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)
NAMES={'no_review':'No review','fifo':'FIFO','edf':'EDF','greedy':'Benefit greedy','density':'Benefit / time',
       'fixed_window':'Fixed window','unguarded':'Unguarded session','sticky_edf':'Sticky EDF','allocation':'Capacity allocation','guarded':'Guarded session'}
COLORS={'no_review':'#777777','fifo':'#999933','edf':'#4477aa','greedy':'#cc6677','density':'#aa4499',
        'fixed_window':'#66ccee','unguarded':'#ddaa33','sticky_edf':'#228833','allocation':'#9999cc','guarded':'#004488'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':11,'axes.labelsize':10,
                     'xtick.labelsize':9,'ytick.labelsize':9,'pdf.fonttype':42,'svg.fonttype':'none',
                     'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.18})

def table(name):
    rows=list(csv.DictReader((ROOT/'analysis'/name).open()))
    for r in rows:
        for k,v in r.items():
            try:r[k]=float(v)
            except (ValueError,TypeError):pass
    return rows
S=table('policy_summary.csv');P=table('paired.csv');D=table('dominance.csv');B=table('bundle_differences.csv')
def row(cid,p):return next(x for x in S if x['condition_id']==cid and x['policy']==p)
def pair(cid,comp='sticky_edf'):return next(x for x in P if x['condition_id']==cid and x['comparison']=='guarded-'+comp)
def save(fig,name):
    fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight');fig.savefig(OUT/(name+'.svg'),bbox_inches='tight');fig.savefig(OUT/(name+'.png'),dpi=300,bbox_inches='tight');plt.close(fig)
    svg=OUT/(name+'.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')

fig,axes=plt.subplots(1,2,figsize=(10,4.4))
for ax,cid,title in zip(axes,[PRIMARY,'core_high_1_12_model_risk'],['Ideal review reference','Saved fallible review; risk-only allocation']):
    for i,(p,name) in enumerate(NAMES.items()):
        r=row(cid,p);dom=next(x['dominated_by'] for x in D if x['condition_id']==cid and x['policy']==p)
        ax.scatter(r['active_time'],r['loss'],color=COLORS[p],s=65,marker='x' if dom else 'o',zorder=4)
        offsets={'allocation':(5,-10),'sticky_edf':(4,-10),'guarded':(-17,10),'edf':(5,8)}
        ax.annotate(str(i+1),(r['active_time'],r['loss']),xytext=offsets.get(p,(4,4+(i%2)*7)),textcoords='offset points',fontsize=9)
    ax.set(xlabel='Modeled active review time (abstract ticks)',ylabel='Unresolved weighted loss / bundle',title=title)
fig.text(.07,-.02,' · '.join('%d %s'%(i+1,n) for i,n in enumerate(NAMES.values()) if i<5),fontsize=9)
fig.text(.07,-.07,' · '.join('%d %s'%(i+1,n) for i,n in enumerate(NAMES.values()) if i>=5),fontsize=9)
fig.text(.07,-.12,'Circles: nondominated mean loss/time. Crosses: dominated. Six source bundles; no human-effort measurement.',fontsize=9)
fig.tight_layout();save(fig,'quality_effort')

fig,axes=plt.subplots(1,2,figsize=(9,3.6),sharey=True)
for ax,comp in zip(axes,['sticky_edf','greedy']):
    vals=[x for x in B if x['condition_id']==PRIMARY and x['comparison']=='guarded-'+comp];vals.sort(key=lambda r:r['bundle'])
    d=[r['loss_difference'] for r in vals];ax.bar(range(6),d,color=['#228833' if x<0 else '#cc6677' if x>0 else '#aaaaaa' for x in d]);ax.axhline(0,color='#222222',lw=.7)
    r=pair(PRIMARY,comp);ax.set(title='Guarded − '+NAMES[comp],xlabel='Constructed source bundle',xticks=list(range(6)),ylim=(-15,15))
    ax.text(.97,.96,'Mean %.2f [%.2f, %.2f]\nW/T/L %d/%d/%d'%(r['loss'],r['loss_low'],r['loss_high'],r['wins'],r['ties'],r['losses']),transform=ax.transAxes,va='top',ha='right',fontsize=9)
axes[0].set_ylabel('Paired weighted loss difference\nNegative favors guarded sessions');fig.tight_layout();save(fig,'paired_differences')

fig,axes=plt.subplots(2,2,figsize=(9,6.4),sharex=True)
for j,load in enumerate(['low','high']):
    for policy in ['edf','greedy','sticky_edf','unguarded','guarded']:
        rs=[row('core_%s_1_%s_ideal'%(load,b),policy) for b in (24,12,6)];x=[18/24,18/12,18/6]
        for ax,metric in zip(axes[:,j],['loss','session_offers']):ax.plot(x,[r[metric] for r in rs],'-o',color=COLORS[policy],label=NAMES[policy],ms=4)
    axes[0,j].set_title(load.capitalize()+' arrival contention');axes[1,j].set_xlabel('Standalone demand / active budget\n(18 ticks divided by available budget)')
axes[0,0].set_ylabel('Weighted loss / bundle');axes[1,0].set_ylabel('Session offers / bundle')
axes[0,0].legend(fontsize=8);fig.tight_layout();save(fig,'demand_capacity')

variants=[(PRIMARY,'Primary'),('core_high_0_12_ideal','Zero setup / switch'),('no_reuse_ideal','No context reuse'),('unrelated_ideal','Unrelated contexts'),('imperfect_ideal','Imperfect suggestions'),('complex_groups_ideal','Higher group overhead'),('slow_decisions_ideal','Slower decisions'),('singleton_ideal','Session bound one'),('no_reconsider_ideal','No reconsideration')]
fig,axes=plt.subplots(1,2,figsize=(9,5.4),sharey=True)
for ax,metric,label in zip(axes,['loss','active_time'],['Loss difference','Active-time difference (ticks)']):
    vals=[pair(cid)[metric] for cid,_ in variants];ax.barh(range(len(vals)),vals,color=['#228833' if v<0 else '#cc6677' for v in vals]);ax.axvline(0,color='#222222',lw=.8);ax.set_xlabel('Guarded − sticky EDF\n'+label)
    ax.set_yticks(range(len(vals)));ax.set_yticklabels([label for _,label in variants]);ax.invert_yaxis()
fig.tight_layout();save(fig,'ablations')

fig,axes=plt.subplots(1,2,figsize=(10,4))
ps=list(NAMES);y=np.arange(len(ps))
for ax,metric,title in zip(axes,['correct','loss'],['Correct diagnoses / 9 tickets','Weighted unresolved loss']):
    rs=[row(PRIMARY,p) for p in ps];values=np.array([r[metric] for r in rs]);low=np.array([r[metric+'_low'] for r in rs]);high=np.array([r[metric+'_high'] for r in rs])
    ax.barh(y,values,color=[COLORS[p] for p in ps]);ax.errorbar(values,y,xerr=[values-low,high-values],fmt='none',ecolor='#333333',capsize=2,lw=.7)
    ax.set_yticks(y);ax.set_yticklabels([NAMES[p] for p in ps]);ax.invert_yaxis();ax.set_xlabel(title)
fig.tight_layout();save(fig,'quality_and_loss')

with gzip.open(ROOT/'evaluation/traces.jsonl.gz','rt') as f:T=[json.loads(x) for x in f]
cases,records,e=load_source();configs=json.loads((ROOT/'declaration.json').read_text())['conditions'];config=next(x for x in configs if x['condition_id']==PRIMARY)

def timeline(bundle,name,comp='sticky_edf'):
    public,_=workload(bundles(cases)[bundle],cases,records,e,config);public.sort(key=lambda r:(r.context,r.request_id))
    ids=[r.request_id for r in public];context_colors={ctx:c for ctx,c in zip(sorted({r.context for r in public}),['#4477aa','#228833','#cc6677'])}
    fig,axes=plt.subplots(2,1,figsize=(9,6),sharex=True)
    for ax,p in zip(axes,[comp,'guarded']):
        trace=next(x for x in T if x['condition_id']==PRIMARY and x['bundle']==bundle and x['policy']==p)
        for i,r in enumerate(public):
            ax.plot([r.arrival,r.deadline],[i,i],color='#b9c4cb',lw=1);ax.scatter(r.arrival,i,marker='>',s=25,c='#555555');ax.scatter(r.deadline,i,marker='x',s=25,c='#222222')
        for event in trace['events']:
            if event['event']!='review_started':continue
            i=ids.index(event['request_id']);start=event['tick'];r=next(r for r in public if r.request_id==event['request_id'])
            for part in ['setup','switch','coordination','decision']:
                length=event['parts'][part]
                if length:ax.barh(i,length,left=start,height=.6,color=context_colors[r.context] if part=='decision' else '#d0d8df',edgecolor='white',hatch='//' if part=='switch' else None);start+=length
            ax.scatter(event['finish'],i,c=context_colors[r.context],s=22,zorder=4)
            ax.text(event['tick'],i-.36,'S'+str(event['session_id']),fontsize=7.5)
        m=trace['metrics'];ax.set_title('%s: loss %g; active time %.2f; %d session offers'%(NAMES[p],m['loss'],m['active_time'],m['session_offers']),loc='left')
        ax.set_yticks(range(len(ids)));ax.set_yticklabels(ids,fontsize=9);ax.invert_yaxis();ax.set_ylim(len(ids)-.5,-.8)
    axes[1].set_xlabel('Abstract simulation ticks · triangle: arrival · cross: cutoff · gray: overhead · color: decision')
    fig.tight_layout();save(fig,name)

timeline(0,'timeline_unfavorable');timeline(1,'timeline_tied')
# Explicit secondary example: first numerical improvement over original greedy,
# not a replacement for the absent favorable primary comparison.
favorable=next(int(x['bundle']) for x in B if x['condition_id']==PRIMARY and x['comparison']=='guarded-greedy' and x['loss_difference']<0)
timeline(favorable,'timeline_secondary_benefit',comp='greedy')
save_json(ROOT/'analysis/secondary_example_selection.json',dict(comparator='greedy',rule='First numerical primary-condition bundle with guarded loss below original benefit greedy; secondary comparator, not a favorable sticky-EDF case',bundle=favorable))
print('Saved 8 figures in PDF/SVG/300-dpi PNG')
