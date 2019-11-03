# coding=utf-8
import tkinter
from tkinter import messagebox
import ctypes
from payload import Payload
import thread
from package import Package
from tkinter import ttk
from encode import Encode
import time


class Gui:
    def __init__(self):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        self.window = tkinter.Tk()
        self.window.title("xssmap")
        self.height = 800
        self.width = 1024
        self.window.geometry("%dx%d+%d+%d" % (self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2, (self.window.winfo_screenheight() - self.height) / 2))
        self.window.resizable(width=False, height=False)
        self.window.iconbitmap("xssmap.ico")
        self.text1 = None
        self.text2 = None
        self.text3 = None
        self.button1 = None
        self.button2 = None
        self.button3 = None
        self.finish = False
        self.p = None
        self.combobox = None
        self.source = None
        self.dist = None
        self.index1 = 0
        self.index2 = 0
        self.ssl = 0
        self.payload = Payload()
        self.package = Package('', 0)
        self.encode = Encode()
        self.setframe1()
        self.setframe2()
        self.setframe3()
        self.setframe4()
        self.setframe5()

    def setflag(self):
        try:
            self.text1.tag_configure('red', foreground='#DC143C')
            self.text1.insert(tkinter.SEL_FIRST, "$", 'red')
            self.text1.insert(tkinter.SEL_LAST, "$", 'red')
            self.button1['state'] = tkinter.DISABLED
        except tkinter.TclError:
            messagebox.showerror("提示", "请选中标记参数")

    def unsetflag(self):
        content = self.text1.get("0.0", "end").strip('\n')
        self.text1.delete("0.0", "end")
        self.text1.insert("0.0", content.replace('$', ''))
        self.button1['state'] = tkinter.NORMAL
        self.text1.see(1000.0)

    def valid(self):
        data = self.source[0: self.index1] + 'jimmywhite' + self.source[self.index2 + 1:]
        self.package.setcontent(data)
        self.package.setssl(self.ssl)
        self.package.process()
        self.package.setcontent(self.dist)
        result = self.package.process()
        if result.find('jimmywhite') > 0:
            return True
        return False

    def typeone(self):
        content = self.source[0: self.index1] + '<jimmywhite>' + self.source[self.index2 + 1:]
        self.package.setcontent(content)
        self.package.process()
        self.package.setcontent(self.dist)
        content = self.package.process()
        index = 0
        while content.find('<jimmywhite>', index + 2) > 0:
            index = content.find('<jimmywhite>', index + 2)
            if content[index - 1] != '"':
                return True
        content = self.source[0: self.index1] + self.encode.urlencode('<jimmywhite>') + self.source[self.index2 + 1:]
        self.package.setcontent(content)
        self.package.process()
        self.package.setcontent(self.dist)
        content = self.package.process()
        index = 0
        while content.find('<jimmywhite>', index + 2) > 0:
            index = content.find('<jimmywhite>', index + 2)
            if content[index - 1] != '"':
                return True
        content = self.source[0: self.index1] + self.encode.unicodeencode('<jimmywhite>') + self.source[self.index2 + 1:]
        self.package.setcontent(content)
        self.package.process()
        self.package.setcontent(self.dist)
        content = self.package.process()
        index = 0
        while content.find('<jimmywhite>', index + 2) > 0:
            index = content.find('<jimmywhite>', index + 2)
            if content[index - 1] != '"':
                return True
        content = self.source[0: self.index1] + self.encode.htmlencode('<jimmywhite>') + self.source[self.index2 + 1:]
        self.package.setcontent(content)
        self.package.process()
        self.package.setcontent(self.dist)
        content = self.package.process()
        index = 0
        while content.find('<jimmywhite>', index + 2) > 0:
            index = content.find('<jimmywhite>', index + 2)
            if content[index - 1] != '"':
                return True
        content = self.source[0: self.index1] + self.encode.doubleencode('<jimmywhite>') + self.source[self.index2 + 1:]
        self.package.setcontent(content)
        self.package.process()
        self.package.setcontent(self.dist)
        content = self.package.process()
        index = 0
        while content.find('<jimmywhite>', index + 2) > 0:
            index = content.find('<jimmywhite>', index + 2)
            if content[index - 1] != '"':
                return True
        content = self.source[0: self.index1] + self.encode.base64encode('<jimmywhite>') + self.source[self.index2 + 1:]
        self.package.setcontent(content)
        self.package.process()
        self.package.setcontent(self.dist)
        content = self.package.process()
        index = 0
        while content.find('<jimmywhite>', index + 2) > 0:
            index = content.find('<jimmywhite>', index + 2)
            if content[index - 1] != '"':
                return True
        return False

    def typetwo(self):
        content = self.source[0: self.index1] + 'jimmywhite' + self.source[self.index2 + 1:]
        self.package.setcontent(content)
        self.package.process()
        self.package.setcontent(self.dist)
        content = self.package.process()
        if content.find('"jimmywhite"') > 0:
            return True
        content = self.source[0: self.index1] + self.encode.doubleencode('jimmywhite') + self.source[self.index2 + 1:]
        self.package.setcontent(content)
        self.package.process()
        self.package.setcontent(self.dist)
        content = self.package.process()
        if content.find('"jimmywhite"') > 0:
            return True
        content = self.source[0: self.index1] + self.encode.base64encode('jimmywhite') + self.source[self.index2 + 1:]
        self.package.setcontent(content)
        self.package.process()
        self.package.setcontent(self.dist)
        content = self.package.process()
        if content.find('"jimmywhite"') > 0:
            return True
        content = self.source[0: self.index1] + self.encode.htmlencode('jimmywhite') + self.source[self.index2 + 1:]
        self.package.setcontent(content)
        self.package.process()
        self.package.setcontent(self.dist)
        content = self.package.process()
        if content.find('"jimmywhite"') > 0:
            return True
        content = self.source[0: self.index1] + self.encode.unicodeencode('jimmywhite') + self.source[self.index2 + 1:]
        self.package.setcontent(content)
        self.package.process()
        self.package.setcontent(self.dist)
        content = self.package.process()
        if content.find('"jimmywhite"') > 0:
            return True
        content = self.source[0: self.index1] + self.encode.urlencode('jimmywhite') + self.source[self.index2 + 1:]
        self.package.setcontent(content)
        self.package.process()
        self.package.setcontent(self.dist)
        content = self.package.process()
        if content.find('"jimmywhite"') > 0:
            return True
        return False

    def testone(self):
        for i in range(0, self.payload.payloads1.__len__()):
            content = self.source[0: self.index1] + self.payload.payloads1[i] + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            index = 0
            while content.find(self.payload.payloads1[i], index + 1) > 0:
                index = content.find(self.payload.payloads1[i], index + 1)
                if content[index - 1] != '"':
                    return self.payload.payloads1[i]
            content = self.source[0: self.index1] + self.encode.urlencode(self.payload.payloads1[i]) + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            index = 0
            while content.find(self.payload.payloads1[i], index + 1) > 0:
                index = content.find(self.payload.payloads1[i], index + 1)
                if content[index - 1] != '"':
                    return self.encode.urlencode(self.payload.payloads1[i])
            content = self.source[0: self.index1] + self.encode.unicodeencode(self.payload.payloads1[i]) + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            index = 0
            while content.find(self.payload.payloads1[i], index + 1) > 0:
                index = content.find(self.payload.payloads1[i], index + 1)
                if content[index - 1] != '"':
                    return self.encode.unicodeencode(self.payload.payloads1[i])
            content = self.source[0: self.index1] + self.encode.htmlencode(self.payload.payloads1[i]) + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            index = 0
            while content.find(self.payload.payloads1[i], index + 1) > 0:
                index = content.find(self.payload.payloads1[i], index + 1)
                if content[index - 1] != '"':
                    return self.encode.htmlencode(self.payload.payloads1[i])
            content = self.source[0: self.index1] + self.encode.base64encode(self.payload.payloads1[i]) + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            index = 0
            while content.find(self.payload.payloads1[i], index + 1) > 0:
                index = content.find(self.payload.payloads1[i], index + 1)
                if content[index - 1] != '"':
                    return self.encode.base64encode(self.payload.payloads1[i])
            content = self.source[0: self.index1] + self.encode.doubleencode(self.payload.payloads1[i]) + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            index = 0
            while content.find(self.payload.payloads1[i], index + 1) > 0:
                index = content.find(self.payload.payloads1[i], index + 1)
                if content[index - 1] != '"':
                    return self.encode.doubleencode(self.payload.payloads1[i])
            content = self.source[0: self.index1] + self.encode.capsencode(self.payload.payloads1[i]) + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            index = 0
            while content.find(self.encode.capsencode(self.payload.payloads1[i]), index + 1) > 0:
                index = content.find(self.encode.capsencode(self.payload.payloads1[i]), index + 1)
                if content[index - 1] != '"':
                    return self.encode.capsencode(self.payload.payloads1[i])
        return 'fail'

    def testtwo(self):
        for i in range(0, self.payload.payloads2.__len__()):
            content = self.source[0: self.index1] + self.payload.payloads2[i] + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            if content.find(self.payload.payloads2[i]) > 0:
                return self.payload.payloads2[i]
            content = self.source[0: self.index1] + self.encode.capsencode(self.payload.payloads2[i]) + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            if content.find(self.encode.capsencode(self.payload.payloads2[i])) > 0:
                return self.encode.capsencode(self.payload.payloads2[i])
            content = self.source[0: self.index1] + self.encode.doubleencode(self.payload.payloads2[i]) + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            if content.find(self.payload.payloads2[i]) > 0:
                return self.encode.doubleencode(self.payload.payloads2[i])
            content = self.source[0: self.index1] + self.encode.base64encode(self.payload.payloads2[i]) + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            if content.find(self.payload.payloads2[i]) > 0:
                return self.encode.base64encode(self.payload.payloads2[i])
            content = self.source[0: self.index1] + self.encode.htmlencode(self.payload.payloads2[i]) + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            if content.find(self.payload.payloads2[i]) > 0:
                return self.encode.htmlencode(self.payload.payloads2[i])
            content = self.source[0: self.index1] + self.encode.unicodeencode(self.payload.payloads2[i]) + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            if content.find(self.payload.payloads2[i]) > 0:
                return self.encode.unicodeencode(self.payload.payloads2[i])
            content = self.source[0: self.index1] + self.encode.urlencode(self.payload.payloads2[i]) + self.source[self.index2 + 1:]
            self.package.setcontent(content)
            self.package.process()
            self.package.setcontent(self.dist)
            content = self.package.process()
            if content.find(self.payload.payloads2[i]) > 0:
                return self.encode.urlencode(self.payload.payloads2[i])
        return 'fail'

    def testxss(self):
        if self.combobox.get() == 'http':
            self.ssl = 0
        else:
            self.ssl = 1
        flag = False
        self.source = self.text1.get("0.0", "end")
        self.dist = self.text2.get("0.0", "end")
        self.index1 = self.source.find('$', 0)
        self.index2 = self.source.find('$', self.index1 + 1)
        if self.valid():
            if self.typeone():
                p = self.testone()
                if p != 'fail':
                    self.p = p
                    self.text3.insert("end", "检测存在XSS!\n")
                    self.text3.insert("end", "PAYLOAD:" + self.p)
                    flag = True
            if self.typetwo() and flag is False:
                p = self.testtwo()
                if p != 'fail':
                    self.p = p
                    self.text3.insert("end", "检测存在XSS!\n")
                    self.text3.insert("end", "PAYLOAD:" + self.p)
        self.finish = True

    def show(self):
        while self.finish is False:
            pass
        tkinter.messagebox.showinfo('XSS检测成功', 'PAYLOAD:' + self.p)

    def start(self):
        self.button3['state'] = 'disabled'
        thread.start_new_thread(self.testxss, ())

    def setframe1(self):
        frame = tkinter.Frame(self.window, height=300)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        label = tkinter.Label(frame, text="XSS输入点")
        label.pack()
        self.text1 = tkinter.Text(frame)
        self.text1.pack(fill=tkinter.X)

    def setframe2(self):
        frame = tkinter.Frame(self.window, height=50)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        frame1 = tkinter.Frame(frame)
        frame1.pack(side=tkinter.LEFT)
        frame2 = tkinter.Frame(frame)
        frame2.pack(side=tkinter.RIGHT)
        self.button1 = tkinter.Button(frame1, text="标记参数", command=self.setflag, cursor="hand2")
        self.button1.pack(ipadx=200)
        self.button2 = tkinter.Button(frame2, text="清除标记", command=self.unsetflag, cursor="hand2")
        self.button2.pack(ipadx=200)

    def setframe3(self):
        frame = tkinter.Frame(self.window, height=300)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        label = tkinter.Label(frame, text="XSS输出点")
        label.pack()
        self.text2 = tkinter.Text(frame)
        self.text2.pack(fill=tkinter.X)

    def setframe4(self):
        frame = tkinter.Frame(self.window, height=100)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        label = tkinter.Label(frame, text="检测结果")
        label.pack()
        self.text3 = tkinter.Text(frame)
        self.text3.pack(fill=tkinter.X)

    def setframe5(self):
        frame = tkinter.Frame(self.window, height=50)
        frame1 = tkinter.Frame(frame, height=50)
        frame2 = tkinter.Frame(frame, height=50)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        frame1.pack(side=tkinter.LEFT)
        frame2.pack(side=tkinter.RIGHT)
        self.combobox = ttk.Combobox(frame1, state="readonly", width=5)
        self.combobox['value'] = ['http', 'https']
        self.combobox.current(0)
        self.combobox.pack(ipadx=200)
        self.button3 = tkinter.Button(frame2, text="开始", command=self.start, cursor="hand2")
        self.button3.pack(ipadx=200)
