from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

LARGE_FONT = ('맑은 고딕', 11)
DEFAULT_BACKGROUND = '.\\coffee.jpeg'

class App(Frame):

    def __init__(self, master, width=0, height=0):
        Frame.__init__(self, master)
        #print(master.winfo_width(), master.winfo_height())

        # 기본 배경 그림
        self.img = Image.open(DEFAULT_BACKGROUND)
        self.defaultImage = ImageTk.PhotoImage(self.img)

        # 라벨(그림)
        self.lblImage = Label(master, image=self.defaultImage, bg='grey')
        self.lblImage.config(width=width, height=height)
        self.lblImage.grid(row=0, column=0, rowspan=3, columnspan=3, padx=5, pady=5, sticky=NSEW)  # 그릇에 담기

        # 라벨 크기
        self.labelWidth = width
        self.labelHeight = height
        self.labelRatio = height/width
        
        # 단추
        self.btnSelectImage = Button(master, text='선택', bg='yellow', font=LARGE_FONT, command=self.select_image)
        self.btnSelectImage.config(width=10, height=2)
        self.btnSelectImage.grid(row=3, column=0, padx=5, pady=5, sticky=NS)

    def select_image(self):        
        # 파일 선택
        selectedFileName = filedialog.askopenfilename(title='그림 파일 선택')

        # 선택한 파일이 있을 때만 작업
        if selectedFileName != '':
            self.img = Image.open(selectedFileName)

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
            self.resized = ImageTk.PhotoImage(self.img)
            self.lblImage.config(image=self.resized)

if __name__ == '__main__':
    root = Tk()
    #root.geometry("400x400")
    #root.rowconfigure(0, weight=1)
    #root.columnconfigure(0, weight=1)

    test = App(root, 400, 300)

    root.mainloop()