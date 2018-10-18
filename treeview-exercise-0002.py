from tkinter import *
from tkinter import ttk
import sqlite3

# 선택한 항목의 태그를 종류와 ID로 구분하여 출력
def doSomething(a):
    curItem = treeview.focus()
    print(treeview.item(curItem)['tags'][0].split('-')[0], treeview.item(curItem)['tags'][0].split('-')[1])

root = Tk()
root.geometry("640x480")
#root.minsize(width=300, height=400)
#root.resizable(width=0, height=0)

content = ttk.Frame(root, padding=(3,3,12,12))

lblTitle = Label(content, text="<문제 유형 선택>")  # 제목
treeview = ttk.Treeview(content)    # 트리 만들기
treeYScroll = ttk.Scrollbar(content, orient=VERTICAL)   # 스크롤바 만들기

treeview.bind('<ButtonRelease-1>', doSomething)

treeYScroll.configure(command=treeview.xview)
treeview.configure(yscrollcommand=treeYScroll.set)

content.grid(row=0, column=0, sticky=(N, S, E, W))
lblTitle.grid(row=0, column=0, columnspan=4, sticky=W)
treeview.grid(row=1, column=0, columnspan=4, sticky=(N, S, E, W))
treeYScroll.grid(row=1, column=4, sticky=N+S)

# Handling Resize
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
content.rowconfigure(1, weight=1)
content.columnconfigure(1, weight=1)

# Treeview 제목 설정
treeview.config(columns=('alive'))
treeview.column('alive', width=50, anchor='center')
treeview.column('#0', width=300)
treeview.heading('alive', text='교육 과정 내인지 여부')

# 데이타베이스에 연결해서 데이타 가져오기
conn = sqlite3.connect("mathProblemDB.db")  # SQLite DB에 연결
cur = conn.cursor() # Connection으로부터 Cursor 생성
cur.execute("SELECT id, name FROM tblBook ORDER BY priority")   # SQL 실행
rows = cur.fetchall()   # 데이타 fetch

# 루트 노드에 책 추가
for row in rows:
    bookID = str(row[0])
    treeview.insert('', 'end', 'book' + bookID, text=row[1], tag='book-' + bookID)

    # 책 아래에 파트 추가
    sqlStr = "SELECT id, name FROM tblPart WHERE bookID = " + str(row[0]) + " ORDER BY priority"
    cur.execute(sqlStr)
    secondRows = cur.fetchall()

    for secondRow in secondRows:
        partID = str(secondRow[0])
        treeview.insert('book' + bookID, 'end', 'part' + partID, text=secondRow[1], tag='part-' + partID)

        # 파트 아래에 장 추가
        sqlStr = "SELECT id, name FROM tblChapter WHERE partID = " + str(secondRow[0]) + " ORDER BY priority"
        cur.execute(sqlStr)
        thirdRows = cur.fetchall()

        for thirdRow in thirdRows:
            chapterID = str(thirdRow[0])
            treeview.insert('part' + partID, 'end', 'chapter' + chapterID, text=thirdRow[1], tag='chapter-' + chapterID)

            # 장 아래에 절 추가
            sqlStr = "SELECT id, name FROM tblSection WHERE chapterID = " + str(thirdRow[0]) + " ORDER BY priority"
            cur.execute(sqlStr)
            fourthRows = cur.fetchall()

            for fourthRow in fourthRows:
                sectionID = str(fourthRow[0])
                treeview.insert('chapter' + chapterID, 'end', 'section' + sectionID, text=fourthRow[1], tag='section-' + sectionID)

                # 절 아래에 절 추가
                sqlStr = "SELECT id, name, alive FROM tblProblemType WHERE sectionID = " + str(fourthRow[0]) + " ORDER BY priority"
                cur.execute(sqlStr)
                fifthRows = cur.fetchall()

                for fifthRow in fifthRows:
                    problemTypeID = str(fifthRow[0])
                    treeview.insert('section' + sectionID, 'end', 'problemType' + problemTypeID, text=fifthRow[1], tag='problemType-' + problemTypeID)
                    
                    if fifthRow[2]:
                        treeview.set('problemType' + problemTypeID, 'alive', 'O')
                    else:
                        treeview.set('problemType' + problemTypeID, 'alive', 'X')

conn.close()    # 데이터베이스에 대한 연결 닫기

root.mainloop()