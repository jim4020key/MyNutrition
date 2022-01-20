import sqlite3
conn = sqlite3.connect("nutrition.db")
cur = conn.cursor()
cur.execute("SELECT * FROM nutrition2")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()
