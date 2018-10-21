from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image, ImageGrab
import sqlite3

HUGE_FONT = ('맑은 고딕', 14, "bold")
LARGE_FONT = ('맑은 고딕', 11)

DEFAULT_BACKGROUND = '.\\coffee.jpeg'

class MPBCurriTreeView(Frame):

    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky=N+W):
        Frame.__init__(self, master)
        
        # 트리에서 선택된 항목의 종류와 ID(기본값)
        self.selectedCurriLevel = ''
        self.selectedCurriID = 0
        self.selectedProblemTypeID = 0

        # 트리와 스크롤바를 담기 위한 그릇
        #self.container = ttk.Frame(master, padding=(3,3,12,12))
        self.container = Frame(master)
        #self.container.config(bg='black')

        self.lblTitle = Label(self.container, text="<문제 유형 선택>", font=HUGE_FONT)  # 제목
        self.lblTitle.config(fg='blue')
        self.trvCurri = ttk.Treeview(self.container, height=20, selectmode='browse')    # 트리 만들기
        #self.treeXScroll = ttk.Scrollbar(self.container, orient=HORIZONTAL)   # 수평 스크롤바 만들기(트리에는 수평 스크롤바가 필요 없는 듯)
        self.treeYScroll = ttk.Scrollbar(self.container, orient=VERTICAL)   # 수직 스크롤바 만들기
        self.lblSelectedCurriLevel = Label(self.container, text='구분')   # 선택한 항목 구분
        self.lblSelectedCurriName = Label(self.container, text='이름', fg='blue')   # 선택한 항목 이름
        self.lblSelectedCurriID = Label(self.container, text='ID') # 선택한 항목 ID

        #self.trvCurri.bind('<ButtonRelease-1>', self.doSomething)    # 클릭했을 때 할 일
        self.trvCurri.bind('<<TreeviewSelect>>', self.treeview_selected)

        # 수평 스크롤바(불필요한 듯)
        #self.treeXScroll.configure(command=self.trvCurri.yview)
        #self.trvCurri.configure(xscrollcommand=self.treeXScroll.set)

        # 수직 스크롤바
        self.treeYScroll.configure(command=self.trvCurri.xview)
        self.trvCurri.configure(yscrollcommand=self.treeYScroll.set)

        # 그려 넣기
        #self.container.grid(row=row, column=column, sticky=(N, S, E, W)) # 그릇 그려 넣기. 인스턴스를 생성한 곳에서 이 그릇을 넣을 프레임 등(인수로 받음)을 만들어야 한다.
        self.lblTitle.grid(row=0, column=0, columnspan=11, sticky=W)
        self.trvCurri.grid(row=1, column=0, columnspan=10, sticky=(N, S, E, W))    # 트리를 그릇에 넣기
        #self.trvCurri.pack(side=LEFT)
        #self.treeXScroll.grid(row=1, column=0, columnspan=2, sticky=E+W)  # 수평 스크롤바를 그릇에 넣기
        self.treeYScroll.grid(row=1, column=10, sticky=N+S)  # 수직 스크롤바를 그릇에 넣기
        #self.treeYScroll.pack(side=LEFT)
        self.lblSelectedCurriLevel.grid(row=2, column=0, padx=10, sticky=E)
        self.lblSelectedCurriName.grid(row=2, column=1, columnspan=8, sticky=W)
        #self.lblSelectedCurriType.pack(side=BOTTOM)
        self.lblSelectedCurriID.grid(row=2, column=9, sticky=E, padx=5)
        #self.lblSelectedCurriID.pack(side=LEFT)
        self.container.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=10, pady=10, stick=sticky)

        # Handling Resize
        self.container.rowconfigure(0, weight=1)
        
        for i in range(1, 10):
            self.container.columnconfigure(i, weight=1)

        # Treeview 제목 설정
        self.trvCurri.config(columns=('alive'))
        self.trvCurri.column('alive', width=135, anchor='center')
        self.trvCurri.column('#0', width=425)
        self.trvCurri.heading('alive', text='교육 과정 내인지 여부')

        # 데이타베이스에 연결해서 데이타 가져오기
        conn = sqlite3.connect("mathProblemDB.db")  # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성
        cur.execute("SELECT id, name FROM tblBook ORDER BY priority")   # SQL 실행
        rows = cur.fetchall()   # 데이타 fetch

        # 교육 과정 관련 트리 만들기
        for row in rows:
            bookID = str(row[0])
            #self.trvCurri.insert('', 'end', 'book' + bookID, text=row[1], tag='book-' + bookID)
            self.trvCurri.insert('', 'end', 'book-' + bookID, text=row[1], tag='book')

            # 책 아래에 파트 추가
            sqlStr = "SELECT id, name FROM tblPart WHERE bookID = " + str(row[0]) + " ORDER BY priority"
            cur.execute(sqlStr)
            secondRows = cur.fetchall()

            for secondRow in secondRows:
                partID = str(secondRow[0])
                #self.trvCurri.insert('book' + bookID, 'end', 'part' + partID, text=secondRow[1], tag='part-' + partID)
                self.trvCurri.insert('book-' + bookID, 'end', 'part-' + partID, text=secondRow[1], tag='part')

                # 파트 아래에 장 추가
                sqlStr = "SELECT id, name FROM tblChapter WHERE partID = " + str(secondRow[0]) + " ORDER BY priority"
                cur.execute(sqlStr)
                thirdRows = cur.fetchall()

                for thirdRow in thirdRows:
                    chapterID = str(thirdRow[0])
                    #self.trvCurri.insert('part' + partID, 'end', 'chapter' + chapterID, text=thirdRow[1], tag='chapter-' + chapterID)
                    self.trvCurri.insert('part-' + partID, 'end', 'chapter-' + chapterID, text=thirdRow[1], tag='chapter')

                    # 장 아래에 절 추가
                    sqlStr = "SELECT id, name FROM tblSection WHERE chapterID = " + str(thirdRow[0]) + " ORDER BY priority"
                    cur.execute(sqlStr)
                    fourthRows = cur.fetchall()

                    for fourthRow in fourthRows:
                        sectionID = str(fourthRow[0])
                        #self.trvCurri.insert('chapter' + chapterID, 'end', 'section' + sectionID, text=fourthRow[1], tag='section-' + sectionID)
                        self.trvCurri.insert('chapter-' + chapterID, 'end', 'section-' + sectionID, text=fourthRow[1], tag='section')

                        # 절 아래에 절 추가
                        sqlStr = "SELECT id, name, alive FROM tblProblemType WHERE sectionID = " + str(fourthRow[0]) + " ORDER BY priority"
                        cur.execute(sqlStr)
                        fifthRows = cur.fetchall()

                        for fifthRow in fifthRows:
                            problemTypeID = str(fifthRow[0])
                            #self.trvCurri.insert('section' + sectionID, 'end', 'problemType' + problemTypeID, text=fifthRow[1], tag='problemType-' + problemTypeID)
                            #self.trvCurri.insert('section-' + sectionID, 'end', 'problemType-' + problemTypeID, text=fifthRow[1], tag='problemType')
                            
                            if fifthRow[2]:
                                self.trvCurri.insert('section-' + sectionID, 'end', 'problemType-' + problemTypeID, text=fifthRow[1], tag='alive')
                                self.trvCurri.set('problemType-' + problemTypeID, 'alive', 'O')
                            else:
                                self.trvCurri.insert('section-' + sectionID, 'end', 'problemType-' + problemTypeID, text=fifthRow[1], tag='dead')
                                self.trvCurri.set('problemType-' + problemTypeID, 'alive', 'X')

        # 트리 색칠
        #self.trvCurri.tag_configure('book', background='yellow')
        #self.trvCurri.tag_configure('part', background='skyblue')
        self.trvCurri.tag_configure('alive', foreground='blue')
        self.trvCurri.tag_configure('dead', background='#C1C1C1', foreground='red') # 교육 과정 밖의 유형은 배경 회색, 글 빨간색으로 처리

        conn.close()    # 데이터베이스에 대한 연결 닫기
    
    # 트리의 어떤 항목이 선택되었을 때 실행되는 함수
    def treeview_selected(self, event):
        #print(self.trvCurri.selection())
        #print(self.trvCurri.focus().split('-')[0], self.trvCurri.focus().split('-')[1]) # 처음 것은 book, part, chapter, section, problemType 중 하나, 뒤에 것은 ID
        self.selectedCurriLevel = self.trvCurri.focus().split('-')[0]
        self.selectedCurriID = self.trvCurri.focus().split('-')[1]
        #print(self.selectedCurriType, self.selectedCurriID)
        #print(self.trvCurri.item(self.trvCurri.focus())['text'])

        # 선택한 항목의 구분 알리기
        #self.lblSelectedCurriLevel['text'] = self.selectedCurriLevel
        if self.selectedCurriLevel == 'book':
            self.lblSelectedCurriLevel['text'] = '책'
        elif self.selectedCurriLevel == 'part':
            self.lblSelectedCurriLevel['text'] = '부'
        elif self.selectedCurriLevel == 'chapter':
            self.lblSelectedCurriLevel['text'] = '장'
        elif self.selectedCurriLevel == 'section':
            self.lblSelectedCurriLevel['text'] = '절'
        elif self.selectedCurriLevel == 'problemType':
            self.lblSelectedCurriLevel['text'] = '문제 유형'

        # 선택한 항목의 이름 알리기
        self.lblSelectedCurriName['text'] = self.trvCurri.item(self.trvCurri.focus())['text']

        # 선택한 항목의 ID 알리기
        self.lblSelectedCurriID['text'] = self.selectedCurriID

        #print(self.getSelectedProblemTypeID())

    # 트리의 선택된 문제 유형 이름과 번호를 알려준다. 선택된 것이 없거나 문제 유형이 아니면(즉 책, 부, 장, 절이면) 0을 반환한다.
    def getSelectedProblemTypeID(self):
        if self.selectedCurriLevel == 'problemType':
            return self.lblSelectedCurriID['text']
        else:
            return 0

    # 임시
    #def doSomething(self, event):
    #    curItem = self.trvCurri.focus()
    #    print(self.trvCurri.item(curItem)['tags'][0].split('-')[0], self.trvCurri.item(curItem)['tags'][0].split('-')[1])



class MPBProblemImageRegistration(Frame):

    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, width=400, height=300, pos=N, sticky=N+W):
        # 인수로 주어진 width와 height는 전체 크기가 아니라 그림 영역의 크기이다.
        # 인수 pos는 명령 단추가 놓일 곳을 가리킨다. (N, S, E, W)

        Frame.__init__(self, master)
        #print(master.winfo_width(), master.winfo_height())

        self.container = Frame(master)

        # 제목
        self.lblTitle = Label(self.container, text='<문제 그림 선택>', font=HUGE_FONT)
        self.lblTitle.config(fg='blue')

        # 기본 배경 그림
        self.img = Image.open(DEFAULT_BACKGROUND)
        self.defaultImage = ImageTk.PhotoImage(self.img)
        self.isDefaultImageUsed = True

        # 라벨(그림)
        self.lblImage = Label(self.container, image=self.defaultImage, bg='grey')
        self.lblImage.config(width=width, height=height, relief=SUNKEN)

        # 라벨 크기
        self.labelWidth = width
        self.labelHeight = height
        self.labelRatio = height/width
        
        # 명령 단추
        # 그림 파일 선택
        self.btnSelectImage = Button(self.container, text='그림 파일 선택', bg='yellow', 
                              wraplength=75, command=self.select_image)
        self.btnSelectImage.config(width=10, height=2)

        # 클립보드에서 가져오기
        self.btnPasteFromClipboard = Button(self.container, text='클립보드에서 가져오기', bg='yellow',
                                     wraplength=90, command=self.paste_from_clipboard)
        self.btnPasteFromClipboard.config(width=10, height=2)

        # 원본 그림 보기
        self.btnSeeOriginal = Button(self.container, text='그림 원본 보기', bg='yellow', 
                              wraplength=75, command=self.see_original)
        self.btnSeeOriginal.config(width=10, height=2)

        # 기존 그림 지우기
        self.btnInitializeImage = Button(self.container, text='초기화', bg='yellow',
                                  command=self.initialize_image)
        self.btnInitializeImage.config(width=10, height=2)

        # 안내용 라벨
        self.lblInfo = Label(self.container)
        self.lblInfo.config(justify=RIGHT, wraplength=width)

        # 편집에 사용된 단 수
        self.lblColumnsUsed = Label(self.container, text='편집 시 사용할 단의 개수: ')
        self.cbbColmunsUsed = ttk.Combobox(self.container)   # 콤보 상자

        # 예상 난이도
        self.lblDifficulty = Label(self.container, text='예상 난이도: ')
        self.cbbDifficulty = ttk.Combobox(self.container)

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
        if pos == S:
            self.lblTitle.grid(row=0, column=0, columnspan=8, sticky=W)
            self.btnSelectImage.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            self.btnPasteFromClipboard.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
            self.btnSeeOriginal.grid(row=1, column=4, columnspan=2, padx=5, pady=5)
            self.btnInitializeImage.grid(row=1, column=6, columnspan=2, padx=5, pady=5)
            self.lblImage.grid(row=2, column=0, rowspan=4, columnspan=8, padx=5, pady=5, sticky=NSEW)
            self.lblInfo.grid(row=6, column=0, columnspan=8, padx=2, sticky=E)
            self.lblColumnsUsed.grid(row=7, column=0, columnspan=4, padx=2, pady=2, sticky=E)
            self.cbbColmunsUsed.grid(row=7, column=4, columnspan=4, padx=2, pady=2, sticky=EW)
            self.lblDifficulty.grid(row=8, column=0, columnspan=4, padx=2, pady=2, sticky=E)
            self.cbbDifficulty.grid(row=8, column=4, columnspan=4, padx=2, pady=2, sticky=EW)
        elif pos == E:
            self.lblTitle.grid(row=0, column=0, columnspan=8, sticky=W)
            self.btnSelectImage.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            self.btnPasteFromClipboard.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            self.btnSeeOriginal.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
            self.btnInitializeImage.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
            self.lblImage.grid(row=1, column=2, rowspan=4, columnspan=6, padx=5, pady=5, sticky=NSEW)
            self.lblInfo.grid(row=5, column=2, columnspan=6, padx=2, sticky=E)
            self.lblColumnsUsed.grid(row=6, column=2, columnspan=3, padx=2, pady=2, sticky=E)
            self.cbbColmunsUsed.grid(row=6, column=5, columnspan=3, sticky=EW, padx=2, pady=2)
            self.lblDifficulty.grid(row=7, column=2, columnspan=3, padx=2, pady=2, sticky=E)
            self.cbbDifficulty.grid(row=7, column=5, columnspan=3, sticky=EW, padx=2, pady=2)
        elif pos == W:
            self.lblTitle.grid(row=0, column=0, columnspan=8, sticky=W)
            self.lblImage.grid(row=1, column=0, rowspan=4, columnspan=6, padx=5, pady=5)
            self.btnSelectImage.grid(row=1, column=6, columnspan=2, padx=5, pady=5)
            self.btnPasteFromClipboard.grid(row=2, column=6, columnspan=2, padx=5, pady=5)
            self.btnSeeOriginal.grid(row=3, column=6, columnspan=2, padx=5, pady=5)
            self.btnInitializeImage.grid(row=4, column=6, columnspan=2, padx=5, pady=5)
            self.lblInfo.grid(row=5, column=0, columnspan=6, padx=2, sticky=E)
            self.lblColumnsUsed.grid(row=6, column=0, columnspan=3, padx=2, pady=2, sticky=E)
            self.cbbColmunsUsed.grid(row=6, column=3, columnspan=3, sticky=EW, padx=2, pady=2)
            self.lblDifficulty.grid(row=7, column=0, columnspan=3, padx=2, pady=2, sticky=E)
            self.cbbDifficulty.grid(row=7, column=3, columnspan=3, sticky=EW, padx=2, pady=2)
        else:   # N
            self.lblTitle.grid(row=0, column=0, columnspan=8, sticky=W)
            self.lblImage.grid(row=1, column=0, rowspan=4, columnspan=8, padx=5, pady=5, sticky=NSEW)
            self.btnSelectImage.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
            self.btnPasteFromClipboard.grid(row=5, column=2, columnspan=2, padx=5, pady=5)
            self.btnSeeOriginal.grid(row=5, column=4, columnspan=2, padx=5, pady=5)
            self.btnInitializeImage.grid(row=5, column=6, columnspan=2, padx=5, pady=5)
            self.lblInfo.grid(row=6, column=0, columnspan=8, padx=2, sticky=E)
            self.lblColumnsUsed.grid(row=7, column=0, columnspan=4, padx=2, pady=2, sticky=E)
            self.cbbColmunsUsed.grid(row=7, column=4, columnspan=4, padx=2, pady=2, sticky=EW)
            self.lblDifficulty.grid(row=8, column=0, columnspan=4, padx=2, pady=2, sticky=E)
            self.cbbDifficulty.grid(row=8, column=4, columnspan=4, padx=2, pady=2, sticky=EW)

        self.container.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=10, pady=10, sticky=sticky)

    def select_image(self):        
        # 파일 선택
        self.selectedFileName = filedialog.askopenfilename(title='그림 파일 선택')

        # 선택한 파일이 있을 때만 작업
        if self.selectedFileName != '':
            self.img = Image.open(self.selectedFileName)
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용)

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
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            #self.lblImage.config(image=self.original)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text=self.selectedFileName)  # 안내용 라벨에 읽어들인 파일 경로 표시

    def paste_from_clipboard(self):
        self.img = ImageGrab.grabclipboard()

        if self.img != None:
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용): 이하 부분은 위와 동일하므로 함수로 만들 것을 고려할 것

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
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text='<클립보드>')  # 안내용 라벨

    def see_original(self):
        try:
            aWin = Toplevel()
            aWin.title(self.selectedFileName)
            aWin.grab_set()

            aLabel = Label(aWin)
            aLabel.config(image=self.original)
            aLabel.pack()
        except:
            pass

    def initialize_image(self):
        self.lblImage.config(image=self.defaultImage)
        self.isDefaultImageUsed = True
        self.lblInfo.config(text='')    # 안내용 라벨
        self.original = None



class MPBAnswerRegistration(Frame):

    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, width=400, height=50, sticky=N+W):
        Frame.__init__(self, master)

        self.container = Frame(master)

        # 제목
        self.lblTitle = Label(self.container, text='<답 관련 정보>', font=HUGE_FONT, fg='blue')

        # 답 형식
        self.lblAnsType = Label(self.container, text='답 형식: ')

        # 답 형식 선택을 위한 라디오 버튼
        self.ansTypeChoice = IntVar()

        self.radAnsTypeObj = Radiobutton(self.container, text='객관식', variable=self.ansTypeChoice, value=1, command=self.callback)
        self.radAnsTypeObj.select()
        self.radAnsTypeSubj = Radiobutton(self.container, text='주관식', variable=self.ansTypeChoice, value=2, command=self.callback)

        # 객관식 답
        self.lblObjAns = Label(self.container, text='객관식 답: ')
        self.cbbObjAns = ttk.Combobox(self.container)

        # 주관식 답
        self.lblSubjAns = Label(self.container, text='주관식 답: ')
        self.lblSubjAnsInfo = Label(self.container, text='(직접 입력)')

        self.enteredAns = StringVar()
        self.txtSubjAns = Entry(self.container, textvariable=self.enteredAns)
        #self.enteredAns.set("<입력하세요.>")

        conn = sqlite3.connect("mathProblemDB.db")  # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성
        cur.execute("SELECT ansNo FROM tblObjAns ORDER BY ansNo")   # SQL 실행
        rows = cur.fetchall()   # 데이타 fetch
        self.cbbObjAns['value'] =([row for row in rows])   # 가져온 데이타를 콤보 상자에 담기
        conn.close()    # Connection 닫기

        # 명령 단추
        self.btnSelectImage = Button(self.container, text='그림 파일 선택', bg='yellow', wraplength=75, command=self.select_image)   # 그림 파일 선택
        self.btnSelectImage.config(width=10, height=2)

        self.btnPasteFromClipboard = Button(self.container, text='클립보드에서 가져오기', bg='yellow', wraplength=90, command=self.paste_from_clipboard)    # 클립보드에서 가져오기
        self.btnPasteFromClipboard.config(width=10, height=2)

        self.btnSeeOriginal = Button(self.container, text='그림 원본 보기', bg='yellow', wraplength=75, command=self.see_original)   # 원본 그림 보기
        self.btnSeeOriginal.config(width=10, height=2)

        self.btnInitializeImage = Button(self.container, text='초기화', bg='yellow', command=self.initialize_image) # 기존 그림 지우기
        self.btnInitializeImage.config(width=10, height=2)

        # 기본 배경 그림
        self.img = Image.open(DEFAULT_BACKGROUND)
        self.defaultImage = ImageTk.PhotoImage(self.img)
        self.isDefaultImageUsed = True

        # 라벨(그림)
        self.lblImage = Label(self.container, image=self.defaultImage, bg='grey')
        self.lblImage.config(width=width, height=height, relief=SUNKEN)

        # 라벨 크기
        self.labelWidth = width
        self.labelHeight = height
        self.labelRatio = height/width

        # 안내용 라벨
        self.lblInfo = Label(self.container)
        self.lblInfo.config(justify=RIGHT, wraplength=width)

        # 도움말
        self.lblHelp = Label(self.container, text="직접 입력한 답과 그림이 동시에 있으면 직접 입력한 답을 사용합니다.", fg='green')

        # 그릇에 담기
        self.lblTitle.grid(row=0, column=0, columnspan=14, padx=2, pady=2, sticky=W)
        self.lblAnsType.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=E)
        self.radAnsTypeObj.grid(row=1, column=2, columnspan=2, padx=2, pady=2, sticky=W)
        self.radAnsTypeSubj.grid(row=1, column=4, columnspan=2, padx=2, pady=2, sticky=W)
        self.lblObjAns.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky=E)
        self.cbbObjAns.grid(row=2, column=2, columnspan=4, padx=2, pady=2)
        self.lblSubjAns.grid(row=3, column=0, columnspan=2, padx=2, pady=2, sticky=E)
        self.lblSubjAnsInfo.grid(row=3, column=2, columnspan=2, padx=2, pady=2, sticky=W)
        self.txtSubjAns.grid(row=3, column=4, columnspan=10, padx=2, pady=2, stick=EW)
        self.btnSelectImage.grid(row=4, column=2, columnspan=3, padx=5, pady=5)
        self.btnPasteFromClipboard.grid(row=4, column=5, columnspan=3, padx=5, pady=5)
        self.btnSeeOriginal.grid(row=4, column=8, columnspan=3, padx=5, pady=5)
        self.btnInitializeImage.grid(row=4, column=11, columnspan=3, padx=5, pady=5)
        self.lblImage.grid(row=5, column=2, columnspan=12, padx=5, pady=5, sticky=NSEW)
        self.lblInfo.grid(row=6, column=2, columnspan=12, padx=2, sticky=E)
        self.lblHelp.grid(row=7, column=2, columnspan=12, padx=2, sticky=EW)

        self.container.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=10, pady=10, sticky=sticky)

    def select_image(self):        
        # 파일 선택
        self.selectedFileName = filedialog.askopenfilename(title='그림 파일 선택')

        # 선택한 파일이 있을 때만 작업
        if self.selectedFileName != '':
            self.img = Image.open(self.selectedFileName)
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용)

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
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            #self.lblImage.config(image=self.original)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text=self.selectedFileName)  # 안내용 라벨에 읽어들인 파일 경로 표시

    def paste_from_clipboard(self):
        self.img = ImageGrab.grabclipboard()

        if self.img != None:
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용): 이하 부분은 위와 동일하므로 함수로 만들 것을 고려할 것

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
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text='<클립보드>')  # 안내용 라벨

    def see_original(self):
        try:
            aWin = Toplevel()
            aWin.title(self.selectedFileName)
            aWin.grab_set()

            aLabel = Label(aWin)
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



class MPBSolutionRegistration(Frame):

    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, width=400, height=150, pos=N, sticky=N+W):
        Frame.__init__(self, master)

        self.container = Frame(master)

        # 제목
        self.lblTitle = Label(self.container, text='<풀이 관련 정보(선택)>', font=HUGE_FONT, fg='blue')

        # 명령 단추
        self.btnSelectImage = Button(self.container, text='그림 파일 선택', bg='yellow', wraplength=75, command=self.select_image)   # 그림 파일 선택
        self.btnSelectImage.config(width=10, height=2)

        self.btnPasteFromClipboard = Button(self.container, text='클립보드에서 가져오기', bg='yellow', wraplength=90, command=self.paste_from_clipboard)    # 클립보드에서 가져오기
        self.btnPasteFromClipboard.config(width=10, height=2)

        self.btnSeeOriginal = Button(self.container, text='그림 원본 보기', bg='yellow', wraplength=75, command=self.see_original)   # 원본 그림 보기
        self.btnSeeOriginal.config(width=10, height=2)

        self.btnInitializeImage = Button(self.container, text='초기화', bg='yellow', command=self.initialize_image) # 기존 그림 지우기
        self.btnInitializeImage.config(width=10, height=2)

        # 기본 배경 그림
        self.img = Image.open(DEFAULT_BACKGROUND)
        self.defaultImage = ImageTk.PhotoImage(self.img)
        self.isDefaultImageUsed = True

        # 라벨(그림)
        self.lblImage = Label(self.container, image=self.defaultImage, bg='grey')
        self.lblImage.config(width=width, height=height, relief=SUNKEN)

        # 라벨 크기
        self.labelWidth = width
        self.labelHeight = height
        self.labelRatio = height/width

        # 안내용 라벨
        self.lblInfo = Label(self.container)
        self.lblInfo.config(justify=RIGHT, wraplength=width)

        # 프레임에 넣기. 기본은 N(아래쪽에 단추 배치)
        if pos == S:
            self.lblTitle.grid(row=0, column=0, columnspan=8, sticky=W)
            self.btnSelectImage.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            self.btnPasteFromClipboard.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
            self.btnSeeOriginal.grid(row=1, column=4, columnspan=2, padx=5, pady=5)
            self.btnInitializeImage.grid(row=1, column=6, columnspan=2, padx=5, pady=5)
            self.lblImage.grid(row=2, column=0, rowspan=4, columnspan=8, padx=5, pady=5, sticky=NSEW)
            self.lblInfo.grid(row=6, column=0, columnspan=8, padx=2, sticky=E)
        elif pos == E:
            self.lblTitle.grid(row=0, column=0, columnspan=8, sticky=W)
            self.btnSelectImage.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            self.btnPasteFromClipboard.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
            self.btnSeeOriginal.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
            self.btnInitializeImage.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
            self.lblImage.grid(row=1, column=2, rowspan=4, columnspan=6, padx=5, pady=5, sticky=NSEW)
            self.lblInfo.grid(row=5, column=2, columnspan=6, padx=2, sticky=E)
        elif pos == W:
            self.lblTitle.grid(row=0, column=0, columnspan=8, sticky=W)
            self.lblImage.grid(row=1, column=0, rowspan=4, columnspan=6, padx=5, pady=5)
            self.btnSelectImage.grid(row=1, column=6, columnspan=2, padx=5, pady=5)
            self.btnPasteFromClipboard.grid(row=2, column=6, columnspan=2, padx=5, pady=5)
            self.btnSeeOriginal.grid(row=3, column=6, columnspan=2, padx=5, pady=5)
            self.btnInitializeImage.grid(row=4, column=6, columnspan=2, padx=5, pady=5)
            self.lblInfo.grid(row=5, column=0, columnspan=6, padx=2, sticky=E)
        else:   # N
            self.lblTitle.grid(row=0, column=0, columnspan=8, sticky=W)
            self.lblImage.grid(row=1, column=0, rowspan=4, columnspan=8, padx=5, pady=5, sticky=NSEW)
            self.btnSelectImage.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
            self.btnPasteFromClipboard.grid(row=5, column=2, columnspan=2, padx=5, pady=5)
            self.btnSeeOriginal.grid(row=5, column=4, columnspan=2, padx=5, pady=5)
            self.btnInitializeImage.grid(row=5, column=6, columnspan=2, padx=5, pady=5)
            self.lblInfo.grid(row=6, column=0, columnspan=8, padx=2, sticky=E)

        self.container.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=10, pady=10, sticky=sticky)

    def select_image(self):        
        # 파일 선택
        self.selectedFileName = filedialog.askopenfilename(title='그림 파일 선택')

        # 선택한 파일이 있을 때만 작업
        if self.selectedFileName != '':
            self.img = Image.open(self.selectedFileName)
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용)

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
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            #self.lblImage.config(image=self.original)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text=self.selectedFileName)  # 안내용 라벨에 읽어들인 파일 경로 표시

    def paste_from_clipboard(self):
        self.img = ImageGrab.grabclipboard()

        if self.img != None:
            self.original = ImageTk.PhotoImage(self.img)    # 크기 변형 전의 그림(저장용): 이하 부분은 위와 동일하므로 함수로 만들 것을 고려할 것

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
            self.resized = ImageTk.PhotoImage(self.img) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text='<클립보드>')  # 안내용 라벨

    def see_original(self):
        try:
            aWin = Toplevel()
            aWin.title(self.selectedFileName)
            aWin.grab_set()

            aLabel = Label(aWin)
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
    root=Tk()
    #root.geometry("640x480")

    # 이 명령으로 인해 프레임 안의 위젯의 크기가 프레임의 크기에 맞추어진다. 프레임의 크기가 클 경우에만 적용된다.
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    #root.resizable(width=False, height=False)
    root.resizable(width=False, height=True)
    
    #for i in range(1, 10):
    #    root.columnconfigure(i, weight=1)

    aTree = MPBCurriTreeView(root, row=0, column=0, rowspan=30, columnspan=30)
    #aTree.config(width=640, height=480)
    #aTree.grid(row=0, column=0)    # 안 됨. 클래스 안에서 써야함.
    #aTree.pack(side=LEFT)  # 안 됨. 클래스 안에서 써야함.

    aImageRegistration = MPBProblemImageRegistration(root, row=0, column=30, rowspan=20, columnspan=20, width=400, height=300)
    #aImageRegistration.grid(row=0, column=1)
    #aImageRegistration.pack(side=LEFT)

    aAns = MPBAnswerRegistration(root, row=30, column=0, width=400, height=50)
    aSol = MPBSolutionRegistration(root, row=30, column=30, width=400, height=175)

    frmOkCancel = Frame(root)   # 확인/취소 버튼을 위한 프레임
    btnOk = Button(frmOkCancel, text='확인', fg='white', bg='blue', font=HUGE_FONT, command=lambda: register_image_problem(aTree))
    #btnOk.tag_configure("WHITE")
    btnCancel = Button(frmOkCancel, text='취소', fg='white', bg='blue', font=HUGE_FONT, command=lambda: root.destroy())
    btnOk.grid(row=0, column=0, padx=5, pady=5)
    btnCancel.grid(row=0, column=1, padx=5, pady=5)
    frmOkCancel.grid(row=49, column=0, columnspan=50)

    root.mainloop()