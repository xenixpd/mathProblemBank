from tkinter import *
from tkinter import ttk, filedialog
from PIL import ImageTk, Image, ImageGrab

LARGE_FONT = ('맑은 고딕', 11)
DEFAULT_BACKGROUND = '.\\coffee.jpeg'

class App(Frame):

    def __init__(self, master, row=0, column=0, width=0, height=0, pos=S):
        # 인수로 주어진 width와 height는 전체 크기가 아니라 그림 영역의 크기이다.
        # 인수 pos는 명령 단추가 놓일 곳을 가리킨다. (N, S, E, W)

        Frame.__init__(self, master)
        #print(master.winfo_width(), master.winfo_height())

        self.container = ttk.Frame(master, padding=(3,3,12,12))

        # 기본 배경 그림
        self.img = Image.open(DEFAULT_BACKGROUND)
        self.defaultImage = ImageTk.PhotoImage(self.img)
        self.isDefaultImageUsed = True

        # 라벨(그림)
        self.lblImage = Label(self.container, image=self.defaultImage, bg='grey')
        self.lblImage.config(width=width, height=height, relief=SUNKEN)

        # 라벨 크기
        self.labelWidth = width
        self.labelHeight = height
        self.labelRatio = height/width
        
        # 명령 단추
        # 그림 파일 선택
        self.btnSelectImage = Button(self.container, text='그림 파일 선택', bg='yellow', font=LARGE_FONT, 
                              wraplength=75, command=self.select_image)
        self.btnSelectImage.config(width=10, height=2)

        # 클립보드에서 가져오기
        self.btnPasteFromClipboard = Button(self.container, text='클립보드에서 가져오기', bg='yellow', font=LARGE_FONT,
                                     wraplength=90, command=self.paste_from_clipboard)
        self.btnPasteFromClipboard.config(width=10, height=2)

        # 기존 그림 지우기
        self.btnInitializeImage = Button(self.container, text='초기화', bg='yellow', font=LARGE_FONT,
                                  command=self.initialize_image)
        self.btnInitializeImage.config(width=10, height=2)

        # 안내용 라벨
        self.lblInfo = Label(self.container)
        self.lblInfo.config(justify=RIGHT, wraplength=width)

        self.container.grid(row=row, column=column, sticky=NSEW)

        # 프레임에 넣기. 기본은 N(아래쪽에 단추 배치)
        if pos == N:
            self.lblImage.grid(row=1, column=0, rowspan=3, columnspan=3, padx=5, pady=5, sticky=NSEW)
            self.btnSelectImage.grid(row=0, column=0, padx=5, pady=5, sticky=NS)
            self.btnPasteFromClipboard.grid(row=0, column=1, padx=5, pady=5, sticky=NS)    
            self.btnInitializeImage.grid(row=0, column=2, padx=5, pady=5)

            self.lblInfo.grid(row=4, column=0, columnspan=3, padx=2, pady=2, sticky=E)
        elif pos == E:
            self.lblImage.grid(row=0, column=0, rowspan=3, columnspan=3, padx=5, pady=5, sticky=NSEW)
            self.btnSelectImage.grid(row=0, column=3, padx=5, pady=5, sticky=NS)
            self.btnPasteFromClipboard.grid(row=1, column=3, padx=5, pady=5, sticky=NS)    
            self.btnInitializeImage.grid(row=2, column=3, padx=5, pady=5)

            self.lblInfo.grid(row=3, column=0, columnspan=3, padx=2, pady=2, sticky=E)
        elif pos == W:
            self.lblImage.grid(row=0, column=1, rowspan=3, columnspan=3, padx=5, pady=5, sticky=NSEW)
            self.btnSelectImage.grid(row=0, column=0, padx=5, pady=5, sticky=NS)
            self.btnPasteFromClipboard.grid(row=1, column=0, padx=5, pady=5, sticky=NS)    
            self.btnInitializeImage.grid(row=2, column=0, padx=5, pady=5)

            self.lblInfo.grid(row=3, column=1, columnspan=3, padx=2, pady=2, sticky=E)
        else:
            self.lblImage.grid(row=1, column=0, rowspan=3, columnspan=3, padx=5, pady=5, sticky=NSEW)
            self.btnSelectImage.grid(row=4, column=0, padx=5, pady=5, sticky=NS)
            self.btnPasteFromClipboard.grid(row=4, column=1, padx=5, pady=5, sticky=NS)    
            self.btnInitializeImage.grid(row=4, column=2, padx=5, pady=5)

            self.lblInfo.grid(row=0, column=0, columnspan=3, padx=2, pady=2, sticky=E)

    def select_image(self):        
        # 파일 선택
        selectedFileName = filedialog.askopenfilename(title='그림 파일 선택')

        # 선택한 파일이 있을 때만 작업
        if selectedFileName != '':
            self.img = Image.open(selectedFileName)
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용)

            imageWidth = self.img.size[0]
            imageHeight = self.img.size[1]
            imageRatio = imageHeight/imageWidth

            if imageRatio < self.labelRatio:
                if imageWidth > self.labelWidth:
                    newWidth = self.labelWidth
                    newHeight = int(self.labelWidth * imageRatio)
                else:   # imageWidth <= self.labelWidth
                    newWidth = imageWidth
                    newHeight = imageHeight
            else:   # imageRatio >= self.labelRatio
                if imageHeight > self.labelHeight:
                    newHeight = self.labelHeight
                    newWidth = int(self.labelHeight / imageRatio)
                else:   # imageHeight <= self.labelHeight
                    newHeight = imageHeight
                    newWidth = imageWidth

            self.img = self.img.resize((newWidth, newHeight), Image.ANTIALIAS)
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            #self.lblImage.config(image=self.original)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text=selectedFileName)  # 안내용 라벨에 읽어들인 파일 경로 표시

    def paste_from_clipboard(self):
        self.img = ImageGrab.grabclipboard()

        if self.img != None:
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용): 이하 부분은 위와 동일하므로 함수로 만들 것을 고려할 것

            imageWidth = self.img.size[0]
            imageHeight = self.img.size[1]
            imageRatio = imageHeight/imageWidth

            if imageRatio < self.labelRatio:
                if imageWidth > self.labelWidth:
                    newWidth = self.labelWidth
                    newHeight = int(self.labelWidth * imageRatio)
                else:   # imageWidth <= self.labelWidth
                    newWidth = imageWidth
                    newHeight = imageHeight
            else:   # imageRatio >= self.labelRatio
                if imageHeight > self.labelHeight:
                    newHeight = self.labelHeight
                    newWidth = int(self.labelHeight / imageRatio)
                else:   # imageHeight <= self.labelHeight
                    newHeight = imageHeight
                    newWidth = imageWidth

            self.img = self.img.resize((newWidth, newHeight), Image.ANTIALIAS)
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text='<클립보드>')  # 안내용 라벨

    def initialize_image(self):
        self.lblImage.config(image=self.defaultImage)
        self.isDefaultImageUsed = True
        self.lblInfo.config(text='')    # 안내용 라벨

if __name__ == '__main__':
    root = Tk()
    #root.geometry("400x400")
    #root.rowconfigure(0, weight=1)
    #root.columnconfigure(0, weight=1)

    test = App(root, 0, 0, 400, 300)

    root.mainloop()