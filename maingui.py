# coding=utf-8
import tkinter
import ctypes
import tkinter.font


class MainGui:
    def __init__(self):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        self.window = tkinter.Tk()
        self.window.title("xssmap")
        self.height = 400
        self.width = 400
        self.window.geometry("%dx%d+%d+%d" % (self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2, (self.window.winfo_screenheight() - self.height) / 2))
        self.window.resizable(width=False, height=False)
        self.window.iconbitmap("xssmap.ico")
        font = tkinter.font.Font(size=15)
        img = tkinter.PhotoImage(file='xssmap.gif')
        label1 = tkinter.Label(image=img)
        label1.pack()
        self.button1 = tkinter.Button(text="完整检测", font=font, cursor="hand2")
        self.button1.pack(ipadx=45, ipady=25, pady=10)
        self.button2 = tkinter.Button(text="URL检测", font=font, cursor="hand2")
        self.button2.pack(ipadx=50, ipady=25, pady=10)
        self.button3 = tkinter.Button(text="数据包检测", font=font, cursor="hand2")
        self.button3.pack(ipadx=32, ipady=25, pady=10)
        self.window.mainloop()


maingui = MainGui()
