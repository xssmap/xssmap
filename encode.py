# coding=utf-8
import base64
import urllib
import cgi


class Encode:
    def __init__(self, payload):
        self.payload = payload

    def capsencode(self):
        pass

    def base64encode(self):
        print base64.b32encode(self.payload)

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

    def urlencode(self):
        print urllib.quote(self.payload)

    def htmlencode(self):
        print cgi.escape(self.payload, quote=1)

encode = Encode("<img src=1>")
encode.base64encode()
encode.urlencode()
encode.htmlencode()
encode.unicodeencode()

