"""해당 유저의 데이터를 데이터별로 정렬하는 함수"""

import pandas as pd



def sorting(name):
    df = pd.read_csv("database.csv")
    df2 = df[df["userID"]==name]
    df2['date'] =pd.to_datetime(df2.date)
    df2 = df2.sort_values(by= 'date')
    df2['date'] = df2['date'].dt.date
    return df2

def sorting2(name):
    df = pd.read_csv("short2.csv")
    df2 = df[df["index"]==name]
    #df2['date'] =pd.to_datetime(df2.date)
    #df2 = df2.sort_values(by= 'date')
    #df2['date'] = df2['date'].dt.date
    return df2

def date_house(df, date):
    date_df = df[ df['date'] == date ]
    return date_df

#df = sorting("minsu")
#print(df)
#datelist = df.date.unique()
#for date in datelist:
#    d =date_house(df, date)
#    print(date, d)


#print(df.iloc[0]['date'])
#print(sorting(name2))
#df['date'] =pd.to_datetime(df.date)
#print( df.sort_values(by='date'))