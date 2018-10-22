import matplotlib
matplotlib.use("TkAgg")

#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import urllib
import json

import pandas as pd
import numpy as np

LARGE_FONT = ('나눔 고딕', 12)

#style.use("dark_background")
style.use("ggplot")


f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)

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
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}    # 그릇에 담을 프레임들을 저장하기 위한 사전

        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)  # 각 페이지를 담기 위한 프레임
            self.frames[F] = frame  # 각 페이지를 담은 프레임을 사전에 등록(키: 클래스, 값: 각 페이지를 담은 프레임)
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, controller):
        frame = self.frames[controller] # controllerㅇ가 키인 프레임(값)을 가져와서 지역 변수에 할당
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="""시작 페이지
        연습 중입니다.
        조금씩 개선해 갑시다.""", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        buttonOne = ttk.Button(self, text="Agree", command=lambda: controller.show_frame(PageOne))
        buttonOne.pack()

        buttonTwo = ttk.Button(self, text="Disagree", command=quit)
        buttonTwo.pack()

        #buttonThree = ttk.Button(self, text="그래프 페이지로 가기", command=lambda: controller.show_frame(PageThree))
        #buttonThree.pack()

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
ani = animation.FuncAnimation(f, animate, interval=1000)    # 1000 ms(1초)마다 animate 함수를 호출하여 f를 갱신한다.
                                                            # f에서는 sampleData.txt를 사용하는데 이 파일이 갱신되면 자동으로 그래프도 갱신된다.
app.mainloop()