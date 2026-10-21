import unittest
from sast_tool.ast_analyzer import ASTAnalyzer
class TestASTAnalyzer(unittest.TestCase):
    def test_eval_detection(self):
        issues = ASTAnalyzer().analyze('eval("2+2")')
        self.assertTrue(any(i['type'] == 'Use of eval' for i in issues))
