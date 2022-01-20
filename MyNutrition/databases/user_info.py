import sqlite3

conn = sqlite3.connect("information.db")

cur = conn.cursor()



conn.execute('CREATE TABLE user_data(name TEXT, age INT, height INT, weight INT, gender TEXT, activity TEXT)')

cur.executemany(
    'INSERT INTO user_data VALUES (?, ?, ?, ?, ?, ?)',
    [('Donghyun', 20, 180, 80, 'male', 'LowActive'),
     ('Seunghyun', 25, 182, 80, 'male', 'HighActive')
    ]
)

conn.commit()
conn.close()