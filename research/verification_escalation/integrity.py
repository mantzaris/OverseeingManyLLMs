"""Public snapshot integrity checks for the online prototype.

Added after the frozen empirical protocol. Its uniform quarantine sensitivity is
post hoc; the historical terminal controller and its outcomes remain unchanged.
"""
import sqlite3
from .common import digest
from .online import OnlineController
from .engine import verification_key
from .controller import candidates

def check_snapshot(snapshot,budget):
 c=sqlite3.connect(':memory:')
 try:
  budget.charge();c.executescript(snapshot);c.execute('PRAGMA query_only=ON')
  quick=c.execute('PRAGMA quick_check').fetchall()
  if quick!=[('ok',)]:return dict(status='failed',reason='sqlite_integrity',details=quick)
  budget.charge();bad=c.execute('PRAGMA foreign_key_check').fetchmany(1)
  if bad:return dict(status='failed',reason='foreign_key_violation',details=bad)
  return dict(status='ok')
 except Exception as e:return dict(status='failed',reason='snapshot_or_budget_failure',details=str(e))
 finally:c.close()

class ValidatedController(OnlineController):
 def inspect(self):
  if not hasattr(self,'integrity_cache'):self.integrity_cache={}
  original=self.tasks;valid=[];blocked=[]
  for t in original:
   key=digest(t['snapshot'])
   if key not in self.integrity_cache:
    self.integrity_cache[key]=check_snapshot(t['snapshot'],self.machine)
    self.log('snapshot_integrity',snapshot_hash=key,status=self.integrity_cache[key]['status'],reason=self.integrity_cache[key].get('reason'))
   if self.integrity_cache[key]['status']=='ok':valid.append(t)
   else:blocked.append(t)
  self.tasks=valid
  try:pending=super().inspect()
  finally:self.tasks=original
  for t in blocked:
   self.records[t['id']]=dict(status='unfinished',reason='source_integrity_failed',key=verification_key(t,candidates(self.preparations[t['id']])[0]),version=t['version'])
  if blocked and self.method=='all_wait':
   for t in valid:
    if self.records[t['id']]['status']=='released':self.records[t['id']]['status']='unfinished';self.records[t['id']]['reason']='global_wait'
  return pending
