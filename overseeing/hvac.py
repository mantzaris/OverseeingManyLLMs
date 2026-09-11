"""Measured FLEXLAB diagnosis and simulated review. Historical paths are unchanged."""
import copy,csv,hashlib,json,math,random,time
from dataclasses import dataclass,asdict
from datetime import datetime
from itertools import permutations
from pathlib import Path

LABELS=('normal','outdoor_damper','heating_valve','cooling_valve')
POLICIES=('no_review','fcfs','edf','uncertainty','greedy','search')
FIELDS={'sat':'Supply Air Temperature','heat_sp':'Supply Air Temperature Heating Set Point','cool_sp':'Supply Air Temperature Cooling Set Point','outdoor':'Outdoor Air Temperature','mixed':'Mixed Air Temperature','return':'Return Air Temperature','fan':'Supply Air Fan Speed Control Signal','damper':'Outdoor Air Damper Control Signal','cool_valve':'Cooling Coil Valve Control Signal','heat_valve':'Heating Coil Valve Control Signal'}
DATES={'SZCAV':{'cooling_valve':['3/11/2017','3/12/2017','3/15/2017','3/16/2017','3/31/2017'],'outdoor_damper':['3/18/2017','3/19/2017','3/20/2017','3/21/2017'],'heating_valve':['3/22/2017','3/23/2017','3/24/2017','3/25/2017','3/26/2017'],'normal':['4/1/2017']},'SZVAV':{'cooling_valve':['9/11/2017','9/22/2017'],'outdoor_damper':['9/18/2017','9/19/2017'],'heating_valve':['9/12/2017','9/14/2017','9/15/2017'],'normal':['9/20/2017','9/21/2017','9/23/2017','9/24/2017']}}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def save(path,x):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')

def prepare(data_dir):
    """Whole days split first per mode/class for development; no adjacent-window split."""
    cases=[];sources=[]
    for mode in ('SZCAV','SZVAV'):
        path=Path(data_dir)/(mode+'.csv');raw=path.read_bytes();sources.append(dict(file=path.name,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)))
        rows=[{k.strip():v for k,v in r.items()} for r in csv.DictReader(raw.decode().splitlines())]
        days=sorted({r['Datetime'].split()[0] for r in rows},key=lambda x:datetime.strptime(x,'%m/%d/%Y'))
        for date in days:
            label=next(k for k,v in DATES[mode].items() if date in v)
            split='development' if date==DATES[mode][label][0] else 'evaluation'
            run_id='run%02d'%len({c['run_id'] for c in cases})
            day=[r for r in rows if r['Datetime'].split()[0]==date]
            assert all(int(r['Fault Detection Ground Truth'])==int(label!='normal') for r in day)
            for j,hour in enumerate((10,12,14)):
                window=[r for r in day if int(r['Datetime'].split()[1].split(':')[0])==hour]
                assert len(window)==60,(mode,date,hour,len(window))
                signals={};stats={}
                for short,long in FIELDS.items():
                    values=[float(r['AHU: '+long]) for r in window]
                    assert all(math.isfinite(v) for v in values)
                    signals[short]=values;stats[short]=[round(sum(values)/60,3),min(values),max(values),round(values[-1]-values[0],3)]
                public=dict(equipment_mode=mode,window_start='%02d:00'%hour,window_end='%02d:59'%hour,sample_interval_minutes=1,n_samples=60,
                    units='sat/heat_sp/cool_sp/outdoor/mixed/return: degrees F; fan/damper/cool_valve/heat_valve: fractional control signals',
                    statistic_order=['mean','min','max','last_minus_first'],readings=stats)
                cases.append(dict(case_id=run_id+'_w'+str(j),run_id=run_id,source_mode=mode,source_date=date,source_label=label,split=split,public=public,signals=signals))
    return cases,sources

def parse(text):
    try:
        x=json.loads(text.strip());d=x['diagnosis'];assert d in LABELS+('abstain',);return d
    except (ValueError,KeyError,AssertionError,TypeError):return 'invalid'

def fit(cases,records):
    """Signed expected accuracy gain includes reviewer harm; development labels only."""
    assert cases and all(c['split']=='development' for c in cases)
    data=[]
    for c in cases:
        p=parse(records[c['case_id']]['proposal']);r=parse(records[c['case_id']]['review'])
        data.append(dict(proposal=p,error=p!=c['source_label'],gain=int(r==c['source_label'])-int(p==c['source_label'])))
    def estimate(xs):return dict(n=len(xs),errors=sum(x['error'] for x in xs),net_corrected=sum(x['gain'] for x in xs),risk=(sum(x['error'] for x in xs)+1)/(len(xs)+2),gain=sum(x['gain'] for x in xs)/(len(xs)+2))
    pooled=estimate(data);bins={}
    for label in LABELS+('abstain','invalid'):
        xs=[x for x in data if x['proposal']==label];e=estimate(xs);e['fallback']=len(xs)<6
        e['prediction']=dict(risk=pooled['risk'],gain=pooled['gain']) if e['fallback'] else dict(risk=e['risk'],gain=e['gain']);bins[label]=e
    result=dict(pooled=pooled,bins=bins,development_cases=[c['case_id'] for c in cases],smoothing='risk Beta(1,1); signed gain numerator corrections minus harms, denominator n+2; bins n<6 pooled')
    result['sha256']=digest(result);return result

@dataclass(frozen=True)
class PublicRequest:
    request_id:str
    agent_id:int
    arrival:int
    cutoff:int
    duration:int
    weight:float
    risk:float
    gain:float
    @property
    def tie(self):return self.arrival,self.agent_id,self.request_id
    def benefit(self,finish):return self.weight*self.gain if finish<=self.cutoff else 0.0

def choose(policy,requests,tick,other_finishes=()):
    assert policy in POLICIES and len(requests)<=3 and all(type(r) is PublicRequest for r in requests)
    assert all(r.arrival<=tick for r in requests)
    start=time.perf_counter();eligible=sorted([r for r in requests if r.benefit(tick+r.duration)>0],key=lambda r:r.tie)
    choice=None;effort=0
    if eligible and policy!='no_review':
        if policy=='fcfs':choice=eligible[0]
        elif policy=='edf':choice=min(eligible,key=lambda r:(r.cutoff,r.tie))
        elif policy=='uncertainty':choice=min(eligible,key=lambda r:(-r.risk,r.tie))
        elif policy=='greedy':choice=min(eligible,key=lambda r:(-r.benefit(tick+r.duration),r.tie))
        else:
            best=(0,0,());effort=1
            for n in range(1,len(eligible)+1):
                for order in permutations(eligible,n):
                    free=[tick]+list(other_finishes);values=[]
                    for r in order:
                        k=min(range(len(free)),key=lambda i:(free[i],i));free[k]+=r.duration;values.append(r.benefit(free[k]))
                    key=(-math.fsum(values),n,tuple(r.tie for r in order));effort+=1
                    if key<best:best=key;choice=order[0]
    return (choice.request_id if choice else None),dict(tick=tick,public_requests=[asdict(r) for r in requests],eligible=[r.request_id for r in eligible],chosen=choice.request_id if choice else None,planning_seconds=time.perf_counter()-start,subsets=effort)

def simulate(cases,records,estimator,policy,duration,capacity,reviewer,weights='heterogeneous'):
    assert len(cases)==3 and len({c['run_id'] for c in cases})==1
    run=cases[0]['run_id'];rng=random.Random(7000+int(run[3:]));cutoffs=[2,4,6];costs=[4,8,12];rng.shuffle(cutoffs);rng.shuffle(costs)
    proposals={c['case_id']:parse(records[c['case_id']]['proposal']) for c in cases}
    # All windows are retrospective diagnostic tickets available after 14:59.
    # Dates and labels stay in evaluator state. Scheduling ticks are abstract.
    pending={};final=dict(proposals);active=[];events=[];done=set();reviewed=[];waiting=0
    for i,c in enumerate(cases):
        p=estimator['bins'][proposals[c['case_id']]]['prediction']
        pending[c['case_id']]=PublicRequest(c['case_id'],i,0,cutoffs[i],duration,8 if weights=='uniform' else costs[i],p['risk'],p['gain'] if reviewer=='model' else p['risk'])
    allreq=dict(pending)
    for tick in range(7):
        for finish,key,started in list(active):
            if finish==tick:
                c=next(c for c in cases if c['case_id']==key)
                new=c['source_label'] if reviewer=='ideal' else parse(records[key]['review'])
                if new=='invalid':new=final[key] # failed review preserves proposal
                final[key]=new;done.add(key);reviewed.append(key);active.remove((finish,key,started))
                events.append(dict(event='review_completed',tick=tick,case_id=key,diagnosis=new))
        for key,r in allreq.items():
            if r.cutoff==tick and key not in done:
                done.add(key);pending.pop(key,None);events.append(dict(event='cutoff',tick=tick,case_id=key,diagnosis=final[key]))
        for _ in range(capacity-len(active)):
            public=list(pending.values());other=[x[0] for x in active]+[tick]*(capacity-len(active)-1)
            selected,record=choose(policy,public,tick,other)
            record.update(event='dispatch');events.append(record)
            if selected:
                r=pending.pop(selected);active.append((tick+duration,selected,tick));waiting+=tick
                events.append(dict(event='review_started',tick=tick,case_id=selected,finish=tick+duration))
    assert not active and len(done)==3
    jobs=[]
    for c in cases:
        key=c['case_id'];initial=proposals[key]==c['source_label'];correct=final[key]==c['source_label']
        jobs.append(dict(case_id=key,initial_correct=initial,correct=correct,reviewed=key in reviewed,correction=not initial and correct,harm=initial and not correct,
            unresolved=not correct,abstained=final[key]=='abstain',preparation_failure=proposals[key]=='invalid',final_diagnosis=final[key],weight=allreq[key].weight,cutoff=allreq[key].cutoff))
    return dict(run_id=run,policy=policy,duration=duration,capacity=capacity,reviewer=reviewer,weights=weights,loss=sum(j['weight'] for j in jobs if not j['correct']),
        correct=sum(j['correct'] for j in jobs),corrections=sum(j['correction'] for j in jobs),harmful_reviews=sum(j['harm'] for j in jobs),unresolved=sum(j['unresolved'] for j in jobs),
        completed_reviews=len(reviewed),review_time=len(reviewed)*duration,waiting_time=waiting,missed_useful=sum(not j['reviewed'] and not j['initial_correct'] and (reviewer=='ideal' or parse(records[j['case_id']]['review'])==next(c['source_label'] for c in cases if c['case_id']==j['case_id'])) for j in jobs),
        sequence=reviewed,jobs=jobs,events=events)

def without_timing(x):
    x=copy.deepcopy(x)
    for e in x['events']:e.pop('planning_seconds',None)
    return x
