import unittest
from agora_probes.NagiosResponse import NagiosResponse, _toString

class NagiosResponseTests(unittest.TestCase):

    def setUp(self):
        self.response = NagiosResponse()

    def testCreation(self):
        self.assertEqual(self.response._code, 0)
        self.assertEqual(self.response._okMsg, '')

        response = NagiosResponse("Everything's OK.")
        self.assertEqual(response._okMsg, "Everything's OK.")

    def testWriteOkMessage(self):
        self.response.writeOkMessage('OK OK')
        self.assertEqual(self.response._msgBagOk, ['OK OK'])
        self.response.writeOkMessage('OK')
        self.assertEqual(self.response._msgBagOk, ['OK OK', 'OK'])
        self.assertEqual(self.response._code, 0)

    def testWriteWarningMessage(self):
        self.response.writeWarningMessage('Warning')
        self.assertEqual(self.response._msgBagWarning, ['Warning'])
        self.assertEqual(self.response._code, 1)
        self.response.writeWarningMessage('Warn')
        self.assertEqual(self.response._msgBagWarning, ['Warning', 'Warn'])
        self.assertEqual(self.response._code, 1)

    def testWriteCriticalMessage(self):
        self.response.writeCriticalMessage('Critical')
        self.assertEqual(self.response._msgBagCritical, ['Critical'])
        self.assertEqual(self.response._code, 2)
        self.response.writeCriticalMessage('Crit')
        self.assertEqual(self.response._msgBagCritical, ['Critical', 'Crit'])
        self.assertEqual(self.response._code, 2)

    def testSetCode(self):
        self.response.setCode(1)
        self.assertEqual(self.response._code, 1)
        self.response.setCode(3)
        self.assertEqual(self.response._code, 3)
        self.response.setCode(15)
        self.assertEqual(self.response._code, 15)

    def testGetMsg(self):
        self.assertEqual(self.response.getMsg(), 'OK - ')
        self.response.writeWarningMessage('Warning')
        self.assertEqual(self.response.getMsg(), 'WARNING - Warning')
        self.response.writeCriticalMessage('Critical')
        self.assertEqual(self.response.getMsg(), 'CRITICAL - Critical')
        self.response.writeWarningMessage('Warning')
        self.assertEqual(self.response.getMsg(), 'CRITICAL - Critical')
        self.response.writeCriticalMessage('Crit2')
        self.assertEqual(self.response.getMsg(), 'CRITICAL - Critical;\nCrit2')
        self.response.setCode(3)
        self.assertEqual(self.response.getMsg(), 'UNKNOWN!')
        self.response.setCode(5)
        self.assertEqual(self.response.getMsg(), 'UNKNOWN!')

    def testToString(self):
        self.assertEqual(_toString([]), "")
        self.assertEqual(_toString(["Critical"]), "Critical")
        self.assertEqual(_toString(["Crit", "Crit2"]), "Crit;\nCrit2")

    def testUpgradeCode(self):
        self.response._upgradeCode(2)
        self.assertEqual(self.response._code, 2)
        self.response._upgradeCode(1)
        self.assertEqual(self.response._code, 2)


if __name__ == '__main__':
    unittest.main()
