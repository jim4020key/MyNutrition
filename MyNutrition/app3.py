"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
#from instagram import getfollowedby, getname
import database, sort_by_date, required, short_extra_database,recommend_shop
import mysql_info
from databases import select, show,insert, nutrition_info
import googlevision
import recommend_food
import pandas as pd
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'some_secret'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost:3306/test'
#app.config['SQLALCHEMY_BINDS'] = {'info' : 'sqlite:///info.db'}
db = SQLAlchemy(app)
Bootstrap(app)

class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    def __init__(self, username, password):
        self.username = username
        self.password = password

#class Info(db.model):
   # __bind_key__ = 'info'
   # id = db.Column(db.Integer, primary_key = True)
    #weight = db.Column(db.Integer, unique=True)
    #height = db.Column(db.Integer, unique=True)
    #gender = db.Column(db.String(80), unique=True)
    #age = db.Column(db.String(80), unique=True)
    #activity = db.Column(db.String(80), unique=True)


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            #username = getname(request.form['username'])
            #print(session.get("userID"))
            return render_template('index.html', userID = session.get("userID"))
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                session["userID"] = name
                return redirect(url_for('home'))
            else:
                flash("Login failed!")
                return render_template('login.html')
        except:
            flash("Login failed!")
            return render_template('login.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    try:
        if request.method == 'POST':
            new_user = User(username=request.form['username'], password=request.form['password'])
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html')
    except:
        flash("이미 사용중인 ID입니다!")
        return render_template('register.html')


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.route("/hello")
def hello():
    return render_template("hello.html")


@app.route("/apply")
def apply():
    return render_template("apply.html")


@app.route("/applyphoto")
def photo_apply():
    userID = session.get("userID")
    location = request.args.get("location")
    date = request.args.get("date")
    time = request.args.get("time")
    ocr = request.args.get("ocr")
    #print(location, height, weight, age, sex, time)
    database.save(userID, location, date, time, ocr)
    # location으로 food code 알아내서 food_ratings.csv 업데이트
    nutri_info = nutrition_info.nutrition(location)
    food_code=nutri_info[2]
    idx = len(pd.read_csv("food_ratings.csv", error_bad_lines=False))
    df = pd.DataFrame({"userId":userID,
                       "Food Code":food_code,
                       "rating":1},
                      index = [idx])
    df.to_csv("food_ratings.csv",mode = "a", header = False, index=False)
    return render_template("apply_photo.html")


@app.route("/upload_done", methods=["POST"])
def upload_done():
    uploaded_files = request.files["file"]
    uploaded_files.save("static/img/{}.jpeg".format(database.now_index()))
    return redirect(url_for('ocr_confirm'))

@app.route("/ocr_confirm")
def ocr_confirm():
    import pandas as pd
    user = session.get("userID")
    try:
        photo = f"img/{database.now_index()}.jpeg"
        path = f"static/{photo}"
        df = googlevision.ocr(path)
        return render_template("ocr.html", photo=photo, tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)
    except:
        flash("영양성분표가 인식되지 않습니다.")
        return redirect(url_for("ocr_revise"))

@app.route("/ocr_revise")
def ocr_revise():
    user = session.get("userID")
    try:
        photo = f"img/{database.now_index()}.jpeg"
        path = f"static/{photo}"
        df = googlevision.ocr(path)
        return render_template("ocr_revise.html", photo=photo, tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)
    except:
        return render_template("ocr_revise.html", photo=None)

@app.route("/ocr_revised",methods=['GET','POST'])
def ocr_revised():
    import pandas as pd
    Energy = request.args.get("Energy")
    Protein = request.args.get("Protein")
    Fat = request.args.get("Fat")
    Carbohydrate = request.args.get("Carbohydrate")
    Dietary_Fiber = request.args.get("Dietary_Fiber")
    Calcium = request.args.get("Calcium")
    Iron = request.args.get("Iron")
    Magnesium = request.args.get("Magnesium")
    Phosphorus = request.args.get("Phosphorus")
    Potassium = request.args.get("Potassium")
    Sodium = request.args.get("Sodium")
    Zinc = request.args.get("Zinc")
    Manganese = request.args.get("Manganese")
    Selenium = request.args.get("Selenium")
    Vitamin_B6 = request.args.get("Vitamin_B6")
    Vitamin_E = request.args.get("Vitamin_E")
    Vitamin_K = request.args.get("Vitamin_K")
    Vitamin_B12 = request.args.get("Vitamin_B12")
    Riboflavin = request.args.get("Riboflavin")
    Niacin = request.args.get("Niacin")
    Total_Vitamin_C = request.args.get("Total_Vitamin_C")
    Folate = request.args.get("Folate")
    Vitamin_A = request.args.get("Vitamin_A")
    
    user = session.get("userID")
    house_info = database.load_house(database.now_index())
    location = house_info["location"]
    idx = len(pd.read_csv("labellist.csv", error_bad_lines=False))
    df = pd.DataFrame({"Energy":Energy,
                       "Protein":Protein,
                       "Fat":Fat,
                       "Carbohydrate":Carbohydrate,
                       "Dietary_Fiber":Dietary_Fiber,
                       "Calcium":Calcium,
                       "Iron":Iron,
                       "Magnesium":Magnesium,
                       "Phosphorus":Phosphorus,
                       "Potassium":Potassium,
                       "Sodium":Sodium,
                       "Zinc":Zinc,
                       "Manganese":Manganese,
                       "Selenium":Selenium,
                       "Vitamin_B6":Vitamin_B6,
                       "Vitamin_E":Vitamin_E,
                       "Vitamin_K":Vitamin_K,
                       "Vitamin_B12":Vitamin_B12,
                       "Riboflavin":Riboflavin,
                       "Niacin":Niacin,
                       "Total_Vitamin_C":Total_Vitamin_C,
                       "Folate":Folate,
                       "Vitamin_A":Vitamin_A,
                       "Food_and_Description" : location},
                      index = [idx])
    df.to_csv("labellist.csv",mode = "a", header = False, index=False)
    return redirect(url_for('home'))

@app.route("/ocr_saved")
def ocr_saved():
    import pandas as pd
    user = session.get("userID")
    house_info = database.load_house(database.now_index())
    location = house_info["location"]
    photo = f"img/{database.now_index()}.jpeg"
    path = f"static/{photo}"
    df = googlevision.ocr(path)
    df['Food_and_Description'] = location
    #df.columns = ["Energy", "Protein", "Fat", "Carbohydrate", "Dietary_Fiber", "Calcium", "Iron", "Magnesium", "Phosphorus", "Potassium", "Sodium", "Zinc", "Manganese", "Selenium", "Vitamin_B6", "Vitamin_E", "Vitamin_K", "Vitamin_B12", "Riboflavin", "Niacin", "Total_Vitamin_C", "Folate", "Vitamin_A", "Food_and_Description"]
    df.to_csv("labellist.csv", mode = "a", header = False, index = False)
    #df=pd.read_html(url_for('ocr_revise'))#, header=0, encoding='utf-8')
    #return df
    return redirect(url_for('home'))


@app.route("/list")
def list():
    user = session.get("userID")
    house_list = database.load_list(user = user)
    length = len(house_list)
    user = session.get("userID")
    return render_template("list.html", house_list=house_list, length=length)


@app.route("/house_info/<int:index>/")
def house_info(index):
    house_info = database.load_house(index)
    location = house_info["location"]
    date = house_info["date"]
    time = house_info["time"]
    ocr = house_info["ocr"]
    photo = f"img/{index}.jpeg"
    if ocr == "yes":
        df = pd.read_csv("labellist.csv")
        nutri_df = df[df["Food_and_Description"] == location]
        if len(nutri_df) ==0:
            nutri_info = nutrition_info.nutrition(location)[5:]
        else:
            nutri_info = nutri_df.iloc[-1]
    else:
        nutri_info = nutrition_info.nutrition(location)[5:]
    return render_template("house_info.html", location=location, date=date,
                           time=time, photo=photo, nutri_info = nutri_info)
@app.route("/analysis")
def analysis():
    name = session.get("userID")
    df = sort_by_date.sorting(name)
    datelist = df.date.unique()
    #print("데이트", datelist)
    length = len(datelist)
    return render_template("analysis.html", datelist = datelist, length= length)
@app.route("/day_analysis/<date>")
def day_analysis(date):
    name = session.get("userID")
    df = sort_by_date.sorting(name)
    #date_df = df[ df['date'] == date ]
    df['date'] = df['date'].astype(str)
    date_df = df[ df['date'] == date ]
    print(date_df)
    #print(date_df)
    #date_df = sort_by_date.date_house(df, date)
    food_list = date_df.location.values
    ocr_list = date_df.ocr.values
    print(ocr_list)
    day_nutrition_sum = nutrition_info.nutrition_sum(food_list, ocr_list)
    
    """필요한 nutrition: required.py에서 nutrition함수에서 얻을수 있음
    나이, 키, 몸무게, 성별, 활동량 알아야함.
    information은 select.py에서 할 수 있음. input: 이름 -> 출력-> 이름/나이/키/몸무게/성별/활동량 """
    info = select.person(name)
    if info == None:
        render_template("information.html")
    age = info[1]
    height = info[2] /10
    weight = info[3]
    gender = info[4]
    activity = info[5]
    required_nutrition = required.nutrition(age, weight, height, gender, activity)

    
    """형식 맞추기"""
    required_dict = required.required_dict(required_nutrition)
    
    """short or extra"""
    short, extra, total = required.short_or_extra(day_nutrition_sum, required_dict)
    
    """short extra 데이터베이스 저장"""
    total['date'] = date
    


    test_df = pd.DataFrame(total,
                         index = [name])
    
    required_df = pd.DataFrame(required_dict , index = [name])
    my_df = pd.DataFrame(day_nutrition_sum, index = [name])
    #print("데이터베이스 저장 실험", test_df)
    test_df.to_csv("short2.csv", mode = "a", header = False)
    
    #그래프 그리려는 영양소
    my_list = my_df.values.tolist()[0]
    required_list = required_df.values.tolist()[0]
    nutrition_list = ['Energy', 'Protein', 'Fat', 'Carbohydrate', 'Dietary_Fiber', 'Calcium', 'Iron', 'Magnesium', 'Phosphorus', 'Potassium', 'Sodium', 
                      'Zinc', 'Manganese',  'Selenium', 'Vitamin_B6', 'Vitamin_E', 'Vitamin_K', 'Vitamin_B12', 'Riboflavin', 'Niacin', 'Total_Vitamin_C', 'Folate', 'Vitamin_A']
    nutrition_jason = json.dumps(nutrition_list)
    topid= sorted(range(len(my_list)),key= lambda i: my_list[i])[-5:]
    #return render_template("index2.html")
    return render_template("analysis_report.html", day_nutrition_sum = day_nutrition_sum , required_dict = required_dict, short = short, extra = extra, total = total,
                          my_list = my_list, r_list = required_list, nutrition_jason= nutrition_jason, topid = topid, nutrition_list = nutrition_list)
        
@app.route("/recommend")
def recommend():
    name = session.get("userID")
    df = sort_by_date.sorting(name)
    datelist = df.date.unique()
    #print("데이트", datelist)
    length = len(datelist)
    return render_template("recommend.html", datelist = datelist, length = length)
@app.route("/recommend2/<date>")
def recommend2(date):
    index = session.get("userID")
    df = sort_by_date.sorting2(index)

    date_df = df[ df['date'] == date ]
    nutrition_df = date_df.iloc[-1]
    nutrition = nutrition_df.to_dict()

    keylist = ['Energy', 'Protein', 'Fat', 'Carbohydrate', 'Dietary_Fiber', 'Calcium', 'Iron', 'Magnesium', 'Phosphorus', 'Potassium', 'Sodium', 'Zinc', 'Manganese', 'Selenium', 
    'Vitamin_B6', 'Vitamin_E', 'Vitamin_K', 'Vitamin_B12', 'Riboflavin', 'Niacin', 'Total_Vitamin_C', 'Folate', 'Vitamin_A']
    short_list = []
    #print("nutriiton", nutrition)
    for key in keylist:
        if nutrition[key]>0:
            short_list.append(key)
            
    #food_recommend_list=[]
    #for name in short_list[1:]:
    #    food_recommend_list.append(recommend_food.recommendation(index, name, nutrition[name]))

    return render_template("recommend2.html", nutrition = nutrition, short_list= short_list[1:])

@app.route("/recommend3/<nutri>/<shortage>")
def recommend3(nutri, shortage):
    index = session.get("userID")
    shortage=float(shortage)
    ori_food = pd.read_csv('/workspace/MyNutrition/nutrition2.csv', encoding = 'utf-8', index_col=0)
    ori_ratings = pd.read_csv('/workspace/MyNutrition/food_ratings.csv', encoding = 'utf-8')
    food_recommend_list=recommend_food.recommendation(index, ori_food, ori_ratings, nutri, shortage)
    food_recommend_list2 = []
    for food in food_recommend_list:
        food2= food.split(",")[0]
        food_recommend_list2.append(food2)
    shop_list = []
    for food in food_recommend_list2:
        shop_dict = recommend_shop.shop(food)
    return render_template("recommend3.html", nutri = nutri, food_recommend_list=food_recommend_list, food_recommend_list2 = food_recommend_list2, shop_list = shop_list)

@app.route("/recommend4", methods=["POST","GET"])
def recommend4():
    menu = None
    if request.method == "POST":
        menu = request.form["shop"]
        shop_dict = recommend_shop.shop(menu)
        return render_template("recommend4.html", menu = menu, shop_dict = shop_dict)
    
@app.route("/recommend5<menu>")
def recommend5(menu):
    shop_dict = recommend_shop.shop(menu)
    shop_name = []
    #print(shop_dict)
    name_list = []
    x_list = []
    y_list = []
    comment_list =[]
    url_list =[]
    star_list = []
    for shop in shop_dict:
        name = shop["shop"]
        x = shop["x"]
        y = shop["y"]
        comment = shop["comment"]
        star = shop["star"]
        url = shop["url"]
        name_list.append(name)
        x_list.append(x)
        y_list.append(y)
        comment_list.append(comment)
        star_list.append(star)
        url_list.append(url)


    name_length = len(name_list)

    return render_template("recommend5.html", shop_dict = shop_dict, name_list = name_list, x_list = x_list, y_list = y_list, comment_list = comment_list,
                          star_list = star_list,url_list = url_list, name_length = name_length)

@app.route("/day_info")
def day_info():
    return render_template("day_info.html")
@app.route("/myinfo")
def myinfo():
    name2 = session.get("userID")
    result = select.person(name2)
    length=str(result)
    #print(result)
    return render_template("information.html",result = result,length=length)
    
@app.route("/info_done", methods=["POST","GET"])
def info_done():
    weight = None
    height = None
    age = None
    gender = None
    activity = None
    if request.method == "POST":
        name = session.get("userID")
        weight = request.form["weight"]
        height = request.form["height"]
        age = request.form["age"]
        gender = request.form["gender"]
        activity = request.form["activity"]
        insert.add(name, age, height, weight, gender, activity)
         #location = request.args.get("location")
    #return redirect(url_for("home"))
    return redirect(url_for("home"))

@app.route("/map")
def map():
    return render_template("map2.html")




if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
