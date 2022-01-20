import sqlite3
import pandas as pd
import numpy as np
def nutrition(name2):
    conn = sqlite3.connect("nutri.db")
    cur = conn.cursor()
    sql = '''SELECT * FROM nutri_data WHERE nutri_data.Food_and_Description LIKE '%{0}%' '''.format(name2)
    #'%'+@TEST+'%'
    #print(sql)
    cur.execute(sql)
    result = cur.fetchone()
    if result:
        return result
    else:
        return None
    conn.commit()
    conn.close()
#location = "된장찌개"
#print(nutrition("피자"))

    
def nutrition_sum(food_list, ocr_list):
    nutrition_list = ['Energy','Protein','Fat','Carbohydrate','Dietary_Fiber','Calcium','Iron','Magnesium','Phosphorus','Potassium','Sodium','Zinc','Manganese','Selenium','Vitamin_B6','Vitamin_E','Vitamin_K','Vitamin_B12','Riboflavin','Niacin','Total_Vitamin_C','Folate','Vitamin_A']
    nutri_dict = {}
    for idx, n in enumerate(nutrition_list):
        nutri_dict[n] = 0
    for idx, food in enumerate(food_list):
        if ocr_list[idx] =="yes": #ocr 인식했음
            df =  pd.read_csv("labellist.csv", index_col = None) #ocr 인식하면 labelist에서 데이터가져와야함
            nutri_df =  df[df["Food_and_Description"] == food]
            if len(nutri_df)==0: #ocr 인식했다 했는데 labellist에 데이터가 없는 경우 -> 그냥 nutrition db에서 가져오기.
                nutri_info = nutrition(food)
                if nutri_info != None:
                    start_index= 5 #영양소가 energy 부터 시작하는데 튜플의 index가 5임
                    for n in nutrition_list:
                        nutri_dict[n] += float(nutri_info[start_index])
                        start_index += 1
            else: #ocr 인식했다 했고, labelist에 데이터 있는 경우
                
                nutri_info = nutri_df.iloc[[-1]] #여기서 nutri_info는 데이터프레임 형태임.
                for n in nutrition_list:
                    nutri_dict[n] += nutri_info[n].values[-1]
        else: #ocr 인식 안했음 -> nutrition db에서 영양성분 가져오기
            nutri_info = nutrition(food)
            if nutri_info != None:
                start_index= 5 #영양소가 energy 부터 시작하는데 튜플의 index가 5임
                for n in nutrition_list: #nutrition_list=['Energy','Protein','Fat','Carbohydrate','Dietary_Fiber' .......]
                    nutri_dict[n] += float(nutri_info[start_index])
                    start_index += 1
    return nutri_dict
    #print("최종".nutri_dict)

#nutrition_sum(["우유","김치찌개"])