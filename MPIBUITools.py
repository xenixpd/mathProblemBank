import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image, ImageGrab
import sqlite3



HUGE_FONT = ('맑은 고딕', 12, "bold")
LARGE_FONT = ('맑은 고딕', 11)
NORMAL_FONT = ('맑은 고딕', 10)

DEFAULT_BACKGROUND = '.\\coffee.jpeg'
UPWARD_ICON = '.\\icon\\upward32.gif'
DOWNWARD_ICON = '.\\icon\\downward32.gif'
CLIPBOARD_IMAGE = None

DB_NAME = '.\\mathProblemDB.db'



current_time_as_integer = lambda: int(round(time.time() * 1000))

        

class MPIBSourceTree(tk.Frame):
    def __init__(self, parent, title="<출처 선택>", treeHeight=20, showID=True, fg='blue', *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 트리에서 선택된 항목의 종류와 ID(기본값)
        self.selectedSourceLevel = ''
        self.selectedSourceID = 0
        self.selectedSourceName = ''
        self.selectedSourceBookID = 0

        self.showID = showID

        self.lblTitle = tk.Label(self, text=title, font=HUGE_FONT, fg=fg) # 제목

        treeContainer = tk.Frame(self) # 트리와 스크롤바를 담는 그릇
        treeContainer.grid_rowconfigure(0, weight=1)
        treeContainer.grid_columnconfigure(0, weight=1)

        self.trvSource = ttk.Treeview(treeContainer, height=treeHeight, selectmode='browse') # 트리 만들기
        self.trvSource.bind('<<TreeviewSelect>>', self.treeview_selected) # 클릭 시 실행할 함수

        self.trvSource.column('#0', width=425, anchor='center')
        self.trvSource.heading('#0', text='출처')
        self.trvSource.config(columns=('alive'))
        self.trvSource.column('alive', width=135, anchor='center')
        self.trvSource.heading('alive', text='현행 교육 과정 여부')

        trvYScroll = ttk.Scrollbar(treeContainer, orient=tk.VERTICAL) # 수직 스크롤바 만들기
        trvYScroll.configure(command=self.trvSource.yview)
        self.trvSource.configure(yscrollcommand=trvYScroll.set)

        # 데이타베이스에 연결해서 데이타 가져오기
        conn = sqlite3.connect(DB_NAME) # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성
        cur.execute("SELECT id, name FROM tblSourceLevelOne ORDER BY priority") # SQL 실행
        rows = cur.fetchall() # 데이타 fetch

        # 출처 관련 트리 만들기
        for row in rows:
            levelOneID = str(row[0])
            self.trvSource.insert('', 'end', '레벨1:' + levelOneID, text=row[1], tag='level1')

            # 레벨 1 아래에 레벨 2 추가
            sqlStr = "SELECT id, name FROM tblSourceLevelTwo WHERE parentID = ? ORDER BY priority"
            cur.execute(sqlStr, (str(row[0]),))
            secondRows = cur.fetchall()

            for secondRow in secondRows:
                levelTwoID = str(secondRow[0])
                self.trvSource.insert('레벨1:' + levelOneID, 'end', '레벨2:' + levelTwoID, text=secondRow[1], tag='level2')

                # 레벨 2 아래에 레벨 3(현재는 기본 레벨(Basic Level)) 추가
                sqlStr = "SELECT id, name, alive FROM tblSource WHERE parentID = ? ORDER BY priority"
                cur.execute(sqlStr, (str(secondRow[0]),))
                thirdRows = cur.fetchall()

                for thirdRow in thirdRows:
                    sourceID = str(thirdRow[0])
                    
                    if thirdRow[2]: # thirdRow[2]에는 dead(0) 또는 alive(1)의 값이 담겨 있다.
                        self.trvSource.insert('레벨2:' + levelTwoID, 'end', '출처:' + sourceID, text=thirdRow[1], tag='alive')
                        self.trvSource.set('출처:' + sourceID, 'alive', 'O')
                    else:
                        self.trvSource.insert('레벨2-' + levelTwoID, 'end', '출처:' + sourceID, text=thirdRow[1], tag='dead')
                        self.trvSource.set('출처:' + sourceID, 'alive', 'X')

        conn.close() # 데이터베이스에 대한 연결 닫기
        
        self.trvSource.tag_configure('alive', foreground='blue') # 트리 색칠
        self.trvSource.tag_configure('dead', background='#C1C1C1', foreground='red') # 교육 과정 밖의 유형은 배경 회색, 글 빨간색으로 처리

        self.trvSource.grid(row=0, column=0, sticky="nsew")
        trvYScroll.grid(row=0, column=1, sticky="ns")

        footerContainer = tk.Frame(self)
        footerContainer.grid_columnconfigure(0, weight=1)
        footerContainer.grid_columnconfigure(1, weight=1)
        footerContainer.grid_columnconfigure(2, weight=1)

        self.lblSelectedSourceLevel = tk.Label(footerContainer, text='출처') # 선택한 항목 구분
        self.lblSelectedSourceName = tk.Label(footerContainer, text='이름', fg='blue') # 선택한 항목 이름
        self.lblSelectedSourceID = tk.Label(footerContainer, text='ID') # 선택한 항목 ID

        self.lblSelectedSourceLevel.grid(row=0, column=0)
        self.lblSelectedSourceName.grid(row=0, column=1)

        if showID:
            self.lblSelectedSourceID.grid(row=0, column=2)

        # 그려 넣기
        self.lblTitle.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        treeContainer.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        footerContainer.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    
    # 트리의 어떤 항목이 선택되었을 때 실행되는 함수
    def treeview_selected(self, event):
        self.selectedSourceLevel = self.trvSource.focus().split(':')[0]
        self.selectedSourceID = self.trvSource.focus().split(':')[1]

        #if self.selectedSourceID == '':
        #    self.selectedSourceID = '-1'

        self.selectedSourceName = self.trvSource.item(self.trvSource.focus())['text']

        # 선택한 항목의 구분 알리기
        self.lblSelectedSourceLevel['text'] = self.selectedSourceLevel

        # 선택한 항목의 이름 알리기
        self.lblSelectedSourceName['text'] = self.selectedSourceName

        # 선택한 항목의 ID 알리기
        self.lblSelectedSourceID['text'] = self.selectedSourceID

    # 트리의 선택된 문제 유형 이름과 번호를 알려준다. 선택된 것이 없거나 문제 유형이 아니면(즉 책, 부, 장, 절이면) 0을 반환한다.
    def getSelectedSourceID(self):
        if self.selectedSourceLevel == '출처':
            return self.lblSelectedSourceID['text']
        else:
            return 0
            
    def getSelectedSourceName(self):
        if self.selectedSourceLevel == '출처':
            return self.lblSelectedSourceName
        else:
            return 0



class MPIBCurriTree(tk.Frame):
    def __init__(self, parent, title="<문제 유형 선택>", treeHeight=20, showID=True, fg='blue', *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        
        # 트리에서 선택된 항목의 종류와 ID(기본값)
        self.selectedCurriLevel = ''
        self.selectedCurriID = 0
        self.selectedCurriName = ''
        self.selectedProblemTypeID = 0

        self.showID = showID

        self.lblTitle = tk.Label(self, text=title, font=HUGE_FONT, fg=fg) # 제목

        treeContainer = tk.Frame(self) # 트리와 스크롤바를 담는 그릇
        treeContainer.grid_rowconfigure(0, weight=1) # 상하로 크기가 변할 때 같이 크기가 변할 구역 설정
        treeContainer.grid_columnconfigure(0, weight=1) # 좌우로 크기가 변할 때 같이 크기가 변할 구역 설정

        self.trvCurri = ttk.Treeview(treeContainer, height=treeHeight, selectmode='browse') # 트리 만들기
        self.trvCurri.bind('<<TreeviewSelect>>', self.treeview_selected) # 클릭 시 실행할 함수

        self.trvCurri.column('#0', width=425, anchor='center') # Treeview 내의 제목 설정
        self.trvCurri.heading('#0', text='구분')

        self.trvCurri.config(columns=('alive')) # 추가할 열 설정
        self.trvCurri.column('alive', width=135, anchor='center')
        self.trvCurri.heading('alive', text='교육 과정 내인지 여부')

        treeYScroll = ttk.Scrollbar(treeContainer, orient=tk.VERTICAL) # 수직 스크롤바 만들기
        treeYScroll.configure(command=self.trvCurri.yview)
        self.trvCurri.configure(yscrollcommand=treeYScroll.set)

        # 데이타베이스에 연결해서 데이타 가져오기
        conn = sqlite3.connect(DB_NAME) # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성
        cur.execute("SELECT id, name FROM tblBook ORDER BY priority") # SQL 실행(책)
        rows = cur.fetchall() # 데이타 fetch

        # 교육 과정 관련 트리 만들기
        for row in rows:
            bookID = str(row[0])
            self.trvCurri.insert('', 'end', '책-' + bookID, text=row[1], tag='book')

            # 책 아래에 부 추가
            sqlStr = "SELECT id, name FROM tblPart WHERE bookID = ? ORDER BY priority"
            cur.execute(sqlStr, (str(row[0]),))
            secondRows = cur.fetchall()

            for secondRow in secondRows:
                partID = str(secondRow[0])
                self.trvCurri.insert('책-' + bookID, 'end', '부-' + partID, text=secondRow[1], tag='part')

                # 부 아래에 장 추가
                sqlStr = "SELECT id, name FROM tblChapter WHERE partID = ? ORDER BY priority"
                cur.execute(sqlStr, (str(secondRow[0]),))
                thirdRows = cur.fetchall()

                for thirdRow in thirdRows:
                    chapterID = str(thirdRow[0])
                    self.trvCurri.insert('부-' + partID, 'end', '장-' + chapterID, text=thirdRow[1], tag='chapter')

                    # 장 아래에 절 추가
                    sqlStr = "SELECT id, name FROM tblSection WHERE chapterID = ? ORDER BY priority"
                    cur.execute(sqlStr, (str(thirdRow[0]),))
                    fourthRows = cur.fetchall()

                    for fourthRow in fourthRows:
                        sectionID = str(fourthRow[0])
                        self.trvCurri.insert('장-' + chapterID, 'end', '절-' + sectionID, text=fourthRow[1], tag='section')

                        # 절 아래에 문제 유형 추가
                        sqlStr = "SELECT id, name, alive FROM tblProblemType WHERE sectionID = ? ORDER BY priority"
                        cur.execute(sqlStr, (str(fourthRow[0]),))
                        fifthRows = cur.fetchall()

                        for fifthRow in fifthRows:
                            problemTypeID = str(fifthRow[0])
                            
                            if fifthRow[2]: # fifthRow[2]에는 dead(0) 또는 alive(1)의 값이 담겨 있다.
                                self.trvCurri.insert('절-' + sectionID, 'end', '문제 유형-' + problemTypeID, text=fifthRow[1], tag='alive')
                                self.trvCurri.set('문제 유형-' + problemTypeID, 'alive', 'O')
                            else:
                                self.trvCurri.insert('절-' + sectionID, 'end', '문제 유형-' + problemTypeID, text=fifthRow[1], tag='dead')
                                self.trvCurri.set('문제 유형-' + problemTypeID, 'alive', 'X')

        conn.close() # 데이터베이스에 대한 연결 닫기
        
        self.trvCurri.tag_configure('alive', foreground='blue') # 트리 색칠
        self.trvCurri.tag_configure('dead', background='#C1C1C1', foreground='red') # 교육 과정 밖의 유형은 배경 회색, 글 빨간색으로 처리

        self.trvCurri.grid(row=0, column=0, sticky="nsew") # 그릇에 담기
        treeYScroll.grid(row=0, column=1, sticky="ns")

        footerContainer = tk.Frame(self)
        footerContainer.grid_columnconfigure(1, weight=1) # 선택한 항목 이름 부분만 틀의 크기 변경에 따라 같이 변하도록 설정

        self.lblSelectedCurriLevel = tk.Label(footerContainer, text='구분') # 선택한 항목 구분
        self.lblSelectedCurriName = tk.Label(footerContainer, text='이름', fg='blue') # 선택한 항목 이름
        self.lblSelectedCurriID = tk.Label(footerContainer, text='ID') # 선택한 항목 ID

        # 그릇에 담기
        self.lblSelectedCurriLevel.grid(row=0, column=0)
        self.lblSelectedCurriName.grid(row=0, column=1)

        if showID:
            self.lblSelectedCurriID.grid(row=0, column=2)

        # 그려 넣기
        self.lblTitle.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        treeContainer.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        footerContainer.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    
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
            
    def getSelectedProblemTypeName(self):
        if self.selectedCurriLevel == '문제 유형':
            return self.selectedCurriName
        else:
            return 0



class MPIBImageSelection(tk.Frame):
# 그림을 보여주는 영역과 함께 그림 파일 선택, 클립보드에서 가져오기, 원본 그림 보기, 초기화의 네 가지 기능을 가진다.
# title: 제목
# imageWidth, imageHeight: 그림 영역의 가로, 세로를 결정한다.
# imagePosition: 그림을 보여줄 영역의 상대적 위치를 정해줄 수 있다.
# imageRelief: 그림 영역의 배경 효과 지정
    def __init__(self, parent, title='<문제 그림 선택>', imageWidth=400, imageHeight=300, imagePosition="n",
                 imageRelief = tk.SUNKEN, temporaryImageFileNameOnly="a", *args, **kwargs):
        # 인수로 주어진 width와 height는 전체 크기가 아니라 그림 영역의 크기이다.
        # 인수 pos는 명령 단추가 놓일 곳을 가리킨다. (N, S, E, W)
        tk.Frame.__init__(self, parent)

        # 제목
        lblTitle = tk.Label(self, text=title, font=HUGE_FONT)
        lblTitle.config(fg='blue')

        # 기본 배경 그림
        self.image = Image.open(DEFAULT_BACKGROUND)
        self.saved = None
        self.defaultImage = ImageTk.PhotoImage(self.image)
        self.isDefaultImageUsed = True
        self.selectedFileName = ''
        self.outputImageName = temporaryImageFileNameOnly + ".png"

        # 라벨(그림 영역)
        self.lblImage = tk.Label(self, image=self.defaultImage, bg='grey')
        self.lblImage.config(width=imageWidth, height=imageHeight, relief=imageRelief)

        # 크기 변경 추척
        self.lblImage.bind('<Configure>', self.configure)
        
        # 명령 단추

        # 명령 단추들을 담을 그릇
        frmButtonContainer = tk.Frame(self)

        # 그림 파일 선택
        btnSelectImage = tk.Button(frmButtonContainer, text='그림 파일 선택', bg='yellow', wraplength=75,
                                   command=lambda : self.select_image(imageWidth, imageHeight))
        btnSelectImage.config(width=10, height=2)

        # 클립보드에서 가져오기
        btnPasteFromClipboard = tk.Button(frmButtonContainer, text='클립보드에서 가져오기', bg='yellow', wraplength=90,
                                          command=lambda : self.paste_from_clipboard(imageWidth, imageHeight))
        btnPasteFromClipboard.config(width=10, height=2)

        # 원본 그림 보기
        btnSeeOriginal = tk.Button(frmButtonContainer, text='그림 원본 보기', bg='yellow', wraplength=75,
                                   command=self.see_original)
        btnSeeOriginal.config(width=10, height=2)

        # 기존 그림 지우기
        btnInitializeImage = tk.Button(frmButtonContainer, text='초기화', bg='yellow', wraplength=75,
                                       command=self.initialize_image)
        btnInitializeImage.config(width=10, height=2)

        # 안내용 라벨
        self.lblInfo = tk.Label(self)
        self.lblInfo.config(justify=tk.RIGHT, wraplength=imageWidth)

        # 프레임에 넣기. imagePosition은 의 이미지의 위치. 기본은 N(아래쪽에 단추 배치)
        if imagePosition == tk.S or imagePosition == "s": # 그림이 남쪽(아래), 단추들은 북쪽(위쪽)
            # 먼저 명령 단추들을 그릇에 담는다.
            btnSelectImage.grid(row=0, column=0) # sticky 옵션이 없으므로 단추의 크기가 변하지 않는다.
            btnPasteFromClipboard.grid(row=0, column=1)
            btnSeeOriginal.grid(row=0, column=2)
            btnInitializeImage.grid(row=0, column=3)

            # 기본 틀의 크기가 변하더라도 위아래 폭은 변하지 않고 단추 사이의 간격만 변하도록 조치
            frmButtonContainer.grid_columnconfigure(0, weight=1)
            frmButtonContainer.grid_columnconfigure(1, weight=1)
            frmButtonContainer.grid_columnconfigure(2, weight=1)
            frmButtonContainer.grid_columnconfigure(3, weight=1)

            # 배치하기
            lblTitle.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky="w")
            frmButtonContainer.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
            self.lblImage.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
            self.lblInfo.grid(row=3, column=0, columnspan=8, padx=5, pady=5, sticky="e")

            # 명령 단추들의 위치에 맞게 기본 틀의 크기 조정도 변경
            self.grid_rowconfigure(2, weight=1)
            self.grid_columnconfigure(0, weight=1)
        elif imagePosition == tk.E or imagePosition == "e": # 그림 오른쪽, 단추 왼쪽
            # 단추 담기
            btnSelectImage.grid(row=0, column=0)
            btnPasteFromClipboard.grid(row=1, column=0)
            btnSeeOriginal.grid(row=2, column=0)
            btnInitializeImage.grid(row=3, column=0)

            frmButtonContainer.grid_rowconfigure(0, weight=1) # 모든 행이 틀이 커질 때 같이 커지도록 조치
            frmButtonContainer.grid_rowconfigure(1, weight=1) # 단추의 크기는 변하지 않게 하였으므로 단추 사이의
            frmButtonContainer.grid_rowconfigure(2, weight=1) # 간격이 넓어질 것으로 기대
            frmButtonContainer.grid_rowconfigure(3, weight=1) # 열 간격은 변하지 않는다.

            # 배치
            lblTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
            frmButtonContainer.grid(row=1, column=0, padx=5, pady=5, sticky="ns")
            self.lblImage.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
            self.lblInfo.grid(row=2, column=1, padx=5, sticky="e")

            # 명령 단추들의 위치에 맞게 기본 틀의 크기 조정도 변경
            self.grid_rowconfigure(1, weight=1)
            self.grid_columnconfigure(1, weight=1)
        elif imagePosition == tk.W or imagePosition == "w": # 그림 왼쪽, 단추 오른쪽
            # 단추 담기
            btnSelectImage.grid(row=0, column=0)
            btnPasteFromClipboard.grid(row=1, column=0)
            btnSeeOriginal.grid(row=2, column=0)
            btnInitializeImage.grid(row=3, column=0)

            frmButtonContainer.grid_rowconfigure(0, weight=1)
            frmButtonContainer.grid_rowconfigure(1, weight=1)
            frmButtonContainer.grid_rowconfigure(2, weight=1)
            frmButtonContainer.grid_rowconfigure(3, weight=1)

            # 배치
            lblTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
            self.lblImage.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            frmButtonContainer.grid(row=1, column=1, padx=5, pady=5, sticky="ns")
            self.lblInfo.grid(row=2, column=0, padx=5, sticky="e")

            # 명령 단추들의 위치에 맞게 기본 틀의 크기 조정도 변경
            self.grid_rowconfigure(1, weight=1)
            self.grid_columnconfigure(0, weight=1)
        else: # 그림 북쪽(위), 단추 남쪽(아래). 기본값
            # 단추 담기
            btnSelectImage.grid(row=0, column=0)
            btnPasteFromClipboard.grid(row=0, column=1)
            btnSeeOriginal.grid(row=0, column=2)
            btnInitializeImage.grid(row=0, column=3)

            # 기본 틀의 크기가 변하더라도 위아래 폭은 변하지 않고 단추 사이의 간격만 변하도록 조치
            frmButtonContainer.grid_columnconfigure(0, weight=1)
            frmButtonContainer.grid_columnconfigure(1, weight=1)
            frmButtonContainer.grid_columnconfigure(2, weight=1)
            frmButtonContainer.grid_columnconfigure(3, weight=1)

            # 배치
            lblTitle.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky="w")
            self.lblImage.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            self.lblInfo.grid(row=2, column=0, padx=5, sticky="e")
            frmButtonContainer.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

            # 명령 단추들의 위치에 맞게 기본 틀의 크기 조정도 변경
            self.grid_rowconfigure(1, weight=1)
            self.grid_columnconfigure(0, weight=1)

    def configure(self, event):
    # 틀 크기 변경 시 그림 크기도 변경
        width, height = event.width, event.height
        self.image = self.saved

        if not self.isDefaultImageUsed:
            imageWidth = self.image.size[0]
            imageHeight = self.image.size[1]
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

            self.image = self.image.resize((newWidth, newHeight), Image.ANTIALIAS)
            self.resized = ImageTk.PhotoImage(self.image) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)

    def select_image(self, width, height):        
        # 파일 선택
        self.selectedFileName = filedialog.askopenfilename(title='그림 파일 선택')

        # 선택한 파일이 있을 때만 작업
        if self.selectedFileName != '':
            self.image = self.saved = Image.open(self.selectedFileName)
            self.image.save(self.outputImageName, "png")
            self.original = ImageTk.PhotoImage(self.image) # 크기 변형 전의 그림(저장용)

            imageWidth = self.image.size[0]
            imageHeight = self.image.size[1]
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

            self.image = self.image.resize((newWidth, newHeight), Image.ANTIALIAS)
            self.resized = ImageTk.PhotoImage(self.image) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text=self.selectedFileName) # 안내용 라벨에 읽어들인 파일 경로 표시

    def paste_from_clipboard(self, width, height):
        self.image = self.saved = ImageGrab.grabclipboard()

        if self.image != None:
            self.image.save(self.outputImageName, "png")
            self.original = ImageTk.PhotoImage(self.image) # 크기 변형 전의 그림(저장용): 이하 부분은 위와 동일하므로 함수로 만들 것을 고려할 것

            imageWidth = self.image.size[0]
            imageHeight = self.image.size[1]
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

            self.imageResized = self.image.resize((newWidth, newHeight), Image.ANTIALIAS)
            self.resized = ImageTk.PhotoImage(self.imageResized) # 크기 변형 후의 그림(보여주기 용)
            self.lblImage.config(image=self.resized)
            self.isDefaultImageUsed = False
            self.lblInfo.config(text='<클립보드>')  # 안내용 라벨
            self.selectedFileName = '<클립보드>'

    def see_original(self):
        if self.selectedFileName != '':
            aWin = tk.Toplevel()
            aWin.title(self.selectedFileName)
            aWin.grab_set()

            aLabel = tk.Label(aWin)
            aLabel.config(image=self.original)
            aLabel.pack()

    def initialize_image(self):
        self.lblImage.config(image=self.defaultImage)
        self.isDefaultImageUsed = True
        self.lblInfo.config(text='')    # 안내용 라벨
        self.original = None
        self.selectedFileName = ''



class MPIBColumnsUsedComboBox(tk.Frame):
# 편집 시 사용된 단의 수를 선택할 수 있게 해주는 간단한 콤보 상자
# boxPos: 콤보 상자의 위치(S 또는 E). 기본값은 tk.E("e")
    def __init__(self, parent, boxPos="e", boxWidth=5, textAnchor="e", *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0, weight=1)
        
        lblColumnsUsed = tk.Label(self, text='편집 시 사용할 단의 개수: ')
        self.cbbColumnsUsed = ttk.Combobox(self)
        self.cbbColumnsUsed.config(width=boxWidth)

        conn = sqlite3.connect(DB_NAME) # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성

        cur.execute("SELECT columns FROM tblColumnsUsed ORDER BY columns") # SQL 실행
        rows = cur.fetchall() # 데이타 fetch
        self.cbbColumnsUsed['value'] =([row for row in rows]) # 가져온 데이타를 콤보 상자에 담기
        conn.close() # Connection 닫기

        lblColumnsUsed.grid(row=0, column=0, sticky=textAnchor)
        
        if boxPos == "s":
            self.cbbColumnsUsed.grid(row=1, column=0, sticky="w")
        else: # "e"
            self.cbbColumnsUsed.grid(row=0, column=1, sticky="w")

    def check(self):
        columnsUsed = self.cbbColumnsUsed.get()

        if columnsUsed == '':
            return False

        conn = sqlite3.connect(DB_NAME)  # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성
        cur.execute("SELECT columns FROM tblColumnsUsed WHERE columns = ?", (columnsUsed,))  # SQL 실행
        rows = cur.fetchone()   # 데이타 fetch

        if rows == None:
            isUsed = False
        else:
            isUsed = True

        conn.close()

        return isUsed



class MPIBDifficultyComboBox(tk.Frame):
# 예상 난이도를 선택할 수 있게 해주는 간단한 콤보 상자
# boxPos: 콤보 상자의 위치(S 또는 E). 기본값은 tk.E("e")
    def __init__(self, parent, boxPos="e", boxWidth=5, textAnchor="e", *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0, weight=1)
        
        lblDifficulty = tk.Label(self, text='예상 난이도: ')
        self.cbbDifficulty = ttk.Combobox(self)
        self.cbbDifficulty.config(width=boxWidth)

        conn = sqlite3.connect(DB_NAME) # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성

        cur.execute("SELECT difficulty FROM tblDifficulty ORDER BY difficulty")  # SQL 실행
        rows = cur.fetchall() # 데이타 fetch
        self.cbbDifficulty['value'] =([row for row in rows]) # 가져온 데이타를 콤보 상자에 담기
        conn.close() # Connection 닫기

        lblDifficulty.grid(row=0, column=0, sticky=textAnchor)
        
        if boxPos == "s":
            self.cbbDifficulty.grid(row=1, column=0, sticky="w")
        else: # "e"
            self.cbbDifficulty.grid(row=0, column=1, sticky="w")

    def check(self):
        diff = self.cbbDifficulty.get()

        if diff == '':
            return False

        conn = sqlite3.connect(DB_NAME)  # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성
        cur.execute("SELECT difficulty FROM tblDifficulty WHERE difficulty = ?", (diff,))  # SQL 실행
        rows = cur.fetchone()   # 데이타 fetch

        if rows == None:
            isOk = False
        else:
            isOk = True

        conn.close()

        return isOk



if __name__ == '__main__':
    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    #aSource = MPIBSourceTree(root, showID=True)
    #aSource.grid(sticky="nsew")

    #aTree = MPIBCurriTree(root, showID=False)
    #aTree.grid(sticky="nsew")

    #aSelection = MPIBImageSelection(root, imagePosition="w")
    #aSelection.grid(sticky="nsew")

    aBox = MPIBDifficultyComboBox(root, textAnchor="ew")
    aBox.grid(sticky="nsew")

    root.mainloop()