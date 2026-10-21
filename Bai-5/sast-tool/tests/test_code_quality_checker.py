import unittest
import tempfile
from pathlib import Path
from sast_tool.code_quality_checker import CodeQualityChecker
class TestCodeQualityChecker(unittest.TestCase):
    def test_flake8_detection(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'bad.py'
            path.write_text('import os\n\n')
            self.assertTrue(any(i['type'] == 'Lint Issue' for i in CodeQualityChecker().check(str(path))))
