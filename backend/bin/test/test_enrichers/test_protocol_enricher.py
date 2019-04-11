import unittest

from main.enrichers.protocol_enricher import ProtocolEnricher


class TestTlsEnricherMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocols = {
            "dhcp": {"frame.protocols": "eth:ethertype:ip:udp:dhcp"},
            "http": {"frame.protocols": "eth:ethertype:ip:tcp:http"},
            "tls": {"frame.protocols": "eth:ethertype:ip:tcp:tls"},
            "stp": {"frame.protocols": "eth:llc:stp"},
            "arp": {"frame.protocols": "eth:ethertype:arp"},
            "": {"frame.protocols": ""}
        }

    def test_protocols(self):
        protocol_enricher = ProtocolEnricher()
        for protocol in self.protocols:
            self.assertEqual(protocol_enricher.get_protocol(self.protocols[protocol]), protocol)

    def test_protocols_set(self):
        protocol_enricher = ProtocolEnricher()
        for protocol in self.protocols:
            protocol_enricher.get_protocol(self.protocols[protocol])

        expected_protocols = set([protocol for protocol in self.protocols if protocol != ""])
        self.assertSetEqual(protocol_enricher.protocols, expected_protocols)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTlsEnricherMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)