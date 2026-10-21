import unittest
from sast_tool.vuln_pattern_matcher import VulnPatternMatcher
class TestVulnPatternMatcher(unittest.TestCase):
    def test_password(self):
        self.assertTrue(VulnPatternMatcher().match('password = "secret"'))
    def test_pickle(self):
        self.assertTrue(VulnPatternMatcher().match('import pickle'))
