from tkinter import *

from MPBUITools import *

def load_problem_registration():
	win = Toplevel()
	win.title('문제 등록(그림)')
	win.resizable(width=False, height=False)
	win.grab_set()

	container = MPBProblemImageRegistration(win, 768)
	container.grid(sticky="nw")

	#win.mainloop()

def load_problem_registration_with_source(): # 관리자만 사용할 수 있게 할 것
	win = Toplevel()
	win.title('문제 등록(그림)')
	win.resizable(width=False, height=False)
	win.grab_set()

	container = MPBProblemImageRegistrationWithSource(win, 768)
	container.grid(sticky="nw")

def exit_MPB():
	root.destroy()

def doNothing():
	print("좋아요. 아주 좋아요")

root = Tk()
tk.Tk.iconbitmap(root, default=".\\icon\\sum64.ico")
tk.Tk.wm_title(root, "수학 문제 은행")

# 주메뉴(메뉴바)
mainMenu = Menu(root)
root.config(menu=mainMenu)

# 메뉴 항목: 문제 등록

# 먼저 주메뉴에 등록
registerProblemMenu = Menu(mainMenu)
mainMenu.add_cascade(label="문제 등록", menu=registerProblemMenu)

# 메뉴 항목 추가
registerProblemMenu.add_command(label="문제(그림) 등록", command=load_problem_registration)
registerProblemMenu.add_command(label="문제(그림) 등록: 관리자용, 출처 항목 추가", command=load_problem_registration_with_source) # 관리자 전용 기능
registerProblemMenu.add_command(label="폴더 단위 문제(그림) 등록", command=doNothing)
registerProblemMenu.add_separator()
registerProblemMenu.add_command(label="종료", command=exit_MPB)


# 메뉴 항목: 문제 편집

# 먼저 주메뉴에 등록
editProblemMenu = Menu(mainMenu)
mainMenu.add_cascade(label="문제 편집", menu=editProblemMenu) # 관리자 전용 기능


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

insertBtn = Button(mainToolbar, text="문제(그림) 등록", command=load_problem_registration)
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