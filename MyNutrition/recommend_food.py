import pandas as pd 
import numpy as np
from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds
#from sqlalchemy import create_engine

#ori_food = pd.read_csv('/workspace/MyNutrition/nutrition2.csv', encoding = 'utf-8', index_col=0)
#ori_ratings = pd.read_csv('/workspace/MyNutrition/food_ratings.csv', encoding = 'utf-8')



def recommendation(user_id, ori_food, ori_ratings, nutrient, shortage):
    #engine = create_engine('mysql+pymysql://user:password@localhost:3306/FOODDB', encoding='utf-8')
    #conn = engine.connect()

    #nutrition_data = pd.read_sql_table('food', conn)
    #food_ratings_data = pd.read_sql_table('rating', conn)
    #food_ratings_data.drop('timestamp', axis = 1, inplace = True)

    #nutrition_data = nutrition_data[nutrition_data[name]>=shortage]
    #conn.close()
    
    food=ori_food.loc[:,['Food groups','Food Code','Food_and_Description']]
    new_ratings=ori_ratings.groupby([ori_ratings['userId'],ori_ratings['Food Code']])['rating'].sum().reset_index()

    user_food_data = new_ratings.pivot(
        index='userId',
        columns='Food Code',
        values='rating'
    ).fillna(0)

    matrix=user_food_data.values
    user_ratings_mean=np.mean(matrix, axis=1)
    matrix_user_mean=matrix-user_ratings_mean.reshape(-1,1)

    U, sigma, Vt = svds(matrix_user_mean, k = 5)
    sigma = np.diag(sigma)
    svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns = user_food_data.columns, index=user_food_data.index)
    
    sorted=df_svd_preds.loc[user_id].sort_values(ascending=False)
    user_data=new_ratings[new_ratings['userId'] == user_id]
    user_history=user_data.merge(ori_food, on='Food Code').sort_values(['rating'], ascending=False)

    recommendations = ori_food[~ori_food['Food Code'].isin(user_history['Food Code'])]
    recommendations = recommendations.merge(pd.DataFrame(sorted).reset_index(), on='Food Code')
    recommendations = recommendations.rename(columns={user_id: 'Predictions'}).sort_values(['Predictions'],ascending=False)
        
    nutri_satisfy=recommendations.merge(ori_food, on=['Food groups','Food Code','Food_and_Description'])
    nutrient=nutrient+'_x'
    satisfying_food=nutri_satisfy[nutri_satisfy[nutrient]>shortage][:3]
    food_title=satisfying_food['Food_and_Description']
    food_title_list=list(food_title)
    
    return food_title_list
    