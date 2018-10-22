import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image, ImageGrab
import sqlite3

HUGE_FONT = ('맑은 고딕', 12, "bold")
LARGE_FONT = ('맑은 고딕', 11)
NORMAL_FONT = ('맑은 고딕', 10)

DEFAULT_BACKGROUND = '.\\coffee.jpeg'
CLIPBOARD_IMAGE = None

class MPBCurriTreeView(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        #tk.Frame.__init__(self, parent, *args, **kwargs)
        tk.Frame.__init__(self, parent)
        
        # 트리에서 선택된 항목의 종류와 ID(기본값)
        self.selectedCurriLevel = ''
        self.selectedCurriID = 0
        self.selectedCurriName = ''
        self.selectedProblemTypeID = 0

        self.lblTitle = tk.Label(self, text="<문제 유형 선택>", font=HUGE_FONT) # 제목
        self.lblTitle.config(fg='blue')

        self.trvCurri = ttk.Treeview(self, height=20, selectmode='browse') # 트리 만들기
        self.trvCurri.bind('<<TreeviewSelect>>', self.treeview_selected) # 클릭 시 실행할 함수
        self.trvCurri.config(columns=('alive')) # Treeview 내의 제목 설정
        self.trvCurri.column('alive', width=135, anchor='center')
        self.trvCurri.heading('alive', text='교육 과정 내인지 여부')
        self.trvCurri.column('#0', width=425)

        treeYScroll = ttk.Scrollbar(self, orient=tk.VERTICAL) # 수직 스크롤바 만들기
        treeYScroll.configure(command=self.trvCurri.xview)
        self.trvCurri.configure(yscrollcommand=treeYScroll.set)

        self.lblSelectedCurriLevel = tk.Label(self, text='구분') # 선택한 항목 구분
        self.lblSelectedCurriName = tk.Label(self, text='이름', fg='blue') # 선택한 항목 이름
        self.lblSelectedCurriID = tk.Label(self, text='ID') # 선택한 항목 ID

        # 데이타베이스에 연결해서 데이타 가져오기
        conn = sqlite3.connect("mathProblemDB.db") # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성
        cur.execute("SELECT id, name FROM tblBook ORDER BY priority") # SQL 실행
        rows = cur.fetchall() # 데이타 fetch

        # 교육 과정 관련 트리 만들기
        for row in rows:
            bookID = str(row[0])
            self.trvCurri.insert('', 'end', '책-' + bookID, text=row[1], tag='book')

            # 책 아래에 파트 추가
            sqlStr = "SELECT id, name FROM tblPart WHERE bookID = " + str(row[0]) + " ORDER BY priority"
            cur.execute(sqlStr)
            secondRows = cur.fetchall()

            for secondRow in secondRows:
                partID = str(secondRow[0])
                self.trvCurri.insert('책-' + bookID, 'end', '부-' + partID, text=secondRow[1], tag='part')

                # 파트 아래에 장 추가
                sqlStr = "SELECT id, name FROM tblChapter WHERE partID = " + str(secondRow[0]) + " ORDER BY priority"
                cur.execute(sqlStr)
                thirdRows = cur.fetchall()

                for thirdRow in thirdRows:
                    chapterID = str(thirdRow[0])
                    self.trvCurri.insert('부-' + partID, 'end', '장-' + chapterID, text=thirdRow[1], tag='chapter')

                    # 장 아래에 절 추가
                    sqlStr = "SELECT id, name FROM tblSection WHERE chapterID = " + str(thirdRow[0]) + " ORDER BY priority"
                    cur.execute(sqlStr)
                    fourthRows = cur.fetchall()

                    for fourthRow in fourthRows:
                        sectionID = str(fourthRow[0])
                        self.trvCurri.insert('장-' + chapterID, 'end', '절-' + sectionID, text=fourthRow[1], tag='section')

                        # 절 아래에 문제 유형 추가
                        sqlStr = "SELECT id, name, alive FROM tblProblemType WHERE sectionID = " + str(fourthRow[0]) + " ORDER BY priority"
                        cur.execute(sqlStr)
                        fifthRows = cur.fetchall()

                        for fifthRow in fifthRows:
                            problemTypeID = str(fifthRow[0])
                            
                            if fifthRow[2]: # fifthRow[2]에는 dead(0) 또는 alive(1)의 값이 담겨 있다.
                                self.trvCurri.insert('절-' + sectionID, 'end', '문제 유형-' + problemTypeID, text=fifthRow[1], tag='alive')
                                self.trvCurri.set('문제 유형-' + problemTypeID, 'alive', 'O')
                            else:
                                self.trvCurri.insert('절-' + sectionID, 'end', '문제 유형-' + problemTypeID, text=fifthRow[1], tag='dead')
                                self.trvCurri.set('문제 유형-' + problemTypeID, 'alive', 'X')

        # 트리 색칠
        self.trvCurri.tag_configure('alive', foreground='blue')
        self.trvCurri.tag_configure('dead', background='#C1C1C1', foreground='red') # 교육 과정 밖의 유형은 배경 회색, 글 빨간색으로 처리

        conn.close() # 데이터베이스에 대한 연결 닫기

        # 그려 넣기
        self.lblTitle.grid(row=0, column=0, columnspan=11, sticky="w")
        self.trvCurri.grid(row=1, column=0, columnspan=10, sticky="nsew")
        treeYScroll.grid(row=1, column=10, sticky="ns")
        self.lblSelectedCurriLevel.grid(row=2, column=0, columnspan=2, padx=10, sticky="e")
        self.lblSelectedCurriName.grid(row=2, column=2, columnspan=7, sticky="w")
        self.lblSelectedCurriID.grid(row=2, column=9, sticky="e", padx=5)
    
    # 트리의 어떤 항목이 선택되었을 때 실행되는 함수
    def treeview_selected(self, event):
        self.selectedCurriLevel = self.trvCurri.focus().split('-')[0]
        self.selectedCurriID = self.trvCurri.focus().split('-')[1]
        self.selectedCurriName = self.trvCurri.item(self.trvCurri.focus())['text']

        # 선택한 항목의 구분 알리기
        self.lblSelectedCurriLevel['text'] = self.selectedCurriLevel

        # 선택한 항목의 이름 알리기
        self.lblSelectedCurriName['text'] = self.selectedCurriName

        # 선택한 항목의 ID 알리기
        self.lblSelectedCurriID['text'] = self.selectedCurriID

    # 트리의 선택된 문제 유형 이름과 번호를 알려준다. 선택된 것이 없거나 문제 유형이 아니면(즉 책, 부, 장, 절이면) 0을 반환한다.
    def getSelectedProblemTypeID(self):
        if self.selectedCurriLevel == '문제 유형':
            return self.lblSelectedCurriID['text']
        else:
            return 0

    # 임시
    #def doSomething(self, event):
    #    curItem = self.trvCurri.focus()
    #    print(self.trvCurri.item(curItem)['tags'][0].split('-')[0], self.trvCurri.item(curItem)['tags'][0].split('-')[1])



class MPBProblemImageRegistration(tk.Frame):

    def __init__(self, parent, width=400, height=300, pos=tk.N, *args, **kwargs):
        # 인수로 주어진 width와 height는 전체 크기가 아니라 그림 영역의 크기이다.
        # 인수 pos는 명령 단추가 놓일 곳을 가리킨다. (N, S, E, W)

        #tk.Frame.__init__(self, parent, *args, **kwargs)
        tk.Frame.__init__(self, parent)
        #print(master.winfo_width(), master.winfo_height())

        # 제목
        lblTitle = tk.Label(self, text='<문제 그림 선택>', font=HUGE_FONT)
        lblTitle.config(fg='blue')

        # 기본 배경 그림
        self.img = Image.open(DEFAULT_BACKGROUND)
        self.defaultImage = ImageTk.PhotoImage(self.img)
        self.isDefaultImageUsed = True

        # 라벨(그림)
        self.lblImage = tk.Label(self, image=self.defaultImage, bg='grey')
        self.lblImage.config(width=width, height=height, relief=tk.SUNKEN)

        # 라벨 크기
        #self.labelWidth = width
        #self.labelHeight = height
        #self.labelRatio = height/width
        
        # 명령 단추
        # 그림 파일 선택
        btnSelectImage = tk.Button(self, text='그림 파일 선택', bg='yellow', wraplength=75, command=lambda: self.select_image(width, height))
        btnSelectImage.config(width=10, height=2)

        # 클립보드에서 가져오기
        btnPasteFromClipboard = tk.Button(self, text='클립보드에서 가져오기', bg='yellow', wraplength=90, command=lambda: self.paste_from_clipboard(width, height))
        btnPasteFromClipboard.config(width=10, height=2)

        # 원본 그림 보기
        btnSeeOriginal = tk.Button(self, text='그림 원본 보기', bg='yellow', wraplength=75, command=self.see_original)
        btnSeeOriginal.config(width=10, height=2)

        # 기존 그림 지우기
        btnInitializeImage = tk.Button(self, text='초기화', bg='yellow', command=self.initialize_image)
        btnInitializeImage.config(width=10, height=2)

        # 안내용 라벨
        self.lblInfo = tk.Label(self)
        self.lblInfo.config(justify=tk.RIGHT, wraplength=width)

        # 편집에 사용된 단 수
        lblColumnsUsed = tk.Label(self, text='편집 시 사용할 단의 개수: ')
        self.cbbColmunsUsed = ttk.Combobox(self)   # 콤보 상자

        # 예상 난이도
        lblDifficulty = tk.Label(self, text='예상 난이도: ')
        self.cbbDifficulty = ttk.Combobox(self)

        conn = sqlite3.connect("mathProblemDB.db")  # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성

        cur.execute("SELECT columns FROM tblColumnsUsed ORDER BY columns")  # SQL 실행
        rows = cur.fetchall()   # 데이타 fetch
        self.cbbColmunsUsed['value'] =([row for row in rows])   # 가져온 데이타를 콤보 상자에 담기
        
        cur.execute("SELECT difficulty FROM tblDifficulty ORDER BY difficulty")  # SQL 실행
        rows = cur.fetchall()   # 데이타 fetch
        self.cbbDifficulty['value'] =([row for row in rows])   # 가져온 데이타를 콤보 상자에 담기

        conn.close()    # Connection 닫기

        # 프레임에 넣기. 기본은 N(아래쪽에 단추 배치)
        if pos == tk.S:
            lblTitle.grid(row=0, column=0, columnspan=8, sticky=tk.W)
            btnSelectImage.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            btnPasteFromClipboard.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
            btnSeeOriginal.grid(row=1, column=4, columnspan=2, padx=5, pady=5)
            btnInitializeImage.grid(row=1, column=6, columnspan=2, padx=5, pady=5)
            self.lblImage.grid(row=2, column=0, rowspan=4, columnspan=8, padx=5, pady=5, sticky=tk.NSEW)
            self.lblInfo.grid(row=6, column=0, columnspan=8, padx=2, sticky=tk.E)
            lblColumnsUsed.grid(row=7, column=0, columnspan=4, padx=2, pady=2, sticky=tk.E)
            self.cbbColmunsUsed.grid(row=7, column=4, columnspan=4, padx=2, pady=2, sticky=tk.EW)
            lblDifficulty.grid(row=8, column=0, columnspan=4, padx=2, pady=2, sticky=tk.E)
            self.cbbDifficulty.grid(row=8, column=4, columnspan=4, padx=2, pady=2, sticky=tk.EW)
        elif pos == tk.E:
            lblTitle.grid(row=0, column=0, columnspan=8, sticky=tk.W)
            btnSelectImage.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            btnPasteFromClipboard.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            btnSeeOriginal.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
            btnInitializeImage.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
            self.lblImage.grid(row=1, column=2, rowspan=4, columnspan=6, padx=5, pady=5, sticky=tk.NSEW)
            self.lblInfo.grid(row=5, column=2, columnspan=6, padx=2, sticky=tk.E)
            lblColumnsUsed.grid(row=6, column=2, columnspan=3, padx=2, pady=2, sticky=tk.E)
            self.cbbColmunsUsed.grid(row=6, column=5, columnspan=3, padx=2, pady=2, sticky=tk.EW)
            lblDifficulty.grid(row=7, column=2, columnspan=3, padx=2, pady=2, sticky=tk.E)
            self.cbbDifficulty.grid(row=7, column=5, columnspan=3, padx=2, pady=2, sticky=tk.EW)
        elif pos == tk.W:
            lblTitle.grid(row=0, column=0, columnspan=8, sticky=tk.W)
            self.lblImage.grid(row=1, column=0, rowspan=4, columnspan=6, padx=5, pady=5)
            btnSelectImage.grid(row=1, column=6, columnspan=2, padx=5, pady=5)
            btnPasteFromClipboard.grid(row=2, column=6, columnspan=2, padx=5, pady=5)
            btnSeeOriginal.grid(row=3, column=6, columnspan=2, padx=5, pady=5)
            btnInitializeImage.grid(row=4, column=6, columnspan=2, padx=5, pady=5)
            self.lblInfo.grid(row=5, column=0, columnspan=6, padx=2, sticky=tk.E)
            lblColumnsUsed.grid(row=6, column=0, columnspan=3, padx=2, pady=2, sticky=tk.E)
            self.cbbColmunsUsed.grid(row=6, column=3, columnspan=3, padx=2, pady=2, sticky=tk.EW)
            lblDifficulty.grid(row=7, column=0, columnspan=3, padx=2, pady=2, sticky=tk.E)
            self.cbbDifficulty.grid(row=7, column=3, columnspan=3, padx=2, pady=2, sticky=tk.EW)
        else:   # tk.N
            lblTitle.grid(row=0, column=0, columnspan=8, sticky=tk.W)
            self.lblImage.grid(row=1, column=0, rowspan=4, columnspan=8, padx=5, pady=5, sticky=tk.NSEW)
            btnSelectImage.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
            btnPasteFromClipboard.grid(row=5, column=2, columnspan=2, padx=5, pady=5)
            btnSeeOriginal.grid(row=5, column=4, columnspan=2, padx=5, pady=5)
            btnInitializeImage.grid(row=5, column=6, columnspan=2, padx=5, pady=5)
            self.lblInfo.grid(row=6, column=0, columnspan=8, padx=2, sticky=tk.E)
            lblColumnsUsed.grid(row=7, column=0, columnspan=4, padx=2, pady=2, sticky=tk.EW)
            self.cbbColmunsUsed.grid(row=7, column=4, columnspan=4, padx=2, pady=2, sticky=tk.EW)
            lblDifficulty.grid(row=8, column=0, columnspan=4, padx=2, pady=2, sticky=tk.EW)
            self.cbbDifficulty.grid(row=8, column=4, columnspan=4, padx=2, pady=2, sticky=tk.EW)

    def select_image(self, width, height):        
        # 파일 선택
        self.selectedFileName = filedialog.askopenfilename(title='그림 파일 선택')

        # 선택한 파일이 있을 때만 작업
        if self.selectedFileName != '':
            self.img = Image.open(self.selectedFileName)
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용)

            imageWidth = self.img.size[0]
            imageHeight = self.img.size[1]
            imageRatio = imageHeight/imageWidth
            labelRatio = height/width

            if imageRatio < labelRatio:
                if imageWidth > width:
                    newWidth = width
                    newHeight = int(width * imageRatio)
                else:   # imageWidth <= width
                    newWidth = imageWidth
                    newHeight = imageHeight
            else:   # imageRatio >= labelRatio
                if imageHeight > height:
                    newHeight = height
                    newWidth = int(height / imageRatio)
                else:   # imageHeight <= height
                    newHeight = imageHeight
                    newWidth = imageWidth

            self.img = self.img.resize((newWidth, newHeight), Image.ANTIALIAS)
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            #self.lblImage.config(image=self.original)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text=self.selectedFileName)  # 안내용 라벨에 읽어들인 파일 경로 표시

    def paste_from_clipboard(self, width, height):
        #self.img = ImageGrab.grabclipboard()
        self.img = ImageGrab.grabclipboard()

        if self.img != None:
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용): 이하 부분은 위와 동일하므로 함수로 만들 것을 고려할 것

            imageWidth = self.img.size[0]
            imageHeight = self.img.size[1]
            imageRatio = imageHeight/imageWidth
            labelRatio = height/width

            if imageRatio < labelRatio:
                if imageWidth > width:
                    newWidth = width
                    newHeight = int(width * imageRatio)
                else:   # imageWidth <= width
                    newWidth = imageWidth
                    newHeight = imageHeight
            else:   # imageRatio >= labelRatio
                if imageHeight > height:
                    newHeight = height
                    newWidth = int(height / imageRatio)
                else:   # imageHeight <= height
                    newHeight = imageHeight
                    newWidth = imageWidth

            self.img = self.img.resize((newWidth, newHeight), Image.ANTIALIAS)
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text='<클립보드>')  # 안내용 라벨

    def see_original(self):
        try:
            aWin = tk.Toplevel()
            aWin.title(self.selectedFileName)
            aWin.grab_set()

            aLabel = tk.Label(aWin)
            aLabel.config(image=self.original)
            aLabel.pack()
        except:
            pass

    def initialize_image(self):
        self.lblImage.config(image=self.defaultImage)
        self.isDefaultImageUsed = True
        self.lblInfo.config(text='')    # 안내용 라벨
        self.original = None



class MPBAnswerRegistration(tk.Frame):

    def __init__(self, parent, width=400, height=50, *args, **kwargs):
        #tk.Frame.__init__(self, parent, *args, **kwargs)
        tk.Frame.__init__(self, parent)

        # 제목
        lblTitle = tk.Label(self, text='<답 관련 정보>', font=HUGE_FONT, fg='blue')

        # 답 형식
        lblAnsType = tk.Label(self, text='답 형식: ')

        # 답 형식 선택을 위한 라디오 버튼
        self.ansTypeChoice = tk.IntVar()

        self.radAnsTypeObj = tk.Radiobutton(self, text='객관식', variable=self.ansTypeChoice, value=1, command=self.callback)
        self.radAnsTypeObj.select()
        self.radAnsTypeSubj = tk.Radiobutton(self, text='주관식', variable=self.ansTypeChoice, value=2, command=self.callback)

        # 객관식 답
        lblObjAns = tk.Label(self, text='객관식 답: ')
        self.cbbObjAns = ttk.Combobox(self)

        # 주관식 답
        lblSubjAns = tk.Label(self, text='주관식 답: ')
        lblSubjAnsInfo = tk.Label(self, text='(직접 입력)')

        self.enteredAns = tk.StringVar()
        self.txtSubjAns = tk.Entry(self, textvariable=self.enteredAns)
        #self.enteredAns.set("<입력하세요.>")

        conn = sqlite3.connect("mathProblemDB.db")  # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성
        cur.execute("SELECT ansNo FROM tblObjAns ORDER BY ansNo")   # SQL 실행
        rows = cur.fetchall()   # 데이타 fetch
        self.cbbObjAns['value'] =([row for row in rows])   # 가져온 데이타를 콤보 상자에 담기
        conn.close()    # Connection 닫기

        # 명령 단추
        btnSelectImage = tk.Button(self, text='그림 파일 선택', bg='yellow', wraplength=75, command=lambda: self.select_image(width, height))   # 그림 파일 선택
        btnSelectImage.config(width=10, height=2)

        btnPasteFromClipboard = tk.Button(self, text='클립보드에서 가져오기', bg='yellow', wraplength=90, command=lambda: self.paste_from_clipboard(width, height))    # 클립보드에서 가져오기
        btnPasteFromClipboard.config(width=10, height=2)

        btnSeeOriginal = tk.Button(self, text='그림 원본 보기', bg='yellow', wraplength=75, command=self.see_original)   # 원본 그림 보기
        btnSeeOriginal.config(width=10, height=2)

        btnInitializeImage = tk.Button(self, text='초기화', bg='yellow', command=self.initialize_image) # 기존 그림 지우기
        btnInitializeImage.config(width=10, height=2)

        # 기본 배경 그림
        self.img = Image.open(DEFAULT_BACKGROUND)
        self.defaultImage = ImageTk.PhotoImage(self.img)
        self.isDefaultImageUsed = True

        # 라벨(그림)
        self.lblImage = tk.Label(self, image=self.defaultImage, bg='grey')
        self.lblImage.config(width=width, height=height, relief=tk.SUNKEN)

        # 안내용 라벨
        self.lblInfo = tk.Label(self)
        self.lblInfo.config(justify=tk.RIGHT, wraplength=width)

        # 도움말
        lblHelp = tk.Label(self, text="직접 입력한 답과 그림이 동시에 있으면 직접 입력한 답을 사용합니다.", fg='green')

        # 그릇에 담기
        lblTitle.grid(row=0, column=0, columnspan=14, padx=2, pady=2, sticky=tk.W)
        lblAnsType.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=tk.E)
        self.radAnsTypeObj.grid(row=1, column=2, columnspan=2, padx=2, pady=2, sticky=tk.W)
        self.radAnsTypeSubj.grid(row=1, column=4, columnspan=2, padx=2, pady=2, sticky=tk.W)
        lblObjAns.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky=tk.E)
        self.cbbObjAns.grid(row=2, column=2, columnspan=4, padx=2, pady=2)
        lblSubjAns.grid(row=3, column=0, columnspan=2, padx=2, pady=2, sticky=tk.E)
        lblSubjAnsInfo.grid(row=3, column=2, columnspan=2, padx=2, pady=2, sticky=tk.W)
        self.txtSubjAns.grid(row=3, column=4, columnspan=10, padx=2, pady=2, stick=tk.EW)
        btnSelectImage.grid(row=4, column=2, columnspan=3, padx=5, pady=5)
        btnPasteFromClipboard.grid(row=4, column=5, columnspan=3, padx=5, pady=5)
        btnSeeOriginal.grid(row=4, column=8, columnspan=3, padx=5, pady=5)
        btnInitializeImage.grid(row=4, column=11, columnspan=3, padx=5, pady=5)
        self.lblImage.grid(row=5, column=2, columnspan=12, padx=5, pady=5, sticky=tk.NSEW)
        self.lblInfo.grid(row=6, column=2, columnspan=12, padx=2, sticky=tk.E)
        lblHelp.grid(row=7, column=2, columnspan=12, padx=2, sticky=tk.EW)

    def select_image(self, width, height):
        # 파일 선택
        self.selectedFileName = filedialog.askopenfilename(title='그림 파일 선택')

        # 선택한 파일이 있을 때만 작업
        if self.selectedFileName != '':
            self.img = Image.open(self.selectedFileName)
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용)

            imageWidth = self.img.size[0]
            imageHeight = self.img.size[1]
            imageRatio = imageHeight/imageWidth
            labelRatio = height/width

            if imageRatio < labelRatio:
                if imageWidth > width:
                    newWidth = width
                    newHeight = int(width * imageRatio)
                else:   # imageWidth <= width
                    newWidth = imageWidth
                    newHeight = imageHeight
            else:   # imageRatio >= labelRatio
                if imageHeight > height:
                    newHeight = height
                    newWidth = int(height / imageRatio)
                else:   # imageHeight <= height
                    newHeight = imageHeight
                    newWidth = imageWidth

            self.img = self.img.resize((newWidth, newHeight), Image.ANTIALIAS)
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text=self.selectedFileName)  # 안내용 라벨에 읽어들인 파일 경로 표시

    def paste_from_clipboard(self, width, height):
        self.img = ImageGrab.grabclipboard()

        if self.img != None:
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용): 이하 부분은 위와 동일하므로 함수로 만들 것을 고려할 것

            imageWidth = self.img.size[0]
            imageHeight = self.img.size[1]
            imageRatio = imageHeight/imageWidth
            labelRatio = height/width

            if imageRatio < labelRatio:
                if imageWidth > width:
                    newWidth = width
                    newHeight = int(width * imageRatio)
                else:   # imageWidth <= width
                    newWidth = imageWidth
                    newHeight = imageHeight
            else:   # imageRatio >= labelRatio
                if imageHeight > height:
                    newHeight = height
                    newWidth = int(height / imageRatio)
                else:   # imageHeight <= height
                    newHeight = imageHeight
                    newWidth = imageWidth

            self.img = self.img.resize((newWidth, newHeight), Image.ANTIALIAS)
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text='<클립보드>')  # 안내용 라벨

    def see_original(self):
        try:
            aWin = tk.Toplevel()
            aWin.title(self.selectedFileName)
            aWin.grab_set()

            aLabel = tk.Label(aWin)
            aLabel.config(image=self.original)
            aLabel.pack()
        except:
            pass

    def initialize_image(self):
        self.lblImage.config(image=self.defaultImage)
        self.isDefaultImageUsed = True
        self.lblInfo.config(text='')    # 안내용 라벨
        self.original = None

    def callback(self):
        pass
        #print(self.ansTypeChoice.get()) # 라디오 버튼에서 선택한 값을 출력(1: 객관식, 2: 주관식)



class MPBSolutionRegistration(tk.Frame):

    def __init__(self, parent, width=400, height=150, pos=tk.N, *args, **kwargs):
        #tk.Frame.__init__(self, parent, *args, **kwargs)
        tk.Frame.__init__(self, parent)

        # 제목
        lblTitle = tk.Label(self, text='<풀이 관련 정보(선택)>', font=HUGE_FONT, fg='blue')

        # 명령 단추
        btnSelectImage = tk.Button(self, text='그림 파일 선택', bg='yellow', wraplength=75, command=lambda: self.select_image(width, height))   # 그림 파일 선택
        btnSelectImage.config(width=10, height=2)

        btnPasteFromClipboard = tk.Button(self, text='클립보드에서 가져오기', bg='yellow', wraplength=90, command=lambda: self.paste_from_clipboard(width, height))    # 클립보드에서 가져오기
        btnPasteFromClipboard.config(width=10, height=2)

        btnSeeOriginal = tk.Button(self, text='그림 원본 보기', bg='yellow', wraplength=75, command=self.see_original)   # 원본 그림 보기
        btnSeeOriginal.config(width=10, height=2)

        btnInitializeImage = tk.Button(self, text='초기화', bg='yellow', command=self.initialize_image) # 기존 그림 지우기
        btnInitializeImage.config(width=10, height=2)

        # 기본 배경 그림
        self.img = Image.open(DEFAULT_BACKGROUND)
        self.defaultImage = ImageTk.PhotoImage(self.img)
        self.isDefaultImageUsed = True

        # 라벨(그림)
        self.lblImage = tk.Label(self, image=self.defaultImage, bg='grey')
        self.lblImage.config(width=width, height=height, relief=tk.SUNKEN)

        # 안내용 라벨
        self.lblInfo = tk.Label(self)
        self.lblInfo.config(justify=tk.RIGHT, wraplength=width)

        # 프레임에 넣기. 기본은 N(아래쪽에 단추 배치)
        if pos == tk.S:
            lblTitle.grid(row=0, column=0, columnspan=8, sticky=tk.W)
            btnSelectImage.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            btnPasteFromClipboard.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
            btnSeeOriginal.grid(row=1, column=4, columnspan=2, padx=5, pady=5)
            btnInitializeImage.grid(row=1, column=6, columnspan=2, padx=5, pady=5)
            self.lblImage.grid(row=2, column=0, rowspan=4, columnspan=8, padx=5, pady=5, sticky=tk.NSEW)
            self.lblInfo.grid(row=6, column=0, columnspan=8, padx=2, sticky=tk.E)
        elif pos == tk.E:
            lblTitle.grid(row=0, column=0, columnspan=8, sticky=tk.W)
            btnSelectImage.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            btnPasteFromClipboard.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            btnSeeOriginal.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
            btnInitializeImage.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
            self.lblImage.grid(row=1, column=2, rowspan=4, columnspan=6, padx=5, pady=5, sticky=tk.NSEW)
            self.lblInfo.grid(row=5, column=2, columnspan=6, padx=2, sticky=tk.E)
        elif pos == tk.W:
            lblTitle.grid(row=0, column=0, columnspan=8, sticky=tk.W)
            self.lblImage.grid(row=1, column=0, rowspan=4, columnspan=6, padx=5, pady=5)
            btnSelectImage.grid(row=1, column=6, columnspan=2, padx=5, pady=5)
            btnPasteFromClipboard.grid(row=2, column=6, columnspan=2, padx=5, pady=5)
            btnSeeOriginal.grid(row=3, column=6, columnspan=2, padx=5, pady=5)
            btnInitializeImage.grid(row=4, column=6, columnspan=2, padx=5, pady=5)
            self.lblInfo.grid(row=5, column=0, columnspan=6, padx=2, sticky=tk.E)
        else:   # N
            lblTitle.grid(row=0, column=0, columnspan=8, sticky=tk.W)
            self.lblImage.grid(row=1, column=0, rowspan=4, columnspan=8, padx=5, pady=5, sticky=tk.NSEW)
            btnSelectImage.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
            btnPasteFromClipboard.grid(row=5, column=2, columnspan=2, padx=5, pady=5)
            btnSeeOriginal.grid(row=5, column=4, columnspan=2, padx=5, pady=5)
            btnInitializeImage.grid(row=5, column=6, columnspan=2, padx=5, pady=5)
            self.lblInfo.grid(row=6, column=0, columnspan=8, padx=2, sticky=tk.E)

    def select_image(self, width, height):        
        # 파일 선택
        self.selectedFileName = filedialog.askopenfilename(title='그림 파일 선택')

        # 선택한 파일이 있을 때만 작업
        if self.selectedFileName != '':
            self.img = Image.open(self.selectedFileName)
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용)

            imageWidth = self.img.size[0]
            imageHeight = self.img.size[1]
            imageRatio = imageHeight/imageWidth
            labelRatio = height/width

            if imageRatio < labelRatio:
                if imageWidth > width:
                    newWidth = width
                    newHeight = int(width * imageRatio)
                else:   # imageWidth <= width
                    newWidth = imageWidth
                    newHeight = imageHeight
            else:   # imageRatio >= labelRatio
                if imageHeight > height:
                    newHeight = height
                    newWidth = int(height / imageRatio)
                else:   # imageHeight <= height
                    newHeight = imageHeight
                    newWidth = imageWidth

            self.img = self.img.resize((newWidth, newHeight), Image.ANTIALIAS)
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text=self.selectedFileName)  # 안내용 라벨에 읽어들인 파일 경로 표시

    def paste_from_clipboard(self, width, height):
        self.img = ImageGrab.grabclipboard()

        if self.img != None:
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용): 이하 부분은 위와 동일하므로 함수로 만들 것을 고려할 것

            imageWidth = self.img.size[0]
            imageHeight = self.img.size[1]
            imageRatio = imageHeight/imageWidth
            labelRatio = height/width

            if imageRatio < labelRatio:
                if imageWidth > width:
                    newWidth = width
                    newHeight = int(width * imageRatio)
                else:   # imageWidth <= width
                    newWidth = imageWidth
                    newHeight = imageHeight
            else:   # imageRatio >= labelRatio
                if imageHeight > height:
                    newHeight = height
                    newWidth = int(height / imageRatio)
                else:   # imageHeight <= labelHeight
                    newHeight = imageHeight
                    newWidth = imageWidth

            self.img = self.img.resize((newWidth, newHeight), Image.ANTIALIAS)
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text='<클립보드>')  # 안내용 라벨

    def see_original(self):
        try:
            aWin = tk.Toplevel()
            aWin.title(self.selectedFileName)
            aWin.grab_set()

            aLabel = tk.Label(aWin)
            aLabel.config(image=self.original)
            aLabel.pack()
        except:
            pass

    def initialize_image(self):
        self.lblImage.config(image=self.defaultImage)
        self.isDefaultImageUsed = True
        self.lblInfo.config(text='')    # 안내용 라벨
        self.original = None



def register_image_problem(ctrlProblemType):
    if ctrlProblemType.getSelectedProblemTypeID() == 0: # 문제 유형 ID, 문제 유형이 아니거나(즉, 책, 부, 장, 절) 선택한 것이 없으면 0을 반환한다.
        messagebox.showerror("문제 유형 없음", "문제 유형을 선택하세요.")
    else:
        print(ctrlProblemType.getSelectedProblemTypeID())

if __name__ == '__main__':
    root=tk.Tk()
    #root.geometry("640x480")
    tk.Tk.iconbitmap(root, default="sum64.ico")
    tk.Tk.wm_title(root, "수학 문제 은행")

    # 이 명령으로 인해 프레임 안의 위젯의 크기가 프레임의 크기에 맞추어진다. 프레임의 크기가 클 경우에만 적용된다.
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.resizable(width=False, height=False)

    aTree = MPBCurriTreeView(root)
    aTree.grid(row=0, column=0, rowspan=30, columnspan=30, padx=10, pady=10)

    anImageRegistration = MPBProblemImageRegistration(root, width=400, height=300, pos=tk.N)
    anImageRegistration.grid(row=0, column=30, rowspan=30, columnspan=20, padx=10, pady=10)

    aAns = MPBAnswerRegistration(root, width=400, height=50)
    aAns.grid(row=30, column=0, rowspan=20, columnspan=30, sticky=tk.N+tk.W, padx=10, pady=10)

    aSol = MPBSolutionRegistration(root, width=400, height=175)
    aSol.grid(row=30, column=30, rowspan=20, columnspan=20, sticky=tk.N+tk.W, padx=10, pady=10)

    frmOkCancel = tk.Frame(root)   # 확인/취소 버튼을 위한 프레임

    btnOk = tk.Button(frmOkCancel, text='확인', fg='white', bg='blue', font=HUGE_FONT, command=lambda: register_image_problem(aTree))
    btnCancel = tk.Button(frmOkCancel, text='취소', fg='white', bg='blue', font=HUGE_FONT, command=lambda: root.destroy())
    btnOk.grid(row=0, column=0, padx=5, pady=5)
    btnCancel.grid(row=0, column=1, padx=5, pady=5)

    frmOkCancel.grid(row=50, column=0, columnspan=50, padx=10, pady=10)

    root.mainloop()