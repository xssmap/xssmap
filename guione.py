# coding=utf-8
import tkinter
from tkinter import ttk
import tkinter.font
import ctypes
from tkinter import scrolledtext


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
        self.setframe1()
        self.setframe2()
        self.setframe3()
        self.window.mainloop()

    def setheader(self):
        self.window2 = tkinter.Tk()
        self.window2.title("自定义首部")
        self.window2.height = 500
        self.window2.width = 600
        self.window2.geometry("%dx%d+%d+%d" % (self.window2.width, self.window2.height, (self.window2.winfo_screenwidth() - self.window2.width) / 2, (self.window2.winfo_screenheight() - self.window2.height) / 2))
        self.window2.resizable(width=False, height=False)
        frame = tkinter.Frame(self.window2, height=480)
        frame.pack(fill=tkinter.X)
        text = tkinter.Text(frame)
        text.pack(fill=tkinter.Y)
        frame2 = tkinter.Frame(self.window2, height=20)
        frame2.pack(fill=tkinter.X)
        frame3 = tkinter.Frame(frame2, height=20)
        frame3.pack(side=tkinter.LEFT)
        frame4 = tkinter.Frame(frame2, height=20)
        frame4.pack(side=tkinter.RIGHT)
        button = tkinter.Button(frame3, text="确定", font=self.font3)
        button.pack(pady=30, ipadx=120)
        button2 = tkinter.Button(frame4, text="取消", font=self.font3)
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
        thread = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        depth = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
        times = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        label = tkinter.Label(frame1, text="域名", font=self.font)
        label.pack(ipadx=10)
        entry = tkinter.Entry(frame2)
        entry.pack(ipadx=80)
        label2 = tkinter.Label(frame3, text="线程", font=self.font)
        label2.pack(ipadx=10)
        combobox = ttk.Combobox(frame4, state="readonly", width=5)
        combobox['value'] = thread
        combobox.current(9)
        combobox.pack()
        label3 = tkinter.Label(frame5, text="深度", font=self.font)
        label3.pack(ipadx=10)
        combobox2 = ttk.Combobox(frame6, state="readonly", width=5)
        combobox2['value'] = depth
        combobox2.current(4)
        combobox2.pack()
        label4 = tkinter.Label(frame7, text="超时", font=self.font)
        label4.pack(ipadx=10)
        combobox3 = ttk.Combobox(frame8, state="readonly", width=5)
        combobox3['value'] = times
        combobox3.current(5)
        combobox3.pack()
        button = tkinter.Button(frame9, text="首部", font=self.font2, cursor="hand2", command=self.setheader)
        button.pack(ipadx=15, padx=10)
        button2 = tkinter.Button(frame10, text="开始", font=self.font2, cursor="hand2")
        button2.pack(ipadx=15, padx=5)

    def setframe2(self):
        frame = tkinter.Frame(self.window, height=360)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        label = tkinter.Label(frame, text="待检测的URL")
        label.pack()
        text = scrolledtext.ScrolledText(frame)
        text.pack(fill=tkinter.X)
        for i in range(0, 20):
            text.insert(tkinter.END, "test\n")
            text.insert(tkinter.END, "test\n")
            text.insert(tkinter.END, "test1\n")

    def setframe3(self):
        frame = tkinter.Frame(self.window, height=360)
        frame.pack(fill=tkinter.X)
        frame.pack_propagate(0)
        label = tkinter.Label(frame, text="存在XSS的URL")
        label.pack()
        text = scrolledtext.ScrolledText(frame)
        text.pack(fill=tkinter.X)
        for i in range(0, 20):
            text.insert(tkinter.END, "test\n")
            text.insert(tkinter.END, "test\n")
            text.insert(tkinter.END, "test1\n")


guione = GuiOne()

