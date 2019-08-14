import requests
import urllib3


class Network:
    def __init__(self, url, data, method, headers):
        self.url = url
        self.data = data
        self.method = method
        self.headers = headers
        self.r = None

    def send(self):
        urllib3.disable_warnings()
        if self.method == 'get':
            self.r = requests.get(url=self.url, headers=self.headers, verify=False)
        else:
            self.r = requests.post(url=self.url, data=self.data, headers=self.headers, verify=False)


