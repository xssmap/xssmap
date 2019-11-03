import re
from network import Network


class Package:
    def __init__(self, content, ssl):
        self.content = content
        self.ssl = ssl
        self.url = None
        self.cookies = None
        self.headers = {}
        self.data = None
        self.left = 0
        self.right = 0

    def setcontent(self, content):
        self.content = content

    def setssl(self, ssl):
        self.ssl = ssl

    def process(self):
        self.cookies = None
        self.headers = {}
        self.data = None
        result = re.findall('Cookie: (.*?)\n', self.content, flags=re.DOTALL + re.MULTILINE)
        if result.__len__() > 0:
            self.cookies = result[0]
        position = self.content.find('\n\n')
        if position > 0:
            self.data = self.content[position + 2:]
        result = re.findall('\n(.*?)\n\n', self.content, flags=re.DOTALL + re.MULTILINE)
        if result.__len__() > 0:
            self.headers = self.headers
        result = re.findall('Host: (.*?)\n', self.content, flags=re.DOTALL + re.MULTILINE)
        if result.__len__() > 0:
            if self.ssl == 1:
                self.url = "https://" + result[0]
            else:
                self.url = "http://" + result[0]
        result = re.findall('POST (.*?) HTTP/1.1', self.content, flags=re.DOTALL + re.MULTILINE)
        if result.__len__() > 0:
            self.url += result[0]
        else:
            result = re.findall('GET (.*?) HTTP/1.1', self.content, flags=re.DOTALL + re.MULTILINE)
            if result.__len__() > 0:
                self.url += result[0]
        result = re.findall('\n(.*?)\n\n', self.content, flags=re.DOTALL + re.MULTILINE)
        result[0] += '\n'
        if result.__len__() > 0:
            i = 0
            while True:
                key = ''
                value = ''
                while result[0][i] != ':':
                    key += result[0][i]
                    i += 1
                i += 2
                while result[0][i] != '\n':
                    value += result[0][i]
                    i += 1
                i += 1
                self.headers.update({key: value})
                if i == result[0].__len__():
                    break
        if self.content[0] == 'P':
            network = Network(self.url, self.data, 'post', self.headers)
            return network.send()
        if self.content[0] == 'G':
            network = Network(self.url, self.data, 'get', self.headers)
            return network.send()


