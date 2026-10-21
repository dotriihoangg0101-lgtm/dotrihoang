import unittest
from sast_tool.security_rule_engine import SecurityRuleEngine
class TestSecurityRuleEngine(unittest.TestCase):
    def test_evaluate(self):
        result = SecurityRuleEngine().evaluate([{'type':'Use of eval','message':'msg','lineno':1,'col_offset':0}], [{'type':'Pattern Match','message':'msg','lineno':2,'col_offset':0}])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['severity'], 'high')
