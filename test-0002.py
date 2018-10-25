import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
import sqlite3
import os
from os import listdir
from os.path import isfile, join

from MPBUITools import MPBAuxProblemTypeSelection
from MPBLibrary import getFileNameFromFullPath

HUGE_FONT = ('맑은 고딕', 12, "bold")
LARGE_FONT = ('맑은 고딕', 11)
NORMAL_FONT = ('맑은 고딕', 10)

DEFAULT_BACKGROUND = '.\\coffee.jpeg'

class MPBProblemSheet(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        lblTitle = tk.Label(self, text="<폴더 단위 문제 등록>(*.jpg, *.png 파일만 지원)", font=HUGE_FONT, fg='blue') # 제목

        headerContainer = tk.Frame(self)
        headerContainer.grid_columnconfigure(1, weight=1)

        self.folder = '' # 선택한 폴더 이름

        btnFolder = tk.Button(headerContainer, text='폴더 선택', command=self.select_folder)
        btnFolder.grid(row=0, column=0)

        self.lblFolder = tk.Label(headerContainer)
        self.lblFolder.grid(row=0, column=1, padx=5, sticky="w")

        sheetContainer = tk.Frame(self)
        sheetContainer.rowconfigure(0, weight=1)
        sheetContainer.columnconfigure(0, weight=1)

        self.problemSheet = ttk.Treeview(sheetContainer, selectmode='browse')

        self.problemSheet.column('#0', anchor='center', minwidth=350)
        self.problemSheet.heading('#0', text='파일명')

        self.problemSheet.config(columns=('sourceID', 'problemTypeID', 'columns', 'difficulty', 'ansType', 'objAns', 'subjAns', ))
        self.problemSheet.column('sourceID', anchor="center", minwidth=75, width=100)
        self.problemSheet.heading('sourceID', text='출처') # 관리자 전용
        self.problemSheet.column('problemTypeID', anchor="center", minwidth=75, width=100)
        self.problemSheet.heading('problemTypeID', text='문제 유형')
        self.problemSheet.column('columns', anchor="center", minwidth=75, width=100)
        self.problemSheet.heading('columns', text='단 수')
        self.problemSheet.column('difficulty', anchor="center", minwidth=75, width=100)
        self.problemSheet.heading('difficulty', text='난이도')
        self.problemSheet.column('ansType', anchor="center", minwidth=75, width=100)
        self.problemSheet.heading('ansType', text='답 유형')
        self.problemSheet.column('objAns', anchor="center", minwidth=75, width=100)
        self.problemSheet.heading('objAns', text='객관식 답')
        self.problemSheet.column('subjAns', anchor="center", minwidth=75, width=100)
        self.problemSheet.heading('subjAns', text='주관식 답')

        yScroll = ttk.Scrollbar(sheetContainer, orient=tk.VERTICAL) # 수직 스크롤바 만들기
        yScroll.configure(command=self.problemSheet.yview)
        self.problemSheet.configure(yscrollcommand=yScroll.set)

        self.problemSheet.grid(row=0, column=0, sticky="nsew")
        yScroll.grid(row=0, column=1, sticky="ns")

        footerContainer = tk.Frame(self)
        footerContainer.grid_rowconfigure(0, weight=1)

        self.image = Image.open(DEFAULT_BACKGROUND)
        self.defaultImage = ImageTk.PhotoImage(self.image)

        lblWidth = 400
        lblHeight = 300

        self.lblImage = tk.Label(footerContainer, image=self.defaultImage, bg='grey')
        self.lblImage.config(width=lblWidth, height=lblHeight, relief=tk.SUNKEN)
        self.lblImage.grid(row=0, column=0, sticky="nw")

        lblTemp = tk.Label(footerContainer, text='임시')
        lblTemp.grid(row=0, column=1, sticky="nsew")
        
        lblTitle.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        headerContainer.grid(row=1, column=0, columnspan=3, padx=10, sticky="w")
        sheetContainer.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        footerContainer.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.problemSheet.bind('<Double-1>', self.on_double_click)
        self.problemSheet.bind('<ButtonRelease-1>', lambda event : self.on_click(event, width=lblWidth, height=lblHeight))
    
    def select_folder(self):
        self.selectedFolder = filedialog.askdirectory()

        if self.selectedFolder != '':
            # 우선 기존 내용 삭제
            for i in self.problemSheet.get_children():
                self.problemSheet.delete(i)

            self.lblImage.config(image=self.defaultImage)

            # 새로운 내용 추가
            self.lblFolder.config(text=self.selectedFolder)
            onlyfiles = [f for f in listdir(self.selectedFolder) if isfile(join(self.selectedFolder, f))]

            for f in onlyfiles:
                _, fExt = os.path.splitext(f)

                if fExt == '.png' or fExt == '.jpg':
                    self.problemSheet.insert('', 'end', join(self.selectedFolder, f), text=f)

    def on_double_click(self, event):
        region = self.problemSheet.identify('region', event.x, event.y)

        if region == 'tree' or region == 'cell':
            item = self.problemSheet.identify('item', event.x, event.y)

            aWin = tk.Toplevel()
            aWin.title(item)
            aWin.grab_set()

            aLabel = tk.Label(aWin)
            #self.img = Image.open(item)
            #self.original = ImageTk.PhotoImage(self.img)
            #aLabel.config(image=self.original)
            self.tempImage = ImageTk.PhotoImage(file=item)
            aLabel.config(image=self.tempImage)
            aLabel.pack()

    def on_click(self, event=None, width=400, height=300):
        region = self.problemSheet.identify('region', event.x, event.y)

        if region == 'tree' or region == 'cell':
            item = self.problemSheet.identify('item', event.x, event.y)
            self.image = Image.open(item)
            self.original = ImageTk.PhotoImage(self.image)

            imageWidth = self.image.size[0]
            imageHeight = self.image.size[1]
            imageRatio = imageHeight/imageWidth
            labelRatio = height/width

            if imageRatio < labelRatio:
                if imageWidth > width:
                    newWidth = width
                    newHeight = int(width * imageRatio)
                else:   # imageWidth <= width
                    newWidth = imageWidth
                    newHeight = imageHeight
            else:   # imageRatio >= labelRatio
                if imageHeight > height:
                    newHeight = height
                    newWidth = int(height / imageRatio)
                else:   # imageHeight <= height
                    newHeight = imageHeight
                    newWidth = imageWidth

            self.image = self.image.resize((newWidth, newHeight), Image.ANTIALIAS)
            self.resized = ImageTk.PhotoImage(self.image)
            self.lblImage.config(image=self.resized)

if __name__ == '__main__':
    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    aSheet = MPBProblemSheet(root)
    aSheet.grid(row=0, column=0, sticky="nsew")

    root.mainloop()