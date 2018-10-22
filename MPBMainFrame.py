from tkinter import *

from MPBUITools import *

def register_problem_image(tree, problem, ans, sol):
    if tree.getSelectedProblemTypeID() == 0:	# 문제 유형 ID, 문제 유형이 아니거나(즉, 책, 부, 장, 절) 선택한 것이 없으면 0을 반환한다.
        messagebox.showerror("문제 유형 없음", "문제 유형을 선택하세요.")
    else:
        print(tree.getSelectedProblemTypeID())

def loadProblemRegistration():
	win = Toplevel()
	win.title('문제 등록(그림)')
	win.resizable(width=False, height=False)
	win.grab_set()

	container = Frame(win)
	container.config(width=1024, height=768)
	
	aTree = MPBCurriTreeView(container)	# 문제 유형
	aTree.grid(row=0, column=0, rowspan=30, columnspan=30, padx=10, pady=10)
	
	aProblem = MPBProblemImageRegistration(container, width=400, height=300, pos=N)	# 문제 등록
	aProblem.grid(row=0, column=30, rowspan=30, columnspan=20, padx=10, pady=10)
	
	anAns = MPBAnswerRegistration(container, width=400, height=50)	# 답 등록
	anAns.grid(row=30, column=0, rowspan=20, columnspan=30, sticky=N+W, padx=10, pady=10)
	
	aSol = MPBSolutionRegistration(container, width=400, height=175)	# 풀이 등록
	aSol.grid(row=30, column=30, rowspan=20, columnspan=20, sticky=N+W, padx=10, pady=10)
	
	frmOkCancel = Frame(container)   # 확인/취소 버튼을 위한 프레임
	
	btnOk = Button(frmOkCancel, text='확인', fg='white', bg='blue', font=HUGE_FONT, command=lambda: register_problem_image(aTree, aProblem, anAns, aSol))
	btnCancel = Button(frmOkCancel, text='취소', fg='white', bg='blue', font=HUGE_FONT, command=lambda: win.destroy())
	btnOk.grid(row=0, column=0, padx=5, pady=5)
	btnCancel.grid(row=1, column=0, padx=5, pady=5)
	
	#frmOkCancel.grid(row=50, column=0, columnspan=50, padx=10, pady=10)
	frmOkCancel.grid(row=0, column=50, rowspan=50, padx=10, pady=10)

	container.grid()

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
insertBtn.grid(row=1, column=0, padx=2, pady=2)

printBtn = Button(mainToolbar, text="기본 검색", command=doNothing)
printBtn.grid(row=1, column=1, padx=2, pady=2)

mainToolbar.grid(row=0, column=0, columnspan=50, sticky=EW)

# 주 상태바
mainStatus = Label(root, text="Preparing to do nothing...", bd=1, relief=SUNKEN, anchor=W)
mainStatus.grid(row=50, column=0, columnspan=50, sticky=EW)

# tkinter 실행
root.mainloop()