import re
from payload import Payload
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

    def process(self):
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
        payload = Payload()
        if self.content[0] == 'G':
            self.left = self.content.find('$')
            self.right = self.content.rfind('$')
        else:
            self.left = self.data.find('$')
            self.right = self.data.rfind('$')
        for item in payload.payloads:
            if self.content[0] == 'P':
                network = Network(self.url, self.data.replace(self.data[self.left:self.right + 1], item), 'post', self.headers)
            else:
                network = Network(self.url, self.data.replace(self.data[self.left:self.right + 1], item), 'get', self.headers)
            network.send()


package = Package('''GET /data/2    .4.1.$6$/version.xml HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1;Miser Report)
Host: miserupdate.aliyun.com
Pragma: no-cache
Connection: close

''', 1)
package.process()


