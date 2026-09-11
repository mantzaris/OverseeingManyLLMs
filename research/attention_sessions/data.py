"""Adapt public evidence; keep evaluator labels and saved responses separate."""
import json,hashlib,random
from pathlib import Path
from dataclasses import asdict,replace
from .method import Request,Settings

HIST=Path('artifacts/stage7_empirical')
ROOT=Path('artifacts/attention_sessions')

def load(split='evaluation'):
    cases=[c for c in json.loads((HIST/'cases.json').read_text()) if c['split']==split]
    estimator=json.loads((HIST/'estimator.json').read_text())
    records={};folder='development_revision1' if split=='development' else 'evaluation'
    for c in cases:
        p=HIST/folder/(c['case_id']+'.json')
        records[c['case_id']]=json.loads(p.read_text()) if p.exists() else {'proposal':'','review':'','missing':True}
    return cases,records,estimator

def parse(text):
    from overseeing.hvac import parse as historical_parse
    return historical_parse(text)

def bundles(cases):
    days=sorted({c['run_id'] for c in cases})
    return [days[i:i+3] for i in range(0,len(days),3)]

def workload(days,cases,records,estimator,condition):
    selected=[c for c in cases if c['run_id'] in days];public=[];private={}
    for j,day in enumerate(days):
        group=sorted([c for c in selected if c['run_id']==day],key=lambda c:c['case_id'])
        rng=random.Random(81000+int(day[3:]));windows=[4,7,10];weights=[4,8,12];rng.shuffle(windows);rng.shuffle(weights)
        for i,c in enumerate(group):
            proposal=parse(records[c['case_id']]['proposal']);review=parse(records[c['case_id']]['review']);pred=estimator['bins'][proposal]['prediction']
            # At each wave all contexts release one retrospective ticket.
            arrival=float(i*(10 if condition['load']=='low' else 1))
            canonical=day if condition.get('contexts','related')!='unrelated' else c['case_id']
            suggestion=canonical
            if condition.get('contexts')=='imperfect' and i==1:suggestion=days[(j+1)%len(days)]
            request=Request(c['case_id'],canonical,suggestion,arrival,arrival+windows[i],weights[i],pred['risk'],
                pred['gain'] if condition['reviewer']=='model' else pred['risk'],proposal,c['public'])
            public.append(request)
            private[c['case_id']]=dict(truth=c['source_label'],review=review,proposal=proposal,missing=records[c['case_id']].get('missing',False))
    return sorted(public,key=lambda r:r.tie),private

def response(private,reviewer,key):
    return private[key]['truth'] if reviewer=='ideal' else private[key]['review']

def settings(condition):
    return Settings(setup=condition['setup'],switch=0 if condition['setup']==0 else .25,
                    budget=condition['budget'],decision=condition.get('decision',1),coordination=condition.get('coordination',.25),
                    reuse=condition.get('reuse',True),max_group=condition.get('max_group',3),reconsider=condition.get('reconsider',True))

def conditions():
    import itertools
    result=[]
    for load,setup,budget,reviewer in itertools.product(('low','high'),(0,.25,1),(6,12,24),('ideal','model','model_risk')):
        result.append(dict(condition_id='core_%s_%s_%s_%s'%(load,setup,budget,reviewer),study='core',load=load,setup=setup,budget=budget,reviewer=reviewer,contexts='related'))
    base=dict(study='sensitivity',load='high',setup=1,budget=12,contexts='related')
    variants={'unrelated':dict(contexts='unrelated'),'imperfect':dict(contexts='imperfect'),'no_reuse':dict(reuse=False),
              'complex_groups':dict(coordination=1),'slow_decisions':dict(decision=2),'singleton':dict(max_group=1),'no_reconsider':dict(reconsider=False)}
    for reviewer in ('ideal','model','model_risk'):
        for name,changes in variants.items():result.append(dict(base,condition_id=name+'_'+reviewer,reviewer=reviewer,**changes) if 'contexts' not in changes else dict(dict(base,**changes),condition_id=name+'_'+reviewer,reviewer=reviewer))
    return result

def save_json(path,x):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
