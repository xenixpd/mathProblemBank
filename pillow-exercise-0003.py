# 다시 할 것
from tkinter import filedialog
from tkinter import *
#from tkinter import ttk
from PIL import ImageTk, Image

HUGE_FONT = ('맑은 고딕', 16)
LARGE_FONT = ('맑은 고딕', 11)

class App(Frame):

    def __init__(self, master, row=0, column=0, pos=0):
        Frame.__init__(self, master)

        # 단추와 라벨(그림)을 담기 위한 그릇
        self.container = Frame(master)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)  

        # 라벨(그림)
        self.lblImage = Label(self.container)
        self.lblImage.configure(width=60, height=20, bg='grey')

        # 단추
        self.btnSelectImageFile = Button(self.container, text='그림 파일 열기', font=LARGE_FONT, wraplength=75, command=self.selectImageFile)
        self.btnSelectImageFile.configure(width=12, height=2, bg='yellow')

        self.btnPasteFromClipboard = Button(self.container, text='클립보드에서 가져오기', font=LARGE_FONT, wraplength=100, command=self.pasteFromClipboard)
        self.btnPasteFromClipboard.configure(width=12, height=2, bg='yellow')

        self.btnInitializeImage = Button(self.container, text='초기화', font=LARGE_FONT, command=self.initializeImage)
        self.btnInitializeImage.configure(width=12, height=2, bg='yellow')

        # 그릇에 담기
        self.container.grid(row=row, column=column, sticky=(N, S, E, W))
        self.lblImage.grid(row=0, column=1, rowspan=3, padx=5, pady=5)
        self.btnSelectImageFile.grid(row=0, column=0, padx=5, pady=5)
        self.btnPasteFromClipboard.grid(row=1, column=0, padx=5, pady=5)
        self.btnInitializeImage.grid(row=2, column=0, padx=5, pady=5)

    def selectImageFile(self):
        selectedFileName = filedialog.askopenfilename(title='그림 파일 선택')
        #print("Select Image File")

        # 선택한 파일이 있을 때만 작업
        if selectedFileName != '':
            #print(self.selectedFileName)
            original = Image.open(selectedFileName)
            print(original.size[0], original.size[1], self.lblImage.winfo_width(), self.lblImage.winfo_height())
            img = ImageTk.PhotoImage(original)
            self.lblImage.configure(image=img)
            self.lblImage.image = img

    def pasteFromClipboard(self):
        print("Paste from Clipboard")

    def initializeImage(self):
        print("Initialize Image")

if __name__ == '__main__':                
    root = Tk()
    root.geometry("640x480")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    
    app = App(root, 0, 0)

    app.mainloop()