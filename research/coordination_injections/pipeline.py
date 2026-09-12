"""Zero-inference parameterized pipeline and controlled synthetic agent."""
from .contracts import contract,unit,DEPENDENCIES

def exact_tool_call(role,c):
 if role in ['analysis','appendix']:return dict(status='replace',query={k:v for k,v in c.items() if k!='scope'},notify=[r for r,ds in DEPENDENCIES.items() if role in ds])
 if role=='chart':return dict(status='replace',view=dict(source='analysis',limit=c['display_n'],unit=unit(c)),title='Ranked stock codes',notify=['report'])
 return dict(status='replace',summary=dict(source='chart',unit=unit(c)),text='Recorded aggregate under the applicable reporting convention.',notify=[])
def deterministic_call(key,role,project,epoch,old,upstream,issues,seed,style,delivery):
 return exact_tool_call(role,contract(project,role,epoch)),dict(call_id=key,status='deterministic_tool',request_sha256=None,attempts=0,tokens=0,seconds=0.)
def pipeline(project,rep,initial=None):
 from .controller import run
 out=run(project,rep,'shared_state',initial,generate_fn=deterministic_call,phase='pipeline',round_limit=1)
 out['method']='pipeline';out['tool_invocations']=len(out['calls']);out['calls']=[]
 return out
