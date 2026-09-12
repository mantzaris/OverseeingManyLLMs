"""Validated local application entry point around the frozen experiment controller.

Authority is supplied by the trusted local application, not inferred from text.
This module is not a network identity or permission service.
"""
from .contracts import DEPENDENCIES,contract
from .controller import run,validate_graph,validate_query

def validate_project(project):
 validate_graph(project['dependencies'])
 change=project['user_change']
 if change.get('source') not in ['authorized_user','authorized_local_user']:raise PermissionError('Peer and dataset messages cannot install instructions')
 if change.get('scope')!='main' or change.get('exceptions')!=['appendix']:raise ValueError('This adapter supports main changes with a protected appendix')
 if project['before']['appendix']!=project['after']['appendix']:raise ValueError('A main-scope change must preserve the appendix exception')
 for epoch in [0,1]:
  for role in ['analysis','appendix']:
   c=contract(project,role,epoch);validate_query({k:v for k,v in c.items() if k!='scope'})
  n=project['before' if epoch==0 else 'after']['display_n']
  if type(n)!=int or not 1<=n<=5:raise ValueError('Unsupported displayed prefix')
 return project

def adapt(project,rep=0,method='targeted',initial=None,**kwargs):
 validate_project(project)
 return run(project,rep,method,initial,**kwargs)
