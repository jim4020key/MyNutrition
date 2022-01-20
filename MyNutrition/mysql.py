import numpy as np 
import pandas as pd
import json
import pymysql
from sqlalchemy import create_engine

meta = pd.read_csv('./nutrition2.csv', encoding = 'utf-8', index_col = 0)
rating = pd.read_csv('./food_ratings.csv', encoding = 'utf-8')
rating['rating']=1
rating.drop('timestamp', axis = 1, inplace = True)

engine = create_engine('mysql+pymysql://user:password@localhost:3306/FOODDB', encoding='utf-8')
conn = engine.connect()
meta.to_sql(name='food', con=engine, index=False, if_exists='replace')
rating.to_sql(name='rating', con=engine, index=False, if_exists='replace')

conn.close()