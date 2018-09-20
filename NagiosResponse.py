class NagiosResponse(object):
    _msgBagWarning = []
    _msgBagCritical = []
    _msgBagOk = []
    _okMsg = ""
    _code = None

    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __init__(self, ok_msg=""):
        self._code = self.OK
        self._okMsg = ok_msg

    def writeOkMessage(self, msg):
        self._msgBagOk.append(msg)

    def writeWarningMessage(self, msg):
        self._msgBagWarning.append(msg)
        self._upgrade_code(self.WARNING)

    def writeCriticalMessage(self, msg):
        self._msgBagCritical.append(msg)
        self._upgrade_code(self.CRITICAL)

    def setCode(self, code):
        self._code = code

    def getMsg(self):
        if self._code == self.WARNING:
            return "WARNING - " + self._toString(self._msgBagWarning)
        elif self._code == self.CRITICAL:
            return "CRITICAL - " + self._toString(self._msgBagCritical)
        elif self._code == self.OK:
            msg = self._okMsg if self._okMsg else self._toString(self._msgBagOk)
            return "OK - " + msg
        else:
            return "UNKNOWN!"

    def printAndExit(self):
        print(self.getMsg())
        raise SystemExit(self._code)

    def _toString(self, msgArray):
        return ';\n'.join(msgArray)

    def _upgrade_code(self, code):
        if code > self._code:
            self._code = code
