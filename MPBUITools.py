from tkinter import *
from tkinter import ttk
import sqlite3

class MPBCurriTreeView(Frame):

    def __init__(self, master, aRow, aCol):
        Frame.__init__(self, master)
        
        self.container = ttk.Frame(master, padding=(3,3,12,12))

        #self.lblTitle = Label(self.container, text="<문제 유형 선택>")  # 제목
        self.trvCurri = ttk.Treeview(self.container, selectmode='browse')    # 트리 만들기
        self.treeYScroll = ttk.Scrollbar(self.container, orient=VERTICAL)   # 스크롤바 만들기

        self.trvCurri.bind('<ButtonRelease-1>', self.doSomething)    # 클릭했을 때 할 일

        self.treeYScroll.configure(command=self.trvCurri.xview)
        self.trvCurri.configure(yscrollcommand=self.treeYScroll.set)

        self.container.grid(row=aRow, column=aCol, sticky=(N, S, E, W))
        #self.lblTitle.grid(row=0, column=0, columnspan=4, sticky=W)
        self.trvCurri.grid(row=0, column=0, sticky=(N, S, E, W))
        self.treeYScroll.grid(row=0, column=1, sticky=N+S)

        # Handling Resize
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        # Treeview 제목 설정
        self.trvCurri.config(columns=('alive'))
        self.trvCurri.column('alive', width=50, anchor='center')
        self.trvCurri.column('#0', width=300)
        self.trvCurri.heading('alive', text='교육 과정 내인지 여부')

        # 데이타베이스에 연결해서 데이타 가져오기
        conn = sqlite3.connect("mathProblemDB.db")  # SQLite DB에 연결
        cur = conn.cursor() # Connection으로부터 Cursor 생성
        cur.execute("SELECT id, name FROM tblBook ORDER BY priority")   # SQL 실행
        rows = cur.fetchall()   # 데이타 fetch

        # 루트 노드에 책 추가
        for row in rows:
            bookID = str(row[0])
            self.trvCurri.insert('', 'end', 'book' + bookID, text=row[1], tag='book-' + bookID)

            # 책 아래에 파트 추가
            sqlStr = "SELECT id, name FROM tblPart WHERE bookID = " + str(row[0]) + " ORDER BY priority"
            cur.execute(sqlStr)
            secondRows = cur.fetchall()

            for secondRow in secondRows:
                partID = str(secondRow[0])
                self.trvCurri.insert('book' + bookID, 'end', 'part' + partID, text=secondRow[1], tag='part-' + partID)

                # 파트 아래에 장 추가
                sqlStr = "SELECT id, name FROM tblChapter WHERE partID = " + str(secondRow[0]) + " ORDER BY priority"
                cur.execute(sqlStr)
                thirdRows = cur.fetchall()

                for thirdRow in thirdRows:
                    chapterID = str(thirdRow[0])
                    self.trvCurri.insert('part' + partID, 'end', 'chapter' + chapterID, text=thirdRow[1], tag='chapter-' + chapterID)

                    # 장 아래에 절 추가
                    sqlStr = "SELECT id, name FROM tblSection WHERE chapterID = " + str(thirdRow[0]) + " ORDER BY priority"
                    cur.execute(sqlStr)
                    fourthRows = cur.fetchall()

                    for fourthRow in fourthRows:
                        sectionID = str(fourthRow[0])
                        self.trvCurri.insert('chapter' + chapterID, 'end', 'section' + sectionID, text=fourthRow[1], tag='section-' + sectionID)

                        # 절 아래에 절 추가
                        sqlStr = "SELECT id, name, alive FROM tblProblemType WHERE sectionID = " + str(fourthRow[0]) + " ORDER BY priority"
                        cur.execute(sqlStr)
                        fifthRows = cur.fetchall()

                        for fifthRow in fifthRows:
                            problemTypeID = str(fifthRow[0])
                            self.trvCurri.insert('section' + sectionID, 'end', 'problemType' + problemTypeID, text=fifthRow[1], tag='problemType-' + problemTypeID)
                            
                            if fifthRow[2]:
                                self.trvCurri.set('problemType' + problemTypeID, 'alive', 'O')
                            else:
                                self.trvCurri.set('problemType' + problemTypeID, 'alive', 'X')

        conn.close()    # 데이터베이스에 대한 연결 닫기

    def doSomething(self, event):
        curItem = self.trvCurri.focus()
        print(self.trvCurri.item(curItem)['tags'][0].split('-')[0], self.trvCurri.item(curItem)['tags'][0].split('-')[1])

if __name__ == '__main__':
    root=Tk()
    root.geometry("640x480")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    aTree=MPBCurriTreeview(root, 0, 0)

    root.mainloop()