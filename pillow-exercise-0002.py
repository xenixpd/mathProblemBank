# Canvas를 이용한 이미지 크기 조정(shrink)

from tkinter import *
from PIL import ImageTk, Image
import easygui

class App(Frame):
    
    def __init__(self, master):

        Frame.__init__(self, master)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)        
        
        self.original = Image.open(easygui.fileopenbox())

        # 캔버스 크기 변경에 대비해 최초의 너비, 높이, 비율을 기억
        self.originalWidth = self.original.size[0]
        self.originalHeight = self.original.size[1]
        self.originalRatio = self.originalHeight/self.originalWidth
        self.resizingCount = 0  # 이게 필요한 이유는 아래 resize 이벤트 핸들러에서 설명

        print("Original H/W ratio: ", self.originalRatio)

        self.image = ImageTk.PhotoImage(self.original)

        self.display = Canvas(self, bd=0, highlightthickness=0)
        self.display.create_image(0, 0, image=self.image, anchor=CENTER, tags="IMG")
        self.display.grid(row=0, column=0, sticky=W+E+N+S)

        self.pack(fill=BOTH, expand=1)
        self.bind("<Configure>", self.resize)

    def resize(self, event):
        # 어떤 이유에서인지는 모르겠으나 그림 파일을 열고 나면 자동으로 한 번 크기가 바뀜
        # 자동으로 한 번 바뀐 크기가 제대로된 크기이므로 이를 반영
        self.resizingCount += 1

        if self.resizingCount == 1:
            self.originalWidth = event.width
            self.originalHeight = event.height
            self.originalRatio = event.height/event.width

        newRatio = event.height/event.width

        if newRatio > self.originalRatio:
            newWidth = event.width
            newHeight = event.width * self.originalRatio
        elif newRatio < self.originalRatio:
            newWidth = event.height / self.originalRatio
            newHeight = event.height
        else:
            newWidth = event.width
            newHeight = event.height

        size = (int(newWidth), int(newHeight))
        resized = self.original.resize(size, Image.ANTIALIAS)

        self.image = ImageTk.PhotoImage(resized)
        self.display.delete("IMG")
        self.display.create_image(int(event.width/2), int(event.height/2), image=self.image, anchor=CENTER, tags="IMG")
        
root = Tk()
app = App(root)

app.mainloop()