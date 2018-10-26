import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image, ImageGrab
import sqlite3
import time



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
    def getSourceID(self):
        if self.selectedSourceLevel == '출처':
            return int(self.lblSelectedSourceID['text'])
        else:
            return 0
            
    def getSourceName(self):
        if self.selectedSourceLevel == '출처':
            return self.lblSelectedSourceName
        else:
            return 0



class MPIBCurriTree(tk.Frame):
    def __init__(self, parent, title="<문제 유형 선택>", treeHeight=20, showID=True, fg='blue', *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
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
    def getProblemTypeID(self):
        if self.selectedCurriLevel == '문제 유형':
            return int(self.lblSelectedCurriID['text'])
        else:
            return 0
            
    def getProblemTypeName(self):
        if self.selectedCurriLevel == '문제 유형':
            return self.selectedCurriName
        else:
            return 0



class MPIBImageSelection(tk.Frame):
# 그림을 보여주는 영역과 함께 그림 파일 선택, 클립보드에서 가져오기, 원본 그림 보기, 초기화의 네 가지 기능을 가진다.
# title: 제목
# imageWidth, imageHeight: 그림 영역의 가로, 세로를 결정한다.
# imagePos: 그림을 보여줄 영역의 상대적 위치를 정해줄 수 있다.
# imageRelief: 그림 영역의 배경 효과 지정
    def __init__(self, parent, useTitle=True, title='<문제 그림 선택>', imageWidth=400, imageHeight=300, imagePos="n",
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

        # 프레임에 넣기. imagePos는 의 이미지의 위치. 기본은 N(아래쪽에 단추 배치)
        if imagePos == tk.S or imagePos == "s": # 그림이 남쪽(아래), 단추들은 북쪽(위쪽)
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
            if useTitle:
                lblTitle.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky="w")

            frmButtonContainer.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
            self.lblImage.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
            self.lblInfo.grid(row=3, column=0, columnspan=8, padx=5, pady=5, sticky="e")

            # 명령 단추들의 위치에 맞게 기본 틀의 크기 조정도 변경
            self.grid_rowconfigure(2, weight=1)
            self.grid_columnconfigure(0, weight=1)
        elif imagePos == tk.E or imagePos == "e": # 그림 오른쪽, 단추 왼쪽
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
            if useTitle:
                lblTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

            frmButtonContainer.grid(row=1, column=0, padx=5, pady=5, sticky="ns")
            self.lblImage.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
            self.lblInfo.grid(row=2, column=1, padx=5, sticky="e")

            # 명령 단추들의 위치에 맞게 기본 틀의 크기 조정도 변경
            self.grid_rowconfigure(1, weight=1)
            self.grid_columnconfigure(1, weight=1)
        elif imagePos == tk.W or imagePos == "w": # 그림 왼쪽, 단추 오른쪽
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
            if useTitle:
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
            if useTitle:
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
        
        if boxPos == tk.S or boxPos == "s":
            self.cbbColumnsUsed.grid(row=1, column=0, sticky=textAnchor)
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

    def get(self):
        if self.check():
            return int(self.cbbColumnsUsed.get())
        else:
            return 0



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
        
        if boxPos == tk.S or boxPos == "s":
            self.cbbDifficulty.grid(row=1, column=0, sticky=textAnchor)
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

    def get(self):
        if self.check():
            return int(self.cbbDifficulty.get())
        else:
            return 0



class MPIBAnsTypeRadioButton(tk.Frame):
# 답 형식(객관식/주관식)을 선택할 수 있게 해주는 간단한 라디오 버튼
# radioPos: 라디오 버튼의 위치(S 또는 E). 기본값은 tk.E("e")
    def __init__(self, parent, radioPos="e", textAnchor="e", *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0, weight=1)

        # 답 형식
        lblAnsType = tk.Label(self, text='답 형식: ')

        # 답 형식 선택을 위한 라디오 버튼
        self.ansTypeChoice = tk.IntVar()

        self.radAnsTypeObj = tk.Radiobutton(self, text='객관식', variable=self.ansTypeChoice, value=1)
        self.radAnsTypeObj.select() # 기본값은 객관식
        self.radAnsTypeSubj = tk.Radiobutton(self, text='주관식', variable=self.ansTypeChoice, value=2)

        # 담기
        lblAnsType.grid(row=0, column=0, sticky=textAnchor)

        if radioPos == tk.S or radioPos == "s":
            self.radAnsTypeObj.grid(row=1, column=0, sticky=textAnchor)
            self.radAnsTypeSubj.grid(row=2, column=0, sticky=textAnchor)
        else:
            self.radAnsTypeObj.grid(row=0, column=1, sticky="w")
            self.radAnsTypeSubj.grid(row=0, column=2, sticky="w")

    def check(self):
        ansType = int(self.ansTypeChoice.get())

        if ansType == 1 or ansType == 2:
            return True
        else:
            return False



class MPIBObjAnsComboBox(tk.Frame):
# 객관식 답을 선택할 수 있게 해주는 간단한 콤보 상자
# boxPos: 콤보 상자의 위치(S 또는 E). 기본값은 tk.E("e")
    def __init__(self, parent, boxPos="e", boxWidth=5, textAnchor="e", *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0, weight=1)

        lblObjAns = tk.Label(self, text='객관식 답: ')
        self.cbbObjAns = ttk.Combobox(self)
        self.cbbObjAns.config(width=boxWidth)

        conn = sqlite3.connect(DB_NAME) # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성
        cur.execute("SELECT ansNo FROM tblObjAns ORDER BY ansNo") # SQL 실행
        rows = cur.fetchall() # 데이타 fetch
        self.cbbObjAns['value'] =([row for row in rows]) # 가져온 데이타를 콤보 상자에 담기
        conn.close()    # Connection 닫기

        lblObjAns.grid(row=0, column=0, sticky=textAnchor)
        
        if boxPos == tk.S or boxPos == "s":
            self.cbbObjAns.grid(row=1, column=0, sticky=textAnchor)
        else: # "e"
            self.cbbObjAns.grid(row=0, column=1, sticky="w")

    def check(self):
        objAns = self.cbbObjAns.get()

        if objAns == '':
            return False

        conn = sqlite3.connect("mathProblemDB.db") # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성
        cur.execute("SELECT ansNo FROM tblObjAns WHERE ansNo = ?", (objAns,)) # SQL 실행
        rows = cur.fetchone() # 데이타 fetch

        if rows == None:
            isOk = False
        else:
            isOk = True

        conn.close()

        return isOk



class MPIBSubjAnsTextBox(tk.Frame):
# 주관식 답을 직접 입력할 수 있게 해주는 간단한 텍스트 상자
# boxPos: 콤보 상자의 위치(S 또는 E). 기본값은 tk.E("e")
    def __init__(self, parent, boxPos="e", textWidth=10, textAnchor="e", *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0, weight=1)

        lblSubjAns = tk.Label(self, text='주관식 답: ')

        container = tk.Frame(self) # '(직접 입력)' 라벨과 실제 답을 입력할 텍스트 상자를 하나로 묶기 위한 그릇

        lblSubjAnsInfo = tk.Label(container, text='(직접 입력)')

        self.enteredAns = tk.StringVar()
        self.txtSubjAns = tk.Entry(container, textvariable=self.enteredAns)
        self.txtSubjAns.config(width=textWidth)

        lblSubjAns.grid(row=0, column=0, sticky=textAnchor)

        if boxPos == tk.S or boxPos == "s":
            lblSubjAnsInfo.grid(row=0, column=0, sticky=textAnchor)
            self.txtSubjAns.grid(row=1, column=0, sticky="ew")
            
            container.grid(row=1, column=0, sticky="ew")
            container.grid_columnconfigure(0, weight=1)
        else:
            lblSubjAnsInfo.grid(row=0, column=0, sticky=textAnchor)
            self.txtSubjAns.grid(row=0, column=1, sticky="ew")
            
            container.grid(row=0, column=1, sticky="ew")
            container.grid_columnconfigure(1, weight=1)

    def get(self):
        return self.txtSubjAns.get()



class MPIBProblemImageSelection(tk.Frame):
    def __init__(self, parent, imageWidth=400, imageHeight=300, imagePos=tk.N, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 제목
        lblTitle = tk.Label(self, text='<문제 그림 선택>', font=HUGE_FONT, fg='blue')
        
        # 그림 선택
        self.problemSelection = MPIBImageSelection(self, useTitle=False, imageWidth=imageWidth, imageHeight=imageHeight,
                                                   imagePos=imagePos, temporaryImageFileNameOnly="problem")

        footer = tk.Frame(self) # 단 수와 예상 난이도를 담을 그릇
        footer.grid_columnconfigure(0, weight=1)
        #footer.grid_columnconfigure(1, weight=1)

        self.columns = MPIBColumnsUsedComboBox(footer, boxWidth=4) # 단 수
        self.columns.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.difficulty = MPIBDifficultyComboBox(footer, boxWidth=4) # 예상 난이도
        self.difficulty.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        lblTitle.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.problemSelection.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        footer.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    def isDefaultImageUsed(self):
        return self.problemSelection.isDefaultImageUsed

    def checkColumns(self):
        return self.columns.check()

    def getColumns(self):
        return self.columns.get()

    def checkDifficulty(self):
        return self.difficulty.check()

    def getDifficulty(self):
        return self.difficulty.get()



class MPIBAnswerImageSelection(tk.Frame):
    def __init__(self, parent, imageWidth=300, imageHeight=150, imagePos=tk.N, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        lblTitle = tk.Label(self, text='<답 관련 정보>', font=HUGE_FONT, fg='blue') # 제목
        lblTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nw")
        
        lblAnsType = tk.Label(self, text='답 형식: ') # 답 형식
        lblAnsType.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        frmAnsType = tk.Frame(self) # 답 형식 선택을 위한 라디오 버튼을 담는 그릇
        frmAnsType.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        self.ansTypeChoice = tk.IntVar() # 답 형식 선택을 위한 라디오 버튼
        self.radAnsTypeObj = tk.Radiobutton(frmAnsType, text='객관식', variable=self.ansTypeChoice, value=1)
        self.radAnsTypeObj.grid(row=0, column=0, sticky="w")
        self.radAnsTypeObj.select()
        self.radAnsTypeSubj = tk.Radiobutton(frmAnsType, text='주관식', variable=self.ansTypeChoice, value=2)
        self.radAnsTypeSubj.grid(row=0, column=1, sticky="w")

        lblObjAns = tk.Label(self, text='객관식 답: ')
        lblObjAns.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.cbbObjAns = ttk.Combobox(self, width=5)
        self.cbbObjAns.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT ansNo FROM tblObjAns ORDER BY ansNo")
        rows = cur.fetchall()
        self.cbbObjAns['value'] =([row for row in rows])
        conn.close()

        lblSubjAns = tk.Label(self, text='주관식 답: ')
        lblSubjAns.grid(row=3, column=0, padx=5, pady=5, sticky="ne")

        frmSubjAns = tk.Frame(self)
        frmSubjAns.grid_columnconfigure(1, weight=1)
        frmSubjAns.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        lblSubjAnsInfo = tk.Label(frmSubjAns, text='(직접 입력)')
        lblSubjAnsInfo.grid(row=0, column=0)

        self.enteredAns = tk.StringVar()
        self.txtSubjAns = tk.Entry(frmSubjAns, textvariable=self.enteredAns)
        self.txtSubjAns.grid(row=0, column=1, sticky="ew")

        self.answerSelection = MPIBImageSelection(self, useTitle=False, imageWidth=imageWidth, imageHeight=imageHeight,
                                                  imagePos=imagePos, temporaryImageFileNameOnly="answer")
        self.answerSelection.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

    def ansType(self):
        return int(self.ansTypeChoice.get())



class MPIBProblemImageRegistration(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.curri = MPIBCurriTree(self, showID=False)
        self.curri.grid(row=0, column=0, sticky="nsew")

        self.problem = MPIBProblemImageSelection(self)
        self.problem.grid(row=0, column=1, sticky="nsew")

        self.ans = MPIBAnswerImageSelection(self, imageWidth=400, imageHeight=100)
        self.ans.grid_columnconfigure(1, weight=0)
        self.ans.grid(row=1, column=0, sticky="nsew")

        self.sol = MPIBImageSelection(self, title='<풀이 정보(선택)>')
        self.sol.grid(row=1, column=1, sticky="nsew")

        frmOkCancel= tk.Frame(self)
        frmOkCancel.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        btnOk = tk.Button(frmOkCancel, text='확인', fg='white', bg='blue', font=HUGE_FONT), command=self.register_image_problem)
        btnOk.grid(row=0, column=0, padx=5)

        btnCancel = tk.Button(frmOkCancel, text='취소', fg='white', bg='blue', font=HUGE_FONT, command=parent.destroy)
        btnCancel.grid(row=0, column=1, padx=5)

    def register_image_problem(self):
        # 문제 유형 ID
        problemTypeID = self.curri.getProblemTypeID())

        if problemTypeID == 0: # 문제 유형 ID. 문제 유형이 아니거나(즉, 책, 부, 장, 절) 선택한 것이 없으면 0을 반환한다.
            messagebox.showerror("문제 유형 오류", "문제 유형을 선택하세요.")
            return

        # 문제 그림
        if self.problem.isDefaultImageUsed:
            messagebox.showerror("문제 그림 없음", "문제 그림을 선택하세요.")
            return

        # 문제 단 수
        columnsUsed = self.problem.getColumns()

        if columnsUsed == 0:
            messagebox.showerror("단의 개수 오류", "문제의 편집 시 사용할 단의 개수를 선택하세요.")
            return
        
        # 예상 난이도
        diff = self.problem.getDifficulty()

        if diff == 0:
            messagebox.showerror("난이도 오류", "난이도를 선택하세요.")
            return

        # 답 형식
        ansType = self.ans.ansType()

        #if not (ansType == 1 or ansType == 2):
        #    messagebox.showerror("답 형식 오류", "답 형식을 선택하세요.")
        #    return

        ansType2 = 0 # 1: 객관식 답, 2: 주관식 답 + 직접 입력, 3: 주관식 답 + 그림
        objAns = ''
        subjAns = ''

        # 답
        if ansType == 1: # 객관식 답일 경우
            if not ans.check_objective_answer():
                messagebox.showerror("객관식 답 오류", "객관식 답을 선택하세요.")
                return
            else:
                objAns = int(ans.cbbObjAns.get())
                ansType2 = 1
        elif ansType == 2: # 주관식 답일 경우
            subjAnsText = ans.txtSubjAns.get()

            if subjAnsText == '' and ans.isDefaultImageUsed: # 직접 입력한 값도 없고 그림도 없으면 오류
                messagebox.showerror("주관식 답 오류", "주관식 답을 직접 입력하거나 그림을 선택하세요.")
                return
            elif subjAnsText != '':
                subjAns = subjAnsText
                ansType2 = 2
            else:
                subjAns = ''
                ansType2 = 3

        # 풀이 단 수
        solColumnsUsed = 1

        if not sol.check_columns_used():
            messagebox.showerror("풀이의 단의 개수 오류", "풀이의 편집 시 사용할 단의 개수를 선택하세요.")
            return
        else:
            solColumnsUsed = int(sol.cbbColumnsUsed.get())

        # 미리 저장해 둔 임시 그림 파일들을 저장용 폴더로 복사
        filename = str(current_time_as_integer())

        shutil.copy("./problem.png", "./MPIB/" + filename + ".png")

        if ansType2 == 3:
            shutil.copy("./answer.png", "./MPIB/" + filename + "_ans.png")

        if not sol.isDefaultImageUsed:
            shutil.copy("./solution.png", "./MPIB/" + filename + "_sol.png")
        
        # 데이타베이스에 추가
        conn = sqlite3.connect("mathProblemDB.db") # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성

        if sol.isDefaultImageUsed: # 풀이 파일 없음
            if ansType2 == 1: # 객관식
                sqlStr = """INSERT INTO tblMPIB
                            (filename, problemTypeID, columns, difficulty, ansType, objAns, subjAnsImageExists, solImageExists)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                cur.execute(sqlStr, (filename, problemTypeID, columnsUsed, diff, ansType, objAns, False, False))
            elif ansType2 == 2: # 주관식 + 텍스트 답
                sqlStr = """INSERT INTO tblMPIB
                            (filename, problemTypeID, columns, difficulty, ansType, subjAns, subjAnsImageExists, solImageExists)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                cur.execute(sqlStr, (filename, problemTypeID, columnsUsed, diff, ansType, subjAns, False, False))
            else: # 주관식 + 그림 답
                sqlStr = """INSERT INTO tblMPIB
                            (filename, problemTypeID, columns, difficulty, ansType, subjAnsImageExists, solImageExists)
                            VALUES (?, ?, ?, ?, ?, ?, ?)"""
                cur.execute(sqlStr, (filename, problemTypeID, columnsUsed, diff, ansType, True, False))
        else: # 풀이 파일 있음
            if ansType2 == 1: # 객관식
                sqlStr = """INSERT INTO tblMPIB
                            (filename, problemTypeID, columns, difficulty, ansType, objAns, subjAnsImageExists, solImageExists, solColumns)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                cur.execute(sqlStr, (filename, problemTypeID, columnsUsed, diff, ansType, objAns, False, True, solColumnsUsed))
            elif ansType2 == 2: # 주관식 + 텍스트 답
                sqlStr = """INSERT INTO tblMPIB
                            (filename, problemTypeID, columns, difficulty, ansType, subjAns, subjAnsImageExists, solImageExists, solColumns)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                cur.execute(sqlStr, (filename, problemTypeID, columnsUsed, diff, ansType, subjAns, False, True, solColumnsUsed))
            else: # 주관식 + 그림 답
                sqlStr = """INSERT INTO tblMPIB
                            (filename, problemTypeID, columns, difficulty, ansType, subjAnsImageExists, solImageExists, solColumns)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                cur.execute(sqlStr, (filename, problemTypeID, columnsUsed, diff, ansType, True, True, solColumnsUsed))

        conn.commit()
        conn.close()

        # 문제 등록에 성공했음을 알리고 보조 유형을 등록할 것인지 묻는다.
        if messagebox.askyesno("문제 등록 성공", "문제 등록에 성공했습니다.\n보조 유형을 추가하시겠습니까?"):
            win = tk.Toplevel()
            win.title("보조 유형 등록")
            win.grab_set()

            container = MPBAuxProblemTypeRegistration(win, cur.lastrowid)
            container.grid()

        # 초기화
        prob.initialize_image()
        ans.initialize_image()
        ans.txtSubjAns.delete(0, tk.END)
        sol.initialize_image()



if __name__ == '__main__':
    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    #aSource = MPIBSourceTree(root, showID=True)
    #aSource.grid(sticky="nsew")

    #aTree = MPIBCurriTree(root, showID=False)
    #aTree.grid(sticky="nsew")

    #aSelection = MPIBImageSelection(root, useTitle=False, imagePos="w")
    #aSelection.grid(sticky="nsew")

    #test = MPIBColumnsUsedComboBox(root, textAnchor="e", boxPos="e")
    #test = MPIBAnsTypeRadioButton(root, textAnchor="w", radioPos="e")
    #test1 = MPIBObjAnsComboBox(root, textAnchor="e", boxPos="e")
    #test1.grid(sticky="nsew")
    #test2 = MPIBSubjAnsTextBox(root, textAnchor="w", boxPos="n")
    #test2.grid(sticky="nsew")

    #test = MPIBProblemImageSelection(root)
    #test = MPIBAnswerImageSelection(root)
    test = MPIBProblemImageRegistration(root)
    test.grid(row=0, column=0, sticky="nsew")

    root.mainloop()