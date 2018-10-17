import sqlite3

# SQLite DB에 연결
conn = sqlite3.connect("mathProblemDB.db")

# Connection으로부터 Cursor 생성
cur = conn.cursor()

# SQL 실행
cur.execute("SELECT * FROM tblBook ORDER BY priority")

# 데이타 fetch
rows = cur.fetchall()

for row in rows:
    print(row)

# Connection 닫기
conn.close()