from tkinter import *

from MPBUITools import *

def register_image_problem(ctrlProblemType):
    if ctrlProblemType.getSelectedProblemTypeID() == 0: # 문제 유형 ID, 문제 유형이 아니거나(즉, 책, 부, 장, 절) 선택한 것이 없으면 0을 반환한다.
        messagebox.showerror("문제 유형 없음", "문제 유형을 선택하세요.")
    else:
        print(ctrlProblemType.getSelectedProblemTypeID())

def loadProblemRegistration():
	win = Toplevel()
	win.title('문제 등록(그림)')
	win.resizable(width=False, height=False)
	win.grab_set()

	aTree = MPBCurriTreeView(win, row=0, column=0, rowspan=30, columnspan=30)	# 교과 선택 용
	aImageRegistration = MPBProblemImageRegistration(win, row=0, column=30, rowspan=20, columnspan=20, width=400, height=300)	# 문제 등록
	aAns = MPBAnswerRegistration(win, row=30, column=0, width=400, height=50)	# 답 등록
	aSol = MPBSolutionRegistration(win, row=30, column=30, width=400, height=175)	# 풀이 등록
	
	frmOkCancel = Frame(win)   # 확인/취소 버튼을 위한 프레임
	btnOk = Button(frmOkCancel, text='확인', fg='white', bg='blue', font=HUGE_FONT, command=lambda: register_image_problem(aTree))
	btnCancel = Button(frmOkCancel, text='취소', fg='white', bg='blue', font=HUGE_FONT, command=lambda: root.destroy())
	btnOk.grid(row=0, column=0, padx=5, pady=5)
	btnCancel.grid(row=0, column=1, padx=5, pady=5)
	frmOkCancel.grid(row=49, column=0, columnspan=50)


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