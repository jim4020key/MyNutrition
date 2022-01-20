import pandas as pd
import numpy as np
def shop(menu):
    shop_list = []
    df4 = pd.read_csv("yongsan_review_index2.csv", index_col = 0)
    for i in df4.index:
        review = df4.iloc[i]["kakao_blog_review_txt"]
        if menu in review:
            shop = df4.iloc[i]['name']
            x = df4.iloc[i]['lon']
            y = df4.iloc[i]['lat']
            comment = df4.iloc[i]['kakao_blog_review_txt']
            star = df4.iloc[i]['kakao_star_point']
            url = df4.iloc[i]['kakao_map_url']
            if star < 3:
                continue
            shop_dict ={
                "shop"  : shop,
                "x" : x,
                "y" : y,
                "comment" : comment,
                "star" : star,
                "url" : url
            }
            shop_list.append(shop_dict)
    return shop_list[:10]



#print(shop("김치찌개"))
        