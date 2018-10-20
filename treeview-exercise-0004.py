from tkinter import *
from tkinter import ttk, filedialog
from PIL import ImageTk, Image, ImageGrab
import sqlite3

LARGE_FONT = ('맑은 고딕', 11)
DEFAULT_BACKGROUND = '.\\coffee.jpeg'

class MPBCurriTreeView(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        
        # 트리에서 선택된 항목의 종류와 ID(기본값)
        self.selectedCurriType = ''
        self.selectedCurriID = 0

        # 트리와 스크롤바를 담기 위한 그릇
        #self.container = ttk.Frame(master, padding=(3,3,12,12))

        #self.lblTitle = Label(self.container, text="<문제 유형 선택>")  # 제목
        self.trvCurri = ttk.Treeview(master, height=20, selectmode='browse')    # 트리 만들기
        #self.treeXScroll = ttk.Scrollbar(self.container, orient=HORIZONTAL)   # 수평 스크롤바 만들기(트리에는 수평 스크롤바가 필요 없는 듯)
        self.treeYScroll = ttk.Scrollbar(master, orient=VERTICAL)   # 수직 스크롤바 만들기
        self.lblSelectedCurriType = Label(master, text='선택한 항목', fg='blue')   # 선택한 항목
        self.lblSelectedCurriID = Label(master, text='항목 번호', fg='blue') # 선택한 항목 ID

        #self.trvCurri.bind('<ButtonRelease-1>', self.doSomething)    # 클릭했을 때 할 일
        self.trvCurri.bind('<<TreeviewSelect>>', self.callback)

        # 수평 스크롤바(불필요한 듯)
        #self.treeXScroll.configure(command=self.trvCurri.yview)
        #self.trvCurri.configure(xscrollcommand=self.treeXScroll.set)

        # 수직 스크롤바
        self.treeYScroll.configure(command=self.trvCurri.xview)
        self.trvCurri.configure(yscrollcommand=self.treeYScroll.set)

        # 그려 넣기
        #self.container.grid(row=row, column=column, sticky=(N, S, E, W)) # 그릇 그려 넣기. 인스턴스를 생성한 곳에서 이 그릇을 넣을 프레임 등(인수로 받음)을 만들어야 한다.
        #self.lblTitle.grid(row=0, column=0, columnspan=4, sticky=W)
        self.trvCurri.grid(row=0, column=0, columnspan=2, sticky=(N, S, E, W))    # 트리를 그릇에 넣기
        #self.trvCurri.pack(side=LEFT)
        #self.treeXScroll.grid(row=1, column=0, columnspan=2, sticky=E+W)  # 수평 스크롤바를 그릇에 넣기
        self.treeYScroll.grid(row=0, column=2, sticky=N+S)  # 수직 스크롤바를 그릇에 넣기
        #self.treeYScroll.pack(side=LEFT)
        self.lblSelectedCurriType.grid(row=1, column=0, sticky=W, padx=10)
        #self.lblSelectedCurriType.pack(side=BOTTOM)
        self.lblSelectedCurriID.grid(row=1, column=1, sticky=E, padx=5)
        #self.lblSelectedCurriID.pack(side=LEFT)

        # Handling Resize
        #self.container.rowconfigure(0, weight=1)
        #self.container.columnconfigure(0, weight=1)

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
    def callback(self, event):
        #print(self.trvCurri.selection())
        #print(self.trvCurri.focus().split('-')[0], self.trvCurri.focus().split('-')[1]) # 처음 것은 book, part, chapter, section, problemType 중 하나, 뒤에 것은 ID
        self.selectedCurriType = self.trvCurri.focus().split('-')[0]
        self.selectedCurriID = self.trvCurri.focus().split('-')[1]
        #print(self.selectedCurriType, self.selectedCurriID)
        #print(self.trvCurri.item(self.trvCurri.focus())['text'])

        # 선택한 항목의 종류 알리기
        #if self.selectedCurriType == 'book':
        #    self.lblSelectedCurriType['text'] = '책'
        #elif self.selectedCurriType == 'part':
        #    self.lblSelectedCurriType['text'] = '부'
        #elif self.selectedCurriType == 'chapter':
        #    self.lblSelectedCurriType['text'] = '장'
        #elif self.selectedCurriType == 'section':
        #    self.lblSelectedCurriType['text'] = '절'
        #elif self.selectedCurriType == 'problemType':
        #    self.lblSelectedCurriType['text'] = '문제 유형'

        # 선택한 항목 알리기
        self.lblSelectedCurriType['text'] = self.trvCurri.item(self.trvCurri.focus())['text']

        # 선택한 항목의 ID 알리기
        self.lblSelectedCurriID['text'] = self.selectedCurriID

    # 임시
    def doSomething(self, event):
        curItem = self.trvCurri.focus()
        print(self.trvCurri.item(curItem)['tags'][0].split('-')[0], self.trvCurri.item(curItem)['tags'][0].split('-')[1])

if __name__ == '__main__':
    root=Tk()
    root.geometry("640x480")
    #root.rowconfigure(0, weight=1)
    #root.columnconfigure(0, weight=1)

    aTree = MPBCurriTreeView(root)
    aTree.grid(row=0, column=0, rowspan=2, columnspan=5)
    #aTree.pack()
    #print(aTree.selectedCurriType, aTree.selectedCurriID)

    #aImageRegistration = MPBProblemImageRegistration(root, row=0, column=1, width=300, height=200)
    #aImageRegistration.grid(row=0, column=1)

    root.mainloop()