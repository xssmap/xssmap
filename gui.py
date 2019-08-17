# coding=utf-8
import tkinter


class Gui:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("xssmap")
        self.height = 1000
        self.width = 1024
        self.window.geometry("%dx%d+%d+%d" % (self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2, (self.window.winfo_screenheight() - self.height) / 2))
        self.window.resizable(width=False, height=False)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.setframe1()
        self.setframe2()
        self.window.mainloop()

    def setframe1(self):
        frame = tkinter.Frame(self.window)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.grid(row=0, column=0)
        label = tkinter.Label(frame, text="XSS输入点")
        label.grid(row=0)
        text = tkinter.Text(frame)
        text.grid(row=1, sticky=tkinter.NSEW)

    def setframe2(self):
        frame = tkinter.Frame(self.window)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.grid(row=1, column=0, sticky=tkinter.NSEW)
        label = tkinter.Label(frame, text="XSS输出点")
        label.grid(row=0)
        text = tkinter.Text(frame)
        text.grid(row=1, sticky=tkinter.NSEW)

    def setframe3(self):
        pass

    def setframe4(self):
        pass

gui = Gui()


