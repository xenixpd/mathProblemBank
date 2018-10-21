from tkinter import *
from PIL import ImageTk, Image

from MPBUITools import MPBCurriTreeView

UPWARD_ICON = '.\\upward32.gif'
DOWNWARD_ICON = '.\\downward32.gif'

class MPBAuxProblemTypeRegistration(Frame):

    def __init__(self, master, *args, **kargs):
        Frame.__init__(self, master, *args, **kargs)

        # 그릇 만들기
        self.container = Frame(master)

        # 교육 과정 선택 트리
        self.trvCurri = MPBCurriTreeView(self.container, row=0, column=0)

        # 추가/제거 단추를 담는 프레임
        self.frmAddRemove = Frame(self.container)

        self.img = Image.open(UPWARD_ICON)   # 추가/제거 단추를 위한 그림 읽기
        self.upwardImage = ImageTk.PhotoImage(self.img)
        self.img = Image.open(DOWNWARD_ICON)
        self.downwardImage = ImageTk.PhotoImage(self.img)

        self.btnAdd = Button(self.frmAddRemove, image=self.upwardImage)    # 추가 단추
        self.btnAdd.grid(row=0, column=0, padx=5, pady=5, sticky=E)
        self.btnRemove = Button(self.frmAddRemove, image=self.downwardImage)   # 제거 단추
        self.btnRemove.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # 그릇에 담기
        self.trvCurri.grid(row=0, column=0, columnspan=50, padx=5, pady=5)
        self.frmAddRemove.grid(row=1, column=0, columnspan=50)

        self.container.grid()

if __name__ == '__main__':
    root = Tk()

    aAux = MPBAuxProblemTypeRegistration(root)
    #aAux.grid(row=0, column=0)

    root.mainloop()