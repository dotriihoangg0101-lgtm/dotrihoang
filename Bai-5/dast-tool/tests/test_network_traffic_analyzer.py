import unittest
from network_traffic_analyzer import NetworkTrafficAnalyzer
class TestNetworkTrafficAnalyzer(unittest.TestCase):
    def test_get_network_stats(self):
        self.assertIsInstance(NetworkTrafficAnalyzer().get_network_stats(), dict)
