#!/usr/bin/env python

import requests
import argparse
from NagiosResponse import NagiosResponse

TIMEOUT = 180

class AgoraHealthCheck:

    SERVICES = '/api/v2/services'
    EXT_SERVICES = '/api/v2/ext-services'
    LOGIN = '/api/v2/auth/login/'
    nagios = NagiosResponse("Agora is up.")

    def __init__(self):
        parser = argparse.ArgumentParser(description="Nagios Probe for Agora")
        parser.add_argument('-H', dest='hostname', required=True, type=str,
                            help='hostname')
        parser.add_argument('-t', dest='timeout', type=int, default=TIMEOUT,
                            help='timeout for requests, default=' + str(TIMEOUT))
        parser.add_argument('-u', dest='username', type=str, help='username')
        parser.add_argument('-p', dest='password', type=str, help='password')
        parser.add_argument('-i', '--insecure', dest='ignore_ssl',
                            action='store_true', default=False,
                            help='ignore SSL errors')

        self.opts = parser.parse_args()
        self.verify_ssl = not self.opts.ignore_ssl

    def check_endpoint(self, endpoint, timeout=TIMEOUT):
        try:
            r = requests.get(endpoint, verify=self.verify_ssl)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            code = e.response.status_code
            if code in [400, 401]:
                self.nagios.writeCriticalMessage("Invalid credentials")
            else:
                self.nagios.writeCriticalMessage("Invalid response code: " + str(code))
        except requests.exceptions.SSLError as e:
            self.nagios.writeCriticalMessage("SSL Error.")
        except requests.exceptions.RequestException as e:
            self.nagios.writeCriticalMessage("Cannot connect to endpoint " + endpoint)

    def login(self):
        try:
            payload = {
                        'username': self.opts.username,
                        'password': self.opts.password,
                        }
            r = requests.post(self.opts.hostname + self.LOGIN, data=payload, verify=self.verify_ssl)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            code = e.response.status_code
            self.nagios.writeCriticalMessage("Invalid response code: " + str(code))
        except requests.exceptions.RequestException as e:
            self.nagios.writeCriticalMessage("Cannot connect to endpoint " + endpoint)

    def run(self):
        self.check_endpoint(self.opts.hostname, self.opts.timeout)
        self.check_endpoint(self.opts.hostname + self.SERVICES, self.opts.timeout)
        self.check_endpoint(self.opts.hostname + self.EXT_SERVICES, self.opts.timeout)

        if self.opts.username and self.opts.password:
            self.login()

        self.nagios.printAndExit()


if __name__ == "__main__":
    check = AgoraHealthCheck()
    check.run()
