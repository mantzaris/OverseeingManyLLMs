import unittest,copy
from .normalize import normalize
class EnvelopeTests(unittest.TestCase):
 def test_equivalent_explicit_envelope(self):
  x={'tool':'summarize','params':{'source':'chart','unit':'items'}};y=normalize(x,'report')
  self.assertEqual(y,{'status':'replace','summary':{'source':'chart','unit':'items'},'notify':[]});self.assertNotIn('status',x)
 def test_no_missing_values_are_inferred(self):
  x={'tool':'summarize','params':{'source':'chart'}};self.assertEqual(normalize(x,'report'),x)
 def test_conflicting_values_rejected(self):
  x={'tool':'summarize','params':{'source':'chart','unit':'items','summary':{'source':'chart','unit':'micro_GBP'}}};self.assertEqual(normalize(x,'report'),x)
 def test_wrong_tool_rejected(self):
  x={'tool':'aggregate','params':{'source':'chart','unit':'items'}};self.assertEqual(normalize(x,'report'),x)
 def test_wrong_values_preserved_for_guard(self):
  x={'tool':'summarize','params':{'source':'chart','unit':'wrong'}};self.assertEqual(normalize(x,'report')['summary']['unit'],'wrong')
 def test_direct_keep_unchanged(self):
  x={'status':'keep','notify':[]};self.assertEqual(normalize(x,'analysis'),x)
if __name__=='__main__':unittest.main()
