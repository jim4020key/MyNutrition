"""설명: 특정 name에 대한 가장 최신의 information을 뽑는다. 이름/나이/키/몸무게/성별/활동량"""
import sqlite3

#name3 = "Seunghyun"
def person(name2):
    conn = sqlite3.connect("information.db") 
    cur = conn.cursor()
    sql = '''SELECT * FROM user_data WHERE user_data.name = '{0}' '''.format(name2)
    #sql = '''SELECT * FROM user_data WHERE user_data.name = 'Seunghyun' '''
    cur.execute(sql)
    result = cur.fetchall()
    #print("result", result)
    #print(result[-1])
    if len(result) != 0:
        return result[-1]
    else:
        return None
    conn.commit()
    conn.close()
    
#person(name3)
