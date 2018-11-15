import unittest
#from mock import mock
from agora_probes.checkhealth import AgoraHealthCheck

class AgoraHealthCheckTests(unittest.TestCase):

    def setUp(self):
        args = ['-D', 'localhost']
        self.probe = AgoraHealthCheck(args)

    def testCreation(self):
        self.assertEqual(self.probe.args.domain, 'localhost')

    def testCheckEndpoint(self):
        self.probe.check_endpoint()
        self.assertEqual(self.probe.nagios._code, 0)

if __name__ == '__main__':
    unittest.main()
