from tkinter import *

from MPBUITools import *

def loadProblemRegistration():
	win = Toplevel()
	win.title('문제 등록(그림)')
	win.resizable(width=False, height=False)
	win.grab_set()

	MPBCurriTreeView(win, row=0, column=0)
	MPBProblemImageRegistration(win, row=0, column=1, width=300, height=300)


def doNothing():
	print("좋아요. 아주 좋아요")

root = Tk()

# 주메뉴(메뉴바)
mainMenu = Menu(root)
root.config(menu=mainMenu)

# 메뉴 항목: 문제 등록

# 먼저 주메뉴에 등록
registerProblemMenu = Menu(mainMenu)
mainMenu.add_cascade(label="문제 등록", menu=registerProblemMenu)

# 메뉴 항목 추가
registerProblemMenu.add_command(label="새 문제 등록...", command=doNothing)
registerProblemMenu.add_command(label="New", command=doNothing)
registerProblemMenu.add_separator()
registerProblemMenu.add_command(label="종료", command=doNothing)

# 메뉴 항목: 문제 검색

# 먼저 주메뉴에 등록
searchProblemMenu = Menu(mainMenu)
mainMenu.add_cascade(label="문제 검색", menu=searchProblemMenu)

# 메뉴 항목 추가
searchProblemMenu.add_command(label="기본 검색", command=doNothing)
searchProblemMenu.add_command(label="Cut", command=doNothing)
searchProblemMenu.add_command(label="Paste", command=doNothing)

# 주 도구바(툴바)
mainToolbar = Frame(root, bg="blue")

insertBtn = Button(mainToolbar, text="문제 등록", command=loadProblemRegistration)
#insertBtn = Button(mainToolbar, text="문제 등록", command=doNothing)
insertBtn.pack(side=LEFT, padx=2, pady=2)

printBtn = Button(mainToolbar, text="기본 검색", command=doNothing)
printBtn.pack(side=LEFT, padx=2, pady=2)

mainToolbar.pack(side=TOP, fill=X)

# 주 상태바
mainStatus = Label(root, text="Preparing to do nothing...", bd=1, relief=SUNKEN, anchor=W)
mainStatus.pack(side=BOTTOM, fill=X)

# tkinter 실행
root.mainloop()