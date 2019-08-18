# coding=utf-8
import tkinter
from tkinter import ttk
from tkinter import messagebox
import ctypes


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
        self.button1 = None
        self.button2 = None
        self.setframe1()
        self.setframe2()
        self.setframe3()
        self.setframe4()
        self.window.mainloop()

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

    def setframe1(self):
        frame = tkinter.Frame(self.window, height=350)
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
        self.button1 = tkinter.Button(frame1, text="标记参数", command=self.setflag)
        self.button1.pack(ipadx=200)
        self.button2 = tkinter.Button(frame2, text="清除标记", command=self.unsetflag)
        self.button2.pack(ipadx=200)

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
        combobox = ttk.Combobox(frame1, state="readonly")
        combobox.pack(side=tkinter.LEFT)
        thread = []
        for i in range(1, 21):
            thread.append(i)
        combobox['value'] = thread
        combobox.current(0)
        button = tkinter.Button(frame2, text="开始")
        button.pack(side=tkinter.LEFT, ipadx=300)

gui = Gui()


