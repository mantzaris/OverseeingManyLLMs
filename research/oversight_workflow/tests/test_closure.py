import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from research.oversight_workflow.common import write
from research.oversight_workflow import transport

class ClosureTests(unittest.TestCase):
    def test_closed_stage_refuses_new_generation_before_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            write(Path(tmp)/'resource_ledger.json',{'final':True})
            with patch.object(transport,'ART',Path(tmp)),patch.object(transport.client,'generate') as generate:
                with self.assertRaisesRegex(RuntimeError,'stage is closed'):transport.generate('fresh',[],0)
                generate.assert_not_called()
