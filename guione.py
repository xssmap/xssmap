# coding=utf-8
import tkinter
from tkinter import ttk
import tkinter.font
import ctypes
from tkinter import scrolledtext
from crawler import Crawler
import thread


class GuiOne:
    def __init__(self):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        self.window = tkinter.Tk()
        self.window2 = None
        self.window.title("xssmap")
        self.height = 800
        self.width = 1024
        self.window.geometry("%dx%d+%d+%d" % (self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2,
                                              (self.window.winfo_screenheight() - self.height) / 2))
        self.window.resizable(width=False, height=False)
        self.window.iconbitmap("xssmap.ico")
        self.font = tkinter.font.Font(size=12)
        self.font2 = tkinter.font.Font(size=10)
        self.font3 = tkinter.font.Font(size=15)
        self.entry = None
        self.text = None
        self.text2 = None
        self.text3 = None
        self.header = None
        self.combobox = None
        self.combobox2 = None
        self.combobox3 = None
        self.headerflag = False
        self.button2 = None
        self.crawler = None
        self.setframe1()
        self.setframe2()
        self.setframe3()

    def start2(self):
        domain = self.entry.get()
        threads = int(self.combobox.get())
        depth = int(self.combobox2.get())
        times = int(self.combobox3.get())
        headers = ""
        if self.headerflag is True:
            headers = self.header
        self.button2['text'] = "开始"
        self.button2['state'] = "disabled"
        self.crawler = Crawler(domain, threads, depth, times, headers, self)
        self.crawler.stepone()

    def start(self):
        thread.start_new_thread(self.start2, ())

    def getheader(self):
        self.header = self.text.get("0.0", "end")
        self.headerflag = True
        self.window2.withdraw()

    def delheader(self):
        self.headerflag = False
        self.window2.withdraw()

    def setheader(self):
        self.window2 = tkinter.Tk()
        self.window2.title("自定义首部")
        self.window2.height = 500
        self.window2.width = 600
        self.window2.geometry("%dx%d+%d+%d" % (self.window2.width, self.window2.height, (self.window2.winfo_screenwidth() - self.window2.width) / 2, (self.window2.winfo_screenheight() - self.window2.height) / 2))
        self.window2.resizable(width=False, height=False)
        frame = tkinter.Frame(self.window2, height=480)
        frame.pack(fill=tkinter.X)
        self.text = tkinter.Text(frame)
        self.text.pack(fill=tkinter.Y)
        frame2 = tkinter.Frame(self.window2, height=20)
        frame2.pack(fill=tkinter.X)
        frame3 = tkinter.Frame(frame2, height=20)
        frame3.pack(side=tkinter.LEFT)
        frame4 = tkinter.Frame(frame2, height=20)
        frame4.pack(side=tkinter.RIGHT)
        button = tkinter.Button(frame3, text="确定", font=self.font3, cursor="hand2", command=self.getheader)
        button.pack(pady=30, ipadx=120)
        button2 = tkinter.Button(frame4, text="取消", font=self.font3, cursor="hand2", command=self.delheader)
        button2.pack(pady=30, ipadx=120)

    def setframe1(self):
        frame = tkinter.Frame(self.window, height=80)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        frame1 = tkinter.Frame(frame)
        frame1.pack(side=tkinter.LEFT)
        frame2 = tkinter.Frame(frame)
        frame2.pack(side=tkinter.LEFT)
        frame3 = tkinter.Frame(frame)
        frame3.pack(side=tkinter.LEFT)
        frame4 = tkinter.Frame(frame)
        frame4.pack(side=tkinter.LEFT)
        frame5 = tkinter.Frame(frame)
        frame5.pack(side=tkinter.LEFT)
        frame6 = tkinter.Frame(frame)
        frame6.pack(side=tkinter.LEFT)
        frame7 = tkinter.Frame(frame)
        frame7.pack(side=tkinter.LEFT)
        frame8 = tkinter.Frame(frame)
        frame8.pack(side=tkinter.LEFT)
        frame9 = tkinter.Frame(frame)
        frame9.pack(side=tkinter.LEFT)
        frame10 = tkinter.Frame(frame)
        frame10.pack(side=tkinter.LEFT)
        threads = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        depth = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
        times = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        label = tkinter.Label(frame1, text="域名", font=self.font)
        label.pack(ipadx=10)
        self.entry = tkinter.Entry(frame2)
        self.entry.pack(ipadx=80)
        label2 = tkinter.Label(frame3, text="线程", font=self.font)
        label2.pack(ipadx=10)
        self.combobox = ttk.Combobox(frame4, state="readonly", width=5)
        self.combobox['value'] = threads
        self.combobox.current(9)
        self.combobox.pack()
        label3 = tkinter.Label(frame5, text="深度", font=self.font)
        label3.pack(ipadx=10)
        self.combobox2 = ttk.Combobox(frame6, state="readonly", width=5)
        self.combobox2['value'] = depth
        self.combobox2.current(4)
        self.combobox2.pack()
        label4 = tkinter.Label(frame7, text="超时", font=self.font)
        label4.pack(ipadx=10)
        self.combobox3 = ttk.Combobox(frame8, state="readonly", width=5)
        self.combobox3['value'] = times
        self.combobox3.current(5)
        self.combobox3.pack()
        button = tkinter.Button(frame9, text="首部", font=self.font2, cursor="hand2", command=self.setheader)
        button.pack(ipadx=15, padx=10)
        self.button2 = tkinter.Button(frame10, text="开始", font=self.font2, cursor="hand2", command=self.start)
        self.button2.pack(ipadx=15, padx=5)

    def setframe2(self):
        frame = tkinter.Frame(self.window, height=360)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        label = tkinter.Label(frame, text="待检测的URL")
        label.pack()
        self.text2 = scrolledtext.ScrolledText(frame)
        self.text2.pack(fill=tkinter.X)

    def setframe3(self):
        frame = tkinter.Frame(self.window, height=360)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        label = tkinter.Label(frame, text="存在XSS的URL")
        label.pack()
        self.text3 = scrolledtext.ScrolledText(frame)
        self.text3.pack(fill=tkinter.X)

