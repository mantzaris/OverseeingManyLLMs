"""Public prepared interpretations -> planner. Labels used only by fit()."""
from collections import defaultdict
from .common import ART, read, write_json, digest
from .collect import records,answers
from .data import norm
from .planner import Factor,Option,Task,OTHER,Planner

BACKENDS=['extract','memory','history']

def predictions(case,prepared,backend):
    if backend=='extract':return {k:r['value'] for k,r in records(prepared['outputs'].get('extract'),case)[0].items()}
    return answers(prepared['outputs'].get(backend))

def fit():
    cases=[c for c in read(ART/'data/public.json') if c['split']=='development']
    targets={r['id']:r['target'] for r in read(ART/'data/evaluation_only.json')};bins=defaultdict(lambda:[0,0])
    for case in cases:
        for rep in range(2):
            prep=read(ART/'prepared'/('development_'+case['id'][:-5]+'_'+str(rep)+'.json'))
            for backend in BACKENDS:
                pred=predictions(case,prep,backend)
                for k in case['fields']:
                    if k in pred:
                        b=bins[(backend,k.split('.')[0])];b[0]+=1;b[1]+=int(norm(pred[k])==norm(targets[case['id']][k]))
    result={}
    for backend in BACKENDS:
        group=[v for (b,d),v in bins.items() if b==backend];n=sum(x[0] for x in group);correct=sum(x[1] for x in group)
        pooled=(correct+1)/(n+2)
        result[backend]={'pooled':dict(n=n,correct=correct,probability=pooled),'domains':{}}
        for domain in ['hotel','restaurant','attraction']:
            nn,cc=bins[(backend,domain)];fallback=nn<10
            result[backend]['domains'][domain]=dict(n=nn,correct=cc,fallback=fallback,
                   probability=pooled if fallback else (cc+1)/(nn+2))
    estimator=dict(estimates=result,development_ids=[c['id'] for c in cases],rule='Beta(1,1) probability of a supplied normalized value being correct, by backend/domain; pooled same backend if fewer than 10 supplied fields. Missing value is unknown, not a calibrated guess.',
        limitation='Small dependent field samples; no claim of calibrated individual confidence. Factor independence across distinct fields is assumed; shared factors are not independent copies.',
        missing_prior='All probability on OTHER; public values not guessed. A paid accurate response can reveal its value.',response_model='Accurate source-label answer for requested field, no additional GPU generation in primary replay.')
    estimator['sha256']=digest(estimator);write_json(ART/'estimator.json',estimator);print(estimator)

def build(case,prepared,estimator,backend='memory',ideal=None,error_weight=4.):
    pred=predictions(case,prepared,backend) if ideal is None else dict(ideal)
    factors=[]
    for key in case['fields']:
        value=pred.get(key);domain=key.split('.')[0]
        prob=1. if ideal is not None else estimator['estimates'][backend]['domains'][domain]['probability']
        choices=(value,OTHER) if value is not None else (OTHER,)
        probabilities=(prob,1-prob) if value is not None else (1.,)
        factors.append(Factor(key,choices,probabilities,scope=case['id']+'/'+domain,
                              source='GPU '+backend+' on released source dialogue' if ideal is None else 'Diagnostic ideal annotation interpretation',
                              status='inferred' if ideal is None else 'confirmed'))
    tasks=[Task(t['id'],(Option(tuple((k,k) for k in t['required'])),),error_weight,t['defer_weight']) for t in case['tasks']]
    return Planner(factors,tasks)

if __name__=='__main__':fit()
