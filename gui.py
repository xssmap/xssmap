import tkinter


class Gui:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("xssmap")
        self.height = 800
        self.width = 800
        self.window.geometry("%dx%d+%d+%d" % (self.width, self.height, (self.window.winfo_screenwidth() - self.width) / 2, (self.window.winfo_screenheight() - self.height) / 2))
        self.window.resizable(width=False, height=False)
        self.window.mainloop()

gui = Gui()


