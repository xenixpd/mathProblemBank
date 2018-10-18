from tkinter import *
#from tkinter import ttk
from PIL import ImageTk, Image

class App(Frame):

    def __init__(self, master, row=0, col=0, pos=0):
        Frame.__init__(self, master)

        # 단추와 라벨(그림)을 담기 위한 그릇
        self.container = Frame(master)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)  

        # 라벨(그림)
        #self.lblImage = Label(self.container)
        #self.lblImage.configure(width=300, height=200)

        # 단추
        self.btnSelectProblemFile = Button(self.container, text='그림 파일 열기', wraplength=5)
        self.btnSelectProblemFile.configure(width=10, height=5)

        self.btnPasteFromClipboard = Button(self.container, text='클립보드에서 가져오기', wraplength=5)
        self.btnInitializeImage = Button(self.container, text='초기화', wraplength=5)
