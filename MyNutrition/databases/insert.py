import sqlite3

#insert into user_data values ("minji", 21, 167, 52, 'female' , 'low activity');
def add(name, age, height, weight, gender, activity):
    conn = sqlite3.connect("information.db") 
    cur = conn.cursor() 
    #sql = """insert into user_data(name, age, height, weight, gender, activity) values (%s, %s, %s)"""
    cur.execute("insert into user_data VALUES(?,?,?,?,?,?)",(name, age, height, weight, gender, activity))
                                                                        
    #cur.execute(sql, (name, age, height, weight, gender, activity))
    conn.commit()
    conn.close()
    return None
  
#name2 = "hayoon"
#age2 = 24
#height2 = 165
#weight2 = 50
#gender2 = "female"
#activity2 = "active"
#add(name2, age2, height2, weight2, gender2, activity2)