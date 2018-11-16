import unittest
import responses
from agora_probes.checkhealth import AgoraHealthCheck

class AgoraHealthCheckTests(unittest.TestCase):
    DOMAIN = 'https://localhost.com'

    def setUp(self):
        args = ['-D', self.DOMAIN]
        self.probe = AgoraHealthCheck(args)

    def testCreation(self):
        self.assertEqual(self.probe.args.domain, self.DOMAIN)

    @responses.activate
    def testCheckEndpoint(self):
        responses.add(responses.GET, self.DOMAIN,
                      status=200)
        self.probe.check_endpoint()
        self.assertEqual(self.probe.nagios._code, 0)

if __name__ == '__main__':
    unittest.main()
