# coding=utf-8
import tkinter
from tkinter import ttk

class Gui:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("xssmap")
        self.height = 800
        self.width = 1024
        self.window.geometry("%dx%d+%d+%d" % (self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2, (self.window.winfo_screenheight() - self.height) / 2))
        self.window.resizable(width=False, height=False)
        self.setframe1()
        self.setframe2()
        self.setframe3()
        self.setframe4()
        self.window.mainloop()

    def setframe1(self):
        frame = tkinter.Frame(self.window, height=350)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        label = tkinter.Label(frame, text="XSS输入点")
        label.pack()
        text = tkinter.Text(frame)
        text.pack(fill=tkinter.X)

    def setframe2(self):
        frame = tkinter.Frame(self.window, height=50)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        frame1 = tkinter.Frame(frame)
        frame1.pack(side=tkinter.LEFT)
        frame2 = tkinter.Frame(frame)
        frame2.pack(side=tkinter.RIGHT)
        button = tkinter.Button(frame1, text="标记参数")
        button.pack(ipadx=200)
        button2 = tkinter.Button(frame2, text="清除标记")
        button2.pack(ipadx=200)

    def setframe3(self):
        frame = tkinter.Frame(self.window, height=350)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        label = tkinter.Label(frame, text="XSS输出点")
        label.pack()
        text = tkinter.Text(frame)
        text.pack(fill=tkinter.X)

    def setframe4(self):
        frame = tkinter.Frame(self.window, height=50)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        frame1 = tkinter.Frame(frame, height=50, width=512)
        frame1.pack(side=tkinter.LEFT)
        frame1.pack_propagate(0)
        frame2 = tkinter.Frame(frame, height=50, width=512)
        frame2.pack(side=tkinter.RIGHT)
        frame2.pack_propagate(0)
        label = tkinter.Label(frame1, text="线程数")
        label.pack(side=tkinter.LEFT, padx=80)
        combobox = ttk.Combobox(frame1)
        combobox.pack(side=tkinter.LEFT)
        button = tkinter.Button(frame2, text="开始")
        button.pack(side=tkinter.LEFT, ipadx=300)

gui = Gui()


