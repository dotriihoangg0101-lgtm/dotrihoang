import unittest
from security_behavior_checker import SecurityBehaviorChecker
class TestSecurityBehaviorChecker(unittest.TestCase):
    def test_suspicious_calls(self):
        self.assertIsInstance(SecurityBehaviorChecker().suspicious_calls(), list)
