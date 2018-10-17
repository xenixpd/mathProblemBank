from tkinter import *
#from PIL import ImageTk, Image
# 콤보 상자 사용을 위해 ttk를 들여온다.
from tkinter import ttk
from tkinter import messagebox

# 임시 명령
def doNothing(self):
    print("좋아요. 아주 좋아요.")

# 루트 생성
root=Tk()
root.title("문제 등록(그림)")
root.configure(background='#1E1E1E')
root.geometry("640x480")

# 배경 그림 넣기
#backgourndImage = PhotoImage(file='.\mathProblemBank\thomas-kolnowski-780791-unsplash.gif')
#panel = Label(root, image=backgourndImage)
#panel.pack(side="bottom", fill="both", expand="yes")

# 제목
lblTitle = Label(root, text="<문제 등록(그림)>")
lblTitle.config(font=("맑은 고딕", 20), bg='#1E1E1E', fg='#007ACC')
lblTitle.grid(row=0, column=0, columnspan=2, padx=0, pady=2)

# 문제 관련 정보
# 제목
lblProblemInfoTitle = Label(root, text="<문제 유형 정보>(필수)")
lblProblemInfoTitle.config(font=("맑은 고딕", 11), bg='#1E1E1E', fg='#007ACC')
lblProblemInfoTitle.grid(row=1, column=0, sticky=W, padx=5, pady=5)

# 프레임
frmProblemInfo = Frame(root)
frmProblemInfo.config(bg='#1E1E1E', highlightbackground="white", highlightcolor="white", highlightthickness=1, bd=0)
frmProblemInfo.grid(row=2, column=0, sticky=W, padx=20, pady=1)

# 라벨(배경을 동일하게 처리하므로 클래스로 만들자.)
lblBook = Label(frmProblemInfo, text="책: ")
lblBook.config(bg='#1E1E1E', fg='white')
lblBook.grid(row=0, column=0, sticky=E, padx=2, pady=2)

lblPart = Label(frmProblemInfo, text="부: ")
lblPart.config(bg='#1E1E1E', fg='white')
lblPart.grid(row=1, column=0, sticky=E, padx=2, pady=2)

lblChapter = Label(frmProblemInfo, text="장: ")
lblChapter.config(bg='#1E1E1E', fg='white')
lblChapter.grid(row=2, column=0, sticky=E, padx=2, pady=2)

lblSection = Label(frmProblemInfo, text="절: ")
lblSection.config(bg='#1E1E1E', fg='white')
lblSection.grid(row=3, column=0, sticky=E, padx=2, pady=2)

lblProblemType = Label(frmProblemInfo, text="문제 유형: ")
lblProblemType.config(bg='#1E1E1E', fg='white')
lblProblemType.grid(row=4, column=0, sticky=E, padx=2, pady=2)

# 콤보 상자
strBook = StringVar()
cbbBook = ttk.Combobox(frmProblemInfo, textvariable=strBook)
cbbBook.grid(row=0, column=1, stick=W, padx=2, pady=2)
cbbBook['values'] = ('중1', '중2', '중3', '수학', '수학1', '수학2', '확률과 통계', '미적분', '기하', '경제 수학')
cbbBook.current(0)
cbbBook.bind("<<ComboboxSelected>>", doNothing)

strPart = StringVar()
cbbPart = ttk.Combobox(frmProblemInfo, textvariable=strPart)
cbbPart.grid(row=1, column=1, stick=W, padx=2, pady=2)
cbbPart['values'] = ('부1', '부2', '부3')
cbbPart.current(0)
cbbPart.bind("<<ComboboxSelected>>", doNothing)

strChapter = StringVar()
cbbChapter = ttk.Combobox(frmProblemInfo, textvariable=strChapter)
cbbChapter.grid(row=2, column=1, stick=W, padx=2, pady=2)
cbbChapter['values'] = ('장1', '장2', '장3')
cbbChapter.current(0)
cbbChapter.bind("<<ComboboxSelected>>", doNothing)

strSection = StringVar()
cbbSection = ttk.Combobox(frmProblemInfo, textvariable=strSection)
cbbSection.grid(row=3, column=1, stick=W, padx=2, pady=2)
cbbSection['values'] = ('절1', '절2', '절3')
cbbSection.current(0)
cbbSection.bind("<<ComboboxSelected>>", doNothing)

strProblemType = StringVar()
cbbProblemType = ttk.Combobox(frmProblemInfo, textvariable=strProblemType)
cbbProblemType.grid(row=4, column=1, stick=W, padx=2, pady=2)
cbbProblemType['values'] = ('중1', '중2', '중3', '수학', '수학1', '수학2', '확률과 통계', '미적분', '기하', '경제 수학')
cbbProblemType.current(0)
cbbProblemType.bind("<<ComboboxSelected>>", doNothing)

#style = ttk.Style()
#style.map('cbbBook', fieldbackground=[('readonly', '#1E1E1E')])

root.mainloop()
