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
    def testCheckEndpointOK(self):
        responses.add(responses.GET, self.DOMAIN,
                      status=200)
        self.probe.check_endpoint()
        self.assertEqual(self.probe.nagios._code, 0)

    @responses.activate
    def testCheckEndpoint404(self):
        responses.add(responses.GET, self.DOMAIN,
                      status=404)
        self.probe.check_endpoint()
        self.assertEqual(self.probe.nagios._code, 2)
        self.assertTrue("Invalid response code" in self.probe.nagios.getMsg())

    @responses.activate
    def testCheckEndpointExtension(self):
        extension = '/services'
        currentEndpoint = self.DOMAIN + extension
        responses.add(responses.GET, currentEndpoint,
                      status=200)
        self.probe.check_endpoint(extension)
        self.assertEqual(self.probe.nagios._code, 0)

    @responses.activate
    def testCheckEndpointJSON(self):
        extension = '/services'
        currentEndpoint = self.DOMAIN + extension
        responses.add(responses.GET, currentEndpoint,
                json={'service': 'http://example.com/'}, status=200)
        self.probe.check_endpoint(extension, checkJSON=True)
        self.assertEqual(self.probe.nagios._code, 0)

    @responses.activate
    def testCheckEndpointJSONEmpty(self):
        extension = '/services'
        currentEndpoint = self.DOMAIN + extension
        responses.add(responses.GET, currentEndpoint,
                json={}, status=200)
        self.probe.check_endpoint(extension, checkJSON=True)
        self.assertEqual(self.probe.nagios._code, 2)
        self.assertTrue("No services found" in self.probe.nagios.getMsg())

    @responses.activate
    def testCheckEndpointJSONMalformed(self):
        extension = '/services'
        currentEndpoint = self.DOMAIN + extension
        responses.add(responses.GET, currentEndpoint,
                status=200)
        self.probe.check_endpoint(extension, checkJSON=True)
        self.assertEqual(self.probe.nagios._code, 2)
        self.assertTrue("Malformed JSON" in self.probe.nagios.getMsg())

    @responses.activate
    def testLoginOK(self):
        args = ['-D', self.DOMAIN, '-u', 'user', '-p', 'pass']
        self.probe = AgoraHealthCheck(args)
        loginExtension = '/login'
        responses.add(responses.POST, self.DOMAIN + loginExtension,
                status=200)
        self.probe.login(loginExtension)
        self.assertEqual(self.probe.nagios._code, 0)

    @responses.activate
    def testLoginFail(self):
        args = ['-D', self.DOMAIN, '-u', 'user', '-p', 'pass']
        self.probe = AgoraHealthCheck(args)
        loginExtension = '/login'
        responses.add(responses.POST, self.DOMAIN + loginExtension,
                status=400)
        self.probe.login(loginExtension)
        self.assertEqual(self.probe.nagios._code, 2)
        self.assertTrue("Cannot login" in self.probe.nagios.getMsg())

    @responses.activate
    def testLogin404(self):
        args = ['-D', self.DOMAIN, '-u', 'user', '-p', 'pass']
        self.probe = AgoraHealthCheck(args)
        loginExtension = '/login'
        responses.add(responses.POST, self.DOMAIN + loginExtension,
                status=404)
        self.probe.login(loginExtension)
        self.assertEqual(self.probe.nagios._code, 2)
        self.assertTrue("Invalid response code" in self.probe.nagios.getMsg())


if __name__ == '__main__':
    unittest.main()
