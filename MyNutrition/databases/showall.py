"""설명: 현재 등록된 user들의 information을 모두 보여줌"""
import sqlite3
conn = sqlite3.connect("information.db")
cur = conn.cursor()
cur.execute("SELECT * FROM user_data")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()
