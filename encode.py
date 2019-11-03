# coding=utf-8
import base64
import urllib
import cgi


class Encode:
    def __init__(self, payload):
        self.payload = payload
        self.capsencode()

    def capsencode(self):
        flag = 0
        for i in range(0, len(self.payload)):
            if self.payload[i] == '=':
                if flag == 1:
                    break
                else:
                    flag = 1
                    if self.payload[0] == '"':
                        break
            if 'a' < self.payload[i] < 'z' and i % 2 == 0:
                self.payload = self.payload[0: i] + chr(ord(self.payload[i]) - 32) + self.payload[i + 1:]

    def base64encode(self):
        return base64.b32encode(self.payload)

    def unicodeencode(self):
        s = ""
        for c in self.payload:
            if c == '<':
                s += '\u003c'
            elif c == '>':
                s += '\u003e'
            elif c == '"':
                s += '\u0022'
            else:
                s += c
        return s

    def urlencode(self):
        return urllib.quote(self.payload)

    def doubleencode(self):
        s = urllib.quote(self.payload)
        ss = ''
        for i in range(0, s.__len__()):
            if s[i] == '%':
                ss += '%25'
            else:
                ss += s[i]
        return ss

    def htmlencode(self):
        print cgi.escape(self.payload, quote=1)


