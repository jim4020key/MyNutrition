import sqlite3

def nutrition(name2):
    conn = sqlite3.connect("nutrition.db")
    cur = conn.cursor()
    #sql = '''SELECT * FROM nutrition2 WHERE nutrition2.Food_and_Description LIKE '%{0}%' '''.format(name2)
    #sql = '''SELECT * FROM nutrition2 WHERE nutrition2.Food_and_Description = '{0}' '''.format(name2)
    #sql = '''SELECT * FROM user_data WHERE user_data.name = '{0}' '''.format(name2)
    sql = '''SELECT * FROM nutrition2 '''
    print(sql)
    cur.execute(sql)
    result = cur.fetchone()
    if result:
        return result
    else:
        return None
    conn.commit()
    conn.close()

print(nutrition("김치찌개"))