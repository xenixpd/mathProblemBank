import matplotlib
matplotlib.use("TkAgg")

#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import ttk

import urllib
import json

import pandas as pd
import numpy as np


LARGE_FONT = ('나눔 고딕', 12)
NORMAL_FONT = ('나눔 고딕', 10)
SMALL_FONT = ('나눔 고딕', 8)

#style.use("dark_background")
style.use("ggplot")

f = Figure()
a = f.add_subplot(111)

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")

    def leavemini():    # 함수 안의 함수를 보여주기 위한 예
        popup.destroy()

    label = ttk.Label(popup, text=msg, font=NORMAL_FONT)
    label.pack(sid="top", fill="x", pady=10)

    B1 = ttk.Button(popup, text="Okay", command=leavemini)
    B1.pack()

    popup.mainloop()

def animate(i):
    pullData = open("sampleData.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []

    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()
    a.plot(xList, yList)

class MBP(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="sum64.ico")
        tk.Tk.wm_title(self, "수학 문제 은행")
        
        container = tk.Frame(self) # 이 클래스는 Tk를 상속했으므로 틀을 가지지 않는다. 따라서 별도의 그릇을 선언해 준다.
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}    # 그릇에 담을 프레임들을 저장하기 위한 사전

        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self) # 각 페이지를 담기 위한 프레임. 시작 페이지를 포함한 각 페이지는 __init__(self, parent, controller) 형태의 생성자를 가져야 한다.
                                       # 생성자의 parent는 여기의 container(이 클래스에서 만든 그릇)이고, 생성자의 controller는 여기의 self(MPB 클래스)이다.
                                       # 각 페이지를 담당하는 클래스가 MP 클래스에 대한 참조를 가져야 여기에서 정의된 show_frame() 함수를 호출할 수 있다.
                                       # MPB 클래스만 tk.Tk를 상속(즉, root)하고, 나머지 각 페이지용 클래스는 tk.Frame을 상속(즉, 틀)한다.
            self.frames[F] = frame # 각 페이지를 담은 프레임을 사전에 등록(키: 클래스, 값: 각 페이지를 담은 프레임)
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont] # controller가 키인 프레임(값)을 가져와서 지역 변수에 할당
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="시작 페이지", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        buttonOne = ttk.Button(self, text="페이지 1로 가기", command=lambda: controller.show_frame(PageOne))
        buttonOne.pack()

        buttonTwo = ttk.Button(self, text="페이지 2로 가기", command=lambda: controller.show_frame(PageTwo))
        buttonTwo.pack()

        buttonThree = ttk.Button(self, text="그래프 페이지로 가기", command=lambda: controller.show_frame(PageThree))
        buttonThree.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="페이지 1", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        buttonHome = ttk.Button(self, text="시작 페이지로 돌아가기", command=lambda: controller.show_frame(StartPage))
        buttonHome.pack()

        buttonTwo = ttk.Button(self, text="페이지 2로 가기", command=lambda: controller.show_frame(PageTwo))
        buttonTwo.pack()

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="페이지 2", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        buttonHome = ttk.Button(self, text="시작 페이지로 돌아가기", command=lambda: controller.show_frame(StartPage))
        buttonHome.pack()

        buttonOne = ttk.Button(self, text="페이지 1로 가기", command=lambda: controller.show_frame(PageOne))
        buttonOne.pack()

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="그래프 페이지!", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        buttonHome = ttk.Button(self, text="시작 페이지로 돌아가기", command=lambda: controller.show_frame(StartPage))
        buttonHome.pack()

        canvas = FigureCanvasTkAgg(f, self)
        #canvas.show()
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        

app = MBP()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=500000)    # 1000 ms(1초)마다 animate 함수를 호출하여 f를 갱신한다.
                                                            # f에서는 sampleData.txt를 사용하는데 이 파일이 갱신되면 자동으로 그래프도 갱신된다.
app.mainloop()