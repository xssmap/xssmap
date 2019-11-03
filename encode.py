# coding=utf-8
import base64
import urllib
import cgi


class Encode:
    def __init__(self):
        pass

    @staticmethod
    def capsencode(payload):
        flag = 0
        for i in range(0, len(payload)):
            if payload[i] == '=':
                if flag == 1:
                    break
                else:
                    flag = 1
                    if payload[0] == '"':
                        break
            if 'a' < payload[i] < 'z' and i % 2 == 0:
                payload = payload[0: i] + chr(ord(payload[i]) - 32) + payload[i + 1:]
        return payload

    @staticmethod
    def base64encode(payload):
        return base64.b32encode(payload)

    @staticmethod
    def unicodeencode(payload):
        s = ""
        for c in payload:
            if c == '<':
                s += '\u003c'
            elif c == '>':
                s += '\u003e'
            elif c == '"':
                s += '\u0022'
            else:
                s += c
        return s

    @staticmethod
    def urlencode(payload):
        return urllib.quote(payload)

    @staticmethod
    def doubleencode(payload):
        s = urllib.quote(payload)
        ss = ''
        for i in range(0, s.__len__()):
            if s[i] == '%':
                ss += '%25'
            else:
                ss += s[i]
        return ss

    @staticmethod
    def htmlencode(payload):
        return cgi.escape(payload, quote=1)


