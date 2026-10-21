import unittest
import tempfile
import json
from pathlib import Path
from sast_tool.sarif_reporter import SarifReporter
class TestSarifReporter(unittest.TestCase):
    def test_generate_report(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'report.sarif'
            SarifReporter().generate_report([{'type':'Test','message':'Test message','lineno':1,'col_offset':0}], str(path))
            self.assertEqual(json.loads(path.read_text())['version'], '2.1.0')
